# 02. PRD

## 제품명

Perplexity Research Agent MAS Workflow MVP

## 문서 역할

이 문서는 `01-domain-def.md`의 성공 기준을 구현 가능한 요구사항으로 바꾼다. 모든 기능 요구사항은 이후 아키텍처, 테스트, 로드맵에서 추적되어야 한다.

## 목적

LangGraph 기반 리서치 Agent Workflow를 학습하고, 개인 위키에 쌓을 수 있는 리서치 보고서를 자동 생성한다.

## 배경

처음부터 Perplexity API를 연결하면 비용과 디버깅 부담이 커진다. 따라서 MVP는 `mock` 모드로 전체 흐름을 먼저 검증하고, 실제 Perplexity 리서치는 `hitl` 모드로 처리한다. `hitl` 모드는 리서치 프롬프트를 생성하고, 사용자가 Perplexity에서 직접 실행한 결과 Markdown 파일을 읽어 후속 파이프라인을 진행한다.

## 사용자 시나리오

1. 사용자가 CLI에 리서치 주제를 입력한다.
2. 시스템이 리서치 계획을 만든다.
3. 사용자는 계획을 보고 `approve`, `revise`, `stop` 중 하나를 선택한다.
4. `approve`이면 리서치 프롬프트가 생성된다.
5. `mock` 모드에서는 Mock 결과를 사용한다.
6. `hitl` 모드에서는 사용자가 Perplexity에 프롬프트를 직접 넣고 결과를 Markdown 파일로 가져온다.
7. 시스템은 사용자 제공 Markdown 파일을 읽어 파싱하고 평가한다.
8. 85점 미만이면 최대 3회까지 개선 프롬프트를 만든다. `hitl` 모드에서는 사용자가 개선 프롬프트로 Perplexity를 다시 실행하고 새 Markdown 결과를 가져온다.
9. 최종 Markdown 보고서와 HTML 보고서를 저장한다.

## 기능 요구사항

| ID | 요구사항 | 우선순위 |
| --- | --- | --- |
| FR-01 | CLI에서 topic을 입력받는다. | Must |
| FR-02 | 실행 모드는 `mock`, `hitl`을 지원한다. | Must |
| FR-03 | 기본 실행 모드는 `mock`이다. | Must |
| FR-04 | Plan 생성 후 사용자 승인을 받는다. | Must |
| FR-05 | `approve` 전에는 Executor를 실행하지 않는다. | Must |
| FR-06 | `revise` 입력 시 Plan을 다시 생성한다. | Must |
| FR-07 | `stop` 입력 시 정상 종료한다. | Must |
| FR-08 | Mock Executor는 고정된 Markdown 리서치 결과를 반환한다. | Must |
| FR-09 | Parser는 Markdown 결과를 구조화한다. | Must |
| FR-10 | Evaluator는 100점 기준 평가 결과를 만든다. | Must |
| FR-11 | 85점 미만이면 개선 루프를 실행한다. | Must |
| FR-12 | 개선 루프는 최대 3회만 실행한다. | Must |
| FR-13 | `quick_summary_report.md`를 생성한다. | Must |
| FR-14 | `report.html`을 생성한다. | Must |
| FR-15 | 실행 로그를 `run_log.json`에 저장한다. | Must |
| FR-16 | `hitl` 모드는 Perplexity 리서치용 프롬프트를 파일로 저장한다. | Must |
| FR-17 | `hitl` 모드는 사용자가 제공한 Markdown 결과 파일을 읽는다. | Must |

## 비기능 요구사항

| ID | 요구사항 |
| --- | --- |
| NFR-01 | 테스트는 pytest로 작성한다. |
| NFR-02 | 기본 Workflow는 API Key 없이 동작한다. |
| NFR-03 | 실패 시 어느 노드에서 실패했는지 기록한다. |
| NFR-04 | 구조는 작고 읽기 쉬워야 한다. |
| NFR-05 | 실제 Perplexity API를 호출하지 않는다. |

## 요구사항 추적 매트릭스

| 요구사항 | 도메인 기준 | 아키텍처 연결 | 테스트 연결 |
| --- | --- | --- | --- |
| FR-01 | D-01, DS-01 | CLI, intake node | `test_graph_flow.py` |
| FR-02 | D-02, DS-01 | mode 선택 정책 | `test_graph_flow.py` |
| FR-03 | D-02, DS-01 | 기본 mode 정책 | `test_graph_flow.py` |
| FR-04 | D-03, DS-02 | Plan Gate | `test_plan_gate.py` |
| FR-05 | D-03, DS-02 | Executor node 진입 조건 | `test_plan_gate.py` |
| FR-06 | D-03, DS-04 | planner node 재실행 | `test_plan_gate.py` |
| FR-07 | D-03, DS-03 | CLI 종료 분기 | `test_plan_gate.py` |
| FR-08 | D-02, DS-01 | `MockResearchExecutor` | `test_executor_mock.py` |
| FR-09 | D-01 | parser node | `test_parser.py` |
| FR-10 | D-04, DS-05 | evaluator node | `test_evaluator.py` |
| FR-11 | D-04, DS-05 | critic/improver loop | `test_improvement_loop.py` |
| FR-12 | D-04, DS-06 | loop guard | `test_improvement_loop.py` |
| FR-13 | D-05, DS-07 | result_builder node | `test_report_builder.py` |
| FR-14 | D-05, DS-07 | html_publisher node | `test_report_builder.py` |
| FR-15 | DS-01, DS-08 | run log writer | `test_graph_flow.py` |
| FR-16 | D-02, DS-09 | prompt export | `test_graph_flow.py` |
| FR-17 | D-02, DS-09 | manual result import | `test_graph_flow.py`, `test_parser.py` |
| NFR-01 | 전체 | tests 폴더 | 전체 pytest |
| NFR-02 | DS-08 | no-key workflow | `test_graph_flow.py` |
| NFR-03 | DS-01 | `run_log.json` | failure logging scenario |
| NFR-04 | 전체 | 작은 모듈 구조 | 코드 리뷰 |
| NFR-05 | D-02 | HITL policy | roadmap checklist |

## CLI 예시

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode mock
python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl
python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl --result-file raw_result_01.md
```

## 인수 조건

- AC-01: `pytest`가 통과한다.
- AC-02: `mock` 모드로 topic 1개를 실행하면 보고서가 생성된다.
- AC-03: 승인 전 Executor 미호출 테스트가 통과한다.
- AC-04: `stop` 시 Executor 미호출 테스트가 통과한다.
- AC-05: `revise` 시 Plan 재생성 테스트가 통과한다.
- AC-06: 개선 루프가 3회를 넘지 않는다.
- AC-07: `hitl` 모드는 Perplexity 프롬프트를 생성하고 결과 파일 입력을 안내한다.
- AC-08: `hitl` 모드는 사용자가 제공한 Markdown 결과 파일을 읽어 파싱/평가/보고서 생성을 진행한다.
- AC-09: 최종 확인 문구로 "문제 없음"을 남길 수 있다.

## 변경 관리 규칙

- 기능 요구사항을 추가하면 `03-architecture.md`, `04-tdd-plan.md`, `05-test-scenarios.md`, `06-implementation-roadmap.md`도 확인한다.
- MVP에서 제외할 기능은 요구사항에 넣지 않고 `07-further-work.md`로 보낸다.
- `Should` 요구사항은 `Must` 요구사항이 통과한 뒤에 구현한다.

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | 기능/비기능 요구사항, CLI 예시, 인수 조건을 포함한다. |
| 명확성 | 4.6 | 요구사항과 인수 조건을 짧은 문장으로 유지했다. |
| 추적성 | 4.8 | 도메인, 아키텍처, 테스트 연결표를 추가했다. |
| 검증가능성 | 4.8 | AC ID와 테스트 연결이 있어 통과 여부를 판단할 수 있다. |
| 유지보수성 | 4.6 | 변경 관리 규칙으로 연관 문서 수정 기준을 명시했다. |
