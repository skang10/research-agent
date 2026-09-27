from backend.app.agents.dependencies import AgentDependencies
from pydantic_ai import RunContext

from app.agents.research_agent import research_agent


@research_agent.tool
async def local(ctx: RunContext[AgentDependencies], query: str) -> list[str]:
    """Search the uploaded documents for relevant information according to the query."""

    return ctx.deps.retriever.retrieve(query)
