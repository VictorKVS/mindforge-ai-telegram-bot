from .scenario_loader import load_scenario
from .evaluator import evaluate


class CurriculumEvaluator:
    def __init__(self, agent):
        self.agent = agent

    def run_scenario(self, scenario_id: str) -> bool:
        scenario = load_scenario(scenario_id)
        text = scenario["input"]["text"]
        result = self.agent.handle_text(text)
        return evaluate(result)
