from app.core.llm_client import chat_completion
from app.prompts.system_prompts import ROUTER_SYSTEM_PROMPT
from app.config.settings import ROUTER_MAX_TOKENS, ROUTER_TEMPERATURE


def is_confident_direct_answer(question: str) -> bool:
    result = chat_completion(messages=[
        {"role": "system", "content":ROUTER_SYSTEM_PROMPT},
        {"role":"user", "content":question}
    ],
    temperature=ROUTER_TEMPERATURE,
    max_tokens=ROUTER_MAX_TOKENS)
    return result["answer"].strip().upper().startswith("YES")