from app.core.chunking import chunk_text
from app.core.llm_client import embed_batch
from app.core.vectore_store import vector_store

def ingest_text(source: str, text:str, scope: str) -> int:
    pieces = chunk_text(text)
    if not pieces:
        return 0

    ids = [f"{scope}::{source}::{i}" for i in range(len(pieces))]
    metadatas = [
       {"source":source, "chunk_index":i, "scope":scope} for i in range(len(pieces))
    ]
    embeddings = embed_batch(pieces)
    vector_store.add(ids, embeddings, pieces, metadatas)

    return len(pieces)