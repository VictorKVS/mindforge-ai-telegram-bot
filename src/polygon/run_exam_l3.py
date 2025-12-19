from src.agent.agent import AgentL0
from src.agent.intent_dispatcher import IntentDispatcher

from src.uag.core.access_controller import UAGAccessController
from src.uag.sandbox.gateway import UAGSandboxGateway
from src.providers.fake_agent_provider import FakeAgentProvider

from src.polygon.runner_l3 import PolygonRunnerL3
from src.polygon.lifecycle import AgentLifecycle


def main():
    # -------------------------------------------------
    # Assemble L3 sandbox dependencies (UAG)
    # -------------------------------------------------

    agent_provider = FakeAgentProvider()
    agent_provider.register_agent("agent_b")

    agent_provider.expose_capability(
        "agent_b",
        {
            "name": "get_public_profile",
            "exposed_fields": ["name", "service_type"],
            "full_data": {
                "name": "Agent B (Provider)",
                "service_type": "pricing",
                "internal_id": "secret_123"
            }
        }
    )

    access_controller = UAGAccessController()

    uag = UAGSandboxGateway(
        access_controller=access_controller,
        agent_provider=agent_provider
    )

    # -------------------------------------------------
    # Agent A
    # -------------------------------------------------

    dispatcher = IntentDispatcher(uag_gateway=uag)

    agent_a = AgentL0(
        agent_id="agent_a",
        intent_dispatcher=dispatcher
    )
    agent_a.lifecycle_state = AgentLifecycle.CERTIFIED_L2

    # -------------------------------------------------
    # Polygon L3
    # -------------------------------------------------

    runner = PolygonRunnerL3(agent=agent_a)

    result = runner.run_l3_certification()
    print(result)


if __name__ == "__main__":
    main()
