import tiktoken
from app.config.settings import CHAT_MODEL, CHUNK_OVERLAP_TOKENS, CHUNK_SIZE_TOKENS

_enconding = tiktoken.encoding_for_model(CHAT_MODEL)

def chunk_text(text: str) -> list[str]:
    tokens = _enconding.encode(text)
    if not tokens:
        return []

    start = 0
    chunks = []
    step = CHUNK_SIZE_TOKENS - CHUNK_OVERLAP_TOKENS 
    while start < len(tokens):
        window = tokens[start: start + CHUNK_SIZE_TOKENS]  
        chunks.append(_enconding.decode(window))
        start += step
    return chunks
