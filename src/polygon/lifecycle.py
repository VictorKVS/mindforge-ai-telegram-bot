class AgentLifecycle:
    PENDING = "PENDING"
    IN_TRIAL = "IN_TRIAL"
    CERTIFIED = "CERTIFIED"
    BLOCKED = "BLOCKED"

    def __init__(self):
        self.state = self.PENDING

    def start_trial(self):
        if self.state != self.PENDING:
            raise RuntimeError("Invalid lifecycle transition")
        self.state = self.IN_TRIAL

    def certify(self):
        self.state = self.CERTIFIED

    def block(self):
        self.state = self.BLOCKED
