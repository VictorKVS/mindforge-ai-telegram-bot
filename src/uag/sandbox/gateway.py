# src/uag/sandbox/gateway.py

from src.uag.core.access_controller import UAGAccessController
from src.providers.fake_agent_provider import FakeAgentProvider


class UAGSandboxGateway:
    """
    Sandbox Gateway — enforcement + routing
    """

    def __init__(
        self,
        access_controller: UAGAccessController,
        agent_provider: FakeAgentProvider
    ):
        self.access_controller = access_controller
        self.agent_provider = agent_provider

    def handle_agent_query(
        self,
        caller_agent_id: str,
        target_agent_id: str,
        capability_name: str
    ) -> dict:
        # --- Access decision ---
        decision = self.access_controller.authorize_agent_query(
            caller_agent_id=caller_agent_id,
            target_agent_id=target_agent_id,
            capability_name=capability_name
        )

        if decision["status"] == "DENY":
            return {
                "status": "DENY",
                "reason": decision.get("reason", "access_denied")
            }

        # --- Execute capability ---
        raw_data = self.agent_provider.execute_capability(
            agent_id=target_agent_id,
            capability_name=capability_name
        )

        # --- Filter response ---
        capability_contract = (
            self.access_controller
            .capability_registry
            .resolve_capability(target_agent_id, capability_name)
        )

        exposed_fields = capability_contract["exposed_fields"]

        filtered_data = {
            field: raw_data[field]
            for field in exposed_fields
            if field in raw_data
        }

        return {
            "status": "OK",
            "data": filtered_data
        }
