"""
Minimal LLM Router for MindForge AI Bot.
Works directly with llm_client (local LLaMA or Mock).
No fallback, no cache, no rate limits — pure MVP.
"""

from src.bot.ai.llm_client import llm_client


async def route(prompt: str) -> str:
    """
    Main routing function.
    Accepts a prompt and returns LLM response via selected client.
    """

    try:
        response = await llm_client.generate(prompt)
        return response

    except Exception as e:
        # Do NOT break the bot — return safe error
        return f"[LLM Router Error] {str(e)}"
