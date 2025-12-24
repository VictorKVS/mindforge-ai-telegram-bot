# src/bot/bot.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\bot.py

Purpose:
Telegram UI / Control Panel for MindForge DEMO.

This module is the main entrypoint for the Telegram bot.

Responsibilities:
- Parse runtime flags (e.g. --demo)
- Run preflight checks
- Initialize Bot and Dispatcher (aiogram)
- Register routers (UI logic only)
- Start polling

Business logic, UAG policies and DEMO actions
are delegated to core modules.
"""

import asyncio
import sys

from aiogram import Bot, Dispatcher

from src.bot.config import settings, override_for_demo

# -------------------------------
# Routers (UI only, EXISTING)
# -------------------------------
from src.bot.handlers.start_menu import router as start_router
from src.bot.handlers.agent_control import router as agent_control_router
from src.bot.handlers.audit_panel import router as audit_router
from src.bot.handlers.status_panel import router as status_router


# ------------------------------------------------------------------
# Runtime flags
# ------------------------------------------------------------------
def parse_args() -> None:
    """
    Parse runtime flags.

    Supported flags:
    --demo : force DEMO mode (runtime override)
    """
    if "--demo" in sys.argv:
        override_for_demo()


# ------------------------------------------------------------------
# Preflight check
# ------------------------------------------------------------------
def preflight_check() -> None:
    """
    Preflight checks before bot startup.

    Purpose:
    - Validate critical configuration
    - Print effective runtime mode
    - Fail fast if configuration is invalid
    """

    errors = []
    warnings = []

    # --- Critical checks ---
    if not settings.TELEGRAM_TOKEN:
        errors.append("TELEGRAM_TOKEN is missing")

    if settings.APP_ENV not in {"demo", "prod"}:
        errors.append(f"Invalid APP_ENV value: {settings.APP_ENV}")

    if settings.DEFAULT_POLICY_MODE not in {"STRICT", "DEMO", "OFF"}:
        errors.append(
            f"Invalid DEFAULT_POLICY_MODE: {settings.DEFAULT_POLICY_MODE}"
        )

    # --- Warnings ---
    if settings.APP_ENV == "prod" and settings.DEFAULT_POLICY_MODE == "OFF":
        warnings.append(
            "Policy mode OFF in PROD environment (HIGH RISK)"
        )

    # --- Report ---
    print("🔍 Preflight check")
    print(f"🌍 ENV: {settings.APP_ENV.upper()}")
    print(f"🛡 Policy mode: {settings.DEFAULT_POLICY_MODE}")

    if warnings:
        print("⚠ WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("❌ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        raise RuntimeError("Preflight check failed")

    print("✅ Preflight check passed")


# ------------------------------------------------------------------
# Main entrypoint
# ------------------------------------------------------------------
async def main() -> None:
    """
    Main async entrypoint.
    """

    # Parse CLI flags (e.g. --demo)
    parse_args()

    # Preflight guard
    preflight_check()

    # Init bot and dispatcher
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    # IMPORTANT: router order matters
    dp.include_router(start_router)
    dp.include_router(agent_control_router)
    dp.include_router(audit_router)
    dp.include_router(status_router)

    print("🚀 MindForge Telegram Control Panel started")
    print(f"🧠 Agent name: {settings.agent_name}")
    print(f"🌍 ENV: {settings.APP_ENV.upper()}")
    print(f"🛡 Default policy mode: {settings.DEFAULT_POLICY_MODE}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
