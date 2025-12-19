
#src/bot/handlers/calendar_handler.py

"""
SpaceAI Training Center — Calendar / Planning Handler

Роль:
- Визуальная демонстрация планирования агентом
- Псевдо-календарь этапов работ
- UI-only слой (без бизнес-логики)

Важно:
- НЕ реальный календарь
- НЕ workflow engine
- Используется только для демо и объяснения
"""

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
import logging
from typing import List, Dict

router = Router()
logger = logging.getLogger(__name__)

# ============================================================
# DEMO DATA — имитация плана работ
# В реальной системе:
# данные из Audit Log + Agent Scheduler + AgentFS
# ============================================================

DEMO_PLAN: List[Dict] = [
    {"date": "20.12.2025", "task": "Подготовка площадки", "agent": "builder", "status": "done"},
    {"date": "21.12.2025", "task": "Расчёт объёмов материалов", "agent": "builder", "status": "done"},
    {"date": "22.12.2025", "task": "Запрос цен у магазинов", "agent": "builder → shop", "status": "done"},
    {"date": "23.12.2025", "task": "Выбор поставщика через UAG", "agent": "UAG", "status": "in_progress"},
    {"date": "24.12.2025", "task": "Оформление доставки", "agent": "shop", "status": "planned"},
]

STATUS_ICON = {
    "done": "✅",
    "in_progress": "⏳",
    "planned": "📌",
}

# ============================================================
# UI TEXTS
# ============================================================

CALENDAR_TEXTS = {
    "explain": (
        "🧠 <b>Логика планирования</b>\n\n"
        "Агент выстроил план, потому что:\n"
        "• без подготовки нельзя считать объёмы\n"
        "• без расчётов нельзя запрашивать цены\n"
        "• без цен нельзя выбрать поставщика\n"
        "• UAG проверяет допустимость каждого шага\n\n"
        "❌ Человек не вмешивается\n"
        "✔ Все решения объяснимы и логируются"
    )
}

# ============================================================
# KEYBOARD
# ============================================================

def calendar_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Обновить план", callback_data="calendar:refresh"),
                InlineKeyboardButton(text="🧠 Почему так?", callback_data="calendar:explain"),
            ],
            [
                InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu:main")
            ]
        ]
    )

# ============================================================
# FORMATTERS
# ============================================================

def format_plan() -> str:
    """
    Форматирует демо-план работ в HTML для Telegram.
    Используется исключительно для отображения.
    """
    lines = [
        "📅 <b>План работ агента</b>\n",
        "Агент самостоятельно планирует этапы,\n"
        "учитывая правила, ограничения и UAG.\n",
    ]

    for item in DEMO_PLAN:
        icon = STATUS_ICON.get(item["status"], "•")
        lines.append(
            f"{icon} <b>{item['date']}</b>\n"
            f"   {item['task']}\n"
            f"   <i>Исполнитель:</i> {item['agent']}\n"
        )

    lines.append(
        "\nℹ️ Это демонстрация.\n"
        "В реальной системе данные формируются\n"
        "из журнала действий агентов."
    )

    return "\n".join(lines)

# ============================================================
# SAFE UI UPDATE
# ============================================================

async def safe_edit_message(
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
            logger.warning(f"Calendar UI edit failed: {e}")

# ============================================================
# CALLBACK ROUTER
# ============================================================

@router.callback_query(lambda c: c.data and c.data.startswith("calendar:"))
async def calendar_router(call: CallbackQuery):
    action = call.data.split(":")[1]

    if action == "refresh":
        await safe_edit_message(call, format_plan(), calendar_menu())

    elif action == "explain":
        await safe_edit_message(call, CALENDAR_TEXTS["explain"], calendar_menu())

    else:
        logger.warning(f"Unknown calendar action: {action}")
        await call.answer("⚠️ Неизвестное действие", show_alert=False)
        return

    await call.answer(cache_time=1)
