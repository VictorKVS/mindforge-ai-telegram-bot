"""
File: src/core/training/building_modules.py

Purpose:
Training modules for construction agents (DEMO).

Used in investor scenario:
- foundation from brick = included
- reinforced concrete = upgrade
"""

from src.core.training.module import TrainingModule


# --------------------------------------------------
# BASIC: Brick foundation (LIGHT STRUCTURES)
# --------------------------------------------------
BRICK_FOUNDATION_MODULE = TrainingModule(
    module_id="MF-BUILD-FND-BRICK",
    description=(
        "Foundation construction for light buildings "
        "(brick, sheds, garages, light houses)."
    ),
    allowed_tasks={
        "calculate_brick_foundation",
        "estimate_materials_brick",
        "query_brick_stores",
        "select_brick_supplier",
        "schedule_brick_delivery",
    },
    upgrade_tasks={
        "calculate_reinforced_concrete",
        "pile_foundation",
        "monolithic_slab",
    },
)


# --------------------------------------------------
# UPGRADE: Reinforced concrete (paid upgrade)
# --------------------------------------------------
REINFORCED_CONCRETE_MODULE = TrainingModule(
    module_id="MF-BUILD-FND-RC",
    description="Reinforced concrete foundations and heavy structures.",
    allowed_tasks={
        "calculate_reinforced_concrete",
        "estimate_rc_materials",
        "query_concrete_plants",
        "schedule_concrete_delivery",
    },
)
