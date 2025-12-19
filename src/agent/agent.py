# src/agent/agent.py

class AgentL0:
    def __init__(self, agent_id: str, intent_dispatcher):
        self.agent_id = agent_id
        self.intent_dispatcher = intent_dispatcher

    def handle_text(self, text: str) -> dict:
        # Простая заглушка: распознаём запрос на цену
        if "цемент" in text:
            return self.intent_dispatcher.dispatch("get_price", {"material": "cement_M500"})
        return {"error": "Не распознано"}