from __future__ import annotations

from app.io import write_yaml_artifact
from app.state import ResearchState, add_log


def build_plan(state: ResearchState) -> dict:
    topic = state["topic"]
    revision = state.get("plan_revision_count", 0)
    return {
        "topic": topic,
        "purpose": state.get("purpose", "개인 학습 및 위키 축적"),
        "depth": state.get("depth", "standard"),
        "report_type": state.get("report_type", "quick_summary"),
        "revision": revision,
        "questions": [
            f"{topic}의 핵심 개념은 무엇인가?",
            f"{topic}의 현재 활용 방식과 장단점은 무엇인가?",
            f"{topic}을 실제 워크플로우에 적용할 때 주의할 점은 무엇인가?",
        ],
        "expected_sections": [
            "Executive Summary",
            "Key Findings",
            "Sources",
            "Limitations",
        ],
    }


def planner_node(state: ResearchState) -> ResearchState:
    state["research_plan"] = build_plan(state)
    state["status"] = "planned"
    write_yaml_artifact(state, "research_plan.yaml", state["research_plan"])
    add_log(state, "planner", "research plan generated", revision=state.get("plan_revision_count", 0))
    return state


def revise_plan(state: ResearchState) -> ResearchState:
    state["plan_revision_count"] = state.get("plan_revision_count", 0) + 1
    return planner_node(state)

