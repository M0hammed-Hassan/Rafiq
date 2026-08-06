from app.core.chunking import chunk_text
from app.core.llm_client import embed_batch
from app.core.vectore_store import vector_store
from app.config.settings import  COMPANY_KB_SCOPE
from app.core.document_loader import load_documents


def run():
    documents = load_documents()
    if not documents:
        print("Nothing to ingest")
        return

    all_chunks, all_metadata, all_ids = [], [], []

    for doc in documents:
        pieces = chunk_text(doc["text"])
        for i, piece in enumerate(pieces):
            all_chunks.append(piece)
            all_metadata.append(
                {"source":doc["source"], "chunk_index":i, "scope":COMPANY_KB_SCOPE}
            )
            all_ids.append(f"{doc['source']}::{i}")

        print(f"{doc["source"]}: {len(pieces)} chunk(s)")

    print(f"Embedding {len(all_chunks)} chunks...")
    embeddings = embed_batch(all_chunks)
    vector_store.add(ids=all_ids, embeddings=embeddings, documents=all_chunks, metadatas=all_metadata)
    print(f"Done. Vectore store now has {vector_store.count()} chunks total.")


if __name__ == "__main__":
    run()