# src/polygon/evaluator.py

class EvaluationResult:
    def __init__(self):
        self.failed = False
        self.suspended = False
        self.violations = []

    def register_fail(self, reason, critical=False):
        self.failed = True
        self.violations.append(reason)
        if critical:
            self.suspended = True
