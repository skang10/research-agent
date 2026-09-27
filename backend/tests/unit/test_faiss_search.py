from app.db.vector_store.faiss import FaissVectorStore


def test_faiss_vector_store():
    store = FaissVectorStore()

    chunks = ["chunk1", "chunk2", "chunk3"]
    embeddings = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
    sources = ["test_file.txt"] * 3
    store.add(chunks, embeddings, sources)

    query_embedding = [0.1, 0.2]
    top_k = 2
    results = store.search(query_embedding, top_k)

    assert len(results) == 2
    assert "chunk1" in results


def test_empty_index_search():
    store = FaissVectorStore()
    query_embedding = [0.1, 0.2]
    top_k = 2
    try:
        store.search(query_embedding, top_k)
    except ValueError as e:
        assert str(e) == "The index is empty. Use the 'add' method to add vectors before searching."
