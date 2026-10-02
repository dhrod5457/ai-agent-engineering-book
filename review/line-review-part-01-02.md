# Line Review — Part I~II

기준일: 2026-10-02
대상:
- chapters/01/draft.md
- chapters/02/draft.md
- chapters/03/draft.md
- chapters/04/draft.md
- chapters/05/draft.md
- chapters/06/draft.md

## 상태

PASS.

Structural Review에서 지적된 책임 경계는 유지하면서 문장 밀도와 표현 일관성을 조정했다.

## 적용한 수정

### 1장
- "실제" 반복 일부 제거
- Agent Capability 설명에서 저자 선언형 문구를 줄이고 직접 정의로 전환
- 최소 Agent 설명을 더 압축
- 결론 문장에서 중복 강조 제거

### 2장
- production / Production 혼용을 "운영" 표현으로 정리
- Production Loop → 운영 Loop
- production 수준 → 운영 수준
- 의미가 바뀌지 않는 범위에서 제품/마케팅식 영어 표현 축소

### 3장
- "실제 Failure" 같은 불필요한 수식 축소
- 초기 production Agent → 초기 운영 Agent
- Harness 정의와 21장 Ablation 예고의 책임 경계 유지

### 4장
- Production Agent → 운영 Agent
- "실제로" 같은 불필요한 강조 축소
- Context와 Durable State 설명은 유지하되 Part III 구현 상세는 침범하지 않음

### 5장
- Generic Tool vs bounded Tool 비교에 반대편 trade-off 추가
- Tool을 지나치게 세분화할 때 호출 수·조합 비용이 증가한다는 점 보강
- Tool Surface의 폭 자체가 trade-off임을 명확화

### 6장
- "MCP Server = Trust Boundary"로 단정될 수 있는 표현 수정
- MCP Server를 여러 enforcement point 중 하나가 될 수 있는 위치로 설명
- "가장 큰 장점" 같은 마케팅성 표현 축소

## Cross-chapter Deduplication 확인

### Model / Harness / Runtime
- 1장: 전체 Architecture preview
- 3장: Harness 책임
- 16장: Runtime containment

Part I에서는 현재 중복 허용 범위다.

### Context / State
- 4장: current inference projection
- 7장: state taxonomy
- 8장: durable state layer

4장에서 7~8장 구현 설명을 추가하지 않는다.

### Tool / Authorization
- 5장: Tool Contract와 Eligibility
- 17장: 실제 Policy Enforcement

5장의 Authorization은 실행 경계 예고 수준으로 유지한다.

### MCP / A2A
- 6장: Capability Provider protocol
- 24장: independent Agent System protocol

6장의 A2A 설명은 비교 예고 수준으로 유지한다.

## Terminology 이슈

전체 Terminology Review에서 처리할 항목:
- Model / model
- Tool / tool
- State / state
- Context / context
- Runtime / runtime
- Memory / memory
- Completion / completion
- Long-running / long-running

현재 Line Review에서는 문장을 크게 흔들지 않기 위해 개념명 대문자 스타일을 그대로 유지했다.

## 결론

Part I~II Line Review: PASS.

다음 우선순위:
1. Part III Line Review
2. Part IV~V Line Review
3. Part VI~VII Line Review
4. Epilogue Line Review
5. Terminology Review
