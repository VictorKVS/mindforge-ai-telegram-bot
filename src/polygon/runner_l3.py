# src/polygon/runner_l3.py

import json
import uuid
from pathlib import Path

from src.polygon.lifecycle import AgentLifecycle
from src.polygon.evaluator import EvaluationResult
from src.polygon.scenario_loader import load_l3_scenarios


class PolygonRunnerL3:
    def __init__(self, agent):
        self.agent = agent
        self.lifecycle_state = agent.lifecycle_state

    def run_l3_certification(self):
        # --- Preconditions ---
        if self.lifecycle_state != AgentLifecycle.CERTIFIED_L2:
            raise RuntimeError("Agent not certified for L3 entry")

        self.lifecycle_state = AgentLifecycle.IN_TRIAL
        evaluation = EvaluationResult()

        scenarios = load_l3_scenarios()

        # --- Trial Phase ---
        for scenario in scenarios:
            print(f"[POLYGON][L3] Running scenario: {scenario.id}")

            result = scenario.execute(self.agent)
            print(f"[POLYGON][L3] Result: {result}")

            if result["status"] == "PASS":
                evaluation.register_pass()
                continue

            evaluation.register_fail(
                reason=result.get("reason", "unknown"),
                critical=result.get("critical", False)
            )
            break  # fail-fast

        # --- Finalization ---
        cert_id = str(uuid.uuid4())

        if evaluation.suspended:
            verdict = "FAIL"
            final_state = AgentLifecycle.SUSPENDED
        elif evaluation.failed:
            verdict = "FAIL"
            final_state = AgentLifecycle.FAIL
        else:
            verdict = "PASS"
            final_state = AgentLifecycle.CERTIFIED_L3

        self.lifecycle_state = final_state
        self._write_verdict(verdict, final_state, cert_id)

        return {
            "verdict": verdict,
            "lifecycle_state": final_state
        }

    def _write_verdict(self, verdict, state, cert_id):
        report = {
            "agent_id": self.agent.agent_id,
            "level": "L3",
            "verdict": verdict,
            "final_state": state,
            "certification_history_id": cert_id
        }

        path = Path("src/polygon/reports/verdict_l3.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
