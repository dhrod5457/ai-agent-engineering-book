# Research

기준일: 2026-10-02

이 디렉터리는 AI Agent Engineering 책의 근거층이다.

목표는 Agent Framework 기능을 나열하는 것이 아니라 다음 경계를 검증하는 것이다.

> Model / Instruction / Context / Tool / Harness / Runtime / State / Memory / Identity / Security / Eval / Orchestration은 각각 무엇을 책임하고 어디서 분리되어야 하는가?

## 조사 구조

~~~text
Source
  ↓
Evidence
  ↓
Failure / Constraint
  ↓
Engineering Principle
  ↓
Component Boundary
  ↓
Architecture Pattern
  ↓
Evaluation Method
~~~

## 디렉터리

- catalog/source-catalog.md: 공식 문서, 논문, benchmark 원문 카탈로그
- topics/01-agent-loop-runtime.md: Agent loop와 runtime
- topics/02-context-state-memory.md: context, state, memory
- topics/03-tools-protocols.md: tool design, MCP, A2A
- topics/04-harness-long-running.md: harness와 long-running agent
- topics/05-security-containment.md: sandbox, permission, prompt injection, containment
- topics/06-evaluation-observability.md: trace, eval, regression
- topics/07-multi-agent-interoperability.md: delegation, handoff, multi-agent, interoperability
- topics/08-benchmarks.md: Agent benchmark와 측정 한계
- topics/09-state-memory-taxonomy.md: session, workspace, goal, artifact, memory taxonomy
- topics/10-agent-identity-authorization.md: workload identity, delegation, credential boundary
- topics/11-sandbox-runtime-isolation.md: OS sandbox, gVisor, microVM, OpenShell
- topics/12-mcp-a2a-task-boundary.md: MCP Task, A2A Task, runtime session 경계
- topics/13-long-horizon-computer-use.md: OSWorld 2.0 기반 장기 업무 실패 분석
- topics/14-coding-agent-harness-comparison.md: Claude Code, Codex, SWE-agent 공통 harness 패턴
- topics/15-eval-ci-regression.md: trace → eval → regression → promotion loop
- topics/16-benchmark-versioning-measurement.md: benchmark versioning과 measurement hygiene
- topics/17-memory-security-write-policy.md: memory poisoning, write gate, retrieval security
- topics/18-durable-state-event-log-replay.md: event history, checkpoint, replay, idempotency
- topics/19-delegated-agent-identity-zero-trust.md: agent identity, delegation, actor chain
- topics/20-risk-adaptive-containment-policy.md: task risk별 sandbox/policy와 권한 확장
- topics/21-external-state-reconciliation.md: source refresh, version, reconciliation
- topics/22-harness-ablation-and-minimalism.md: harness ablation, scaffold debt, minimal baseline
- synthesis/agent-engineering-reference-model.md: 1차 reference model v0.1
- synthesis/agent-engineering-reference-model-v0.2.md: 2차 reference model
- synthesis/agent-engineering-reference-model-v0.3.md: 3차 reference model / Agent State Plane
- meta/methodology.md: 조사와 근거 관리 방법

## 현재 결론

3차 조사에서는 **Agent State Plane**이 책의 중심 개념 후보로 구체화됐다.

~~~text
Identity / Delegation
        ↓
Agent Definition
        ↓
Context Engine
        ↓
Agent Harness
        ↔
Agent State Plane
        │
        ├─ Event History
        ├─ Checkpoint / Snapshot
        ├─ Goal / Progress
        ├─ Artifact
        ├─ Approval
        ├─ External Source Version
        └─ Memory Reference
        ↓
Capability / Policy Gateway
        ↓
Execution Runtime
        ↓
External World
~~~

핵심 경계:

~~~text
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

Agent State Plane
≠ Software Factory Control Plane
~~~

Persistent Memory는 자동 write bucket으로 두지 않는다. Memory write를 privileged side effect로 보고 provenance, scope, security, contradiction, lifecycle을 거쳐 Accept / Review / Quarantine한다.

Long-horizon Agent는 internal state만 믿지 않고 irreversible action, resume, handoff, completion 전에 authoritative external source를 refresh/reconcile해야 한다.

Multi-agent는 여전히 선택적 상위 구조다. 먼저 single-agent의 State Plane, identity, policy, runtime, verification이 성립해야 한다.
