from dataclasses import dataclass
from typing import Optional, Dict, Any


# =====================================================
# POLICY RULE
# =====================================================

@dataclass
class PolicyRule:
    id: str
    policy: str                # DEMO | TRUST | PAYMENT | UAG | *
    priority: int              # чем выше — тем раньше
    action_prefix: str         # purchase. / demo. / *
    decision: str              # ALLOW | DENY | INFO

    reason_code: str
    reason_human: str
    how_to_fix: Optional[str] = None
    description: Optional[str] = None

    def matches(
        self,
        *,
        action: str,
        mode: str,
        trust_level: int,
    ) -> bool:
        # 1️⃣ policy scope
        if self.policy != "*" and self.policy != mode:
            return False

        # 2️⃣ wildcard
        if self.action_prefix == "*":
            return True

        # 3️⃣ prefix match (СТРОГО)
        return action.startswith(self.action_prefix)


# =====================================================
# POLICY DECISION
# =====================================================

@dataclass
class PolicyDecision:
    decision: str              # ALLOW | DENY | INFO
    rule_id: str
    policy: str
    message: str
    payload: Dict[str, Any]

    @classmethod
    def from_rule(cls, rule: PolicyRule) -> "PolicyDecision":
        return cls(
            decision=rule.decision,
            rule_id=rule.id,
            policy=rule.policy,
            message=rule.reason_human,
            payload={
                "reason_code": rule.reason_code,
                "how_to_fix": rule.how_to_fix,
            },
        )

    @classmethod
    def allow_default(cls) -> "PolicyDecision":
        return cls(
            decision="ALLOW",
            rule_id="DEFAULT",
            policy="DEFAULT",
            message="Разрешено по умолчанию",
            payload={},
        )
