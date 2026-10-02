# Chapter Evidence Map

기준일: 2026-10-02
대상: Phase 7 reviewed manuscript

이 문서는 장 끝의 단순 "주요 근거" 목록을 출판 원고의 claim-level source note로 전환하기 위한 중간 맵이다.

## Evidence Class

~~~text
[O] Official / Protocol
[V] Vendor Engineering / Production Case
[R] Research / Benchmark
[P] Preprint / Emerging Research
[B] Book Synthesis
~~~

규칙:
- [O] protocol fact는 version/date를 함께 기록한다.
- [V] vendor 구현을 업계 표준 architecture로 일반화하지 않는다.
- [R] benchmark/task/environment 범위를 벗어나 일반화하지 않는다.
- [P] 본문에서 preprint임을 명시하고 "제안/관찰/보고" 수준의 동사를 사용한다.
- [B] 외부 표준이 아니라 이 책의 synthesis라고 최초 등장 시 밝힌다.

---

## Part I. Model에서 Agent System으로

### 1장. Model과 Agent는 무엇이 다른가

핵심 claim:
- Model Capability ≠ Agent Capability. [B]
- Agent behavior는 Model 외에도 Tool/Context/Harness/Runtime에 영향을 받는다. [V][R]
- Tool interface 설계가 실제 coding-agent 성능에 영향을 줄 수 있다. [R]

Source:
- [R] SWE-agent / ACI
- [V] OpenAI Agents SDK
- [V] Anthropic Building Effective Agents
- [B] research/synthesis/agent-engineering-reference-model-v0.3.md

주의:
ACI는 SWE-agent의 framing이며 모든 Tool 시스템의 표준명으로 쓰지 않는다.

### 2장. Agent Loop를 설계한다

핵심 claim:
- Agent loop는 observation → decision → action → observation의 반복 구조를 가진다. [R][V]
- Tool proposal과 실제 Side Effect 사이에는 validation/authorization/execution boundary가 필요하다. [B]
- Completion Claim과 Task Completion은 다를 수 있다. [B]

Source:
- [R] ReAct
- [V] OpenAI Running Agents
- [V] Google ADK
- [B] topics/01-agent-loop-runtime.md

### 3장. Harness Engineering

핵심 claim:
- Harness는 Context, Tool, State, Control을 연결하는 execution-control layer다. [B]
- Harness component는 Model/Task distribution에 대한 engineering hypothesis로 취급할 수 있다. [B][V]
- Model upgrade는 기존 scaffold 재검증 trigger가 될 수 있다. [V]

Source:
- [V] Anthropic long-running harness / managed agent material
- [B] topics/04-harness-long-running.md
- [B] topics/22-harness-ablation-and-minimalism.md

주의:
Harness Debt는 이 책의 synthesis다.

---

## Part II. Context와 Capability Interface

### 4장. Context는 저장소가 아니다

핵심 claim:
- Context는 current inference input이며 durable storage와 다르다. [B][V]
- 더 많은 Context가 자동으로 더 좋은 Agent를 만들지는 않는다. [V][R]
- State → Context Projection 구조가 long-running execution에 유용하다. [B]

Source:
- [V] Anthropic Context Engineering
- [V] OpenAI session/memory material
- [B] topics/02-context-state-memory.md
- [B] topics/09-state-memory-taxonomy.md

### 5장. Tool은 Agent-Computer Interface다

핵심 claim:
- Raw API와 Agent-facing Tool interface는 같은 설계 문제가 아니다. [R][B]
- Tool schema/name/result contract가 Agent의 action space에 영향을 준다. [R][V]
- Tool result는 trusted instruction이 아니라 external observation일 수 있다. [B][V]

Source:
- [R] SWE-agent ACI
- [V] Anthropic Tool Engineering
- [B] topics/03-tools-protocols.md

### 6장. MCP와 Capability Boundary

핵심 claim:
- MCP는 Agent와 capability/context provider 사이의 protocol boundary다. [O]
- MCP ≠ Agent Harness. [B]
- 2026-07-28 base revision은 stateless core를 사용한다. [O]
- Tasks는 2026-10-02 기준 별도 Draft extension이다. [O]

Source:
- [O] MCP 2026-07-28 base specification
- [O] MCP Tasks extension draft
- [B] topics/12-mcp-a2a-task-boundary.md

Freshness:
- review/freshness/mcp-2026-10-02.md

---

## Part III. Durable State와 Long-running Execution

### 7장. Session, Workspace, Goal, Memory를 분리한다

핵심 claim:
- Session / Run / Workspace / Goal / Artifact / Memory는 lifecycle과 authority가 다르다. [B][V]
- Memory는 execution recovery state와 구분하는 편이 안전하다. [B]

Source:
- [V] OpenAI Sessions / Goals / Memory
- [V] AWS AgentCore Runtime
- [V] Google ADK Session/Event model
- [B] topics/09-state-memory-taxonomy.md

### 8장. Agent State Plane

핵심 claim:
- Agent execution continuity를 Process/Runtime lifetime 밖에서 유지하는 별도 responsibility layer가 필요하다. [B]
- Event History / Goal / Artifact / Approval / Source Version은 대표 responsibility다. [B][V][R]
- Agent State Plane ≠ Factory Control Plane. [B]

Source:
- [R] Temporal Durable Execution concepts
- [V] LangGraph Persistence
- [V] OpenAI Sessions
- [B] synthesis/reference-model-v0.3

주의:
Agent State Plane은 이 책의 핵심 synthesis이며 특정 DB/Event Sourcing 구현을 뜻하지 않는다.

### 9장. 실패 후 이어가는 Agent

핵심 claim:
- Retry ≠ Recovery. [B]
- Replay ≠ Model/Side Effect 재실행. [R][B]
- External mutation에는 idempotency/reconciliation이 필요할 수 있다. [R][B]

Source:
- [R] Temporal replay/durable execution
- [V] Anthropic managed-agent recovery patterns
- [B] topics/18-durable-state-event-log-replay.md

### 10장. Long-running Agent

핵심 claim:
- Long Context ≠ Long-running Execution. [B]
- multi-item state / hidden state / dynamic environment가 long-horizon difficulty를 만든다. [R][P]
- Task-State Horizon은 emerging measurement idea다. [P]

Source:
- [V] Anthropic Long-running Harness
- [P] OSWorld 2.0
- [P] Task-State Horizon

Freshness:
- review/freshness/long-running-2026-10-02.md

### 11장. External State Reconciliation

핵심 claim:
- Refresh ≠ Reconciliation. [B]
- Version Conflict ≠ Decision Conflict. [P]
- selective revalidation은 affected decision condition만 다시 확인하는 접근이다. [P]
- optimistic concurrency / CAS는 stale write를 막는 established software pattern이다. [R]

Source:
- [P] From Version Conflicts to Decision Conflicts
- [P] Task-State Horizon
- [P] AgentRewind
- [P] OSWorld 2.0
- [R] optimistic concurrency / transaction patterns

주의:
Selective Revalidation 연구는 controlled feasibility이며 production generality를 입증한 것으로 표현하지 않는다.

---

## Part IV. Memory

### 12장. Agent Memory의 실제 경계

핵심 claim:
- Session ≠ Checkpoint ≠ Memory ≠ Source of Truth. [B]
- Memory retrieval은 relevance뿐 아니라 scope/freshness/authority를 고려해야 한다. [B][V]

Source:
- [V] OpenAI Sessions / Memory
- [B] topics/02-context-state-memory.md
- [B] topics/09-state-memory-taxonomy.md

### 13장. Memory Write는 Side Effect다

핵심 claim:
- Persistent Memory Write는 future behavior에 영향을 주는 privileged Side Effect로 볼 수 있다. [B][P][V]
- memory poisoning은 session을 넘어 지속될 수 있다. [P][V]
- write-time filtering만으로 compositional/dormant attack을 충분히 막기 어려울 수 있다. [P]

Source:
- [V] Microsoft Guarding AI Memory
- [P] MPBench / MemSecBench / MemPoison / MemSentry
- [B] topics/17-memory-security-write-policy.md

주의:
Memory Write Gate와 Accept/Review/Quarantine은 이 책의 policy synthesis다.

Freshness:
- review/freshness/security-2026-10-02.md

---

## Part V. Identity, Credential, Runtime, Policy

### 14장. Agent Identity와 Delegation

핵심 claim:
- User / Application / Agent / Workload / Tool / Resource identity는 구분할 수 있다. [B][V]
- Delegated Access와 Autonomous Access는 credential/authority model이 다르다. [V]
- Discovery ≠ Authentication ≠ Authorization ≠ Approval. [B][O]

Source:
- [V] Microsoft Entra Agent ID
- [V] Microsoft Agent OBO
- [V] AWS AgentCore Identity
- [O] A2A authorization model

주의:
Entra의 special service principal model은 Microsoft 구현이다.

### 15장. Credential을 Agent에서 분리한다

핵심 claim:
- Standing broad credential을 Agent Runtime에 직접 노출하면 blast radius가 커질 수 있다. [B][V]
- short-lived/delegated/workload credential과 gateway injection은 위험을 줄이는 설계 패턴이다. [V]
- Sandbox ≠ Credential Scope. [B]

Source:
- [V] Microsoft OBO
- [V] AWS AgentCore Identity
- [V] NVIDIA OpenShell
- [B] topics/19-delegated-agent-identity-zero-trust.md

### 16장. Sandbox와 Containment

핵심 claim:
- Containment는 Agent가 도달 가능한 filesystem/process/network/runtime 범위를 제한한다. [B][V]
- OS sandbox / container / userspace kernel / microVM은 절대적 단일 ranking이 아니라 trade-off다. [V]
- Disposable Runtime + Durable State는 recovery 구조와 결합할 수 있다. [B]

Source:
- [V] Claude Code Sandboxing
- [V] gVisor
- [V] Firecracker
- [V] AWS AgentCore Runtime
- [V] NVIDIA OpenShell

### 17장. Risk-adaptive Policy

핵심 claim:
- 모든 Action의 Risk가 같지 않으며 control profile을 다르게 적용할 수 있다. [B][V]
- 모든 Action을 Human Review로 보내면 reviewer fatigue가 생길 수 있다. [V]
- authoritative risk classification은 deterministic/external policy와 결합하는 편이 안전하다. [V][B]

Source:
- [V] AWS Agentic AI Lens
- [V] AWS Cedar multi-agent authorization
- [V] OpenShell Policy
- [V] Claude Code Auto Mode
- [B] targeted/17-risk-adaptive-policy.md

주의:
R0~R4는 illustrative synthesis다.

---

## Part VI. Trace, Eval, Improvement

### 18장. Trace 없이는 Agent를 디버깅할 수 없다

핵심 claim:
- final output만으로 Model/Tool/State/Policy/Runtime failure를 구분하기 어렵다. [B][V]
- Trace는 execution path와 causation을 재구성하는 관찰 data다. [B][V]
- Event History와 Observability Trace는 목적이 다를 수 있다. [B]

Source:
- [V] OpenAI Trace Grading / Agent Evals
- [B] topics/06-evaluation-observability.md

### 19장. Agent를 어떻게 평가할 것인가

핵심 claim:
- Agent Eval은 Output뿐 아니라 Trajectory / Outcome / Reliability / Security를 볼 수 있다. [V][R]
- repeated reliability와 infrastructure noise를 고려해야 한다. [R][V]
- benchmark result는 Model 단독 점수가 아니라 system result로 해석해야 한다. [B]

Source:
- [V] OpenAI Agent Evals
- [V] Anthropic Agent Evals / Infrastructure Noise
- [R/P] OSWorld / OSWorld 2.0
- [R] tau / tau2-bench
- [B] topics/16-benchmark-versioning-measurement.md

### 20장. Eval을 CI로 만든다

핵심 claim:
- production failure를 reusable regression case로 승격할 수 있다. [B][V]
- PR / nightly / release / shadow / canary는 cost에 따라 eval cadence를 나누는 패턴이다. [B][V]
- AgentVersion은 reproducible comparison을 위한 book synthesis다. [B]

Source:
- [V] OpenAI Agent Improvement Loop / Macro Evals
- [B] topics/15-eval-ci-regression.md

### 21장. Harness Ablation과 Debt

핵심 claim:
- Harness component는 engineering hypothesis로 다룰 수 있다. [B]
- single-run ablation 결과는 run-to-run variance 때문에 과해석하면 안 된다. [V]
- Model upgrade 시 marginal component value를 다시 측정할 수 있다. [B][V]

Source:
- [V] Anthropic Automated Alignment Researchers harness ablation
- [V] Anthropic Harness Design / Managed Agents
- [B] topics/22-harness-ablation-and-minimalism.md
- [B] targeted/21-harness-ablation.md

주의:
Harness Debt는 book synthesis다.

---

## Part VII. Multi-Agent와 Production Boundary

### 22장. Single-Agent First

핵심 claim:
- Multi-Agent는 complexity를 제거하지 않고 context/ownership/permission/coordination boundary를 추가한다. [B][V]
- context isolation / permission isolation / independent review / parallelism이 명확할 때 분리 가치가 있다. [B][V]

Source:
- [V] Anthropic Building Effective Agents
- [B] topics/07-multi-agent-interoperability.md

### 23장. Agent-as-Tool과 Handoff

핵심 claim:
- Manager ownership 유지와 ownership transfer는 서로 다른 collaboration pattern이다. [B][V]
- Handoff는 Context뿐 아니라 State/Authorization boundary를 다시 평가할 수 있다. [B]

Source:
- [V] OpenAI Agents SDK
- [V] Google ADK
- [B] topics/07-multi-agent-interoperability.md

주의:
Agent-as-Tool / Handoff의 정확한 제품 semantics보다 ownership 차이에 집중한다.

### 24장. A2A와 Remote Agent

핵심 claim:
- A2A는 independent Agent System 사이의 interoperability protocol이다. [O]
- 2026-10-02 기준 latest explicitly published version은 0.3.0이다. [O]
- A2A Task ≠ MCP Task ≠ Factory Task. [B]
- Agent Card discovery ≠ Authorization. [O][B]

Source:
- [O] A2A 0.3.0 specification
- [B] topics/12-mcp-a2a-task-boundary.md

Freshness:
- review/freshness/a2a-2026-10-02.md

### 25장. Minimum Viable Production Agent

핵심 claim:
- Agent는 모든 advanced component를 처음부터 가질 필요가 없다. [B]
- Boundary → Verification → Observability → Autonomy 순서로 생각하는 것이 이 책의 synthesis다. [B]
- Agent State Plane ≠ Factory Control Plane. [B]

Source:
- [B] planning/concept.md
- [B] planning/scope.md
- [B] synthesis/reference-model-v0.3
- [B] 전체 research synthesis

---

# Publication-time Evidence Gate

출간 원고에서 다음을 확인한다.

## Protocol Facts
- MCP base revision / Tasks lifecycle
- A2A stable version / TaskState
- vendor SDK feature names

## Preprints
- OSWorld 2.0
- Task-State Horizon
- Selective Revalidation
- AgentRewind
- memory-security papers

확인:
- newer revision
- peer review / venue status
- benchmark correction
- implementation availability

## Vendor Engineering
- Entra Agent ID lifecycle
- Claude Code sandbox implementation
- AWS Agentic AI Lens wording
- OpenShell policy / credential behavior
- OpenAI / Anthropic agent eval product naming

## Book Synthesis
다음은 citation으로 "증명"하려 하지 않는다.

- Agent State Plane
- Harness Debt
- Memory Write Gate
- AgentVersion
- R0~R4 control profile
- Agent-as-Tool / Handoff ownership distinction

대신 여러 source family에서 반복되는 responsibility를 종합한 저자의 framework임을 명시한다.

# Status

~~~text
Broad Research              완료
Targeted Research           완료
Draft                       완료
Structural Review           완료
Line Review                 완료
Terminology / Dedup         완료
Evidence Map v2             완료
Claim-level Source Notes    Manuscript Assembly에서 반영
~~~
