from unittest.mock import MagicMock
from src.bot.ai.llm_router import LLMRouter


def test_cached_ask():
    router = LLMRouter()

    # реальный вызов выполняется 1 раз
    router.providers["llama"].ask = MagicMock(return_value="[llama] cached")

    r1 = router.ask("prompt1", provider="llama")
    r2 = router.ask("prompt1", provider="llama")

    assert r1 == r2
    router.providers["llama"].ask.assert_called_once()
