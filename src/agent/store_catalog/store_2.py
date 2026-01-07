# src/core/agents/store_catalog/store_2.py

"""
БалансСтрой — магазин «золотая середина»

Особенности:
- оптимальное соотношение цена / качество
- средняя скорость доставки
- самые популярные позиции рынка
"""

STORE_2_MATERIALS = [
    {
        "sku": "brick-balance-m125",
        "name": "Кирпич рядовой М125",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 3.7,
        "color": "красный",
        "manufacturer": "БалансКирпич",
        "composition": "глина",
        "strength_class": "М125",
        "frost_resistance": "F50",
        "price_per_unit": 35,
        "available_qty": 4000,
    },
    {
        "sku": "brick-balance-m150",
        "name": "Кирпич рядовой М150",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 3.9,
        "color": "красно-коричневый",
        "manufacturer": "БалансКирпич",
        "composition": "глина",
        "strength_class": "М150",
        "frost_resistance": "F75",
        "price_per_unit": 39,
        "available_qty": 2600,
    },
    {
        "sku": "tools-basic-set",
        "name": "Набор каменщика (мастерок, уровень, отвес)",
        "manufacturer": "ToolMaster",
        "composition": "металл / пластик",
        "price_per_unit": 1850,
        "available_qty": 150,
    },
]
