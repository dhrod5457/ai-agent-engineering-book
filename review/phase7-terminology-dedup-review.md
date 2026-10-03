# Phase 7 Terminology / Cross-chapter Dedup Review

기준일: 2026-10-02
브랜치: review/phase7-line-edit

## 결과

PASS.

## Terminology

전체 25장 + Epilogue에 대해 다음 canonical 표기를 검사했다.

- Long-running
- Side Effect
- Agent State Plane
- Factory Control Plane
- Source of Truth
- Completion Authority
- 일반 prose의 production Agent / production system / production environment

비정상 casing: 0건.

planning/terminology.md에는 다음 정의를 추가했다.

- Side Effect
- Completion Claim
- Completion Authority
- Verification
- Long-running Agent
- Memory Write Gate
- AgentVersion
- Agent-as-Tool
- Handoff
- Remote Agent

## Cross-chapter Deduplication

### 기계 검사

Part별로 60자 이상 prose paragraph의 exact duplication을 검사했다.

결과:
- Part I~III: 0
- Part IV~VI: 0
- Part VI~VII + Epilogue: 0

exact duplication이 없다는 것이 semantic overlap이 없다는 뜻은 아니다.

### Semantic overlap 수정

#### 1장 ↔ 25장
1장의 전체 production-agent 확장 roadmap을 제거했다.
1장은 "control/verification first" 원칙만 남기고 실제 확장 순서는 25장으로 위임했다.

#### 3장 ↔ 21장
3장의 Component Record 상세 schema를 제거했다.
3장은 존재 이유 기록의 원칙만 남기고 detailed record / ablation은 21장으로 위임했다.

#### 22장 ↔ 25장
25장의 Multi-Agent 도입 조건 목록을 압축했다.
상세 판단 기준은 22장에 남기고 25장은 전체 확장 순서에서의 위치만 설명한다.

#### 25장 ↔ Epilogue
이전 Line Review에서 Epilogue의 반복 Multi-Agent 문단을 제거했다.

## 의도적으로 유지한 반복

다음 문장은 책의 conceptual spine이므로 중복 제거 대상에서 제외한다.

~~~text
Model ≠ Agent
Context ≠ Durable State
Memory ≠ Source of Truth
Sandbox ≠ Authorization
Completion Claim ≠ Completion Authority
Agent State Plane ≠ Factory Control Plane
~~~

단, 같은 문장의 상세 설명은 각 장의 책임에 맞게 다르게 유지한다.

## 결론

Terminology Review: PASS
Cross-chapter Deduplication: PASS

다음:
Evidence / Citation Review
