from aiogram import Router, types
from aiogram.filters import Command

from src.bot.ai.task_engine import (
    load_tasks,
    save_tasks,
    get_next_id,
    auto_categorize,
    run_task
)

router = Router()

FOUNDATION_KEYWORDS = [
    "фундамент",
    "ленточный фундамент",
    "хочу фундамент",
    "сделать фундамент"
]

# ---------------------------
# /taskadd
# ---------------------------
@router.message(Command("taskadd"))
async def task_add(message: types.Message):
    parts = message.text.split(maxsplit=2)

    if len(parts) < 2:
        await message.answer("Использование: /taskadd <категория?> <текст>")
        return

    if len(parts) >= 3:
        category = parts[1]
        text = parts[2]
    else:
        text = parts[1]
        category = await auto_categorize(text)

    tasks = load_tasks()
    t_id = get_next_id(tasks)

    tasks.append({
        "id": t_id,
        "task": text,
        "category": category,
        "status": "new",
        "result": None
    })

    save_tasks(tasks)

    await message.answer(f"📝 Задача создана (ID {t_id})\nКатегория: {category}\n{text}")

# ---------------------------
# /tasklist
# ---------------------------
@router.message(Command("tasklist"))
async def task_list(message: types.Message):
    tasks = load_tasks()

    if not tasks:
        return await message.answer("📭 Нет задач.")

    txt = "📋 <b>Задачи:</b>\n\n"
    for t in tasks:
        txt += f"ID {t['id']} — {t['task']} ({t['category']}) [{t['status']}]\n"

    await message.answer(txt, parse_mode="HTML")

# ---------------------------
# /taskrun
# ---------------------------
@router.message(Command("taskrun"))
async def task_run(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Использование: /taskrun <id>")

    t_id = int(parts[1])

    await message.answer("⚙ Выполняю задачу...")

    result, err = await run_task(t_id)

    if err:
        await message.answer(f"❌ Ошибка: {err}")
    else:
        await message.answer(f"✅ Результат:\n{result}")

# ---------------------------
# Детектор строительных задач
# ---------------------------
@router.message()
async def foundation_detector(message: types.Message):
    text = (message.text or "").lower()

    if any(k in text for k in FOUNDATION_KEYWORDS):
        tasks = load_tasks()
        t_id = get_next_id(tasks)

        tasks.append({
            "id": t_id,
            "task": message.text,
            "category": "build",
            "status": "new",
            "result": None
        })

        save_tasks(tasks)

        await message.answer(f"🏗 Создана строительная задача ID {t_id}. Рассчитываю...")

        result, err = await run_task(t_id)

        if err:
            return await message.answer(f"❌ Ошибка: {err}")

        return await message.answer(f"📐 <b>Проект:</b>\n<pre>{result}</pre>", parse_mode="HTML")
