# src/bot/handlers/assistant_handler.py

from src.polygon.scenario_registry import ScenarioRegistry
from src.polygon.scenario_formatter import format_scenario_for_telegram

from aiogram.filters import Command
from src.polygon.scenario_registry import ScenarioRegistry
from src.polygon.scenario_formatter import format_scenario_for_telegram

@router.message(Command("scenario"))
async def scenario_cmd(message):
    if message.text.strip() != "/scenario last":
        return await message.answer(
            "Использование: /scenario last",
            parse_mode=None
        )

    scenario = ScenarioRegistry.yaml_last()
    if not scenario:
        return await message.answer(
            "📭 Пока нет обучающих сценариев.",
            parse_mode=None
        )

    text = format_scenario_for_telegram(scenario)
    await message.answer(text, parse_mode=None)

    

    @router.message(Command("scenario"))
    async def scenario_cmd(message):
         if message.text.strip() != "/scenario last":
            return await message.answer(
               "Использование: /scenario last",
            parse_mode=None
             )

    scenario = ScenarioRegistry.yaml_last()
    if not scenario:
        return await message.answer(
            "📭 Пока нет обучающих сценариев.",
            parse_mode=None
        )

    text = format_scenario_for_telegram(scenario)
    await message.answer(text, parse_mode=None)

