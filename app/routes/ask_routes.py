import time
import logging
from app.core.retrieval import retrieve
from app.core.synthesis import synthesize
from app.config.settings import CHAT_MODEL
from fastapi import APIRouter, HTTPException
from app.core.vectore_store import vector_store
from app.dto.ask import AskRequest, AskResponse


logger = logging.getLogger("rafiq")
router = APIRouter()


@router.get("/health")
def health():
    return {
        "status":"ok",
        "model":CHAT_MODEL,
        "indexed_chunks":vector_store.count()
    }


@router.post("/api/ask", response_model=AskResponse)
def ask(payload:AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    started = time.perf_counter()

    chunks = retrieve(question)
    result = synthesize(question, chunks)

    latency_ms = int((time.perf_counter() - started) * 1000)

    answer = result["answer"]    

    if result["finish_reason"] == "length":
        answer += "\n\n[Note: this answer maybe incomplete, it hits the length lmit]"
    logger.info(
        "question=%r source=%s usage=%s latency_ms=%d",
        question[:80], result["sources"], result["usage"], latency_ms
    )

    return AskResponse(
        answer=answer,
        usage=result["usage"],
        latency_ms=latency_ms,
        session_id=payload.session_id,
        finish_reason=result["finish_reason"],
    )
