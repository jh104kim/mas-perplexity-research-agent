# 05. Test Scenarios

## 문서 역할

이 문서는 TDD 계획을 실제 테스트 시나리오로 바꾼다. 각 시나리오는 Given/When/Then 형태로 작성하고, 나중에 pytest 테스트명으로 옮길 수 있어야 한다.

## 테스트 파일 계획

| 파일 | 목적 |
| --- | --- |
| `tests/test_graph_flow.py` | 전체 Workflow가 mock mode에서 끝까지 도는지 확인 |
| `tests/test_plan_gate.py` | approve / revise / stop 동작 확인 |
| `tests/test_executor_mock.py` | Mock Executor 동작 확인 |
| `tests/test_parser.py` | Markdown 결과 파싱 확인 |
| `tests/test_evaluator.py` | 평가 점수 계산과 pass/fail 확인 |
| `tests/test_improvement_loop.py` | 개선 루프 최대 3회 제한 확인 |
| `tests/test_report_builder.py` | Markdown, HTML 보고서 생성 확인 |

보안 시나리오는 새 파일을 늘리지 않고 `test_graph_flow.py`와 `test_report_builder.py` 안에서 검증한다.

## 시나리오 ID 규칙

| 접두어 | 의미 |
| --- | --- |
| TC-GATE | Plan 승인 게이트 |
| TC-EXEC | Mock 실행과 HITL 결과 입력 |
| TC-EVAL | 평가 |
| TC-LOOP | 개선 루프 |
| TC-REPORT | 보고서와 산출물 |
| TC-SEC | 보안 |

## Plan Gate 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-GATE-01 | Plan이 생성됨 | 사용자가 `approve` 입력 | Executor 실행 가능 상태가 된다. | FR-04, FR-05 |
| TC-GATE-02 | Plan이 생성됨 | 사용자가 `stop` 입력 | Executor 미실행, 정상 종료 | FR-07 |
| TC-GATE-03 | Plan이 생성됨 | 사용자가 `revise` 입력 | Plan 재생성 | FR-06 |
| TC-GATE-04 | Plan이 생성됨 | 잘못된 입력 | 다시 입력 요청 | FR-04 |

## Executor 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-EXEC-01 | mode가 `mock` | Executor 실행 | Mock Markdown 반환 | FR-08 |
| TC-EXEC-02 | mode가 `hitl` | Plan 승인 | Perplexity 리서치 프롬프트 생성 | FR-16 |
| TC-EXEC-03 | mode가 `hitl` | Markdown 결과 파일 전달 | 파일 내용을 `raw_results`로 읽음 | FR-17 |
| TC-EXEC-04 | Plan 미승인 | Workflow 진행 | 프롬프트 생성과 결과 파일 읽기 미실행 | FR-05 |

## Evaluator 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-EVAL-01 | 결과 품질이 충분함 | 평가 실행 | 85점 이상 | FR-10 |
| TC-EVAL-02 | 결과 품질이 낮음 | 평가 실행 | 85점 미만 | FR-10 |
| TC-EVAL-03 | 85점 이상 | Workflow 진행 | 개선 루프 없음 | FR-11 |
| TC-EVAL-04 | 85점 미만 | Workflow 진행 | Critic, Improver 실행 | FR-11 |

## Improvement Loop 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-LOOP-01 | 점수 85점 미만 | 개선 횟수 0회 | 재실행 | FR-11, FR-12 |
| TC-LOOP-02 | 점수 85점 미만 | 개선 횟수 2회 | 재실행 | FR-11, FR-12 |
| TC-LOOP-03 | 점수 85점 미만 | 개선 횟수 3회 | 더 이상 재실행하지 않음 | FR-12 |
| TC-LOOP-04 | 3회 후에도 미달 | 보고서 생성 | 한계와 개선 필요점을 포함 | FR-12, FR-13 |

## Report 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-REPORT-01 | parsed_result 존재 | Report Builder 실행 | `quick_summary_report.md` 생성 | FR-13 |
| TC-REPORT-02 | quick summary 존재 | HTML Publisher 실행 | `report.html` 생성 | FR-14 |
| TC-REPORT-03 | 노드 실패 발생 | 로그 저장 | `run_log.json`에 실패 노드 기록 | FR-15, NFR-03 |

## 보안 시나리오

| ID | Given | When | Then | 연결 요구사항 |
| --- | --- | --- | --- | --- |
| TC-SEC-01 | API Key가 없어도 됨 | mock/hitl 실행 | Key 없이 Workflow 진행 | NFR-02 |
| TC-SEC-02 | hitl 결과 파일이 없음 | Workflow 진행 | 사용자 입력 필요 상태 기록 | NFR-03 |
| TC-SEC-03 | 보고서 생성 | 내용 확인 | 환경변수 값이 보고서에 노출되지 않음 | NFR-02 |

## 테스트명 예시

```text
test_plan_gate_does_not_call_executor_before_approve
test_stop_exits_without_executor_call
test_revise_regenerates_plan
test_hitl_mode_exports_perplexity_prompt
test_hitl_mode_reads_user_result_markdown
test_improvement_loop_stops_after_three_attempts
test_report_builder_writes_markdown_and_html
```

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | Gate, Executor, 평가, 루프, 보고서, 보안 시나리오를 포함한다. |
| 명확성 | 4.7 | 모든 시나리오를 Given/When/Then으로 맞췄다. |
| 추적성 | 4.8 | 각 시나리오가 FR/NFR 요구사항과 연결된다. |
| 검증가능성 | 4.8 | TC ID와 테스트명 예시가 있어 pytest로 옮기기 쉽다. |
| 유지보수성 | 4.6 | 접두어 규칙으로 시나리오 추가 위치가 명확하다. |
