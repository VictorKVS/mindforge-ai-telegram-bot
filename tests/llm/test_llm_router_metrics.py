from src.bot.ai.llm_router import LLMRouter


def test_metrics_reset():
    router = LLMRouter()

    router.ask("hello", provider="llama")
    router.ask("world", provider="llama")

    metrics_before = router.get_metrics()

    assert metrics_before["total_requests"] >= 2

    metrics_after = router.get_metrics(reset=True)

    assert metrics_after["total_requests"] >= 2
    assert router.total_requests == 0
    assert router.error_count == 0
