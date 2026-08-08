from app.core.llm_client import embed_text
from app.core.vectore_store import vector_store
from app.config.settings import COMPANY_KB_SCOPE, TOP_K

def retrieve(question: str, top_k: int = TOP_K, scope: str = COMPANY_KB_SCOPE) -> list[dict]:
    query_embedding = embed_text(question)
    return vector_store.query(query_embedding, top_k=top_k, scope=scope)