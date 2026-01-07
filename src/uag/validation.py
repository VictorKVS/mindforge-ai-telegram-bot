REQUIRED_FIELDS = ["agent_id", "intent", "target", "query"]

def validate_request(req: dict):
    for f in REQUIRED_FIELDS:
        if f not in req:
            return False, f"missing_{f}"
    return True, None
