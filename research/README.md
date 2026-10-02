# Research

기준일: 2026-10-02

이 디렉터리는 AI Agent Engineering 책의 근거층이다.

목표는 Agent Framework 기능을 나열하는 것이 아니라 다음 경계를 검증하는 것이다.

> Model / Instruction / Context / Tool / Harness / Runtime / State / Security / Eval / Orchestration은 각각 무엇을 책임하고 어디서 분리되어야 하는가?

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
- synthesis/agent-engineering-reference-model.md: 현재 근거를 종합한 초기 reference model
- meta/methodology.md: 조사와 근거 관리 방법

## 1차 결론

현재 자료를 교차하면 Agent를 단순히 “LLM + Tool”로 정의하는 것은 부족하다.

실제 Agent 시스템에는 최소한 다음 관심사가 반복해서 등장한다.

1. Model inference
2. Instruction
3. Context assembly
4. Agent loop
5. Tool contract
6. Execution runtime
7. Session / state
8. Permission / approval / containment
9. Trace / observability
10. Evaluation

Multi-agent orchestration은 그 위에 올라가는 선택적 계층으로 본다.

이 연구에서는 처음부터 Multi-agent를 전제하지 않는다. Single-agent의 loop, tool boundary, state, runtime, eval이 먼저 성립해야 한다.
