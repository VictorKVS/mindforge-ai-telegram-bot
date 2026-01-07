# src/core/audit_log.py
"""
File: src/core/audit_log.py

Purpose:
Audit log for MindForge (UAG-lite, DEMO-ready).

Responsibilities:
- Record ALLOW / DENY decisions from agents
- Store agent_id, agent_role, action, policy, reason
- Provide unified event format for dashboards
- Emit structured logs (SOC / SIEM ready)

Storage:
- In-memory (DEMO)
- Interface is stable for DB / MQ replacement
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
    Record an audit event from an agent.

    :param agent_id: Unique agent identifier
    :param agent_role: master | store | trainer | etc
    :param action: Logical action name
    :param decision: ALLOW | DENY
    :param policy: Policy ID if applicable
    :param reason: Human-readable explanation
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

    # --- Centralized structured logging ---
    logger.info(
        "AUDIT "
        f"agent_id={agent_id} "
        f"agent_role={agent_role} "
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
