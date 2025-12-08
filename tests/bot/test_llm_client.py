from src.bot.ai.llm_client import LLMClient

class MockResponse:
    """Эмуляция ответа HTTP-клиента."""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


def mock_post(url, json):
    return MockResponse({"context": ["Mock context"], "tokens_used": 10})


def test_llm_client_context(monkeypatch):
    monkeypatch.setattr("httpx.post", mock_post)

    client = LLMClient()
    context = client.get_context("AI")

    assert context == ["Mock context"]


def test_llm_client_generate(monkeypatch):
    monkeypatch.setattr("httpx.post", mock_post)

    client = LLMClient()
    result = client.generate("Explain AI")

    assert "Explain AI" in result
    assert "Mock context" in result
