"""
File: src/core/agents/base.py

Purpose:
Canonical base class for all MindForge agents.

This class defines:
- Identity
- Lifecycle
- Audit integration
- Runtime state

All specific agents MUST inherit from this class.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

from src.core.audit_log import record_event


class AgentBase(ABC):
    """
    Canonical MindForge Agent.

    This class MUST NOT contain business logic.
    """

    def __init__(
        self,
        *,
        agent_id: str,
        role: str,
        version: str = "1.0",
    ) -> None:
        self.agent_id = agent_id
        self.role = role
        self.version = version

        self.started_at: datetime | None = None
        self.is_running: bool = False

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------
    def start(self) -> None:
        self.is_running = True
        self.started_at = datetime.utcnow()

        self.audit(
            action="agent_start",
            decision="ALLOW",
            reason="Agent started",
        )

    def stop(self) -> None:
        self.is_running = False

        self.audit(
            action="agent_stop",
            decision="DENY",
            reason="Agent stopped",
        )

    def status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "version": self.version,
            "running": self.is_running,
            "started_at": self.started_at,
        }

    # -------------------------------------------------
    # Audit
    # -------------------------------------------------
    def audit(
        self,
        *,
        action: str,
        decision: str,
        policy: str | None = None,
        reason: str | None = None,
    ) -> None:
        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action=action,
            decision=decision,
            policy=policy,
            reason=reason,
        )

    # -------------------------------------------------
    # Interaction
    # -------------------------------------------------
    @abstractmethod
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming event.

        Must be implemented by concrete agents.
        """
        raise NotImplementedError
