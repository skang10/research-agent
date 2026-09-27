from app.retrieval.chunker import VanillaChunker


def test_vanilla_chunker():
    chunker = VanillaChunker(chunk_size=10)
    content = "This is a test. This is only a test. This is a very long sentence that should be split into multiple chunks."  # noqa: E501
    chunks = chunker.chunk(content)
    assert chunks == [
        "This is a test.",
        "This is only a test.",
        "This is a very long sentence that should be split into multiple chunks.",  # noqa: E501
    ]


def test_empty_content():
    chunker = VanillaChunker(chunk_size=10)
    content = ""
    chunks = chunker.chunk(content)
    assert chunks == []
