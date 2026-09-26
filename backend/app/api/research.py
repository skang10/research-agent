import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schema import ResearchRequest

router = APIRouter()


@router.post("/api/research")
async def research(request: ResearchRequest) -> StreamingResponse:

    async def generate_response():

        yield f"Received request: {request.request}\n"

        yield "Starting research...\n"

        for i in range(5):
            await asyncio.sleep(1)
            yield f"Chunk {i + 1}\n"

        yield "Research completed.\n"

    return StreamingResponse(generate_response(), media_type="text/plain")
