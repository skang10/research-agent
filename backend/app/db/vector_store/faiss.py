import faiss
import numpy as np

from app.db.vector_store.base import VectorStore


class FaissVectorStore(VectorStore):
    def __init__(self):
        self.index = None
        self.chunks = []

    def _setup_faiss_index(self, dimension: int) -> None:
        self.dimension = dimension
        self.index = faiss.IndexHNSWFlat(
            dimension, 32, faiss.METRIC_INNER_PRODUCT
        )  # M=32: neighbors per node
        self.index.hnsw.efConstruction = 40  # graph construction quality
        self.index.hnsw.efSearch = 64  # higher = better recall, slower
        self.chunks = []

    def add(self, chunks: list[str], embeddings: list[list[float]]) -> None:
        vectors = np.array(embeddings, dtype="float32")
        faiss.normalize_L2(vectors)
        dimension = vectors.shape[1]

        if self.index is None:
            self._setup_faiss_index(dimension)

        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(self, query_embedding: list[float], top_k: int) -> list[str]:
        if self.index is None:
            raise ValueError(
                "The index is empty. Use the 'add' method to add vectors before searching."
            )

        query_vector = np.array([query_embedding], dtype="float32")

        faiss.normalize_L2(query_vector)

        _, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:  # check for valid index
                results.append(self.chunks[idx])
        return results
