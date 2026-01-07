"""
File: src/core/agents/store_base.py

Purpose:
Base StoreAgent for MindForge DEMO.

Responsibilities:
- Represent a material store
- Provide price list to MasterAgent
- Respect AgentBase lifecycle
- Emit audit and system chat events
"""

from typing import List, Dict

from src.core.agents.base import AgentBase
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class StoreAgent(AgentBase):
    """
    Base class for store agents.
    """

    def __init__(
        self,
        *,
        agent_id: str,
        materials: List[Dict],
        delivery_price: int,
        delivery_days: int,
    ):
        super().__init__(agent_id=agent_id, role="store")
        self.materials = materials
        self.delivery_price = delivery_price
        self.delivery_days = delivery_days

    def get_price_list(self) -> Dict:
        """
        Return structured price list.
        """
        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="provide_price_list",
            decision="ALLOW",
            policy="STORE_CATALOG",
            reason="Store provided materials catalog",
        )

        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message="📦 Отправляю прайс-лист материалов",
        )

        return {
            "store_id": self.agent_id,
            "materials": self.materials,
            "delivery_price": self.delivery_price,
            "delivery_days": self.delivery_days,
        }
