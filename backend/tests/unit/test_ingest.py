import pytest
from fastapi import UploadFile

from app.db.vector_store.faiss import FaissVectorStore
from app.retrieval.chunker import VanillaChunker
from app.retrieval.embedder import FakeEmbedder
from app.retrieval.ingest import Ingestor
from app.retrieval.parser import VanillaParser


@pytest.mark.asyncio
async def test_ingestor():
    parser = VanillaParser()
    chunker = VanillaChunker()
    embedder = FakeEmbedder()
    vector_store = FaissVectorStore()

    ingestor = Ingestor(parser, chunker, embedder, vector_store)

    with open("tests/fixtures/test_source.txt", "rb") as f:  # noqa: ASYNC230
        upload_file = UploadFile(
            filename="test_source.txt",
            file=f,
            headers={"content-type": "text/plain"},
        )

        await ingestor.ingest(upload_file)

    assert len(vector_store.chunks) > 0
    assert vector_store.index is not None
    assert vector_store.index.ntotal == len(vector_store.chunks)
