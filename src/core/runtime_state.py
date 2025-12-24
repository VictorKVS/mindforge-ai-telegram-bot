"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\core\\runtime_state.py

Purpose:
Runtime state holder for MindForge DEMO.

Responsibilities:
- Store current agent state (enabled / disabled)
- Store current policy mode (STRICT / DEMO / OFF)
- Provide async-safe snapshot access

This is a DEMO in-memory implementation.
In production this can be backed by:
- Redis
- DB
- Control Plane API
"""

import asyncio
from typing import Dict


class RuntimeState:
    """
    In-memory runtime state (DEMO).
    """

    def __init__(self):
        self._lock = asyncio.Lock()
        self._state: Dict = {
            "agent_enabled": False,
            "policy_mode": "DEMO",  # STRICT / DEMO / OFF
        }

    async def snapshot(self) -> Dict:
        """
        Return a copy of current runtime state.
        """
        async with self._lock:
            return dict(self._state)

    async def set_agent_enabled(self, enabled: bool) -> None:
        async with self._lock:
            self._state["agent_enabled"] = enabled

    async def set_policy_mode(self, mode: str) -> None:
        async with self._lock:
            self._state["policy_mode"] = mode


# Global singleton (DEMO scope)
STATE = RuntimeState()
