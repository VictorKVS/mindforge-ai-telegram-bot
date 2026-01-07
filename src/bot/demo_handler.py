from aiogram import Router
from aiogram.types import CallbackQuery
import logging

router = Router()
logger = logging.getLogger("mindforge.handlers.demo")


@router.callback_query(lambda c: c.data == "demo:start")
async def demo_start(callback: CallbackQuery):
    user = callback.from_user

    logger.info(
        "DEMO_START | user_id=%s | username=%s",
        user.id,
        user.username
    )

    await callback.answer()  # убирает "часики"

    await callback.message.answer(
        "🔍 *DEMO STEP 1 — ИНИЦИАЛИЗАЦИЯ*\n\n"
        "• UAG создаёт сессию\n"
        "• Включается DEMO-контур\n"
        "• Назначается trust-профиль\n"
        "• Все действия логируются\n\n"
        "_Это контролируемая среда_",
        parse_mode="Markdown"
    )
