from __future__ import annotations

from app.state import ResearchState, add_log


def improver_node(state: ResearchState) -> ResearchState:
    state["improvement_count"] = state.get("improvement_count", 0) + 1
    state["improvement_prompt"] = f"""이전 결과의 평가 점수는 {state.get("evaluation_score", 0)}점입니다.
아래 피드백을 반영해서 더 완성도 높은 리서치 결과를 다시 작성해줘.

{state.get("critic_notes", "")}
"""
    add_log(state, "improver", "improvement prompt generated", improvement_count=state["improvement_count"])
    return state

