
"""
File: src/core/runtime_state.py

Purpose:
Runtime state holder for MindForge DEMO.
"""

import asyncio
from typing import Dict

class RuntimeState:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._state: Dict = {
            "agent_enabled": False,
            "policy_mode": "DEMO",
        }

    async def snapshot(self) -> Dict:
        async with self._lock:
            return dict(self._state)

    async def set_agent_enabled(self, enabled: bool) -> None:
        async with self._lock:
            self._state["agent_enabled"] = enabled

    async def set_policy_mode(self, mode: str) -> None:
        async with self._lock:
            self._state["policy_mode"] = mode

STATE = RuntimeState()
