"""
Minimal LLM Router for MindForge AI Bot.
Works directly with llm_client (local LLaMA or Mock).
No fallback, no cache, no rate limits — pure MVP.
"""

"""
Minimal LLM Router for MindForge AI Bot.
Uses local LLaMA via llm_client.
"""

import os
from datetime import datetime
from src.bot.ai.llm_client import llm_client

# -------------------------------------------------------
# Загружаем системный промпт
# -------------------------------------------------------

PROMPT_PATH = "src/bot/prompts/assistant_main.txt"


def load_system_prompt():
    if os.path.exists(PROMPT_PATH):
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "Ты — MindForge Assistant. Помогай пользователю безопасно и корректно."


SYSTEM_PROMPT = load_system_prompt()


# -------------------------------------------------------
# Главная функция маршрутизации
# -------------------------------------------------------

async def route(user_message: str) -> str:
    """
    Объединяем системный промпт + дату + сообщение пользователя,
    отправляем в локальную модель LLaMA.
    """

    today = datetime.now().strftime("%d.%m.%Y")

    final_prompt = (
        SYSTEM_PROMPT.strip()
        + f"\n\n[ТЕКУЩАЯ ДАТА] {today}"
        + f"\n[ПОЛЬЗОВАТЕЛЬ]\n{user_message}"
        + "\n[ОТВЕТ АССИСТЕНТА]\n"
    )

    # ЛОГ (но не ломает импорт)
    print("\n====== LLM ROUTER PROMPT ======")
    print(final_prompt)
    print("================================\n")

    try:
        response = await llm_client.generate(final_prompt)
        return response.strip()

    except Exception as e:
        return f"[LLM Router Error] {str(e)}"
