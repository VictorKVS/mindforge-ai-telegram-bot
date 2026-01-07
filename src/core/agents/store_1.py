"""
File: src/core/agents/store_1.py

Purpose:
StoreAgent #1 — строительный магазин (кирпичи + базовые материалы).

Role in DEMO:
- Предоставляет прайс-лист мастеру
- Участвует в выборе по стратегии PRICE / QUALITY / SPEED
- Работает через UAG-подобный интерфейс

Design:
- Максимально простой
- Реалистичные параметры (ГОСТ, вес, размеры)
- Без бизнес-логики мастера
"""

from typing import Dict, List

from src.core.agents.base import AgentBase
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class StoreAgent1(AgentBase):
    def __init__(self):
        super().__init__(agent_id="store-001", role="store")

        # -----------------------------
        # Каталог магазина (DEMO)
        # -----------------------------
        self.materials: List[Dict] = [
            {
                "material": "brick",
                "name": "Кирпич керамический М150",
                "gost": "ГОСТ 530-2012",
                "size_mm": "250×120×65",
                "weight_kg": 3.5,
                "color": "красный",
                "manufacturer": "Завод №1",
                "composition": "глина",
                "price_per_unit": 28.0,
                "quality_score": 7.5,
                "delivery_days": 2,
            },
            {
                "material": "cement",
                "name": "Цемент М500",
                "gost": "ГОСТ 31108-2020",
                "weight_kg": 50,
                "price_per_unit": 420.0,
                "quality_score": 8.0,
                "delivery_days": 1,
            },
            {
                "material": "tool_level",
                "name": "Строительный уровень 1м",
                "manufacturer": "StroyPro",
                "price_per_unit": 950.0,
                "quality_score": 7.0,
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
                f"📦 Прайс-лист предоставлен\n"
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
            reason=f"Provided price list for {material}",
        )

        return offers
