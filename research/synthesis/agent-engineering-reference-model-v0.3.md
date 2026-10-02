# Agent Engineering Reference Model v0.3

기준일: 2026-10-02

이 문서는 3차 리서치 결과를 반영한 종합 모델이다.

v0.2에서 State를 여러 종류로 분리했다면, v0.3에서는 이를 실제 Agent 실행을 지탱하는 **Agent State Plane**으로 구체화한다.

## 1. 정의

> AI Agent Engineering은 Model을 실제 환경에서 안전하고 복구 가능하게 판단·행동시키기 위해 Context, State, Memory, Tool Interface, Harness, Runtime, Identity, Policy, Observability, Evaluation을 설계하는 소프트웨어 엔지니어링 활동이다.

이 책의 범위는 다음 사이에 있다.

~~~text
Instruction Engineering
        ↓
Agent Engineering
        ↓
Cloud Execution
        ↓
Software Factory
~~~

## 2. Reference Architecture

~~~text
                 Human / Upstream System
                          │
                          ▼
                ┌─────────────────────┐
                │ Identity / Delegation│
                │ user / app / agent  │
                │ tool / resource     │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Agent Definition    │
                │ model / instruction │
                │ output contract     │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Context Engine      │
                │ retrieval / history │
                │ state projection    │
                │ tool schema         │
                └─────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Agent Harness       │
                │ loop / goal / stop  │
                │ retry / handoff     │
                │ budget / reconcile  │
                └──────┬────────┬─────┘
                       │        │
                       │        ▼
                       │  ┌──────────────────────┐
                       │  │ Agent State Plane    │
                       │  │                      │
                       │  │ Event History        │
                       │  │ Checkpoint/Snapshot  │
                       │  │ Goal/Progress        │
                       │  │ Artifact Index       │
                       │  │ Approval State       │
                       │  │ Source Versions      │
                       │  │ Memory References    │
                       │  └──────────┬───────────┘
                       │             │
                       │             ▼
                       │  ┌──────────────────────┐
                       │  │ Memory Boundary      │
                       │  │ propose/write gate   │
                       │  │ provenance/scope     │
                       │  │ retrieve/quarantine  │
                       │  └──────────────────────┘
                       │
                       ▼
             ┌───────────────────────────┐
             │ Capability / Policy Gateway│
             │ discovery / authz          │
             │ validation / approval      │
             │ credential injection       │
             │ result filtering           │
             └────────────┬───────────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Execution Runtime   │
                │ sandbox / microVM   │
                │ filesystem/network │
                │ browser/shell       │
                └─────────┬───────────┘
                          │
                          ▼
                    External World

Cross-cutting:
- Trace / Audit
- Eval / Regression
- Cost / Latency
- Security Policy
- Versioning
~~~

## 3. Agent State Plane

Agent State Plane은 모든 정보를 한 DB에 저장한다는 뜻이 아니다.

핵심 책임은:

> Agent가 process, context window, runtime session을 잃어도 무엇을 했고 어디까지 진행했으며 무엇을 다시 하면 안 되는지 복구할 수 있게 하는 것

이다.

### 최소 구성 후보

~~~text
Event History
= 실행 사실의 append-only history

Checkpoint / Snapshot
= 빠른 resume를 위한 materialized state

Goal / Progress
= 현재 completion contract와 milestone

Artifact Index
= 생성·검증된 결과물 reference

Approval State
= pause/resume 가능한 human/policy decision

External Source Versions
= 의존 중인 authoritative source와 revision

Memory References
= 장기 기억의 pointer와 provenance
~~~

## 4. Event History와 Replay

Durable execution 시스템의 중요한 교훈은 state를 process memory가 아니라 event history에서 복구한다는 것이다.

그러나 Agent에서는 LLM inference와 외부 side effect를 deterministic하게 재실행하면 안 된다.

따라서:

~~~text
Replay
≠ Re-run Model
≠ Re-run Tool Side Effect
~~~

과거 결과를 event로 기록하고 projection을 재구성한다.

예:

~~~text
model.completed
tool.authorized
tool.completed
approval.granted
artifact.verified
~~~

Recovery 시 이미 완료된 external mutation은 idempotency와 event record를 기준으로 중복 실행을 막는다.

## 5. Context는 State Plane의 Projection이다

Model은 전체 event history를 읽을 필요가 없다.

~~~text
State Plane
    ↓ projection
Context Engine
    ↓
Current Inference Context
~~~

즉 Context는 저장소가 아니라 현재 decision을 위해 만들어진 view다.

이 관점은 context compaction과 durable state를 혼동하지 않게 한다.

## 6. Memory는 State Plane 전체가 아니다

Persistent Memory는 Agent State Plane의 한 subsystem 또는 참조 대상이다.

~~~text
Execution State
≠ Long-term Memory
~~~

Memory의 목적은 미래 run에서 유용한 knowledge/lesson을 재사용하는 것이다.

Execution recovery에 필요한 state를 Memory에 맡기면 안 된다.

## 7. Memory Write Gate

3차 조사에서 가장 강해진 원칙 중 하나다.

~~~text
Observation
   ↓
Memory Candidate
   ↓
Provenance
   ↓
Scope
   ↓
Security / Privacy
   ↓
Contradiction / Freshness
   ↓
Policy
   ├─ Accept
   ├─ Review
   └─ Quarantine
~~~

Persistent memory write는 미래 Agent behavior를 바꾸므로 privileged side effect로 본다.

Memory retrieval도 단순 similarity search가 아니라:

- relevance
- authorization
- provenance
- freshness
- contradiction
- composition risk

를 고려한다.

## 8. External State Reconciliation

Long-horizon Agent는 external world의 snapshot을 working state로 들고 일한다.

하지만 external world는 바뀐다.

따라서 Harness에 다음 loop가 필요하다.

~~~text
Read
→ Project
→ Act
→ Refresh
→ Compare
→ Reconcile
→ Re-plan
→ Verify
~~~

특히 다음 시점에는 refresh를 강하게 고려한다.

- irreversible action 직전
- approval 이후 resume
- long pause 이후
- retry / recovery
- handoff
- external version mismatch
- final completion 검증

가능하면 version / ETag / revision을 이용해 optimistic concurrency를 사용한다.

## 9. Identity Chain

Agent action의 actor를 한 개의 service account로 축약하지 않는다.

~~~text
Human / Initiator
      ↓
Application
      ↓
Agent Identity
      ↓
Tool Identity / Credential
      ↓
Resource
~~~

Delegated mode와 autonomous mode를 분리한다.

### Delegated

~~~text
User
→ consent/scope
→ Agent
→ on-behalf-of token
→ Resource
~~~

### Autonomous

~~~text
System / Scheduler
→ Agent Workload Identity
→ app/workload token
→ Resource
~~~

Memory write provenance와 audit에도 이 identity chain을 연결한다.

## 10. Risk-adaptive Policy

모든 task에 같은 sandbox와 approval 정책을 쓰지 않는다.

예시:

~~~text
R0  offline/read-only
R1  workspace mutation
R2  external read
R3  bounded external write
R4  high-impact / irreversible
~~~

Risk에 따라 다음을 조합한다.

- isolation level
- filesystem scope
- network scope
- credential scope
- tool allowlist
- approval
- independent verifier
- rollback requirement

## 11. Policy Expansion

Agent가 deny를 만났다고 스스로 권한을 넓혀서는 안 된다.

권장 흐름:

~~~text
Deny
→ Inspect
→ Agent proposes minimal change
→ Deterministic validation
→ Risk analysis / prover
→ Review / Approval
→ Apply versioned policy
→ Retry
~~~

Agent는 policy change를 제안할 수 있지만 authority는 외부 control plane에 둔다.

## 12. Harness Minimalism

Harness는 기능 목록이 아니라 검증 가능한 가설의 집합이다.

각 component는 다음 질문에 답해야 한다.

> 이 component가 어떤 known failure를 줄이며, 그 효과를 어떤 eval로 증명했는가?

추천 과정:

~~~text
Minimal Baseline
→ Add Component
→ Eval
→ Measure Marginal Value
→ Keep / Remove
~~~

Model upgrade 때는 기존 Harness를 그대로 유지하지 않는다.

~~~text
New Model
→ Old Harness Eval
→ Minimal Baseline
→ Component Ablation
→ Security Regression
→ Long-horizon Regression
→ Promotion
~~~

## 13. Harness Debt

다음은 Harness Debt 후보다.

- 오래된 model workaround
- 중복 planner/verifier
- conflicting instruction
- 사용되지 않는 state
- 필요성 불명의 memory
- redundant tool wrapper
- 과도한 subagent
- benchmark-specific scaffold

Instruction Debt와 마찬가지로 주기적으로 제거한다.

## 14. Evaluation Unit

Agent System은 model 이름으로 version하지 않는다.

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

이 tuple 중 하나가 바뀌면 regression 가능성이 있다.

## 15. 핵심 경계식

~~~text
Model Capability
≠ Agent Capability

Context
≠ Durable State

Session
≠ Goal

Workspace
≠ Memory

Memory
≠ Source of Truth

Replay
≠ Side-effect Re-execution

Capability Discovery
≠ Authorization

Sandbox
≠ Authorization

Approval
≠ Containment

Protocol Task
≠ Product / Factory Task

Harness Complexity
≠ Agent Capability
~~~

## 16. 현재 핵심 원칙

1. Agent State는 process lifetime보다 오래 살아야 할 수 있다.
2. Event History는 execution recovery의 backbone이 될 수 있다.
3. Context는 State의 projection으로 본다.
4. Persistent Memory Write는 privileged side effect다.
5. Memory에는 provenance, scope, lifecycle이 필요하다.
6. Long-horizon Agent는 external source를 주기적으로 reconcile해야 한다.
7. User/App/Agent/Tool/Resource identity를 분리한다.
8. Credential은 action boundary에서 short-lived하게 주입하는 방향이 안전하다.
9. Task Risk에 따라 containment와 approval을 다르게 적용한다.
10. Agent는 권한 확대를 제안할 수 있지만 스스로 적용하지 않는다.
11. Harness component는 검증 가능한 engineering hypothesis다.
12. Model upgrade 시 Harness를 다시 줄이고 재검증한다.
13. Completion은 internal story가 아니라 current external state와 artifact evidence로 판정한다.

## 17. 이 책에서 State Plane을 다루는 경계

이 책의 Agent State Plane은 **하나의 Agent execution을 지속·복구·검증하는 state**를 다룬다.

다음은 software-factory-book의 범위다.

- 조직 backlog
- 여러 Task 간 dependency
- Worker fleet scheduling
- repository delivery
- merge/deploy authority
- cross-project orchestration

즉:

~~~text
Agent State Plane
= execution continuity

Software Factory Control Plane
= work system continuity
~~~

로 경계를 유지한다.

## 18. 다음 단계

현재 리서치로 책의 중심 개념 후보는 충분히 좁혀졌다.

다음 단계에서는 새 자료를 무작정 더 모으기보다:

1. source coverage gap audit
2. concept.md 작성
3. scope.md 작성
4. terminology / boundary table
5. chapter candidate clustering

순으로 넘어갈 수 있다.

추가 리서치가 필요한 세부 영역:

- memory lineage / selective repair implementation
- Agent event schema 실제 구현 비교
- identity propagation across MCP/A2A
- policy risk scoring formalization
- state reconciliation benchmark
- harness ablation benchmark methodology
