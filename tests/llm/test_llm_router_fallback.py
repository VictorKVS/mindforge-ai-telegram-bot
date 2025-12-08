import pytest
from unittest.mock import MagicMock, patch
from src.bot.ai.llm_router import LLMRouter


def test_fallback_on_failure():
    router = LLMRouter()

    # Первый провайдер ломается
    router.providers["llama"].ask = MagicMock(side_effect=Exception("LLAMA FAIL"))

    # Второй провайдер работает
    router.providers["openai"].ask = MagicMock(return_value="[openai] ok")

    result = router.ask("hello", provider="llama")

    assert "[openai]" in result.lower()
    assert router.error_count >= 1
