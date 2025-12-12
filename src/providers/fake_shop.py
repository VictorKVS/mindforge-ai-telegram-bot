def get_price(query: dict) -> dict:
    product = query.get("product", "").lower()
    if "цемент" in product:
        return {
            "product": "Цемент М500",
            "price": 520,
            "currency": "RUB"
        }
    return {
        "product": product,
        "price": None,
        "currency": "RUB"
    }
