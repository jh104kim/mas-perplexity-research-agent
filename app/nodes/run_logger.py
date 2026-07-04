from __future__ import annotations

from app.io import write_json_artifact
from app.state import ResearchState


def run_logger_node(state: ResearchState) -> ResearchState:
    write_json_artifact(
        state,
        "run_log.json",
        {
            "status": state.get("status", "completed"),
            "topic": state.get("topic"),
            "mode": state.get("executor_mode"),
            "evaluation_score": state.get("evaluation_score"),
            "improvement_count": state.get("improvement_count"),
            "errors": state.get("errors", []),
            "events": state.get("run_log", []),
        },
    )
    return state

