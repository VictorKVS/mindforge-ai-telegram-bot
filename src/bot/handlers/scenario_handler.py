
# src/bot/handlers/scenario_handler.py


from aiogram import Router, types
from aiogram.filters import Command

from src.polygon.scenario_registry import ScenarioRegistry
from src.polygon.scenario_formatter import format_scenario_for_telegram

router = Router()


@router.message(Command("scenario"))
async def scenario_cmd(message: types.Message):
    parts = message.text.split(maxsplit=2)

    if len(parts) < 2:
        return await message.answer(
            "Использование:\n"
            "/scenario last\n"
            "/scenario list\n"
            "/scenario diff",
            parse_mode=None
        )

    sub = parts[1].lower()

    # -------------------------
    # /scenario last
    # -------------------------
    if sub == "last":
        scenario = ScenarioRegistry.yaml_last()
        if not scenario:
            return await message.answer(
                "📭 Пока нет YAML-сценариев.\nЗапусти /teacher teach",
                parse_mode=None
            )

        return await message.answer(
            format_scenario_for_telegram(scenario),
            parse_mode=None
        )

    # -------------------------
    # /scenario list
    # -------------------------
    if sub == "list":
        all_yaml = ScenarioRegistry.yaml_all()
        if not all_yaml:
            return await message.answer(
                "📭 YAML-сценариев пока нет.",
                parse_mode=None
            )

        txt = "📚 Последние сценарии:\n\n"
        for s in all_yaml[-10:]:
            txt += f"• {s.get('scenario_id','?')} ({s.get('created_at','?')})\n"

        return await message.answer(txt, parse_mode=None)

    # -------------------------
    # /scenario diff
    # -------------------------
    if sub == "diff":
        all_yaml = ScenarioRegistry.yaml_all()
        if len(all_yaml) < 2:
            return await message.answer(
                "Нужно минимум 2 сценария для diff.",
                parse_mode=None
            )

        a = all_yaml[-2]
        b = all_yaml[-1]

        a_intents = {st.get("intent") for st in a.get("steps", [])}
        b_intents = {st.get("intent") for st in b.get("steps", [])}

        added = sorted(b_intents - a_intents)
        removed = sorted(a_intents - b_intents)

        txt = (
            "🧾 DIFF сценариев\n\n"
            f"A: {a.get('scenario_id','?')}\n"
            f"B: {b.get('scenario_id','?')}\n\n"
            "➕ Добавилось:\n"
            + ("\n".join(f"• {x}" for x in added) if added else "—")
            + "\n\n"
            "➖ Ушло:\n"
            + ("\n".join(f"• {x}" for x in removed) if removed else "—")
        )

        return await message.answer(txt, parse_mode=None)

    return await message.answer(
        "Неизвестная команда.\nИспользуй: /scenario last | list | diff",
        parse_mode=None
    )
