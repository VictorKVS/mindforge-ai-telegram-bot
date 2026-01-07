"""
LLM Client module:
- supports mock LLM (tests / fallback)
- supports Local LLaMA via llama-cpp-python (GGUF)
"""

from pathlib import Path
import asyncio
from llama_cpp import Llama
from src.bot.config import settings


# -------------------------------------------------------------------
# 1. MOCK CLIENT (для тестов / fallback)
# -------------------------------------------------------------------
class LLMClient:
    """Mock LLM client."""

    def generate(self, prompt: str) -> str:
        return f"[MOCK LLM] Response to: {prompt}"


# -------------------------------------------------------------------
# 2. Local LLaMA Client
# -------------------------------------------------------------------
class LocalLLMClient:
    """Local LLaMA model using llama-cpp-python."""

    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return

        print("🔥 Local LLaMA loading...")

        model_path = Path(settings.LOCAL_LLM_MODEL_PATH).resolve()

        if not model_path.exists():
            raise RuntimeError(
                f"Local LLaMA model not found: {model_path}"
            )

        self._model = Llama(
            model_path=str(model_path),
            n_ctx=getattr(settings, "LOCAL_LLM_CTX", 4096),
            n_threads=getattr(settings, "LOCAL_LLM_THREADS", 8),
            n_gpu_layers=0,  # SAFE DEFAULT (portable)
            verbose=False,
        )

        print("✅ Local LLaMA loaded!")

    async def generate(self, prompt: str) -> str:
        """Async-safe text generation."""

        self._load_model()

        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(
            None,
            lambda: self._model(
                prompt,
                max_tokens=256,
                temperature=0.7,
            ),
        )

        return output["choices"][0]["text"].strip()


# -------------------------------------------------------------------
# 3. Factory
# -------------------------------------------------------------------
def get_llm_client():
    if getattr(settings, "LOCAL_LLM_ENABLED", False):
        return LocalLLMClient()

    return LLMClient()


# Singleton
llm_client = get_llm_client()
