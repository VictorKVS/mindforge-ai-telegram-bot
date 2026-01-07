"""
File: src/core/agents/master.py

Purpose:
MasterAgent — управляющий агент строителя.

Responsibilities:
- Проверка лицензии на материалы
- Выбор стратегии (PRICE / QUALITY / SPEED)
- Запрос прайсов у StoreAgents
- Выбор оптимального магазина
- Фиксация решения в audit_log
- Передача контекста TrainerAgent для объяснения

This is the core DEMO value for investors.
"""

from typing import Dict, List, Optional

from src.core.agents.base import AgentBase
from src.core.agents.registry import REGISTRY
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class MasterAgent(AgentBase):
    # -------------------------
    # Supported strategies
    # -------------------------
    STRATEGY_PRICE = "PRICE"
    STRATEGY_QUALITY = "QUALITY"
    STRATEGY_SPEED = "SPEED"

    def __init__(self, *, agent_id: str, strategy: str = STRATEGY_PRICE):
        """
        Master agent constructor.

        agent_id is mandatory to keep Registry / Audit consistent.
        """
        super().__init__(agent_id=agent_id, role="master")

        self.strategy = strategy

        # DEMO license: allowed materials
        self.allowed_materials = {"brick"}

        # Last decision snapshot (for TrainerAgent)
        self.last_decision: Optional[Dict] = None

    # ------------------------------------------------------------------
    # LICENSE CHECK
    # ------------------------------------------------------------------
    def evaluate_material_access(self, material: str) -> bool:
        """
        Check if material is covered by current license.
        """

        allowed = material in self.allowed_materials

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="material_license_check",
            decision="ALLOW" if allowed else "DENY",
            policy="LICENSE",
            reason=(
                f"Material '{material}' "
                f"{'allowed' if allowed else 'not allowed'} by license"
            ),
        )

        return allowed

    # ------------------------------------------------------------------
    # MAIN LOGIC: STORE SELECTION
    # ------------------------------------------------------------------
    def select_store_for_material(self, material: str) -> Optional[Dict]:
        """
        Select best store according to strategy.
        """

        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=(
                f"🧠 Начинаю подбор магазина\n"
                f"Материал: `{material}`\n"
                f"Стратегия: `{self.strategy}`"
            ),
        )

        offers: List[Dict] = []

        # Collect offers from all stores
        for store in REGISTRY.by_role("store"):
            price_list = store.get_price_list()

            for item in price_list["materials"]:
                if item["code"] != material:
                    continue

                offers.append({
                    "store_id": store.agent_id,
                    "store_name": price_list["store_name"],
                    "price_per_unit": item["price_per_unit"],
                    "quality_score": item["quality_score"],
                    "delivery_days": price_list["delivery_days"],
                })

        if not offers:
            SYSTEM_CHAT.emit(
                source=self.agent_id,
                agent_id=self.agent_id,
                agent_role=self.role,
                message="❌ Нет предложений от магазинов",
            )
            return None

        # -------------------------
        # Strategy application
        # -------------------------
        if self.strategy == self.STRATEGY_PRICE:
            selected = min(offers, key=lambda o: o["price_per_unit"])

        elif self.strategy == self.STRATEGY_QUALITY:
            selected = max(offers, key=lambda o: o["quality_score"])

        elif self.strategy == self.STRATEGY_SPEED:
            selected = min(offers, key=lambda o: o["delivery_days"])

        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        # Save decision snapshot
        self.last_decision = {
            "strategy": self.strategy,
            "material": material,
            "selected_store": selected["store_id"],
            "price": selected["price_per_unit"],
            "quality": selected["quality_score"],
            "delivery_days": selected["delivery_days"],
            "offers_considered": len(offers),
        }

        # Audit log
        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="store_selection",
            decision="ALLOW",
            policy=f"STRATEGY:{self.strategy}",
            reason=(
                f"Selected store {selected['store_id']} "
                f"for material '{material}'"
            ),
        )

        # System chat
        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=(
                f"✅ Выбран магазин `{selected['store_id']}`\n"
                f"Цена: `{selected['price_per_unit']}`\n"
                f"Качество: `{selected['quality_score']}`\n"
                f"Доставка (дн): `{selected['delivery_days']}`"
            ),
        )

        return selected

    # ------------------------------------------------------------------
    # Strategy management
    # ------------------------------------------------------------------
    def set_strategy(self, strategy: str) -> None:
        """
        Change master strategy.
        """

        self.strategy = strategy

        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=f"🔁 Стратегия изменена на `{strategy}`",
        )

        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="change_strategy",
            decision="ALLOW",
            policy="MASTER_CONTROL",
            reason=f"Strategy set to {strategy}",
        )
