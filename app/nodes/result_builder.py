from __future__ import annotations

from app.io import write_text_artifact
from app.state import ResearchState, add_log


def build_quick_report(state: ResearchState) -> str:
    parsed = state.get("parsed_result", {})
    findings = parsed.get("key_findings", [])
    sources = parsed.get("sources", [])
    plan_questions = state.get("research_plan", {}).get("questions", [])
    limitations: list[str] = []
    if state.get("evaluation_score", 0) < 85:
        limitations.append("평가 기준 85점에 도달하지 못해 추가 리서치가 필요하다.")
    if state.get("improvement_count", 0) >= 3 and state.get("evaluation_score", 0) < 85:
        limitations.append("개선 루프 최대 3회에 도달했다.")
    if state.get("awaiting_hitl"):
        limitations.append("HITL 결과 Markdown 파일 입력이 필요하다.")

    finding_block = "\n".join(f"- {item}" for item in findings) or "- 핵심 발견 없음"
    source_block = "\n".join(f"- {item}" for item in sources) or "- 출처 없음"
    limitation_block = "\n".join(f"- {item}" for item in limitations) or "- 특별한 한계 없음"
    next_question_block = "\n".join(f"- {item}" for item in plan_questions[:3]) or "- 후속 질문 없음"

    return f"""# Quick Summary Report

## Topic
{state.get("topic", "")}

## Executive Summary
{parsed.get("executive_summary", "") or "요약 없음"}

## Key Findings
{finding_block}

## Evaluation
- Score: {state.get("evaluation_score", 0)}
- Improvement Count: {state.get("improvement_count", 0)}

## Sources
{source_block}

## Source Summary
- Source Count: {len(sources)}
- Finding Count: {len(findings)}

## Limitations
{limitation_block}

## Next Questions
{next_question_block}
"""


def result_builder_node(state: ResearchState) -> ResearchState:
    report = build_quick_report(state)
    state["quick_summary_report"] = report
    write_text_artifact(state, "quick_summary_report.md", report)
    add_log(state, "result_builder", "quick summary report generated")
    return state
