# 01. Domain Definition

## 한 줄 정의

이 프로젝트는 사용자가 입력한 주제를 바탕으로 리서치 계획을 만들고, 승인 후 리서치 결과를 생성, 평가, 개선, 보고서화하는 CLI 기반 Research Agent Workflow이다.

## 문서 역할

이 문서는 프로젝트의 기준선을 정한다. 이후 문서는 이 기준을 더 자세한 요구사항, 설계, 테스트, 구현 계획으로 나눈다.

| 도메인 ID | 내용 | 연결 문서 |
| --- | --- | --- |
| D-01 | CLI 기반 리서치 Workflow | `02-prd.md`, `03-architecture.md` |
| D-02 | Mock 우선 및 HITL 리서치 전략 | `02-prd.md`, `04-tdd-plan.md` |
| D-03 | Plan 승인 게이트 | `02-prd.md`, `05-test-scenarios.md` |
| D-04 | Evaluation 및 개선 루프 | `02-prd.md`, `04-tdd-plan.md` |
| D-05 | Markdown/HTML 보고서 생성 | `03-architecture.md`, `06-implementation-roadmap.md` |
| D-06 | MVP 제외 기능 관리 | `07-further-work.md` |

## 해결하려는 문제

리서치 자동화는 바로 실제 API를 붙이면 비용, 실패 원인, 품질 문제를 한 번에 다루게 된다.

그래서 MVP에서는 먼저 `Mock Executor`로 전체 흐름을 검증한다. 실제 Perplexity 리서치는 API로 자동 호출하지 않고, 시스템이 만든 프롬프트를 사용자가 Perplexity에 직접 넣은 뒤 결과 Markdown 파일을 가져오는 HITL 방식으로 처리한다.

## 핵심 사용자

- 개인 학습자
- 리서치 내용을 위키나 노트로 축적하려는 사람
- LangGraph 기반 Agent Workflow를 학습하려는 개발자

## 핵심 용어

| 용어 | 의미 |
| --- | --- |
| ResearchState | 워크플로우 전체에서 공유되는 상태 값 |
| Plan | 리서치 전에 생성되는 조사 계획 |
| Plan Gate | 사용자가 CLI에서 `approve`, `revise`, `stop`을 선택하는 단계 |
| Executor | 실제 리서치를 실행하는 구성요소 |
| Mock Executor | API 없이 고정된 가짜 리서치 결과를 반환하는 Executor |
| HITL | Human-in-the-loop. 사람이 중간 단계에 참여하는 방식 |
| Manual Research Executor | 사용자가 가져온 Markdown 결과 파일을 읽는 Executor |
| Perplexity Prompt | 사용자가 Perplexity에 직접 입력할 리서치 프롬프트 |
| Evaluator | 리서치 결과를 100점 기준으로 평가하는 노드 |
| Critic | 낮은 점수의 원인을 피드백하는 노드 |
| Improver | Critic 피드백을 바탕으로 개선 프롬프트를 만드는 노드 |
| Quick Report | 최종 요약 Markdown 보고서 |
| HTML Publisher | Markdown 결과를 HTML 파일로 저장하는 노드 |

## MVP 범위

MVP에 포함한다.

- CLI topic 입력
- Plan 생성
- CLI 승인 게이트
- Mock Executor 실행
- Perplexity 리서치용 프롬프트 생성
- HITL 결과 파일 입력
- Parser 실행
- Evaluator 실행
- 85점 미만일 때 개선 루프
- 개선 루프 최대 3회 제한
- `quick_summary_report.md` 생성
- `report.html` 생성
- `run_log.json` 생성

MVP에서 제외한다.

- Perplexity API 직접 호출
- 웹 UI
- 대시보드
- Obsidian 자동 저장
- Slack 알림
- Perplexity Web UI 브라우저 자동화
- 복잡한 데이터베이스 저장

## MVP 경계 판단표

| 질문 | MVP 판단 |
| --- | --- |
| CLI 없이 웹 화면이 필요한가? | 아니다. CLI만 사용한다. |
| 실제 Perplexity API가 필요한가? | 아니다. HITL로 사용자가 직접 실행한다. |
| 보고서가 여러 형식이어야 하는가? | 아니다. Markdown 1개와 HTML 1개만 만든다. |
| 개선 루프가 무제한이어야 하는가? | 아니다. 최대 3회로 제한한다. |
| 외부 알림이나 DB 저장이 필요한가? | 아니다. MVP 이후로 미룬다. |

## 성공 기준

- DS-01: `mock` 모드에서 전체 흐름이 끝까지 실행된다.
- DS-02: 승인 전에는 Executor가 실행되지 않는다.
- DS-03: `stop`이면 Executor가 실행되지 않는다.
- DS-04: `revise`이면 Plan이 다시 생성된다.
- DS-05: 평가 점수가 85점 미만이면 개선 루프가 실행된다.
- DS-06: 개선 루프는 3회를 넘지 않는다.
- DS-07: 최종 보고서와 HTML 파일이 생성된다.
- DS-08: API Key 없이 1차 MVP와 HITL 리서치 흐름이 동작한다.
- DS-09: HITL 모드에서는 사용자가 제공한 Markdown 결과 파일을 읽어 후속 파이프라인을 실행한다.

## PRD 추적 링크

| 성공 기준 | 연결 요구사항 |
| --- | --- |
| DS-01 | FR-01, FR-02, FR-03, FR-08, FR-15 |
| DS-02 | FR-04, FR-05 |
| DS-03 | FR-07 |
| DS-04 | FR-06 |
| DS-05 | FR-10, FR-11 |
| DS-06 | FR-12 |
| DS-07 | FR-13, FR-14 |
| DS-08 | NFR-02, NFR-05 |
| DS-09 | FR-16, FR-17 |

## 문서 자체 평가

| 기준 | 점수 | 근거 |
| --- | --- | --- |
| 완정성 | 4.7 | 문제, 사용자, 용어, MVP 포함/제외, 성공 기준을 포함한다. |
| 명확성 | 4.8 | MVP 경계를 질문형 표로 정리해 오해를 줄였다. |
| 추적성 | 4.6 | 도메인 ID와 PRD 요구사항 연결표를 추가했다. |
| 검증가능성 | 4.6 | 성공 기준을 DS ID로 분리해 테스트 연결이 가능하다. |
| 유지보수성 | 4.7 | 기능 범위가 바뀌면 MVP 경계와 추적 링크를 수정하면 된다. |
