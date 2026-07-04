# 08. Implementation TODO

## 문서 역할

이 문서는 구현 작업을 체크리스트로 쪼갠다. `06-implementation-roadmap.md`가 큰 순서라면, 이 문서는 실제로 하나씩 처리할 작업 목록이다.

## 기준

- 1차 MVP는 `mock` 모드로 전체 Workflow를 완성하는 범위다.
- 2차 확장은 실제 Perplexity 연결과 MVP 이후 기능이다.
- 사용자가 말한 `MPV`는 문서에서는 일반적인 표현인 `MVP`로 정리한다.
- 각 항목은 테스트 가능해야 한다.

## 1차 MVP 구현 TODO

| ID | TODO | 구현 방법 | 완료 기준 |
| --- | --- | --- | --- |
| MVP-01 | Python 프로젝트 골격 생성 | `pyproject.toml`, `app/`, `tests/`를 만든다. 필요한 의존성은 최소로 시작한다. | `python -m pytest` 명령을 실행할 수 있다. |
| MVP-02 | `ResearchState` 정의 | `app/state.py`에 topic, mode, plan, result, score, errors 등 상태 필드를 정의한다. | 상태 객체를 테스트에서 생성할 수 있다. |
| MVP-03 | Executor Protocol 정의 | `app/executors/base.py`에 `ResearchExecutor` Protocol을 만든다. | Mock/Perplexity Executor가 같은 인터페이스를 따른다. |
| MVP-04 | Mock Executor 구현 | `app/executors/mock_executor.py`에서 고정 Markdown 결과를 반환한다. | `test_executor_mock.py` 통과 |
| MVP-05 | Planner 노드 구현 | topic을 받아 간단한 리서치 계획을 만든다. | `research_plan.yaml` 생성 가능 |
| MVP-06 | CLI Plan Gate 구현 | `approve`, `revise`, `stop` 입력만 허용한다. | approve 전 Executor 미호출, stop 미호출, revise 재생성 테스트 통과 |
| MVP-07 | Prompt Builder 구현 | 승인된 Plan을 Executor용 프롬프트로 변환한다. | `research_prompt.md` 생성 가능 |
| MVP-08 | LangGraph 기본 흐름 연결 | planner, prompt_builder, executor, parser, evaluator, report 노드를 연결한다. | mock mode 전체 흐름 테스트 통과 |
| MVP-09 | Parser 구현 | raw Markdown에서 summary, findings, sources를 구조화한다. | `parsed_result.json` 생성 가능 |
| MVP-10 | Evaluator 구현 | 100점 기준으로 결과를 평가하고 85점 통과 여부를 판단한다. | `evaluation_report.yaml` 생성 가능 |
| MVP-11 | Critic/Improver 구현 | 85점 미만이면 피드백과 개선 프롬프트를 만든다. | 개선 루프 진입 테스트 통과 |
| MVP-12 | 개선 루프 최대 3회 제한 | `improvement_count`로 반복 횟수를 제어한다. | 3회 초과 반복 없음 |
| MVP-13 | Quick Report 생성 | 최종 결과를 `quick_summary_report.md`로 저장한다. | Markdown 보고서 생성 테스트 통과 |
| MVP-14 | HTML Publisher 구현 | Markdown 보고서를 단순 HTML로 변환해 `report.html`로 저장한다. | HTML 보고서 생성 테스트 통과 |
| MVP-15 | Run Log 저장 | 실행 단계, 에러, 산출물 경로를 `run_log.json`에 기록한다. | 실패 노드 기록 테스트 통과 |
| MVP-16 | README 작성 | 설치, mock 실행, 테스트 방법을 짧게 정리한다. | 새 사용자가 mock 실행 가능 |
| MVP-17 | 1차 E2E 검증 | `pytest`와 mock CLI 실행을 수행한다. | 문서 기준으로 "문제 없음" 판단 가능 |

## 1차 MVP 테스트 TODO

| ID | 테스트 파일 | 검증 내용 |
| --- | --- | --- |
| TEST-01 | `tests/test_plan_gate.py` | approve / revise / stop 동작 |
| TEST-02 | `tests/test_executor_mock.py` | Mock Executor Markdown 반환 |
| TEST-03 | `tests/test_parser.py` | raw result 구조화 |
| TEST-04 | `tests/test_evaluator.py` | 85점 기준 평가 |
| TEST-05 | `tests/test_improvement_loop.py` | 개선 루프 최대 3회 |
| TEST-06 | `tests/test_report_builder.py` | Markdown/HTML 보고서 생성 |
| TEST-07 | `tests/test_graph_flow.py` | mock mode 전체 Workflow |

## 2차 확장 TODO

| ID | TODO | 구현 방법 | 완료 기준 |
| --- | --- | --- | --- |
| EXT-01 | Perplexity Executor 추가 | `app/executors/perplexity_executor.py`에서 실제 API/MCP 호출을 구현한다. | mode가 `perplexity`일 때 실제 Executor 선택 |
| EXT-02 | API Key 로딩 | `.env` 또는 환경변수에서 Key를 읽는다. | Key 없을 때 명확한 에러 |
| EXT-03 | API Key 마스킹 | 로그, 보고서, 에러 메시지에 Key 원문이 남지 않게 한다. | 보안 테스트 통과 |
| EXT-04 | Perplexity mode 수동 검증 | 실제 topic 1개로 API 호출을 확인한다. | `raw_result_01.md` 저장 |
| EXT-05 | 보고서 품질 개선 | 출처 품질, 한계점, 다음 질문 섹션을 강화한다. | 보고서 템플릿 테스트 통과 |
| EXT-06 | 날짜별 출력 폴더 | 실행마다 별도 폴더에 산출물을 저장한다. | 이전 실행 결과가 덮어써지지 않음 |
| EXT-07 | Obsidian 저장 검토 | 안정된 Markdown을 Vault로 복사하는 옵션을 검토한다. | `07-further-work.md` 승격 기준 충족 |
| EXT-08 | 웹 대시보드 검토 | 실행 이력이 많아졌을 때만 도입을 검토한다. | CLI 한계가 명확할 때 PRD 업데이트 |
| EXT-09 | Slack 알림 검토 | 자동 실행이나 팀 공유가 필요할 때만 검토한다. | 외부 연동 테스트 계획 수립 |

## 구현 순서 추천

1. MVP-01부터 MVP-04까지 만들고 가장 작은 테스트를 통과시킨다.
2. MVP-05부터 MVP-08까지 만들어 mock Workflow를 연결한다.
3. MVP-09부터 MVP-14까지 만들어 결과물을 저장한다.
4. MVP-10부터 MVP-12까지 평가와 개선 루프를 보강한다.
5. MVP-15부터 MVP-17까지 로그, README, E2E 검증을 마무리한다.
6. 1차 MVP가 안정되면 EXT-01부터 2차 확장을 시작한다.

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | 1차 MVP, 테스트, 2차 확장 작업을 모두 포함한다. |
| 명확성 | 4.8 | 각 TODO에 구현 방법과 완료 기준을 붙였다. |
| 추적성 | 4.6 | 로드맵과 테스트 문서의 구현 단위로 연결된다. |
| 검증가능성 | 4.8 | 각 항목이 테스트나 산출물 기준으로 완료 판단 가능하다. |
| 유지보수성 | 4.7 | MVP/EXT ID로 이후 작업 상태를 관리할 수 있다. |
