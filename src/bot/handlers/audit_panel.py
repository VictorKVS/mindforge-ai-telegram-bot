from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data.startswith("why_"))
async def why_uag(callback: CallbackQuery):
    await callback.message.answer(
        "🔍 *ПОЧЕМУ ТАК (UAG)*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "• Действие проверено политиками\n"
        "• Агент имеет право принять заказ\n"
        "• Включён DEMO-контур (sandbox)\n"
        "• Все параметры валидированы\n"
        "• Событие зафиксировано в аудит-логе\n\n"
        "_Никаких автономных решений._",
        parse_mode="Markdown"
    )
    await callback.answer()
