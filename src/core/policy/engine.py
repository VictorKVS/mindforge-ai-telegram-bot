# src/core/policy/engine.py

import yaml
from pathlib import Path
from typing import List, Dict, Any

from src.core.policy.models import PolicyRule, PolicyDecision


class PolicyEngine:
    """
    L1 Policy Engine
    - deterministic
    - ordered by priority
    - explainable
    """

    def __init__(self, rules_path: str):
        self.rules_path = Path(rules_path)
        self.rules: List[PolicyRule] = []
        self.when_conditions: Dict[str, Dict[str, Any]] = {}
        self._load_rules()

    # -----------------------------------------------------
    # LOAD RULES
    # -----------------------------------------------------
    def _load_rules(self):
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Policy rules not found: {self.rules_path}")

        data = yaml.safe_load(self.rules_path.read_text(encoding="utf-8"))

        for raw in data.get("rules", []):
            # when — условие применения
            when = raw.pop("when", {})

            # DSL → Domain mapping
            if "message" in raw and "reason_human" not in raw:
                raw["reason_human"] = raw.pop("message")

            raw.setdefault("priority", 100)
            raw.setdefault("action_prefix", "*")
            raw.setdefault("reason_code", raw.get("id", "UNKNOWN_RULE"))

            rule = PolicyRule(**raw)

            self.rules.append(rule)
            self.when_conditions[rule.id] = when

        # приоритет: выше → раньше
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    # -----------------------------------------------------
    # WHEN MATCHING
    # -----------------------------------------------------
    def _when_matches(
        self,
        when: Dict[str, Any],
        *,
        mode: str,
        trust_level: int,
    ) -> bool:
        if not when:
            return True

        if "mode" in when and when["mode"] != mode:
            return False

        if "trust_level" in when:
            expr = str(when["trust_level"]).strip()

            if expr.startswith("<="):
                return trust_level <= int(expr[2:])
            if expr.startswith(">="):
                return trust_level >= int(expr[2:])
            if expr.startswith("<"):
                return trust_level < int(expr[1:])
            if expr.startswith(">"):
                return trust_level > int(expr[1:])
            if expr.isdigit():
                return trust_level == int(expr)

        return True

    # -----------------------------------------------------
    # EVALUATE
    # -----------------------------------------------------
    def evaluate(
        self,
        *,
        session_id: str,
        user_id: int,
        username: str,
        action: str,
        state: str | None,
        mode: str,
        trust_level: int,
        payload: dict,
    ) -> PolicyDecision:

        for rule in self.rules:
            when = self.when_conditions.get(rule.id, {})

            # 1️⃣ проверяем when
            if not self._when_matches(
                when,
                mode=mode,
                trust_level=trust_level,
            ):
                continue

            # 2️⃣ проверяем правило
            if rule.matches(
                action=action,
                mode=mode,
                trust_level=trust_level,
            ):
                return PolicyDecision(
                    decision=rule.decision,
                    rule_id=rule.id,
                    policy=rule.policy,
                    message=rule.reason_human,
                    payload={
                        "reason_code": rule.reason_code,
                        "how_to_fix": rule.how_to_fix,
                        "description": rule.description,
                    },
                )

        # default ALLOW
        return PolicyDecision(
            decision="ALLOW",
            rule_id="DEFAULT",
            policy="DEFAULT",
            message="Разрешено по умолчанию",
            payload={},
        )
