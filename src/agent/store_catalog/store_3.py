# src/core/agents/store_catalog/# src/core/agents/store_catalog/store_3.py

"""
ЭкономСтрой — дешёвый магазин
Отличается:
- самый дешёвый кирпич
- медленная доставка
- ОДНА позиция, которой нет у других (учебный триггер)
"""

STORE_3_MATERIALS = [
    {
        "sku": "brick-econom-std",
        "name": "Кирпич рядовой М100",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 3.6,
        "color": "красный",
        "manufacturer": "ЭкономКирпич",
        "composition": "глина",
        "price_per_unit": 28,
        "available_qty": 5000,
    },
    {
        "sku": "brick-special-x1",
        "name": "Кирпич силикатный X1",
        "gost": "ГОСТ 379-2015",
        "size_mm": "250x120x88",
        "weight_kg": 4.3,
        "color": "белый",
        "manufacturer": "SilicaStone",
        "composition": "известь + песок",
        "price_per_unit": 31,
        "available_qty": 1200,
        "⚠️_special": True,  # ← НЕТ У ДРУГИХ МАГАЗИНОВ
    },
]


"""
ЭкономСтрой — дешёвый магазин
Отличается:
- самый дешёвый кирпич
- медленная доставка
- ОДНА позиция, которой нет у других (учебный триггер)
"""

STORE_3_MATERIALS = [
    {
        "sku": "brick-econom-std",
        "name": "Кирпич рядовой М100",
        "gost": "ГОСТ 530-2012",
        "size_mm": "250x120x65",
        "weight_kg": 3.6,
        "color": "красный",
        "manufacturer": "ЭкономКирпич",
        "composition": "глина",
        "price_per_unit": 28,
        "available_qty": 5000,
    },
    {
        "sku": "brick-special-x1",
        "name": "Кирпич силикатный X1",
        "gost": "ГОСТ 379-2015",
        "size_mm": "250x120x88",
        "weight_kg": 4.3,
        "color": "белый",
        "manufacturer": "SilicaStone",
        "composition": "известь + песок",
        "price_per_unit": 31,
        "available_qty": 1200,
        "⚠️_special": True,  # ← НЕТ У ДРУГИХ МАГАЗИНОВ
    },
]
