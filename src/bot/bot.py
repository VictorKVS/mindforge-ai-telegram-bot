import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.config import settings
from src.bot.handlers.security_filter import security_router
from src.bot.handlers.model_handler import router as model_router
from src.bot.handlers.interview_handler import router as interview_router

logging.basicConfig(level=logging.INFO)

# Хранилище состояний FSM
storage = MemoryStorage()

# Основной объект бота
bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")

# Диспетчер — центр маршрутизации событий
dp = Dispatcher(storage=storage)

# Регистрируем роутеры
dp.include_router(security_router)
dp.include_router(model_router)
dp.include_router(interview_router)


async def main():
    """
    Точка входа Telegram бота.
    Компактно, чисто, промышленно.
    """
    logging.info("🚀 MindForge Telegram Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
