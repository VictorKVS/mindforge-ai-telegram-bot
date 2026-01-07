# src/core/system_chat.py
"""
File: src/core/system_chat.py

Purpose:
Central System Chat for MindForge Agent Ecosystem.

Responsibilities:
- Act as a shared "room" where all agents publish messages
- Preserve message history for DEMO / dashboards
- Emit structured events for UI layers (Telegram / Web later)

IMPORTANT:
- NO Telegram code here
- NO agent logic here
- This is an infrastructure / observability layer
"""

from datetime import datetime
from typing import Dict, List, Callable, Optional


class SystemChat:
    """
    Central event bus / shared chat for all agents.
    """

    def __init__(self) -> None:
        self._messages: List[Dict] = []
        self._subscribers: List[Callable[[Dict], None]] = []

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------
    def emit(
        self,
        *,
        source: str,
        agent_id: str,
        agent_role: str,
        message: str,
        level: str = "INFO",
    ) -> None:
        """
        Emit a message into the system chat.

        :param source: who emitted (SYSTEM / agent_id)
        :param agent_id: emitting agent id
        :param agent_role: role of agent
        :param message: human-readable message
        :param level: INFO | WARN | ERROR
        """

        event = {
            "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds"),
            "source": source,
            "agent_id": agent_id,
            "agent_role": agent_role,
            "level": level,
            "message": message,
        }

        # Store in memory (DEMO)
        self._messages.append(event)

        # Notify subscribers (Telegram bridge, WebSocket, etc.)
        for subscriber in self._subscribers:
            try:
                subscriber(event)
            except Exception:
                # Subscriber errors must NOT break system
                pass

    # ------------------------------------------------------------------
    # Compatibility alias (older code)
    # ------------------------------------------------------------------
    def post(
        self,
        *,
        source: str,
        agent_id: str,
        agent_role: str,
        message: str,
        level: str = "INFO",
    ) -> None:
        """
        Backward-compatible alias.
        """
        self.emit(
            source=source,
            agent_id=agent_id,
            agent_role=agent_role,
            message=message,
            level=level,
        )

    # ------------------------------------------------------------------
    # Observability helpers
    # ------------------------------------------------------------------
    def history(self, limit: int = 50) -> List[Dict]:
        """
        Return last N system chat messages.
        """
        return self._messages[-limit:]

    def clear(self) -> None:
        """
        Clear chat history (useful between DEMO runs).
        """
        self._messages.clear()

    # ------------------------------------------------------------------
    # Subscription API (Telegram / Web)
    # ------------------------------------------------------------------
    def subscribe(self, callback: Callable[[Dict], None]) -> None:
        """
        Subscribe to new messages.

        callback(event: Dict) -> None
        """
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Dict], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback)


# ------------------------------------------------------------------
# Global singleton
# ------------------------------------------------------------------
SYSTEM_CHAT = SystemChat()
