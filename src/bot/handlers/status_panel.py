"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\status_panel.py

Purpose:
System status panel for MindForge DEMO.

Responsibilities:
- Display current runtime state (agent, policy mode)
- Display environment (DEMO / PROD)
- Display audit statistics
- NO business logic (read-only UI)

This panel is used to demonstrate
observability and control transparency.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.runtime_state import STATE
from src.core.audit_log import get_events
from src.bot.config import settings

router = Router()

# -------------------------
# Callback IDs
# -------------------------
CB_STATUS_PANEL = "panel:status"
CB_STATUS_REFRESH = "panel:status:refresh"
CB_BACK_TO_MAIN = "panel:back"


# -------------------------
# Keyboards
# -------------------------
def status_panel_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔄 Обновить", callback_data=CB_STATUS_REFRESH)
    kb.button(text="⬅ Назад", callback_data=CB_BACK_TO_MAIN)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------
# Helpers
# -------------------------
async def render_status_text() -> str:
    """
    Build system status text.
    """
    snap = await STATE.snapshot()
    events = get_events(limit=100)

    agent_status = "🟢 ENABLED" if snap["agent_enabled"] else "🔴 DISABLED"
    policy_mode = snap["policy_mode"]
    env = settings.APP_ENV.upper()

    return (
        "📊 *System Status*\n\n"
        f"🧠 Agent: {agent_status}\n"
        f"🛡 Policy mode: `{policy_mode}`\n"
        f"🌍 Environment: `{env}`\n\n"
        f"🧾 Audit events: `{len(events)}`\n\n"
        "_This panel is read-only._"
    )


# -------------------------
# Handlers
# -------------------------
@router.callback_query(F.data == CB_STATUS_PANEL)
async def open_status_panel(callback: CallbackQuery):
    """
    Open system status panel.
    """
    text = await render_status_text()

    await callback.message.edit_text(
        text,
        reply_markup=status_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == CB_STATUS_REFRESH)
async def refresh_status_panel(callback: CallbackQuery):
    """
    Refresh system status panel.
    """
    text = await render_status_text()

    await callback.message.edit_text(
        text,
        reply_markup=status_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()
