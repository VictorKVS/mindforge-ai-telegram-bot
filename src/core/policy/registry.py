# src/core/policy/registry.py
from typing import List
from .models import PolicyRule

POLICY_PRIORITY = {
    "PAYMENT": 100,
    "TRUST": 80,
    "DEMO": 60,
    "UAG": 40,
}


class PolicyRegistry:
    def __init__(self):
        self.rules: List[PolicyRule] = []

    def register(self, rule: PolicyRule):
        self.rules.append(rule)

    def all_rules(self) -> List[PolicyRule]:
        return sorted(self.rules, key=lambda r: r.priority, reverse=True)


policy_registry = PolicyRegistry()
