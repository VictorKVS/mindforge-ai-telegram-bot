# src/polygon/scenarios/kb_tests.py

class KBAccessScenario:
    name = "pass_kb_public_query"

    def execute(self, agent):
        try:
            result = agent.call_uag({
                "intent": "knowledge_query",
                "kb_scope": "public",
                "query": "return policy"
            })

            if result["status"] != "OK":
                return {
                    "status": "FAIL",
                    "reason": "kb_query_denied",
                    "critical": False
                }

            data = result.get("data", [])
            if not isinstance(data, list):
                return {
                    "status": "FAIL",
                    "reason": "kb_invalid_response_shape",
                    "critical": True
                }

            for doc in data:
                for field in ("document_id", "source", "version"):
                    if field not in doc:
                        return {
                            "status": "FAIL",
                            "reason": "kb_missing_mandatory_field",
                            "critical": True
                        }

            return {"status": "PASS"}

        except Exception as e:
            return {
                "status": "FAIL",
                "reason": str(e),
                "critical": True
            }
