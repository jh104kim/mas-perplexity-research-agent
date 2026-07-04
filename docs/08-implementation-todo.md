# 08. Implementation TODO

## 문서 역할

이 문서는 구현 작업을 체크리스트로 쪼갠다. `06-implementation-roadmap.md`가 큰 순서라면, 이 문서는 실제로 하나씩 처리할 작업 목록이다.

## 기준

- 1차 MVP는 `mock` 모드와 `hitl` 모드로 전체 Workflow를 완성하는 범위다.
- 2차 확장은 보고서 품질, 저장 구조, 편의 기능 개선이다.
- 사용자가 말한 `MPV`는 문서에서는 일반적인 표현인 `MVP`로 정리한다.
- 각 항목은 테스트 가능해야 한다.

## 1차 MVP 구현 TODO

| ID | TODO | 구현 방법 | 완료 기준 |
| --- | --- | --- | --- |
| MVP-01 | Python 프로젝트 골격 생성 | `pyproject.toml`, `app/`, `tests/`를 만든다. 필요한 의존성은 최소로 시작한다. | `python -m pytest` 명령을 실행할 수 있다. |
| MVP-02 | `ResearchState` 정의 | `app/state.py`에 topic, mode, plan, result, score, errors 등 상태 필드를 정의한다. | 상태 객체를 테스트에서 생성할 수 있다. |
| MVP-03 | Executor Protocol 정의 | `app/executors/base.py`에 `ResearchExecutor` Protocol을 만든다. | Mock 결과와 HITL 결과가 같은 raw 결과 형식으로 처리된다. |
| MVP-04 | Mock Executor 구현 | `app/executors/mock_executor.py`에서 고정 Markdown 결과를 반환한다. | `test_executor_mock.py` 통과 |
| MVP-05 | Planner 노드 구현 | topic을 받아 간단한 리서치 계획을 만든다. | `research_plan.yaml` 생성 가능 |
| MVP-06 | CLI Plan Gate 구현 | `approve`, `revise`, `stop` 입력만 허용한다. | approve 전 Executor 미호출, stop 미호출, revise 재생성 테스트 통과 |
| MVP-07 | Prompt Builder 구현 | 승인된 Plan을 Perplexity 직접 실행용 프롬프트로 변환한다. | `research_prompt.md` 생성 가능 |
| MVP-08 | HITL 결과 파일 입력 구현 | `hitl` 모드에서 사용자가 가져온 Markdown 파일을 읽는다. | `raw_result_01.md` 또는 `--result-file` 입력 가능 |
| MVP-09 | LangGraph 기본 흐름 연결 | planner, prompt_builder, mock executor, hitl loader, parser, evaluator, report 노드를 연결한다. | mock/hitl mode 전체 흐름 테스트 통과 |
| MVP-10 | Parser 구현 | raw Markdown에서 summary, findings, sources를 구조화한다. | `parsed_result.json` 생성 가능 |
| MVP-11 | Evaluator 구현 | 100점 기준으로 결과를 평가하고 85점 통과 여부를 판단한다. | `evaluation_report.yaml` 생성 가능 |
| MVP-12 | Critic/Improver 구현 | 85점 미만이면 피드백과 개선 프롬프트를 만든다. HITL 모드에서는 사용자가 개선 프롬프트로 다시 직접 리서치한다. | 개선 루프 진입 테스트 통과 |
| MVP-13 | 개선 루프 최대 3회 제한 | `improvement_count`로 반복 횟수를 제어한다. | 3회 초과 반복 없음 |
| MVP-14 | Quick Report 생성 | 최종 결과를 `quick_summary_report.md`로 저장한다. | Markdown 보고서 생성 테스트 통과 |
| MVP-15 | HTML Publisher 구현 | Markdown 보고서를 단순 HTML로 변환해 `report.html`로 저장한다. | HTML 보고서 생성 테스트 통과 |
| MVP-16 | Run Log 저장 | 실행 단계, 에러, 산출물 경로를 `run_log.json`에 기록한다. | 실패 노드 기록 테스트 통과 |
| MVP-17 | README 작성 | 설치, mock 실행, hitl 실행, 테스트 방법을 짧게 정리한다. | 새 사용자가 mock/hitl 실행 가능 |
| MVP-18 | 1차 E2E 검증 | `pytest`, mock CLI 실행, hitl fixture 실행을 수행한다. | 문서 기준으로 "문제 없음" 판단 가능 |

## 1차 MVP 테스트 TODO

| ID | 테스트 파일 | 검증 내용 |
| --- | --- | --- |
| TEST-01 | `tests/test_plan_gate.py` | approve / revise / stop 동작 |
| TEST-02 | `tests/test_executor_mock.py` | Mock Executor Markdown 반환 |
| TEST-03 | `tests/test_parser.py` | raw result 구조화 |
| TEST-04 | `tests/test_evaluator.py` | 85점 기준 평가 |
| TEST-05 | `tests/test_improvement_loop.py` | 개선 루프 최대 3회 |
| TEST-06 | `tests/test_report_builder.py` | Markdown/HTML 보고서 생성 |
| TEST-07 | `tests/test_graph_flow.py` | mock/hitl mode 전체 Workflow |

## 2차 확장 TODO

| ID | TODO | 구현 방법 | 완료 기준 |
| --- | --- | --- | --- |
| EXT-01 | 보고서 품질 개선 | 출처 품질, 한계점, 다음 질문 섹션을 강화한다. | 보고서 템플릿 테스트 통과 |
| EXT-02 | 날짜별 출력 폴더 | 실행마다 별도 폴더에 산출물을 저장한다. | 이전 실행 결과가 덮어써지지 않음 |
| EXT-03 | HITL 사용성 개선 | 프롬프트 복사 안내, 결과 파일 경로 안내, 재시도 메시지를 개선한다. | 사용자가 다음 행동을 명확히 알 수 있음 |
| EXT-04 | Obsidian 저장 검토 | 안정된 Markdown을 Vault로 복사하는 옵션을 검토한다. | `07-further-work.md` 승격 기준 충족 |
| EXT-05 | 웹 대시보드 검토 | 실행 이력이 많아졌을 때만 도입을 검토한다. | CLI 한계가 명확할 때 PRD 업데이트 |
| EXT-06 | Slack 알림 검토 | 자동 실행이나 팀 공유가 필요할 때만 검토한다. | 외부 연동 테스트 계획 수립 |
| EXT-07 | Perplexity API 직접 호출 검토 | HITL 방식이 반복 작업에 비효율적일 때만 검토한다. | PRD 승격, 비용/보안 기준, 별도 테스트 계획 필요 |

## 구현 순서 추천

1. MVP-01부터 MVP-04까지 만들고 가장 작은 테스트를 통과시킨다.
2. MVP-05부터 MVP-09까지 만들어 mock/hitl Workflow를 연결한다.
3. MVP-10부터 MVP-15까지 만들어 파싱, 평가, 결과물을 저장한다.
4. MVP-11부터 MVP-13까지 평가와 개선 루프를 보강한다.
5. MVP-16부터 MVP-18까지 로그, README, E2E 검증을 마무리한다.
6. 1차 MVP가 안정되면 EXT-01부터 2차 확장을 시작한다.

## Phase별 진행 게이트

각 Phase는 TDD, E2E, Threshold를 모두 통과해야 다음 단계로 넘어간다.

| Gate | 범위 | TDD 기준 | E2E 기준 | 다음 단계 Threshold |
| --- | --- | --- | --- | --- |
| G0 | 문서/계획 점검 | 문서 자체 평가 전부 4.5 이상 | 문서 간 ID 연결 확인 | 미완성 표현 없음, 확인 필요 항목 정리 |
| G1 | MVP-01~MVP-04 | State, Executor Protocol, Mock Executor 테스트 통과 | Mock Executor 단독 실행 가능 | 핵심 인터페이스 변경 없이 다음 단계 진행 가능 |
| G2 | MVP-05~MVP-09 | Plan Gate, Prompt Builder, HITL Loader 테스트 통과 | approve/revise/stop 및 hitl fixture 흐름 검증 | 승인 전 프롬프트/결과 파일 읽기 미실행 보장 |
| G3 | MVP-10~MVP-13 | Parser, Evaluator, Improvement Loop 테스트 통과 | 낮은 품질 Mock 또는 HITL fixture로 개선 루프 검증 | 85점 기준, 최대 3회 제한 보장 |
| G4 | MVP-14~MVP-16 | Report, HTML, Run Log 테스트 통과 | mock/hitl 실행 후 산출물 전체 생성 | 필수 산출물 누락 없음 |
| G5 | MVP-17~MVP-18 | 전체 pytest 통과 | mock CLI와 hitl fixture topic 1개 완주 | 1차 MVP 완료, "문제 없음" 판단 가능 |
| G6 | EXT-01~EXT-03 | 확장별 테스트 추가 | 확장 기능별 E2E 검증 | 1차 MVP 회귀 없음 |
| G7 | EXT-05 이후 | 확장별 테스트 추가 | 확장 기능별 E2E 검증 | PRD 승격 기준 충족 |

## 개선 루프 운영 방식

Gate를 통과하지 못하면 최대 3회까지만 개선 루프를 돈다.

```text
실패 원인 기록
→ 가장 작은 수정
→ 관련 테스트 재실행
→ E2E 재확인
→ 통과하면 다음 Gate 진행
```

| 루프 | 할 일 | 종료 조건 |
| --- | --- | --- |
| 1회차 | 실패 원인을 좁히고 최소 수정한다. | 관련 테스트 통과 |
| 2회차 | 설계/문서 불일치를 확인하고 수정한다. | 테스트와 문서 기준 동시 충족 |
| 3회차 | 남은 실패를 정리하고 우회가 아닌 근본 수정만 한다. | Gate 통과 또는 확인 필요 항목 등록 |

3회 후에도 Gate를 통과하지 못하면 다음 단계로 넘어가지 않는다. 이때 원인, 영향 범위, 사용자 확인이 필요한 사항을 `확인필요.md`에 기록한다.

## 최종 완료 기준

1차 MVP 완료 기준:

- `python -m pytest` 전체 통과
- `python -m app.cli --topic "LangGraph MAS Workflow" --mode mock` 실행 성공
- `python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl --result-file raw_result_01.md` 실행 성공
- approve 전 Executor 미호출 확인
- stop 시 Executor 미호출 확인
- revise 시 Plan 재생성 확인
- improvement loop 3회 초과 없음
- `research_prompt.md`, `quick_summary_report.md`, `report.html`, `run_log.json` 생성
- README에 mock 실행법, hitl 실행법, 테스트법 작성

2차 확장 완료 기준:

- 1차 MVP 기준이 계속 통과
- HITL 사용성이 개선되어도 기존 mock/hitl 테스트가 통과
- API 직접 호출 기능은 PRD 승격 전에는 구현하지 않음
- Further Work 기능은 PRD 승격 후 별도 테스트가 생긴 경우에만 구현

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.8 | 1차 MVP, HITL, 테스트, 2차 확장, Gate, 개선 루프를 포함한다. |
| 명확성 | 4.8 | 각 TODO에 구현 방법, 완료 기준, 다음 단계 조건을 붙였다. |
| 추적성 | 4.7 | 로드맵, 테스트 문서, Gate 기준으로 구현 단위가 연결된다. |
| 검증가능성 | 4.9 | 각 Gate가 TDD/E2E/Threshold로 완료 판단 가능하다. |
| 유지보수성 | 4.7 | MVP/EXT ID로 이후 작업 상태를 관리할 수 있다. |
