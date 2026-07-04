# 06. Implementation Roadmap

## 문서 역할

이 문서는 PRD, 아키텍처, TDD 계획을 실제 구현 순서로 바꾼다. 구현자는 이 문서를 체크리스트처럼 사용한다.

세부 작업 체크리스트는 `08-implementation-todo.md`에서 관리한다.

## 전체 전략

3단계로 나누어 구현한다.

```text
Phase 1: Mock Workflow Skeleton
Phase 2: Evaluation Loop
Phase 3: HITL Perplexity Result Import
```

## 단계별 추적 요약

| 단계 | 주요 요구사항 | 주요 테스트 | 산출물 |
| --- | --- | --- | --- |
| Phase 1 | FR-01~FR-10, FR-13~FR-15 | Plan Gate, Mock, Parser, Report, Graph | 기본 Workflow와 파일 산출물 |
| Phase 2 | FR-10~FR-12 | Evaluator, Improvement Loop | 평가/개선 루프 |
| Phase 3 | FR-02, FR-16, FR-17, NFR-02 | HITL mode, 결과 파일 입력 테스트 | Perplexity 프롬프트와 사용자 제공 Markdown 입력 |

Phase 1부터 Phase 3까지는 `08-implementation-todo.md`의 1차 MVP 구현 TODO에 해당한다. Further Work는 2차 확장 TODO에 해당한다.

## Phase 1. Mock Workflow Skeleton

목표:

- Perplexity 없이 전체 Workflow가 끝까지 도는지 확인한다.

구현 순서:

1. 프로젝트 구조 생성
2. `ResearchState` 정의
3. `ResearchExecutor` Protocol 정의
4. `MockResearchExecutor` 구현
5. Planner 노드 구현
6. CLI 승인 게이트 구현
7. Executor 노드 구현
8. Parser 노드 구현
9. Evaluator 노드 구현
10. Report Builder 구현
11. HTML Publisher 구현
12. pytest 작성 및 통과

완료 기준:

- `pytest` 통과
- `mock` 모드 CLI 실행 성공
- 승인 전 Executor 미호출
- `stop` 시 Executor 미호출
- `revise` 시 Plan 재생성
- `quick_summary_report.md` 생성
- `report.html` 생성

완료 후 확인할 문서:

- `03-architecture.md`의 컴포넌트 책임과 실제 파일이 맞는지 확인한다.
- `05-test-scenarios.md`의 TC-GATE, TC-EXEC, TC-REPORT가 테스트로 구현됐는지 확인한다.

## Phase 2. Evaluation Loop

목표:

- 85점 미만일 때 Critic, Improver, Executor 재실행이 정상 동작하는지 확인한다.

구현 순서:

1. 낮은 품질 결과를 반환하는 Mock 옵션 추가
2. Evaluator가 85점 미만을 반환하는 테스트 작성
3. Critic 노드 구현
4. Improver 노드 구현
5. 개선 루프 조건 연결
6. 최대 3회 제한 테스트 작성
7. 3회 후에도 미달인 경우 보고서에 한계 포함

완료 기준:

- 85점 이상이면 종료
- 85점 미만이면 개선 루프 실행
- 3회 초과 반복 없음
- 실패 한계가 보고서에 표시됨

완료 후 확인할 문서:

- `04-tdd-plan.md`의 TDD-07, TDD-08이 통과하는지 확인한다.
- `05-test-scenarios.md`의 TC-EVAL, TC-LOOP가 테스트로 구현됐는지 확인한다.

## Phase 3. HITL Perplexity Result Import

목표:

- 검증된 Workflow에 Perplexity 리서치 프롬프트 생성과 사용자 제공 Markdown 결과 파일 입력을 추가한다.

구현 순서:

1. `hitl` mode 선택 로직 추가
2. Perplexity 리서치 프롬프트를 `research_prompt.md`로 저장
3. 사용자에게 Perplexity 직접 실행 안내 메시지 출력
4. `result_file` 또는 기본 `raw_result_01.md` 파일 읽기
5. 결과 파일이 없을 때 사용자 입력 필요 상태 기록
6. mock mode 회귀 테스트 실행
7. hitl mode fixture 파일 기반 E2E 검증

완료 기준:

- `research_prompt.md` 생성
- 사용자가 가져온 `raw_result_01.md` 읽기
- API Key 없이 동작
- 결과 파일이 없으면 어느 단계에서 대기/실패했는지 `run_log.json`에 기록됨
- Parser 이후 Graph 구조는 mock mode와 동일함

완료 후 확인할 문서:

- `02-prd.md`의 FR-16, FR-17, NFR-02가 만족되는지 확인한다.
- `07-further-work.md`로 보류한 API 직접 호출, Web UI 자동화와 혼동하지 않는다.

## 최종 확인 체크리스트

- [ ] `pytest` 통과
- [ ] mock mode에서 topic 1개 실행 성공
- [ ] approve 전 Executor 미호출 확인
- [ ] stop 시 Executor 미호출 확인
- [ ] revise 시 Plan 재생성 확인
- [ ] improvement loop 3회 초과 없음 확인
- [ ] `quick_summary_report.md` 생성 확인
- [ ] `report.html` 생성 확인
- [ ] hitl mode에서 Perplexity 프롬프트 생성 확인
- [ ] hitl mode에서 사용자 제공 Markdown 결과 파일 입력 확인
- [ ] API Key 없이 동작 확인
- [ ] 문제가 없으면 "문제 없음" 명시

## 구현 중 문서 업데이트 규칙

- 새 파일이 추가되면 `03-architecture.md`의 폴더 구조와 컴포넌트 책임을 확인한다.
- 새 테스트가 추가되면 `04-tdd-plan.md`와 `05-test-scenarios.md`의 매핑을 확인한다.
- MVP 제외 기능을 구현하고 싶어지면 먼저 `02-prd.md`에서 요구사항 승격 여부를 판단한다.

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | 3개 Phase, 완료 기준, 최종 체크리스트를 포함한다. |
| 명확성 | 4.7 | 구현 순서를 단계별로 단순하게 정리했다. |
| 추적성 | 4.8 | Phase별 요구사항, 테스트, 산출물을 연결했다. |
| 검증가능성 | 4.7 | 각 Phase 완료 기준과 최종 체크리스트가 있다. |
| 유지보수성 | 4.7 | 구현 중 문서 업데이트 규칙을 추가했다. |
