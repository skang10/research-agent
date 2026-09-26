import os

import pytest

from app.retrieval.embedder import OpenRouterEmbedder


@pytest.mark.asyncio
@pytest.mark.integration
async def test_openrouter_embedder():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY is not set")

    embedder = OpenRouterEmbedder()

    chunks = [
        "RAG retrieves relevant documents.",
        "Machine learning models learn from data.",
    ]

    embeddings = await embedder.embed(chunks)

    assert len(embeddings) == 2
    assert len(embeddings[0]) > 0
    assert len(embeddings[0]) == len(embeddings[1])
