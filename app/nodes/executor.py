from __future__ import annotations

from app.executors.mock_executor import MockResearchExecutor
from app.io import write_text_artifact
from app.state import ResearchState, add_log


def mock_executor_node(state: ResearchState) -> ResearchState:
    executor = MockResearchExecutor()
    raw = executor.run(state.get("research_prompt", ""), state)
    state.setdefault("raw_results", []).append(raw)
    index = len(state["raw_results"])
    write_text_artifact(state, f"raw_result_{index:02}.md", raw)
    add_log(state, "mock_executor", "mock research result generated", attempt=index)
    return state

