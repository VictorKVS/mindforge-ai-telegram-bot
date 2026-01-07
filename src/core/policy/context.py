# src/core/policy/context.py
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class PolicyContext:
    session_id: str
    user_id: int
    username: str
    action: str
    state: Optional[str]
    mode: str                  # DEMO | PROD
    trust_level: int
    payload: Dict[str, Any]