# src/bot/handlers/demo_handler.py

from aiogram import Router, types
from aiogram.filters import Command

from src.agent.builder_agent import BuilderAgent
from src.agent.shop_agent import ShopAgent

router = Router()


@router.message(Command("demo"))
async def demo_cmd(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or parts[1] != "build":
        return await message.answer(
            "Использование:\n/demo build",
            parse_mode=None
        )

    builder = BuilderAgent()
    shop = ShopAgent()

    await message.answer(builder.describe(), parse_mode=None)

    materials = builder.request_materials()
    await message.answer(
        f"📦 Запрос материалов:\n{materials}",
        parse_mode=None
    )

    prices = shop.get_price(materials)
    await message.answer(
        f"💰 Прайс от магазина:\n{prices}",
        parse_mode=None
    )

    delivery = shop.confirm_delivery()
    await message.answer(delivery, parse_mode=None)
