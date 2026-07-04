# AGENTS.md

## 기본 응답 원칙

- 한글로 답변한다.
- 오버엔지니어링을 피한다.
- 초중급자도 이해할 수 있게 핵심 이유를 쉽게 설명한다.
- 답변은 간결하게 한다.
- 추가 제안은 필요할 때 마지막에 1~2개만 한다.

## 문서 품질 게이트

문서를 새로 만들거나 수정할 때는 아래 5개 기준을 확인한다.

| 기준 | 의미 | 통과 기준 |
| --- | --- | --- |
| 완정성 | 필요한 내용이 빠짐없이 들어갔는가 | 4.5 / 5 이상 |
| 명확성 | 초중급자도 오해 없이 이해 가능한가 | 4.5 / 5 이상 |
| 추적성 | 도메인, 요구사항, 설계, 테스트, 구현 계획이 연결되는가 | 4.5 / 5 이상 |
| 검증가능성 | 통과/실패를 판단할 수 있는 기준이 있는가 | 4.5 / 5 이상 |
| 유지보수성 | 나중에 수정할 위치와 영향 범위가 분명한가 | 4.5 / 5 이상 |

문서별 점수가 4.5 미만이면 해당 문서를 먼저 보완한다.

## 프로젝트 목표

Perplexity Research Agent MAS Workflow MVP를 만든다.

사용자는 주제를 입력하고, 시스템은 다음 흐름으로 리서치 결과를 만든다.

```text
주제 입력
→ 리서치 계획 생성
→ CLI에서 approve / revise / stop 선택
→ 승인된 경우에만 Executor 실행
→ 결과 파싱
→ 평가
→ 필요 시 개선 루프 최대 3회
→ quick_summary_report.md 생성
→ report.html 생성
```

## 가장 중요한 구현 원칙

- 처음에는 반드시 `mock` 모드로 만든다.
- `mock` 모드 테스트가 통과하기 전까지 실제 Perplexity 호출을 붙이지 않는다.
- LangGraph 흐름과 Executor 구현을 분리한다.
- `perplexity` 모드는 Executor만 교체한다.
- Plan 승인 전에는 Executor를 절대 실행하지 않는다.
- 평가 기준은 85점으로 고정한다.
- 개선 루프는 최대 3회까지만 허용한다.
- API Key는 로그, 보고서, 테스트 출력에 노출하지 않는다.

## 문서 읽는 순서

1. `docs/01-domain-def.md`
2. `docs/02-prd.md`
3. `docs/03-architecture.md`
4. `docs/04-tdd-plan.md`
5. `docs/05-test-scenarios.md`
6. `docs/06-implementation-roadmap.md`
7. `docs/07-further-work.md`
8. `docs/08-implementation-todo.md`

## 문서 E2E 추적 규칙

- `01-domain-def.md`는 문제, 사용자, MVP 범위, 성공 기준을 정의한다.
- `02-prd.md`는 도메인 성공 기준을 기능/비기능 요구사항 ID로 바꾼다.
- `03-architecture.md`는 PRD 요구사항을 컴포넌트, 상태, 산출물로 연결한다.
- `04-tdd-plan.md`는 요구사항별 테스트 작성 순서를 정한다.
- `05-test-scenarios.md`는 실제 Given/When/Then 검증 조건을 정의한다.
- `06-implementation-roadmap.md`는 테스트를 통과시키는 구현 순서를 정한다.
- `07-further-work.md`는 MVP에서 제외한 기능과 재검토 조건을 관리한다.
- `08-implementation-todo.md`는 실제 구현 작업을 1차 MVP와 2차 확장 TODO로 쪼갠다.

새 요구사항이 생기면 PRD, 아키텍처, 테스트, 로드맵의 연결 여부를 같이 확인한다.

## 개발 진행 순서

1. 프로젝트 기본 구조를 만든다.
2. `ResearchState`를 정의한다.
3. `ResearchExecutor` Protocol을 정의한다.
4. `MockResearchExecutor`를 만든다.
5. LangGraph 노드를 연결한다.
6. CLI Plan 승인 게이트를 만든다.
7. Parser, Evaluator, Critic, Improver를 만든다.
8. Markdown 보고서와 HTML 보고서를 만든다.
9. pytest로 mock mode 전체 흐름을 검증한다.
10. 마지막에 `PerplexityResearchExecutor`를 추가한다.
11. README를 작성한다.

## TDD 작업 방식

각 기능은 아래 순서로 진행한다.

```text
실패하는 테스트 작성
→ 최소 코드 구현
→ 테스트 통과 확인
→ 필요한 만큼만 정리
```

처음부터 완벽한 구조를 만들려고 하지 않는다. 테스트가 요구하는 만큼만 구현한다.

## MVP 산출물

실행 결과로 아래 파일이 프로젝트 폴더 안에 생성되어야 한다.

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

## 보류할 기능

아래 기능은 MVP에 넣지 않고 문서에만 남긴다.

- Perplexity Web UI 자동화
- 웹 대시보드
- Obsidian 저장
- Slack 알림
- 예약 실행
- 멀티 사용자 기능

## 플러그인 사용 원칙

- 로컬 Markdown 문서와 코드 수정은 기본 파일 도구로 처리한다.
- GitHub 이슈, PR, CI 확인이 필요할 때만 GitHub 플러그인을 사용한다.
- Google Docs, Sheets, Slides로 옮겨야 할 때만 Google Drive 계열 플러그인을 사용한다.
- HTML 결과를 실제 화면으로 확인해야 하는 구현 단계에서는 브라우저 검증 플러그인을 사용할 수 있다.
- 플러그인은 문제 해결에 직접 필요할 때만 사용한다.

## AGENTS.md 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | 응답 원칙, 구현 원칙, 문서 규칙, 플러그인 기준을 포함한다. |
| 명확성 | 4.7 | 초중급자가 따라갈 수 있도록 짧은 문장과 표로 정리했다. |
| 추적성 | 4.6 | 문서 읽는 순서와 E2E 연결 규칙을 명시했다. |
| 검증가능성 | 4.6 | 문서 품질 점수 기준과 MVP 완료 기준을 제시했다. |
| 유지보수성 | 4.7 | 새 요구사항 발생 시 어느 문서를 함께 수정할지 기준이 있다. |
