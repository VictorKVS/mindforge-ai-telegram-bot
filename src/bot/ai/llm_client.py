"""
LLM Client module: supports both mock LLM (for tests)
and Local LLaMA model via llama-cpp-python.
"""

from llama_cpp import Llama
from src.bot.config import settings


# -------------------------------------------------------------------
# 1. MOCK CLIENT (для тестов)
# -------------------------------------------------------------------
class LLMClient:
    """Mock LLM client for tests."""

    def get_context(self, query: str):
        # Тестовая модель всегда возвращает один и тот же контекст
        return ["Mock context"]

    def generate(self, prompt: str):
        # Тесты ожидают строго такую структуру ответа
        context = self.get_context(prompt)[0]
        return f"LLM response to: {prompt}\nContext: {context}"


# -------------------------------------------------------------------
# 2. Local LLaMA Client
# -------------------------------------------------------------------
class LocalLLMClient:
    """Local LLaMA model using llama-cpp-python (GGUF)."""

    def __init__(self):
        print("🔥 Local LLaMA loading...")

        self.model = Llama(
            model_path=settings.LOCAL_LLM_MODEL_PATH,
            n_ctx=settings.LOCAL_LLM_CTX,
            n_threads=settings.LOCAL_LLM_THREADS,
            n_gpu_layers=settings.LOCAL_LLM_GPU_LAYERS,
            verbose=False,
        )

        print("✅ Local LLaMA loaded!")

    async def generate(self, prompt: str) -> str:
        """Generate text using the local LLaMA model."""
        output = self.model(
            prompt,
            max_tokens=256,
            temperature=0.7,
        )

        return output["choices"][0]["text"].strip()


# -------------------------------------------------------------------
# 3. Factory — выбираем клиента
# -------------------------------------------------------------------
def get_llm_client():
    """
    Выбирает модель:
      - если LOCAL_LLM_ENABLED = true → LocalLLM
      - иначе → Mock LLM (для тестов)
    """
    if getattr(settings, "LOCAL_LLM_ENABLED", False):
        return LocalLLMClient()

    return LLMClient()


# Единственный экземпляр — используется по всему проекту
llm_client = get_llm_client()
