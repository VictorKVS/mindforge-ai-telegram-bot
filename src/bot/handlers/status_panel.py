# src/bot/handlers/status_panel.py
"""
File: src/bot/handlers/status_panel.py

Purpose:
System status panel for MindForge DEMO.

Responsibilities:
- Display registered agents and their roles
- Show ONLINE / OFFLINE state per agent
- Display environment and policy mode
- Read-only UI (no control logic)

This panel demonstrates observability
and is the base for future dashboards.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.agents.registry import REGISTRY
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
def render_agents_block() -> str:
    """
    Render agent list from AgentRegistry.
    """
    agents = REGISTRY.list_agents()

    if not agents:
        return "_Агенты не зарегистрированы._"

    lines = []
    for agent in agents:
        status_icon = "🟢" if agent["is_running"] else "🔴"
        status_text = "ONLINE" if agent["is_running"] else "OFFLINE"

        lines.append(
            f"{status_icon} *{agent['agent_id']}*\n"
            f"• Role: `{agent['role']}`\n"
            f"• Status: `{status_text}`"
        )

    return "\n\n".join(lines)


def render_status_text() -> str:
    """
    Build full system status text.
    """
    agents_count = REGISTRY.count()
    env = settings.APP_ENV.upper()
    policy = settings.DEFAULT_POLICY_MODE

    return (
        "📊 *System Status*\n\n"
        f"🤖 Registered agents: `{agents_count}`\n"
        f"🌍 Environment: `{env}`\n"
        f"🛡 Policy mode: `{policy}`\n\n"
        "— — —\n\n"
        f"{render_agents_block()}\n\n"
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
    text = render_status_text()

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
    text = render_status_text()

    await callback.message.edit_text(
        text,
        reply_markup=status_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()
