from app.core.llm_client import chat_completion
from app.prompts.system_prompts import RAFIQ_SYSTEM_PROMPT, build_context_block, build_user_message

def synthesize(question:str, chunks:list[dict]) -> dict:
    context_block = build_context_block(chunks)
    user_message = build_user_message(question, context_block)

    results = chat_completion(messages=[
        {"role":"system", "content":RAFIQ_SYSTEM_PROMPT},
        {"role":"user", "content":user_message}
    ])

    results["sources"] = sorted({chunk["source"] for chunk in chunks})
    return results
