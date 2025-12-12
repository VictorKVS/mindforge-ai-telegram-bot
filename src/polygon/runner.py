import yaml
from src.agent.agent import AgentL0
from .lifecycle import AgentLifecycle
from .curriculum_evaluator import CurriculumEvaluator


class PolygonRunner:
    def __init__(self):
        self.agent = AgentL0()
        self.lifecycle = AgentLifecycle()
        self.evaluator = CurriculumEvaluator(self.agent)

    def run_curriculum(self) -> dict:
        self.lifecycle.start_trial()

        with open("src/polygon/curriculum.yaml", "r", encoding="utf-8") as f:
            curriculum = yaml.safe_load(f)

        for scenario_id in curriculum["mandatory_scenarios"]:
            passed = self.evaluator.run_scenario(scenario_id)
            if not passed:
                self.lifecycle.block()
                return {
                    "verdict": "FAIL",
                    "failed_scenario": scenario_id,
                    "lifecycle_state": self.lifecycle.state
                }

        self.lifecycle.certify()
        return {
            "verdict": "PASS",
            "lifecycle_state": self.lifecycle.state
        }
