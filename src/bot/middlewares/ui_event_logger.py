import time
import asyncio
import logging
from typing import Dict, Any, Optional, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.core.audit.db import audit_db

log = logging.getLogger("mindforge.middleware.ui")

# In-memory lock: (user_id, action, state)
_ui_locks: Dict[tuple, float] = {}
LOCK_TIMEOUT = 30  # секунд


class UIButtonLoggerMiddleware(BaseMiddleware):
    """
    UI Governance Middleware
    - предотвращает дублирующие клики
    - логирует ВСЕ события через Audit Ledger
    - не имеет прямого доступа к БД
    """

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:

        if not isinstance(event, CallbackQuery) or not event.data:
            return await handler(event, data)

        user = event.from_user
        action = event.data

        # FSM
        state: Optional[FSMContext] = data.get("state")
        state_name = None
        session_id = None

        if state:
            try:
                state_name = await state.get_state()
                fsm_data = await state.get_data()
                session_id = fsm_data.get("session_id")
            except Exception:
                pass

        # Если нет сессии — НЕ логируем (fail-safe)
        if not session_id:
            return await handler(event, data)

        lock_key = (user.id, action, state_name)
        now = time.time()

        # ==================================================
        # УРОВЕНЬ 1 — БЛОК ДУБЛИРУЮЩИХ КЛИКОВ
        # ==================================================
        if lock_key in _ui_locks:
            elapsed = now - _ui_locks[lock_key]
            if elapsed < LOCK_TIMEOUT:
                # 🧾 AUDIT: POLICY DENY
                audit_db.log_event(
                    session_id=session_id,
                    user_id=user.id,
                    username=user.username or "",
                    event_type="POLICY",
                    action=action,
                    state=state_name,
                    decision="DENY",
                    policy="UI_LOCK",
                    source="MIDDLEWARE",
                    payload={
                        "reason": "duplicate_click",
                        "cooldown_left": round(LOCK_TIMEOUT - elapsed, 1),
                    },
                )

                await event.answer(
                    "⛔ Действие уже выполняется.\n\n"
                    "Подождите, пока текущая операция не завершится.",
                    show_alert=True,
                )

                log.warning(
                    "UI_LOCK_BLOCKED | user=%s | action=%s | state=%s",
                    user.id,
                    action,
                    state_name,
                )
                return

        # Устанавливаем lock
        _ui_locks[lock_key] = now

        try:
            # 🧾 AUDIT: UI_EVENT
            audit_db.log_event(
                session_id=session_id,
                user_id=user.id,
                username=user.username or "",
                event_type="UI_EVENT",
                action=action,
                state=state_name,
                decision="INFO",
                policy="UAG",
                source="UI-CALLBACK",
                payload={},
            )

            # Выполняем handler
            return await handler(event, data)

        finally:
            # ==================================================
            # УРОВЕНЬ 2 — ОТЛОЖЕННЫЙ UNLOCK
            # ==================================================
            async def _delayed_unlock():
                await asyncio.sleep(2)
                _ui_locks.pop(lock_key, None)

            asyncio.create_task(_delayed_unlock())


def clear_ui_lock(user_id: Optional[int] = None, action: Optional[str] = None):
    """Административная очистка UI-locks"""
    if user_id is None:
        _ui_locks.clear()
        return

    keys = [
        k for k in _ui_locks.keys()
        if k[0] == user_id and (action is None or k[1] == action)
    ]
    for k in keys:
        _ui_locks.pop(k, None)
