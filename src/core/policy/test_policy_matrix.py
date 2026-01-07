# tests/policy/test_policy_matrix.py

import pytest

from src.core.policy import policy_engine
from tests.policy.fixtures import PolicyTestCase


TEST_MATRIX = [
    PolicyTestCase(
        name="DEMO blocks purchase",
        action="purchase.execute",
        mode="DEMO",
        trust_level=0,
        expected_decision="DENY",
        expected_rule="RULE-DEMO-01",
    ),
    PolicyTestCase(
        name="DEMO blocks admin",
        action="admin.delete_user",
        mode="DEMO",
        trust_level=3,
        expected_decision="DENY",
        expected_rule="RULE-DEMO-02",
    ),
    PolicyTestCase(
        name="PROD allows purchase",
        action="purchase.execute",
        mode="PROD",
        trust_level=3,
        expected_decision="ALLOW",
        expected_rule="DEFAULT",
    ),
    PolicyTestCase(
        name="Unknown action allowed",
        action="help.show",
        mode="DEMO",
        trust_level=0,
        expected_decision="ALLOW",
        expected_rule="DEFAULT",
    ),
]


@pytest.mark.parametrize("case", TEST_MATRIX, ids=lambda c: c.name)
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
    assert decision.rule_id == case.expected_rule
