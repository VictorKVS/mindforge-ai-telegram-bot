# src/providers/fake_agent_provider.py

from typing import Dict


class FakeAgentProvider:
    """
    Fake Agent Provider (L3, sandbox-only)

    Представляет Agent B как provider.
    НЕ выполняет:
    - проверок прав доступа
    - фильтрации данных
    - логики безопасности

    Его задача — вернуть ПОЛНЫЕ данные capability.
    """

    def __init__(self):
        # agent_id -> capabilities
        self._agents: Dict[str, Dict[str, dict]] = {}

    def register_agent(self, agent_id: str) -> None:
        """
        Регистрирует агента-провайдера.
        """
        if agent_id not in self._agents:
            self._agents[agent_id] = {}

    def expose_capability(self, agent_id: str, capability_contract: dict) -> None:
        """
        Регистрирует capability для агента.

        capability_contract example:
        {
            "name": "get_public_profile",
            "exposed_fields": ["name", "service_type"],
            "full_data": {
                "name": "Agent B (Provider)",
                "service_type": "pricing",
                "internal_id": "secret_123"
            }
        }
        """
        if agent_id not in self._agents:
            raise ValueError(f"Agent '{agent_id}' is not registered")

        capability_name = capability_contract.get("name")
        if not capability_name:
            raise ValueError("Capability contract must contain 'name'")

        self._agents[agent_id][capability_name] = capability_contract

    def execute_capability(self, agent_id: str, capability_name: str) -> dict:
        """
        Выполняет capability и возвращает ПОЛНЫЕ данные.

        Никакой фильтрации.
        Никаких проверок прав.
        """
        if agent_id not in self._agents:
            raise ValueError(f"Unknown agent '{agent_id}'")

        capabilities = self._agents[agent_id]
        if capability_name not in capabilities:
            raise ValueError(
                f"Capability '{capability_name}' not found for agent '{agent_id}'"
            )

        capability = capabilities[capability_name]

        # Возвращаем ВСЕ данные — фильтрация будет в UAG
        return capability.get("full_data", {})
