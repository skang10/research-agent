from fastapi import UploadFile

from app.db.vector_store.base import VectorStore
from app.retrieval.chunker import Chunker
from app.retrieval.embedder import Embedder
from app.retrieval.parser import Parser


class Ingestor:
    def __init__(
        self, parser: Parser, chunker: Chunker, embedder: Embedder, vector_store: VectorStore
    ):
        self.parser = parser
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    async def ingest(self, file: UploadFile) -> None:

        # 1. Read the file content
        content = await file.read()
        content_type = file.content_type

        # 2. Parse the content
        parsed_content = self.parser.parse(content, content_type)

        # 3. Chunk the parsed content
        chunks = self.chunker.chunk(parsed_content)

        # 4. Embed the chunks
        embeddings = await self.embedder.embed(chunks)

        # 5. Store the chunks and embeddings in the vector store
        self.vector_store.add(chunks, embeddings)
