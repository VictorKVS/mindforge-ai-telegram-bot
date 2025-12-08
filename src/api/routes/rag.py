from fastapi import APIRouter
from pydantic import BaseModel
from src.bot.ai.rag_engine import RAGEngine

router = APIRouter()
rag = RAGEngine()

class RAGQuery(BaseModel):
    query: str
    k: int = 3

@router.post("/query")   # ← ДОЛЖНО БЫТЬ ТАК
def rag_query(payload: RAGQuery):
    context = rag.query(payload.query, payload.k)
    return {"query": payload.query, "context": context}
