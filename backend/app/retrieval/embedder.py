from abc import ABC, abstractmethod

import requests

from app.config import config, openrouter_api_key


class Embedder(ABC):
    @abstractmethod
    def embed(self, chunks: list[str]) -> list[list[float]]:
        pass


class OpenRouterEmbedder(Embedder):
    def embed(self, chunks: list[str]) -> list[list[float]]:

        # https://openrouter.ai/docs/api_reference/embeddings

        print(f"Sending {len(chunks)} chunks to OpenRouter API for embedding...")
        print("Embedding model used: ", config.retrieval.embedding_model)

        response = requests.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={"model": config.retrieval.embedding_model, "input": chunks},
        )

        data = response.json()
        embeddings = [item["embedding"] for item in data["data"]]
        print(f"Received {len(embeddings)} embeddings from OpenRouter API.")
        print("Embedding dimension: ", len(embeddings[0]) if embeddings else 0)

        return embeddings
