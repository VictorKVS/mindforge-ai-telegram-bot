"""
File: src/core/audit_log.py

Purpose:
Audit log for MindForge / UAG-lite DEMO.

Responsibilities:
- Record ALLOW / DENY decisions
- Attach agent identity and role
- Store policy, reason, timestamp
- Emit audit events to centralized logger
- Provide in-memory history for DEMO and debugging

This implementation is in-memory.
It can be replaced later by DB / SIEM / message queue
without changing the interface.
"""

from datetime import datetime
from typing import Dict, List

from src.core.logger import logger


# ---------------------------------------------------------------------
# In-memory audit storage (DEMO scope)
# ---------------------------------------------------------------------
_AUDIT_EVENTS: List[Dict] = []


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------
def record_event(
    *,
    agent_id: str,
    agent_role: str,
    action: str,
    decision: str,
    policy: str | None = None,
    reason: str | None = None,
) -> None:
    """
    Record an audit event.

    :param agent_id: Unique agent identifier
    :param agent_role: Agent role (master / store / trainer)
    :param action: Logical action name
    :param decision: ALLOW or DENY
    :param policy: Policy ID if applicable
    :param reason: Human-readable reason
    """

    timestamp = datetime.utcnow().isoformat(timespec="seconds")

    event = {
        "timestamp_utc": timestamp,
        "agent_id": agent_id,
        "agent_role": agent_role,
        "action": action,
        "decision": decision,
        "policy": policy,
        "reason": reason,
    }

    # --- In-memory storage (DEMO) ---
    _AUDIT_EVENTS.append(event)

    # --- Centralized logging (SOC / SIEM ready) ---
    logger.info(
        "AUDIT "
        f"agent_id={agent_id} "
        f"role={agent_role} "
        f"decision={decision} "
        f"action={action} "
        f"policy={policy} "
        f"reason={reason} "
        f"timestamp={timestamp}"
    )


def get_events(limit: int = 10) -> List[Dict]:
    """
    Return last audit events (most recent first).

    :param limit: Max number of events
    """
    return list(reversed(_AUDIT_EVENTS[-limit:]))
