from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime

from src.bot.ai.llm_router import route

# ------------------------------
# Создаём Router
# ------------------------------
router = Router()


# ------------------------------
# /start
# ------------------------------
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет! Я MindForge Assistant.\n"
        "Могу отвечать на вопросы, составлять планы и помогать.\n\n"
        "Попробуй: /ask Привет!\n"
        "Список команд: /help"
    )


# ------------------------------
# /help
# ------------------------------
@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📚 Команды:\n"
        "/ask <текст> — спросить ассистента\n"
        "/plan <задача> — создать план действий\n"
        "/today — текущая дата\n"
        "/who — кто я\n"
    )


# ------------------------------
# /today
# ------------------------------
@router.message(Command("today"))
async def today_cmd(message: types.Message):
    today = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"📅 Сегодня: <b>{today}</b>")


# ------------------------------
# /who
# ------------------------------
@router.message(Command("who"))
async def who_cmd(message: types.Message):
    resp = await route("кто ты?")
    await message.answer(resp)


# ------------------------------
# /ask
# ------------------------------
@router.message(Command("ask"))
async def ask_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        return await message.answer("Использование: /ask <вопрос>")

    question = parts[1]
    await message.answer("⏳ Думаю…")

    print(f"[ASK] User question: {question}")   # ЛОГ

    resp = await route(question)

    print(f"[ASK] LLaMA response: {resp}")      # ЛОГ

    await message.answer(resp)


# ------------------------------
# /plan
# ------------------------------
@router.message(Command("plan"))
async def plan_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        return await message.answer("Использование: /plan <задача>")

    query = f"Составь подробный план: {parts[1]}"
    resp = await route(query)
    await message.answer(resp)


# ------------------------------
# Обычные сообщения — диалог
# ------------------------------
@router.message()
async def general_dialogue(message: types.Message):
    print(f"[DIALOG] User: {message.text}")  # ЛОГ
    resp = await route(message.text)
    print(f"[DIALOG] LLaMA: {resp}")         # ЛОГ
    await message.answer(resp)
