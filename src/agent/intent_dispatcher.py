from src.uag.sandbox.gateway import UAGSandboxGateway


class IntentDispatcher:
    def __init__(self):
        self.uag = UAGSandboxGateway()

    def dispatch(self, intent_payload: dict) -> dict:
        payload = {
            "agent_id": "agent_l0",
            "intent": intent_payload["intent"],
            "query": intent_payload["params"],
            "context": {
                "env": "sandbox",
                "source": "agent"
            }
        }
        return self.uag.handle(payload)
