"""
File: apps/control_app/app.py

Purpose:
Control / Analytics application for MindForge.

Responsibilities:
- Aggregate audit & log data
- Calculate metrics (decisions, policies, risk)
- Print DEMO control report (CLI)
"""

from apps.control_app.metrics.decisions import decision_metrics
from apps.control_app.metrics.policies import policy_metrics
from apps.control_app.metrics.risk import risk_metrics

from apps.control_app.data_sources.audit import load_audit_events


def main() -> None:
    print("\n=== 🧠 MindForge Control Report (DEMO) ===\n")

    events = load_audit_events()

    print("[DECISIONS]")
    print(decision_metrics(events))
    print()

    print("[POLICIES]")
    print(policy_metrics(events))
    print()

    print("[RISK]")
    print(risk_metrics(events))
    print()

    print("=== END REPORT ===\n")


if __name__ == "__main__":
    main()
