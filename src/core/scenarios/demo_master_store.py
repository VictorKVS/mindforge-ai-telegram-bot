## src/core/scenarios/demo_master_store.py
"""
File: src/core/scenarios/demo_master_store.py

Purpose:
Investor DEMO scenario:
Builder agent calculating brick foundation
with licensing, store comparison and explanation.
"""

from src.core.agents.registry import REGISTRY
from src.core.system_chat import SYSTEM_CHAT


def run_demo_master_store(
    *,
    requested_material: str = "brick",
) -> None:
    # -------------------------------------------------
    # DEMO start
    # -------------------------------------------------
    SYSTEM_CHAT.emit(
        source="SYSTEM",
        agent_id="system",
        agent_role="system",
        message="▶ DEMO scenario started",
    )

    masters = REGISTRY.by_role("master")
    trainers = REGISTRY.by_role("trainer")
    stores = REGISTRY.by_role("store")

    if not masters or not trainers or not stores:
        SYSTEM_CHAT.emit(
            source="SYSTEM",
            agent_id="system",
            agent_role="system",
            message="❌ DEMO failed: agents not ready",
        )
        return

    master = masters[0]
    trainer = trainers[0]

    master.start()
    trainer.start()

    for store in stores:
        store.start()

    # -------------------------------------------------
    # Request received
    # -------------------------------------------------
    SYSTEM_CHAT.emit(
        source=master.agent_id,
        agent_id=master.agent_id,
        agent_role=master.role,
        message=(
            f"📥 Получена заявка:\n"
            f"Фундамент 6×6 м\n"
            f"Материал: {requested_material}"
        ),
    )

    # -------------------------------------------------
    # License check (KEY INVESTOR MOMENT)
    # -------------------------------------------------
    allowed = master.evaluate_material_access(requested_material)

    if not allowed:
        SYSTEM_CHAT.emit(
            source=master.agent_id,
            agent_id=master.agent_id,
            agent_role=master.role,
            message=(
                f"❌ Материал '{requested_material}' не входит в текущую лицензию.\n"
                "Требуется доплата. Обратитесь к продавцу."
            ),
        )
        return

    SYSTEM_CHAT.emit(
        source=master.agent_id,
        agent_id=master.agent_id,
        agent_role=master.role,
        message=f"🛡 Лицензия подтверждена: {requested_material}",
    )

    # -------------------------------------------------
    # Store price requests
    # -------------------------------------------------
    for store in stores:
        SYSTEM_CHAT.emit(
            source=store.agent_id,
            agent_id=store.agent_id,
            agent_role=store.role,
            message="🏬 Предоставляю прайс на кирпич для фундамента",
        )

    # -------------------------------------------------
    # Store selection by strategy
    # -------------------------------------------------
    selected_store = master.choose_store()

    SYSTEM_CHAT.emit(
        source=master.agent_id,
        agent_id=master.agent_id,
        agent_role=master.role,
        message=(
            "📊 Магазин выбран\n"
            f"{master.explain_last_decision()}"
        ),
    )

    # -------------------------------------------------
    # Trainer explanation
    # -------------------------------------------------
    trainer.explain_last_decision()

    # -------------------------------------------------
    # DEMO end
    # -------------------------------------------------
    SYSTEM_CHAT.emit(
        source="SYSTEM",
        agent_id="system",
        agent_role="system",
        message="✅ DEMO scenario completed",
    )
