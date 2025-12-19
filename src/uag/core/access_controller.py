from .rbac import is_intent_allowed
from .validator import validate_request, UAGValidationError
from .audit import log_decision
from src.agents.loader import load_agent_spec

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


def check_agent_permission(payload: dict) -> tuple[bool, str]:
    """
    Проверка intent по AgentSpec.yaml
    """
    agent_id = payload.get("agent_id")
    intent = payload.get("intent")
    env = payload.get("env")

    spec = load_agent_spec(agent_id)

    role = spec.get("role", {})
    level = role.get("level", 0)

    capabilities = spec.get("capabilities", {})
    constraints = spec.get("constraints", {})

    # 1. Проверка окружения
    allowed_envs = constraints.get("allowed_envs", [])
    if env not in allowed_envs:
        return False, f"env '{env}' not allowed"

    # 2. Запрещённые интенты
    if intent in constraints.get("forbidden_intents", []):
        return False, f"intent '{intent}' is forbidden"

    # 3. Capabilities
    flat_caps = {
        cap
        for group in capabilities.values()
        for cap in group
    }

    if intent not in flat_caps:
        return False, f"intent '{intent}' not in agent capabilities"

    # 4. Минимальный уровень (пример логики)
    if intent == "build_foundation" and level < 3:
        return False, "insufficient agent level"

    return True, "allowed"

