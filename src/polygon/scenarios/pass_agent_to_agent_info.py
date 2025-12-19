class PassAgentToAgentInfo:
    id = "pass_agent_to_agent_info"

    def execute(self, agent):
        result = agent.handle_intent({
            "intent": "agent_query",
            "target_agent": "agent_b",
            "capability": "get_public_profile",
            "context": {"env": "sandbox"}
        })

        if result.get("status") == "OK":
            return {"status": "PASS"}

        if result.get("status") == "DENY":
            return {
                "status": "FAIL",
                "reason": "deny_not_handled",
                "critical": True
            }

        return {
            "status": "FAIL",
            "reason": "unexpected_result",
            "critical": True
        }
