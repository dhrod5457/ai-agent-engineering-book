# 8장. Agent State Plane

Agent가 5분짜리 작업만 한다면 Process Memory와 Conversation History만으로도 충분할 수 있다.

문제는 작업이 길어질 때 시작된다.

Agent가 코드를 수정하고 테스트를 돌린다. 승인 대기 상태로 들어간다. 몇 시간 뒤 사람이 승인한다. 그 사이 Runtime은 종료됐다. 새 Runtime에서 Agent를 다시 시작해야 한다.

이때 "이전 대화를 요약해서 다시 넣자"만으로 충분할까.

이미 어떤 Tool이 실행됐는지, 어떤 Side Effect가 성공했는지, 어떤 Artifact가 만들어졌는지, 어떤 Source Version을 기준으로 결정했는지 알아야 한다면 부족하다.

이 책에서는 이런 실행 연속성을 담당하는 계층을 **Agent State Plane**이라고 부른다.

이 용어는 외부 표준명이 아니다. 여러 Agent SDK, Durable Execution, Long-running Harness 사례에서 반복되는 책임을 설명하기 위해 이 책에서 사용하는 synthesis다.

## Agent State Plane이 해결하려는 문제

핵심 질문은 하나다.

> Agent가 Process, Runtime, Context를 잃어도 무엇을 했고 어디까지 진행했으며 무엇을 다시 하면 안 되는지 어떻게 복구할 것인가?

이 질문은 Conversation Memory보다 넓다.

예를 들어 다음 상태를 생각해보자.

~~~text
Goal G-100
Status: AWAITING_APPROVAL

Completed:
- repository inspected
- patch created
- targeted tests passed

Pending:
- create_pull_request

Approval:
- requested for PR creation

Artifacts:
- patch.diff
- test-report.json

Source:
- main@abc123
~~~

이 정보가 있다면 Runtime을 종료해도 이후 다시 실행할 수 있다.

## State Plane은 하나의 Database를 의미하지 않는다

"State Plane"이라는 이름 때문에 하나의 중앙 Database를 떠올릴 수 있다.

이 책에서 중요한 것은 Storage Product가 아니라 Responsibility다.

구현은 여러 방식일 수 있다.

- relational DB
- document store
- event store
- object storage
- workflow engine
- mixed architecture

핵심은 State의 Owner와 Lifecycle이 Process Lifetime과 분리된다는 점이다.

~~~text
Agent Process
   ↓ read/write
State Plane
   ↓
Durable Storage
~~~

Process가 죽어도 State는 남는다.

## 최소 구성

이 책의 Reference Model에서는 다음을 최소 후보로 둔다.

~~~text
Agent State Plane
- Event History
- Checkpoint / Snapshot
- Goal / Progress
- Artifact Index
- Approval State
- External Source Version
- Memory Reference
~~~

모든 시스템이 일곱 개 Table을 만들어야 한다는 뜻이 아니다.

각 책임이 구분돼야 한다는 뜻이다.

## Event History

Event History는 실행 중 발생한 사실을 시간 순서로 남긴다.

예:

~~~text
run.started
model.completed
tool.proposed
tool.authorized
tool.completed
artifact.created
approval.requested
run.paused
~~~

Event는 "현재 상태" 자체보다 "어떻게 현재 상태가 됐는가"를 설명한다.

이 차이는 Recovery와 Audit에서 중요하다.

예를 들어 현재 State가 AWAITING_APPROVAL이라는 사실만 저장하면 어떤 Action 승인을 기다리는지 알기 어렵다.

Event에는 다음을 남길 수 있다.

~~~text
approval.requested
action: create_pull_request
repository: org/app
base: main
head: feature/fix
requested_at: ...
~~~

## Projection

Model에게 Event History 전체를 보여주지는 않는다.

State Plane에서 목적별 Projection을 만든다.

~~~text
Event History
    │
    ├─→ Current Run State
    ├─→ Goal Progress
    ├─→ Approval State
    ├─→ Artifact Index
    └─→ Context Projection
~~~

이 구조에서 Context는 State의 View다.

앞 장의 원칙이 여기서 구체화된다.

~~~text
Durable State
      ↓
Projection
      ↓
Current Context
~~~

## Goal / Progress

Goal은 Completion Contract다.

Progress는 현재 Goal에서 어디까지 진행했는지 나타낸다.

예:

~~~text
Goal:
  fix timeout handling

Milestones:
  [x] reproduce failure
  [x] identify cause
  [x] patch
  [ ] integration test
  [ ] create PR
~~~

Progress를 Model의 자유 텍스트 Summary만으로 관리하지 않는 이유는 Completion 판단과 Recovery에 사용하기 위해서다.

물론 Progress 자체도 틀릴 수 있다.

그래서 실제 Artifact와 Verification Result를 함께 연결한다.

## Artifact Index

Artifact를 State Plane이 직접 저장할 수도 있고 외부 Storage Reference만 관리할 수도 있다.

예:

~~~text
artifact_id: art-55
type: test_report
uri: object://agent-runs/g100/test-report.json
checksum: ...
verified: true
~~~

중요한 것은 Artifact 존재와 Correctness를 분리하는 것이다.

~~~text
Artifact Exists
≠ Artifact Verified
~~~

OSWorld 2.0 같은 Long-horizon 사례에서도 파일이 존재한다는 사실을 실제 결과 정확성으로 오해하는 실패가 관찰된다.

## Approval State

Human Approval은 Process가 살아 있는 동안만 기다리는 Blocking Call이 아니다.

Durable State로 표현할 수 있다.

~~~text
approval_id: ap-7
status: pending
action_ref: tool-call-88
requested_by: agent-12
requested_at: ...
~~~

Runtime은 종료될 수 있다.

승인 이벤트가 오면 새 Runtime이 Resume할 수 있다.

이 구조는 Human-in-the-loop를 정상적인 State Transition으로 만든다.

## External Source Version

Agent는 외부 Source의 Snapshot을 보고 결정한다.

장시간 작업에서는 Source가 바뀔 수 있다.

따라서 State Plane에 다음 Reference를 남길 가치가 있다.

~~~text
source: git-main
version: abc123

source: approval-policy
version: 41

source: customer-record
version: 812
~~~

이 Metadata는 이후 Reconciliation에서 사용된다.

"무엇을 봤는가"를 기록하지 않으면 stale decision을 감지하기 어렵다.

## Memory Reference

Long-term Memory는 State Plane 전체가 아니다.

하지만 현재 Run이 어떤 Memory를 사용했는지는 Trace/Audit을 위해 연결할 수 있다.

~~~text
memory_ref:
  mem-101
  mem-202
~~~

이렇게 하면 나중에 잘못된 Memory가 어떤 Run에 영향을 줬는지 추적하기 쉬워진다.

## Event Sourcing을 반드시 써야 하는가

아니다.

Agent State Plane이라는 개념이 Event Sourcing Architecture를 강제하는 것은 아니다.

하지만 Event History 관점은 몇 가지 장점이 있다.

- 실행 이력을 복구하기 쉽다.
- Side Effect가 이미 실행됐는지 판단하기 쉽다.
- Approval과 Retry 이유를 추적할 수 있다.
- Projection을 다시 만들 수 있다.
- Audit과 Eval 데이터로 활용할 수 있다.

반대로 모든 이벤트를 세밀하게 저장하면 복잡성과 비용이 커진다.

따라서 필요한 수준의 Event Granularity를 선택해야 한다.

## Conversation Log와 Execution History

둘은 일부 겹치지만 같은 것이 아니다.

Conversation Log에는 다음이 있을 수 있다.

~~~text
user: PR 만들어줘
assistant: 생성하겠습니다
~~~

Execution History에는 다음이 필요할 수 있다.

~~~text
tool.proposed
policy.allowed
tool.started
tool.completed
external_id: PR-220
~~~

따라서:

~~~text
Conversation History
⊂ Execution History
~~~

로 보는 편이 정확하다.

모델에게 보여줄 Conversation과 시스템이 복구에 사용할 Execution History의 목적이 다르다.

## Snapshot과 Checkpoint

Event가 길어지면 매번 처음부터 Projection을 만드는 것이 비효율적일 수 있다.

그래서 Snapshot을 둘 수 있다.

~~~text
Events 1..1000
      ↓
Snapshot @1000
      +
Events 1001..current
~~~

Snapshot은 성능 최적화다.

Audit History나 Canonical Event를 없애는 것과는 다르다.

Checkpoint는 현재 실행을 이어가기 위한 상태를 Materialize하는 의미로 사용할 수 있다.

이 책에서는 Checkpoint를 Long-term Memory와 구분한다.

~~~text
Checkpoint
= Execution Continuity

Memory
= Future Reuse
~~~

## State Plane과 Runtime

좋은 구조에서는 Runtime을 교체할 수 있다.

~~~text
Runtime A
  ↓ crash

State Plane
  ↓ restore

Runtime B
  ↓ resume
~~~

이때 Workspace까지 완전히 복구해야 하는 Task라면:

- Git Commit
- Artifact Archive
- Workspace Snapshot
- Rebuild Script

같은 별도 수단이 필요할 수 있다.

State Plane은 Workspace 자체와 동일하지 않다.

## State Plane과 Harness

Harness는 State를 읽고 다음 Transition을 만든다.

~~~text
State Plane
    ↓
Harness
    ↓
Model / Tool
    ↓
New Events
    ↓
State Plane
~~~

이 관계에서 Harness는 Control Logic이고 State Plane은 Durable Record다.

둘을 분리하면 Harness를 Upgrade하거나 Restart해도 State를 유지할 수 있다.

## State Plane과 Software Factory Control Plane

여기서 경계를 명확히 해야 한다.

Agent State Plane은 한 Agent Run/Goal의 실행 연속성을 다룬다.

Software Factory Control Plane은 여러 Work Item과 Worker를 다룬다.

~~~text
Agent State Plane
- one run
- one goal
- execution continuity

Factory Control Plane
- many tasks
- worker fleet
- scheduling
- assignment
- delivery
~~~

실제 시스템에서는 두 계층이 연결될 수 있다.

하지만 개념적으로 분리해야 책임이 명확해진다.

## 작은 예: 승인 후 PR 생성

Agent가 코드를 수정하고 테스트까지 통과했다.

PR 생성은 외부 Write라 Approval이 필요하다.

Event 흐름을 보자.

~~~text
goal.started
tool.completed: edit_file
tool.completed: run_test
artifact.verified: test_report
approval.requested: create_pull_request
run.paused
~~~

몇 시간 뒤:

~~~text
approval.granted
run.resumed
tool.proposed: create_pull_request
policy.allowed
tool.completed: PR-220
artifact.created: pr_ref
goal.completed
~~~

중간 Process가 존재하지 않아도 된다.

Execution Continuity가 State Plane에 있기 때문이다.

## State Plane에 너무 많은 것을 넣지 않는다

State Plane을 만들기 시작하면 모든 데이터를 넣고 싶어진다.

하지만 다음은 분리할 수 있다.

- 대용량 Raw Log → Artifact Storage
- Repository 전체 → Git
- User Profile 전체 → Identity/Profile System
- Long-term Knowledge → Memory Store
- External Canonical Data → Source System

State Plane은 Reference와 실행에 필요한 Metadata를 유지하면 된다.

핵심은 Source of Truth를 복제하는 것이 아니다.

Execution Continuity를 유지하는 것이다.

## 이 장에서 가져갈 것

Agent State Plane은 이 책의 중심 개념이다.

다시 정의하면:

> **Agent State Plane은 Agent가 Process, Runtime, Context를 잃어도 실행 이력과 현재 목표, Progress, Approval, Artifact, External Source Reference를 바탕으로 작업을 이어갈 수 있게 하는 상태 관리 계층이다.**

이 정의에서 중요한 것은 저장 기술이 아니다.

Responsibility Boundary다.

다음 장에서는 State Plane이 실제 Failure Recovery에 어떻게 사용되는지 다룬다.

특히 Replay를 "모든 것을 다시 실행하는 것"으로 오해하면 어떤 문제가 생기는지, External Side Effect를 중복 없이 복구하려면 무엇이 필요한지 살펴본다.

## 주요 근거

- Temporal Durable Execution
- LangGraph Persistence
- Anthropic Managed Agents
- OpenAI Agents SDK Sessions
- research/topics/18-durable-state-event-log-replay.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
