from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.research import router as research_router
from app.api.sources import router as sources_router
from app.config import backend_host, backend_port, frontend_url
from app.db.vector_store.faiss import FaissVectorStore
from app.retrieval.chunker import VanillaChunker
from app.retrieval.embedder import OpenRouterEmbedder
from app.retrieval.ingest import Ingestor
from app.retrieval.parser import VanillaParser
from app.retrieval.retriever import Retriever


@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_store = FaissVectorStore()
    parser = VanillaParser()
    chunker = VanillaChunker()
    embedder = OpenRouterEmbedder()
    app.state.ingestor = Ingestor(parser, chunker, embedder, vector_store)
    app.state.retriever = Retriever(vector_store, embedder)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sources_router)
app.include_router(research_router)


@app.get("/")
async def root():
    return {"message": "Backend is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=backend_host, port=backend_port, reload=True)
