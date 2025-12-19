# src/bot/handlers/teacher_handler.py

from aiogram import Router, types
from aiogram.filters import Command

from src.polygon.teacher.teacher_agent import TeacherAgent
from src.polygon.scenario_registry import ScenarioRegistry
from src.polygon.scenario_formatter import format_scenario_for_telegram

router = Router()


@router.message(Command("teacher"))
async def teacher_cmd(message: types.Message):
    """
    Команда обучения агента из последнего YAML-сценария

    Использование:
    /teacher teach
    """
    parts = message.text.split(maxsplit=1)

    # допускаем: "/teacher teach", "/teacher teach что-то"
    if len(parts) < 2 or not parts[1].lower().startswith("teach"):
        return await message.answer(
            "Использование:\n/teacher teach",
            parse_mode=None
        )

    agent = TeacherAgent()

    scenario = ScenarioRegistry.yaml_last()
    if not scenario:
        return await message.answer(
            "📭 Нет сценариев для обучения.",
            parse_mode=None
        )

    # обучение (пока логическое: анализ, регистрация знаний)
    agent.learn_from_scenario(scenario)

    text = "🧠 <b>Обучение завершено</b>\n\n"
    text += format_scenario_for_telegram(scenario)

    await message.answer(text, parse_mode="HTML")

