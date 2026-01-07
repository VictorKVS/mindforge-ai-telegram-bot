"""
File: src/core/policy_loader.py

Purpose:
Load and validate Policy-as-Code configuration.
"""

from pathlib import Path
import yaml


_POLICY_CACHE = None


def load_policy_config() -> dict:
    global _POLICY_CACHE

    if _POLICY_CACHE is not None:
        return _POLICY_CACHE

    config_path = Path("configs/risk_policy.yaml")

    if not config_path.exists():
        raise FileNotFoundError(
            "Policy config not found: configs/risk_policy.yaml"
        )

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    _POLICY_CACHE = data
    return data


def resolve_risk_level(score: int, thresholds: dict) -> str:
    if score < thresholds["low"]:
        return "LOW"
    if score < thresholds["medium"]:
        return "MEDIUM"
    return "HIGH"
