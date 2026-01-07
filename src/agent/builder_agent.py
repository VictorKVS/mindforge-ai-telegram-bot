# src/agents/builder_agent.py

class BuilderAgent:
    agent_id = "builder_v1"
    role = "foundation_builder"

    def describe(self) -> str:
        return (
            "👷 Я агент-строитель фундаментов.\n\n"
            "Я умею:\n"
            "• рассчитывать фундамент\n"
            "• определять материалы\n"
            "• запрашивать цены\n"
            "• формировать заказ\n"
        )

    def request_materials(self) -> dict:
        return {
            "brick": "brick_m100",
            "cement": "cement_25kg",
            "volume": "1000 bricks"
        }
