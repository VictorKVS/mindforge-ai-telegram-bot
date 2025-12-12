ALLOWED = {
    "agent_l0": ["get_price"]
}

def check_rbac(agent_id: str, intent: str):
    if intent in ALLOWED.get(agent_id, []):
        return True, None
    return False, "rbac_violation"
