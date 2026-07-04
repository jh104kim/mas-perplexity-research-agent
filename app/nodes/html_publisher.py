from __future__ import annotations

from app.io import markdown_to_html, write_text_artifact
from app.state import ResearchState, add_log


def html_publisher_node(state: ResearchState) -> ResearchState:
    html = markdown_to_html(state.get("quick_summary_report", ""), title="Research Report")
    state["html_report"] = html
    write_text_artifact(state, "report.html", html)
    add_log(state, "html_publisher", "html report generated")
    return state

