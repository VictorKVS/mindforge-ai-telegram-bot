def decision_stats(events):
    allow = sum(1 for e in events if e["decision"] == "ALLOW")
    deny = sum(1 for e in events if e["decision"] == "DENY")

    return {
        "allow": allow,
        "deny": deny,
        "total": allow + deny,
    }
