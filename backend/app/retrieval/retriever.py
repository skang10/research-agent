from app.config import config
from app.db.vector_store.faiss import FaissVectorStore
from app.retrieval.embedder import Embedder


class Retriever:
    def __init__(self, vector_store: FaissVectorStore, embedder: Embedder):

        self.vector_store = vector_store
        self.embedder = embedder

    async def retrieve(self, query: str, top_k: int | None = None) -> list[str]:

        if not top_k:
            top_k = config.retrieval.top_k

        # 1. Embed the query
        embeddings = await self.embedder.embed([query])
        query_embedding = embeddings[0]

        # 2. Search the vector store
        results = self.vector_store.search(query_embedding, top_k)

        return results

    def list_sources(self):
        sources = self.vector_store.list_sources()
        print(f"Uploaded sources: {sources}")
        return self.vector_store.list_sources()
