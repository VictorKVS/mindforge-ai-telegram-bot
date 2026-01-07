from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class SessionOut(BaseModel):
    session_id: str
    user_id: int
    username: Optional[str]
    started_at: str
    last_state: Optional[str]
    trust_level: Optional[int]
    mode: str


class AuditEventOut(BaseModel):
    ts: str
    event_type: str
    action: str
    state: Optional[str]
    decision: Optional[str]
    policy: Optional[str]
    source: Optional[str]
    payload: Dict[str, Any]
