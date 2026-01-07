import json
from pathlib import Path
from jsonschema import validate, ValidationError

from src.uag.core.access_controller import check_agent_permission
from src.uag.core.audit import log_decision
from src.agents.loader import load_agent_spec


SCHEMA_PATH = Path("contracts/uag/uag_request_schema.json")


class UAGValidationError(Exception):
    pass


def validate_request(payload: dict) -> dict:
    """
    Полная валидация UAG-запроса:
    1) JSON Schema
    2) AgentSpec / capabilities
    3) Audit
    """

    # --------------------------------------------------
    # 1. JSON Schema validation
    # --------------------------------------------------
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        raise UAGValidationError(f"Schema validation error: {e.message}")

    # --------------------------------------------------
    # 2. Agent permission check (AgentSpec)
    # --------------------------------------------------
    allowed, reason = check_agent_permission(payload)

    agent_id = payload.get("agent_id")
    intent = payload.get("intent")
    env = payload.get("env")

    # Загружаем AgentSpec ОДИН РАЗ
    spec = load_agent_spec(agent_id)

    decision = "ALLOW" if allowed else "DENY"

    # --------------------------------------------------
    # 3. Audit log (single source of truth)
    # --------------------------------------------------
    audit_record = {
        "agent_id": agent_id,
        "intent": intent,
        "env": env,
        "decision": decision,
        "reason": reason,

        # Контекст агента
        "agent_role": spec["role"]["name"],
        "agent_level": spec["role"]["level"],
        "agent_spec_version": spec.get("version", "unknown"),
    }

    log_decision(audit_record)

    # --------------------------------------------------
    # 4. Final decision
    # --------------------------------------------------
    if not allowed:
        return {
            "decision": "DENY",
            "reason": reason
        }

    return {
        "decision": "ALLOW",
        "reason": "validated"
    }

