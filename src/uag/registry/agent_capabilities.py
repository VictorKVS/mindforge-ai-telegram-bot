# src/uag/registry/agent_capabilities.py

from typing import Dict, List


class CapabilityRegistry:
    """
    Capability Registry (L3)

    Хранит capability contracts для agent-to-agent interaction.
    Единственный источник правды о том:
    - кто что может запрашивать
    - у кого
    """

    def __init__(self):
        # target_agent_id -> capability_name -> contract
        self._registry: Dict[str, Dict[str, dict]] = {}

    def register_agent(self, agent_id: str) -> None:
        """
        Регистрирует агента как владельца capability.
        """
        if agent_id not in self._registry:
            self._registry[agent_id] = {}

    def register_capability(self, target_agent_id: str, capability_contract: dict) -> None:
        """
        Регистрирует capability contract.

        capability_contract example:
        {
            "name": "get_public_profile",
            "allowed_callers": ["agent_a"],
            "exposed_fields": ["name", "service_type"]
        }
        """
        if target_agent_id not in self._registry:
            raise ValueError(f"Target agent '{target_agent_id}' not registered")

        capability_name = capability_contract.get("name")
        if not capability_name:
            raise ValueError("Capability contract must contain 'name'")

        allowed_callers = capability_contract.get("allowed_callers")
        if not isinstance(allowed_callers, list):
            raise ValueError("Capability contract must contain 'allowed_callers' list")

        exposed_fields = capability_contract.get("exposed_fields")
        if not isinstance(exposed_fields, list):
            raise ValueError("Capability contract must contain 'exposed_fields' list")

        self._registry[target_agent_id][capability_name] = capability_contract

    def resolve_capability(self, target_agent_id: str, capability_name: str) -> dict:
        """
        Возвращает capability contract без проверок доступа.
        """
        if target_agent_id not in self._registry:
            raise ValueError(f"Unknown target agent '{target_agent_id}'")

        capabilities = self._registry[target_agent_id]
        if capability_name not in capabilities:
            raise ValueError(
                f"Capability '{capability_name}' not found for agent '{target_agent_id}'"
            )

        return capabilities[capability_name]

    def validate_caller(
        self,
        caller_agent_id: str,
        target_agent_id: str,
        capability_name: str
    ) -> bool:
        """
        Проверяет, разрешён ли caller для capability.
        """
        capability = self.resolve_capability(target_agent_id, capability_name)

        allowed_callers: List[str] = capability["allowed_callers"]
        return caller_agent_id in allowed_callers
