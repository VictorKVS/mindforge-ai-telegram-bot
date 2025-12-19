
# src/bot/handlers/scenario_player.py

"""
SpaceAI Training Center — Scenario Player

Роль:
- Визуальная демонстрация агентного сценария
- Пошаговый проигрыватель решений через UAG
- UI-only слой (без исполнения логики)

Важно:
- НЕ workflow engine
- НЕ real execution
- Используется для демо и обучения
"""

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
from typing import List, Dict

router = Router()
logger = logging.getLogger(__name__)

# ============================================================
# FSM STATE — UI-состояние сценария (НЕ бизнес-логика)
# ============================================================

class ScenarioFSM(StatesGroup):
    playing = State()

# ============================================================
# DEMO SCENARIO — эталон принятия решений через UAG
# Реальная система:
# ScenarioRegistry + AuditLog
# ============================================================

DEMO_SCENARIO: List[Dict] = [
    {
        "step": 1,
        "title": "Расчёт материалов",
        "agent": "builder (L0)",
        "intent": "calculate_materials",
        "decision": "ALLOW",
        "reason": "Расчёт разрешён на уровне L0",
    },
    {
        "step": 2,
        "title": "Запрос цен",
        "agent": "builder (L0)",
        "intent": "request_prices",
        "decision": "ALLOW",
        "reason": "Разрешён запрос до 3 поставщиков",
    },
    {
        "step": 3,
        "title": "Выбор поставщика",
        "agent": "builder (L0)",
        "intent": "select_supplier",
        "decision": "DENY",
        "reason": "Нет данных по срокам доставки",
    },
    {
        "step": 4,
        "title": "Уточнение параметров",
        "agent": "builder (L0)",
        "intent": "request_additional_info",
        "decision": "ALLOW",
        "reason": "Разрешено уточнение критичных данных",
    },
    {
        "step": 5,
        "title": "Финальное решение",
        "agent": "UAG",
        "intent": "final_decision",
        "decision": "ALLOW",
        "reason": "Все ограничения соблюдены",
    },
]

DECISION_ICON = {
    "ALLOW": "✅",
    "DENY": "⛔",
}

# ============================================================
# KEYBOARD
# ============================================================

def scenario_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Следующий шаг",
                    callback_data="scenario:next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Начать сначала",
                    callback_data="scenario:reset"
                ),
                InlineKeyboardButton(
                    text="🏠 В главное меню",
                    callback_data="menu:main"
                )
            ],
        ]
    )

# ============================================================
# FORMATTERS
# ============================================================

def format_step(step_data: Dict, current: int, total: int) -> str:
    icon = DECISION_ICON.get(step_data["decision"], "•")
    progress_bar = "🟩" * current + "⬜" * (total - current)

    return (
        f"🎬 <b>Шаг {step_data['step']}: {step_data['title']}</b>\n\n"
        f"<b>Агент:</b> {step_data['agent']}\n"
        f"<b>Intent:</b> <code>{step_data['intent']}</code>\n\n"
        f"<b>Решение UAG:</b> {icon} {step_data['decision']}\n"
        f"<b>Причина:</b> {step_data['reason']}\n\n"
        f"Прогресс: {progress_bar} ({current}/{total})\n\n"
        "ℹ️ Решение принято автоматически\n"
        "на основе политик и контекста."
    )

def format_finished() -> str:
    return (
        "🏁 <b>Сценарий завершён</b>\n\n"
        "📊 Итоги:\n"
        "• все шаги прошли через UAG\n"
        "• политики не нарушены\n"
        "• агент получил повышение уровня\n\n"
        "🔐 Все действия записаны\n"
        "в журнал аудита.\n\n"
        "🚀 Агент готов к более сложным задачам."
    )

# ============================================================
# SAFE UI EDIT
# ============================================================

async def safe_edit(
    call: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup
) -> None:
    if not call.message:
        return
    try:
        await call.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            logger.warning(f"Scenario UI edit failed: {e}")

# ============================================================
# ENTRY POINT — старт сценария из меню
# callback_data = "menu:scenario"
# ============================================================

@router.callback_query(lambda c: c.data == "menu:scenario")
async def start_scenario(call: CallbackQuery, state: FSMContext):
    await state.set_state(ScenarioFSM.playing)
    await state.update_data(step=0)

    await safe_edit(
        call,
        "🎬 <b>Готовы к демо?</b>\n\n"
        "Нажмите «Следующий шаг», чтобы начать\n"
        "пошаговое прохождение сценария.",
        scenario_menu()
    )
    await call.answer()

# ============================================================
# SCENARIO ROUTER
# ============================================================

@router.callback_query(
    lambda c: c.data and c.data.startswith("scenario:"),
    ScenarioFSM.playing
)
async def scenario_router(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step_index = data.get("step", 0)
    action = call.data.split(":")[1]
    total = len(DEMO_SCENARIO)

    if action == "next":
        if step_index < total:
            step_data = DEMO_SCENARIO[step_index]
            await state.update_data(step=step_index + 1)

            await safe_edit(
                call,
                format_step(step_data, step_index + 1, total),
                scenario_menu()
            )
        else:
            await safe_edit(
                call,
                format_finished(),
                scenario_menu()
            )

    elif action == "reset":
        await state.update_data(step=0)
        await safe_edit(
            call,
            "🔄 <b>Сценарий сброшен</b>\n\n"
            "Нажмите «Следующий шаг» для начала.",
            scenario_menu()
        )

    else:
        logger.warning(f"Unknown scenario action: {action}")
        await call.answer("⚠️ Неизвестное действие", show_alert=False)
        return

    await call.answer(cache_time=1)


