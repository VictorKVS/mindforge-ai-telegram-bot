# src/bot/bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.config import settings
from src.bot.handlers.security_filter import SecurityFilter
from src.bot.handlers.assistant_handler import router as assistant_router
from src.bot.handlers.task_handler import router as task_router


logging.basicConfig(level="INFO")
logger = logging.getLogger("MindForgeBot")


async def main():
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    security = SecurityFilter()

    # ---------------------------------------------------
    # 1) SECURITY FILTER — обрабатывает ТОЛЬКО обычные сообщения, НЕ команды
    # ---------------------------------------------------
    @dp.message(F.text & ~F.text.startswith("/"))
    async def security_check(message):
        text = message.text or ""

        if not security.check(text):
            await message.answer("⚠️ Сообщение заблокировано системой безопасности KM-6.")
            return

        # безопасное сообщение → пропускаем дальше
        pass

    # ---------------------------------------------------
    # 2) РЕГИСТРАЦИЯ РОУТЕРОВ
    # ---------------------------------------------------
    dp.include_router(assistant_router)   # /start, /help, /ask…
    dp.include_router(task_router)        # задачи + фундамент

    logger.info("🚀 MindForge Assistant started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

