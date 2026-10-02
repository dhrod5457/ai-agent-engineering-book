# Table of Contents

기준일: 2026-10-02
상태: v0.1

# AI Agent Engineering

부제 후보:

**LLM을 실제 작업 가능한 Agent로 만드는 설계 원칙**

## Part I. Model에서 Agent로

### 1장. Model과 Agent는 무엇이 다른가
- Model Capability와 Agent Capability
- Prompt wrapper의 한계
- Agent를 실행 시스템으로 보기
- 책 전체 Reference Model

### 2장. Agent Loop를 설계한다
- Input → Context → Model → Action → Observation
- Stop Condition
- Retry
- Budget
- Interruption / Resume
- Failure Classification

### 3장. Harness Engineering
- Harness란 무엇인가
- Framework와 Harness의 차이
- Agent Definition과 Runtime의 경계
- Minimal Harness
- Harness를 versioned software로 보기

## Part II. Context와 Tool을 설계한다

### 4장. Context는 저장소가 아니다
- Context as finite attention
- Context Projection
- Progressive Context
- Retrieval
- Tool Schema Selection
- Compaction과 한계
- Context Pollution

### 5장. Tool은 Agent-Computer Interface다
- Tool vs Raw API
- Capability Boundary
- Tool Name / Description / Schema
- Result Contract
- Error Model
- Side Effect
- Tool Output Trust

### 6장. MCP와 Capability Boundary
- MCP의 위치
- Tool / Resource / Prompt
- Stateless Core
- Tasks Extension
- Capability Discovery
- Authorization과의 경계

## Part III. Agent State Plane

### 7장. Session, Workspace, Goal, Memory를 분리한다
- Inference Context
- Conversation / Session
- Run State
- Workspace
- Goal
- Artifact
- Memory
- External Source of Truth

### 8장. Agent State Plane
- 왜 별도 State Plane이 필요한가
- Event History
- Checkpoint / Snapshot
- Goal / Progress
- Artifact Index
- Approval State
- External Source Version
- Context Projection

### 9장. 실패 후 이어가는 Agent
- Pause / Resume
- Crash Recovery
- Replay
- Side-effect 재실행 방지
- Idempotency
- Event Schema
- Snapshot

### 10장. Long-running Agent
- Context Window보다 긴 작업
- Milestone
- Phase Budget
- Progress State
- Hidden State
- Multi-item State Tracking
- Horizon Exhaustion

### 11장. External State Reconciliation
- Working State vs Source of Truth
- Refresh Trigger
- Source Registry
- Authority Ranking
- Version / ETag
- Optimistic Concurrency
- Re-plan
- Final Verification

## Part IV. Memory를 안전하게 사용한다

### 12장. Agent Memory의 실제 경계
- Session과 Memory
- Working State와 Memory
- Memory Scope
- Freshness
- Retrieval
- Memory를 Source of Truth로 쓰지 않는 이유

### 13장. Memory Write는 Side Effect다
- Memory Candidate
- Provenance
- Scope
- Write Gate
- Poisoning
- Compositional Attack
- Quarantine
- Forget / Repair
- Memory Audit

## Part V. Identity, Security, Runtime

### 14장. Agent Identity와 Delegation
- Human / Application / Agent / Tool / Resource Identity
- Delegated vs Autonomous
- Actor Chain
- Capability Discovery vs Authentication vs Authorization
- Agent Lifecycle

### 15장. Credential을 Agent에서 분리한다
- Standing Credential의 위험
- Short-lived Token
- Credential Broker
- Gateway Injection
- Scope
- Audit
- Tool Identity

### 16장. Sandbox와 Containment
- Sandbox가 필요한 이유
- Filesystem / Network / Process
- OS Sandbox
- gVisor
- Container
- MicroVM
- Runtime State는 Durable State가 아니다

### 17장. Risk-adaptive Policy
- R0~R4 illustrative risk model
- Authorization / Approval / Containment
- Policy as Code
- Fail Closed
- Policy Expansion
- Agent proposes, Control Plane approves

## Part VI. Agent를 관찰하고 개선한다

### 18장. Trace 없이는 Agent를 디버깅할 수 없다
- Model Trace
- Tool Trace
- State Transition
- Approval
- Handoff
- Runtime Failure
- Audit vs Debugging
- Cost / Latency

### 19장. Agent를 어떻게 평가할 것인가
- Output Eval
- Trajectory Eval
- Tool Routing
- State Handling
- Security Eval
- Outcome Eval
- Repeated Reliability
- Infrastructure Noise
- Benchmark Versioning

### 20장. Eval을 CI로 만든다
- Production Failure → Regression
- Capability Dataset
- Security Dataset
- Long-horizon Dataset
- PR / Nightly / Release Gate
- Shadow / Canary
- Model Upgrade Audit

### 21장. Harness Ablation과 Debt
- Minimal Baseline
- Component Inventory
- Marginal Value
- Interaction Effect
- Model Upgrade
- Scaffold Debt
- Load-bearing Component

## Part VII. Multi-Agent와 Production Boundary

### 22장. Single-Agent First
- Multi-Agent가 해결하지 못하는 문제
- Agent 수보다 경계가 먼저인 이유
- 언제 specialist가 필요한가
- Context Isolation
- Permission Isolation
- Parallelism

### 23장. Agent-as-Tool과 Handoff
- Manager Pattern
- Agent-as-Tool
- Ownership Handoff
- Context Transfer
- Authority Transfer
- Independent Verifier

### 24장. A2A와 Remote Agent
- Agent Card
- Message
- Task
- Artifact
- Lifecycle
- Authorization
- MCP와의 차이
- Remote Agent vs Local Subagent

### 25장. Minimum Viable Production Agent
- Minimal Agent
- Capability Maturity
- Control before Autonomy
- Verification before Scale
- Agent State Plane과 Software Factory Control Plane의 경계

# Epilogue. Agent를 더 똑똑하게 만드는 것보다 시스템을 더 믿을 수 있게 만든다

- Model Capability는 계속 변한다
- Harness도 함께 변한다
- Agent Engineering의 장기 목표
- Software Factory로 이어지는 경계

# Appendix 후보

## Appendix A. Agent Engineering Checklist
- Context
- State
- Tool
- Runtime
- Identity
- Security
- Eval

## Appendix B. Agent State Event Catalog
- event type 예시
- correlation / causation
- idempotency key

## Appendix C. Risk / Policy Matrix
- illustrative R0~R4
- sandbox / credential / approval mapping

## Appendix D. Eval Case Template
- task
- environment
- tools
- expected outcome
- grader
- repeat count
- risk

## Appendix E. Product / Protocol Reference
- OpenAI Agents SDK
- Claude Code
- Google ADK
- MCP
- A2A
- AgentCore
- OpenShell

# 구조 요약

~~~text
Part I
Model → Agent

Part II
Context → Tool

Part III
State → Recovery → Long-running

Part IV
Memory

Part V
Identity → Security → Runtime

Part VI
Trace → Eval → Harness Improvement

Part VII
Multi-Agent → Production Boundary
~~~

총 25장 + Epilogue.

# 현재 판단

25장은 다소 많지만 각 장의 책임 경계가 분명하다.

초고 단계에서 다음 압축 후보를 검토한다.

- 14장 + 15장 병합 가능
- 18장 + 19장 일부 병합 가능
- 22장 + 23장 병합 가능

압축 시 22~23장 수준까지 줄일 수 있다.
