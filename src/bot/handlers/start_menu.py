# src/bot/handlers/start_menu.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\start_menu.py

Purpose:
Start menu (main control panel) for MindForge Telegram bot.

Responsibilities:
- Show main control buttons
- Route DEMO actions (ALLOW / DENY)
- Write audit records for each decision
- Delegate business logic to core.demo_actions

This file contains ONLY Telegram UI logic.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.core.audit_log import record_event, get_events
from src.core.runtime_state import STATE


from src.core.demo_actions import (
    demo_allowed_action,
    demo_forbidden_action,
)
from src.core.audit_log import record_event

router = Router()

# -------------------------
# Callback IDs
# -------------------------
CB_DEMO_ALLOW = "demo:allow"
CB_DEMO_DENY = "demo:deny"
CB_AUDIT_PANEL = "panel:audit"
CB_POLICY_STRICT = "policy:STRICT"
CB_POLICY_DEMO = "policy:DEMO"
CB_POLICY_OFF = "policy:OFF"



# -------------------------
# Keyboards
# -------------------------
def main_menu_keyboard():
    """
    Build main control panel keyboard.
    """
    kb = InlineKeyboardBuilder()

    kb.button(text="▶ Включить агента", callback_data="agent:on")
    kb.button(text="⏹ Остановить агента", callback_data="agent:off")

    kb.button(text="🛡 Панель безопасности", callback_data="panel:audit")
    kb.button(text="🔄 Панель взаимодействия", callback_data="panel:interaction")

    kb.button(text="📊 Статус системы", callback_data="panel:status")
    kb.button(text="📜 Audit log (последние решения)", callback_data=CB_AUDIT_PANEL)
   


    # DEMO buttons
    kb.button(text="✅ DEMO: Разрешённое действие", callback_data=CB_DEMO_ALLOW)
    kb.button(text="❌ DEMO: Запрещённое действие", callback_data=CB_DEMO_DENY)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------
# Handlers
# -------------------------
@router.message(F.text == "/start")
async def start_menu(message: Message):
    """
    Entry point for the bot.
    Shows the main control panel.
    """
    await message.answer(
        "🧠 *MindForge Control Panel*\n\n"
        "Выберите действие:",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == CB_DEMO_ALLOW)
async def handle_demo_allow(callback: CallbackQuery):
    """
    Handle DEMO allowed action.
    """
    result = await demo_allowed_action()

    if result["status"] == "ALLOW":
        record_event(
            action="demo_allowed_action",
            decision="ALLOW",
        )

        text = (
            "✅ *DEMO: Действие разрешено*\n\n"
            f"Результат:\n`{result['result']}`"
        )
    else:
        record_event(
            action="demo_allowed_action",
            decision="DENY",
            policy=result["policy"],
            reason=result["reason"],
        )

        text = (
            "❌ *DEMO: Действие отклонено*\n\n"
            f"Причина: `{result['reason']}`\n"
            f"Policy: `{result['policy']}`"
        )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == CB_DEMO_DENY)
async def handle_demo_deny(callback: CallbackQuery):
    """
    Handle DEMO forbidden action.
    """
    result = await demo_forbidden_action()

    record_event(
        action="demo_forbidden_action",
        decision="DENY",
        policy=result["policy"],
        reason=result["reason"],
    )

    text = (
        "❌ *DEMO: Действие отклонено*\n\n"
        f"Причина: `{result['reason']}`\n"
        f"Policy: `{result['policy']}`\n\n"
        "💡 Это демонстрация срабатывания UAG-политики."
    )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data == CB_AUDIT_PANEL)
async def handle_audit_panel(callback: CallbackQuery):
    """
    Show last audit events.
    """
    events = get_events(limit=5)

    if not events:
        text = (
            "📜 *Audit log*\n\n"
            "Записей пока нет."
        )
    else:
        lines = []
        for e in events:
            line = (
                f"• `{e['timestamp_utc']}`\n"
                f"  action: `{e['action']}`\n"
                f"  decision: *{e['decision']}*"
            )
            if e.get("policy"):
                line += f"\n  policy: `{e['policy']}`"
            if e.get("reason"):
                line += f"\n  reason: `{e['reason']}`"
            lines.append(line)

        text = (
            "📜 *Audit log (последние решения)*\n\n"
            + "\n\n".join(lines)
        )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


def policy_panel_keyboard():
    """
    Build policy mode control keyboard.
    """
    kb = InlineKeyboardBuilder()

    kb.button(text="🔒 STRICT", callback_data=CB_POLICY_STRICT)
    kb.button(text="🧪 DEMO", callback_data=CB_POLICY_DEMO)
    kb.button(text="⚠ OFF", callback_data=CB_POLICY_OFF)

    kb.button(text="⬅ Назад", callback_data="nav:home")

    kb.adjust(3, 1)
    return kb.as_markup()



@router.callback_query(F.data == "panel:security")
async def handle_security_panel(callback: CallbackQuery):
    """
    Show policy control panel.
    """
    snap = await STATE.snapshot()

    text = (
        "🛡 *Панель безопасности*\n\n"
        f"Текущий режим политики: `{snap['policy_mode']}`\n\n"
        "Выберите режим:"
    )

    await callback.message.edit_text(
        text,
        reply_markup=policy_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data.startswith("policy:"))
async def handle_policy_switch(callback: CallbackQuery):
    """
    Switch policy mode (STRICT / DEMO / OFF).
    """
    mode = callback.data.split("policy:", 1)[1]

    await STATE.set_policy_mode(mode)

    text = (
        "🛡 *Панель безопасности*\n\n"
        f"✅ Режим политики установлен: `{mode}`"
    )

    await callback.message.edit_text(
        text,
        reply_markup=policy_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()

@router.callback_query(F.data == "nav:home")
async def handle_nav_home(callback: CallbackQuery):
    """
    Return to main menu.
    """
    await callback.message.edit_text(
        "🧠 *MindForge Control Panel*\n\n"
        "Выберите действие:",
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()



