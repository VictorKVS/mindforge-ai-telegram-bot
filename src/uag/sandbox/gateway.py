from src.uag.core.access_controller import UAGAccessController
from .provider_registry import PROVIDERS


class UAGSandboxGateway:
    def __init__(self):
        self.controller = UAGAccessController()

    def handle(self, payload: dict) -> dict:
        decision = self.controller.handle(payload)

        if decision["status"] != "allowed":
            return decision

        intent = payload["intent"]
        provider = PROVIDERS.get(intent)

        if not provider:
            return {"status": "denied", "reason": "unknown_provider"}

        result = provider(payload["query"])
        return {
            "status": "ok",
            "data": result
        }
