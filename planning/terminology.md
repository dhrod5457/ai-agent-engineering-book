# Terminology and Boundary

기준일: 2026-10-02

이 문서는 책 전체에서 혼동하기 쉬운 핵심 용어의 의미와 경계를 고정한다.

## Model

LLM inference engine.

포함:
- language/reasoning
- structured output
- tool call proposal

포함하지 않음:
- durable state ownership
- credential enforcement
- sandbox
- actual side effect authorization

## Agent

Model을 Context, Tool, State, Runtime과 연결해 반복적으로 관찰하고 행동하게 하는 실행 주체.

~~~text
Agent
= Model
+ Harness
+ Context
+ Tools
+ State
+ Runtime
+ Policy
~~~

완전한 수학식이 아니라 책임 경계를 설명하기 위한 개념식이다.

## Agent Definition

Agent의 정적 또는 상대적으로 안정적인 정의.

예:
- model selection
- role/instruction
- output contract
- tool eligibility
- default policy

## Harness

Model을 실제 Agent 실행으로 만드는 control logic.

책임:
- loop
- context assembly
- tool dispatch
- stop condition
- retry
- interruption/resume
- handoff
- budget
- verification hook
- trace emission

Framework 제품명과 동일한 개념이 아니다.

## Runtime

실제 code/tool side effect가 발생하는 실행환경.

예:
- process
- container
- sandbox
- VM / microVM
- filesystem
- network
- browser
- shell
- compute resource

## Context

현재 한 번의 model inference에 실제로 들어가는 정보.

~~~text
Context
≠ State Store
~~~

## Session

여러 turn의 conversation continuity.

대화 history를 유지할 수 있지만 Goal, Workspace, Long-term Memory와 동일하지 않다.

## Run

Agent가 하나의 입력 또는 Goal을 처리하는 실행 lifecycle.

예:
- started
- paused
- resumed
- completed
- failed

## Workspace

Agent가 작업 중 사용하는 실행환경 상태.

예:
- checked-out repository
- temporary files
- browser state
- installed packages

Workspace가 durable하다고 가정하지 않는다.

## Goal

Agent가 완료해야 하는 objective와 completion contract.

포함 후보:
- objective
- scope
- constraint
- budget
- completion condition
- verification requirement

## Task

문맥에 따라 의미가 달라질 수 있으므로 반드시 qualifier를 붙인다.

- Agent Goal / Agent Task
- MCP Task
- A2A Task
- Factory Task

책에서는 단독 "Task" 사용을 최소화한다.

## Artifact

Agent가 생성하거나 전달하는 검증 가능한 결과물.

예:
- file
- commit
- report
- screenshot
- generated document
- structured result

## State

시간에 따라 변하는 Agent 실행 정보의 상위 개념.

이 책에서는 State를 하나의 저장소로 정의하지 않는다.

## Agent State Plane

Agent execution continuity를 보장하기 위한 상태 관리 계층.

포함 후보:
- event history
- checkpoint
- goal/progress
- approval state
- artifact index
- source version
- memory reference

Software Factory Control Plane과 분리한다.

## Event History

실행 중 발생한 사실을 시간 순서로 기록한 history.

예:
- model.completed
- tool.authorized
- tool.completed
- approval.granted

Event를 model context 전체에 직접 넣는 것은 아니다.

## Checkpoint

빠른 resume를 위해 특정 시점의 execution state를 materialize한 것.

Long-term Memory와 분리한다.

## Snapshot

긴 event history replay 비용을 줄이기 위한 materialized state.

Canonical audit history를 대체하지 않는다.

## Memory

미래 run에서 재사용할 수 있도록 보존하는 장기 정보.

예:
- learned preference
- reusable lesson
- previous solution pattern

Execution recovery state와 분리한다.

## Memory Candidate

Observation 또는 result 중 long-term memory로 승격 가능한 후보.

Write policy를 통과하기 전에는 trusted memory가 아니다.

## Source of Truth

Agent 외부에 존재하는 authoritative canonical source.

예:
- current Git HEAD
- production configuration
- approved requirement
- current DB record

Memory나 internal note보다 우선할 수 있다.

## Reconciliation

Agent의 working state와 authoritative external state를 비교하고 차이를 반영하는 과정.

## Tool

Model이 요청할 수 있는 bounded capability interface.

Tool은 raw API와 동일하지 않을 수 있다.

## Agent-Computer Interface

Agent가 외부 컴퓨터/환경과 상호작용하는 action/observation interface.

Tool design의 상위 관점.

## Capability

Agent가 사용할 수 있는 기능.

예:
- file read
- GitHub mutation
- browser
- database read

Capability discovery와 authorization을 분리한다.

## MCP

Agent와 capability/context provider를 연결하는 protocol.

Agent Harness 전체가 아니다.

## A2A

독립 Agent System 사이의 remote collaboration protocol.

내부 subagent 호출과 동일하지 않다.

## Identity

행동 주체를 구분하는 security principal.

이 책에서 구분:
- human identity
- application identity
- agent identity
- workload identity
- tool identity
- resource identity

## Delegation

한 principal이 다른 principal에게 일정 scope 내 action authority를 위임하는 것.

## Authentication

누가 요청했는지 확인.

## Authorization

현재 principal이 해당 resource/action을 수행할 권한이 있는지 결정.

## Approval

권한이 있어도 이번 action을 지금 실행해도 되는지 추가 판단.

## Policy

Agent action에 적용되는 deterministic or externally enforced rule.

System prompt와 분리한다.

## Sandbox

Agent workload가 접근 가능한 filesystem/process/network/runtime 범위를 제한하는 containment mechanism.

Authorization을 대체하지 않는다.

## Containment

Agent가 잘못 행동하더라도 피해 범위를 제한하는 runtime/security boundary.

## Guardrail

입력, 출력, tool action, policy 등에 적용되는 검사/통제의 일반적 표현.

구체 구현이 prompt인지 deterministic enforcement인지 구분해서 설명한다.

## Trace

Agent execution의 model/tool/state/policy event를 재구성할 수 있는 관찰 데이터.

## Eval

Agent behavior 또는 outcome이 기대 기준을 만족하는지 반복 가능하게 측정하는 체계.

## Grader

Eval case 결과를 판정하는 mechanism.

예:
- deterministic code
- environment state check
- model grader
- human review

## Harness Ablation

Harness component를 제거/비활성화해 실제 기여도를 측정하는 실험.

## Harness Debt

더 이상 필요 없거나 이유가 사라진 scaffold가 누적된 상태.

## Multi-Agent

둘 이상의 Agent execution 주체가 역할을 나누는 구조.

기본값이 아니라 complexity trade-off가 정당화될 때 사용하는 구조.

## Software Factory Control Plane

여러 work item, worker, delivery를 durable하게 관리하는 상위 생산 시스템 계층.

~~~text
Agent State Plane
= one agent execution continuity

Factory Control Plane
= many work items / workers / delivery continuity
~~~

## Side Effect

Agent 또는 Tool 실행이 외부 상태를 실제로 바꾸는 효과.

예:
- file write
- issue creation
- message send
- deployment
- payment

Model이 Action을 제안하는 것과 실제 Side Effect가 발생하는 것을 분리한다.

## Completion Claim

Model 또는 Agent가 Goal을 완료했다고 주장하는 것.

자연어 self-report 또는 structured completion signal일 수 있다.

## Completion Authority

Goal이 실제로 완료됐는지 최종 판정하는 책임.

가능하면 다음처럼 Model self-report 밖의 Evidence와 연결한다.

- deterministic test
- artifact validation
- external state check
- policy / human acceptance

~~~text
Completion Claim
≠ Completion Authority
~~~

## Verification

Artifact, Side Effect, External State가 Goal의 completion condition을 만족하는지 확인하는 과정.

가능한 경우 deterministic verifier를 우선하고, 정성 판단이 필요한 부분만 Model/Human Grader를 사용한다.

## Long-running Agent

하나의 짧은 inference/session 범위를 넘어 Goal, Progress, External State, Artifact를 지속적으로 추적해야 하는 Agent 실행.

Long Context와 동일한 개념이 아니다.

## Memory Write Gate

Observation 또는 Result를 Persistent Memory로 승격하기 전에 provenance, scope, sensitivity, contradiction, freshness 등을 검사하는 이 책의 synthesis.

외부 표준 용어가 아니다.

## AgentVersion

Agent behavior에 영향을 주는 구성요소의 version boundary를 설명하기 위한 이 책의 synthesis.

예:

~~~text
AgentVersion = (
  model,
  instruction,
  context_policy,
  harness,
  state_schema,
  memory_policy,
  tools,
  runtime,
  policy,
  grader
)
~~~

정확한 표준 tuple이 아니라 reproducible evaluation을 위한 개념이다.

## Agent-as-Tool

Manager Agent가 전체 Goal과 ownership을 유지한 채 Specialist Agent에게 bounded subtask를 요청하고 결과를 돌려받는 협업 pattern.

제품별 공식 용어와 동일하다고 가정하지 않는다.

## Handoff

현재 Work 또는 Interaction의 ownership을 다른 Agent에게 넘기는 transition.

Context 전달뿐 아니라 Goal State와 Effective Authorization 재평가가 필요할 수 있다.

## Remote Agent

독립된 Runtime, State, Policy를 가진 별도 Agent System.

Local Subagent 또는 bounded Tool과 동일하지 않다.


# 표기 규칙

본문에서 Architecture의 정의된 개념은 영문 Title Case를 유지한다.

- Agent
- Model
- Harness
- Context
- Tool
- State
- Memory
- Runtime
- Sandbox
- Trace
- Eval
- Goal
- Artifact
- Identity
- Authorization
- Approval
- Completion
- Side Effect
- Long-running

일반 서술의 production은 "운영"을 우선한다.

다만 다음은 원문 또는 label을 유지한다.

- Minimum Viable Production Agent
- Production Readiness Checklist
- Production DB / Cluster 같은 예시 이름
- environment == "production" 같은 literal value
- 논문/문서 제목

책 자체의 synthesis 명칭은 정확히 유지한다.

- Agent State Plane
- Harness Debt
- Memory Write Gate
- AgentVersion
- Factory Control Plane
