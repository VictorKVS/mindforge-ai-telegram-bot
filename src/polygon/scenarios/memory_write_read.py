# src/polygon/scenarios/memory_write_read.py

class MemoryWriteReadScenario:
    id = "pass_memory_write_read"

    def execute(self, agent):
        result = agent.memory_write("session", "key", {"x": 1})

        if result["status"] == "DENY":
            return {
                "status": "FAIL",
                "reason": "memory_write_denied",
                "critical": True   # ← ВОТ ЭТО
            }

        read = agent.memory_read("session", "key")

        if read["data"] is None:
            return {
                "status": "FAIL",
                "reason": "memory_read_empty",
                "critical": False
            }

        return {"status": "PASS"}
