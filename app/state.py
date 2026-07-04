from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, TypedDict


ExecutorMode = Literal["mock", "hitl"]
PlanStatus = Literal["pending", "approve", "revise", "stop"]


class ResearchState(TypedDict, total=False):
    topic: str
    purpose: str
    depth: str
    report_type: str
    executor_mode: ExecutorMode
    result_file: str
    result_files: list[str]
    research_plan: dict[str, Any]
    plan_status: PlanStatus
    research_prompt: str
    raw_results: list[str]
    parsed_result: dict[str, Any]
    evaluation_score: int
    evaluation_report: dict[str, Any]
    evaluation_history: list[int]
    critic_notes: str
    improvement_prompt: str
    improvement_count: int
    quick_summary_report: str
    html_report: str
    output_dir: str
    errors: list[dict[str, str]]
    run_log: list[dict[str, Any]]
    status: str
    awaiting_hitl: bool
    plan_revision_count: int
    score_sequence: list[int]
    force_low_quality: bool


def create_initial_state(
    topic: str,
    *,
    mode: ExecutorMode = "mock",
    output_dir: str | Path = ".",
    result_file: str | None = None,
    purpose: str = "개인 학습 및 위키 축적",
    depth: str = "standard",
    report_type: str = "quick_summary",
) -> ResearchState:
    state: ResearchState = {
        "topic": topic,
        "purpose": purpose,
        "depth": depth,
        "report_type": report_type,
        "executor_mode": mode,
        "research_plan": {},
        "plan_status": "pending",
        "research_prompt": "",
        "raw_results": [],
        "parsed_result": {},
        "evaluation_score": 0,
        "evaluation_report": {},
        "evaluation_history": [],
        "critic_notes": "",
        "improvement_prompt": "",
        "improvement_count": 0,
        "quick_summary_report": "",
        "html_report": "",
        "output_dir": str(output_dir),
        "errors": [],
        "run_log": [],
        "status": "created",
        "awaiting_hitl": False,
        "plan_revision_count": 0,
    }
    if result_file:
        state["result_file"] = str(result_file)
    return state


def get_output_dir(state: ResearchState) -> Path:
    output_dir = Path(state.get("output_dir") or ".")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def add_log(state: ResearchState, node: str, message: str, **extra: Any) -> None:
    state.setdefault("run_log", []).append({"node": node, "message": message, **extra})


def add_error(state: ResearchState, node: str, message: str) -> None:
    state.setdefault("errors", []).append({"node": node, "message": message})
    add_log(state, node, message, level="error")

