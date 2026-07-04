# 진행log.md

## 2026-07-04 18:02:41 +09:00

### 요청

현재 Markdown 파일에 문제가 없다면 전체 구현 계획을 다시 점검하고, TODO의 Phase별 진행 방안에 대해 TDD, E2E, 다음 단계 Threshold, 최대 3회 개선 루프를 포함한 완료 계획을 정리한다. 사용자 확인이 필요한 사항은 `확인필요.md`, 진행 내역은 `진행log.md`에 저장한다.

### 수행 내용

- 현재 Markdown 파일 목록 확인
- 미완성 표현과 4.5 미만 품질 점수 검색
- Git 상태 확인
- `docs/08-implementation-todo.md`에 Phase별 진행 게이트 추가
- `docs/08-implementation-todo.md`에 TDD/E2E/Threshold 기준 추가
- `docs/08-implementation-todo.md`에 최대 3회 개선 루프 운영 방식 추가
- `docs/08-implementation-todo.md`에 1차 MVP/2차 확장 최종 완료 기준 추가
- `확인필요.md` 생성

### 점검 결과

| 항목 | 결과 |
| --- | --- |
| Markdown 파일 존재 여부 | 정상 |
| 문서 자체 평가 4.5 미만 | 없음 |
| 미완성 placeholder | 없음 |
| 문서 간 큰 충돌 | 없음 |
| 즉시 사용자 확인 필요 | 없음 |
| 추가 플러그인 필요 | 없음 |

### 발견한 참고 사항

- `TODO`는 미완성 표시가 아니라 구현 체크리스트 문서 제목과 항목명으로 사용 중이다.
- 현재 작업은 문서 계획 보강이므로 pytest 실행 대상은 아직 없다.
- 다음 구현 단계는 `docs/08-implementation-todo.md`의 `MVP-01`부터 시작하면 된다.

### 다음 단계

1. `MVP-01~MVP-04` 범위로 Python 프로젝트 골격과 Mock Executor 테스트를 만든다.
2. 해당 범위의 TDD를 먼저 통과시킨다.
3. Gate `G1` 기준을 통과하면 Plan Gate와 Mock Workflow Skeleton으로 넘어간다.

## 2026-07-04 API Key 사전 점검

### 요청

Perplexity API Key, OpenAI API Key 등 구현 전에 필요한 항목이 있는지 미리 확인한다.

### 수행 내용

- 프로젝트 문서에서 API Key 관련 요구사항 검색
- 로컬 환경변수 존재 여부만 확인
- Perplexity 공식 문서 기준 환경변수명 확인
- OpenAI 공식 문서 기준 환경변수명 확인
- `확인필요.md`에 API Key 사전 점검 결과 반영

### 결과

| 항목 | 상태 | 판단 |
| --- | --- | --- |
| `PERPLEXITY_API_KEY` | missing | 당시에는 2차 Perplexity 연결 전 필요로 판단했으나, 이후 HITL 전환으로 현재 기준 불필요 |
| `PPLX_API_KEY` | missing | 현재 공식 문서 기준 기본 변수명으로 사용하지 않음 |
| `OPENAI_API_KEY` | missing | 현재 기획에는 필수 아님, OpenAI 모델 확장 시 필요 |

### 결론

1차 MVP는 Mock Executor 기반이라 API Key 없이 진행 가능하다고 판단했다. 이후 HITL Perplexity Workflow 전환으로 실제 Perplexity API 호출은 보류되었고, 현재 기준 `PERPLEXITY_API_KEY`는 필요하지 않다.

## 2026-07-04 HITL Perplexity Workflow 전환

### 요청

Perplexity 리서치는 API로 직접 호출하지 않고, 시스템이 리서치 진행 프롬프트를 만들면 사용자가 Perplexity에서 직접 실행한 뒤 결과 Markdown 파일을 가져오는 방식으로 전체 Workflow를 수정한다.

### 수행 내용

- `perplexity` API/Executor 전제를 `hitl` 모드로 변경
- Perplexity API 직접 호출을 MVP 제외 및 Further Work 항목으로 이동
- `ManualResearchExecutor` 또는 `hitl_result_loader`가 사용자 제공 Markdown 파일을 읽는 구조로 변경
- CLI 예시를 `--mode hitl --result-file raw_result_01.md` 기준으로 변경
- TDD/E2E 기준을 실제 API 호출 테스트가 아닌 fixture Markdown 파일 입력 테스트로 변경
- `확인필요.md`에서 Perplexity API Key를 현재 불필요 항목으로 변경

### 변경 후 기준

| 항목 | 변경 전 | 변경 후 |
| --- | --- | --- |
| 실제 Perplexity 연결 | API Executor | HITL 수동 실행 |
| 실행 모드 | `mock`, `perplexity` | `mock`, `hitl` |
| 결과 획득 | API 응답 | 사용자가 가져온 Markdown 파일 |
| API Key | 2차 확장부터 필요 | 현재 기준 불필요 |
| 테스트 방식 | API Key/Executor 선택 검증 | 프롬프트 생성과 Markdown fixture 입력 검증 |

### 결론

1차 MVP는 API Key 없이 `mock`과 `hitl` 모드까지 구현한다. Perplexity API 직접 호출은 반복 작업 부담이 명확해질 때만 별도 PRD 승격 후 검토한다.

## 2026-07-04 18:23:41 +09:00 MVP 구현 및 검증

### 요청

이전에 정리한 빌드 진행 방안을 반영해 phase별로 진행하고, 마무리까지 구현한다.

### 구현 내용

- Python 프로젝트 골격 생성: `pyproject.toml`, `app/`, `tests/`
- `ResearchState` 정의
- `ResearchExecutor` Protocol 정의
- `MockResearchExecutor` 구현
- HITL 결과 파일 입력용 `ManualResearchExecutor`와 `hitl_result_loader` 구현
- Planner, Prompt Builder, Parser, Evaluator, Critic, Improver 구현
- LangGraph 기반 mock/hitl Workflow 연결
- CLI Plan Gate 구현: `approve`, `revise`, `stop`
- Markdown/HTML 보고서 생성
- `run_log.json` 저장
- README 작성
- 프롬프트 템플릿 파일 추가

### 검증 결과

| 항목 | 결과 |
| --- | --- |
| `python -m pytest` | 12 passed |
| mock CLI E2E | 통과 |
| hitl CLI E2E | 통과 |
| approve 전 Executor 미호출 | 테스트 통과 |
| stop 시 Executor 미호출 | 테스트 통과 |
| revise 시 Plan 재생성 | 테스트 통과 |
| improvement loop 최대 3회 | 테스트 통과 |
| Markdown/HTML 보고서 생성 | 테스트 통과 |
| API Key 필요 여부 | 현재 기준 불필요 |

### E2E 명령

```bash
python -m pytest
```

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode mock
```

```bash
python -m app.cli --topic "LangGraph MAS Workflow" --mode hitl --result-file tests/fixtures/hitl_result.md
```

### 참고

- CLI E2E는 임시 출력 폴더에서 수행했다.
- `pip install -e ".[dev]"` 과정에서 생성된 `*.egg-info/`는 `.gitignore`에 추가하고 제거했다.
