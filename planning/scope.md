# Scope

기준일: 2026-10-02

## 범위 원칙

이 책의 중심은 **LLM을 실제 환경에서 안전하고 복구 가능하게 행동하는 Agent로 만들기 위한 실행 구조를 어떻게 설계할 것인가**이다.

새로운 주제를 추가할 때 다음 질문으로 판단한다.

> 이 내용이 독자가 실제 Agent의 Context, State, Tool, Harness, Runtime, Identity, Security, Eval을 설계하는 데 직접 도움이 되는가?

- YES: 핵심 본문
- 직접 필요하지만 구현 깊이가 높은 내용: Advanced Topic
- Cloud 운영에 더 가까움: cloud-agent-book
- 조직의 Work orchestration에 더 가까움: software-factory-book
- instruction file 작성법에 더 가까움: ai-instruction-engineering-book
- 일반 LLM 이론: 제외

---

# 대상 독자

주 대상:

- Senior Software Engineer
- Backend / Platform Engineer
- AI Application Engineer
- Agent Runtime / Harness 개발자
- Tech Lead / Architect
- Coding Agent / Workflow Agent를 실제 서비스에 넣으려는 개발자

독자는 다음을 알고 있다고 가정한다.

- API / JSON / HTTP
- basic authentication / authorization
- Git / CI
- container / process 기본 개념
- LLM / tool calling 기본 사용 경험

다음은 사전 지식으로 요구하지 않는다.

- Foundation Model 학습
- RLHF / RL 내부 구현
- formal verification
- distributed workflow engine internals
- kernel internals
- identity provider 구현

---

# 독자가 마지막에 할 수 있어야 하는 것

- Model과 Agent를 구분할 수 있다.
- 어떤 상태를 Context에 넣고 어떤 상태를 durable하게 저장해야 하는지 판단할 수 있다.
- Session, Workspace, Goal, Artifact, Memory를 분리할 수 있다.
- Tool Interface를 Agent 관점에서 설계할 수 있다.
- Agent Loop와 Stop Condition을 설계할 수 있다.
- 실패 후 resume/recovery 구조를 만들 수 있다.
- Memory Write Policy를 설계할 수 있다.
- User / Agent / Tool identity를 분리할 수 있다.
- Credential을 Agent와 분리할 수 있다.
- Sandbox / Authorization / Approval을 분리할 수 있다.
- Task Risk에 따라 policy를 설계할 수 있다.
- Trace와 Eval을 구축할 수 있다.
- Harness 변경을 regression으로 검증할 수 있다.
- Multi-Agent가 필요한지 판단할 수 있다.

---

# 핵심 본문 범위

## 1. Model에서 Agent로

반드시 다룬다.

- Model vs Agent
- Agent loop
- observation/action cycle
- stop condition
- tool call
- structured result
- retry
- interruption/resume

핵심 질문:

> 무엇이 단순 LLM 호출을 Agent 실행으로 바꾸는가?

---

## 2. Agent Harness

반드시 다룬다.

- loop
- context assembly
- tool dispatch
- stop
- retry
- budget
- handoff
- approval interruption
- verification hook
- trace emission

Harness를 Framework와 동일시하지 않는다.

특정 SDK 사용법보다 responsibility boundary를 설명한다.

---

## 3. Context Engineering

다룬다.

- context budget
- progressive context
- retrieval
- history projection
- tool schema selection
- compaction
- stale context
- context pollution
- result filtering

다루지 않을 것:

- 일반 RAG 제품 구축 전체
- vector DB 비교
- embedding 모델 벤치마크 전체

---

## 4. Agent State Plane

책의 핵심 범위다.

다룬다.

- Event History
- Checkpoint
- Snapshot
- Goal / Progress
- Approval State
- Artifact Index
- Source Version
- Memory Reference
- pause/resume
- recovery
- replay
- idempotency

핵심 질문:

> Agent가 process와 context를 잃어도 작업을 어떻게 이어갈 것인가?

---

## 5. State Taxonomy

반드시 구분한다.

- Inference Context
- Conversation / Session
- Run State
- Workspace
- Goal / Task State
- Artifact
- Long-term Memory
- External Source of Truth

---

## 6. Memory

다룬다.

- memory purpose
- write candidate
- provenance
- scope
- retention
- retrieval
- stale memory
- contradiction
- quarantine
- repair
- forgetting
- poisoning

다루지 않을 것:

- 인간 인지과학 전체
- foundation model internal memory
- vector DB 제품별 사용법

---

## 7. External State Reconciliation

다룬다.

- source registry
- source authority
- source version
- refresh trigger
- optimistic concurrency
- invalidation
- re-plan
- final verification

Long-running Agent에서 핵심 범위로 본다.

---

## 8. Tool Engineering

다룬다.

- capability boundary
- tool naming
- description
- schema
- result contract
- side effect
- error model
- provenance
- trust
- output size
- ACI

특정 API wrapper 작성법은 최소화한다.

---

## 9. MCP

다룬다.

- MCP의 위치
- Tool / Resource / Prompt
- stateless core
- Tasks extension
- authorization boundary

다루지 않을 것:

- 모든 MCP SDK API
- MCP Server 구현 튜토리얼 전체

---

## 10. A2A

다룬다.

- remote Agent collaboration
- Agent Card
- Message
- Task
- Artifact
- lifecycle
- authorization

핵심은 MCP와의 경계다.

다루지 않을 것:

- A2A를 이용한 조직 전체 workflow engine 구현

---

## 11. Identity and Delegation

핵심 본문 범위다.

- user identity
- application identity
- agent identity
- workload identity
- tool identity
- resource identity
- delegated access
- autonomous access
- actor chain
- lifecycle

---

## 12. Credential Boundary

다룬다.

- short-lived token
- credential broker
- gateway injection
- scope
- rotation
- audit

다루지 않을 것:

- OAuth / OIDC 프로토콜 전체 교과서
- IdP 제품 전체 비교

---

## 13. Runtime / Sandbox

다룬다.

- process isolation
- filesystem
- network
- container
- gVisor
- microVM
- credential exposure
- runtime lifecycle
- ephemeral state

특정 kernel 기술의 내부 구현은 Advanced Topic으로 제한한다.

---

## 14. Risk-adaptive Policy

다룬다.

- read/write risk
- reversible / irreversible
- production boundary
- data sensitivity
- isolation tier
- approval
- verifier
- rollback

Risk scoring framework는 설명하되 법적 compliance framework 전체로 확장하지 않는다.

---

## 15. Policy Mutation

다룬다.

- deny
- inspect
- policy proposal
- deterministic validation
- risk analysis
- approval
- apply
- rollback

Agent가 self-authorize하는 구조는 권장하지 않는다.

---

## 16. Security

다룬다.

- prompt injection
- tool result trust
- memory poisoning
- sandbox
- least privilege
- credential boundary
- approval fatigue
- audit

다루지 않을 것:

- 일반 AppSec 전체
- 보안 인증 프레임워크 전체
- 모델 alignment 연구 전체

---

## 17. Observability

다룬다.

- model trace
- tool trace
- state transition
- approval
- handoff
- runtime error
- cost
- latency

Logging product 비교는 하지 않는다.

---

## 18. Evaluation

핵심 범위다.

- output eval
- trajectory eval
- tool routing
- argument quality
- policy compliance
- security eval
- outcome eval
- repeated reliability
- infrastructure noise
- benchmark versioning

---

## 19. Eval CI

다룬다.

- production failure → regression
- capability dataset
- security dataset
- long-horizon dataset
- release gate
- shadow
- canary
- model upgrade audit

---

## 20. Harness Ablation

다룬다.

- minimal baseline
- component inventory
- ablation
- marginal value
- interaction effect
- scaffold debt
- model upgrade re-evaluation

---

## 21. Multi-Agent

다룬다.

- single-agent first
- agent-as-tool
- handoff
- specialist
- context isolation
- permission separation
- independent verifier
- coordination cost

Multi-Agent framework의 사용법은 범위 밖이다.

---

# Advanced Topic으로 제한할 범위

- event sourcing 구현 세부
- formal state machine
- vector memory indexing
- kernel sandbox 내부
- microVM orchestration
- agent identity federation
- distributed tracing internals
- policy theorem/prover
- capability-based security 이론
- deterministic workflow engine 구현

핵심 개념 이해에 필요한 수준까지만 다룬다.

---

# 다른 책으로 넘길 범위

## ai-instruction-engineering-book

- CLAUDE.md 작성법
- AGENTS.md
- Skill 작성법
- Rule 구조
- Hook 작성
- instruction-specific eval

이 책에서는 instruction loading과 runtime integration만 다룬다.

---

## cloud-agent-book

- Local vs Cloud Task Routing
- Cloud Runner
- Git Handoff
- Remote Workspace
- Cloud Environment
- CPU/RAM/Token 비용
- Cloud execution optimization

이 책에서는 Runtime의 구조와 security boundary까지만 다룬다.

---

## software-factory-book

- Durable Backlog
- Requirement → Task
- Scheduler
- Worker Fleet
- Lease
- Assignment
- Retry at work-system level
- Acceptance Authority
- Delivery
- Merge / Deploy
- Feedback loop

이 책의 Agent State Plane과 Factory Control Plane을 분리한다.

~~~text
Agent State Plane
= 하나의 Agent Run / Goal continuity

Factory Control Plane
= 여러 Work / Worker / Delivery continuity
~~~

---

# 명시적으로 제외할 주제

## 1. LLM 학습

- pretraining
- fine-tuning 상세
- RLHF
- optimizer
- model architecture

## 2. Prompt Engineering 입문

- 좋은 질문 작성법
- 일반 system prompt 모음
- 역할 부여 템플릿

## 3. Agent Framework 튜토리얼

- LangGraph 따라 만들기
- OpenAI Agents SDK API 전체
- Google ADK 사용법 전체
- CrewAI 사용법

제품은 구조를 설명하는 사례로만 사용한다.

## 4. Multi-Agent 조직론

- 가상의 CEO/CPO/Developer Agent 조직
- Agent 회사 만들기
- 인간 조직 모사

핵심 범위가 아니다.

## 5. Software Factory 전체

Task queue, Worker fleet, merge, deploy는 별도 책으로 유지한다.

---

# 제품 사용 범위

다음 제품/프로젝트는 원칙 설명을 위한 사례로 사용한다.

- OpenAI Agents SDK / Codex
- Anthropic Claude Code
- Google ADK
- SWE-agent
- MCP
- A2A
- LangGraph
- Temporal
- AWS AgentCore
- NVIDIA OpenShell
- gVisor
- Firecracker

제품 syntax와 기능은 빠르게 바뀌므로 기준일과 출처를 research에서 관리한다.

본문은 특정 API 형태에 의존하지 않는다.

---

# 책의 최종 경계

이 책은 다음 질문에 답한다.

> 하나의 AI Agent가 실제 환경에서 도구를 사용해 장시간 작업하고, 중간에 실패해도 복구하며, 적절한 권한 안에서 행동하고, 실제 outcome으로 완료를 증명하려면 어떤 엔지니어링 구조가 필요한가?

반대로 다음 질문은 다른 책으로 넘긴다.

> 조직의 수많은 Task와 Agent Worker를 어떻게 지속적으로 배정·검증·전달할 것인가?

그 질문은 AI Software Factory의 영역이다.
