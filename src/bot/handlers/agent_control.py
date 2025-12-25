"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\agent_control.py

Purpose:
Agent control panel for MindForge DEMO.

Responsibilities:
- Enable / disable agent runtime
- Write control actions to audit log
- Provide immediate UI feedback

This handler performs ONLY control-plane actions.
No business logic, no policy decisions.
"""


from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.runtime_state import STATE
from src.core.audit_log import record_event
from src.core.logger import logger

router = Router()

# -------------------------
# Callback IDs
# -------------------------
CB_AGENT_ON = "agent:on"
CB_AGENT_OFF = "agent:off"
CB_BACK_TO_MAIN = "panel:back"


# -------------------------
# Keyboards
# -------------------------
def agent_control_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="▶ Включить агента", callback_data=CB_AGENT_ON)
    kb.button(text="⏹ Остановить агента", callback_data=CB_AGENT_OFF)
    kb.button(text="⬅ Назад", callback_data=CB_BACK_TO_MAIN)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------
# Handlers
# -------------------------
@router.callback_query(F.data == CB_AGENT_ON)
async def handle_agent_on(callback: CallbackQuery):
    """
    Enable agent runtime.
    """
    await STATE.set_agent_enabled(True)

    record_event(
        action="agent_enable",
        decision="ALLOW",
        policy="CONTROL_PLANE",
        reason="Agent enabled by operator",
    )

    text = (
        "▶ *Агент включён*\n\n"
        "Runtime агента активирован.\n"
        "Политики будут применяться согласно текущему режиму."
    )

    await callback.message.edit_text(
        text,
        reply_markup=agent_control_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Агент включён")


@router.callback_query(F.data == CB_AGENT_OFF)
async def handle_agent_off(callback: CallbackQuery):
    """
    Disable agent runtime.
    """
    await STATE.set_agent_enabled(False)

    record_event(
        action="agent_disable",
        decision="DENY",
        policy="CONTROL_PLANE",
        reason="Agent disabled by operator",
    )

    text = (
        "⏹ *Агент остановлен*\n\n"
        "Все действия агента заблокированы.\n"
        "Попытки выполнения будут отклоняться политикой."
    )

    await callback.message.edit_text(
        text,
        reply_markup=agent_control_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Агент остановлен")
@router.callback_query(F.data == CB_AGENT_ON)
async def handle_agent_on(callback: CallbackQuery):
    logger.info(
        f"AGENT_CONTROL ENABLE "
        f"user_id={callback.from_user.id}"
    )

    await STATE.set_agent_enabled(True)

    record_event(
        action="agent_enable",
        decision="ALLOW",
        policy="CONTROL_PLANE",
        reason="Agent enabled by operator",
    )
