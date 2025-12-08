from time import sleep
from src.bot.ai.llm_router import LLMRouter


def test_rate_limit():
    router = LLMRouter()

    provider = "llama"

    # Заполняем лимит
    for _ in range(router.rate_limits[provider][1]):
        assert router._check_rate_limit(provider) is True

    # Следующий вызов должен быть заблокирован
    assert router._check_rate_limit(provider) is False
