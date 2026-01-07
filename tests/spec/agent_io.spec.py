"""
Executable spec for Agent IO policy.

Covers:
- input sources
- output targets
- filesystem access
- memory invariants
- payload limits

ADR refs:
- ADR-004: Deterministic Agent Runtime Contract
- ADR-006: Policy Engine & Guardrails as Code
"""

import yaml
from pathlib import Path
import pytest


POLICY_PATH = Path("policies/agents/agent_io.yaml")


# =================================================
# Helpers
# =================================================

def load_policy():
    assert POLICY_PATH.exists(), "agent_io.yaml policy missing"
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
        "input",
        "output",
        "filesystem",
        "memory",
        "context",
        "audit",
        "agent_constraints",
    ]:
        assert field in policy, f"Missing top-level field: {field}"


# =================================================
# Input rules
# =================================================

def test_input_sources_are_explicit():
    policy = load_policy()
    input_cfg = policy["input"]

    assert "allowed_sources" in input_cfg
    assert "forbidden_sources" in input_cfg

    assert "network" in input_cfg["forbidden_sources"]
    assert "external_api" in input_cfg["forbidden_sources"]


def test_input_payload_limit_is_set():
    policy = load_policy()
    assert policy["input"]["max_payload_size_kb"] > 0
    assert policy["input"]["max_payload_size_kb"] <= 512


# =================================================
# Output rules
# =================================================

def test_output_targets_are_restricted():
    policy = load_policy()
    output_cfg = policy["output"]

    assert "allowed_targets" in output_cfg
    assert "forbidden_targets" in output_cfg

    assert "network" in output_cfg["forbidden_targets"]
    assert "external_api" in output_cfg["forbidden_targets"]


def test_output_payload_limit_is_set():
    policy = load_policy()
    assert policy["output"]["max_payload_size_kb"] > 0
    assert policy["output"]["max_payload_size_kb"] <= 512


# =================================================
# Filesystem rules
# =================================================

def test_filesystem_read_restrictions():
    policy = load_policy()
    fs = policy["filesystem"]["read"]

    assert "allowed_paths" in fs
    assert "forbidden_paths" in fs

    assert "/etc" in fs["forbidden_paths"]
    assert "~/.ssh" in fs["forbidden_paths"]


def test_filesystem_write_restrictions():
    policy = load_policy()
    fs = policy["filesystem"]["write"]

    assert "allowed_paths" in fs
    assert "forbidden_paths" in fs

    assert "policies/" in fs["forbidden_paths"]
    assert "tests/spec/" in fs["forbidden_paths"]


# =================================================
# Memory invariants (CRITICAL)
# =================================================

def test_agent_memory_is_disabled():
    policy = load_policy()
    memory = policy["memory"]

    assert memory["enabled"] is False, "Agent memory MUST be disabled in v0"


# =================================================
# Context handling
# =================================================

def test_context_limits_exist():
    policy = load_policy()
    ctx = policy["context"]

    assert ctx["max_items"] > 0
    assert ctx["expiration"]["enabled"] is True
    assert ctx["expiration"]["ttl_seconds"] > 0


# =================================================
# Agent constraints
# =================================================

def test_agent_constraints_are_strict():
    policy = load_policy()
    c = policy["agent_constraints"]

    assert c["allow_self_prompting"] is False
    assert c["allow_context_expansion"] is False
    assert c["allow_hidden_state"] is False


# =================================================
# Audit requirements
# =================================================

def test_audit_logging_is_enabled():
    policy = load_policy()
    audit = policy["audit"]

    assert audit["log_inputs"] is True
    assert audit["log_outputs"] is True
    assert "log_destination" in audit
