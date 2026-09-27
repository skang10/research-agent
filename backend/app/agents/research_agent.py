from pydantic_ai import Agent, RunContext

from app.agents.dependencies import AgentDependencies
from app.config import config

SYSTEM_PROMPT = "You are a research agent. "

research_agent = Agent(
    model=f"openrouter:{config.research_agent.model}",
    deps_type=AgentDependencies,
    instructions=SYSTEM_PROMPT,
)


@research_agent.tool
async def local_search(ctx: RunContext[AgentDependencies], query: str) -> list[str]:
    """Search the uploaded documents for relevant information according to the query."""

    print(f"[agent] local_search called with: {query}")

    return await ctx.deps.retriever.retrieve(query)
