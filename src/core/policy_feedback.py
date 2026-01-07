"""
File: src/core/policy_feedback.py

Purpose:
Adaptive policy feedback loop (Policy-as-Code).
"""

from src.core.runtime_state import STATE
from src.core.logger import logger
from src.core.policy_loader import load_policy_config, resolve_risk_level


def apply_policy_feedback(risk: dict) -> dict:
    """
    Apply policy changes based on risk score and YAML policy config.
    """

    config = load_policy_config()
    thresholds = config["thresholds"]
    levels = config["levels"]

    score = risk["risk_score"]
    level = resolve_risk_level(score, thresholds)
    rules = levels[level]

    snap = STATE.get_sync_snapshot()

    decision = {
        "risk_score": score,
        "risk_level": level,
        "previous_policy": snap["policy_mode"],
        "new_policy": rules["policy_mode"],
        "agent_enabled": rules["agent_enabled"],
        "reason": f"Risk level = {level}",
    }

    # --- Apply ---
    STATE.set_policy_mode_sync(rules["policy_mode"])
    STATE.set_agent_enabled_sync(rules["agent_enabled"])

    # --- Log ---
    log_fn = {
        "info": logger.info,
        "warning": logger.warning,
        "critical": logger.error,
    }.get(rules.get("severity", "info"), logger.info)

    log_fn(
        "POLICY_FEEDBACK "
        f"risk_score={score} "
        f"level={level} "
        f"policy={rules['policy_mode']} "
        f"agent_enabled={rules['agent_enabled']}"
    )

    return decision
