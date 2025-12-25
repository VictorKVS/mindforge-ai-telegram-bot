"""

src/core/agents/registry.py
Purpose:
Global registry of running agents.
"""

from typing import Dict
from src.core.agents.base import AgentBase


class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, AgentBase] = {}

    def register(self, agent: AgentBase):
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> AgentBase | None:
        return self._agents.get(agent_id)

    def all(self):
        return list(self._agents.values())


# Global singleton
AGENTS = AgentRegistry()
