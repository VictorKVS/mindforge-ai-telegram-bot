"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\core\\audit_log.py

Purpose:
Audit log for UAG-lite DEMO.

Responsibilities:
- Record ALLOW / DENY decisions
- Store policy, reason, timestamp
- Provide in-memory history for DEMO and debugging

This implementation is in-memory.
It can be replaced later by DB / SIEM / message queue
without changing the interface.
"""

from datetime import datetime
from typing import Dict, List


# In-memory audit storage (DEMO scope)
_AUDIT_EVENTS: List[Dict] = []


def record_event(
    *,
    action: str,
    decision: str,
    policy: str | None = None,
    reason: str | None = None,
) -> None:
    """
    Record an audit event.

    :param action: Logical action name (e.g. demo_allowed_action)
    :param decision: ALLOW or DENY
    :param policy: Policy ID if denied
    :param reason: Human-readable reason
    """

    event = {
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds"),
        "action": action,
        "decision": decision,
        "policy": policy,
        "reason": reason,
    }

    _AUDIT_EVENTS.append(event)


def get_events(limit: int = 10) -> List[Dict]:
    """
    Return last audit events (most recent first).
    """
    return list(reversed(_AUDIT_EVENTS[-limit:]))
