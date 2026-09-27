import os

import pytest

from app.agents.research_agent import research_agent


@pytest.mark.integration
def test_research_agent():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY is not set")

    result = research_agent.run_sync("Who is the attendee of the meeting?")

    print(result.output)

    assert result.output
    assert len(result.output) > 0
