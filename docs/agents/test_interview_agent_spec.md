# Test Plan — Interview Agent (KM-6)

## 1. Test: Question Generation
### Input:
role="Python", level="L2"
### Expected:
- non-empty question string
- complexity keywords matching L2

## 2. Test: Answer Evaluation
### Input:
answer="Threading uses OS threads..."
### Expected:
- score between 0.0–1.0
- breakdown per metrics

## 3. Test: Difficulty Adjustment
### Input:
score=0.85
### Expected:
next_level = L3

## 4. Test: Fetch Context (KR API)
Mock:
`/rag/query` -> returns vector matches

Expected:
- context injected into evaluator
- no direct LLM calls

## 5. Test: Report Builder
Given interview history:
questions, answers, scores
Expected:
- JSON report containing summary, strengths, weaknesses

## 6. Test: Invalid Inputs
role=None → error
level="L9" → error
answer="" → error