class FakeShop:
    def execute(self, intent: str, query: dict):
        if intent == "get_price":
            return {
                "product": query.get("product"),
                "price": 520
            }
        return None
