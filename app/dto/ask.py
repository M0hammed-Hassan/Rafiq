from pydantic import BaseModel, Field
from app.config.settings import MAX_QUESTION_CHARS


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_CHARS)
    session_id: str | None = None

class AskResponse(BaseModel):
    answer: str
    usage: dict
    latency_ms: int
    finish_reason:str
    session_id: str | None = None
