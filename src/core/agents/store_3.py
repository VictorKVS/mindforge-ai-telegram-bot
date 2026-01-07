"""
File: src/core/agents/store_3.py

Purpose:
StoreAgent #3 — строительный магазин с упором на СКОРОСТЬ доставки.

Role in DEMO:
- Минимальные сроки поставки
- Используется MasterAgent при стратегии SPEED
- Склад рядом с объектом (Горелово)

Key characteristics:
- Доставка сегодня / завтра
- Среднее качество
- Цена выше, чем у дешёвого магазина, но ниже премиума
"""

from typing import Dict, List

from src.core.agents.base import AgentBase
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class StoreAgent3(AgentBase):
    def __init__(self):
        super().__init__(agent_id="store-003", role="store")

        # -----------------------------
        # Каталог магазина (DEMO)
        # -----------------------------
        self.materials: List[Dict] = [
            {
                "material": "brick",
                "name": "Кирпич строительный М150 (склад Горелово)",
                "gost": "ГОСТ 530-2012",
                "size_mm": "250×120×65",
                "weight_kg": 3.5,
                "color": "красный",
                "manufacturer": "РегионСтрой",
                "composition": "глина",
                "price_per_unit": 34.0,
                "quality_score": 8.1,
                "delivery_days": 1,
                "delivery_note": "Доставка сегодня манипулятором",
            },
            {
                "material": "cement",
                "name": "Цемент М500",
                "gost": "ГОСТ 31108-2020",
                "weight_kg": 50,
                "price_per_unit": 540.0,
                "quality_score": 8.0,
                "delivery_days": 1,
            },
            {
                "material": "tool_level",
                "name": "Пузырьковый уровень 1.5 м",
                "manufacturer": "StroyBasic",
                "price_per_unit": 1800.0,
                "quality_score": 7.8,
                "delivery_days": 0,
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
                f"⚡ Срочный прайс предоставлен\n"
                f"Материал: `{material}`\n"
                f"Склад: Горелово\n"
                f"Позиций: `{len(offers)}`"
            ),
        )

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="provide_price",
            decision="ALLOW",
            policy="STORE_ACCESS",
            reason=f"Provided fast delivery price list for {material}",
        )

        return offers
