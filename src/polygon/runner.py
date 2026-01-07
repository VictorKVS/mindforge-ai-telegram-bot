import json
import uuid
from pathlib import Path

from src.polygon.lifecycle import AgentLifecycle
from src.polygon.evaluator import EvaluationResult
from src.polygon.scenario_loader import load_l2_scenarios


class PolygonRunner:
    def __init__(self, agent):
        self.agent = agent
        self.lifecycle_state = agent.lifecycle_state

    def run_l2_certification(self):
        # --- Pre-flight ---
        if not AgentLifecycle.can_start_l2(self.lifecycle_state):
            raise RuntimeError("Agent not certified for L2 entry")

        self.lifecycle_state = AgentLifecycle.IN_TRIAL
        evaluation = EvaluationResult()

        scenarios = load_l2_scenarios()

        # --- Trial Phase ---
        for scenario in scenarios:
            print(f"[POLYGON] Running scenario: {scenario.id}")
            result = scenario.execute(self.agent)
            print(f"[POLYGON] Result: {result}")

            if result["status"] == "PASS":
                evaluation.register_pass()
                continue

            evaluation.register_fail(
                reason=result.get("reason", "unknown"),
                critical=result.get("critical", False),
            )
            break  # fail-fast

        # --- Finalization ---
        certification_id = str(uuid.uuid4())

        if evaluation.suspended:
            final_state = AgentLifecycle.SUSPENDED
            verdict = "FAIL"
        elif evaluation.failed:
            final_state = AgentLifecycle.FAIL
            verdict = "FAIL"
        else:
            final_state = AgentLifecycle.CERTIFIED_L2
            verdict = "PASS"

        self.lifecycle_state = final_state
        self._write_verdict(verdict, final_state, certification_id)

        return {
            "verdict": verdict,
            "lifecycle_state": final_state,
        }

    def _write_verdict(self, verdict, state, cert_id):
        report = {
            "agent_id": self.agent.agent_id,
            "level": "L2",
            "verdict": verdict,
            "final_state": state,
            "certification_history_id": cert_id,
        }

        report_path = Path("src/polygon/reports/verdict.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
