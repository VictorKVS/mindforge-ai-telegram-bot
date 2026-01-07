import yaml
from typing import Dict, Any, Optional

from src.core.audit.db import audit_db

class PolicyDecision:
    def __init__(self, decision: str, rule_id: str, policy: str, message: str):
        self.decision = decision
        self.rule_id = rule_id
        self.policy = policy
        self.message = message


class PolicyEngine:
    def __init__(self, rules_path: str):
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)["rules"]

    def evaluate(
        self,
        *,
        session_id: str,
        user_id: int,
        username: str,
        action: str,
        state: Optional[str],
        mode: str,
        trust_level: int,
        payload: Optional[Dict[str, Any]] = None,
    ) -> PolicyDecision:

        for rule in self.rules:
            when = rule.get("when", {})

            if "mode" in when and when["mode"] != mode:
                continue

            if "action" in when and when["action"] != action:
                continue

            if "action_prefix" in when and not action.startswith(when["action_prefix"]):
                continue

            if "min_trust" in when and trust_level < when["min_trust"]:
                continue

            # 🔐 RULE MATCHED
            decision = PolicyDecision(
                decision=rule["decision"],
                rule_id=rule["id"],
                policy=rule["policy"],
                message=rule.get("message", ""),
            )

            # 🧾 AUDIT
            audit_db.log_event(
                session_id=session_id,
                user_id=user_id,
                username=username,
                event_type="POLICY",
                action=action,
                state=state,
                decision=decision.decision,
                policy=decision.policy,
                source=decision.rule_id,
                payload=payload or {},
            )

            return decision

        # DEFAULT: ALLOW
        return PolicyDecision(
            decision="ALLOW",
            rule_id="DEFAULT",
            policy="NONE",
            message="No policy restrictions",
        )
