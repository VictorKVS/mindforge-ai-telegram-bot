# src/agent/security/security_layer.py

import json
import os
from typing import Dict, Any

class SecurityLayer:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """Загружает правила безопасности из JSON-файла."""
        rules_path = os.path.join(os.path.dirname(__file__), "security_rules.json")
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate(self, event: Dict[str, Any]) -> bool:
        """
        Проверка входящих данных и действий агента.
        С