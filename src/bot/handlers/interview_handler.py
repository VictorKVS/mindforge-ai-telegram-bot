# src/bot/handlers/interview_handler.py

import logging
from typing import Dict, Any, Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter

from src.bot.ai.llm_router import route  # LLaMA

log = logging.getLogger("mindforge.handlers.interview")

router = Router()


# ===============================================================
#  FSM состояния интервью
# ===============================================================

class InterviewState(StatesGroup):
    waiting_for_topic = State()
    asking_question = State()
    waiting_for_answer = State()
    review_mode = State()  # Для оценки ответа


# ===============================================================
#  Вспомогательные функции
# ===============================================================

async def generate_question(topic: str, context: Optional[str] = None) -> str:
    """Генерация вопроса по теме"""
    prompt = f"Сгенерируй один сложный и интересный вопрос по теме '{topic}'."
    if context:
        prompt += f"\nУчти контекст предыдущих вопросов: {context}"
    return await route(prompt)


async def evaluate_answer(question: str, user_answer: str, topic: str) -> Dict[str, Any]:
    """Оценка ответа пользователя"""
    evaluation_prompt = (
        f"Тема интервью: {topic}\n"
        f"Вопрос: {question}\n"
        f"Ответ пользователя: {user_answer}\n\n"
        f"Оцени ответ по следующим критериям:\n"
        f"1. Правильность (1-5 баллов)\n"
        f"2. Полнота (1-5 баллов)\n"
        f"3. Структура (1-5 баллов)\n"
        f"4. Примеры/доказательства (1-5 баллов)\n\n"
        f"Дай краткое обоснование оценки и предложи, что можно улучшить."
    )
    
    evaluation_text = await route(evaluation_prompt)
    
    # Парсинг оценки (простая эвристика)
    score = 3  # среднее по умолчанию
    if "5" in evaluation_text:
        score = 5
    elif "4" in evaluation_text:
        score = 4
    elif "2" in evaluation_text or "1" in evaluation_text:
        score = 2
    
    return {
        "text": evaluation_text,
        "score": score,
        "question": question,
        "user_answer": user_answer
    }


# ===============================================================
#  /interview — запуск
# ===============================================================

@router.message(Command("interview"))
async def start_interview(message: Message, state: FSMContext):
    """
    Пользователь запускает интервью.
    """
    await state.clear()
    await state.set_state(InterviewState.waiting_for_topic)
    
    log.info(
        "INTERVIEW_START | user_id=%s | username=%s",
        message.from_user.id,
        message.from_user.username
    )
    
    await message.answer(
        "📝 *Режим интервью*\n\n"
        "О чём провести интервью?\n\n"
        "*Примеры тем:*\n"
        "• Python / Django / FastAPI\n"
        "• DevOps / Docker / Kubernetes\n"
        "• Machine Learning / LLM\n"
        "• Cybersecurity / ИБ\n"
        "• System Design / Архитектура\n\n"
        "Напишите тему одним словом или короткой фразой.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Отмена",
                        callback_data="interview_cancel"
                    )
                ]
            ]
        )
    )


# ===============================================================
#  Отмена интервью
# ===============================================================

@router.callback_query(F.data == "interview_cancel")
async def cancel_interview(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Интервью отменено.")
    await call.answer()


# ===============================================================
#  Получение темы интервью
# ===============================================================

@router.message(InterviewState.waiting_for_topic)
async def set_topic(message: Message, state: FSMContext):
    topic = message.text.strip()
    
    if len(topic) < 2 or len(topic) > 100:
        await message.answer(
            "⚠️ Пожалуйста, укажите тему от 2 до 100 символов.\n"
            "Например: `Python` или `Machine Learning`.",
            parse_mode="Markdown"
        )
        return
    
    # Сохраняем тему и инициализируем историю
    await state.update_data({
        "topic": topic,
        "questions_asked": 0,
        "total_score": 0,
        "history": []
    })
    
    await message.answer(
        f"🎯 *Тема интервью:* **{topic}**\n\n"
        "Сейчас я задам вам первый вопрос...",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛑 Завершить интервью",
                        callback_data="interview_stop"
                    )
                ]
            ]
        )
    )
    
    # Генерируем первый вопрос
    try:
        question = await generate_question(topic)
        
        await state.update_data({
            "last_question": question,
            "questions_asked": 1
        })
        
        await state.set_state(InterviewState.waiting_for_answer)
        
        await message.answer(
            f"❓ *Вопрос 1:*\n\n{question}\n\n"
            "Напишите ваш ответ в свободной форме.",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        log.error(f"Error generating question: {e}")
        await message.answer(
            "😕 Произошла ошибка при генерации вопроса. "
            "Попробуйте начать заново: /interview"
        )
        await state.clear()


# ===============================================================
#  Ответ пользователя → следующий вопрос
# ===============================================================

@router.message(InterviewState.waiting_for_answer)
async def process_answer(message: Message, state: FSMContext):
    user_answer = message.text.strip()
    
    if len(user_answer) < 5:
        await message.answer(
            "⚠️ Пожалуйста, напишите более развернутый ответ "
            "(минимум 5 символов)."
        )
        return
    
    data = await state.get_data()
    topic = data.get("topic")
    last_question = data.get("last_question")
    questions_asked = data.get("questions_asked", 0)
    total_score = data.get("total_score", 0)
    history = data.get("history", [])
    
    # Показываем что обрабатываем ответ
    processing_msg = await message.answer("⏳ Оцениваю ваш ответ...")
    
    # Оцениваем ответ
    try:
        evaluation = await evaluate_answer(last_question, user_answer, topic)
        
        # Обновляем статистику
        questions_asked += 1
        total_score += evaluation["score"]
        average_score = total_score / questions_asked if questions_asked > 0 else 0
        
        # Сохраняем в историю
        history.append({
            "question": last_question,
            "answer": user_answer,
            "evaluation": evaluation["text"],
            "score": evaluation["score"]
        })
        
        await state.update_data({
            "questions_asked": questions_asked,
            "total_score": total_score,
            "history": history,
            "last_evaluation": evaluation
        })
        
        # Удаляем сообщение "обработка"
        await processing_msg.delete()
        
        # Показываем оценку
        await message.answer(
            f"📊 *Оценка ответа:*\n\n"
            f"• Вопрос: {last_question}\n"
            f"• Ваш ответ: {user_answer[:100]}...\n"
            f"• Оценка: {evaluation['score']}/5\n\n"
            f"*Анализ:*\n{evaluation['text']}\n\n"
            f"📈 *Статистика:* {questions_asked} вопросов, "
            f"средний балл: {average_score:.1f}/5",
            parse_mode="Markdown"
        )
        
        # Генерируем следующий вопрос
        if questions_asked >= 10:  # Максимум 10 вопросов
            await state.set_state(InterviewState.review_mode)
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📊 Полный отчет",
                            callback_data="interview_report"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Новое интервью",
                            callback_data="interview_new"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="📤 Экспорт истории",
                            callback_data="interview_export"
                        )
                    ]
                ]
            )
            
            await message.answer(
                "🎉 *Интервью завершено!*\n\n"
                f"Вы ответили на {questions_asked} вопросов по теме '{topic}'.\n"
                f"Средний балл: {average_score:.1f}/5\n\n"
                "Что дальше?",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            return
        
        # Генерируем следующий вопрос
        next_question = await generate_question(
            topic, 
            context=f"Уже были заданы вопросы: {', '.join([h['question'][:50] + '...' for h in history[-3:]])}"
        )
        
        await state.update_data({
            "last_question": next_question
        })
        
        await message.answer(
            f"❓ *Вопрос {questions_asked + 1}:*\n\n{next_question}\n\n"
            "Напишите ваш ответ:",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        log.error(f"Error evaluating answer: {e}")
        await message.answer(
            "😕 Произошла ошибка при оценке ответа. "
            "Попробуйте ответить заново или начать новое интервью: /interview"
        )


# ===============================================================
#  Обработчики кнопок в режиме review
# ===============================================================

@router.callback_query(StateFilter(InterviewState.review_mode), F.data == "interview_report")
async def show_full_report(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])
    
    report = "📋 *Полный отчет по интервью*\n\n"
    
    for i, item in enumerate(history, 1):
        report += f"*Вопрос {i}:* {item['question'][:100]}...\n"
        report += f"*Оценка:* {item['score']}/5\n\n"
    
    total_questions = len(history)
    average_score = sum(item['score'] for item in history) / total_questions if total_questions > 0 else 0
    
    report += f"📈 *Итог:* {total_questions} вопросов, средний балл: {average_score:.1f}/5"
    
    await call.message.answer(report, parse_mode="Markdown")
    await call.answer()


@router.callback_query(StateFilter(InterviewState.review_mode), F.data == "interview_new")
async def start_new_interview(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("🔄 Начинаем новое интервью...")
    await start_interview(call.message, state)
    await call.answer()


@router.callback_query(StateFilter(InterviewState.review_mode), F.data == "interview_export")
async def export_history(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic", "Неизвестная тема")
    history = data.get("history", [])
    
    export_text = f"Интервью по теме: {topic}\n"
    export_text += "=" * 50 + "\n\n"
    
    for i, item in enumerate(history, 1):
        export_text += f"ВОПРОС {i}:\n{item['question']}\n\n"
        export_text += f"ОТВЕТ:\n{item['answer']}\n\n"
        export_text += f"ОЦЕНКА ({item['score']}/5):\n{item['evaluation']}\n"
        export_text += "-" * 50 + "\n\n"
    
    # В реальном приложении можно сохранить в файл или отправить как документ
    await call.message.answer(
        f"📤 *Экспорт истории*\n\n"
        f"История интервью по теме '{topic}' подготовлена к экспорту.\n"
        f"Всего вопросов: {len(history)}\n\n"
        "В будущей версии будет возможность скачать файл.",
        parse_mode="Markdown"
    )
    await call.answer()


# ===============================================================
#  /interviewstop — для выхода в любое время
# ===============================================================

@router.message(Command("interviewstop"))
@router.message(Command("stop"))
async def stop_interview(message: Message, state: FSMContext):
    data = await state.get_data()
    questions_asked = data.get("questions_asked", 0)
    
    if questions_asked > 0:
        total_score = data.get("total_score", 0)
        average_score = total_score / questions_asked if questions_asked > 0 else 0
        
        await message.answer(
            f"🛑 *Интервью остановлено*\n\n"
            f"• Задано вопросов: {questions_asked}\n"
            f"• Средний балл: {average_score:.1f}/5\n\n"
            f"Чтобы начать заново: /interview",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "🛑 Интервью остановлено.\n\n"
            "Чтобы начать заново: /interview"
        )
    
    await state.clear()


# ===============================================================
#  Обработчик для команды /interviewhelp
# ===============================================================

@router.message(Command("interviewhelp"))
async def interview_help(message: Message):
    help_text = (
        "📚 *Помощь по режиму интервью*\n\n"
        "*/interview* – Начать новое интервью\n"
        "*/interviewstop* или */stop* – Остановить текущее интервью\n"
        "*/interviewhelp* – Эта справка\n\n"
        "*Как это работает:*\n"
        "1. Выбираете тему (Python, DevOps, ML и т.д.)\n"
        "2. Бот задает вопросы по теме\n"
        "3. Вы отвечаете в свободной форме\n"
        "4. Бот оценивает ваш ответ и дает обратную связь\n"
        "5. Процесс продолжается до 10 вопросов\n\n"
        "*Советы:*\n"
        "• Отвечайте развернуто, с примерами\n"
        "• Используйте технические термины\n"
        "• Не бойтесь ошибаться – это обучение!"
    )
    
    await message.answer(help_text, parse_mode="Markdown")