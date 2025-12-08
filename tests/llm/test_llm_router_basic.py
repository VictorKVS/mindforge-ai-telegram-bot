import pytest
from unittest.mock import MagicMock, patch
from src.bot.ai.llm_router import LLMRouter


@pytest.fixture
def router():
    return LLMRouter()


def test_list_providers(router):
    providers = router.list_providers()
    assert "llama" in providers
    assert "openai" in providers


def test_set_default_valid(router):
    router.set_default("openai")
    assert router.active == "openai"


def test_set_default_invalid(router):
    with pytest.raises(ValueError):
        router.set_default("nonexistent")


def test_ask_basic(router):
    result = router.ask("hello", provider="llama")
    assert "[llama]" in result.lower()
