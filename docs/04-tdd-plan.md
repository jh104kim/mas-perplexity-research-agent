# 04. TDD Plan

## TDD 목표

작은 테스트를 먼저 만들고, 테스트를 통과시키는 만큼만 구현한다.

이 프로젝트에서 가장 중요한 검증 대상은 다음 4가지다.

1. Plan 승인 전 Executor가 실행되지 않는가
2. Workflow가 mock mode에서 끝까지 도는가
3. 평가 점수에 따라 개선 루프가 정확히 동작하는가
4. 최종 산출물이 생성되는가

## 문서 역할

이 문서는 PRD 요구사항을 테스트 작성 순서로 바꾼다. 구현자는 이 문서를 보고 어떤 테스트부터 작성할지 결정한다.

## 기본 사이클

```text
Red: 실패하는 테스트 작성
Green: 최소 구현으로 통과
Refactor: 중복과 이름만 정리
```

## Phase 1. Mock Workflow Skeleton

목표는 Perplexity 없이 전체 흐름이 끝까지 도는 것이다.

먼저 작성할 테스트:

- `test_executor_mock.py`
- `test_plan_gate.py`
- `test_parser.py`
- `test_evaluator.py`
- `test_report_builder.py`
- `test_graph_flow.py`

검증할 내용:

- Mock Executor가 Markdown 문자열을 반환한다.
- `approve` 전에는 Executor가 실행되지 않는다.
- `stop`이면 Executor가 실행되지 않는다.
- `revise`이면 Plan이 다시 생성된다.
- `quick_summary_report.md`가 생성된다.
- `report.html`이 생성된다.

## Phase 2. Evaluation Loop

목표는 85점 미만일 때 개선 루프가 정상 동작하는지 확인하는 것이다.

먼저 작성할 테스트:

- `test_improvement_loop.py`
- `test_evaluator.py`

검증할 내용:

- 85점 이상이면 루프 없이 종료한다.
- 85점 미만이면 Critic, Improver를 거쳐 Executor를 다시 실행한다.
- 개선 횟수는 최대 3회다.
- 3회 후에도 미달이면 한계가 포함된 보고서를 만든다.

## Phase 3. Perplexity Executor

목표는 검증된 Workflow 뒤에 실제 Executor만 붙이는 것이다.

먼저 작성할 테스트:

- mode가 `perplexity`이면 `PerplexityResearchExecutor`가 선택된다.
- Graph 구조는 mock mode와 동일하다.
- API Key가 없는 경우 명확한 에러를 낸다.
- API Key는 로그와 보고서에 남지 않는다.

## 테스트 우선순위

1. Plan Gate 테스트
2. Mock Executor 테스트
3. Parser 테스트
4. Evaluator 테스트
5. Improvement Loop 테스트
6. Report Builder 테스트
7. Graph 전체 흐름 테스트
8. Perplexity Executor 선택 테스트

## 요구사항별 테스트 매핑

| 테스트 ID | 요구사항 | 테스트 파일 | 핵심 검증 |
| --- | --- | --- | --- |
| TDD-01 | FR-01, FR-02, FR-03 | `test_graph_flow.py` | topic과 mode로 Workflow 시작 |
| TDD-02 | FR-04, FR-05 | `test_plan_gate.py` | approve 전 Executor 미호출 |
| TDD-03 | FR-06 | `test_plan_gate.py` | revise 시 Plan 재생성 |
| TDD-04 | FR-07 | `test_plan_gate.py` | stop 시 정상 종료 |
| TDD-05 | FR-08 | `test_executor_mock.py` | Mock Markdown 반환 |
| TDD-06 | FR-09 | `test_parser.py` | raw result 구조화 |
| TDD-07 | FR-10 | `test_evaluator.py` | 100점 기준 평가 |
| TDD-08 | FR-11, FR-12 | `test_improvement_loop.py` | 85점 미만 루프, 최대 3회 |
| TDD-09 | FR-13, FR-14 | `test_report_builder.py` | Markdown/HTML 보고서 생성 |
| TDD-10 | FR-15, NFR-03 | `test_graph_flow.py` | `run_log.json` 생성과 실패 노드 기록 |
| TDD-11 | FR-16, NFR-02 | `test_graph_flow.py`, `test_report_builder.py` | Executor 교체와 API Key 미노출 |

## 테스트 작성 원칙

- 한 테스트는 하나의 핵심 행동만 검증한다.
- 실제 Perplexity API 호출은 기본 단위 테스트에서 하지 않는다.
- 파일 생성 테스트는 임시 디렉터리를 사용한다.
- Plan Gate 테스트에서는 Mock Executor 호출 횟수를 확인한다.
- 개선 루프 테스트에서는 의도적으로 낮은 점수를 반환하는 Mock을 사용한다.

## 완료 기준

아래 항목이 모두 만족되면 MVP TDD는 완료로 본다.

- 모든 pytest 통과
- mock mode CLI 실행 성공
- 승인 전 Executor 미호출 확인
- 개선 루프 3회 제한 확인
- Markdown 보고서 생성 확인
- HTML 보고서 생성 확인
- API Key 노출 방지 확인

## TDD 단계별 완료 판정

| 단계 | 완료 판정 |
| --- | --- |
| Phase 1 | Plan Gate, Mock Executor, Parser, Report 테스트가 통과한다. |
| Phase 2 | Evaluator와 Improvement Loop 테스트가 통과한다. |
| Phase 3 | Perplexity Executor 선택과 API Key 미노출 테스트가 통과한다. |

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | TDD 목표, 단계, 우선순위, 요구사항별 테스트를 포함한다. |
| 명확성 | 4.7 | 테스트 작성 원칙을 짧게 분리했다. |
| 추적성 | 4.8 | PRD 요구사항과 테스트 파일을 TDD ID로 연결했다. |
| 검증가능성 | 4.8 | 단계별 완료 판정이 있어 통과 여부를 판단할 수 있다. |
| 유지보수성 | 4.6 | 요구사항이 바뀌면 매핑표와 단계 판정만 갱신하면 된다. |
