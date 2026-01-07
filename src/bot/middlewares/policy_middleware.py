import logging
from typing import Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.core.policy import policy_engine
from src.core.policy.context import PolicyContext

log = logging.getLogger("mindforge.policy.middleware")


class PolicyMiddleware(BaseMiddleware):
    """
    AG-7.1
    Глобальный Policy Enforcement Middleware
    """

    async def __call__(self, handler, event, data: Dict[str, Any]):
        # --- интересуют только пользовательские события ---
        if not isinstance(event, (CallbackQuery, Message)):
            return await handler(event, data)

        user = event.from_user
        if not user:
            return await handler(event, data)

        # --- FSM ---
        state: FSMContext | None = data.get("state")
        state_name = await state.get_state() if state else None

        # --- session_id из FSM ---
        session_id = None
        if state:
            fsm_data = await state.get_data()
            session_id = fsm_data.get("session_id")

        # если нет сессии — policy не применяем
        if not session_id:
            return await handler(event, data)

        # --- определяем action ---
        if isinstance(event, CallbackQuery):
            action = event.data
        elif isinstance(event, Message):
            action = event.text or "message"
        else:
            action = "unknown"

        # --- контекст политики ---
        ctx = PolicyContext(
            session_id=session_id,
            user_id=user.id,
            username=user.username or "",
            action=action,
            state=state_name,
            mode="DEMO",          # позже будет из сессии
            trust_level=0,        # AG-8
            payload={},
        )

        # --- POLICY EVALUATION ---
        decision = policy_engine.evaluate(
            session_id=ctx.session_id,
            user_id=ctx.user_id,
            username=ctx.username,
            action=ctx.action,
            state=ctx.state,
            mode=ctx.mode,
            trust_level=ctx.trust_level,
            payload=ctx.payload,
        )

        log.info(
            "POLICY_CHECK | action=%s | decision=%s | rule=%s",
            ctx.action,
            decision.decision,
            decision.rule_id,
        )

        # --- DENY → стоп ---
        if decision.decision == "DENY":
            await event.answer(
                f"⛔ *ДЕЙСТВИЕ ЗАБЛОКИРОВАНО*\n\n{decision.message}",
                parse_mode="Markdown",
                show_alert=True if isinstance(event, CallbackQuery) else False,
            )
            return  # ❌ handler НЕ вызывается

        # --- INFO → просто идём дальше ---
        return await handler(event, data)
