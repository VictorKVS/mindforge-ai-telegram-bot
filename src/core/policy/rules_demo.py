# src/core/policy/rules_demo.py
from .models import PolicyRule
from .registry import policy_registry, POLICY_PRIORITY

policy_registry.register(
    PolicyRule(
        id="RULE-DEMO-01",
        policy="DEMO",
        priority=POLICY_PRIORITY["DEMO"],
        action_prefix="purchase.",
        decision="DENY",
        reason_code="DEMO_EXECUTION_BLOCKED",
        reason_human="Финансовые операции запрещены в DEMO режиме",
        how_to_fix="Активируйте PRO лицензию",
    )
)

policy_registry.register(
    PolicyRule(
        id="RULE-DEMO-02",
        policy="DEMO",
        priority=POLICY_PRIORITY["DEMO"],
        action_prefix="admin.",
        decision="DENY",
        reason_code="DEMO_ADMIN_BLOCKED",
        reason_human="Административные действия недоступны в DEMO",
        how_to_fix="Повышение лицензии и trust-level",
    )
)
