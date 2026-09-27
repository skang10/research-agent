import os
from pathlib import Path

import dotenv
import yaml
from pydantic import BaseModel

dotenv.load_dotenv()

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config.yaml"


class StorageConfig(BaseModel):
    sources_dir: str


class RetrievalConfig(BaseModel):
    chunk_size: int
    embedding_model: str


class ResearchAgentConfig(BaseModel):
    model: str


class AppConfig(BaseModel):
    storage: StorageConfig
    retrieval: RetrievalConfig
    research_agent: ResearchAgentConfig


def load_config(file_path: str) -> AppConfig:

    with open(file_path) as f:
        config_dict = yaml.safe_load(f)
    return AppConfig.model_validate(config_dict)


config = load_config(DEFAULT_CONFIG)

backend_host = os.getenv("BACKEND_HOST", "127.0.0.1")
backend_port = int(os.getenv("BACKEND_PORT", 8787))
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
