from .intent_recognizer import recognize_intent
from .intent_dispatcher import IntentDispatcher
from .contracts import IntentRegistry


class AgentL0:
    """
    Agent L0 — мыслящий, но бесправный агент.
    Формирует intent и ВСЕГДА действует через UAG.
    """

    def __init__(self):
        self.registry = IntentRegistry()
        self.dispatcher = IntentDispatcher()

    def handle_text(self, text: str) -> dict:
        intent_payload = recognize_intent(text)

        intent = intent_payload["intent"]
        if not self.registry.is_known_intent(intent):
            raise ValueError(f"Unknown intent: {intent}")

        return self.dispatcher.dispatch(intent_payload)
