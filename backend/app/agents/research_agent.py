from pydantic_ai import Agent

from app.agents.dependencies import AgentDependencies
from app.config import config

SYSTEM_PROMPT = "You are a research agent."

research_agent = Agent(
    model=f"openrouter:{config.research_agent.model}",
    deps_type=AgentDependencies,
    instructions=SYSTEM_PROMPT,
)
