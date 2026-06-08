"""FastAPI backend for the group RAG chatbot."""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.task10_generation import generate_with_citation, llm_is_configured

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("rag.backend")
ROOT_DIR = Path(__file__).parent
FRONTEND_DIR = ROOT_DIR / "frontend"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    top_k: int = Field(default=5, ge=1, le=10)
    use_memory: bool = True
    use_llm: bool = True


class SourceDocument(BaseModel):
    content: str
    score: float = 0.0
    metadata: dict = Field(default_factory=dict)
    source: str = "hybrid"


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[SourceDocument]
    retrieval_source: str
    generation_mode: str
    llm_error: str | None = None
    created_at: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: str


app = FastAPI(
    title="Drug Law RAG Chatbot API",
    version="1.0.0",
    description="Backend API for the group RAG chatbot requirement.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS: dict[str, list[Message]] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _contextualize(session_id: str, message: str, use_memory: bool) -> str:
    if not use_memory:
        return message

    history = SESSIONS.get(session_id, [])[-6:]
    if not history:
        return message

    turns = [f"{item.role}: {item.content}" for item in history]
    return "Ngữ cảnh hội thoại gần đây:\n" + "\n".join(turns) + f"\n\nCâu hỏi hiện tại: {message}"


@app.get("/")
def frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    logger.info("Health check llm_configured=%s active_sessions=%s", llm_is_configured(), len(SESSIONS))
    return {
        "status": "ok",
        "llm_configured": llm_is_configured(),
        "active_sessions": len(SESSIONS),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid4())
    SESSIONS.setdefault(session_id, [])
    logger.info(
        "Chat request session_id=%s chars=%s top_k=%s use_memory=%s use_llm=%s",
        session_id,
        len(request.message),
        request.top_k,
        request.use_memory,
        request.use_llm,
    )

    SESSIONS[session_id].append(
        Message(role="user", content=request.message, created_at=_now())
    )

    query = _contextualize(session_id, request.message, request.use_memory)
    result = generate_with_citation(query, top_k=request.top_k, use_llm=request.use_llm)
    answer = result.get("answer", "Tôi không thể xác minh thông tin này từ nguồn hiện có.")
    logger.info(
        "Chat response session_id=%s generation_mode=%s retrieval_source=%s sources=%s answer_chars=%s",
        session_id,
        result.get("generation_mode", "local"),
        result.get("retrieval_source", "none"),
        len(result.get("sources", [])),
        len(answer),
    )

    SESSIONS[session_id].append(
        Message(role="assistant", content=answer, created_at=_now())
    )

    sources = []
    for item in result.get("sources", []):
        sources.append(
            SourceDocument(
                content=item.get("content", ""),
                score=float(item.get("score", 0.0)),
                metadata=item.get("metadata", {}),
                source=item.get("source", result.get("retrieval_source", "hybrid")),
            )
        )

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=sources,
        retrieval_source=result.get("retrieval_source", "none"),
        generation_mode=result.get("generation_mode", "local"),
        llm_error=result.get("llm_error") or None,
        created_at=_now(),
    )


@app.get("/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    return {"session_id": session_id, "messages": SESSIONS.get(session_id, [])}


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str) -> dict:
    existed = session_id in SESSIONS
    SESSIONS.pop(session_id, None)
    return {"session_id": session_id, "deleted": existed}
