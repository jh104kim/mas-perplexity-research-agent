from __future__ import annotations

from app.io import write_yaml_artifact
from app.state import ResearchState, add_log


PASS_SCORE = 85


def evaluate_parsed_result(parsed: dict, state: ResearchState | None = None) -> dict:
    if state and state.get("score_sequence"):
        index = len(state.get("evaluation_history", []))
        sequence = state["score_sequence"]
        score = sequence[min(index, len(sequence) - 1)]
    else:
        score = 40
        if parsed.get("executive_summary"):
            score += 20
        score += min(len(parsed.get("key_findings", [])) * 10, 25)
        score += min(len(parsed.get("sources", [])) * 5, 15)
        score = min(score, 100)

    missing: list[str] = []
    if not parsed.get("executive_summary"):
        missing.append("executive_summary")
    if len(parsed.get("key_findings", [])) < 2:
        missing.append("key_findings")
    if len(parsed.get("sources", [])) < 2:
        missing.append("sources")

    return {
        "score": score,
        "pass_score": PASS_SCORE,
        "passed": score >= PASS_SCORE,
        "missing": missing,
    }


def evaluator_node(state: ResearchState) -> ResearchState:
    report = evaluate_parsed_result(state.get("parsed_result", {}), state)
    state["evaluation_score"] = int(report["score"])
    state["evaluation_report"] = report
    state.setdefault("evaluation_history", []).append(state["evaluation_score"])
    write_yaml_artifact(state, "evaluation_report.yaml", report)
    add_log(state, "evaluator", "result evaluated", score=state["evaluation_score"], passed=report["passed"])
    return state

