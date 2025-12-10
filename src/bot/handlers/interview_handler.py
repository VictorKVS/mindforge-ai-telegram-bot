# src/bot/handlers/interview_handler.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from src.bot.ai.llm_router import route  # LLaMA

router = Router()


# ===============================================================
#  FSM состояния интервью
# ===============================================================

class InterviewState(StatesGroup):
    waiting_for_topic = State()
    asking_question = State()
    waiting_for_answer = State()


# ===============================================================
#  /interview — запуск
# ===============================================================

@router.message(Command("interview"))
async def start_interview(message: types.Message, state: FSMContext):
    """
    Пользователь запускает интервью.
    """
    await state.set_state(InterviewState.waiting_for_topic)
    await message.answer(
        "📝 О чём провести интервью?\n\n"
        "Например: `Python`, `DevOps`, `LLM`, `ИБ`.",
        parse_mode="Markdown"
    )


# ===============================================================
#  Получение темы интервью
# ===============================================================

@router.message(InterviewState.waiting_for_topic)
async def set_topic(message: types.Message, state: FSMContext):
    topic = message.text.strip()

    await state.update_data(topic=topic)

    await message.answer(f"👍 Тема интервью установлена: **{topic}**", parse_mode="Markdown")

    # генерируем первый вопрос
    question = await route(f"Сгенерируй один сложный вопрос по теме '{topic}'.")
    await state.update_data(last_question=question)

    await state.set_state(InterviewState.waiting_for_answer)
    await message.answer(f"❓ {question}")


# ===============================================================
#  Ответ пользователя → следующий вопрос
# ===============================================================

@router.message(InterviewState.waiting_for_answer)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")
    user_answer = message.text

    # Оценка ответа через LLaMA
    evaluation = await route(
        f"Вопрос: {data['last_question']}\n"
        f"Ответ пользователя: {user_answer}\n\n"
        f"Оцени ответ по шкале 1–5 и кратко обоснуй."
    )

    await message.answer(f"📊 *Оценка:*\n{evaluation}", parse_mode="Markdown")

    # генерируем следующий вопрос
    next_q = await route(f"Сгенерируй ещё один хороший вопрос по теме '{topic}'.")
    await state.update_data(last_question=next_q)

    await message.answer(f"❓ {next_q}")


# ===============================================================
#  /interviewstop — для выхода
# ===============================================================

@router.message(Command("interviewstop"))
async def stop_interview(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🛑 Интервью остановлено.")
