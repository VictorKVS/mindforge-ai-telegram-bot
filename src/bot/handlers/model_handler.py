# src/bot/handlers/model_handler.py

from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime

from src.bot.ai.llm_router import route
from src.bot.ai.task_engine import (
    load_tasks,
    save_tasks,
    get_next_id,
    auto_categorize,
    run_task
)

router = Router()

# ---------------------------------------------------------
# Категории задач
# ---------------------------------------------------------

TASK_CATEGORIES = {
    "market": "Анализ рынка",
    "osint": "Разведка",
    "analysis": "Аналитика",
    "llm": "Генерация",
    "interview": "Интервью",
    "workflow": "Многошаговые процессы",
    "build": "Строительство (фундамент)"
}

FOUNDATION_KEYWORDS = [
    "фундамент",
    "ленточный фундамент",
    "сделать фундамент",
    "хочу фундамент"
]

# =========================================================
# 1️⃣ АССИСТЕНТ — ОСНОВНЫЕ КОМАНДЫ
# =========================================================

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🤖 <b>MindForge Assistant запущен!</b>\n\n"
        "Доступные команды:\n"
        "• /ask <вопрос> — спросить ИИ\n"
        "• /plan <задача> — составить план\n"
        "• /today — текущая дата\n"
        "• /who — кто я\n"
        "• /taskadd — создать задачу\n"
        "• /tasklist — список задач\n"
        "• /model — категории задач\n\n"
        "Для строительного агента: просто напиши «хочу фундамент».",
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📚 <b>Команды ассистента</b>\n"
        "/ask <вопрос>\n"
        "/plan <задача>\n"
        "/today — текущая дата\n"
        "/who — описание ИИ\n\n"
        "📦 <b>Task Manager</b>\n"
        "/taskadd <категория?> <текст>\n"
        "/tasklist\n"
        "/taskstatus <id>\n"
        "/taskrun <id>\n"
        "/taskrunall\n\n"
        "🏗 Строительный агент запускается по словам: «хочу фундамент»."
    )


@router.message(Command("today"))
async def today_cmd(message: types.Message):
    today = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"📅 Сегодня: <b>{today}</b>")


@router.message(Command("who"))
async def who_cmd(message: types.Message):
    resp = await route("кто ты?")
    await message.answer(resp)


@router.message(Command("ask"))
async def ask_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Использование: /ask <вопрос>")

    resp = await route(parts[1])
    await message.answer(resp)


@router.message(Command("plan"))
async def plan_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Использование: /plan <задача>")

    query = f"Составь детальный пошаговый план: {parts[1]}"
    resp = await route(query)
    await message.answer(resp)


# =========================================================
# 2️⃣ TASK MANAGER — задачи, категории, агенты
# =========================================================

@router.message(Command("model"))
async def model_cmd(message: types.Message):
    text = "📘 <b>Категории задач</b>\n\n"
    for k, v in TASK_CATEGORIES.items():
        text += f"• <b>{k}</b>: {v}\n"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("taskadd"))
async def task_add(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        return await message.answer("Использование: /taskadd <категория?> <текст>")

    # категория указана явно
    if len(parts) >= 3 and parts[1].lower() in TASK_CATEGORIES:
        category = parts[1].lower()
        text = parts[2]
    else:
        # автоопределение категории
        text = " ".join(parts[1:])
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

    await message.answer(
        f"📝 Создана задача {t_id}\nКатегория: {category}\nТекст: {text}"
    )


@router.message(Command("tasklist"))
async def task_list(message: types.Message):
    tasks = load_tasks()
    if not tasks:
        return await message.answer("📭 Нет задач.")

    txt = "📋 <b>Задачи</b>\n\n"
    for t in tasks:
        txt += (
            f"ID {t['id']}: {t['task']}\n"
            f"Категория: {t['category']}\n"
            f"Статус: {t['status']}\n\n"
        )

    await message.answer(txt, parse_mode="HTML")


@router.message(Command("taskstatus"))
async def task_status(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Использование: /taskstatus <id>")

    t_id = int(parts[1])
    tasks = load_tasks()
    t = next((x for x in tasks if x["id"] == t_id), None)

    if not t:
        return await message.answer("❌ Задача не найдена.")

    txt = (
        f"📌 <b>Задача {t_id}</b>\n"
        f"Категория: {t['category']}\n"
        f"Текст: {t['task']}\n"
        f"Статус: {t['status']}\n"
    )

    if t["result"]:
        txt += f"\n<b>Результат:</b>\n{t['result']}"

    await message.answer(txt, parse_mode="HTML")


@router.message(Command("taskrun"))
async def task_run(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("Использование: /taskrun <id>")

    t_id = int(parts[1])
    await message.answer("⚙ Запускаю агента...")

    result, err = await run_task(t_id)

    if err:
        return await message.answer(f"❌ Ошибка: {err}")

    await message.answer(f"✅ Готово:\n{result}")


@router.message(Command("taskrunall"))
async def task_run_all(message: types.Message):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["status"] == "new"]

    if not new_tasks:
        return await message.answer("📭 Нет новых задач.")

    await message.answer(f"⚙ Выполняю {len(new_tasks)} задач...")

    results = []
    for t in new_tasks:
        result, err = await run_task(t["id"])
        if err:
            results.append(f"❌ {t['id']}: {err}")
        else:
            results.append(f"✅ {t['id']}: OK")

    await message.answer("\n".join(results))


# =========================================================
# 3️⃣ СТРОИТЕЛЬНЫЙ АГЕНТ (фундамент)
# =========================================================

@router.message()
async def foundation_or_chat(message: types.Message):

    if not message.text:
        return

    text = message.text.lower()

    # 1) Если это фундамент — перехватываем
    if any(w in text for w in FOUNDATION_KEYWORDS):
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

        await message.answer(f"🏗 Создана строительная задача {t_id}. Запускаю расчёт...")

        result, err = await run_task(t_id)

        if err:
            return await message.answer(f"❌ Ошибка: {err}")

        return await message.answer(
            f"📐 <b>Проект фундамента:</b>\n<pre>{result}</pre>",
            parse_mode="HTML"
        )

    # 2) Иначе — обычная беседа с ассистентом
    resp = await route(message.text)
    await message.answer(resp)
