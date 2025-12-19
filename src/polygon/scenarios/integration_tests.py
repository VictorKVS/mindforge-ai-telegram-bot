# src/polygon/scenarios/integration_tests.py

class IntegrationScenario:
    name = "integration_memory_kb_chain"

    def execute(self, agent):
        try:
            # Step 1: write context
            agent.call_uag({
                "intent": "memory_write",
                "memory_scope": "session",
                "key": "topic",
                "value": {"query": "return policy"}
            })

            # Step 2: read context
            mem = agent.call_uag({
                "intent": "memory_read",
                "memory_scope": "session",
                "key": "topic"
            })

            query = mem["data"]["value"]["query"]

            # Step 3: KB query using memory-derived input
            kb = agent.call_uag({
                "intent": "knowledge_query",
                "kb_scope": "public",
                "query": query
            })

            if kb["status"] != "OK":
                return {
                    "status": "FAIL",
                    "reason": "kb_query_failed_after_memory",
                    "critical": False
                }

            return {"status": "PASS"}

        except Exception as e:
            return {
                "status": "FAIL",
                "reason": str(e),
                "critical": True
            }
