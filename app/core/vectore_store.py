import chromadb
from app.config.settings import CHROMA_DIR, COLLECTION_NAME

class VectoreStore:
    def __init__(self):
        self._client = chromadb.PersistentClient(path = CHROMA_DIR)
        self._collection = self._client.get_or_create_collection(COLLECTION_NAME)

    def add(self, ids:list[str], embeddings:list[list[float]], documents: list[str], metadatas:list[dict]) -> None:
        self._collection.add(ids = ids,
                             embeddings=embeddings,
                             documents=documents,
                             metadatas=metadatas)        

    def query(self, embedding: list[float], top_k: int, scope: str | None = None) -> list[dict]:
        where = {"scope":scope} if scope else None
        results = self._collection.query(query_embeddings=[embedding],
                                         n_results = top_k,
                                         where=where)

        chunks = []
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0] 

        for i in range(len(ids)):
            chunks.append(
                {
                    "id": ids[i],
                    "text": docs[i],
                    "source": metas[i].get("source"),
                    "distance":distances[i]
                }
            )
        return chunks

    def count(self) -> int:
        return self._collection.count()
  

# Module Level Singletone
vector_store = VectoreStore()