# src/uag/sandbox/provider_registry.py

from typing import Dict, Any

from src.providers.fake_memory_provider import FakeMemoryProvider
from src.providers.fake_kb_provider import FakeKBProvider


class SandboxProviderRegistry:
    """
    Registry of sandbox-only providers.
    No access logic here.
    """

    def __init__(self):
        self._memory_provider = FakeMemoryProvider()
        self._kb_provider = FakeKBProvider()

    # -------- Memory --------

    def get_memory_provider(self) -> FakeMemoryProvider:
        return self._memory_provider

    # -------- Knowledge Base --------

    def get_kb_provider(self) -> FakeKBProvider:
        return self._kb_provider
