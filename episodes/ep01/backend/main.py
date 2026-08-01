import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set"
    )

MODEL = os.getenv("OPENAI_MODEL")
REQUEST_TIMEOUT_SECONDS = 20

SYSTEM_PROMPT = (
    "You are an internal assistant for company employees"
    "Answer clearly and concistly. If you don't know the answer"
    "say so directly instead of guessing"
)

MAX_QUESTION_CHARS = 200

client = OpenAI(api_key=API_KEY, timeout=REQUEST_TIMEOUT_SECONDS)

app = FastAPI(title="Baseline Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_origins=["*"],
    allow_methods=["POST"],
)

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_CHARS)

class AskResponse(BaseModel):
    answer: str
    usage: dict
    latency_ms: int
    finish_reason:str



@app.get("/health")
def health():
    return {"status":"ok", "model":MODEL}


@app.post("/api/ask", response_model=AskResponse)
def ask(payload:AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    started = time.perf_counter()

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content":SYSTEM_PROMPT},
            {"role":"user", "content":question}
        ],
        temperature=0.3,
        max_tokens=200)

    latency_ms = int((time.perf_counter() - started) * 1000)
    
    choice = completion.choices[0]
    answer = choice.message.content or ""
    finish_reason = choice.finish_reason

    if finish_reason == "length":
        answer += "\n\n[Note: this answer maybe incomplete, it hits the length lmit]"
    elif finish_reason == "content_filter":
        raise HTTPException(status_code=422, detail="This question couldn't be answered")

    usage = {
        "prompt_tokens":completion.usage.prompt_tokens,
        "completion_tokens":completion.usage.completion_tokens,
        "total_tokens":completion.usage.total_tokens
    }

    return AskResponse(
        usage=usage,
        answer=answer,
        finish_reason=finish_reason,
        latency_ms=latency_ms
    )

