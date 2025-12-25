# apps/control_app/metrics/policies.py

"""
Policy usage metrics.
"""

from collections import Counter


def policy_metrics(events: list[dict]) -> dict:
    policies = [e["policy"] for e in events if e.get("policy")]
    return dict(Counter(policies))
