# src/bot/handlers/agent_control.py
"""
File: src/bot/handlers/agent_control.py

Purpose:
Agent control panel for MindForge DEMO.

Responsibilities:
- Start / stop real agents via AgentRegistry
- Write control actions to audit log
- Provide immediate UI feedback

This handler performs ONLY control-plane actions.
No business logic, no policies, no LLM calls.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.agents.registry import REGISTRY

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

    kb.button(text="▶ Включить агентов", callback_data=CB_AGENT_ON)
    kb.button(text="⏹ Остановить агентов", callback_data=CB_AGENT_OFF)
    kb.button(text="⬅ Назад", callback_data=CB_BACK_TO_MAIN)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------
# Handlers
# -------------------------
@router.callback_query(F.data == CB_AGENT_ON)
async def handle_agent_on(callback: CallbackQuery):
    """
    Start all registered agents.
    """
    REGISTRY.start_all()

    count = REGISTRY.count()

    text = (
        "▶ *Агенты запущены*\n\n"
        f"Активных агентов: `{count}`\n\n"
        "_Все агенты переведены в ONLINE._"
    )

    await callback.message.edit_text(
        text,
        reply_markup=agent_control_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Агенты запущены")


@router.callback_query(F.data == CB_AGENT_OFF)
async def handle_agent_off(callback: CallbackQuery):
    """
    Stop all registered agents.
    """
    REGISTRY.stop_all()

    count = REGISTRY.count()

    text = (
        "⏹ *Агенты остановлены*\n\n"
        f"Всего агентов: `{count}`\n\n"
        "_Все агенты переведены в OFFLINE._"
    )

    await callback.message.edit_text(
        text,
        reply_markup=agent_control_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Агенты остановлены")
