from pydantic_ai import Agent, RunContext
from pydantic_ai.common_tools.tavily import tavily_search_tool
from pydantic_ai.common_tools.web_fetch import web_fetch_tool

from app.agents.dependencies import AgentDependencies
from app.config import config, tavily_api_key

SYSTEM_PROMPT = "You are a research agent. "

research_agent = Agent(
    model=f"openrouter:{config.research_agent.model}",
    tools=[tavily_search_tool(tavily_api_key), web_fetch_tool()],
    deps_type=AgentDependencies,
    instructions=SYSTEM_PROMPT,
)


@research_agent.instructions
async def source_context(
    ctx: RunContext[AgentDependencies],
) -> str:
    sources = ctx.deps.retriever.list_sources()

    if not sources:
        return "No local source documents are currently available."

    return (
        "The user has uploaded the following source documents: "
        + ", ".join(sources)
        + ". Search these documents with local_search when relevant."
    )


@research_agent.tool
async def local_search(ctx: RunContext[AgentDependencies], query: str) -> list[str]:
    """Search the uploaded documents for relevant information according to the query."""

    print(f"[agent] local_search called with: {query}")

    return await ctx.deps.retriever.retrieve(query)
