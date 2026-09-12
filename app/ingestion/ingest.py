from app.core.chunking import chunk_text
from app.core.ingestion import ingest_text
from app.core.llm_client import embed_batch
from app.core.vectore_store import vector_store
from app.config.settings import  COMPANY_KB_SCOPE
from app.core.document_loader import load_documents


def run():
    documents = load_documents()
    if not documents:
        print("Nothing to ingest")
        return

    total_chunks = 0

    for doc in documents:
        count = ingest_text(doc["source"], doc["text"],COMPANY_KB_SCOPE)
        total_chunks += count

    print(f"Done. Vector store now has {vector_store.count()} chunk total")
    
if __name__ == "__main__":
    run()