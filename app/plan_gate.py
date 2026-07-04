from __future__ import annotations

from app.io import write_yaml_artifact
from app.nodes.planner import planner_node, revise_plan
from app.nodes.run_logger import run_logger_node
from app.state import PlanStatus, ResearchState, add_log


VALID_DECISIONS = {"approve", "revise", "stop"}


def apply_plan_decision(state: ResearchState, decision: str) -> ResearchState:
    normalized = decision.strip().lower()
    if normalized not in VALID_DECISIONS:
        raise ValueError("Plan decision must be one of: approve, revise, stop")

    state["plan_status"] = normalized  # type: ignore[typeddict-item]
    if normalized == "approve":
        write_yaml_artifact(state, "approved_plan.yaml", state.get("research_plan", {}))
        state["status"] = "approved"
        add_log(state, "plan_gate", "plan approved")
        return state
    if normalized == "revise":
        add_log(state, "plan_gate", "plan revision requested")
        return revise_plan(state)

    state["status"] = "stopped"
    add_log(state, "plan_gate", "workflow stopped before research")
    run_logger_node(state)
    return state


def run_plan_gate_with_decisions(state: ResearchState, decisions: list[str]) -> ResearchState:
    if not state.get("research_plan"):
        planner_node(state)

    for decision in decisions:
        apply_plan_decision(state, decision)
        if state.get("plan_status") in {"approve", "stop"}:
            return state

    raise ValueError("Plan gate decisions ended before approve or stop")

