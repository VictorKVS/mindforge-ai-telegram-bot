# src/uag/helpers/intent_resolver.py

from src.uag.intents import INTENTS


def resolve_intent(message_text: str, command: str | None = None) -> str:
    """
    Определяет intent на уровне UAG.
    """

    if command == "who":
        return INTENTS["who"]

    if command == "ask":
        return INTENTS["ask"]

    if command == "plan":
        return INTENTS["plan"]

    if command == "taskadd":
        return INTENTS["task_add"]

    if command == "tasklist":
        return INTENTS["task_list"]

    if command == "taskstatus":
        return INTENTS["task_status"]

    if command in ("taskrun", "taskrunall"):
        return INTENTS["task_run"]

    # доменный хак (как у тебя сейчас)
    text = message_text.lower()
    if any(w in text for w in ["фундамент", "ленточный фундамент", "хочу фундамент"]):
        return INTENTS["build_foundation"]

    return INTENTS["chat"]
