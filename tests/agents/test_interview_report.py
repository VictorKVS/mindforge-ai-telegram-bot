from src.bot.ai.agents.interview_agent import InterviewAgent, InterviewStep


def test_build_report_basic():
    ag = InterviewAgent()

    history = [
        InterviewStep(question="Q1", answer="A1", score=0.5, level="L1"),
        InterviewStep(question="Q2", answer="A2", score=0.8, level="L2"),
    ]

    report = ag.build_report(history)

    assert "summary" in report
    assert "average_score" in report["summary"]
    assert report["summary"]["total_questions"] == 2
    assert "history" in report
    assert isinstance(report["history"], list)
    assert len(report["history"]) == 2
    assert "session_id" in report


def test_report_improvement_detected():
    ag = InterviewAgent()

    history = [
        InterviewStep("Q1", "A1", 0.1, "L1"),
        InterviewStep("Q2", "A2", 0.9, "L2"),
    ]

    report = ag.build_report(history)
    assert report["summary"]["improvement"] > 0.5
