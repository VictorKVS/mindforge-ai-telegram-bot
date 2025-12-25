"""
File: apps/control_app/data_sources/audit.py

Purpose:
Read-only adapter for audit events.
"""

from src.core.audit_log import get_events


def load_audit_events(limit: int = 50):
    return get_events(limit=limit)