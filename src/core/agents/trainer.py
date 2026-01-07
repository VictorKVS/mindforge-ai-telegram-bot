"""
File: src/core/agents/trainer.py

Purpose:
TrainerAgent — обучающий и объясняющий агент.

Responsibilities:
- Объяснять последнее решение MasterAgent
- Показывать логику выбора (цена / качество / время)
- Делать DEMO понятным для инвесторов и клиентов
- Формировать доверие к UAG и агентам

TrainerAgent НЕ принимает решений.
Он объясняет, обучает и фиксирует понимание.
"""

from typing import Optional, Dict

from src.core.agents.base import AgentBase
from src.core.agents.registry import REGISTRY
from src.core.audit_log import record_event
from src.core.system_chat import SYSTEM_CHAT


class TrainerAgent(AgentBase):
    def __init__(self):
        super().__init__(agent_id="trainer-001", role="trainer")

    # ------------------------------------------------------------------
    # MAIN EXPLANATION METHOD
    # ------------------------------------------------------------------
    def explain_last_decision(self) -> None:
        """
        Explain last MasterAgent decision in human-readable form.
        """

        masters = REGISTRY.by_role("master")

        if not masters:
            SYSTEM_CHAT.emit(
                source=self.agent_id,
                agent_id=self.agent_id,
                agent_role=self.role,
                message="❌ Нет MasterAgent для объяснения решения",
            )
            return

        master = masters[0]
        decision: Optional[Dict] = getattr(master, "last_decision", None)

        if not decision:
            SYSTEM_CHAT.emit(
                source=self.agent_id,
                agent_id=self.agent_id,
                agent_role=self.role,
                message="ℹ️ Пока нет решений для объяснения",
            )
            return

        # -------------------------------------------------
        # Build explanation text
        # -------------------------------------------------
        explanation = (
            "🎓 *Пояснение решения мастера*\n\n"
            f"🔹 Материал: `{decision['material']}`\n"
            f"🔹 Стратегия: `{decision['strategy']}`\n\n"
            f"🏪 Выбран магазин: `{decision['selected_store']}`\n\n"
            "📊 Причины выбора:\n"
        )

        if decision["strategy"] == "PRICE":
            explanation += (
                f"• Самая низкая цена: `{decision['price']}`\n"
                f"• Рассмотрено предложений: `{decision['offers_considered']}`\n"
            )

        elif decision["strategy"] == "QUALITY":
            explanation += (
                f"• Наивысшее качество: `{decision['quality']}`\n"
                f"• Проверены характеристики и ГОСТ\n"
            )

        elif decision["strategy"] == "SPEED":
            explanation += (
                f"• Самая быстрая доставка: `{decision['delivery_days']} дн.`\n"
                f"• Минимизация простоев работ\n"
            )

        explanation += (
            "\n🧠 *Вывод:*\n"
            "Решение принято автоматически на основе выбранной стратегии,\n"
            "данных от магазинов и правил UAG.\n\n"
            "_Мастер может изменить стратегию в любой момент._"
        )

        # -------------------------------------------------
        # Emit explanation
        # -------------------------------------------------
        SYSTEM_CHAT.emit(
            source=self.agent_id,
            agent_id=self.agent_id,
            agent_role=self.role,
            message=explanation,
        )

        # -------------------------------------------------
        # Audit log
        # -------------------------------------------------
        record_event(
            agent_id=self.agent_id,
            agent_role=self.role,
            action="explain_decision",
            decision="ALLOW",
            policy="TRANSPARENCY",
            reason=f"Explained decision using strategy {decision['strategy']}",
        )
