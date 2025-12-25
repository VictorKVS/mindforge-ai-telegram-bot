# src/bot/bot.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\bot.py

Purpose:
Telegram UI / Control Panel for MindForge DEMO.

This module is the main entrypoint for the Telegram bot.
"""

import asyncio
import sys

from aiogram import Bot, Dispatcher

from src.bot.config import settings, override_for_demo

# -------------------------------------------------
# Routers (UI only)
# -------------------------------------------------
from src.bot.handlers.start_menu import router as start_router
from src.bot.handlers.agent_control import router as agent_control_router
from src.bot.handlers.audit_panel import router as audit_router
from src.bot.handlers.status_panel import router as status_router
from src.bot.handlers.security_panel import router as security_router


# -------------------------------------------------
# Runtime flags
# -------------------------------------------------
def parse_args() -> None:
    if "--demo" in sys.argv:
        override_for_demo()

# -------------------------------------------------
# Preflight check
# -------------------------------------------------
def preflight_check() -> None:
    if not settings.TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is missing")

    print("🔍 Preflight check")
    print(f"🌍 ENV: {settings.APP_ENV.upper()}")
    print(f"🛡 Policy mode: {settings.DEFAULT_POLICY_MODE}")
    print("✅ Preflight check passed")


# -------------------------------------------------
# Main entrypoint
# -------------------------------------------------
async def main() -> None:
    parse_args()
    preflight_check()

    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    # -------------------------------------------------
    # Router registration (feature-flag driven)
    # -------------------------------------------------
    dp.include_router(start_router)

    if settings.FEATURE_AGENT_CONTROL:
        dp.include_router(agent_control_router)

    if settings.FEATURE_AUDIT_PANEL:
        dp.include_router(audit_router)
        dp.include_router(security_router)  # ← ВАЖНО: здесь правильно

    if settings.FEATURE_STATUS_PANEL:
        dp.include_router(status_router)

    # -------------------------------------------------
    # Startup banner
    # -------------------------------------------------
    print("🚀 MindForge Telegram Control Panel started")
    print(f"🧠 Agent name: {settings.AGENT_NAME}")
    print(f"📦 App version: {settings.APP_VERSION}")
    print(f"🎨 Brand profile: {settings.BRAND_PROFILE}")
    print(f"🌍 ENV: {settings.APP_ENV.upper()}")
    print(f"🛡 Default policy mode: {settings.DEFAULT_POLICY_MODE}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
