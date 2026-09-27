from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic_ai import (
    Agent,
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    ThinkingPartDelta,
)

from app.agents.dependencies import AgentDependencies
from app.agents.research_agent import research_agent
from app.models.schema import ResearchRequest

router = APIRouter()


@router.post("/api/research")
async def research(
    body: ResearchRequest,
    request: Request,
) -> StreamingResponse:

    agent_deps = AgentDependencies(retriever=request.app.state.retriever)

    async def generate_response():
        async with research_agent.iter(
            body.request,
            deps=agent_deps,
        ) as run:
            async for node in run:
                # NOTE: streaming generated with AI with reference:
                # https://pydantic.dev/docs/ai/core-concepts/agent/#streaming-all-events-and-output

                # Model activity
                if Agent.is_model_request_node(node):
                    async with node.stream(run.ctx) as stream:
                        thinking_started = False
                        final_result_started = False

                        async for event in stream:
                            # Thinking delta
                            if isinstance(event, PartDeltaEvent):
                                if isinstance(
                                    event.delta,
                                    ThinkingPartDelta,
                                ):
                                    if not thinking_started:
                                        yield "\n[Thinking] "
                                        thinking_started = True

                                    yield event.delta.content_delta

                            # Final answer starts
                            elif isinstance(event, FinalResultEvent):
                                final_result_started = True
                                break

                        # Final answer delta
                        if final_result_started:
                            yield "\n\n[Answer] "

                            async for text in stream.stream_text(delta=True):
                                yield text

                # Tool activity
                elif Agent.is_call_tools_node(node):
                    async with node.stream(run.ctx) as stream:
                        async for event in stream:
                            if isinstance(
                                event,
                                FunctionToolCallEvent,
                            ):
                                yield (f"\n\n[Tool] Calling {event.part.tool_name}...\n")

                            elif isinstance(
                                event,
                                FunctionToolResultEvent,
                            ):
                                yield (f"[Tool] {event.part.tool_name} completed.")

    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
    )
