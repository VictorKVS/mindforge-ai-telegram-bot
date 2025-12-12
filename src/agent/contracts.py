import yaml
from pathlib import Path

INTENTS_PATH = Path("contracts/intents/agent_intents.yaml")


class IntentRegistry:
    def __init__(self, path: Path = INTENTS_PATH):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.intents = data.get("intents", {})

    def is_known_intent(self, intent: str) -> bool:
        return intent in self.intents

    def get_schema(self, intent: str):
        return self.intents[intent]["schema"]
