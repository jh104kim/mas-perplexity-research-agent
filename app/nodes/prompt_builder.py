from __future__ import annotations

from app.io import write_text_artifact
from app.state import ResearchState, add_log


def build_research_prompt(state: ResearchState) -> str:
    plan = state.get("research_plan", {})
    questions = plan.get("questions", [])
    question_block = "\n".join(f"{idx + 1}. {question}" for idx, question in enumerate(questions))
    improvement = state.get("improvement_prompt", "").strip()
    improvement_block = f"\n\n## 개선 요청\n{improvement}\n" if improvement else ""

    return f"""# Perplexity Research Prompt

너는 리서치 전문가다. 아래 주제에 대해 신뢰할 수 있는 출처를 바탕으로 한국어 Markdown 리서치 결과를 작성해줘.

## 주제
{state.get("topic", "")}

## 목적
{state.get("purpose", "개인 학습 및 위키 축적")}

## 조사 질문
{question_block}

## 출력 형식
- `# Research Result` 제목으로 시작
- `## Executive Summary`
- `## Key Findings`
- `## Sources`
- 가능하면 출처 URL 포함
- 과장하지 말고 한계나 불확실성도 적기
{improvement_block}
"""


def prompt_builder_node(state: ResearchState) -> ResearchState:
    state["research_prompt"] = build_research_prompt(state)
    write_text_artifact(state, "research_prompt.md", state["research_prompt"])
    add_log(state, "prompt_builder", "research prompt generated")
    return state

