# Phase 7 Line Review — Part I~II

기준일: 2026-10-02
대상:
- chapters/01/draft.md
- chapters/02/draft.md
- chapters/03/draft.md
- chapters/04/draft.md
- chapters/05/draft.md
- chapters/06/draft.md

## 결과

PASS.

Part I~II는 구조를 유지하면서 문장, 중복, 용어 경계를 정리했다.

## 주요 수정

### 1장
- SWE-agent의 ACI를 업계 표준명처럼 읽히지 않도록 표현 보정
- Framework / Architecture 설명 중복 압축
- 기능 수를 maturity로 보는 표현을 더 명확하게 부정

### 2장
- Handoff preview를 Part VII를 침범하지 않는 수준으로 압축
- State Machine 설명을 deterministic rule과 model judgment의 분리로 정리
- 불필요한 결론 signpost 제거

### 3장
- Brain / Hands / Session 비유 제거
- Harness / Runtime / Durable State의 실제 lifecycle 경계로 교체
- Session을 execution state 전체처럼 읽히게 할 수 있는 충돌 제거
- 예시 숫자를 일반 원칙으로 오해할 수 있는 문장 제거
- Harness component는 반복 failure와 eval evidence에서 추가한다는 원칙 강화

### 4장
- "More Context"를 절대 명제가 아니라 자동 개선이 아니라는 경고로 수정
- Conversation History ⊂ Execution State 식 제거
- Conversation History를 Context Source 중 하나로 재정의
- Context / State 중복 설명 압축

### 5장
- Generic Tool의 비용을 금전이 아닌 decision burden으로 명확화
- ACI가 SWE-agent의 용어임을 명시
- "Product Interface"를 더 정확한 "Agent-facing Interface"로 변경
- Tool granularity 양쪽의 trade-off 유지

### 6장
- MCP 2026-07-28 base specification의 stateless core를 최신 공식 문서로 재확인
- Tasks가 base core가 아니라 별도 extension이며 현재 Draft임을 본문에 명시
- Discovery/Authorization 설명 중복 통합
- 본문 중심과 거리가 있는 Capability Cache 절 제거
- MCP Server를 possible enforcement point로 한정

## 유지한 핵심 경계

~~~text
Model ≠ Agent
Framework ≠ Architecture
Harness ≠ Runtime
Context ≠ Durable State
Tool ≠ Raw API
Eligibility ≠ Authorization
MCP ≠ Harness
Protocol Session ≠ Agent Goal
MCP Task ≠ Product / Factory Task
~~~

## Line Review에서 발견한 구조적 문제

1건.

3장의 Brain / Hands / Session 비유가 7장의 State Taxonomy와 충돌할 수 있었다.

해결:
- 해당 비유 제거
- Harness / Runtime / Durable State 책임으로 직접 표현

## Freshness

MCP 관련 현재 확인:
- base protocol revision 2026-07-28: final
- TypeScript SDK v2: 2026-07-28 stable release line
- Tasks: separate extension, documentation status Draft

상세:
- review/freshness/mcp-2026-10-02.md

## 다음 대상

Part III 7~11장.

우선 검토:
- 7장 taxonomy와 8장 State Plane 중복
- 8장 synthesis 용어의 과도한 표준화 표현
- 9장 replay / retry / recovery 문장 정밀화
- 10장 Long-running의 예시 수치 제거/보정
- 11장 selective revalidation의 preprint 한계 표현
