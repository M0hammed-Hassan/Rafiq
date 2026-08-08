RAFIQ_SYSTEM_PROMPT = (
    "You are Rafiq, and internal assistant for company employees"
    "You can answer user generic questions (e.g, places, sience, technology, traveling, and more)"
    "if the user asked a specific question related to the company knowledge base, answer using only the context provided"
)

def build_user_message(question: str, context_block: str) -> str:
    return f"Context:\n{context_block}\n\nQuestion: {question}"

def build_context_block(chunks: list[dict]) -> str:
    if not chunks:
        return "(no relevent context found)"

    parts = [f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in chunks]
    return "\n\n---\n\n".join(parts)
