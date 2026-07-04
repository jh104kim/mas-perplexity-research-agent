from __future__ import annotations

from app.io import write_text_artifact
from app.state import ResearchState, add_log


def critic_node(state: ResearchState) -> ResearchState:
    report = state.get("evaluation_report", {})
    missing = report.get("missing", [])
    notes = [
        "# Critic Notes",
        "",
        f"- Current score: {state.get('evaluation_score', 0)}",
        f"- Pass score: {report.get('pass_score', 85)}",
    ]
    if missing:
        notes.append(f"- Missing or weak sections: {', '.join(missing)}")
    else:
        notes.append("- Improve depth, source quality, and actionability.")

    state["critic_notes"] = "\n".join(notes) + "\n"
    write_text_artifact(state, "critic_notes.md", state["critic_notes"])
    add_log(state, "critic", "critic notes generated")
    return state

