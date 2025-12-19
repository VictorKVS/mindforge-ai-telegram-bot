# --- L3 scenarios loader ---

from src.polygon.scenarios.pass_agent_to_agent_info import PassAgentToAgentInfo


def load_l3_scenarios():
    return [
        PassAgentToAgentInfo(),
    ]
