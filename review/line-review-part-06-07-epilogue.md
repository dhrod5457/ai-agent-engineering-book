# Line Review — Part VI~VII + Epilogue

기준일: 2026-10-02
대상:
- chapters/18/draft.md
- chapters/19/draft.md
- chapters/20/draft.md
- chapters/21/draft.md
- chapters/22/draft.md
- chapters/23/draft.md
- chapters/24/draft.md
- chapters/25/draft.md
- chapters/epilogue/draft.md

## 상태

PASS.

후반부는 앞에서 이미 정의한 개념을 다시 설명하기보다 측정, 개선, 확장, 도입 순서로 회수하는 것이 목적이다. 불필요한 "실제" 반복과 Production 표현을 줄이고, 각 장의 역할을 유지했다.

## Part VI

### 18장 Trace
- "실제 시스템 행동" → "시스템 행동"
- Trace의 목적을 internal reasoning 보관이 아니라 execution reconstruction으로 유지

### 19장 Eval
- Production/실제 표현을 운영/Environment 최종 상태 중심으로 정리
- Output / Trajectory / Outcome / Reliability 구분 유지

### 20장 Eval CI
- Production Failure → 운영 실패로 자연스럽게 정리
- Shadow / Canary / AgentVersion 구조 유지
- 운영 failure를 regression으로 승격하는 메시지를 명확히 유지

### 21장 Harness Ablation
- "실제로 필요한가/기여했는가" 같은 강조 축소
- repeated trials, variance, capability slice는 그대로 유지

## Part VII

### 22장 Single-Agent First
- "실제로" 반복 제거
- Multi-Agent 도입 판단을 capability boundary와 coordination cost 중심으로 유지

### 23장 Agent-as-Tool / Handoff
- "검토 완료"와 실제 검토 내용의 차이를 더 직접적으로 표현
- 독립 verifier는 구조적으로 독립해야 한다는 점으로 수정

### 24장 A2A
- 도입 순서 연결 문장 압축
- MCP/A2A/Factory Task 경계 유지

### 25장 Minimum Viable Production Agent
- "실제 Task/실제 실패/실제 이득" 반복 축소
- 기능 수보다 control/recovery/verification을 성숙 기준으로 유지

## Epilogue

- "실제" 반복을 줄이고 Agent Capability, Completion, 생산 시스템 경계를 직접 표현
- 마지막 핵심 문장은 유지:

> 좋은 Agent 시스템은 모델을 무조건 믿는 시스템이 아니라, 모델을 덜 믿어도 실제 일을 맡길 수 있는 시스템이다.

이 문장의 "실제"는 장식이 아니라 book thesis의 의미를 강화하므로 유지한다.

## Cross-chapter Dedup 확인

### Trace / Eval / Eval CI
- 18장: 관찰 데이터
- 19장: 평가 방법
- 20장: 개발·배포 lifecycle에 연결

역할 분리 유지.

### Harness Minimalism / Ablation / Single-Agent First
- 3장: Harness component를 hypothesis로 소개
- 21장: component effect 측정
- 22장: multi-agent complexity 판단
- 25장: 도입 순서

같은 "더 많이 넣는 것이 성숙이 아니다" 메시지는 spine으로 유지하되 세부 설명은 각 장 책임에 맞게 제한한다.

### Agent State Plane / Factory Control Plane
- 8장: 정의
- 25장: adoption boundary
- Epilogue: 다음 책으로 연결

반복 허용.

## 결론

Part VI~VII + Epilogue Line Review: PASS.

전체 Line Review 완료.

다음:
1. Terminology Review
2. Cross-chapter Deduplication
3. Evidence / Citation Review
