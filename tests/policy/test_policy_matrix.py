# tests/policy/test_policy_matrix.py

import pytest

from src.core.policy import policy_engine
from .fixtures import PolicyTestCase


TEST_CASES = [
    PolicyTestCase(
        name="DEMO blocks purchase execution",
        action="purchase.execute",
        mode="DEMO",
        trust_level=0,
        expected_decision="DENY",
        expected_rule_id="RULE-DEMO-01",
    ),
    PolicyTestCase(
        name="Default allow for harmless action",
        action="demo.view",
        mode="DEMO",
        trust_level=0,
        expected_decision="ALLOW",
        expected_rule_id="DEFAULT",
    ),
]


@pytest.mark.parametrize("case", TEST_CASES, ids=lambda c: c.name)
def test_policy_matrix(case: PolicyTestCase):
    decision = policy_engine.evaluate(
        session_id="test-session",
        user_id=1,
        username="tester",
        action=case.action,
        state=None,
        mode=case.mode,
        trust_level=case.trust_level,
        payload={},
    )

    assert decision.decision == case.expected_decision

    if case.expected_rule_id is not None:
        assert decision.rule_id == case.expected_rule_id
