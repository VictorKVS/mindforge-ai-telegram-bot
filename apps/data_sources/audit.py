# apps/control_app/data_sources/audit.py

from src.core.audit_log import get_events


def load_audit_events(limit: int = 1000):
    """
    Load audit events from agent audit log.
    """
    return get_events(limit=limit)
