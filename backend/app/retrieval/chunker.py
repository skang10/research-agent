import re
from abc import ABC, abstractmethod

from app.config import config


class Chunker(ABC):
    @abstractmethod
    def chunk(self, content: str) -> list[str]:
        pass


class VanillaChunker(Chunker):
    def __init__(self, chunk_size: int = None):
        if chunk_size is not None:
            self.chunk_size = chunk_size
        else:
            self.chunk_size = config.retrieval.chunk_size

    def chunk(self, content: str) -> list[str]:
        # 1. split into sentences using regex
        # 2. group sentences into chunks if size <= chunk_size

        sentences = re.split(r"(?<=[.!?])\s+", content.strip())
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)

        return chunks


class LlamaIndexChunker(Chunker):
    def chunk(self, content: str) -> list[str]:
        raise NotImplementedError("LlamaIndexChunker is not implemented yet.")
