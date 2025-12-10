import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from src.bot.config import settings
from src.bot.handlers.security_filter import SecurityFilter
from src.bot.handlers.model_handler import router as model_router
from src.bot.handlers.interview_handler import router as interview_router
from src.bot.ai.llm_router import route


# ======================================================
# LOGGING
# ======================================================
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("MindForgeBot")


# ======================================================
# BOT + DISPATCHER
# ======================================================
bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ======================================================
# SECURITY FILTER (ГЛОБАЛЬНЫЙ ПЕРЕХВАТЧИК)
# ======================================================
security = SecurityFilter()


@dp.message()
async def global_security_check(message: Message):
    """
    Глобальная проверка всех входящих сообщений:
    - если опасно → блокируем
    - если ок → пропускаем дальше
    """

    text = message.text or ""

    if not security.check(text):
        await message.answer("⚠️ Сообщение заблокировано системой безопасности KM-6.")
        logging.warning(f"[SECURITY] Blocked message: {text}")
        return  # ВАЖНО: останавливаем цепочку, НЕ пропускаем дальше

    # ВАЖНО: возвращаем None → остальные хендлеры будут работать
    return


# ======================================================
# /start
# ======================================================
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🤖 <b>MindForge AI Bot</b> запущен!\n"
        "Готов к работе.\n\n"
        "Команды:\n"
        "/ask &lt;вопрос&gt; — спросить LLaMA\n"
        "/model — управление моделями\n"
        "/interview — начать интервью",
    )


# ======================================================
# /ask
# ======================================================
@dp.message(Command("ask"))
async def ask_llama(message: Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Использование: <code>/ask &lt;вопрос&gt;</code>")
        return

    question = parts[1]

    await message.answer("⏳ Думаю…")

    answer = await route(question)

    await message.answer(f"🧠 <b>Ответ LLaMA:</b>\n\n{answer}")


# ======================================================
# Подключение роутеров функциональности
# ======================================================
dp.include_router(model_router)
dp.include_router(interview_router)


# ======================================================
# MAIN ENTRY POINT
# ======================================================
async def main():
    logger.info("🚀 MindForge Telegram Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
