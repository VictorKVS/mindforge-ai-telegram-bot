"""
File: src/core/agents/store.py

Purpose:
StoreAgent for MindForge DEMO.

Role:
- Acts as a material supplier (mini-store)
- Provides price lists for construction materials
- Has its own delivery terms, discounts, specialties
- Does NOT make decisions, only responds to requests

Each StoreAgent represents an independent supplier
connected via UAG.
"""

from typing import Dict, List

from src.core.agents.base import AgentBase
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class StoreAgent(AgentBase):
    """
    Store / Supplier agent.
    """

    def __init__(
        self,
        *,
        agent_id: str,
        store_name: str,
        materials: List[Dict],
        delivery_days: int,
        delivery_price: int,
    ):
        """
        Initialize store agent.

        :param agent_id: Unique store agent ID
        :param store_name: Human-readable store name
        :param materials: List of materials with specs and prices
        :param delivery_days: Delivery time in days
        :param delivery_price: Delivery cost in RUB
        """
        super().__init__(agent_id=agent_id, role="store")

        self.store_name = store_name
        self.materials = materials
        self.delivery_days = delivery_days
        self.delivery_price = delivery_price

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_price_list(self) -> Dict:
        """
        Return full price list with delivery terms.
        """

        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=(
                f"🏪 Магазин: *{self.store_name}*\n"
                f"🚚 Доставка: {self.delivery_days} дн., {self.delivery_price} ₽\n"
                f"📦 Материалов: {len(self.materials)}"
            ),
        )

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="provide_price_list",
            decision="ALLOW",
            policy="STORE_PUBLIC_OFFER",
            reason=f"{self.store_name} price list provided",
        )

        return {
            "store_id": self.agent_id,
            "store_name": self.store_name,
            "delivery_days": self.delivery_days,
            "delivery_price": self.delivery_price,
            "materials": self.materials,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def has_material(self, material_code: str) -> bool:
        """
        Check if store has a specific material by code.
        """
        return any(m["code"] == material_code for m in self.materials)
