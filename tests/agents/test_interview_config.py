from src.bot.ai.agents.interview_agent import InterviewAgent, AgentConfig


def test_config_overrides_thresholds():
    config = AgentConfig(
        evaluation_threshold_easy=0.4,
        evaluation_threshold_hard=0.9
    )
    ag = InterviewAgent(config=config)

    # Hard threshold 0.9 → no increase
    level = ag.adjust_difficulty(0.85, "L2")
    assert level == "L2"

    # Easy threshold 0.4 → decrease
    level2 = ag.adjust_difficulty(0.3, "L2")
    assert level2 == "L1"


def test_context_disabled():
    config = AgentConfig(enable_context_retrieval=False)
    ag = InterviewAgent(config=config)

    ctx = ag.fetch_context("something")
    assert ctx == []  # context retrieval disabled
