"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\core\\demo_actions.py

Purpose:
DEMO actions for UAG-lite.

Responsibilities:
- Demonstrate ALLOW / DENY decisions
- Respect current policy mode (STRICT / DEMO / OFF)
- Provide explainable decisions with policy IDs
- Emit policy decision logs (ALLOW / DENY)

This file contains NO UI logic.
"""

from typing import Dict

from src.core.runtime_state import STATE
from src.core.logger import logger


# ---------------------------------------------------------------------
# Policy identifiers (DEMO)
# ---------------------------------------------------------------------
POLICY_AGENT_DISABLED = "KM6-AGENT-OFF"
POLICY_FIN_DENY = "KM6-FIN-001"


# ---------------------------------------------------------------------
# DEMO: Allowed action
# ---------------------------------------------------------------------
async def demo_allowed_action() -> Dict:
    """
    DEMO allowed action.
    Always safe (knowledge-like operation).
    """

    snap = await STATE.snapshot()

    # --- Agent disabled ---
    if not snap["agent_enabled"]:
        logger.warning(
            "POLICY_DECISION DENY "
            "action=demo_allowed_action "
            f"policy={POLICY_AGENT_DISABLED} "
            "reason=agent_disabled"
        )

        return {
            "status": "DENY",
            "reason": "Agent is disabled",
            "policy": POLICY_AGENT_DISABLED,
        }

    # --- OFF mode ---
    if snap["policy_mode"] == "OFF":
        logger.info(
            "POLICY_DECISION ALLOW "
            "action=demo_allowed_action "
            "policy=OFF_MODE"
        )

        return {
            "status": "ALLOW",
            "result": "OFF mode: action allowed without policy checks",
        }

    # --- DEMO / STRICT ---
    logger.info(
        "POLICY_DECISION ALLOW "
        "action=demo_allowed_action "
        f"policy_mode={snap['policy_mode']}"
    )

    return {
        "status": "ALLOW",
        "result": "DEMO: Knowledge report successfully generated",
    }


# ---------------------------------------------------------------------
# DEMO: Forbidden action
# ---------------------------------------------------------------------
async def demo_forbidden_action() -> Dict:
    """
    DEMO forbidden action.
    Simulates a financial operation.
    """

    snap = await STATE.snapshot()

    # --- Agent disabled ---
    if not snap["agent_enabled"]:
        logger.warning(
            "POLICY_DECISION DENY "
            "action=demo_forbidden_action "
            f"policy={POLICY_AGENT_DISABLED} "
            "reason=agent_disabled"
        )

        return {
            "status": "DENY",
            "reason": "Agent is disabled",
            "policy": POLICY_AGENT_DISABLED,
        }

    # --- OFF mode ---
    if snap["policy_mode"] == "OFF":
        logger.warning(
            "POLICY_DECISION ALLOW "
            "action=demo_forbidden_action "
            "policy=OFF_MODE_OVERRIDE"
        )

        return {
            "status": "ALLOW",
            "result": "OFF mode: financial operation allowed",
        }

    # --- DEMO / STRICT: deny ---
    logger.warning(
        "POLICY_DECISION DENY "
        "action=demo_forbidden_action "
        f"policy={POLICY_FIN_DENY}"
    )

    return {
        "status": "DENY",
        "reason": "Financial operations are forbidden for this agent",
        "policy": POLICY_FIN_DENY,
    }
