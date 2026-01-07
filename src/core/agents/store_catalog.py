# src/core/agents/store_catalog.py
"""
Store catalogs for DEMO.

Contains static material lists for StoreAgents.
Easy to replace by DB / API later.
"""

# -------------------------
# Store #1 — базовый
# -------------------------
STORE_1_MATERIALS = [
    {
        "material": "brick",
        "name": "Кирпич керамический М150",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250×120×65",
        "weight_kg": 3.5,
        "color": "красный",
        "manufacturer": "ЛСР",
        "price_per_unit": 28,
    },
    {
        "material": "cement",
        "name": "Цемент ПЦ 500",
        "gost": "ГОСТ 31108-2020",
        "weight_kg": 50,
        "price_per_unit": 520,
    },
]

# -------------------------
# Store #2 — особенный (для DEMO)
# -------------------------
STORE_2_MATERIALS = [
    {
        "material": "brick",
        "name": "Кирпич клинкерный М300",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250×120×65",
        "weight_kg": 4.2,
        "color": "тёмно-коричневый",
        "manufacturer": "CRH",
        "price_per_unit": 65,
        "note": "Повышенная прочность, морозостойкость F100",
    },
    {
        "material": "cement",
        "name": "Цемент ПЦ 400",
        "gost": "ГОСТ 31108-2020",
        "weight_kg": 50,
        "price_per_unit": 470,
    },
]

# -------------------------
# Store #3 — дешёвый, долгая доставка
# -------------------------
STORE_3_MATERIALS = [
    {
        "material": "brick",
        "name": "Кирпич силикатный М125",
        "gost": "ГОСТ 379-2015",
        "size_mm": "250×120×65",
        "weight_kg": 3.8,
        "color": "белый",
        "manufacturer": "Группа Эталон",
        "price_per_unit": 24,
    },
]
