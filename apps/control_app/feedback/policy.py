"""
feedback/policy.py

Render policy feedback decision.
"""

def render_policy_feedback(decision: dict) -> str:
    return (
        f"Policy change:\n"
        f"- From: {decision['previous_policy']}\n"
        f"- To:   {decision['new_policy']}\n"
        f"- Agent enabled: {decision['agent_enabled']}\n"
        f"- Reason: {decision['reason']}"
    )
