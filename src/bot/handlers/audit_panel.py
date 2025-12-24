"""
File: I:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\audit_panel.py

Purpose:
Audit / Security panel for MindForge Telegram DEMO.

Responsibilities:
- Show audit log entries (ALLOW / DENY decisions)
- Demonstrate UAG-style decision traceability
- NO business logic here (UI only)

This handler reads data from core.audit_log
and presents it in a human-readable form.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.audit_log import get_last_events

router = Router()

# -------------------------
# Callback IDs
# -------------------------
CB_AUDIT_PANEL = "panel:audit"
CB_AUDIT_REFRESH = "panel:audit:refresh"
CB_BACK_TO_MAIN = "panel:back"


# -------------------------
# Keyboards
# -------------------------
def audit_panel_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔄 Обновить", callback_data=CB_AUDIT_REFRESH)
    kb.button(text="⬅ Назад", callback_data=CB_BACK_TO_MAIN)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------
# Helpers
# -------------------------
def render_audit_events(events: list[dict]) -> str:
    """
    Render audit events into markdown text.
    """
    if not events:
        return "_Журнал пуст. Действия ещё не выполнялись._"

    lines = []
    for e in events:
        status_icon = "✅" if e["decision"] == "ALLOW" else "❌"

        lines.append(
            f"{status_icon} *{e['decision']}*\n"
            f"• Action: `{e['action']}`\n"
            f"• Policy: `{e['policy']}`\n"
            f"• Time: `{e['timestamp']}`"
        )

    return "\n\n".join(lines)


# -------------------------
# Handlers
# -------------------------
@router.callback_query(F.data == CB_AUDIT_PANEL)
async def open_audit_panel(callback: CallbackQuery):
    """
    Open audit panel.
    """
    events = get_last_events(limit=5)

    text = (
        "🛡 *Security / Audit Panel*\n\n"
        "Последние решения UAG:\n\n"
        f"{render_audit_events(events)}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=audit_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == CB_AUDIT_REFRESH)
async def refresh_audit_panel(callback: CallbackQuery):
    """
    Refresh audit panel content.
    """
    events = get_last_events(limit=5)

    text = (
        "🛡 *Security / Audit Panel*\n\n"
        "Последние решения UAG:\n\n"
        f"{render_audit_events(events)}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=audit_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()
