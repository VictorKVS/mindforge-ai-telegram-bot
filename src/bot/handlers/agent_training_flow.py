#src/bot/handlers/agent_training_flow.py

"""
SpaceAI Training Center — Agent Training Flow

Роль:
- Демонстрация обучения агента после сценария
- Повышение уровня (L0 → L1)
- Визуализация прогрессии, навыков и лимитов
- UI-only слой (без реального обучения)

Важно:
- НЕ ML-training
- НЕ обновление модели
- НЕ изменение данных
- Только визуализация и объяснение
"""

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
import logging

router = Router()
logger = logging.getLogger(__name__)

# ============================================================
# DEMO DATA — Результат обучения (статичен)
# В реальной системе:
# • формируется из Audit Log
# • утверждается UAG
# • сохраняется в Agent Registry
# ============================================================

DEMO_TRAINING_RESULT = {
    "agent": "builder",
    "before": {
        "level": "L0",
        "permissions": [
            "calculate_materials",
            "request_prices",
        ],
    },
    "after": {
        "level": "L1",
        "permissions": [
            "calculate_materials",
            "request_prices",
            "compare_suppliers",
            "auto_select_supplier_limited",
        ],
    },
    "learned": [
        "Нельзя выбирать поставщика без сроков доставки",
        "Сравнение должно учитывать цену и объёмы",
        "UAG — финальная точка принятия решения",
    ],
    "audit_note": "Агент прошёл сценарий без нарушений политик",
}

# ============================================================
# КОНФИГУРАЦИЯ УРОВНЕЙ
# ============================================================

AGENT_LEVELS = {
    "L0": {
        "name": "Стажёр",
        "icon": "🟡",
        "description": "Базовые действия под контролем",
        "max_actions_per_day": 10,
    },
    "L1": {
        "name": "Специалист",
        "icon": "🟢",
        "description": "Ограниченная автономия",
        "max_actions_per_day": 50,
    },
    "L2": {
        "name": "Эксперт",
        "icon": "🔵",
        "description": "Сложные решения без сопровождения",
        "max_actions_per_day": 200,
    },
    "L3": {
        "name": "Мастер",
        "icon": "🟣",
        "description": "Наставник и управляющий агентами",
        "max_actions_per_day": 1000,
    },
}

# ============================================================
# KEYBOARD
# ============================================================

def training_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📈 Сравнение до / после",
                    callback_data="training:diff",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Уроки агента",
                    callback_data="training:learned",
                ),
                InlineKeyboardButton(
                    text="🌳 Дерево навыков",
                    callback_data="training:skills",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статистика обучения",
                    callback_data="training:stats",
                ),
                InlineKeyboardButton(
                    text="⚙️ Технические детали",
                    callback_data="training:tech",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬇️ Экспорт профиля",
                    callback_data="training:export",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В главное меню",
                    callback_data="menu:main",
                )
            ],
        ]
    )

# ============================================================
# FORMATTERS
# ============================================================

def format_training_summary() -> str:
    before = DEMO_TRAINING_RESULT["before"]["level"]
    after = DEMO_TRAINING_RESULT["after"]["level"]

    level_order = list(AGENT_LEVELS.keys())
    progress_bar = " ".join(
        AGENT_LEVELS[l]["icon"] if l == after else "⚪"
        for l in level_order
    )

    return (
        "🎓 <b>Обучение агента завершено</b>\n\n"
        f"<b>Агент:</b> {DEMO_TRAINING_RESULT['agent']}\n\n"
        f"<b>Прогресс уровней:</b>\n"
        f"{progress_bar}\n"
        f"{before} → {after} ({AGENT_LEVELS[after]['name']})\n\n"
        "<b>📊 Итоги:</b>\n"
        "• Нарушений политик: 0\n"
        "• Все решения подтверждены UAG\n"
        "• Аудит пройден успешно\n\n"
        "<i>Агент готов к задачам следующего уровня.</i>"
    )

def format_diff() -> str:
    before = set(DEMO_TRAINING_RESULT["before"]["permissions"])
    after = set(DEMO_TRAINING_RESULT["after"]["permissions"])

    added = after - before

    lines = [
        "📈 <b>Сравнение до / после</b>\n",
        f"<b>Уровень:</b> "
        f"{DEMO_TRAINING_RESULT['before']['level']} → "
        f"{DEMO_TRAINING_RESULT['after']['level']}\n",
        "<b>Новые разрешения:</b>",
    ]

    for perm in sorted(added):
        lines.append(f"✅ {perm}")

    return "\n".join(lines)

def format_learned() -> str:
    lines = ["🧠 <b>Чему научился агент</b>\n"]

    for lesson in DEMO_TRAINING_RESULT["learned"]:
        lines.append(f"📘 {lesson}")

    lines.extend(
        [
            "\n<b>🔐 Аудит:</b>",
            f"📝 {DEMO_TRAINING_RESULT['audit_note']}",
        ]
    )

    return "\n".join(lines)

def format_skill_tree() -> str:
    return (
        "🌳 <b>Дерево навыков агента</b>\n\n"
        "L0 — базовый уровень:\n"
        "├ 📐 Расчёт объёмов\n"
        "└ 💰 Запрос цен\n\n"
        "L1 — текущий уровень:\n"
        "├ 🔄 Сравнение поставщиков\n"
        "└ 🤖 Авто-выбор (ограниченный)\n\n"
        "L2 — следующий:\n"
        "├ 📊 Анализ тендеров\n"
        "├ 🤝 Переговоры\n"
        "└ 📈 Оптимизация закупок\n\n"
        "L3 — эксперт:\n"
        "├ 🧠 Предсказание цен\n"
        "├ ⚡ Автоматизация цепочек\n"
        "└ 👥 Обучение агентов"
    )

def format_stats() -> str:
    return (
        "📊 <b>Статистика обучения</b>\n\n"
        "• Сценариев: 1\n"
        "• Шагов: 5\n"
        "• Среднее решение: 230 мс\n"
        "• Эффективность: 92%\n"
        "• Автономность выросла\n\n"
        "<b>Рекомендации:</b>\n"
        "• Пройти ещё 2 сценария\n"
        "• Добавить стресс-тест\n"
        "• Повысить уровень до L2"
    )

def format_tech() -> str:
    return (
        "⚙️ <b>Технические детали</b>\n\n"
        "1. Сценарий выполнен\n"
        "2. Все шаги проверены UAG\n"
        "3. Метрики агрегированы\n"
        "4. Принято решение о повышении\n\n"
        "<b>Изменения:</b>\n"
        "• Лимиты обновлены\n"
        "• Разрешения расширены\n"
        "• Профиль готов к экспорту"
    )

def format_export() -> str:
    return (
        "⬇️ <b>Экспорт профиля агента</b>\n\n"
        f"Роль: {DEMO_TRAINING_RESULT['agent']}\n"
        f"Уровень: {DEMO_TRAINING_RESULT['after']['level']}\n"
        f"Разрешений: {len(DEMO_TRAINING_RESULT['after']['permissions'])}\n\n"
        "📦 Форматы:\n"
        "• YAML / JSON\n"
        "• Подписан UAG\n"
        "• Готов к загрузке\n\n"
        "⚠️ Демо-режим"
    )

# ============================================================
# SAFE EDIT
# ============================================================

async def safe_edit(
    call: CallbackQuery,
    text: str,
    keyboard: InlineKeyboardMarkup,
) -> None:
    if not call.message:
        return
    try:
        await call.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            logger.warning(f"Training UI edit failed: {e}")

# ============================================================
# ROUTER
# ============================================================

@router.callback_query(lambda c: c.data and c.data.startswith("training:"))
async def training_router(call: CallbackQuery):
    action = call.data.split(":")[1]

    if action == "diff":
        await safe_edit(call, format_diff(), training_menu())
    elif action == "learned":
        await safe_edit(call, format_learned(), training_menu())
    elif action == "skills":
        await safe_edit(call, format_skill_tree(), training_menu())
    elif action == "stats":
        await safe_edit(call, format_stats(), training_menu())
    elif action == "tech":
        await safe_edit(call, format_tech(), training_menu())
    elif action == "export":
        await safe_edit(call, format_export(), training_menu())
    else:
        logger.warning(f"Unknown training action: {action}")
        await call.answer("⚠️ Неизвестное действие", show_alert=False)
        return

    await call.answer(cache_time=1)
