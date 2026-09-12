from app.core.llm_client import chat_completion
from app.prompts.system_prompts import DIRECT_SYSTEM_PROMPT

def answer_directly(question: str) -> dict:
    result = chat_completion(
        messages=[
            {"role": "system", "content":DIRECT_SYSTEM_PROMPT},
            {"role":"user", "content": question}
        ],
        temperature=0.3,
        max_tokens=500
    )
    result["sources"] = []
    return result