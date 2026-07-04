# MAS Perplexity Research Agent

HITL 기반 Perplexity Research Agent MVP입니다.

## 목표

```text
주제 입력
→ 리서치 계획 생성
→ CLI 승인
→ Perplexity용 프롬프트 생성
→ mock 또는 HITL 결과 입력
→ 파싱
→ 평가
→ 개선 루프 최대 3회
→ Markdown/HTML 보고서 생성
```

## 설치

```bash
python -m pip install -e ".[dev]"
```

## 테스트

```bash
python -m pytest
```

## Mock 실행

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode mock
```

자동 승인으로 실행하려면:

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode mock --auto-approve
```

## HITL 실행

먼저 프롬프트를 생성한다.

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl
```

생성된 `research_prompt.md`를 Perplexity에 직접 입력한 뒤 결과를 Markdown 파일로 저장한다. 그다음 결과 파일을 지정해서 실행한다.

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl --result-file raw_result_01.md
```

## 주요 산출물

- `research_plan.yaml`
- `approved_plan.yaml`
- `research_prompt.md`
- `raw_result_01.md`
- `parsed_result.json`
- `evaluation_report.yaml`
- `critic_notes.md`
- `quick_summary_report.md`
- `report.html`
- `run_log.json`

## 현재 정책

- Perplexity API 직접 호출은 하지 않는다.
- API Key 없이 `mock`, `hitl` 모드가 동작한다.
- Perplexity API 직접 호출은 Further Work로 보류한다.

