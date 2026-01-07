def audit_log(request, status, reason):
    print({
        "agent": request.get("agent_id"),
        "intent": request.get("intent"),
        "target": request.get("target"),
        "status": status,
        "reason": reason
    })
