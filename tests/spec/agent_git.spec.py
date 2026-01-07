"""
Executable spec for Agent Git policy.

Covers:
- allowed git operations
- forbidden operations
- branch protections
- commit requirements
- push rules
- fail-safe behavior

ADR refs:
- ADR-004: Deterministic Agent Runtime Contract
- ADR-006: Policy Engine & Guardrails as Code
- ADR-007: End-to-End Production Pipeline
"""

import yaml
from pathlib import Path
import pytest


POLICY_PATH = Path("policies/agents/agent_git.yaml")


# =================================================
# Helpers
# =================================================

def load_policy():
    assert POLICY_PATH.exists(), "agent_git.yaml policy missing"
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# =================================================
# Core structure
# =================================================

def test_policy_has_required_top_level_fields():
    policy = load_policy()

    for field in [
        "version",
        "type",
        "git",
        "branches",
        "commits",
        "push",
        "fail_safe",
        "audit",
        "agent_constraints",
    ]:
        assert field in policy, f"Missing top-level field: {field}"


# =================================================
# Git operations
# =================================================

def test_allowed_git_operations_are_explicit():
    git = load_policy()["git"]

    assert "allowed_operations" in git
    assert "forbidden_operations" in git

    assert "status" in git["allowed_operations"]
    assert "diff" in git["allowed_operations"]
    assert "commit" in git["allowed_operations"]
    assert "push" in git["allowed_operations"]

    assert "rebase" in git["forbidden_operations"]
    assert "reset" in git["forbidden_operations"]
    assert "filter-branch" in git["forbidden_operations"]


# =================================================
# Branch rules
# =================================================

def test_branch_protection_rules_exist():
    branches = load_policy()["branches"]

    assert "protected" in branches
    assert "allowed_patterns" in branches

    assert "main" in branches["protected"]
    assert "master" in branches["protected"]


def test_direct_commits_to_protected_branches_forbidden():
    branches = load_policy()["branches"]

    assert branches["allow_direct_commit"] is False


# =================================================
# Commit rules
# =================================================

def test_commit_message_policy_exists():
    commits = load_policy()["commits"]

    assert commits["require_message"] is True
    assert commits["require_conventional_format"] is True
    assert commits["max_message_length"] > 0


def test_commit_content_restrictions():
    commits = load_policy()["commits"]

    assert commits["allow_binary_files"] is False
    assert commits["allow_large_files"] is False


# =================================================
# Push rules
# =================================================

def test_push_rules_are_restrictive():
    push = load_policy()["push"]

    assert push["require_clean_status"] is True
    assert push["allow_force_push"] is False
    assert push["require_upstream"] is True


# =================================================
# Fail-safe behavior
# =================================================

def test_fail_safe_is_enabled():
    fail_safe = load_policy()["fail_safe"]

    assert fail_safe["enabled"] is True
    assert fail_safe["on_violation"] == "abort"
    assert fail_safe["on_error"] == "pause"


# =================================================
# Agent constraints
# =================================================

def test_agent_constraints_are_strict():
    c = load_policy()["agent_constraints"]

    assert c["allow_self_decision"] is False
    assert c["allow_git_config_change"] is False
    assert c["allow_history_rewrite"] is False


# =================================================
# Audit requirements
# =================================================

def test_audit_logging_is_enabled():
    audit = load_policy()["audit"]

    assert audit["log_commands"] is True
    assert audit["log_commits"] is True
    assert audit["log_pushes"] is True
    assert "log_destination" in audit
