"""
File: apps/control_app/app.py

Purpose:
MindForge Control Dashboard (CLI, DEMO).

Responsibilities:
- Read audit events
- Compute metrics (decisions, risk, policies)
- Apply adaptive policy feedback
- Log all control-plane activity
- Display explainable system state

NO UI framework.
NO Telegram dependencies.
"""

from apps.control_app.data_sources.audit import load_audit_events
from apps.control_app.metrics.risk import risk_score
from apps.control_app.metrics.decisions import decision_metrics
from apps.control_app.metrics.policies import policy_stats
from apps.control_app.feedback.policy import render_policy_feedback

from src.core.policy_feedback import apply_policy_feedback
from src.core.logger import logger


def print_block(title: str):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


def main():
    logger.info("CONTROL_APP_START")

    events = load_audit_events(limit=50)
    logger.info(f"CONTROL_APP_LOADED_EVENTS count={len(events)}")

    print_block("🧠 MindForge Control Dashboard")

    if not events:
        logger.info("CONTROL_APP_IDLE no_audit_events")
        print("ℹ️ No audit events yet. System is idle.")
        return

    # --- Metrics ---
    decisions = decision_metrics(events)
    risk = risk_score(events)
    policies = policy_stats(events)

    logger.info(
        "CONTROL_APP_METRICS "
        f"allow={decisions['allow']} "
        f"deny={decisions['deny']} "
        f"risk_score={risk['risk_score']} "
        f"risk_level={risk['level']}"
    )

    # --- Feedback ---
    feedback = apply_policy_feedback(risk)

    logger.info(
        "CONTROL_APP_FEEDBACK_APPLIED "
        f"previous_policy={feedback['previous_policy']} "
        f"new_policy={feedback['new_policy']} "
        f"agent_enabled={feedback['agent_enabled']}"
    )

    # --- Output ---
    print_block("📊 Decisions")
    print(decisions)

    print_block("⚠ Risk")
    print(risk)

    print_block("🛡 Policies")
    print(policies)

    print_block("🔁 Policy Feedback Applied")
    print(render_policy_feedback(feedback))

    logger.info("CONTROL_APP_FINISHED")


if __name__ == "__main__":
    main()
