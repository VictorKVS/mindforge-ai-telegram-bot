# src/bot/handlers/start_menu.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\handlers\\start_menu.py

Purpose:
Main start menu (Control Panel) for MindForge Telegram DEMO.

Responsibilities:
- Display main control sections
- Respect feature flags from config
- Provide a clear, product-style UI
- Route navigation ONLY (no business logic)

Design notes:
- "+" prefix indicates available / enabled functionality
- UI is structured as a control panel, not a chat
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.config import settings

router = Router()

# -------------------------------------------------
# Callback IDs
# -------------------------------------------------
CB_AGENT_ON = "agent:on"
CB_AGENT_OFF = "agent:off"

CB_AUDIT_PANEL = "panel:audit"
CB_STATUS_PANEL = "panel:status"

CB_BACK_TO_MAIN = "panel:back"


# -------------------------------------------------
# Keyboards
# -------------------------------------------------
def main_menu_keyboard():
    """
    Build the main control panel keyboard.

    "+" prefix visually indicates enabled / available modules.
    """
    kb = InlineKeyboardBuilder()

    # --- Agent Control ---
    if settings.FEATURE_AGENT_CONTROL:
        kb.button(
            text="+ ▶ Включить агента",
            callback_data=CB_AGENT_ON,
        )
        kb.button(
            text="+ ⏹ Остановить агента",
            callback_data=CB_AGENT_OFF,
        )

    # --- Security / Audit ---
    if settings.FEATURE_AUDIT_PANEL:
        kb.button(
            text="+ 🛡 Панель безопасности / аудит",
            callback_data=CB_AUDIT_PANEL,
        )

    # --- System Status ---
    if settings.FEATURE_STATUS_PANEL:
        kb.button(
            text="+ 📊 Статус системы",
            callback_data=CB_STATUS_PANEL,
        )

    kb.adjust(1)
    return kb.as_markup()


# -------------------------------------------------
# Text builders
# -------------------------------------------------
def build_start_text() -> str:
    """
    Build unified start menu text.
    """
    return (
        f"🧠 *{settings.AGENT_NAME}*\n\n"
        f"+ 📦 Version: `{settings.APP_VERSION}`\n"
        f"+ 🎨 Brand profile: `{settings.BRAND_PROFILE}`\n"
        f"+ 🌍 Environment: `{settings.APP_ENV.upper()}`\n"
        f"+ 🛡 Policy mode: `{settings.DEFAULT_POLICY_MODE}`\n\n"
        "Выберите доступный модуль управления:"
    )


# -------------------------------------------------
# Handlers
# -------------------------------------------------
@router.message(F.text == "/start")
async def start_menu(message: Message):
    """
    Entry point for the bot.

    Shows the main control panel.
    """
    await message.answer(
        build_start_text(),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == CB_BACK_TO_MAIN)
async def back_to_main(callback: CallbackQuery):
    """
    Universal handler to return to the main control panel.
    """
    await callback.message.edit_text(
        build_start_text(),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()
