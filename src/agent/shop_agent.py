# src/agent/shop_agent.py

class ShopAgent:
    agent_id = "shop_v1"
    role = "materials_shop"

    def get_price(self, materials: dict) -> dict:
        return {
            "brick_m100": "0.45 €/шт",
            "cement_25kg": "6 €/мешок",
            "delivery": "120 €"
        }

    def confirm_delivery(self) -> str:
        return (
            "🚚 Доставка подтверждена.\n"
            "Дата: завтра\n"
            "Статус: в обработке"
        )
