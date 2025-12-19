# src/uag/helpers/executor.py

from src.uag.core.access_controller import UAGAccessController
from src.uag.helpers.payload_builder import build_uag_payload

uag = UAGAccessController()


def execute_uag(
    *,
    agent_id: str,
    intent: str,
    text: str | None = None,
    params: dict | None = None,
    role: str = "agent_l0",
    env: str = "telegram",
    mode: str | None = None,
) -> dict:
    payload = build_uag_payload(
        agent_id=agent_id,
        intent=intent,
        env=env,
        text=text,
        params=params,
        mode=mode,
    )

    return uag.handle(payload, role=role)
