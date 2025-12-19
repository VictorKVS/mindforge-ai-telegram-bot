# src/bot/bot.py

import asyncio
from aiogram import Bot, Dispatcher
from src.bot.config import settings

# Routers
from src.bot.handlers.start_menu import router as start_router
from src.bot.handlers.training_center import router as training_router
from src.bot.handlers.scenarios import router as scenario_router
from src.bot.handlers.calendar import router as calendar_router

from src.bot.handlers.calendar_handler import router as calendar_router
dp.include_router(calendar_router)

from src.bot.handlers.scenario_player import router as scenario_player_router
dp.include_router(scenario_player_router)

async def main():
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    # Порядок важен
    dp.include_router(start_router)
    dp.include_router(training_router)
    dp.include_router(scenario_router)
    dp.include_router(calendar_router)

    print("🚀 SpaceAI Training Center started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
