# uag/gateway.py

def handle(request: dict) -> dict:
    required_fields = ["agent_id", "intent", "target", "query"]

    for field in required_fields:
        if field not in request:
            return {"status": "denied", "reason": f"missing_{field}"}

    # L0: allow only get_price
    if request["intent"] != "get_price":
        return {"status": "denied", "reason": "intent_not_allowed"}

    return {
        "status": "ok",
        "data": {
            "message": "stub response from UAG"
        }
    }
