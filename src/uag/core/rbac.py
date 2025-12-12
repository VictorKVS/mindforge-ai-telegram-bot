ROLE_INTENTS = {
    "agent_l0": {"get_price", "get_info"}
}


def is_intent_allowed(role: str, intent: str) -> bool:
    return intent in ROLE_INTENTS.get(role, set())
