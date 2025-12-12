from .agent import AgentL0


def run_agent(text: str) -> dict:
    agent = AgentL0()
    return agent.handle_text(text)


if __name__ == "__main__":
    result = run_agent("Сколько стоит цемент М500?")
    print(result)
