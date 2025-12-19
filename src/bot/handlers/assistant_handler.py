from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime

from src.bot.ai.llm_router import route
from src.polygon.scenario_registry import ScenarioRegistry
from src.polygon.scenario_formatter import format_scenario_for_telegram


from src.polygon.teacher.teacher_agent import TeacherAgent

router = Router()

# ------------------------------
# /start
# ------------------------------
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет! Я MindForge Assistant.\n"
        "Могу отвечать на вопросы, составлять планы и работать со сценариями.\n\n"
        "Команды:\n"
        "/ask <вопрос>\n"
        "/plan <задача>\n"
        "/scenario last | list | diff\n"
        "/help"
    )


# ------------------------------
# /help
# ------------------------------
@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📚 Доступные команды:\n\n"
        "/ask <вопрос> — спросить ассистента\n"
        "/plan <задача> — составить план\n"
        "/today — текущая дата\n"
        "/who — кто я\n\n"
        "🧠 Сценарии:\n"
        "/scenario last — последний сценарий\n"
        "/scenario list — список сценариев\n"
        "/scenario diff — различия между двумя последними\n"
    )


# ------------------------------
# /today
# ------------------------------
@router.message(Command("today"))
async def today_cmd(message: types.Message):
    today = datetime.now().strftime("%d.%m.%Y")
    await message.answer(f"📅 Сегодня: {today}")


# ------------------------------
# /who
# ------------------------------
@router.message(Command("who"))
async def who_cmd(message: types.Message):
    await message.answer("Я — MindForge Assistant v1.0. Управляю агентами, сценариями и диалогом.")


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

    resp = await route(question)
    await message.answer(resp)


# ------------------------------
# /plan
# ------------------------------
@router.message(Command("plan"))
async def plan_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Использование: /plan <задача>")

    await message.answer("⏳ Строю план…")
    query = f"Составь подробный пошаговый план: {parts[1]}"
    resp = await route(query)
    await message.answer(resp)


# =========================================================
# /scenario
# =========================================================
@router.message(Command("scenario"))
async def scenario_cmd(message: types.Message):
    parts = message.text.split(maxsplit=2)

    if len(parts) < 2:
        return await message.answer(
            "Использование:\n"
            "/scenario last\n"
            "/scenario list\n"
            "/scenario diff"
        )

    sub = parts[1].lower()

    if sub == "last":
        s = ScenarioRegistry.yaml_last()
        if not s:
            return await message.answer("📭 YAML-сценариев пока нет.")
        return await message.answer(
            format_scenario_for_telegram(s),
            parse_mode=None
        )

    if sub == "list":
        all_yaml = ScenarioRegistry.yaml_all()
        if not all_yaml:
            return await message.answer("📭 YAML-сценариев пока нет.")

        txt = "📚 Последние сценарии:\n\n"
        for x in all_yaml[-10:]:
            txt += f"• {x.get('scenario_id','?')} ({x.get('created_at','?')})\n"

        return await message.answer(txt)

    if sub == "diff":
        all_yaml = ScenarioRegistry.yaml_all()
        if len(all_yaml) < 2:
            return await message.answer("Нужно минимум 2 сценария для diff.")

        a = all_yaml[-2]
        b = all_yaml[-1]

        a_intents = {st["intent"] for st in a.get("steps", [])}
        b_intents = {st["intent"] for st in b.get("steps", [])}

        added = b_intents - a_intents
        removed = a_intents - b_intents

        txt = (
            "🧾 DIFF сценариев\n\n"
            f"A: {a.get('scenario_id')}\n"
            f"B: {b.get('scenario_id')}\n\n"
            "➕ Добавлено:\n"
            + ("\n".join(f"• {x}" for x in added) if added else "—")
            + "\n\n➖ Удалено:\n"
            + ("\n".join(f"• {x}" for x in removed) if removed else "—")
        )

        return await message.answer(txt)

    return await message.answer("Неизвестная подкоманда /scenario")


# =========================================================
# ОБЫЧНЫЙ ТЕКСТ → LLM
# =========================================================
@router.message()
async def general_dialogue(message: types.Message):
    # ❗ КОМАНДЫ СЮДА НЕ ПОПАДАЮТ
    if message.text.startswith("/"):
        return

    resp = await route(message.text)
    await message.answer(resp)




@router.message(Command("teacher"))
async def teacher_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or parts[1] != "teach":
        return await message.answer(
            "Использование:\n/teacher teach",
            parse_mode=None
        )

    agent = TeacherAgent()
    result = agent.teach()

    if not result:
        return await message.answer(
            "📭 Нет данных для обучения.\nСначала должен появиться audit.log",
            parse_mode=None
        )

    await message.answer(
        f"🎓 Обучение завершено!\n\n"
        f"Создан сценарий:\n{result.name}",
        parse_mode=None
    )
