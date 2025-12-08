from src.bot.ai.llm_router import LLMRouter


def test_temporary_provider():
    router = LLMRouter()
    original = router.active

    with router.temporary_provider("openai"):
        assert router.active == "openai"

    assert router.active == original
