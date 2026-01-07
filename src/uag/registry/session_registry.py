# src/uag/registry/session_registry.py

class SessionState:
    def __init__(self):
        self.mode = None        # builder | shop
        self.agent_id = None

_sessions = {}  # telegram_user_id -> SessionState


def get_session(user_id: int) -> SessionState:
    if user_id not in _sessions:
        _sessions[user_id] = SessionState()
    return _sessions[user_id]
