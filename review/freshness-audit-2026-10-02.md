# Publication-time Freshness Audit

기준일: 2026-10-02
대상: 25개 본장 + Epilogue + Research Source Catalog

## 결론

PASS WITH CORRECTIONS.

현재 원고의 중심 Architecture와 Engineering Principle을 뒤집는 변경은 발견되지 않았다.

다만 현재 제품·프로토콜 상태를 기준으로 두 항목은 본문 수정이 필요했고 즉시 반영했다.

1. A2A latest released specification: 0.3 계열 → 1.0.0
2. AWS AgentCore: 기본 ephemeral compute 외에 managed session storage(Preview) 추가

이외 high-priority source는 현재 주장과 일치한다.

---

# 1. MCP

## 확인 결과

2026-10-02 기준:

- 2026-07-28: FINAL
- 2026-12-15: NOT READY

2026-07-28에서 다음 핵심 변화가 유지된다.

- stateless protocol core
- protocol-level session 제거
- explicit state handle
- self-describing request
- Tasks extension
- authorization hardening

## 원고 영향

6장과 12번 research topic의 현재 설명 유지 가능.

MCP Task와 Runtime Session / Factory Task를 분리하는 책의 경계도 유지된다.

## 상태

PASS.

출간 시점에 새로운 FINAL spec이 나왔는지만 다시 확인한다.

---

# 2. A2A

## 확인 결과

2026-10-02 기준 최신 Released Specification은 **1.0.0**이다.

초기 조사에서 확인한 0.3 계열 이후 breaking change와 versioning 구조가 추가됐다.

1.0에서도 책이 사용하는 다음 핵심 개념은 유지된다.

- Agent Card
- Message
- Task
- Artifact
- Stateful Task Lifecycle
- INPUT_REQUIRED
- AUTH_REQUIRED
- streaming / push update
- server-side authentication / authorization responsibilities

1.0에서는 protocol version negotiation과 Agent Card interface declaration이 더 명확해졌다.

또 AUTH_REQUIRED state transition 자체는 특정 operation authorization을 의미하지 않는다.

## 원고 영향

24장에:

- 2026-10-02 latest release 1.0.0
- 버전별 wire format보다 stable responsibility boundary를 설명한다는 문장
- AUTH_REQUIRED ≠ authorization grant

를 추가했다.

research/topics/12와 Source Catalog도 1.0.0 기준으로 갱신했다.

## 상태

CORRECTED / PASS.

---

# 3. OpenAI Agents SDK / Codex

## 확인 결과

현재 공식 문서에서 다음 구조가 유지된다.

- conversational Session과 Agent long-term memory 구분
- Sandbox Session과 conversational Session 구분
- memory progressive disclosure
- stale memory보다 current environment 우선
- Goal을 persisted objective / completion condition과 연결

## 원고 영향

7장, 12장의 State / Memory 경계 유지 가능.

## 상태

PASS.

---

# 4. AWS AgentCore Runtime

## 확인 결과

기본 Runtime Session은:

- dedicated microVM
- isolated CPU / memory / filesystem
- compute lifecycle 종료 시 microVM termination
- 기본 memory/local disk는 ephemeral

구조를 유지한다.

그러나 현재는 **managed session storage (Preview)**를 추가로 제공한다.

이 storage는:

- microVM session별 격리
- stop/resume 사이 filesystem restoration
- service-managed durability
- 14-day idle expiry
- runtime version update 시 reset

특성을 가진다.

따라서 다음 식은 너무 강하다.

~~~text
Runtime Workspace
= always ephemeral
~~~

더 정확한 경계는:

~~~text
Runtime Compute Lifecycle
≠ Workspace Persistence Lifecycle
≠ Agent Execution State
≠ Long-term Memory
~~~

이다.

## 원고 영향

7장:
- Workspace가 persistence를 지원할 수도 있음을 추가
- persistence가 Goal / Approval / Durable State와 같지는 않음을 명시

16장:
- Runtime Session = ephemeral이라는 단정을 제거
- Session Storage와 Agent State Plane의 책임을 분리

research/topics/09, 11과 Source Catalog 갱신.

## 상태

CORRECTED / PASS.

---

# 5. AWS Agentic AI Lens

## 확인 결과

2026-10-02 현재 guidance에서 다음이 유지된다.

- every tool invocation에 external authorization
- agent identity + originating user context propagation
- prompt-only authorization은 불충분
- high-risk mutation에 HITL checkpoint
- risk-tiered human approval
- deterministic risk classification
- temporary / dynamic permission boundary

## 원고 영향

17장 Risk-adaptive Policy의 근거 유지.

R0~R4는 AWS taxonomy가 아니라 이 책의 illustrative control profile로 계속 명시한다.

## 상태

PASS.

---

# 6. Anthropic Claude Code Sandboxing / Auto Mode

## 확인 결과

Sandboxing 자료의 핵심:

- filesystem isolation
- network isolation
- approval fatigue 감소
- sandbox boundary 내부의 더 높은 autonomy

가 유지된다.

2026 Auto Mode 자료도 permission prompt를 전부 제거하는 대신 classifier / safe path / sandbox 등 layered controls를 사용하는 방향을 유지한다.

## 원고 영향

16~17장 유지 가능.

vendor 내부 운영 수치는 일반 한계로 확대하지 않는다.

## 상태

PASS.

---

# 7. NVIDIA OpenShell

## 확인 결과

현재 자료에서 다음 구조 유지:

- trusted supervisor
- less-trusted sandbox / agent child
- filesystem / process / network policy
- credential binding/injection
- dynamic policy update
- policy validation outside workload

## 원고 영향

15~17장 유지 가능.

## 상태

PASS.

---

# 8. OSWorld 2.0

## 확인 결과

공식 사이트 기준:

- 108 long-horizon tasks
- 31 self-hosted websites
- human median 약 1.6 hours
- 69.6% tasks > 1 hour
- 평균 수백 Agent steps
- 27.25 average scoring checkpoints

Challenge Phenomena에는 다음이 현재도 포함된다.

- Cross-source Reasoning
- Implicit-state Inference
- Multi-item State Tracking
- Conflict Disambiguation
- Dynamic Environment
- Proactive Interaction

## 원고 영향

10~11장 Long-running / Reconciliation 논리 유지 가능.

Leaderboard 수치는 빠르게 바뀌므로 책의 핵심 주장에 사용하지 않는다.

## 상태

PASS.

---

# 9. tau2-bench

## 확인 결과

1.0.1 grading change와 release 사이 score 비호환 경고가 유지된다.

같은 trajectory도 grader change로 score가 변할 수 있다는 점은 Benchmark Versioning의 근거로 계속 사용할 수 있다.

## 원고 영향

19장 유지 가능.

## 상태

PASS.

---

# 10. Memory Security Research

2026-10-02 기준 다음 자료는 여전히 emerging research / preprint로 취급한다.

- MPBench — arXiv:2606.04329
- MemSecBench — arXiv:2607.27080
- MemPoison — arXiv:2607.14651
- MemSentry — arXiv:2609.08747

현재 확인된 핵심 방향:

- persistent memory poisoning
- write → execute → repair lifecycle
- compositional / dormant corruption
- Accept / Review / Quarantine write gate

은 유지된다.

## 원고 영향

13장의 Memory Write Gate는 책의 synthesis로 유지한다.

개별 논문 결과를 업계 일반 사실이나 표준으로 표현하지 않는다.

## 상태

PASS WITH PREPRINT LABEL.

---

# Freshness Risk Register

## High Volatility

출간 직전 반드시 다시 확인:

1. MCP latest FINAL specification
2. A2A latest Released Specification
3. OpenAI Agents SDK Sandbox / Memory / Goals
4. AWS AgentCore Runtime / Session Storage
5. Microsoft Entra Agent ID
6. AWS Agentic AI Lens
7. NVIDIA OpenShell
8. Claude Code Auto Mode / Sandboxing

## Medium Volatility

1. OSWorld 2.0 leaderboard
2. tau2-bench release
3. vendor feature names
4. preview / GA status

## Research Status Volatility

1. MPBench
2. MemSecBench
3. MemPoison
4. MemSentry
5. Selective Revalidation
6. Task-State Horizon
7. AgentRewind

논문이 peer-reviewed 상태로 변경됐는지 출간 직전에 확인한다.

---

# Publication Rule

본문 핵심 논리는 다음과 같이 버전 변화에 독립적으로 유지한다.

~~~text
Current Product Fact
        ↓
Responsibility Boundary
        ↓
Engineering Principle
~~~

제품 이름과 API 문법이 바뀌어도 Responsibility Boundary가 유지되는 서술을 우선한다.

---

# Final Status

~~~text
Line Review                PASS
Terminology Review         PASS
Cross-chapter Dedup        PASS
Evidence / Citation        PASS
Freshness Audit            PASS WITH CORRECTIONS
~~~

Phase 7 Review를 완료할 수 있다.

다음 단계:

> Manuscript Assembly
