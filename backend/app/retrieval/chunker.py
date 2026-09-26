import re
from abc import ABC, abstractmethod


class Chunker(ABC):
    @abstractmethod
    def chunk(self, content: str) -> list[str]:
        pass


class VanillaChunker(Chunker):
    def __init__(self, chunk_size: int = 1024):
        self.chunk_size = chunk_size

    def chunk(self, content: str) -> list[str]:
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
