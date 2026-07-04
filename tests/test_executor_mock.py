from app.executors.mock_executor import MockResearchExecutor
from app.state import create_initial_state


def test_mock_executor_returns_markdown():
    state = create_initial_state("LangGraph MAS Workflow")
    result = MockResearchExecutor().run("prompt", state)

    assert result.startswith("# Mock Research Result")
    assert "## Executive Summary" in result
    assert "## Key Findings" in result
    assert "## Sources" in result

