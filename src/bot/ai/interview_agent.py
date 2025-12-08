import re
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel


# =============================================================
# KR API CLIENT
# =============================================================

class KRClient:
    """
    Placeholder для взаимодействия с Knowledge Retrieval API.
    В тестах заменяется через mock.
    """

    def query(self, query_text: str) -> List[str]:
        # В реальном применение: POST /rag/query
        return []


# =============================================================
# CONFIGURATION MODEL
# =============================================================

class AgentConfig(BaseModel):
    default_role: str = "Python"
    start_level: str = "L1"

    evaluation_threshold_easy: float = 0.5
    evaluation_threshold_hard: float = 0.8

    max_questions: int = 10
    enable_context_retrieval: bool = True
    enable_llm_eval: bool = False  # Зарезервировано под расширение
    llm_backend: Optional[str] = None


# =============================================================
# INTERVIEW SESSION STEP CONTAINER
# =============================================================

class InterviewStep:
    """
    Хранит одно действие агента: вопрос → ответ → оценка.
    """

    def __init__(
        self,
        question: str,
        level: str,
        answer: Optional[str] = None,
        score: float = 0.0,
        feedback: Optional[str] = None,
    ):
        self.question = question
        self.answer = answer
        self.score = score
        self.level = level
        self.timestamp = datetime.now()
        self.feedback = feedback

    def to_dict(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "score": self.score,
            "level": self.level,
            "timestamp": self.timestamp.isoformat(),
            "feedback": self.feedback,
        }


# =============================================================
# MAIN INTERVIEW AGENT (KM-6 MODULE)
# =============================================================

class InterviewAgent:
    """
    InterviewAgent — KM-6 когнитивный модуль.
    Реализует:
    - генерацию вопросов
    - адаптивную сложность
    - эвристическую оценку ответа
    - интеграцию с KR API
    - историю сеанса
    - расширенную аналитику
    """

    LEVELS = ["L1", "L2", "L3", "L4", "L5", "L6"]

    QUESTION_BANK = {
        "Python": {
            "L1": [
                "What is a variable in Python?",
                "Explain the difference between a list and a tuple."
            ],
            "L2": [
                "What is a virtual environment and why is it used?",
                "Explain how Python decorators work."
            ],
            "L3": [
                "Explain the difference between asyncio and threading.",
                "What is WSGI, and why do Python servers use it?"
            ],
            "L4": [
                "How would you design a scalable microservice architecture?",
                "When should Redis be used in backend applications?"
            ],
            "L5": [
                "Explain GIL and how it impacts multithreaded Python applications.",
                "How do you optimize CPU-bound workloads in Python?"
            ],
            "L6": [
                "Design a fault-tolerant distributed system for high-load tasks.",
                "Explain how you would orchestrate large-scale data pipelines."
            ]
        }
    }

    # ---------------------------------------------------------
    # INIT
    # ---------------------------------------------------------
    def __init__(
        self,
        kr_client: Optional[KRClient] = None,
        config: Optional[AgentConfig] = None,
    ):
        self.kr_client = kr_client or KRClient()
        self.config = config or AgentConfig()

    # ---------------------------------------------------------
    # QUESTION GENERATION
    # ---------------------------------------------------------
    def generate_question(
        self,
        role: str,
        level: str,
        question_index: int = 0
    ) -> str:
        if role not in self.QUESTION_BANK:
            raise ValueError(f"Unsupported role: {role}")

        if level not in self.QUESTION_BANK[role]:
            raise ValueError(f"Unsupported level: {level}")

        questions = self.QUESTION_BANK[role][level]

        # Циклический индекс для расширения в будущем
        idx = question_index % len(questions)

        return questions[idx]

    # ---------------------------------------------------------
    # CONTEXT FETCHING
    # ---------------------------------------------------------
    def fetch_context(self, answer_text: str) -> List[str]:
        if not self.config.enable_context_retrieval:
            return []

        return self.kr_client.query(answer_text)

    # ---------------------------------------------------------
    # ANSWER EVALUATION
    # ---------------------------------------------------------
    def evaluate_answer(
        self,
        answer: str,
        context: Optional[List[str]] = None
    ) -> float:

        if not answer or not isinstance(answer, str):
            return 0.0

        score = 0.0
        text = answer.lower().strip()

        # correctness
        keywords = ["python", "thread", "async", "event", "gil", "concurrency"]
        correctness = any(kw in text for kw in keywords)
        score += 0.35 if correctness else 0.05

        # depth
        depth_factor = min(len(text.split()) / 15, 1.0)
        score += depth_factor * 0.25

        # structure
        structure_ok = bool(re.search(r"[.;:]", text))
        score += 0.15 if structure_ok else 0.05

        # relevance
        if context:
            relevance = any(c.lower() in text for c in context)
            score += 0.15 if relevance else 0.05
        else:
            score += 0.05

        # reasoning
        reasoning_ok = any(x in text for x in ["because", "so ", "therefore", "thus"])
        score += 0.10 if reasoning_ok else 0.02

        return min(score, 1.0)

    # ---------------------------------------------------------
    # DIFFICULTY ADJUSTMENT
    # ---------------------------------------------------------
    def adjust_difficulty(self, score: float, current_level: str) -> str:
        if current_level not in self.LEVELS:
            raise ValueError(f"Invalid level: {current_level}")

        idx = self.LEVELS.index(current_level)

        if score >= self.config.evaluation_threshold_hard and idx < len(self.LEVELS) - 1:
            return self.LEVELS[idx + 1]

        if score < self.config.evaluation_threshold_easy and idx > 0:
            return self.LEVELS[idx - 1]

        return current_level

    # ---------------------------------------------------------
    # REPORT
    # ---------------------------------------------------------
    def build_report(self, history: List[InterviewStep]) -> Dict[str, Any]:
        if not history:
            return {"error": "No interview data"}

        scores = [step.score for step in history]
        avg_score = sum(scores) / len(scores)
        delta = scores[-1] - scores[0] if len(scores) > 1 else 0

        strengths = []
        weaknesses = []

        if avg_score >= 0.7:
            strengths.append("Strong reasoning and technical knowledge.")
        else:
            weaknesses.append("Needs deeper technical understanding.")

        if delta > 0.1:
            strengths.append("Demonstrated improvement during interview.")

        by_level = {}
        for step in history:
            by_level.setdefault(step.level, []).append(step.score)

        return {
            "session_id": str(uuid.uuid4()),
            "summary": {
                "total_questions": len(history),
                "average_score": round(avg_score, 3),
                "improvement": round(delta, 3),
            },
            "by_level": {
                level: {
                    "count": len(scores),
                    "avg_score": round(sum(scores) / len(scores), 3)
                }
                for level, scores in by_level.items()
            },
            "history": [s.to_dict() for s in history],
            "timestamp": datetime.now().isoformat()
        }

    # ---------------------------------------------------------
    # RUN STEP
    # ---------------------------------------------------------
    def run_step(
        self,
        role: str,
        level: str,
        answer: Optional[str],
        history: List[InterviewStep]
    ) -> Dict[str, Any]:

        # STEP 1 — нет ответа → генерируем вопрос
        if answer is None:
            q = self.generate_question(role, level)
            step = InterviewStep(question=q, level=level)
            history.append(step)
            return {"question": q, "level": level}

        # STEP 2 — получаем последний вопрос
        last_step = history[-1]

        # STEP 3 — контекст
        context = self.fetch_context(answer)

        # STEP 4 — оценка
        score = self.evaluate_answer(answer, context)
        last_step.answer = answer
        last_step.score = score

        # STEP 5 — изменяем уровень сложности
        next_level = self.adjust_difficulty(score, level)

        # STEP 6 — новый вопрос
        next_question = self.generate_question(role, next_level)

        new_step = InterviewStep(question=next_question, level=next_level)
        history.append(new_step)

        return {
            "score": score,
            "next_level": next_level,
            "next_question": next_question
        }
