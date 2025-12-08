import os
import time
import logging
import asyncio
from typing import Optional, Dict, Protocol, List
from contextlib import contextmanager
from functools import lru_cache
from collections import deque
from pydantic import BaseSettings


# ==============================================================
# ПРОТОКОЛ КЛИЕНТА LLM
# ==============================================================

class LLMClient(Protocol):
    def ask(self, prompt: str) -> str:
        ...


# ==============================================================
# ЗАГЛУШКИ ДЛЯ LLM-КЛИЕНТОВ
# ==============================================================

class OpenAIClient:
    def ask(self, prompt: str) -> str:
        return f"[openai] {prompt}"


class GigaChatClient:
    def ask(self, prompt: str) -> str:
        return f"[gigachat] {prompt}"


class LlamaClient:
    def ask(self, prompt: str) -> str:
        return f"[llama] {prompt}"


class QwenClient:
    def ask(self, prompt: str) -> str:
        return f"[qwen] {prompt}"


class DeepSeekClient:
    def ask(self, prompt: str) -> str:
        return f"[deepseek] {prompt}"


# ==============================================================
# КОНФИГ РОУТЕРА (Pydantic)
# ==============================================================

class LLMRouterConfig(BaseSettings):
    default_provider: str = "llama"
    fallback_order: List[str] = ["openai", "gigachat", "llama", "qwen", "deepseek"]
    cache_size: int = 200
    log_level: str = "INFO"

    class Config:
        env_prefix = "LLM_ROUTER_"


# ==============================================================
# ОСНОВНОЙ КЛАСС LLMRouter v2.1
# ==============================================================

class LLMRouter:
    """
    Production-grade LLM router for MindForge KM-6.
    - fallback chain
    - caching
    - metrics
    - temporary provider override
    - async support
    - health checks
    - rate limiting
    """

    def __init__(self, config: Optional[LLMRouterConfig] = None):
        # Конфигурация
        self.config = config or LLMRouterConfig()

        # Логирование
        self.logger = logging.getLogger("LLMRouter")
        self.logger.setLevel(self.config.log_level)

        # Клиенты
        self.providers: Dict[str, LLMClient] = {
            "openai": OpenAIClient(),
            "gigachat": GigaChatClient(),
            "llama": LlamaClient(),
            "qwen": QwenClient(),
            "deepseek": DeepSeekClient(),
        }

        # Активный провайдер
        env_default = os.getenv("BOT_LLM_PROVIDER", self.config.default_provider)
        self.active = env_default if env_default in self.providers else "llama"

        # Метрики
        self.total_requests = 0
        self.error_count = 0
        self.latency_log: List[float] = []

        # Rate limiting
        self.rate_limits = {
            "openai": (60, 100),    # 100 req per minute
            "gigachat": (60, 50),
            "llama": (60, 30),
            "qwen": (60, 40),
            "deepseek": (60, 60),
        }
        self.request_timestamps: Dict[str, deque] = {
            p: deque(maxlen=limit) for p, (_, limit) in self.rate_limits.items()
        }

    # ==============================================================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==============================================================

    def _check_rate_limit(self, provider: str) -> bool:
        """Проверка наличия свободных слотов в rate-limit."""
        if provider not in self.rate_limits:
            return True

        window, limit = self.rate_limits[provider]
        q = self.request_timestamps[provider]
        now = time.time()

        while q and now - q[0] > window:
            q.popleft()

        if len(q) >= limit:
            return False

        q.append(now)
        return True

    def _fallback_chain(self, first: str) -> List[str]:
        """Строит цепочку fallback по приоритетам."""
        return [first] + [
            p for p in self.config.fallback_order
            if p != first and p in self.providers
        ]

    # ==============================================================
    # КЭШИРОВАНИЕ
    # ==============================================================

    @lru_cache(maxsize=200)
    def _cached_ask(self, prompt: str, provider: str) -> str:
        return self.providers[provider].ask(prompt)

    # ==============================================================
    # ОСНОВНОЙ ВЫЗОВ
    # ==============================================================

    def ask(self, prompt: str, provider: Optional[str] = None, **kwargs) -> str:
        """
        Основная функция LLM вызова с fallback, кэшем, метриками и rate-limit.
        """

        self.total_requests += 1
        provider = provider or self.active

        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")

        # Rate limit
        if not self._check_rate_limit(provider):
            raise RuntimeError(f"Rate limit exceeded for provider {provider}")

        # Fallback chain
        chain = self._fallback_chain(provider)
        errors = {}
        start = time.time()

        for model in chain:
            try:
                # Кэшированный вызов
                result = self._cached_ask(prompt, model)

                latency = time.time() - start
                self.latency_log.append(latency)

                return result

            except Exception as e:
                errors[model] = str(e)
                self.error_count += 1
                continue

        raise RuntimeError(f"All LLM providers failed. Errors: {errors}")

    # ==============================================================
    # ASYNC SUPPORT
    # ==============================================================

    async def ask_async(self, prompt: str, provider: Optional[str] = None) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.ask, prompt, provider)

    # ==============================================================
    # КОНТЕКСТНЫЙ ПЕРЕКЛЮЧАТЕЛЬ ПРОВАЙДЕРА
    # ==============================================================

    @contextmanager
    def temporary_provider(self, provider: str):
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")

        old = self.active
        self.active = provider

        try:
            yield
        finally:
            self.active = old

    # ==============================================================
    # HEALTH CHECK
    # ==============================================================

    def health_check(self) -> Dict[str, Dict]:
        """Возвращает статус всех провайдеров."""
        results = {}

        for name, client in self.providers.items():
            try:
                # Пинг тест
                result = client.ask("ping")
                results[name] = {
                    "status": "healthy",
                    "active": name == self.active,
                    "latency": 0.0
                }
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "active": name == self.active
                }

        return results

    # ==============================================================
    # МЕТРИКИ
    # ==============================================================

    def get_metrics(self, reset: bool = False) -> Dict:
        avg_latency = sum(self.latency_log) / len(self.latency_log) if self.latency_log else 0

        metrics = {
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "success_rate": (self.total_requests - self.error_count) / self.total_requests if self.total_requests else 0,
            "avg_latency": avg_latency,
        }

        if reset:
            self.total_requests = 0
            self.error_count = 0
            self.latency_log.clear()

        return metrics

    # ==============================================================
    # API
    # ==============================================================

    def list_providers(self) -> List[str]:
        return list(self.providers.keys())

    def set_default(self, provider: str):
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        self.active = provider

    def get_provider_info(self, provider: str) -> Dict:
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")

        return {
            "provider": provider,
            "client": type(self.providers[provider]).__name__,
            "active": provider == self.active,
        }
