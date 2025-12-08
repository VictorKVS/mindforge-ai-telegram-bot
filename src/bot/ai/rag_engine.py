class RAGEngine:
    """Simple mock RAG engine for testing purposes."""

    def query(self, query: str, k: int = 3):
        # If query contains known keyword → return mock context
        if query.lower() == "ai":
            return ["context 1 for AI", "context 2 for AI"]

        # Otherwise → return standard "not found"
        return ["No context found"]
