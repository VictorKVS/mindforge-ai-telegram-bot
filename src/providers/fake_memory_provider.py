# src/providers/fake_memory_provider.py

import time
from typing import Any, Dict, Optional


class FakeMemoryProvider:
    """
    Fake Memory Provider (L2)
    -------------------------
    - sandbox-only
    - in-memory
    - intent-driven
    - no persistence
    - no access logic
    """

    def __init__(self, default_ttl: int = 3600):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._ttl: Dict[str, float] = {}
        self.default_ttl = default_ttl

    # -------------------------
    # Internal helpers
    # -------------------------

    def _make_key(self, agent_id: str, scope: str, key: str) -> str:
        return f"{agent_id}:{scope}:{key}"

    def _is_expired(self, full_key: str) -> bool:
        expires_at = self._ttl.get(full_key)
        if expires_at is None:
            return False
        return time.time() > expires_at

    def _cleanup_if_expired(self, full_key: str) -> None:
        if self._is_expired(full_key):
            self._store.pop(full_key, None)
            self._ttl.pop(full_key, None)

    # -------------------------
    # Public API (called by UAG)
    # -------------------------

    def read(
        self,
        agent_id: str,
        scope: str,
        key: str
    ) -> Optional[Any]:
        """
        memory_read
        """
        full_key = self._make_key(agent_id, scope, key)
        self._cleanup_if_expired(full_key)

        record = self._store.get(full_key)
        if record is None:
            return None

        return record["value"]

    def write(
        self,
        agent_id: str,
        scope: str,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """
        memory_write
        """
        full_key = self._make_key(agent_id, scope, key)

        self._store[full_key] = {
            "value": value,
            "created_at": time.time()
        }

        effective_ttl = ttl if ttl is not None else self.default_ttl
        self._ttl[full_key] = time.time() + effective_ttl

    def clear(
        self,
        agent_id: str,
        scope: str,
        key: Optional[str] = None
    ) -> None:
        """
        memory_clear
        """
        if key:
            full_key = self._make_key(agent_id, scope, key)
            self._store.pop(full_key, None)
            self._ttl.pop(full_key, None)
            return

        # clear whole scope for agent (explicit)
        prefix = f"{agent_id}:{scope}:"
        keys_to_delete = [k for k in self._store if k.startswith(prefix)]

        for k in keys_to_delete:
            self._store.pop(k, None)
            self._ttl.pop(k, None)
