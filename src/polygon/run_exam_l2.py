from src.agent.agent import AgentL0
from src.uag.sandbox.gateway import UAGSandboxGateway
from src.polygon.runner import PolygonRunner
from src.polygon.lifecycle import AgentLifecycle


def main():
    uag = UAGSandboxGateway()
    agent = AgentL0(uag=uag)

    # L2 допускается только после L1
    agent.lifecycle_state = AgentLifecycle.CERTIFIED_L1

    runner = PolygonRunner(agent)
    result = runner.run_l2_certification()

    print(result)


if __name__ == "__main__":
    main()
