from __future__ import annotations

from pathlib import Path

from app.executors.base import ResearchExecutor
from app.state import ResearchState


class ManualResearchExecutor(ResearchExecutor):
    def run(self, prompt: str, state: ResearchState) -> str:
        result_file = state.get("result_file")
        if not result_file:
            raise FileNotFoundError("HITL mode requires --result-file or raw_result_01.md")

        path = Path(result_file)
        if not path.exists():
            raise FileNotFoundError(f"HITL result file not found: {path}")
        return path.read_text(encoding="utf-8")

