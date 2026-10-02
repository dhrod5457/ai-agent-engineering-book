# Agent Engineering Reference Model v0.1

기준일: 2026-10-02

이 문서는 1차 리서치를 바탕으로 만든 초기 종합 모델이다. 아직 책의 확정 정의가 아니다.

## 1. Agent Engineering의 대상

초기 정의:

> AI Agent Engineering은 Model을 실제 환경에서 반복적으로 판단하고 행동하는 실행 주체로 만들기 위해 Context, Tool, Harness, Runtime, State, Security Boundary, Observability, Evaluation을 설계하는 소프트웨어 엔지니어링 활동이다.

핵심은 Agent Prompt 작성보다 넓고 Software Factory 전체 운영보다 좁다.

## 2. Reference Architecture

~~~text
User / Upstream System
          │
          ▼
┌──────────────────────────┐
│ Agent Definition         │
│ - Model                  │
│ - Instructions           │
│ - Output Contract        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Context Engine           │
│ - History projection     │
│ - Retrieval              │
│ - Tool schemas           │
│ - State summary          │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Agent Harness            │
│ - Loop                   │
│ - Stop condition         │
│ - Retry                  │
│ - Handoff                │
│ - Approval interruption  │
└───────┬──────────┬───────┘
        │          │
        │          └──────────────┐
        ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│ Tool Gateway     │      │ State / Session  │
│ - Schema         │      │ - Event log      │
│ - Permission     │      │ - Checkpoint     │
│ - Validation     │      │ - Artifacts      │
│ - Result filter  │      │ - Memory refs    │
└────────┬─────────┘      └──────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Execution Runtime        │
│ - Sandbox / VM           │
│ - Filesystem             │
│ - Network                │
│ - Credentials            │
│ - Browser / Shell        │
└────────────┬─────────────┘
             │
             ▼
        External World

Cross-cutting:
- Guardrails / Approval
- Trace / Audit
- Metrics / Cost
- Eval / Regression
~~~

## 3. Component Boundary

### Model

책에서 Model은 inference engine으로 한정한다.

책임:
- next decision
- structured output
- tool call proposal
- language/reasoning

책임 아님:
- durable state ownership
- credential enforcement
- process isolation
- actual side effect authorization

### Instruction

Agent의 role, constraints, behavior guidance.

상세한 파일 작성법은 ai-instruction-engineering-book으로 넘긴다.

이 책에서는 Instruction이 Harness 안에서 어떻게 load되고 context에 배치되는지만 다룬다.

### Context Engine

현재 inference에 어떤 information을 넣을지 결정한다.

핵심:
- relevance
- freshness
- provenance
- token budget
- compaction
- progressive retrieval

### Harness

Model을 반복 실행 가능한 Agent로 만드는 control logic.

핵심:
- loop
- tool dispatch
- retry
- stop
- interruption/resume
- handoff
- context refresh

### Tool Gateway

Model proposal을 실제 capability 호출로 연결한다.

핵심:
- schema
- validation
- permission
- approval
- result normalization
- output filtering

### Runtime

실제 side effect가 발생하는 환경.

핵심:
- OS/process
- filesystem
- network
- sandbox/VM
- credential
- compute resource

### State / Session

Process와 context가 사라져도 이어져야 하는 상태.

핵심:
- event
- checkpoint
- current progress
- artifact reference
- approval pending state

### Memory

장기적으로 재사용할 정보.

State와 분리한다.

Memory는 optional capability이며 기본값으로 무제한 축적하지 않는다.

### Observability

Agent가 무엇을 했는지 재구성한다.

- model call
- tool call
- handoff
- approval
- runtime error
- timing
- cost

### Eval

Agent System 변경이 실제 능력과 신뢰성을 개선했는지 측정한다.

평가 단위:
- output
- trajectory
- outcome
- reliability
- security
- cost/latency

## 4. 중요한 경계식

~~~text
Model Capability
≠ Agent Capability

Agent
≠ Prompt + Model

Context
≠ Memory

Tool Protocol
≠ Agent Harness

Harness
≠ Runtime

Agent Orchestration
≠ Software Factory
~~~

## 5. Agent Capability 식

현재 연구 가설:

~~~text
Agent Capability
≈ f(
  Model,
  Instruction,
  Context,
  Tool Interface,
  Harness,
  Runtime,
  State,
  Security Boundary,
  Evaluation Feedback
)
~~~

Agent benchmark에서 runtime resource와 harness가 결과를 바꿀 수 있으므로 Model benchmark 하나로 Agent를 평가하지 않는다.

## 6. Reliability 우선순위

초기 권고 순서:

~~~text
Single Agent
→ Clear Tool Contract
→ Reproducible Runtime
→ Trace
→ Eval
→ State / Recovery
→ Security Boundary
→ Long-running
→ Multi-agent
~~~

Multi-agent는 앞 단계의 문제를 해결하지 않는다. 오히려 failure surface를 늘릴 수 있다.

## 7. 다른 책과의 경계

### ai-instruction-engineering-book
- CLAUDE.md
- AGENTS.md
- Rules
- Skills
- Hooks
- instruction eval

### 이 책
- Agent loop
- context/state
- tool interface
- harness
- runtime
- security
- agent eval
- multi-agent patterns

### cloud-agent-book
- local/cloud routing
- prepared cloud environment
- runner
- Git handoff
- cloud cost / resource

### software-factory-book
- durable task
- scheduler
- worker fleet
- acceptance
- recovery at work-system level
- delivery
- feedback loop

## 8. 다음 리서치 우선순위

1. Memory architecture와 state taxonomy
2. Tool design eval 실제 사례
3. Long-running checkpoint/recovery 구현 비교
4. Agent identity / authorization
5. Sandbox / network containment 구현 비교
6. MCP 2026-07-28 Tasks와 A2A Task 경계
7. 최신 tau 계열 benchmark 변화
8. OSWorld 2.0 / computer-use agent architecture
9. Coding agent harness 비교
10. Eval corpus versioning과 CI 통합
