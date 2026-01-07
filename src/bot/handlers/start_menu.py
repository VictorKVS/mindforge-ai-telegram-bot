import logging

from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.states.demo_states import DemoStates
from src.core.audit.db import audit_db

log = logging.getLogger("mindforge.handlers.start_menu")

router = Router()


# =========================================================
# /start — точка входа в UAG-сессию
# =========================================================
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user

    log.info(
        "CMD_START | user_id=%s | username=%s | chat_id=%s",
        user.id,
        user.username,
        message.chat.id,
    )

    # FSM reset
    await state.clear()

    # 🔐 START GOVERNANCE SESSION
    session_id = audit_db.start_session(
        user_id=user.id,
        username=user.username or "",
        mode="DEMO",
        trust_level=0,
        state="start_menu",
    )

    # сохраняем session_id в FSM
    await state.update_data(session_id=session_id)

    # 🧾 AUDIT: UI_EVENT
    audit_db.log_event(
        session_id=session_id,
        user_id=user.id,
        username=user.username or "",
        event_type="UI_EVENT",
        action="start",
        state="start_menu",
        decision="INFO",
        policy="DEMO",
        source="UI",
        payload={"cmd": "/start"},
    )

    await message.answer(
        "🧠 *MindForge DEMO*\n\n"
        "Управляемые AI-агенты.\n"
        "Без магии. Без автономии.\n\n"
        "_Демо ~2 минуты_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="▶️ Начать DEMO",
                        callback_data="demo_start",
                    )
                ]
            ]
        ),
    )


# =========================================================
# DEMO → Dashboard
# =========================================================
@router.callback_query(F.data == "demo_start")
async def demo_start_callback(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    session_id = data.get("session_id")

    user = call.from_user

    # FSM
    await state.set_state(DemoStates.dashboard)

    # обновляем состояние сессии
    if session_id:
        audit_db.update_state(session_id, "dashboard")

        # 🧾 AUDIT: FSM transition
        audit_db.log_event(
            session_id=session_id,
            user_id=user.id,
            username=user.username or "",
            event_type="FSM",
            action="enter_dashboard",
            state="dashboard",
            decision="INFO",
            policy="TRUST",
            source="FSM-DEMO",
            payload={
                "state": "dashboard",
                "trust_check": "passed",
            },
        )

    log.info(
        "DEMO | dashboard | user:%s | enter_dashboard | TRUST_LEVEL_CHECK | ADR-0002",
        user.id,
    )

    await call.message.edit_text(
        "⚙️ *ЦЕНТР УПРАВЛЕНИЯ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👨‍🏫 Агент-Учитель — 🟢 Онлайн | Trust 6/6\n"
        "👷 Агент-Строитель — 🟡 Free | Trust 3/6\n\n"
        "_Выберите действие:_",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔓 Активировать PRO",
                        callback_data="demo_activate_pro",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Уровни доверия",
                        callback_data="demo_trust_info",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="▶️ Продолжить DEMO",
                        callback_data="demo_continue",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔍 ПОЧЕМУ ТАК (UAG)",
                        callback_data="why_dashboard",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏪ Session Replay",
                        callback_data="session_replay",
                    )
                ],
            ]
        ),
    )
