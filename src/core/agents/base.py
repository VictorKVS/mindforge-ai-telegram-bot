"""
File: src/core/agents/base.py

Purpose:
Canonical base class for all agents.

Responsibilities:
- Agent identity (id, role)
- Lifecycle control (start / stop)
- Audit helper
- Store last decision for explanation
"""

from src.core.audit_log import record_event


class AgentBase:
    def __init__(self, *, agent_id: str, role: str) -> None:
        self.agent_id = agent_id
        self.role = role
        self.is_running: bool = False
        self._last_decision: dict | None = None

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------
    def start(self) -> None:
        self.is_running = True

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="agent_start",
            decision="ALLOW",
            policy="LIFECYCLE",
            reason="Agent started",
        )

    def stop(self) -> None:
        self.is_running = False

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="agent_stop",
            decision="DENY",
            policy="LIFECYCLE",
            reason="Agent stopped",
        )

    # -------------------------------------------------
    # Decision handling
    # -------------------------------------------------
    def _store_decision(self, decision: dict) -> None:
        self._last_decision = decision

    def get_last_decision(self) -> dict | None:
        return self._last_decision

  
    # ------------------------------------------------------------------
    # DEMO safety stubs (НЕ бизнес-логика)
    # ------------------------------------------------------------------
    def evaluate_material_access(self, material: str) -> bool:
        """
        DEMO stub.
        Базовый агент не принимает решений.
        """
        return False
