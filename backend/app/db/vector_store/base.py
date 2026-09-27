from abc import ABC, abstractmethod


class VectorStore(ABC):
    @abstractmethod
    def add(self, chunks: list[str], embeddings: list[list[float]], sources: list[str]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int) -> list[str]:
        pass
