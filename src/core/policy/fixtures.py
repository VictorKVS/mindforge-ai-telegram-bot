# tests/policy/fixtures.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class PolicyTestCase:
    name: str

    # INPUT
    action: str
    mode: str = "DEMO"
    trust_level: int = 0

    # EXPECTED
    expected_decision: str = "ALLOW"
    expected_rule_id: Optional[str] = None


