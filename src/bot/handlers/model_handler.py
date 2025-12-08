from aiogram import Router, types
from src.bot.ai.llm_router import LLMRouter

router = Router()
llm_router = LLMRouter()


# ----------------------------------------------------------
# /model — help
# ----------------------------------------------------------

@router.message(commands=["model"])
async def model_help(message: types.Message):
    await message.answer(
        "📡 *LLM Model Manager*\n\n"
        "/model list – список доступных моделей\n"
        "/model current – активная модель\n"
        "/model set <имя> – изменить модель\n"
        "/model health – проверить состояние моделей\n"
        "/model metrics – метрики роутера\n",
        parse_mode="Markdown"
    )


# ----------------------------------------------------------
# /model list
# ----------------------------------------------------------

@router.message(commands=["modellist"])
async def model_list(message: types.Message):
    providers = llm_router.list_providers()
    active = llm_router.active

    text = "🤖 *Available LLM Providers:*\n\n"
    for p in providers:
        marker = "🟢" if p == active else "⚪"
        text += f"{marker} `{p}`\n"

    await message.answer(text, parse_mode="Markdown")


# ----------------------------------------------------------
# /model current
# ----------------------------------------------------------

@router.message(commands=["modelcurrent"])
async def model_current(message: types.Message):
    await message.answer(
        f"🔍 Current LLM Provider: *{llm_router.active}*",
        parse_mode="Markdown"
    )


# ----------------------------------------------------------
# /model set <name>
# ----------------------------------------------------------

@router.message(commands=["modelset"])
async def model_set(message: types.Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("⚠ Использование: /modelset <имя_модели>")
        return

    provider = args[1]

    try:
        llm_router.set_default(provider)
        await message.answer(f"✅ Модель переключена на: *{provider}*", parse_mode="Markdown")

    except ValueError:
        await message.answer("❌ Неизвестный провайдер. Используйте /modellist")


# ----------------------------------------------------------
# /model health
# ----------------------------------------------------------

@router.message(commands=["modelhealth"])
async def model_health(message: types.Message):
    info = llm_router.health_check()

    text = "🩺 *LLM Health Status*\n\n"

    for p, st in info.items():
        if st["status"] == "healthy":
            text += f"🟢 {p}: OK\n"
        else:
            text += f"🔴 {p}: ERROR – `{st.get('error', 'unknown')}`\n"

    await message.answer(text, parse_mode="Markdown")


# ----------------------------------------------------------
# /model metrics
# ----------------------------------------------------------

@router.message(commands=["modelmetrics"])
async def model_metrics(message: types.Message):
    m = llm_router.get_metrics()

    text = (
        "📊 *LLM Router Metrics*\n\n"
        f"Total Requests: {m['total_requests']}\n"
        f"Errors: {m['error_count']}\n"
        f"Success Rate: {m['success_rate']:.2%}\n"
        f"Avg Latency: {m['avg_latency']:.3f} sec\n"
    )

    await message.answer(text, parse_mode="Markdown")
