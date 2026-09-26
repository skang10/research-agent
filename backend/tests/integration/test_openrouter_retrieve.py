import os

import pytest
from fastapi import UploadFile

from app.db.vector_store.faiss import FaissVectorStore
from app.retrieval.chunker import VanillaChunker
from app.retrieval.embedder import OpenRouterEmbedder
from app.retrieval.ingest import Ingestor
from app.retrieval.parser import VanillaParser
from app.retrieval.retriever import Retriever


@pytest.mark.asyncio
@pytest.mark.integration
async def test_openrouter_ingest():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY is not set")

    parser = VanillaParser()
    chunker = VanillaChunker(chunk_size=20)
    embedder = OpenRouterEmbedder()
    vector_store = FaissVectorStore()
    retriever = Retriever(vector_store, embedder)

    ingestor = Ingestor(parser, chunker, embedder, vector_store)

    with open("tests/fixtures/test_source.txt", "rb") as f:  # noqa: ASYNC230
        upload_file = UploadFile(
            filename="test_source.txt",
            file=f,
            headers={"content-type": "text/plain"},
        )

        await ingestor.ingest(upload_file)

    search_query = "Who attended the meeting?"
    search_results = await retriever.retrieve(search_query, top_k=3)
    print(f"Search results for query '{search_query}': {search_results}")

    assert len(search_results) > 0
    assert any("Mara" in chunk for chunk in search_results)
