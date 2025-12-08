from unittest.mock import patch
from src.bot.ai.agents.interview_agent import InterviewAgent, InterviewStep


@patch("src.bot.ai.agents.interview_agent.KRClient.query")
def test_interview_flow(mock_query):
    mock_query.return_value = ["asyncio", "threading"]
    ag = InterviewAgent()
    history = []

    # Step 1: First question
    step1 = ag.run_step("Python", "L2", answer=None, history=history)
    assert "question" in step1
    assert len(history) == 1

    # Step 2: Submit answer
    step2 = ag.run_step("Python", "L2", answer="Asyncio uses event loop", history=history)
    assert "score" in step2
    assert "next_question" in step2
    assert len(history) == 2

    # Ensure history entries are InterviewStep
    assert isinstance(history[0], InterviewStep)
    assert isinstance(history[1], InterviewStep)
