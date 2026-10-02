# Chapter Candidate Clusters

기준일: 2026-10-02

이 문서는 최종 TOC가 아니다.

현재 Concept / Scope / Research를 독자가 이해하기 좋은 학습 순서로 묶기 위한 chapter candidate다.

## 전체 서사

책의 흐름 후보:

~~~text
Model
→ Agent
→ Context
→ Tools
→ Harness
→ State
→ Long-running
→ Identity / Security
→ Evaluation
→ Multi-Agent
→ Production Readiness
~~~

핵심은 기능 목록이 아니라 Agent가 점점 더 현실 세계의 side effect와 긴 시간을 다루도록 확장하는 순서다.

# Cluster A. Model에서 Agent로

## 후보 장 A1. Model과 Agent는 무엇이 다른가

핵심:
- Model Capability vs Agent Capability
- prompt wrapper의 한계
- observation/action loop

## 후보 장 A2. Agent Loop를 설계한다

핵심:
- model → tool → observation
- stop condition
- failure
- budget
- interruption

## 후보 장 A3. Harness Engineering

핵심:
- harness responsibility
- framework와 harness의 차이
- minimal agent
- harness as software

# Cluster B. Context와 Tool

## 후보 장 B1. Context는 저장소가 아니다

핵심:
- finite attention
- projection
- progressive context
- compaction

## 후보 장 B2. Tool은 Agent-Computer Interface다

핵심:
- tool boundary
- schema
- result
- error
- side effect

## 후보 장 B3. MCP와 Capability Boundary

핵심:
- MCP의 위치
- discovery
- authorization
- Tasks extension

# Cluster C. Agent State Plane

## 후보 장 C1. Session, Workspace, Goal, Memory를 분리한다

책의 핵심 taxonomy.

## 후보 장 C2. Agent State Plane

핵심:
- event history
- checkpoint
- artifact
- approval
- source version

## 후보 장 C3. 실패 후 이어가는 Agent

핵심:
- pause/resume
- recovery
- replay
- idempotency

## 후보 장 C4. Long-running Agent

핵심:
- milestone
- phase budget
- horizon
- dynamic environment
- external state

## 후보 장 C5. Reconciliation과 Source of Truth

핵심:
- refresh
- version
- optimistic concurrency
- stale state
- final verification

# Cluster D. Memory

## 후보 장 D1. Agent Memory의 실제 경계

핵심:
- session vs memory
- memory purpose
- scope
- freshness

## 후보 장 D2. Memory Write는 Side Effect다

핵심:
- provenance
- write gate
- poisoning
- quarantine
- repair

Memory를 한 장으로 압축할지 두 장으로 나눌지는 분량 보고 결정.

# Cluster E. Identity, Policy, Runtime

## 후보 장 E1. Agent Identity와 Delegation

핵심:
- user/app/agent/tool/resource
- delegated/autonomous
- actor chain

## 후보 장 E2. Credential을 Agent에게 주지 않는 법

핵심:
- token exchange
- short-lived credential
- gateway injection
- least privilege

E1과 합칠 가능성 있음.

## 후보 장 E3. Sandbox와 Containment

핵심:
- filesystem/network/process
- container/gVisor/microVM
- runtime lifecycle

## 후보 장 E4. Risk-adaptive Policy

핵심:
- task risk
- approval
- deterministic policy
- policy expansion
- fail closed

# Cluster F. Eval과 Improvement

## 후보 장 F1. Trace 없이는 Agent를 디버깅할 수 없다

핵심:
- trace model
- model/tool/state/policy event
- audit vs debugging

## 후보 장 F2. Agent를 어떻게 평가할 것인가

핵심:
- output
- trajectory
- outcome
- reliability
- infra noise

## 후보 장 F3. Eval을 CI로 만든다

핵심:
- failure → regression
- capability/security dataset
- release gate
- shadow/canary

## 후보 장 F4. Harness Ablation과 Debt

핵심:
- minimal baseline
- marginal value
- model upgrade audit
- scaffold removal

# Cluster G. Multi-Agent와 경계 확장

## 후보 장 G1. Single-Agent First

핵심:
- multi-agent가 해결하지 못하는 것
- 언제 분리할 것인가

## 후보 장 G2. Agent-as-Tool과 Handoff

핵심:
- manager
- specialist
- ownership
- context transfer

## 후보 장 G3. A2A와 Remote Agent

핵심:
- Agent Card
- Task
- Artifact
- authorization
- MCP와의 차이

# Cluster H. Production Agent의 최소 구조

## 후보 장 H1. Minimum Viable Production Agent

~~~text
Model
+ Instruction
+ Small Tool Surface
+ Controlled Runtime
+ Trace
+ Deterministic Verification
~~~

에서 시작.

## 후보 장 H2. Agent Capability Maturity

확장 순서:

~~~text
Minimal Agent
→ Tool Contract
→ Runtime
→ Trace
→ Eval
→ Durable State
→ Identity/Policy
→ Memory
→ Long-running
→ Multi-Agent
~~~

## 후보 장 H3. Agent Engineering과 Software Factory의 경계

핵심:
- Agent State Plane
- Factory Control Plane
- execution continuity
- work-system continuity

이 장은 Epilogue 또는 마지막 장으로 이동 가능.

# 예상 Part 구조 후보

현재로서는 다음 7부가 가장 자연스럽다.

~~~text
Part I   Model에서 Agent로
Part II  Context와 Tool을 설계한다
Part III Agent State Plane
Part IV  Memory와 Long-running
Part V   Identity, Security, Runtime
Part VI  Trace, Eval, Harness Improvement
Part VII Multi-Agent와 Production Boundary
~~~

총 장수 후보: 18~22장.

아직 TOC로 확정하지 않는다.

## TOC 설계 전 해결할 것

- Memory를 1장/2장 중 어느 정도로 둘지
- Identity와 Credential을 합칠지
- MCP와 A2A를 각 Part에서 분산 설명할지 별도 protocol 장을 둘지
- Sandbox 기술 비교를 본문/부록 어디까지 넣을지
- 마지막 Part에서 software-factory-book 중복을 얼마나 줄일지
