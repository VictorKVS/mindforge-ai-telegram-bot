from unittest.mock import MagicMock
from src.bot.ai.llm_router import LLMRouter


def test_health_check():
    router = LLMRouter()

    # Один провайдер работает
    router.providers["llama"].ask = MagicMock(return_value="ok")

    # Один падает
    router.providers["openai"].ask = MagicMock(side_effect=Exception("FAIL"))

    status = router.health_check()

    assert status["llama"]["status"] == "healthy"
    assert status["openai"]["status"] == "error"
