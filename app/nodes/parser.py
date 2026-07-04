from __future__ import annotations

from app.io import write_json_artifact
from app.state import ResearchState, add_error, add_log


def _section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    capture = False
    collected: list[str] = []
    target = heading.lower()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip().lower()
            if capture:
                break
            capture = current == target
            continue
        if capture:
            collected.append(line)
    return "\n".join(collected).strip()


def _list_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def parse_markdown_result(markdown: str) -> dict:
    summary = _section(markdown, "Executive Summary")
    findings_text = _section(markdown, "Key Findings")
    sources_text = _section(markdown, "Sources")
    findings = _list_items(findings_text)
    sources = _list_items(sources_text)
    return {
        "title": next((line[2:].strip() for line in markdown.splitlines() if line.startswith("# ")), "Research Result"),
        "executive_summary": summary,
        "key_findings": findings,
        "sources": sources,
        "raw_length": len(markdown),
    }


def parser_node(state: ResearchState) -> ResearchState:
    raw_results = state.get("raw_results", [])
    if not raw_results:
        add_error(state, "parser", "raw_results is empty")
        return state
    parsed = parse_markdown_result(raw_results[-1])
    state["parsed_result"] = parsed
    write_json_artifact(state, "parsed_result.json", parsed)
    add_log(state, "parser", "raw result parsed", findings=len(parsed["key_findings"]), sources=len(parsed["sources"]))
    return state

