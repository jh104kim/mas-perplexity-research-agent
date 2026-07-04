from __future__ import annotations

from app.executors.base import ResearchExecutor
from app.state import ResearchState


class MockResearchExecutor(ResearchExecutor):
    def run(self, prompt: str, state: ResearchState) -> str:
        topic = state.get("topic", "Unknown Topic")
        if state.get("force_low_quality"):
            return f"""# Mock Research Result

## Executive Summary
Short note about {topic}.

## Key Findings
- Limited finding

## Sources
- https://example.com/limited
"""

        improvement_note = ""
        if state.get("improvement_count", 0) > 0:
            improvement_note = "\n- Improved coverage based on critic feedback"

        return f"""# Mock Research Result

## Executive Summary
This is a mock research result for workflow validation about {topic}.

## Key Findings
- Finding 1: LangGraph can organize a research workflow as explicit nodes.
- Finding 2: A HITL step keeps Perplexity usage under user control.
- Finding 3: Evaluation should check source coverage, structure, and actionability.{improvement_note}

## Sources
- https://example.com/source-1
- https://example.com/source-2
- https://example.com/source-3
"""

