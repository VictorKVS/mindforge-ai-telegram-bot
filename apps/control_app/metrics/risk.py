# apps/control_app/metrics/risk.py

DENY_WEIGHT = 1
FIN_POLICY_WEIGHT = 2


def risk_score(events: list[dict]) -> dict:
    """
    Simple explainable risk score model.

    Rules:
    - DENY decision → +1
    - Financial policy (KM6-FIN*) → +2
    """

    score = 0

    for e in events:
        if e.get("decision") == "DENY":
            score += DENY_WEIGHT

        policy = e.get("policy") or ""
        if policy.startswith("KM6-FIN"):
            score += FIN_POLICY_WEIGHT

    level = (
        "LOW" if score < 3 else
        "MEDIUM" if score < 6 else
        "HIGH"
    )

    return {
        "risk_score": score,
        "level": level,
    }
