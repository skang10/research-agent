from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.agents.dependencies import AgentDependencies
from app.agents.research_agent import research_agent
from app.models.schema import ResearchRequest

router = APIRouter()


@router.post("/api/research")
async def research(body: ResearchRequest, request: Request) -> StreamingResponse:

    agent_deps = AgentDependencies(retriever=request.app.state.retriever)

    async def generate_response():
        query = body.request
        result = await research_agent.run(query, deps=agent_deps)
        yield result.output

    return StreamingResponse(generate_response(), media_type="text/plain")
