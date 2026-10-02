# Agent Engineering Reference Model v0.2

기준일: 2026-10-02

이 문서는 2차 리서치 결과를 반영한 종합 모델이다.

## 1. 정의

> AI Agent Engineering은 Model을 실제 환경에서 반복적으로 판단하고 행동하는 실행 주체로 만들기 위해 Context, State, Tool Interface, Harness, Runtime, Identity, Security Boundary, Observability, Evaluation을 설계하는 소프트웨어 엔지니어링 활동이다.

핵심 경계:

~~~text
Prompt Engineering
< Agent Engineering
< Software Factory Engineering
~~~

## 2. Reference Architecture

~~~text
User / Upstream System
          │
          ▼
┌─────────────────────────────┐
│ Identity / Delegation       │
│ - user identity             │
│ - workload identity         │
│ - consent / scopes          │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ Agent Definition            │
│ - model                     │
│ - instruction               │
│ - output contract           │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ Context Engine              │
│ - history projection        │
│ - retrieval                 │
│ - tool schemas              │
│ - state projection          │
│ - compaction                │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ Agent Harness               │
│ - loop                      │
│ - goal / stop               │
│ - retry                     │
│ - handoff                   │
│ - interruption / resume     │
│ - budget                    │
│ - refresh / reconcile       │
└──────┬───────────┬──────────┘
       │           │
       │           ▼
       │   ┌──────────────────────────┐
       │   │ State Plane              │
       │   │ - session                │
       │   │ - run                    │
       │   │ - workspace refs         │
       │   │ - goal / progress        │
       │   │ - artifact refs          │
       │   │ - long-term memory       │
       │   └──────────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Tool / Capability Gateway   │
│ - discovery                 │
│ - schema                    │
│ - authz                     │
│ - validation                │
│ - approval                  │
│ - credential injection      │
│ - result filtering          │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ Execution Runtime           │
│ - sandbox / microVM         │
│ - filesystem               │
│ - network                   │
│ - browser / shell           │
│ - compute                   │
└────────────┬────────────────┘
             │
             ▼
        External World

Cross-cutting:
- Trace / Audit
- Eval / Regression
- Cost / Latency
- Security Policy
~~~

## 3. State Plane 세분화

v0.1의 Session / State를 다음으로 분해한다.

~~~text
Inference Context
Conversation / Session State
Run State
Workspace State
Goal / Task State
Artifact State
Long-term Memory
External Source of Truth
~~~

핵심 원칙:

- Context는 현재 inference projection이다.
- Session은 대화/turn continuity다.
- Workspace는 runtime state다.
- Goal은 completion contract다.
- Artifact는 결과물이다.
- Memory는 미래 run을 위한 재사용 가능한 lesson이다.
- External Source of Truth는 Agent가 소유하지 않는다.

따라서:

~~~text
Session
≠ Workspace
≠ Goal
≠ Memory
≠ Source of Truth
~~~

## 4. Long-horizon Agent의 추가 책임

OSWorld 2.0과 장기 coding harness 사례를 반영하면 장기 Agent에는 단순 loop보다 다음이 필요하다.

~~~text
Goal
→ Milestone
→ Working State
→ Action
→ Refresh External State
→ Reconcile
→ Checkpoint
→ Verify Outcome
↺
~~~

장기 실패의 주요 원인 후보:

- stale internal state
- hidden state 미복구
- multi-item omission
- dynamic update 미반영
- search/preparation이 horizon을 소비
- artifact existence를 correctness로 착각
- 불확실한 상태에서 질문하지 않고 추정

## 5. Security Model

Agent security는 네 층으로 나눈다.

~~~text
Identity
Who is acting?

Authorization
What may this principal do?

Containment
What can a compromised agent physically reach?

Approval / Policy
Should this particular action execute now?
~~~

Permission prompt 하나로 이 네 책임을 대체하지 않는다.

Credential은 가능한 한 model context와 sandbox 내부에 직접 노출하지 않고 gateway boundary에서 주입한다.

## 6. Runtime Isolation

격리 방식은 위험과 비용에 따라 선택한다.

~~~text
OS policy / sandbox
→ userspace kernel
→ container + strong policy
→ microVM
→ dedicated VM/host
~~~

강한 isolation도 과도한 credential scope를 해결하지는 못한다.

따라서:

~~~text
Isolation + Least Privilege + Policy + Verification
~~~

조합이 필요하다.

## 7. Protocol Boundary

### MCP

~~~text
Agent ↔ Capability Provider
~~~

2026-07-28부터 stateless core가 기본이며 long-running Tasks는 extension이다.

### A2A

~~~text
Agent System ↔ Independent Agent System
~~~

Task, Message, Artifact, lifecycle을 통해 delegated work를 표현한다.

### 내부 Domain Task

Protocol Task와 내부 work record를 동일시하지 않는다.

~~~text
Factory / Product Task
  ├─ Agent Run
  ├─ MCP Task
  └─ A2A Task
~~~

## 8. Harness를 versioned software로 본다

Harness에는 다음이 포함될 수 있다.

- instruction loading
- context selection
- agent loop
- tool surface
- stop condition
- goal lifecycle
- retry
- compaction
- permission
- handoff
- verification
- trace

강한 model이 출시되면 기존 scaffold가 계속 유효한지 다시 측정한다.

추천:

~~~text
New Model
→ Existing Harness Eval
→ Component Ablation
→ Tool / Prompt Retune
→ Security Regression
→ Long-horizon Regression
→ Promotion
~~~

## 9. Eval CI

Agent system의 모든 변경은 regression 대상이다.

~~~text
Production Failure
→ Reusable Eval
→ Regression Dataset
→ Candidate Change
→ Offline Eval
→ Shadow / Canary
→ Promotion
~~~

평가 단위는 model 이름이 아니라 다음 tuple이다.

~~~text
AgentVersion = (
  model,
  instruction,
  harness,
  tools,
  runtime,
  environment,
  policy,
  memory/config,
  grader
)
~~~

## 10. Benchmark 해석

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

Benchmark도 versioned software다.

task/grader 변경으로 같은 trajectory 점수가 바뀔 수 있으므로 benchmark version, task revision, grader version을 기록한다.

## 11. 현재 핵심 원칙

1. Model Capability와 Agent Capability를 분리한다.
2. Agent는 Prompt + Tool 목록이 아니다.
3. Context, Session, Workspace, Goal, Memory를 분리한다.
4. Tool은 Agent-Computer Interface다.
5. Harness는 versioned software component다.
6. Runtime은 disposable하게 만들 수 있어야 한다.
7. Credential과 model context를 분리한다.
8. Approval보다 containment와 least privilege를 먼저 설계한다.
9. Long-horizon에서는 state refresh와 reconciliation이 핵심이다.
10. Completion은 실제 outcome과 evidence로 판정한다.
11. Multi-agent는 기본값이 아니다.
12. Eval을 CI와 production feedback loop에 연결한다.

## 12. 다음 연구 질문

- State Plane을 event sourcing으로 구현할 때 최소 event schema는 무엇인가.
- memory write 권한과 memory poisoning 방어를 어떻게 설계할 것인가.
- workload identity와 user delegation을 표준 protocol에서 어떻게 전달할 것인가.
- sandbox policy를 task risk에 따라 자동 선택할 수 있는가.
- Agent가 external source refresh 필요성을 어떻게 판단할 것인가.
- long-horizon budget을 phase별로 어떻게 배분할 것인가.
- Harness component ablation을 자동화할 수 있는가.
- Eval dataset drift를 어떻게 감지할 것인가.
