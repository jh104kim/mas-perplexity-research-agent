from __future__ import annotations

from typing import Protocol

from app.state import ResearchState


class ResearchExecutor(Protocol):
    def run(self, prompt: str, state: ResearchState) -> str:
        ...

