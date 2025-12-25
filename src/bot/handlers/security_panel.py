# src/bot/handlers/security_panel.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\security_panel.py

Purpose:
Security / Policy control panel for MindForge DEMO.

Responsibilities:
- Display current policy mode
- Allow switching policy mode (STRICT / DEMO / OFF)
- Write control-plane actions to audit log
- NO business logic (no decisions, no enforcement)

Design notes:
- "+" prefix indicates active / available controls
- This panel demonstrates governance & control transparency
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.runtime_state import STATE
from src.core.audit_log import record_event
from src.bot.config import settings

router = Router()

# -------------------------------------------------
# Callback IDs
# -------------------------------------------------
CB_POLICY_STRICT = "policy:strict"
CB_POLICY_DEMO = "policy:demo"
CB_POLICY_OFF = "policy:off"

CB_BACK_TO_MAIN = "panel:back"


# -------------------------------------------------
# Keyboards
# -------------------------------------------------
async def security_panel_keyboard():
    """
    Build policy control keyboard.

    Current policy mode is visually highlighted.
    """
    snap = await STATE.snapshot()
    current = snap["policy_mode"]

    kb = InlineKeyboardBuilder()

    def label(mode: str, title: str) -> str:
        return f"+ 🔘 {title}" if current == mode else f"+ ⚪ {title}"

    kb.button(
        text=label("STRICT", "STRICT — Максимальная защита"),
        callback_data=CB_POLICY_STRICT,
    )
    kb.button(
        text=label("DEMO", "DEMO — Демонстрационный режим"),
        callback_data=CB_POLICY_DEMO,
    )
    kb.button(
        text=label("OFF", "OFF — Политики отключены"),
        callback_data=CB_POLICY_OFF,
    )

    kb.button(text="+ ⬅ Назад в Control Panel", callback_data=CB_BACK_TO_MAIN)

    kb.adjust(1)
    return kb.as_markup()


# -------------------------------------------------
# Text builder
# -------------------------------------------------
async def build_security_text() -> str:
    """
    Build security panel text.
    """
    snap = await STATE.snapshot()

    return (
        "🛡 *Security / Policy Control Panel*\n\n"
        f"+ 🌍 Environment: `{settings.APP_ENV.upper()}`\n"
        f"+ 🛡 Current policy mode: `{snap['policy_mode']}`\n\n"
        "Выберите режим политик:\n"
        "_(изменения применяются мгновенно)_"
    )


# -------------------------------------------------
# Handlers
# -------------------------------------------------
@router.callback_query(F.data == "panel:audit")
async def open_security_panel(callback: CallbackQuery):
    """
    Open security / policy panel.
    """
    await callback.message.edit_text(
        await build_security_text(),
        reply_markup=await security_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == CB_POLICY_STRICT)
async def set_policy_strict(callback: CallbackQuery):
    await STATE.set_policy_mode("STRICT")

    record_event(
        action="policy_switch",
        decision="ALLOW",
        policy="CONTROL_PLANE",
        reason="Policy mode switched to STRICT by operator",
    )

    await callback.message.edit_text(
        await build_security_text(),
        reply_markup=await security_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Policy mode: STRICT")


@router.callback_query(F.data == CB_POLICY_DEMO)
async def set_policy_demo(callback: CallbackQuery):
    await STATE.set_policy_mode("DEMO")

    record_event(
        action="policy_switch",
        decision="ALLOW",
        policy="CONTROL_PLANE",
        reason="Policy mode switched to DEMO by operator",
    )

    await callback.message.edit_text(
        await build_security_text(),
        reply_markup=await security_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Policy mode: DEMO")


@router.callback_query(F.data == CB_POLICY_OFF)
async def set_policy_off(callback: CallbackQuery):
    await STATE.set_policy_mode("OFF")

    record_event(
        action="policy_switch",
        decision="ALLOW",
        policy="CONTROL_PLANE",
        reason="Policy mode switched to OFF by operator",
    )

    await callback.message.edit_text(
        await build_security_text(),
        reply_markup=await security_panel_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer("Policy mode: OFF")
