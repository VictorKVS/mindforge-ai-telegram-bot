from fastapi import FastAPI
from src.api.routes.rag import router as rag_router

app = FastAPI()

app.include_router(rag_router, prefix="/rag")
