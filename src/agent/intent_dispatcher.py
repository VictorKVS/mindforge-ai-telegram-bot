# src/agent/intent_dispatcher.py

class IntentDispatcher:
    def __init__(self, uag_gateway):
        self.uag_gateway = uag_gateway  # ← зависимость от UAG

    def dispatch(self, intent_name: str, params: dict):
        intent = {
            "message_type": "INTENT",
            "sender": "agent_master_001",
            "target": "central_supply_hub",
            "level": 3,
            "intent": {"name": intent_name, "params": params}
        }
        return self.uag_gateway.send_intent(intent)