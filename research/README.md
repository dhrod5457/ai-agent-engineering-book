# Research

기준일: 2026-10-02

이 디렉터리는 AI Agent Engineering 책의 근거층이다.

목표는 Agent Framework 기능을 나열하는 것이 아니라 다음 경계를 검증하는 것이다.

> Model / Instruction / Context / Tool / Harness / Runtime / State / Identity / Security / Eval / Orchestration은 각각 무엇을 책임하고 어디서 분리되어야 하는가?

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
- synthesis/agent-engineering-reference-model.md: 1차 reference model v0.1
- synthesis/agent-engineering-reference-model-v0.2.md: 2차 조사 반영 reference model
- meta/methodology.md: 조사와 근거 관리 방법

## 현재 결론

Agent를 단순히 LLM + Tool로 정의하는 것은 부족하다.

현재 가장 설명력이 높은 구조는 다음과 같다.

~~~text
Identity / Delegation
        ↓
Agent Definition
        ↓
Context Engine
        ↓
Agent Harness
        ↔ State Plane
        ↓
Tool / Capability Gateway
        ↓
Execution Runtime
        ↓
External World

Cross-cutting:
Trace / Audit / Eval / Security Policy
~~~

특히 2차 조사에서 State를 하나의 저장소로 보면 안 된다는 점이 명확해졌다.

~~~text
Context
≠ Session
≠ Workspace
≠ Goal
≠ Artifact
≠ Long-term Memory
≠ External Source of Truth
~~~

또한 long-horizon Agent에서는 단순 context 확대보다 state refresh, reconciliation, milestone, verification reserve가 중요하다.

Multi-agent는 여전히 선택적 상위 구조로 본다. Single-agent의 tool boundary, state, runtime, identity, eval이 먼저 성립해야 한다.
