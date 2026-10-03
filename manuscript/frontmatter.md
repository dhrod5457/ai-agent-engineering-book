# AI Agent Engineering

## LLM을 실제 작업 가능한 Agent로 만드는 설계 원칙

상태: Manuscript Assembly v0.1
기준일: 2026-10-02

## 이 책의 질문

이 책은 "어떤 Agent Framework를 쓸 것인가"보다 다음 질문을 다룬다.

~~~text
Model의 판단을 실제 행동으로 바꿀 때
어떤 책임을 어디에 둘 것인가?
~~~

핵심 범위:

- Agent Loop와 Harness
- Context와 Tool Interface
- Durable State와 Recovery
- Long-running Execution
- Memory와 Memory Security
- Identity / Credential / Sandbox / Policy
- Trace / Eval / Harness Improvement
- Multi-Agent와 Remote Agent Boundary

## 핵심 경계

~~~text
Model ≠ Agent
Context ≠ Durable State
Session ≠ Goal
Memory ≠ Source of Truth
Harness ≠ Runtime
Sandbox ≠ Authorization
Completion Claim ≠ Completion Authority
MCP Task ≠ A2A Task ≠ Factory Task
Agent State Plane ≠ Factory Control Plane
~~~

## Source Note

원고의 `[S-*]`는 외부 Source ID, `[B-*]`는 이 책의 synthesis ID다.

정의:
- planning/source-catalog.md
- planning/source-note-conventions.md

Protocol, product, preprint처럼 변경 가능성이 높은 사실은 `review/freshness/`의 publication-time gate에서 다시 검증한다.
