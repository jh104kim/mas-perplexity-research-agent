from __future__ import annotations

from pathlib import Path

from app.io import artifact_path, write_text_artifact
from app.state import ResearchState, add_error, add_log


def resolve_result_file(state: ResearchState) -> Path:
    raw_count = len(state.get("raw_results", []))
    result_files = state.get("result_files") or []
    if raw_count < len(result_files):
        return Path(result_files[raw_count])
    if state.get("result_file"):
        return Path(state["result_file"])
    return artifact_path(state, f"raw_result_{raw_count + 1:02}.md")


def hitl_result_loader_node(state: ResearchState) -> ResearchState:
    result_path = resolve_result_file(state)
    if not result_path.exists():
        state["awaiting_hitl"] = True
        state["status"] = "awaiting_hitl_result"
        write_text_artifact(
            state,
            "hitl_instructions.md",
            f"""# HITL Instructions

1. Open `research_prompt.md`.
2. Paste the prompt into Perplexity manually.
3. Save the Perplexity Markdown result to `{result_path}`.
4. Re-run the CLI with `--mode hitl --result-file "{result_path}"`.

No API key is required for this workflow.
""",
        )
        add_error(state, "hitl_result_loader", f"HITL result file not found: {result_path}")
        return state

    raw = result_path.read_text(encoding="utf-8")
    state.setdefault("raw_results", []).append(raw)
    state["awaiting_hitl"] = False
    index = len(state["raw_results"])
    write_text_artifact(state, f"raw_result_{index:02}.md", raw)
    add_log(state, "hitl_result_loader", "HITL result markdown loaded", path=str(result_path), attempt=index)
    return state
