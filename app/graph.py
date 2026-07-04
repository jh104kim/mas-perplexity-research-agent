from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langgraph.graph import END, StateGraph

from app.nodes.critic import critic_node
from app.nodes.evaluator import PASS_SCORE, evaluator_node
from app.nodes.executor import mock_executor_node
from app.nodes.hitl_result_loader import hitl_result_loader_node
from app.nodes.html_publisher import html_publisher_node
from app.nodes.improver import improver_node
from app.nodes.parser import parser_node
from app.nodes.planner import planner_node
from app.nodes.prompt_builder import prompt_builder_node
from app.nodes.result_builder import result_builder_node
from app.nodes.run_logger import run_logger_node
from app.plan_gate import run_plan_gate_with_decisions
from app.state import ExecutorMode, ResearchState, add_log, create_initial_state


def _route_mode(state: ResearchState) -> str:
    return "hitl_result_loader" if state.get("executor_mode") == "hitl" else "mock_executor"


def _route_after_source(state: ResearchState) -> str:
    if state.get("awaiting_hitl"):
        return "result_builder"
    return "parser"


def _route_after_evaluation(state: ResearchState) -> str:
    max_improvements = int(state.get("max_improvements", 3))  # type: ignore[arg-type]
    if state.get("evaluation_score", 0) >= PASS_SCORE:
        return "result_builder"
    if state.get("improvement_count", 0) >= max_improvements:
        return "result_builder"
    return "critic"


def build_research_graph():
    graph = StateGraph(ResearchState)
    graph.add_node("prompt_builder", prompt_builder_node)
    graph.add_node("mock_executor", mock_executor_node)
    graph.add_node("hitl_result_loader", hitl_result_loader_node)
    graph.add_node("parser", parser_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("critic", critic_node)
    graph.add_node("improver", improver_node)
    graph.add_node("result_builder", result_builder_node)
    graph.add_node("html_publisher", html_publisher_node)
    graph.add_node("run_logger", run_logger_node)

    graph.set_entry_point("prompt_builder")
    graph.add_conditional_edges(
        "prompt_builder",
        _route_mode,
        {
            "mock_executor": "mock_executor",
            "hitl_result_loader": "hitl_result_loader",
        },
    )
    graph.add_conditional_edges(
        "mock_executor",
        _route_after_source,
        {
            "parser": "parser",
            "result_builder": "result_builder",
        },
    )
    graph.add_conditional_edges(
        "hitl_result_loader",
        _route_after_source,
        {
            "parser": "parser",
            "result_builder": "result_builder",
        },
    )
    graph.add_edge("parser", "evaluator")
    graph.add_conditional_edges(
        "evaluator",
        _route_after_evaluation,
        {
            "critic": "critic",
            "result_builder": "result_builder",
        },
    )
    graph.add_edge("critic", "improver")
    graph.add_edge("improver", "prompt_builder")
    graph.add_edge("result_builder", "html_publisher")
    graph.add_edge("html_publisher", "run_logger")
    graph.add_edge("run_logger", END)
    return graph.compile()


def run_approved_state(state: ResearchState) -> ResearchState:
    if state.get("plan_status") != "approve":
        add_log(state, "graph", "research graph skipped because plan is not approved")
        run_logger_node(state)
        return state

    app = build_research_graph()
    result = app.invoke(state)
    result["status"] = result.get("status") or "completed"
    if not result.get("awaiting_hitl"):
        result["status"] = "completed"
    run_logger_node(result)
    return result


def run_research(
    topic: str,
    *,
    mode: ExecutorMode = "mock",
    output_dir: str | Path = ".",
    result_file: str | None = None,
    result_files: Iterable[str] | None = None,
    plan_decisions: list[str] | None = None,
    score_sequence: list[int] | None = None,
    force_low_quality: bool = False,
) -> ResearchState:
    state = create_initial_state(topic, mode=mode, output_dir=output_dir, result_file=result_file)
    if result_files:
        state["result_files"] = list(result_files)
    if score_sequence:
        state["score_sequence"] = score_sequence
    if force_low_quality:
        state["force_low_quality"] = True

    decisions = plan_decisions or ["approve"]
    planner_node(state)
    run_plan_gate_with_decisions(state, decisions)
    if state.get("plan_status") != "approve":
        return state
    return run_approved_state(state)

