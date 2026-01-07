"""
File: src/core/agents/registry.py

Purpose:
Central registry for all agents in the system.

Responsibilities:
- Register / unregister agents
- Enforce unique agent_id
- Provide lookup by id / role
- Control agent lifecycle (start / stop)
"""

from typing import Dict, List

from src.core.agents.base import AgentBase


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, AgentBase] = {}

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------
    def register(self, agent: AgentBase) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(
                f"Agent with id '{agent.agent_id}' already registered"
            )

        self._agents[agent.agent_id] = agent

    def unregister(self, agent_id: str) -> None:
        if agent_id in self._agents:
            del self._agents[agent_id]

    # -------------------------------------------------
    # Lookup
    # -------------------------------------------------
    def get(self, agent_id: str) -> AgentBase | None:
        return self._agents.get(agent_id)

    def by_role(self, role: str) -> List[AgentBase]:
        return [
            agent for agent in self._agents.values()
            if agent.role == role
        ]

    def all(self) -> List[AgentBase]:
        return list(self._agents.values())

    def count(self) -> int:
        return len(self._agents)

    # -------------------------------------------------
    # Lifecycle control
    # -------------------------------------------------
    def start_all(self) -> None:
        for agent in self._agents.values():
            agent.start()

    def stop_all(self) -> None:
        for agent in self._agents.values():
            agent.stop()


# -------------------------------------------------
# Global registry (singleton by design)
# -------------------------------------------------
REGISTRY = AgentRegistry()
