# MindForge KM-6 — Interview Agent Specification (v1.0)

## 1. Purpose
Interview Agent is an autonomous AI module responsible for:
- conducting structured technical interviews,
- generating questions of increasing difficulty,
- evaluating candidate answers,
- adjusting difficulty dynamically,
- producing final interview reports.

It operates strictly behind MindForge UAG and uses KR API to fetch relevant domain knowledge.

---

## 2. Inputs

| Field   | Type | Description                                      |
|---------|------|--------------------------------------------------|
| `role`  | str  | Target job role (e.g., `"Python Backend Engineer"`) |
| `level` | str  | Initial difficulty level (`L1`–`L6`)              |
| `answer`| str  | Candidate's answer text                          |

---

## 3. Outputs

| Field         | Type | Description                              |
|---------------|------|------------------------------------------|
| `question`    | str  | Next question                            |
| `score`       | float| Evaluation score (`0.0`–`1.0`)           |
| `next_level`  | str  | Updated difficulty level                  |
| `report`      | dict | Final interview summary (on completion)  |
---

## 4. Capabilities
- generate_question(level, role)
- evaluate_answer(answer, context)
- adjust_difficulty(score)
- build_report(history)

---

## 5. Security Requirements
- MUST pass through UAG policy layer
- MUST not access LLM directly (UAG routes requests)
- MUST mask sensitive data in reports
- MUST log all decisions for audit
- MUST use KR API for context retrieval

---

## 6. External Dependencies
- KR API → `/rag/query`
- UAG → action routing
- LLM → controlled reasoning

---
## 7. Evaluation Algorithm

The final score is computed as a **weighted sum** of five core metrics:

| Metric        | Weight |
|---------------|--------|
| `correctness` | 0.35   |
| `depth`       | 0.25   |
| `structure`   | 0.15   |
| `relevance`   | 0.15   |
| `reasoning`   | 0.10   |

> **Formula**:  
> `Score = (correctness × 0.35) + (depth × 0.25) + (structure × 0.15) + (relevance × 0.15) + (reasoning × 0.10)`  
>  
> Final score is normalized to the range **0.0 – 1.0**.

---

## 8. Python Module Structure

src/bot/ai/agents/interview_agent.py
│
├── class InterviewAgent
│ ├── generate_question()
│ ├── evaluate_answer()
│ ├── adjust_difficulty()
│ ├── build_report()
│ ├── fetch_context()
│ └── run_step()

yaml
Копировать код

---

## 9. Test Coverage Requirements
- test_question_generation
- test_answer_scoring
- test_difficulty_adjustment
- test_report_builder
- test_context_fetching
- test_invalid_inputs