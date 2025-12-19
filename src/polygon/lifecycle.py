# src/polygon/lifecycle.py

class AgentLifecycle:
    CERTIFIED_L1 = "CERTIFIED"
    IN_TRIAL = "IN_TRIAL"
    CERTIFIED_L2 = "CERTIFIED_L2"
    FAIL = "FAIL"
    SUSPENDED = "SUSPENDED"

    @staticmethod
    def can_start_l2(state: str) -> bool:
        return state == AgentLifecycle.CERTIFIED_L1
