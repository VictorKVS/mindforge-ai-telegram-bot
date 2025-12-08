from src.bot.ai.rag_engine import RAGEngine

def test_rag_engine_basic():
    rag = RAGEngine()
    result = rag.query("AI", k=2)

    assert type(result) is list
    assert len(result) > 0
    assert "AI" or "ai" in " ".join(result).lower()


def test_rag_engine_no_match():
    rag = RAGEngine()
    result = rag.query("no_such_topic", k=2)

    assert result == ["No context found"]
