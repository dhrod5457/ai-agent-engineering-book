# AI Agent Engineering

LLM을 단순한 응답 모델이 아니라 실제 환경에서 도구를 사용하고 상태를 이어가며 검증 가능한 결과를 만드는 **Agent**로 구성하는 방법을 연구하고 정리하는 책 프로젝트입니다.

## 중심 질문

> LLM을 실제 작업 가능한 Agent로 만들기 위해 Model, Instruction, Context, Tool, Harness, Runtime, State, Guardrail, Eval을 어떻게 분리하고 조합해야 하는가?

이 저장소는 특정 Agent Framework 사용 설명서를 목표로 하지 않습니다. 제품별 API보다 오래 유지되는 Agent Engineering의 구조와 설계 원칙을 찾는 것이 목표입니다.

## 현재 단계

```text
Phase 1 Research       진행 중
Phase 2 Concept        미착수
Phase 3 Scope          미착수
Phase 4 TOC            미착수
Phase 5 Chapter Plan   미착수
Phase 6 Draft          미착수
```

## 초기 연구 축

```text
Model
  ↓
Instruction / Context
  ↓
Agent Loop / Harness
  ↓
Tool Interface
  ↓
Runtime / Sandbox
  ↓
State / Memory
  ↓
Guardrail / Approval
  ↓
Trace / Eval
  ↓
Outcome
```

추가 연구 축:

- Long-running Agent
- Tool / MCP / A2A
- Security / Containment
- Agent Evaluation
- Multi-agent / Delegation / Handoff
- Computer-use / Coding Agent benchmark
- Model capability와 Agent capability의 분리

## 다른 책과의 경계

- `ai-instruction-engineering-book`: CLAUDE.md, AGENTS.md, Rule, Skill, Hook 등 지침 엔지니어링
- `cloud-agent-book`: Local/Cloud 실행 위치, Runner, Git handoff, Cloud execution
- `software-factory-book`: Durable Task, Worker, Scheduler, Control Plane, Verification, Delivery
- 이 책: **한 Agent를 실제 작업 가능한 실행 시스템으로 만드는 Harness와 Runtime 설계**

## Research

1차 리서치는 `research/` 아래에서 관리합니다.

- `research/catalog/`: 출처 카탈로그
- `research/topics/`: 주제별 근거 정리
- `research/synthesis/`: 여러 출처를 교차해 만든 종합 모델
- `research/meta/`: 조사 방법과 품질 기준

기준일: 2026-10-02
