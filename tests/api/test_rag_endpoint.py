import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_rag_query_success():
    """Проверяем, что эндпоинт /rag/query работает нормально."""
    payload = {
        "query": "Tell me about AI",
        "k": 2
    }

    response = client.post("/rag/query", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "context" in data
    assert type(data["context"]) is list
    assert len(data["context"]) > 0  # обязательно есть контекст
    assert "tokens_used" in data


def test_rag_query_no_context():
    """Проверяем поведение, если RAG ничего не нашёл."""
    payload = {
        "query": "abracadabra",
        "k": 3
    }

    response = client.post("/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["context"][0] == "No context found"
