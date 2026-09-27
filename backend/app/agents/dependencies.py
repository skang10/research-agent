# https://pydantic.dev/docs/ai/core-concepts/dependencies/#accessing-dependencies

from dataclasses import dataclass

from app.retrieval.retriever import Retriever


@dataclass
class AgentDependencies:
    retriever: Retriever
