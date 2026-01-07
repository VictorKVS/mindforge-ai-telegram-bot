from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(lambda c: c.data == "demo_start")
async def demo_dashboard(callback: CallbackQuery):
    await callback.message.answer(
        "⚙️ *ЦЕНТР УПРАВЛЕНИЯ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👨‍🏫 *Агент-Учитель*\n"
        "Статус: 🟢 Онлайн\n"
        "Доверие: 6 / 6\n"
        "Роль: Security · Trust · Audit\n\n"
        "👷 *Агент-Строитель*\n"
        "Статус: 🟡 Free\n"
        "Доверие: 3 / 6\n"
        "Доступно: расчёты\n"
        "Заблокировано: платежи, интеграции\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔓 Активировать PRO", callback_data="demo_pro")],
            [
                InlineKeyboardButton(text="📊 Доверие", callback_data="demo_trust"),
                InlineKeyboardButton(text="▶️ Далее", callback_data="demo_order")
            ]
        ])
    )
    await callback.answer()
