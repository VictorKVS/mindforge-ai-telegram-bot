import pytest
import asyncio
from src.bot.ai.llm_router import LLMRouter


@pytest.mark.asyncio
async def test_ask_async():
    router = LLMRouter()
    result = await router.ask_async("hello", provider="llama")
    assert "llama" in result.lower()
