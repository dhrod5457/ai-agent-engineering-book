# Manuscript Structural Review v1

기준일: 2026-10-02
대상: 25개 본장 + Epilogue 1차 Draft

## 상태

~~~text
Part I   1~3장    PASS
Part II  4~6장    PASS
Part III 7~11장   PASS
Part IV  12~13장  PASS
Part V   14~17장  PASS
Part VI  18~21장  PASS
Part VII 22~25장  PASS
Epilogue          PASS
~~~

본문 25장 약 158.8k자, Epilogue 포함 약 161.9k자의 1차 원고가 작성됐다.

이는 문자 수 기준의 작업량 확인용 수치이며 최종 출판 분량을 의미하지 않는다.

## 전체 서사

현재 원고는 다음 흐름을 가진다.

~~~text
Model
→ Agent Loop
→ Harness
→ Context
→ Tool
→ MCP
→ State Taxonomy
→ Agent State Plane
→ Recovery
→ Long-running
→ Reconciliation
→ Memory
→ Memory Security
→ Identity
→ Credential
→ Sandbox
→ Risk Policy
→ Trace
→ Eval
→ Eval CI
→ Harness Ablation
→ Multi-Agent
→ Handoff
→ A2A
→ Minimum Production Agent
→ Software Factory Boundary
~~~

핵심 논리는 끊기지 않는다.

## 책의 중심 주장

전체 원고에서 다음 네 주장이 일관되게 유지된다.

### 1. Model Capability ≠ Agent Capability

Agent는 Model만이 아니라 Context, Tool, Harness, State, Runtime, Policy, Eval의 결합이다.

### 2. Deterministic where possible, Agentic where necessary

Retry count, authorization, test result처럼 기계가 판정 가능한 영역은 System에 둔다.

Open-ended diagnosis, planning, synthesis는 Model이 담당할 수 있다.

### 3. Context ≠ Durable State

Long-running Agent의 핵심은 더 큰 Context만이 아니라 execution continuity다.

### 4. Completion Claim ≠ Completion Authority

가능하면 actual artifact / external state / deterministic verifier로 완료를 판정한다.

이 네 축이 전체 Part에 반복적으로 연결된다.

## 이 책의 독자적 중심 개념

### Agent State Plane

8장을 중심으로 7, 9, 10, 11장에 연결된다.

정의:

> Agent가 Process, Runtime, Context를 잃어도 실행 이력과 Goal, Progress, Approval, Artifact, External Source Reference를 바탕으로 작업을 이어갈 수 있게 하는 상태 관리 계층.

주의:
- 외부 표준 용어처럼 쓰지 않는다.
- Event Sourcing을 필수 구현처럼 쓰지 않는다.
- Factory Control Plane과 분리한다.

현재 책의 가장 차별적인 synthesis다.

### Memory Write Gate

13장에서 Memory를 future behavior에 영향을 주는 privileged side effect로 정의한다.

### Harness Debt

3장에서 소개하고 21장에서 운영 방법으로 회수한다.

### Risk R0~R4

17장의 illustrative control profile이다. 표준 taxonomy가 아니다.

## Part 간 연결

### Part I → II
Harness가 Model에게 무엇을 보여주고 어떤 Action Surface를 줄 것인가로 연결.

### Part II → III
Context/Tool Interface만으로는 multi-turn execution continuity가 해결되지 않으므로 State로 이동.

### Part III → IV
State 전체와 Long-term Memory를 분리한 뒤 Memory lifecycle과 security를 별도 심화.

### Part IV → V
Memory까지 관리해도 실제 External Action에는 Identity/Credential/Runtime Policy가 필요하므로 Security Boundary로 이동.

### Part V → VI
Control이 있어도 실제 행동을 관찰·측정해야 하므로 Trace/Eval로 이동.

### Part VI → VII
Single-Agent가 측정 가능하고 통제 가능해진 뒤 Multi-Agent complexity를 추가.

연결 상태: PASS.

## 반복이 의도적으로 필요한 핵심 식

다음은 장 사이에 반복되지만 책의 spine 역할을 한다.

~~~text
Model ≠ Agent
Context ≠ Durable State
Memory ≠ Source of Truth
Sandbox ≠ Authorization
Completion Claim ≠ Completion Authority
Agent State Plane ≠ Factory Control Plane
~~~

완전히 제거하지 않는다.

다만 Line Review에서 동일한 설명 문단까지 반복되는 경우 압축한다.

## Line Review 우선 중복 후보

### Model / Harness / Runtime 설명
1장, 3장, 16장에 반복.

각 장의 역할:
- 1장: 전체 architecture preview
- 3장: Harness 상세
- 16장: Runtime containment

Preview 문장을 줄일 수 있다.

### Context vs State
4장, 7장, 8장에 반복.

각 장의 역할:
- 4장: inference working set
- 7장: taxonomy
- 8장: durable layer

같은 정의 문장을 반복하지 말고 후속 장에서 참조하도록 다듬는다.

### Memory vs Source of Truth
7, 11, 12, 13장에 반복.

핵심 문장은 유지하되 사례 중복을 줄인다.

### Identity / Authorization / Approval
6, 14, 17, 24장에 반복.

6/24장은 protocol boundary preview 수준으로 압축 가능.

### Single-Agent First
3, 21, 22, 25장에 반복.

3장은 Harness minimalism,
21장은 ablation,
22장은 multi-agent decision,
25장은 adoption sequence로 역할을 분명히 유지한다.

## 용어 일관성 검토 필요

Line Review에서 다음 표기를 통일한다.

- production / Production
- model / Model
- tool / Tool
- state / State
- memory / Memory
- runtime / Runtime
- side effect / Side Effect
- long-running / Long-running
- completion / Completion

현재 Draft는 개념명 강조를 위해 영문 대문자를 많이 사용한다.

최종 문체에서는 일반명사는 한국어/소문자로 줄이고 실제 개념명만 일관되게 유지하는 편이 자연스럽다.

## Source 처리

현재 초고의 "주요 근거"는 장별 Research Pointer 역할이다.

출판 원고 단계에서는:
- 직접 주장
- vendor observation
- preprint
- protocol fact
- book synthesis

를 구분해 각 문장 또는 절의 source note로 연결해야 한다.

특히 출간 직전 재검증:
- MCP version
- A2A version
- Entra Agent ID 상태
- AWS Agentic AI Lens
- Claude Code sandbox/auto mode
- OSWorld 2.0
- Memory security preprints

## 분량 균형

Part I~V는 장당 대략 5.5k~8.0k자.
Part VI는 약 5.2k~5.6k자.
Part VII는 약 3.9k~5.1k자.

Line Review 전에는 억지로 동일 분량을 맞추지 않는다.

Part VII는 통합/경계 장이므로 상대적으로 짧은 것이 구조적으로 문제는 아니다.

## 부족한 구조

현재 Structural Gap으로 판단되는 필수 신규 장은 없다.

다음은 Appendix로 충분하다.

- Agent State Event Catalog
- Risk / Policy Matrix
- Eval Case Template
- Product / Protocol Version Reference
- Agent Engineering Checklist

## 전체 Structural Review 결론

PASS.

Phase 6 Draft는 완료로 전환할 수 있다.

다음 Phase:

~~~text
Phase 7 Review
1. Line Review
2. Evidence / Citation Review
3. Terminology Review
4. Cross-chapter Deduplication
5. Publication-time Freshness Audit
6. Manuscript Assembly
~~~

첫 Review 대상은 Part I~II부터 시작한다.
