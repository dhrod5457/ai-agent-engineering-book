# Concept

기준일: 2026-10-02

## 현재 작업 제목

**AI Agent Engineering**

부제 후보:

**LLM을 실제 작업 가능한 Agent로 만드는 설계 원칙**

이 문서는 1~3차 리서치에서 확인한 Agent Runtime, Context, State, Memory, Tool Interface, Harness, Sandbox, Identity, Security, Eval 자료를 바탕으로 책 전체의 중심 개념을 고정한다.

---

# 중심 주제

이 책의 중심 주제는 **LLM을 단순 응답 모델이 아니라 실제 환경에서 도구를 사용하고 상태를 이어가며 안전하고 검증 가능한 결과를 만드는 Agent로 구성하는 방법**이다.

이 책은 특정 Agent Framework 사용 설명서가 아니다.

또한 Multi-Agent 시스템을 많이 만드는 방법을 설명하는 책도 아니다.

핵심 질문은 다음과 같다.

> Model을 실제 작업 가능한 Agent로 만들기 위해 Context, State, Tool Interface, Harness, Runtime, Identity, Security, Eval을 어떻게 분리하고 조합해야 하는가?

독자가 마지막에 답할 수 있어야 하는 질문:

> 이 Agent는 어떤 상태를 유지하고, 어떤 Tool을 어떤 권한으로 사용하며, 실패 후 어떻게 이어가고, 실제 완료를 무엇으로 검증해야 하는가?

---

# 핵심 정의

책에서 사용할 기본 정의:

> **AI Agent Engineering은 Model을 실제 환경에서 안전하고 복구 가능하게 판단·행동시키기 위해 Context, State, Memory, Tool Interface, Harness, Runtime, Identity, Policy, Observability, Evaluation을 설계하는 소프트웨어 엔지니어링 활동이다.**

이를 구조로 표현하면 다음과 같다.

~~~text
Human / Upstream System
        ↓
Identity / Delegation
        ↓
Agent Definition
        ↓
Context Engine
        ↓
Agent Harness
        ↔
Agent State Plane
        ↓
Capability / Policy Gateway
        ↓
Execution Runtime
        ↓
External World

Cross-cutting:
Trace / Audit / Eval / Security / Cost
~~~

---

# 책의 핵심 관점

## 1. Model Capability와 Agent Capability를 분리한다

책 전체의 출발점:

~~~text
Model Capability
≠ Agent Capability
~~~

Agent의 실제 능력은 Model 하나로 결정되지 않는다.

~~~text
Agent Capability
≈ f(
  Model,
  Instruction,
  Context,
  Tool Interface,
  Harness,
  State,
  Memory,
  Runtime,
  Identity,
  Security Policy,
  Evaluation Feedback
)
~~~

따라서 benchmark score 하나로 Agent 전체를 설명하지 않는다.

---

## 2. Agent는 Prompt + Tool 목록이 아니다

최소 Agent는 반복 구조를 가진다.

~~~text
Input
→ Context
→ Model
→ Decision
→ Tool / Action
→ Observation
→ Next Context
↺
~~~

Production Agent에는 여기에 추가로 다음이 필요하다.

- stop condition
- retry
- interruption / resume
- budget
- approval
- tracing
- state continuity
- verification
- failure classification

핵심 원칙:

> Agent의 자율성은 model output이 아니라 Harness와 Runtime 안에서 실행된다.

---

## 3. Context는 저장소가 아니다

Context는 현재 inference에 들어가는 제한된 attention budget이다.

따라서:

~~~text
More Context
≠ Better Agent
~~~

Context Engine의 목표는 모든 정보를 넣는 것이 아니라 현재 decision에 필요한 high-signal information을 projection하는 것이다.

~~~text
Durable State
      ↓
Context Projection
      ↓
Current Inference
~~~

핵심 원칙:

> Context는 State의 projection이지 State 자체가 아니다.

---

## 4. Agent State Plane을 별도 계층으로 본다

장기 Agent에서 가장 중요한 문제 중 하나는 process나 context window가 사라져도 작업 상태를 잃지 않는 것이다.

책에서는 이를 **Agent State Plane**으로 정의한다.

~~~text
Agent State Plane
- Event History
- Checkpoint / Snapshot
- Goal / Progress
- Artifact Index
- Approval State
- External Source Version
- Memory Reference
~~~

핵심 책임:

> Agent가 process, runtime, context를 잃어도 무엇을 했고 어디까지 진행했으며 무엇을 다시 하면 안 되는지 복구할 수 있게 한다.

---

## 5. State 종류를 분리한다

다음 개념을 하나의 Memory로 합치지 않는다.

~~~text
Inference Context
≠ Conversation / Session State
≠ Run State
≠ Workspace State
≠ Goal / Task State
≠ Artifact State
≠ Long-term Memory
≠ External Source of Truth
~~~

### Session
대화와 turn continuity.

### Run State
현재 실행의 interruption, retry, approval 등.

### Workspace
filesystem, process, browser 같은 실행환경 상태.

### Goal
완료해야 할 objective와 completion contract.

### Artifact
실제 결과물.

### Memory
미래 실행에서 재사용할 lesson / preference / knowledge.

### External Source of Truth
Agent가 소유하지 않는 canonical data.

---

## 6. Replay와 Side Effect 재실행을 분리한다

Durable execution 관점에서 event history는 중요하지만 Agent에서는 model/tool을 무조건 replay하면 안 된다.

~~~text
Replay
≠ Re-run Model
≠ Re-run Side Effect
~~~

과거 model/tool 결과를 event로 기록하고 state projection을 복구한다.

외부 mutation은 가능한 한 idempotency key와 execution record를 사용한다.

---

## 7. Memory Write는 Privileged Side Effect다

Persistent Memory는 미래 Agent 행동에 영향을 준다.

따라서 자동 memory write를 단순 저장으로 취급하지 않는다.

~~~text
Observation
→ Memory Candidate
→ Provenance
→ Scope
→ Security / Privacy
→ Contradiction / Freshness
→ Policy
    ├─ Accept
    ├─ Review
    └─ Quarantine
~~~

핵심 원칙:

> Memory는 많이 저장하는 것이 아니라 안전하게 승격하고 필요할 때 선택적으로 불러오는 것이 중요하다.

---

## 8. Memory는 Source of Truth가 아니다

Memory는 stale할 수 있다.

따라서 irreversible action 전에는 가능한 한 authoritative source를 다시 확인한다.

~~~text
Memory / Working State
      ↓
Refresh Canonical Source
      ↓
Reconcile
      ↓
Act
~~~

Long-running Agent에서 가장 중요한 문제 중 하나는 reasoning depth보다 **state freshness**다.

---

## 9. External State Reconciliation을 Harness 책임으로 본다

외부 세계는 Agent가 작업하는 동안 바뀐다.

장기 Agent는 다음 loop를 가져야 한다.

~~~text
Read
→ Project
→ Act
→ Refresh
→ Compare
→ Reconcile
→ Re-plan
→ Verify
↺
~~~

Refresh가 특히 중요한 시점:

- irreversible action 직전
- approval 후 resume
- long pause 후
- retry / recovery
- handoff
- source version mismatch
- final completion

---

## 10. Tool은 Agent-Computer Interface다

Tool은 단순 API wrapper가 아니다.

좋은 Tool은 Agent가 행동 공간을 이해하고 안전하게 실행할 수 있도록 설계된 interface다.

고려 대상:

- name
- description
- input schema
- output schema
- side effect
- permission
- failure mode
- result size
- provenance
- trust level

핵심 원칙:

> Tool Interface도 Agent Capability의 일부다.

---

## 11. Tool Protocol과 Agent Harness를 분리한다

MCP는 capability/context integration boundary다.

A2A는 independent Agent System 간 work protocol이다.

둘 다 Agent 전체가 아니다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

또한:

~~~text
MCP Task
≠ A2A Task
≠ Runtime Session
≠ Product / Factory Task
~~~

같은 이름의 Task를 내부 domain object로 곧바로 통합하지 않는다.

---

## 12. Identity를 독립 계층으로 본다

Agent가 실제 side effect를 수행하려면 누가 행동하는지 명확해야 한다.

구분:

~~~text
Human User Identity
Application Identity
Agent Identity
Workload Identity
Tool Identity
Resource Identity
~~~

또한:

~~~text
Discovery
≠ Authentication
≠ Authorization
≠ Approval
~~~

Delegated와 Autonomous access를 분리한다.

---

## 13. Credential은 Model Context에서 분리한다

가능하면 Agent가 raw credential을 직접 보유하지 않게 한다.

추천 구조:

~~~text
Agent Intent
→ Capability Gateway
→ Authorization
→ Short-lived Credential Injection
→ External API
~~~

핵심 원칙:

> Agent가 무엇을 해야 하는지 판단하는 것과 실제 credential을 소유하는 것을 분리한다.

---

## 14. Sandbox와 Authorization을 분리한다

Sandbox는 Agent가 물리적으로 어디까지 접근할 수 있는지 제한한다.

Authorization은 어떤 action을 할 수 있는지 제한한다.

~~~text
Isolation
= WHERE

Authorization
= WHAT

Approval / Policy
= WHEN
~~~

세 가지가 모두 필요하다.

---

## 15. Risk-adaptive Policy를 사용한다

모든 Agent Task를 같은 권한으로 실행하지 않는다.

예시:

~~~text
R0 Offline / Read
R1 Workspace Mutation
R2 External Read
R3 Bounded External Write
R4 High-impact / Irreversible
~~~

Risk에 따라:

- sandbox level
- filesystem scope
- network scope
- credential scope
- approval
- independent verifier
- rollback

을 다르게 적용한다.

---

## 16. Agent는 권한 확대를 제안할 수 있지만 적용하지 않는다

Deny가 발생했을 때:

~~~text
Deny
→ Inspect
→ Agent proposes minimal change
→ Deterministic validation
→ Risk analysis
→ Approval
→ Apply
→ Retry
~~~

핵심 원칙:

> Agent에게 policy mutation authority까지 주지 않는다.

---

## 17. Harness를 Versioned Software로 본다

Harness는 다음 가설들의 집합이다.

- planner가 필요한가
- memory가 필요한가
- evaluator가 필요한가
- subagent가 필요한가
- progress artifact가 필요한가
- compaction이 필요한가

각 component는 실제 failure를 해결하는지 측정해야 한다.

~~~text
Minimal Baseline
→ Add Component
→ Eval
→ Measure Marginal Value
→ Keep / Remove
~~~

---

## 18. Harness Debt를 관리한다

Agent 실패가 발생할 때마다 scaffold를 추가하면 복잡도가 계속 늘어난다.

Harness Debt 후보:

- 오래된 model workaround
- 중복 planner
- 중복 verifier
- conflicting instruction
- obsolete tool wrapper
- unused state
- 필요성 불명의 memory
- 과도한 subagent

핵심 원칙:

> 강한 Model이 나오면 Harness도 다시 줄여본다.

---

## 19. Completion Claim과 Outcome Verification을 분리한다

Agent가 완료했다고 말하는 것은 완료가 아니다.

~~~text
Agent Completion Claim
        ↓
Refresh External Source
        ↓
Inspect Actual Artifact / State
        ↓
Independent Verification
        ↓
Completion
~~~

특히 long-horizon task에서 internal checklist를 actual source보다 신뢰하지 않는다.

---

## 20. Trace는 Agent 개발의 기본 데이터다

Final output만 보면 실패 원인을 구분하기 어렵다.

Trace 후보:

- model request/result
- tool proposal
- authorization
- tool execution
- approval
- state update
- handoff
- retry
- runtime error
- cost / latency

Trace는 audit뿐 아니라 eval과 improvement의 원천이다.

---

## 21. Eval은 Output보다 넓다

평가 대상:

~~~text
Output
Trajectory
Tool Selection
Tool Arguments
State Handling
Policy Compliance
Security
Outcome
Reliability
Cost / Latency
Recovery
~~~

Agent System은 model 이름 하나로 version하지 않는다.

~~~text
AgentVersion = (
  model,
  instruction,
  context policy,
  harness,
  state schema,
  memory policy,
  tools,
  identity policy,
  runtime,
  sandbox policy,
  grader
)
~~~

---

## 22. Eval을 CI에 연결한다

Production failure를 reusable eval case로 승격한다.

~~~text
Production Failure
→ Triage
→ Regression Case
→ Candidate Change
→ Offline Eval
→ Shadow / Canary
→ Promotion
~~~

known failure가 사람 기억에만 남지 않게 한다.

---

## 23. Benchmark도 Versioned Software다

Agent benchmark score는 model만의 성능이 아니다.

~~~text
Benchmark Score
=
Model
+ Harness
+ Tool Interface
+ State Strategy
+ Runtime
+ Policy
+ Environment
+ Grader
+ Noise
~~~

따라서 benchmark version, task revision, grader version, runtime resource를 함께 기록한다.

---

## 24. Multi-Agent는 기본값이 아니다

먼저 하나의 Agent가 다음을 제대로 해야 한다.

- context
- state
- tool
- runtime
- identity
- security
- trace
- eval

그 다음 다음 이유가 명확할 때만 multi-agent를 추가한다.

- context isolation
- independent specialist
- permission separation
- parallel work
- independent review

핵심 원칙:

> Agent 수보다 경계 설계가 먼저다.

---

# 다른 책과의 관계

## AI Instruction Engineering

다룬다:

- CLAUDE.md
- AGENTS.md
- Rules
- Skills
- Hooks
- instruction eval

이 책에서는 Instruction을 하나의 Agent Definition 요소로만 다룬다.

## Cloud Agent

다룬다:

- Local / Cloud routing
- Cloud execution
- prepared environment
- Git handoff
- Runner
- cloud resource / cost

이 책에서는 Runtime 자체의 설계 원칙까지만 다룬다.

## AI Software Factory

다룬다:

- Durable Work
- Scheduler
- Worker Fleet
- Control Plane
- Acceptance
- Delivery
- Factory-level Recovery

이 책에서는 하나의 Agent execution continuity까지만 다룬다.

~~~text
Agent State Plane
= execution continuity

Software Factory Control Plane
= work-system continuity
~~~

---

# Minimum Viable Agent Engineering

처음부터 Memory, Multi-Agent, Planner를 모두 넣을 필요는 없다.

최소 형태:

~~~text
Model
+ Clear Instruction
+ Small Tool Surface
+ Controlled Runtime
+ Deterministic Verification
+ Trace
~~~

다음 순서로 확장한다.

~~~text
Minimal Agent
→ Clear Tool Contract
→ Reproducible Runtime
→ Trace
→ Eval
→ Durable State
→ Identity / Policy
→ Memory
→ Long-running
→ Multi-agent
~~~

핵심 원칙:

> Capability보다 먼저 Control과 Verification을 만든다.

---

# 책 전체의 핵심 원칙

1. Model Capability와 Agent Capability를 분리한다.
2. Agent는 Prompt + Tool 목록이 아니다.
3. Context는 Durable State가 아니다.
4. Session, Workspace, Goal, Memory를 분리한다.
5. Agent State Plane을 process와 context 밖에 둔다.
6. Replay와 Side-effect 재실행을 분리한다.
7. Memory Write를 privileged side effect로 본다.
8. Memory를 Source of Truth로 사용하지 않는다.
9. Long-running Agent는 External State를 reconcile한다.
10. Tool을 Agent-Computer Interface로 설계한다.
11. Capability Discovery와 Authorization을 분리한다.
12. Credential을 Model Context에서 분리한다.
13. Sandbox, Authorization, Approval을 분리한다.
14. Task Risk에 따라 containment를 다르게 적용한다.
15. Agent는 권한 확대를 제안할 수 있지만 적용하지 않는다.
16. Harness를 versioned software로 다룬다.
17. Harness component는 검증 가능한 가설이어야 한다.
18. Completion Claim과 Completion Authority를 분리한다.
19. Trace와 Eval을 Agent 개발 loop의 일부로 만든다.
20. Multi-Agent는 Single-Agent의 약점을 숨기는 수단이 아니다.
