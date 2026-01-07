def recognize_intent(text: str) -> dict:
    """
    Минимальная L0-реализация.
    Позже будет заменена на LLM-based extraction.
    """
    text_lower = text.lower()

    if "цена" in text_lower or "стоит" in text_lower:
        return {
            "intent": "get_price",
            "params": {
                "product": text
            }
        }

    return {
        "intent": "get_info",
        "params": {
            "topic": text
        }
    }
