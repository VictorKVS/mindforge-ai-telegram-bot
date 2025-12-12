import json
from src.agent.agent import AgentL0
from .lifecycle import AgentLifecycle
from .evaluator import evaluate


class PolygonRunner:
    def __init__(self):
        self.agent = AgentL0()
        self.lifecycle = AgentLifecycle()

    def run_pass_get_price(self) -> dict:
        self.lifecycle.start_trial()

        result = self.agent.handle_text("Сколько стоит цемент М500?")
        passed = evaluate(result)

        verdict = {
            "scenario": "pass_get_price",
            "verdict": "PASS" if passed else "FAIL"
        }

        if passed:
            self.lifecycle.certify()
        else:
            self.lifecycle.block()

        verdict["lifecycle_state"] = self.lifecycle.state
        return verdict
