# AI Agent Engineering

LLM을 단순한 응답 모델이 아니라 실제 환경에서 도구를 사용하고 상태를 이어가며 검증 가능한 결과를 만드는 **Agent**로 구성하는 방법을 연구하고 정리하는 책 프로젝트입니다.

## 중심 질문

> LLM을 실제 작업 가능한 Agent로 만들기 위해 Model, Context, State, Memory, Tool, Harness, Runtime, Identity, Policy, Eval을 어떻게 분리하고 조합해야 하는가?

이 저장소는 특정 Agent Framework 사용 설명서를 목표로 하지 않습니다. 제품별 API보다 오래 유지되는 Agent Engineering의 구조와 설계 원칙을 찾는 것이 목표입니다.

## 현재 단계

~~~text
Phase 1 Research       1~3차 broad research 완료
Phase 2 Concept        완료
Phase 3 Scope          완료
Phase 4 TOC            v0.1 완료
Phase 5 Chapter Plan   완료
Phase 6 Draft          완료
Phase 7 Review         Evidence Review 완료
~~~

Broad Research는 종료하고, 이후에는 장별 초고에 필요한 Targeted Research만 추가합니다.

## 현재 Reference Model

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
        ├─ Artifact Index
        ├─ Approval State
        ├─ External Source Version
        └─ Memory Reference
        ↓
Capability / Policy Gateway
        ↓
Execution Runtime
        ↓
External World
~~~

Cross-cutting:

- Trace / Audit
- Eval / Regression
- Security Policy
- Cost / Latency
- Versioning

## 핵심 경계

~~~text
Model Capability
≠ Agent Capability

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

Capability Discovery
≠ Authorization

Sandbox
≠ Authorization

Approval
≠ Containment

Agent State Plane
≠ Software Factory Control Plane
~~~

## 다른 책과의 경계

- `ai-instruction-engineering-book`: CLAUDE.md, AGENTS.md, Rule, Skill, Hook 등 지침 엔지니어링
- `cloud-agent-book`: Local/Cloud 실행 위치, Runner, Git handoff, Cloud execution
- `software-factory-book`: Durable Work, Worker Fleet, Scheduler, Control Plane, Verification, Delivery
- 이 책: **하나의 Agent를 실제 작업 가능한 실행 시스템으로 만드는 구조**

## Source of Truth

Planning:

- `planning/concept.md`
- `planning/scope.md`
- `planning/terminology.md`
- `planning/research-gap-audit.md`
- `planning/toc.md`
- `planning/chapter-evidence-map.md`

Research:

- `research/catalog/source-catalog.md`
- `research/topics/`
- `research/synthesis/agent-engineering-reference-model-v0.3.md`
- `research/meta/methodology.md`

## 현재 책 구조

~~~text
Part I   Model에서 Agent로
Part II  Context와 Tool을 설계한다
Part III Agent State Plane
Part IV  Memory를 안전하게 사용한다
Part V   Identity, Security, Runtime
Part VI  Agent를 관찰하고 개선한다
Part VII Multi-Agent와 Production Boundary
~~~

현재 TOC는 25장 + Epilogue v0.1이다.

## 다음 단계

1. Publication-time Freshness Audit
2. Manuscript Assembly

기준일: 2026-10-02

## 공통 독서판

[공통 디자인 2026.10.04-preview.1 발행 파일](https://github.com/dhrod5457/ai-agent-engineering-book/releases/tag/2026.10.04-preview.1) · [독서판 제작·검증 규칙](publication/common-reading/README.md). 기존 원고와 검토 상태를 보존한 새 디자인 판입니다.
