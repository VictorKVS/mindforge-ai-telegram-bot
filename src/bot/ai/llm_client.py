class LLMClient:
    """Mock LLM client for tests."""

    def get_context(self, query: str):
        # Test expects this exact string
        return ["Mock context"]

    def generate(self, prompt: str):
        # Test requires merged prompt + context
        context = self.get_context(prompt)[0]
        return f"LLM response to: {prompt}\nContext: {context}"
