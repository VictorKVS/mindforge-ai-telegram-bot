# src/bot/handlers/model_handler.py

import json
import os
from aiogram import Router, types
from aiogram.filters import Command

from src.bot.ai.llm_router import route
from src.bot.ai.task_engine import (
    load_tasks,
    save_tasks,
    get_next_id,
    auto_categorize,
    run_task
)

router = Router()

TASK_DB_PATH = "tasks.json"

TASK_CATEGORIES = {
    "market": "Анализ рынка и цен",
    "osint": "Разведка, внешние источники",
    "analysis": "Аналитические задачи",
    "llm": "Генерация, reasoning",
    "interview": "Оценка компетенций",
    "workflow": "Многошаговые процессы"
}


# ---------------------------------------------------------
# /model help
# ---------------------------------------------------------

@router.message(Command("model"))
async def model_help(message: types.Message):
    text = "📡 <b>MindForge Task Manager v4.0</b>\n\n"
    text += "<b>Категории:</b>\n"

    for key, desc in TASK_CATEGORIES.items():
        text += f"• <b>{key}</b>: {desc}\n"

    text += (
        "\n<b>Команды:</b>\n"
        "/taskadd <категория?> <текст> – создать задачу\n"
        "/tasklist – список задач\n"
        "/tasklist <категория> – фильтр\n"
        "/taskremove <id> – удалить задачу\n"
        "/taskstatus <id> – статус задачи\n"
        "/taskrun <id> – выполнить задачу\n"
        "/taskrunall – выполнить все новые задачи\n"
    )

    await message.answer(text, parse_mode="HTML")


# ---------------------------------------------------------
# /taskadd — создание задачи (гибрид: вручную + авто)
# ---------------------------------------------------------

@router.message(Command("taskadd"))
async def task_add(message: types.Message):
    parts = message.text.split(maxsplit=2)

    if len(parts) < 2:
        await message.answer("Использование: /taskadd <категория?> <текст задачи>")
        return

    # Если категория указана
    if len(parts) >= 3 and parts[1].lower() in TASK_CATEGORIES:
        category = parts[1].lower()
        task_text = parts[2]
    else:
        # Категория не указана → автоопределение
        task_text = " ".join(parts[1:])
        category = await auto_categorize(task_text)

    tasks = load_tasks()
    task_id = get_next_id(tasks)

    task_obj = {
        "id": task_id,
        "task": task_text,
        "category": category,
        "status": "new",
        "result": None
    }

    tasks.append(task_obj)
    save_tasks(tasks)

    await message.answer(
        f"📝 Задача создана!\n"
        f"<b>ID:</b> {task_id}\n"
        f"<b>Категория:</b> {category}\n"
        f"<b>Текст:</b> {task_text}",
        parse_mode="HTML"
    )


# ---------------------------------------------------------
# /tasklist — список задач
# ---------------------------------------------------------

@router.message(Command("tasklist"))
async def task_list(message: types.Message):
    parts = message.text.split(maxsplit=1)
    category_filter = None

    if len(parts) == 2:
        category_filter = parts[1].lower()

    tasks = load_tasks()

    if category_filter:
        tasks = [t for t in tasks if t["category"] == category_filter]

    if not tasks:
        await message.answer("📭 Список задач пуст.")
        return

    text = "📋 <b>Задачи:</b>\n\n"
    for t in tasks:
        text += (
            f"🔹 <b>ID:</b> {t['id']}\n"
            f"   <b>Категория:</b> {t['category']}\n"
            f"   <b>Задача:</b> {t['task']}\n"
            f"   <b>Статус:</b> {t['status']}\n\n"
        )

    await message.answer(text, parse_mode="HTML")


# ---------------------------------------------------------
# /taskremove — удаление задачи
# ---------------------------------------------------------

@router.message(Command("taskremove"))
async def task_remove(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /taskremove <id>")
        return

    task_id = int(parts[1])
    tasks = load_tasks()

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)

    await message.answer(f"🗑 Задача {task_id} удалена.")


# ---------------------------------------------------------
# /taskstatus — статус и результат задачи
# ---------------------------------------------------------

@router.message(Command("taskstatus"))
async def task_status(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /taskstatus <id>")
        return

    task_id = int(parts[1])

    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        await message.answer("❌ Задача не найдена.")
        return

    text = (
        f"📌 <b>Задача {task_id}</b>\n"
        f"<b>Категория:</b> {task['category']}\n"
        f"<b>Текст:</b> {task['task']}\n"
        f"<b>Статус:</b> {task['status']}\n"
    )

    if task["result"]:
        text += f"\n<b>Результат агента:</b>\n{task['result']}"

    await message.answer(text, parse_mode="HTML")


# ---------------------------------------------------------
# /taskrun — выполнить задачу агентом
# ---------------------------------------------------------

@router.message(Command("taskrun"))
async def task_run(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /taskrun <id>")
        return

    task_id = int(parts[1])

    await message.answer("⚙ Запускаю агента…")

    result, error = await run_task(task_id)

    if error:
        await message.answer(f"❌ Ошибка: {error}")
        return

    await message.answer(f"✅ Готово!\n\n<b>Результат:</b>\n{result}", parse_mode="HTML")


# ---------------------------------------------------------
# /taskrunall — выполнить все новые задачи
# ---------------------------------------------------------

@router.message(Command("taskrunall"))
async def task_run_all(message: types.Message):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["status"] == "new"]

    if not new_tasks:
        await message.answer("📭 Нет задач для выполнения.")
        return

    await message.answer(f"⚙ Выполняю {len(new_tasks)} задач…")

    results = []

    for t in new_tasks:
        result, error = await run_task(t["id"])
        if error:
            results.append(f"❌ ID {t['id']}: {error}")
        else:
            results.append(f"✅ ID {t['id']}: выполнено")

    text = "📊 <b>Результаты:</b>\n" + "\n".join(results)
    await message.answer(text, parse_mode="HTML")

# ---------------------------------------------------------
# 0. Детектор строительных задач ("хочу фундамент")
# ---------------------------------------------------------

from src.bot.ai.task_engine import load_tasks, save_tasks, get_next_id, run_task

FOUNDATION_KEYWORDS = [
    "фундамент",
    "ленточный фундамент",
    "сделать фундамент",
    "хочу фундамент"
]


@router.message()
async def foundation_detector(message: types.Message):
    """
    Автоматически перехватывает фразы вида:
    - "хочу фундамент"
    - "сделать фундамент"
    - "фундамент ленточный"
    и запускает FoundationAgent.
    """

    if not message.text:
        return

    text = message.text.lower()

    # ищем ключевые слова
    if any(key in text for key in FOUNDATION_KEYWORDS):

        # создаём новую задачу категории "build"
        tasks = load_tasks()
        task_id = get_next_id(tasks)

        task_obj = {
            "id": task_id,
            "task": message.text,
            "category": "build",
            "status": "new",
            "result": None
        }

        tasks.append(task_obj)
        save_tasks(tasks)

        # предварительное сообщение
        await message.answer(
            f"🏗️ Обнаружен запрос на строительство фундамента.\n"
            f"Создаю задачу №{task_id} и запускаю проектирование..."
        )

        # запускаем FoundationAgent
        result, error = await run_task(task_id)

        if error:
            await message.answer(f"❌ Ошибка: {error}")
            return

        # выводим предварительный проект
        await message.answer(
            f"📐 <b>Предварительный проект фундамента:</b>\n\n{result}",
            parse_mode="HTML"
        )

        return
