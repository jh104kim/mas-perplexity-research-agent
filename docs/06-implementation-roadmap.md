# 06. Implementation Roadmap

## 문서 역할

이 문서는 PRD, 아키텍처, TDD 계획을 실제 구현 순서로 바꾼다. 구현자는 이 문서를 체크리스트처럼 사용한다.

세부 작업 체크리스트는 `08-implementation-todo.md`에서 관리한다.

## 전체 전략

3단계로 나누어 구현한다.

```text
Phase 1: Mock Workflow Skeleton
Phase 2: Evaluation Loop
Phase 3: Perplexity Executor 연결
```

## 단계별 추적 요약

| 단계 | 주요 요구사항 | 주요 테스트 | 산출물 |
| --- | --- | --- | --- |
| Phase 1 | FR-01~FR-10, FR-13~FR-15 | Plan Gate, Mock, Parser, Report, Graph | 기본 Workflow와 파일 산출물 |
| Phase 2 | FR-10~FR-12 | Evaluator, Improvement Loop | 평가/개선 루프 |
| Phase 3 | FR-02, FR-16, NFR-02 | Executor mode, 보안 테스트 | Perplexity Executor |

Phase 1과 Phase 2는 `08-implementation-todo.md`의 1차 MVP 구현 TODO에 해당한다. Phase 3과 Further Work는 2차 확장 TODO에 해당한다.

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

## Phase 3. Perplexity Executor 연결

목표:

- 검증된 Workflow에 실제 Perplexity 호출부만 추가한다.

구현 순서:

1. `PerplexityResearchExecutor` 추가
2. `.env`에서 API Key 로드
3. mode 선택 로직 추가
4. API 호출 실패 처리 추가
5. API Key 마스킹 테스트 추가
6. mock mode 회귀 테스트 실행
7. perplexity mode 수동 실행 검증

완료 기준:

- API 호출 성공
- `raw_result_01.md` 저장
- API Key 로그 미노출
- API Key 보고서 미노출
- 실패 노드가 `run_log.json`에 기록됨
- Graph 구조 변경 없이 Executor만 교체됨

완료 후 확인할 문서:

- `02-prd.md`의 FR-16, NFR-02가 만족되는지 확인한다.
- `07-further-work.md`로 보류한 Web UI 자동화와 혼동하지 않는다.

## 최종 확인 체크리스트

- [ ] `pytest` 통과
- [ ] mock mode에서 topic 1개 실행 성공
- [ ] approve 전 Executor 미호출 확인
- [ ] stop 시 Executor 미호출 확인
- [ ] revise 시 Plan 재생성 확인
- [ ] improvement loop 3회 초과 없음 확인
- [ ] `quick_summary_report.md` 생성 확인
- [ ] `report.html` 생성 확인
- [ ] perplexity mode에서 Executor만 교체 확인
- [ ] API Key 노출 없음 확인
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
