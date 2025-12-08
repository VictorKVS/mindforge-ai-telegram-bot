import pytest
from unittest.mock import patch
from src.bot.ai.agents.interview_agent import (
    InterviewAgent,
    InterviewStep,
    AgentConfig,
    KRClient
)


@pytest.fixture
def agent():
    return InterviewAgent()


def test_generate_question_valid():
    q = agent().generate_question(role="Python", level="L2", question_index=0)
    assert isinstance(q, str)
    assert len(q) > 5


def test_generate_question_invalid_role():
    with pytest.raises(ValueError):
        agent().generate_question("Java", "L1")


def test_generate_question_invalid_level():
    with pytest.raises(ValueError):
        agent().generate_question("Python", "L99")


@patch("src.bot.ai.agents.interview_agent.KRClient.query")
def test_fetch_context(mock_query):
    mock_query.return_value = ["threading", "asyncio"]
    ag = InterviewAgent()
    ctx = ag.fetch_context("test")
    assert ctx == ["threading", "asyncio"]


def test_evaluate_answer_basic():
    ag = agent()
    score = ag.evaluate_answer("Python uses GIL for threading")
    assert 0.0 <= score <= 1.0
    assert score > 0.05  # должна быть > минимального


def test_evaluate_answer_with_context():
    ag = agent()
    score = ag.evaluate_answer(
        "Asyncio uses event loop", 
        context=["event loop", "concurrency"]
    )
    assert score > 0.2


def test_adjust_difficulty_increase():
    ag = agent()
    next_level = ag.adjust_difficulty(0.9, "L2")
    assert next_level == "L3"


def test_adjust_difficulty_decrease():
    ag = agent()
    next_level = ag.adjust_difficulty(0.3, "L3")
    assert next_level == "L2"


def test_adjust_difficulty_stay():
    ag = agent()
    next_level = ag.adjust_difficulty(0.6, "L3")
    assert next_level == "L3"
