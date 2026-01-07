# src/core/agents/store_catalog/store_1.py

"""
ПрофиСтрой — магазин с упором на КАЧЕСТВО

Особенности:
- кирпичи повышенной прочности
- стабильные ГОСТ
- быстрая доставка
- дороже среднего
"""

STORE_1_MATERIALS = [
    {
        "sku": "brick-pro-m150",
        "name": "Кирпич полнотелый М150",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 3.8,
        "color": "красный",
        "manufacturer": "ПрофиКирпич",
        "composition": "глина",
        "strength_class": "М150",
        "frost_resistance": "F75",
        "price_per_unit": 42,
        "available_qty": 3000,
    },
    {
        "sku": "brick-pro-m200",
        "name": "Кирпич полнотелый М200",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 4.0,
        "color": "темно-красный",
        "manufacturer": "ПрофиКирпич",
        "composition": "глина",
        "strength_class": "М200",
        "frost_resistance": "F100",
        "price_per_unit": 48,
        "available_qty": 1800,
    },
    {
        "sku": "cement-pro-500",
        "name": "Цемент ПЦ 500-Д0",
        "gost": "ГОСТ 31108-2020",
        "weight_kg": 50,
        "manufacturer": "ЕвроЦемент",
        "composition": "портландцемент",
        "price_per_unit": 520,
        "available_qty": 600,
    },
]
