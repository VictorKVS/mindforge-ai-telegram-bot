# apps/control_app/metrics/decisions.py

def decision_stats(events):
    total = len(events)
    allow = sum(1 for e in events if e["decision"] == "ALLOW")
    deny = sum(1 for e in events if e["decision"] == "DENY")

    return {
        "total": total,
        "allow": allow,
        "deny": deny,
        "allow_ratio": round(allow / total, 2) if total else 0,
    }
