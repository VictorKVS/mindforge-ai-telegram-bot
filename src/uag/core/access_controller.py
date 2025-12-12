from .rbac import is_intent_allowed
from .validator import validate_request, UAGValidationError
from .audit import log_decision


class UAGAccessController:
    def handle(self, payload: dict, role: str = "agent_l0") -> dict:
        try:
            validate_request(payload)
        except UAGValidationError:
            log_decision(payload["agent_id"], payload.get("intent"), "DENY", payload["context"]["env"])
            return {"status": "denied", "reason": "schema_invalid"}

        intent = payload["intent"]
        env = payload["context"]["env"]

        if not is_intent_allowed(role, intent):
            log_decision(payload["agent_id"], intent, "DENY", env)
            return {"status": "denied", "reason": "rbac_violation"}

        log_decision(payload["agent_id"], intent, "ALLOW", env)
        return {"status": "allowed"}
