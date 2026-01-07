from src.core.agents.store import StoreAgent

STORE_2_MATERIALS = [
    {
        "code": "BRICK_M150_RED",
        "name": "Кирпич М150 (эконом)",
        "gost": "ГОСТ 530-2012",
        "size": "250×120×65 мм",
        "weight": "3.6 кг",
        "color": "красный",
        "manufacturer": "РегионКирпич",
        "composition": "глина",
        "price_per_unit": 34,
    },
    {
        "code": "CEMENT_M500",
        "name": "Цемент М500",
        "gost": "ГОСТ 31108-2020",
        "weight": "50 кг",
        "manufacturer": "РегионЦемент",
        "price_per_unit": 400,
    },
]

store_2 = StoreAgent(
    agent_id="store-002",
    store_name="База СтройЭконом",
    materials=STORE_2_MATERIALS,
    delivery_days=5,
    delivery_price=3500,
)
