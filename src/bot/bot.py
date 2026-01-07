import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.config import settings

# ---- ROUTERS ----
from src.bot.handlers.start_menu import router as start_menu_router
from src.bot.handlers.uag_schema import router as uag_schema_router
from src.bot.handlers.session_replay import router as session_replay_router

# ---- MIDDLEWARE ----
from src.bot.middlewares.policy_middleware import PolicyMiddleware
from src.bot.middlewares.ui_event_logger import UIButtonLoggerMiddleware


# ---------------------------------------------------------------------
# LOGGING SETUP
# ---------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)

log = logging.getLogger("mindforge.bot")


# ---------------------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------------------
async def main() -> None:
    log.info("BOOT | MindForge Telegram Bot starting")
    log.info("ENV  | %s", settings.APP_ENV)
    log.info("MODE | %s", settings.DEFAULT_POLICY_MODE)

    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    dp = Dispatcher()

    # =====================================================
    # MIDDLEWARE PIPELINE (ORDER IS CRITICAL)
    # =====================================================

    # 1️⃣ POLICY — ПЕРВЫЙ (AG-7.1)
    dp.update.middleware(PolicyMiddleware())

    # 2️⃣ UI EVENT LOGGER / LOCKS
    dp.callback_query.middleware(UIButtonLoggerMiddleware())

    # =====================================================
    # ROUTERS
    # =====================================================
    dp.include_router(start_menu_router)
    dp.include_router(uag_schema_router)
    dp.include_router(session_replay_router)

    log.info("BOT | polling start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
