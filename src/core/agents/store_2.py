"""
File: src/core/agents/store_2.py

Purpose:
StoreAgent #2 — строительный магазин с упором на КАЧЕСТВО.

Role in DEMO:
- Предоставляет премиальные материалы
- Используется MasterAgent при стратегии QUALITY
- Работает через UAG-подобный интерфейс

Key difference from StoreAgent1:
- Выше качество
- Чуть выше цена
- Дольше доставка
"""

from typing import Dict, List

from src.core.agents.base import AgentBase
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class StoreAgent2(AgentBase):
    def __init__(self):
        super().__init__(agent_id="store-002", role="store")

        # -----------------------------
        # Каталог магазина (DEMO)
        # -----------------------------
        self.materials: List[Dict] = [
            {
                "material": "brick",
                "name": "Кирпич клинкерный М200",
                "gost": "ГОСТ 530-2012",
                "size_mm": "250×120×65",
                "weight_kg": 3.9,
                "color": "тёмно-красный",
                "manufacturer": "КлинкерПром",
                "composition": "обожжённая глина",
                "price_per_unit": 39.0,
                "quality_score": 9.4,
                "delivery_days": 4,
            },
            {
                "material": "cement",
                "name": "Цемент М600 (быстротвердеющий)",
                "gost": "ГОСТ 31108-2020",
                "weight_kg": 50,
                "price_per_unit": 610.0,
                "quality_score": 9.2,
                "delivery_days": 2,
            },
            {
                "material": "tool_level",
                "name": "Лазерный уровень профессиональный",
                "manufacturer": "GeoMaster",
                "price_per_unit": 7800.0,
                "quality_score": 9.6,
                "delivery_days": 1,
            },
        ]

    # ------------------------------------------------------------------
    # PUBLIC API (used by MasterAgent)
    # ------------------------------------------------------------------
    def get_price_list(self, material: str) -> List[Dict]:
        """
        Return price list for requested material.
        """

        offers = [m for m in self.materials if m["material"] == material]

        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=(
                f"📦 Прайс-лист (премиум) предоставлен\n"
                f"Материал: `{material}`\n"
                f"Позиций: `{len(offers)}`"
            ),
        )

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="provide_price",
            decision="ALLOW",
            policy="STORE_ACCESS",
            reason=f"Provided premium price list for {material}",
        )

        return offers
