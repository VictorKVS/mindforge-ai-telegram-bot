# src/core/demo_actions.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\core\\demo_actions.py

Purpose:
DEMO actions for UAG-lite.

Responsibilities:
- Demonstrate ALLOW / DENY decisions
- Respect current policy mode (STRICT / DEMO / OFF)
- Provide explainable decisions with policy IDs

This file contains NO UI logic.
"""

from typing import Dict
from src.core.runtime_state import STATE

# Policy identifiers (DEMO)
POLICY_AGENT_DISABLED = "KM6-AGENT-OFF"
POLICY_FIN_DENY = "KM6-FIN-001"


async def demo_allowed_action() -> Dict:
    """
    DEMO allowed action.
    Always safe (knowledge-like operation).
    """
    snap = await STATE.snapshot()

    if not snap["agent_enabled"]:
        return {
            "status": "DENY",
            "reason": "Agent is disabled",
            "policy": POLICY_AGENT_DISABLED,
        }

    # In OFF mode everything is allowed
    if snap["policy_mode"] == "OFF":
        return {
            "status": "ALLOW",
            "result": "OFF mode: action allowed without policy checks",
        }

    # STRICT and DEMO both allow this action
    return {
        "status": "ALLOW",
        "result": "DEMO: Knowledge report successfully generated",
    }


async def demo_forbidden_action() -> Dict:
    """
    DEMO forbidden action.
    Simulates a financial operation.
    """
    snap = await STATE.snapshot()

    if not snap["agent_enabled"]:
        return {
            "status": "DENY",
            "reason": "Agent is disabled",
            "policy": POLICY_AGENT_DISABLED,
        }

    # OFF mode: explicitly allow forbidden actions
    if snap["policy_mode"] == "OFF":
        return {
            "status": "ALLOW",
            "result": "OFF mode: financial operation allowed",
        }

    # STRICT and DEMO: deny financial operations
    return {
        "status": "DENY",
        "reason": "Financial operations are forbidden for this agent",
        "policy": POLICY_FIN_DENY,
    }
