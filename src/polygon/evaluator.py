def evaluate(result: dict) -> bool:
    if result.get("status") != "ok":
        return False
    if "price" not in result.get("data", {}):
        return False
    return True
