from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PolicyContext:
    session_id: str
    user_id: int
    username: str
    action: str
    state: Optional[str]
    mode: str
    trust_level: int
    payload: Dict[str, Any]
