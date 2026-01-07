# src/core/policy/__init__.py
from src.core.policy.engine import PolicyEngine

policy_engine = PolicyEngine(
    rules_path="src/core/policy/rules.yaml"
)
