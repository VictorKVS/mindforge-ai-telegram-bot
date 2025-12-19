# src/polygon/scenarios/memory_tests.py

class MemoryAccessScenario:
    name = "pass_memory_write_read_cycle"

    def execute(self, agent):
        try:
            # write
            write_result = agent.call_uag({
                "intent": "memory_write",
                "memory_scope": "session",
                "key": "order_state",
                "value": {"step": "price_received"}
            })

            if write_result["status"] != "OK":
                return {
                    "status": "FAIL",
                    "reason": "memory_write_failed",
                    "critical": False
                }

            # read
            read_result = agent.call_uag({
                "intent": "memory_read",
                "memory_scope": "session",
                "key": "order_state"
            })

            if read_result["status"] != "OK":
                return {
                    "status": "FAIL",
                    "reason": "memory_read_failed",
                    "critical": False
                }

            if read_result["data"]["value"]["step"] != "price_received":
                return {
                    "status": "FAIL",
                    "reason": "memory_value_mismatch",
                    "critical": False
                }

            return {"status": "PASS"}

        except Exception as e:
            return {
                "status": "FAIL",
                "reason": str(e),
                "critical": True
            }
