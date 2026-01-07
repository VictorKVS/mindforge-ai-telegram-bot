# src/core/agents/store.py

from src.core.agents.base import AgentBase

class StoreAgent(AgentBase):
    def __init__(
        self,
        *,
        agent_id: str,
        name: str,
        materials: list[dict],
        delivery_price: int,
        delivery_days: int,
    ):
        super().__init__(agent_id=agent_id, role="store")
        self.name = name
        self.materials = materials
        self.delivery_price = delivery_price
        self.delivery_days = delivery_days

    def get_price_list(self) -> list[dict]:
        return self.materials
