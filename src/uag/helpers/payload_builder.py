# src/uag/helpers/payload_builder.py

from typing import Optional, Dict, Any
from datetime import datetime


def build_uag_payload(
    *,
    agent_id: str,
    intent: str,
    env: str = "telegram",
    text: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    mode: Optional[str] = None,
) -> dict:
    """
    Универсальный payload для UAG AccessController.

    Используется для:
    - Telegram
    - API
    - Agent-to-Agent
    - сценариев Teacher Agent
    """

    payload = {
        "agent_id": agent_id,
        "intent": intent,
        "context": {
            "env": env,
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    if text:
        payload["context"]["text"] = text

    if mode:
        payload["context"]["mode"] = mode

    if params:
        payload["context"]["params"] = params

    return payload
