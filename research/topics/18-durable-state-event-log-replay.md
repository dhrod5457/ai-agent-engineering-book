# Durable State, Event Log, and Replay

기준일: 2026-10-02

## 문제

Long-running Agent가 process crash, context reset, runtime replacement 뒤에도 같은 작업을 이어가려면 무엇을 저장해야 하는가?

단순 snapshot만으로는 다음을 설명하기 어렵다.

- 왜 현재 상태가 됐는가
- 어떤 tool call이 이미 실행됐는가
- side effect를 다시 실행해도 되는가
- approval이 어디서 멈췄는가
- recovery 중 어떤 action을 replay해야 하는가

따라서 State Plane의 핵심 후보로 event history를 검토한다.

## Durable Execution에서 얻는 교훈

Temporal은 Workflow의 state와 progress를 Event History로 보존하고 Worker가 event history를 replay하여 local state를 재구성한다.

핵심 구조:

~~~text
Event History
    ↓
Deterministic Replay
    ↓
Rebuild Workflow State
    ↓
New Decision
    ↓
Command
    ↓
New Event
~~~

Worker가 죽어도 event history가 남아 있으면 다른 Worker가 state를 복구할 수 있다.

이 원리는 Agent runtime에도 참고할 가치가 크다.

## 그러나 Agent는 Temporal Workflow와 다르다

LLM inference는 본질적으로 nondeterministic할 수 있고 외부 tool call은 side effect를 만든다.

따라서 과거 event를 replay하면서 다음을 무조건 다시 실행하면 안 된다.

- model call
- payment
- email send
- GitHub mutation
- deployment
- production DB mutation

Agent State Plane에서는 결과를 event로 기록하고 replay 시 재사용해야 한다.

~~~text
Decision Requested
→ Model Result Recorded
→ Tool Proposed
→ Policy Decision Recorded
→ Tool Executed Once
→ Tool Result Recorded
→ State Projection Updated
~~~

Recovery에서는 이미 완료된 external side effect를 다시 실행하지 않는다.

## Event와 Projection

권장 구조:

~~~text
Immutable Event Log
      │
      ├─→ Session Projection
      ├─→ Goal / Progress Projection
      ├─→ Approval Projection
      ├─→ Tool Execution Projection
      ├─→ Artifact Index
      └─→ Context Projection
~~~

Model에게 event log 전체를 넣지 않는다.

Context Engine은 현재 turn에 필요한 projection만 만든다.

## Event 후보

~~~text
run.started
input.received

model.requested
model.completed
model.failed

tool.proposed
tool.authorized
tool.denied
tool.started
tool.completed
tool.failed

approval.requested
approval.granted
approval.rejected

goal.created
goal.updated
milestone.completed

artifact.created
artifact.verified

memory.proposed
memory.accepted
memory.quarantined

state.reconciled
source.refreshed

run.paused
run.resumed
run.completed
run.failed
~~~

## Idempotency

External side effect에는 가능한 한 idempotency key가 필요하다.

예:

~~~text
taskId + actionType + logicalOperationId
~~~

같은 recovery event가 다시 처리돼도 중복 email, 중복 payment, 중복 issue 생성이 발생하지 않도록 한다.

## Snapshot

Event history가 길어지면 모든 event를 매번 replay하는 비용이 커진다.

따라서:

~~~text
Events 1..1000
        ↓
Snapshot @1000
        ↓
Events 1001..current
~~~

형태를 사용할 수 있다.

Snapshot은 acceleration artifact이고 canonical audit history는 event log에 남긴다.

## Checkpoint와 Long-term Memory 분리

LangGraph는 thread-scoped state를 checkpointer로, cross-thread long-term memory를 store로 분리한다.

이 구분은 Agent State Plane에도 유효하다.

~~~text
Checkpoint
= current execution continuity

Memory
= future execution reuse
~~~

둘을 같은 table/API로 취급하면 lifecycle과 security policy가 섞인다.

## Event Log와 Conversation Log도 다르다

Conversation message만으로 execution state를 재구성할 수 없는 경우가 많다.

Tool authorization, retry, internal checkpoint, idempotency, runtime failure는 대화 메시지가 아닐 수 있다.

따라서:

~~~text
Conversation History
⊂ Execution History
~~~

로 보는 편이 정확하다.

## Determinism Boundary

Agent system에서 deterministic replay 가능한 부분:

- state transition
- policy outcome if version pinned
- recorded result projection
- deterministic business rule

다시 계산하지 않는 편이 좋은 부분:

- stochastic model output
- external mutable query
- irreversible side effect

필요하면 새로운 decision으로 명시적으로 재실행하고 새 event를 남긴다.

## Schema Versioning

Event schema도 versioned software다.

필요 항목:

- event_type
- event_version
- event_id
- aggregate / run id
- timestamp
- actor
- causation_id
- correlation_id
- payload
- policy / harness version
- source / provenance

## 책에 반영할 핵심 원칙

1. Durable Agent State는 process memory 밖에 있어야 한다.
2. Event Log와 Context를 분리한다.
3. Replay는 side effect 재실행을 의미하지 않는다.
4. Model/tool 결과를 execution history에 기록한다.
5. External mutation에는 idempotency가 필요하다.
6. Checkpoint와 Long-term Memory를 분리한다.
7. Conversation history만으로 recovery를 설계하지 않는다.
8. Snapshot은 optimization이고 Event History가 audit backbone이다.
9. State projection은 목적별로 분리한다.

## 주요 근거

- Temporal Durable Execution / Workflow Task replay
- LangGraph Persistence — Checkpointer vs Store
- Anthropic Managed Agents — durable session/event separation
- OpenAI Agents Sessions / Goal state
