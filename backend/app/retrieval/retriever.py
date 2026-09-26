from app.db.vector_store.faiss import FaissVectorStore
from app.retrieval.embedder import Embedder


class Retriever:
    def __init__(self, vector_store: FaissVectorStore, embedder: Embedder):

        self.vector_store = vector_store
        self.embedder = embedder

    async def retrieve(self, query: str, top_k: int) -> list[str]:
        # 1. Embed the query
        embeddings = await self.embedder.embed([query])
        query_embedding = embeddings[0]

        # 2. Search the vector store
        results = self.vector_store.search(query_embedding, top_k)

        return results
