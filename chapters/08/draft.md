# 8장. Agent State Plane

에이전트가 5분짜리 작업만 한다면 프로세스 메모리와 대화 기록만으로도 충분할 수 있다. 문제는 작업이 길어질 때 시작된다. 에이전트가 코드를 수정하고 테스트를 돌린다. 승인 대기 상태로 들어간다. 몇 시간 뒤 사람이 승인한다. 그 사이 실행 환경은 종료됐다. 새 실행 환경에서 에이전트를 다시 시작해야 한다. 이때 "이전 대화를 요약해서 다시 넣자"만으로 충분할까. 이미 어떤 도구가 실행됐는지, 어떤 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)가 성공했는지, 어떤 산출물이 만들어졌는지, 어떤 원본 버전을 기준으로 결정했는지 알아야 한다면 부족하다.

이 책에서는 이런 실행 연속성을 담당하는 계층을 **에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)**이라고 부른다. 이 용어는 외부 표준명이 아니다. 여러 에이전트 SDK, 중단 뒤에도 이어갈 수 있는 실행, 장시간 작업용 하네스 사례에서 반복되는 책임을 설명하기 위해 이 책에서 사용하는 설명용 개념이다.

## Agent State Plane이 해결하려는 문제

핵심 질문은 하나다.

> 에이전트가 프로세스, 실행 환경, 컨텍스트(Context: 모델에 전달하는 정보)를 잃어도 무엇을 했고 어디까지 진행했으며 무엇을 다시 하면 안 되는지 어떻게 복구할 것인가?

이 질문은 Conversation Memory보다 넓다. 예를 들어 다음 상태를 생각해보자.

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

이 정보가 있다면 실행 환경을 종료해도 이후 다시 실행할 수 있다.

## State Plane은 하나의 Database를 의미하지 않는다

"상태 관리 계층"이라는 이름 때문에 하나의 중앙 Database를 떠올릴 수 있다. 이 책이 살펴보려는 것은 어떤 저장 제품을 쓰느냐보다, 어느 부분이 어떤 정보를 책임지고 보존하느냐다. 구현은 여러 방식일 수 있다.

- relational DB
- document store
- event store
- object storage
- workflow engine
- mixed architecture

핵심은 상태의 담당자와 유지 과정이 Process Lifetime과 분리된다는 점이다.

~~~text
Agent Process
   ↓ read/write
State Plane
   ↓
Durable Storage
~~~

프로세스가 죽어도 상태는 남는다.

## Reference 구성

이 책의 Reference Model에서는 다음 책임을 대표 구성요소로 둔다.

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

모든 시스템이 이 항목을 각각 별도 Table이나 서비스로 구현해야 한다는 뜻은 아니다. 필요한 책임과 유지 과정을 구분하기 위한 참조다.

## Event History

이벤트 이력은 실행 중 발생한 사실을 시간 순서로 남긴다.

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

이벤트는 "현재 상태" 자체보다 "어떻게 현재 상태가 됐는가"를 설명한다. 이 차이는 복구와 감사에서 중요하다. 예를 들어 현재 상태가 AWAITING_APPROVAL이라는 사실만 저장하면 어떤 행동 승인을 기다리는지 알기 어렵다. 이벤트에는 다음을 남길 수 있다.

~~~text
approval.requested
action: create_pull_request
repository: org/app
base: main
head: feature/fix
requested_at: ...
~~~

## Projection

모델에게 이벤트 이력 전체를 보여주지는 않는다. 상태 관리 계층에서 목적에 따라 필요한 정보를 골라 상태 표현을 만든다.

~~~text
Event History
    │
    ├─→ Current Run State
    ├─→ Goal Progress
    ├─→ Approval State
    ├─→ Artifact Index
    └─→ Context Projection
~~~

이 구조에서 컨텍스트는 상태를 목적에 맞게 보여주는 표현이다. 앞 장의 원칙이 여기서 구체화된다.

~~~text
Durable State
      ↓
Projection
      ↓
Current Context
~~~

## Goal / Progress

목표는 완료를 인정할 조건이다. 진행 상황은 현재 목표에서 어디까지 진행했는지 나타낸다.

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

진행 상황을 모델의 자유 텍스트 요약만으로 관리하지 않는 이유는 완료 판단과 복구에 사용하기 위해서다. 물론 진행 상황 자체도 틀릴 수 있다. 그래서 산출물과 Verification Result를 함께 연결한다.

## Artifact Index

산출물을 상태 관리 계층이 직접 저장할 수도 있고 외부 Storage Reference만 관리할 수도 있다.

예:

~~~text
artifact_id: art-55
type: test_report
uri: object://agent-runs/g100/test-report.json
checksum: ...
verified: true
~~~

중요한 것은 산출물 존재와 Correctness를 분리하는 것이다.

~~~text
Artifact Exists
≠ Artifact Verified
~~~

OSWorld 2.0 같은 Long-horizon 사례에서도 파일이 존재한다는 사실을 결과의 정확성으로 오해하는 실패가 관찰된다.

## Approval State

사람의 승인은 프로세스가 살아 있는 동안만 기다리는 Blocking Call이 아니다. 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)로 표현할 수 있다.

~~~text
approval_id: ap-7
status: pending
action_ref: tool-call-88
requested_by: agent-12
requested_at: ...
~~~

실행 환경은 종료될 수 있다. 승인 이벤트가 오면 새 실행 환경이 실행 재개할 수 있다. 이 구조는 Human-in-the-loop를 정상적인 State Transition으로 만든다.

## External Source Version

에이전트는 외부 정보 원본의 상태 사본(Snapshot: 특정 시점의 상태 사본)을 보고 결정한다. 장시간 작업에서는 정보 원본이 바뀔 수 있다. 따라서 상태 관리 계층에 다음 참조를 남길 가치가 있다.

~~~text
source: git-main
version: abc123

source: approval-policy
version: 41

source: customer-record
version: 812
~~~

이 부가 정보는 이후 상태 재조정(Reconciliation: 현재 외부 상태와 내부 판단을 다시 맞추는 과정)에서 사용된다. "무엇을 봤는가"를 기록하지 않으면 stale decision을 감지하기 어렵다.

## Memory Reference

장기 메모리는 상태 관리 계층 전체가 아니다. 하지만 현재 개별 실행이 어떤 메모리를 사용했는지는 Trace/Audit을 위해 연결할 수 있다.

~~~text
memory_ref:
  mem-101
  mem-202
~~~

이렇게 하면 나중에 잘못된 메모리가 어떤 개별 실행에 영향을 줬는지 추적하기 쉬워진다.

## Event Sourcing을 반드시 써야 하는가

아니다. 에이전트 상태 관리 계층이라는 개념이 Event Sourcing Architecture를 강제하는 것은 아니다. 하지만 이벤트 이력 관점은 몇 가지 장점이 있다.

- 실행 이력을 복구하기 쉽다.
- 외부 상태 변화가 이미 실행됐는지 판단하기 쉽다.
- 승인과 재시도 이유를 추적할 수 있다.
- 투영을 다시 만들 수 있다.
- 감사와 평가 데이터로 활용할 수 있다.

반대로 모든 이벤트를 세밀하게 저장하면 복잡성과 비용이 커진다. 따라서 필요한 수준의 Event Granularity를 선택해야 한다.

## Conversation Log와 Execution History

둘은 일부 겹치지만 같은 것이 아니다. Conversation Log에는 다음이 있을 수 있다.

~~~text
user: PR 만들어줘
assistant: 생성하겠습니다
~~~

실행 이력에는 다음이 필요할 수 있다.

~~~text
tool.proposed
policy.allowed
tool.started
tool.completed
external_id: PR-220
~~~

대화 기록과 실행 이력은 일부 이벤트를 공유할 수 있지만 목적이 다르다. 대화는 모델과 사용자의 상호작용을 보존하고, 실행 이력은 복구와 감사에 필요한 실행 사실을 보존한다.

## Snapshot과 Checkpoint

이벤트가 길어지면 매번 처음부터 투영을 만드는 것이 비효율적일 수 있다. 그래서 상태 사본을 둘 수 있다.

~~~text
Events 1..1000
      ↓
Snapshot @1000
      +
Events 1001..current
~~~

상태 사본은 성능 최적화다. Audit History나 Canonical Event를 없애는 것과는 다르다. 체크포인트(Checkpoint: 실행을 이어가기 위한 상태 기록)는 현재 실행을 이어가기 위한 상태를 Materialize하는 의미로 사용할 수 있다. 이 책에서는 체크포인트를 장기 메모리와 구분한다.

~~~text
Checkpoint
= Execution Continuity

Memory
= Future Reuse
~~~

## State Plane과 Runtime

좋은 구조에서는 실행 환경을 교체할 수 있다.

~~~text
Runtime A
  ↓ crash

State Plane
  ↓ restore

Runtime B
  ↓ resume
~~~

이때 작업 공간까지 완전히 복구해야 하는 작업이라면:

- Git Commit
- Artifact Archive
- Workspace Snapshot
- Rebuild Script

같은 별도 수단이 필요할 수 있다. 상태 관리 계층은 작업 공간 자체와 동일하지 않다.

## State Plane과 Harness

하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)는 상태를 읽고 다음 상태 전환을 만든다.

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

이 관계에서 하네스는 Control Logic이고 상태 관리 계층은 Durable Record다. 둘을 분리하면 하네스를 Upgrade하거나 Restart해도 상태를 유지할 수 있다.

## State Plane과 Software Factory Control Plane

여기서 경계를 명확히 해야 한다. 에이전트 상태 관리 계층은 한 에이전트 Run/Goal의 실행 연속성을 다룬다. 소프트웨어 팩토리의 제어 계층은 여러 작업 항목과 그 작업을 수행하는 주체를 함께 관리한다.

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

운영 시스템에서는 두 계층이 연결될 수 있다. 하지만 개념적으로 분리해야 책임이 명확해진다.

## 작은 예: 승인 후 PR 생성

에이전트가 코드를 수정하고 테스트까지 통과했다. PR 생성은 외부 쓰기라 승인이 필요하다. 이벤트 흐름을 보자.

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

중간 프로세스가 존재하지 않아도 된다. 실행의 연속성이 상태 관리 계층에 있기 때문이다.

## State Plane에 너무 많은 것을 넣지 않는다

상태 관리 계층을 만들기 시작하면 모든 데이터를 넣고 싶어진다. 하지만 다음은 분리할 수 있다.

- 대용량 Raw Log → Artifact Storage
- 저장소 전체 → Git
- User Profile 전체 → Identity/Profile System
- Long-term Knowledge → Memory Store
- External Canonical Data → Source System

상태 관리 계층은 참조와 실행에 필요한 부가 정보를 유지하면 된다. 핵심은 기준 원본의 모든 내용을 복제하려는 것이 아니다. 실행의 연속성을 유지하는 것이다.

## 이 장에서 가져갈 것

에이전트 상태 관리 계층은 이 책 전체에서 반복해서 사용할 설명용 개념이다.

다시 정의하면:

> **에이전트 상태 관리 계층은 에이전트가 프로세스, 실행 환경, 컨텍스트를 잃어도 실행 이력과 현재 목표, 진행 상황, 승인, 산출물, External Source Reference를 바탕으로 작업을 이어갈 수 있게 하는 상태 관리 계층이다.**

이 정의에서 중요한 것은 저장 기술이 아니다. 책임 경계다. 다음 장에서는 상태 관리 계층이 Failure Recovery에 어떻게 사용되는지 다룬다. 특히 Replay를 "모든 것을 다시 실행하는 것"으로 오해하면 어떤 문제가 생기는지, External Side Effect를 중복 없이 복구하려면 무엇이 필요한지 살펴본다.

## 주요 근거

- Temporal Durable Execution
- LangGraph Persistence
- Anthropic Managed Agents
- OpenAI Agents SDK Sessions
- research/topics/18-durable-state-event-log-replay.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
