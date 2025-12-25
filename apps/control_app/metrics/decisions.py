"""
apps/control_app/metrics/decisions.py

Decision metrics for MindForge control app.
"""

def decision_metrics(events: list[dict]) -> dict:
    total = len(events)

    if total == 0:
        return {
            "total": 0,
            "allow": 0,
            "deny": 0,
            "allow_ratio": 0.0,
        }

    allow = sum(1 for e in events if e["decision"] == "ALLOW")
    deny = total - allow

    return {
        "total": total,
        "allow": allow,
        "deny": deny,
        "allow_ratio": round(allow / total, 2),
    }
