# Part III. Agent State Plane

Part III는 이 책의 중심부다.

Context Window를 오래 유지하는 것과 실행 상태를 durable하게 유지하는 것을 분리하고, Crash Recovery와 Long-running, External State Reconciliation을 하나의 흐름으로 연결한다.

<!-- source-draft: chapters/07/draft.md -->

## 7장. Session, Workspace, Goal, Memory를 분리한다

Agent를 오래 실행하기 시작하면 거의 모든 문제가 "상태"라는 이름 아래 모인다.

대화 기록도 상태다. 현재 작업 디렉터리도 상태다. 완료해야 할 목표도 상태다. 생성한 파일도 상태다. 이전 실행에서 배운 내용도 상태다.

문제는 이들을 같은 것으로 취급할 때 생긴다.

Session을 지우면 Goal이 사라지고, Runtime이 종료되면 Progress가 사라지고, 오래된 Memory가 현재 사실보다 우선하고, Conversation Summary가 실행 이력을 대신하게 된다.

Long-running Agent를 설계하려면 먼저 **서로 다른 수명과 권한을 가진 상태를 분리해야 한다.**

### "Memory"라는 단어가 너무 많은 것을 가린다

Agent 제품에서는 다음 기능을 모두 Memory라고 부르는 경우가 있다.

- Conversation History
- User Preference
- Current Task Progress
- Previous Tool Result
- Workspace File
- Long-term Lesson
- Retrieved Document

사용자 경험 관점에서는 이해하기 쉬운 표현일 수 있다.

Architecture에서는 위험하다.

각 항목의 수명과 신뢰도가 다르기 때문이다.

이 책에서는 다음을 구분한다.

~~~text
Inference Context
Conversation / Session State
Run State
Workspace State
Goal State
Artifact State
Long-term Memory
External Source of Truth
~~~

이 taxonomy는 업계 표준이 아니라 여러 SDK와 Runtime 구현에서 반복되는 lifecycle과 authority 차이를 설명하기 위한 working model이다.

### Inference Context

Context는 현재 한 번의 Model Inference에 들어가는 정보다.

앞 장에서 본 것처럼 Context는 Projection이다.

~~~text
State / Sources
      ↓
Context Selection
      ↓
Inference Context
~~~

Context는 일시적이다.

다음 Turn에는 다른 정보가 들어갈 수 있다.

### Conversation / Session State

Session은 여러 Turn의 대화 연속성을 유지한다.

예:

~~~text
User Message
Assistant Message
Tool Call
Tool Result
User Correction
~~~

Session은 매우 유용하다.

하지만 Session이 Goal이나 Runtime State 전체를 의미하지는 않는다.

예를 들어 사용자와 20 Turn을 대화했다고 해서 현재 Goal의 Completion Condition이 명확하게 구조화돼 있다는 보장은 없다.

Session History에는 "테스트가 통과했다"고 적혀 있어도 Artifact나 Test Result가 현재 유효한지는 별도 확인해야 한다.

### Run State

Run State는 현재 실행의 lifecycle을 표현한다.

예:

~~~text
READY
RUNNING
AWAITING_INPUT
AWAITING_APPROVAL
VERIFYING
COMPLETED
FAILED
~~~

Run State는 Conversation보다 시스템 제어에 가깝다.

모델이 자연어로 "승인 대기 중입니다"라고 말하는 것과 시스템 상태가 AWAITING_APPROVAL인 것은 다르다.

후자는 Scheduler나 API가 deterministic하게 처리할 수 있다.

### Workspace State

Workspace는 실행환경의 상태다.

예:

- checked-out repository
- modified file
- installed package
- browser tab
- temporary build artifact
- local cache

Workspace는 편리하지만 durable하다고 가정하면 안 된다.

Cloud Runtime, Container, MicroVM은 종료될 수 있다.

~~~text
Workspace Exists
≠ Durable State Exists
~~~

AWS AgentCore 같은 Runtime 사례도 Session별 격리 환경을 제공한다. 기본 microVM의 memory와 local disk는 compute lifecycle에 묶이지만, 2026-10-02 기준 별도 managed session storage를 구성하면 stop/resume 사이에 filesystem을 복원할 수 있다. 다만 이 storage도 session lifecycle과 runtime version에 제약을 받으므로 Goal, Approval, Long-term Memory 같은 Durable State와 동일하게 취급하지 않는다.

따라서 Workspace가 유지될 수 있더라도 실행 연속성의 유일한 근거로 삼지 않는 편이 복구에 유리하다.

### Goal State

Goal은 Agent가 무엇을 완료해야 하는지 표현한다.

예:

~~~text
objective
scope
constraints
budget
completion condition
verification requirement
~~~

Goal을 단순 User Prompt와 동일시하지 않는다.

사용자 Prompt가 다음과 같다고 하자.

> 로그인 오류 좀 고쳐줘.

실행 Goal은 더 구체적이어야 할 수 있다.

~~~text
Objective:
OAuth callback 오류 수정

Scope:
auth module only

Verification:
targeted test + integration test pass

Do not:
change public API

Budget:
max 30 tool turns
~~~

Goal은 현재 실행의 Completion Contract다.

### Artifact State

Artifact는 Agent가 만든 결과물이다.

예:

- file
- commit
- report
- screenshot
- generated document
- structured output

Artifact는 "완료했다"는 말과 다르다.

Artifact에는 다음 Metadata가 필요할 수 있다.

- location
- checksum
- created_at
- source run
- verification state
- version

특히 장기 Agent에서는 Artifact가 다음 Session의 Handoff 역할도 한다.

### Long-term Memory

Memory는 미래 실행에서 재사용할 정보를 보존한다.

예:

- 사용자의 선호
- 특정 Repository의 반복되는 작업 규칙
- 이전 해결에서 얻은 Lesson
- Agent가 자주 실수하는 Pattern

Memory는 현재 실행의 복구 상태를 담는 기본 저장소로 보지 않는다.

~~~text
Checkpoint
= 현재 실행을 이어가기 위한 것

Memory
= 미래 실행에 재사용할 것
~~~

둘은 목적이 다르다.

### External Source of Truth

가장 중요한 상태가 Agent 내부에 없을 수도 있다.

예:

- 현재 Git HEAD
- Production Configuration
- Approved Requirement
- Current DB Record
- 최신 승인 상태
- 현재 가격
- 실제 배포 상태

이런 정보는 Agent가 소유하지 않는다.

Agent가 내부 State나 Memory에 복사해 둘 수는 있지만 복사본이 Canonical Source가 되지는 않는다.

~~~text
Working Copy
≠ Source of Truth
~~~

이 구분은 11장의 External State Reconciliation에서 중요해진다.

### 같은 정보도 수명이 다르다

하나의 정보가 여러 형태로 존재할 수 있다.

예를 들어 "현재 Branch는 feature/auth-fix"라는 사실을 생각해보자.

~~~text
Workspace:
git branch에서 실제 확인한 현재 값

Run State:
이 Run이 feature/auth-fix에서 시작했다고 기록

Context:
현재 Turn에서 Model에게 branch 정보를 제공

Memory:
"이 Repository는 feature branch를 사용한다"라는 과거 Lesson
~~~

시간이 지나 Branch가 바뀌면 이 값들은 서로 달라질 수 있다.

그래서 State에는 단순 Value뿐 아니라 다음 Metadata가 중요하다.

- source
- version
- timestamp
- owner
- scope
- freshness
- invalidation condition

### State Promotion

모든 Observation을 Durable State로 저장할 필요는 없다.

예를 들어 Shell Tool이 출력한 수천 줄 Log를 영구 저장하는 것은 과할 수 있다.

여기서는 편의상 Observation을 더 오래 유지되는 State로 옮기는 과정을 State Promotion이라고 부른다.

~~~text
Ephemeral Observation
        ↓
Working State
        ↓
Checkpoint-worthy State
        ↓
Durable Goal / Artifact
        ↓
Optional Long-term Memory
~~~

Promotion 기준은 다음과 같을 수 있다.

- Recovery에 필요한가.
- Audit에 필요한가.
- Completion 판단에 필요한가.
- 다시 계산하기 비싼가.
- 다음 Session에서도 필요할 가능성이 높은가.
- 사용자의 명시적 Correction인가.

이 기준이 없으면 Agent System은 모든 것을 저장하거나 중요한 것을 놓치는 두 극단으로 가기 쉽다.

### Freshness와 Validity

State는 저장돼 있다고 유효한 것이 아니다.

예를 들어 다음 Memory가 있다고 하자.

~~~text
Production DB host = db-prod-1
~~~

몇 달 뒤 실제 환경은 db-prod-2로 바뀌었다.

Memory가 존재한다는 사실은 정확성을 보장하지 않는다.

따라서 State는 가능한 한 freshness와 invalidation rule을 가져야 한다.

예:

~~~text
source: infra-config
observed_version: 184
observed_at: 2026-10-02T10:20
valid_until: unknown
refresh_before: production_mutation
~~~

### Session을 Goal로 사용하면 생기는 문제

Goal을 Conversation에만 의존하면 다음 일이 생긴다.

사용자가 처음에 요구한다.

> 테스트를 고쳐줘.

중간에 다음 Correction을 준다.

> public API는 바꾸지 마.

Agent가 Compaction을 수행하면서 두 번째 조건이 Summary에서 약해질 수 있다.

Goal이 별도 구조라면 Constraint를 명시적으로 유지할 수 있다.

~~~text
Goal
objective: fix failing test
constraint:
  - public API must not change
~~~

Conversation은 Goal을 수정하는 Input이 될 수 있다.

Goal 자체와 동일하지 않다.

### Workspace를 Checkpoint로 사용하면 생기는 문제

Agent가 Local File을 수정했다.

프로세스가 죽었다.

Workspace가 유지돼 있다면 운 좋게 이어갈 수 있다.

하지만 다음 정보를 알 수 없을 수 있다.

- 수정이 완료된 것인가.
- Test는 실행했는가.
- 어떤 Tool Result를 기준으로 수정했는가.
- External Mutation은 이미 했는가.
- 다음 Step은 무엇인가.

Workspace는 실제 변경을 담지만 Execution Intent를 설명하지 않는다.

그래서 Durable State가 따로 필요하다.

### Memory를 Source of Truth로 사용하면 생기는 문제

Memory는 과거 정보를 재사용하기 위한 내부 데이터이고, External Source of Truth는 현재의 Canonical Data다. 둘이 충돌하면 기본적으로 최신 Authoritative Source를 다시 확인해야 한다.

이 원칙의 운영 측면은 11장의 Reconciliation에서, Memory 자체의 lifecycle과 security는 Part IV에서 자세히 다룬다.

### 작은 예: Coding Agent의 State

하나의 Coding Task를 분해해보자.

~~~text
Goal
- UserService timeout bug 수정
- 관련 test pass

Session
- 사용자와의 대화
- 추가 요구사항

Run State
- RUNNING

Workspace
- branch feature/timeout-fix
- modified UserService.java

Artifact
- commit candidate
- test report

Memory
- 이 Repository는 integration test가 느리다는 과거 Lesson

External Source
- current remote main HEAD
- current CI configuration
~~~

이 분리를 하면 어떤 State를 어디에서 복구해야 하는지 선명해진다.

### 이 장에서 가져갈 것

Agent에서 "State"라는 단어 하나로 모든 것을 설명하면 Lifecycle과 Trust Boundary가 섞인다.

최소한 다음 경계를 유지한다.

~~~text
Context
≠ Session
≠ Run
≠ Workspace
≠ Goal
≠ Artifact
≠ Memory
≠ Source of Truth
~~~

다음 질문은 자연스럽다.

이렇게 분리한 상태를 어디에서 관리할 것인가.

프로세스가 죽고 Runtime이 교체돼도 Goal과 Progress, Approval과 Artifact를 잃지 않으려면 어떤 계층이 필요할까.

다음 장에서는 이 책의 핵심 synthesis인 Agent State Plane을 다룬다.

### Source Notes

- [S-OAI-AGENTS]
- [S-GOOGLE-ADK]
- [S-AWS-AGENTCORE-RUNTIME]

---

<!-- source-draft: chapters/08/draft.md -->

## 8장. Agent State Plane

Agent가 5분짜리 작업만 한다면 Process Memory와 Conversation History만으로도 충분할 수 있다.

문제는 작업이 길어질 때 시작된다.

Agent가 코드를 수정하고 테스트를 돌린다. 승인 대기 상태로 들어간다. 몇 시간 뒤 사람이 승인한다. 그 사이 Runtime은 종료됐다. 새 Runtime에서 Agent를 다시 시작해야 한다.

이때 "이전 대화를 요약해서 다시 넣자"만으로 충분할까.

이미 어떤 Tool이 실행됐는지, 어떤 Side Effect가 성공했는지, 어떤 Artifact가 만들어졌는지, 어떤 Source Version을 기준으로 결정했는지 알아야 한다면 부족하다.

이 책에서는 이런 실행 연속성을 담당하는 계층을 **Agent State Plane**이라고 부른다.

이 용어는 외부 표준명이 아니다. 여러 Agent SDK, Durable Execution, Long-running Harness 사례에서 반복되는 책임을 설명하기 위해 이 책에서 사용하는 synthesis다.

### Agent State Plane이 해결하려는 문제

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

### State Plane은 하나의 Database를 의미하지 않는다

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

### Reference 구성

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

모든 시스템이 이 항목을 각각 별도 Table이나 Service로 구현해야 한다는 뜻은 아니다. 필요한 책임과 lifecycle을 구분하기 위한 Reference다.

### Event History

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

### Projection

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

### Goal / Progress

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

그래서 Artifact와 Verification Result를 함께 연결한다.

### Artifact Index

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

OSWorld 2.0 같은 Long-horizon 사례에서도 파일이 존재한다는 사실을 결과의 정확성으로 오해하는 실패가 관찰된다.

### Approval State

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

### External Source Version

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

### Memory Reference

Long-term Memory는 State Plane 전체가 아니다.

하지만 현재 Run이 어떤 Memory를 사용했는지는 Trace/Audit을 위해 연결할 수 있다.

~~~text
memory_ref:
  mem-101
  mem-202
~~~

이렇게 하면 나중에 잘못된 Memory가 어떤 Run에 영향을 줬는지 추적하기 쉬워진다.

### Event Sourcing을 반드시 써야 하는가

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

### Conversation Log와 Execution History

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

Conversation History와 Execution History는 일부 Event를 공유할 수 있지만 목적이 다르다. Conversation은 모델과 사용자의 상호작용을 보존하고, Execution History는 복구와 Audit에 필요한 실행 사실을 보존한다.

### Snapshot과 Checkpoint

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

### State Plane과 Runtime

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

### State Plane과 Harness

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

### State Plane과 Software Factory Control Plane

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

운영 시스템에서는 두 계층이 연결될 수 있다.

하지만 개념적으로 분리해야 책임이 명확해진다.

### 작은 예: 승인 후 PR 생성

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

### State Plane에 너무 많은 것을 넣지 않는다

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

### 이 장에서 가져갈 것

Agent State Plane은 이 책 전체에서 반복해서 사용할 synthesis다.

다시 정의하면:

> **Agent State Plane은 Agent가 Process, Runtime, Context를 잃어도 실행 이력과 현재 목표, Progress, Approval, Artifact, External Source Reference를 바탕으로 작업을 이어갈 수 있게 하는 상태 관리 계층이다.**

이 정의에서 중요한 것은 저장 기술이 아니다.

Responsibility Boundary다.

다음 장에서는 State Plane이 Failure Recovery에 어떻게 사용되는지 다룬다.

특히 Replay를 "모든 것을 다시 실행하는 것"으로 오해하면 어떤 문제가 생기는지, External Side Effect를 중복 없이 복구하려면 무엇이 필요한지 살펴본다.

### Source Notes

- [S-TEMPORAL]
- [S-LANGGRAPH-PERSIST]
- [B-STATE-PLANE]

---

<!-- source-draft: chapters/09/draft.md -->

## 9장. 실패 후 이어가는 Agent

Agent가 External API를 호출했다.

API는 성공했다.

그 직후 Agent Process가 죽었다.

새 Process가 시작됐다. 마지막으로 저장된 Context에는 API 성공 결과가 없다.

Agent는 같은 Action을 다시 실행해야 할까.

이 질문은 Long-running Agent에서 가장 위험한 Recovery 문제 중 하나다.

실행을 이어간다는 것은 이전 Prompt를 다시 넣는 것과 다르다. 이미 일어난 Side Effect와 아직 일어나지 않은 Side Effect를 구분해야 한다.

### Recovery와 Retry는 다르다

Retry는 같은 논리 작업을 다시 시도하는 동작이다. Recovery는 시스템이 중단된 뒤 **현재 상태를 다시 구성하고 안전한 다음 Action을 결정하는 과정**이며, 그 결과로 Retry를 선택할 수도 있다.

~~~text
Retry
= operation attempt again

Recovery
= reconstruct state
  + determine what already happened
  + decide next safe step
~~~

두 개념을 섞으면 중복 Side Effect가 생길 수 있다.

### Replay는 재실행이 아니다

Durable Execution 시스템에서는 Event History를 Replay해 Workflow State를 복구하는 방식이 널리 사용된다.

Agent에 이 개념을 가져올 때 주의해야 한다.

LLM Inference와 External Tool을 무조건 다시 실행하면 안 된다.

~~~text
Replay
≠ Re-run Model
≠ Re-run External Side Effect
~~~

대신 과거 결과를 기록해두고 그 기록으로 State를 재구성한다.

예:

~~~text
model.completed
tool.proposed
tool.authorized
tool.started
tool.completed
~~~

Recovery 시 tool.completed Event가 있다면 해당 Operation을 다시 실행할 필요가 없을 수 있다.

### 왜 Model Call도 그대로 Replay하지 않는가

LLM 호출은 같은 Input에서도 결과가 달라질 수 있고 Model Version도 바뀔 수 있다. 따라서 과거 실행 상태를 복구할 때는 당시 Model Result를 다시 생성하려 하기보다 기록된 결과를 Execution History의 사실로 사용하는 편이 안전하다.

~~~text
model.requested
model.completed:
  output_ref
  model_version
  context_ref
~~~

Recovery 후 새로운 판단이 필요하면 그것은 새로운 Model Call이다.

과거 Call의 재현이 아니다.

### Side Effect는 가장 조심해야 한다

다음 Tool을 생각해보자.

~~~text
send_email
create_issue
charge_payment
deploy_release
merge_pull_request
~~~

이들은 중복 실행 비용이 크다.

예를 들어 create_issue가 실제 서버에서는 성공했지만 Client가 Timeout을 받았다.

Agent는 실패라고 생각할 수 있다.

바로 Retry하면 같은 Issue가 두 개 만들어질 수 있다.

그래서 External Mutation에는 가능한 한 Idempotency가 필요하다.

### Idempotency Key

논리적으로 같은 Operation에 같은 Key를 사용한다.

예:

~~~text
goal_id + operation_type + logical_operation_id
~~~

예를 들어:

~~~text
G-100:create_issue:bug-report-1
~~~

Server가 Idempotency를 지원하면 같은 Key로 다시 요청해도 기존 결과를 반환할 수 있다.

Server가 지원하지 않는다면 Harness가 External ID나 실행 Record를 확인해 중복 여부를 판단해야 한다.

Agent Harness만으로 exactly-once semantics를 쉽게 보장할 수 있다고 가정하지 않는다.

### Tool Execution State

External Tool Call은 최소한 다음 Lifecycle을 기록할 수 있다.

~~~text
PROPOSED
AUTHORIZED
STARTED
COMPLETED
FAILED
UNKNOWN
~~~

UNKNOWN이 중요하다.

Client가 Timeout됐는데 Server 결과를 모르는 상태다.

이때 단순 Retry보다 먼저 External System을 조회해야 할 수 있다.

~~~text
UNKNOWN
   ↓
Query External State
   ├─ Already Applied → mark COMPLETED
   └─ Not Applied → retry
~~~

### Crash Point를 생각한다

하나의 Tool Call에는 여러 Crash Point가 있다.

~~~text
1. before request
2. request sent
3. server applied action
4. response returned
5. event persisted
~~~

3과 5 사이에서 Crash가 나면 가장 까다롭다.

외부 Side Effect는 발생했지만 내부 State는 기록되지 않았다.

이 문제를 완전히 없애기 어렵다.

그래서:

- idempotency
- external operation id
- reconciliation
- transaction/outbox pattern
- explicit UNKNOWN state

같은 기법이 필요해진다.

### Pause / Resume

Recovery는 Crash만을 의미하지 않는다.

Human Approval이나 User Input을 기다리는 Pause도 같은 구조를 사용한다.

~~~text
RUNNING
  ↓
approval.requested
  ↓
PAUSED
  ↓
approval.granted
  ↓
RESUMED
~~~

Resume 시점에는 다음을 다시 확인해야 할 수 있다.

- Approval 대상 Action이 여전히 유효한가.
- External Source가 바뀌지 않았는가.
- Credential Scope가 아직 유효한가.
- Runtime을 새로 만들어야 하는가.

따라서 Resume는 "이전 다음 Step을 그대로 실행"하는 것이 아니다.

새로운 Current State에서 Pending Intent를 재검증한다.

### Retry Budget

Recovery 후에도 실패가 반복될 수 있다.

Retry Count를 State에 저장해야 하는 이유다.

~~~text
operation: run_test
attempt: 3
last_failure: timeout
budget_remaining: 1
~~~

Process Memory에만 Retry Count가 있으면 Restart할 때 다시 0으로 돌아가 무한 반복할 수 있다.

### Snapshot

Event History가 커지면 매번 처음부터 State를 재구성하는 비용이 커진다.

Snapshot을 사용할 수 있다.

~~~text
Snapshot @ event 500
+
Events 501..current
~~~

Snapshot에는 현재 Projection을 저장한다.

예:

- Run State
- Goal Progress
- Pending Approval
- Artifact References
- Retry Counters

Snapshot이 있어도 중요한 Event History를 바로 삭제해야 하는 것은 아니다.

Retention과 Audit 요구에 따라 결정한다.

### Schema Versioning

Agent System이 발전하면 Event Schema도 바뀐다.

예:

~~~text
tool.completed v1
tool.completed v2
  + external_operation_id
~~~

Old Run을 복구하려면 Version 호환이 필요하다.

Event에는 다음 Metadata가 유용하다.

~~~text
event_type
event_version
event_id
run_id
timestamp
actor
causation_id
correlation_id
payload
harness_version
policy_version
~~~

모든 시스템이 같은 필드를 가져야 한다는 의미는 아니다.

Recovery와 Audit에 필요한 최소 Metadata를 설계해야 한다.

### Deterministic Rule과 Model Decision을 나눈다

Recovery에서는 가능한 한 알려진 규칙을 시스템이 처리한다.

예:

~~~text
Tool COMPLETED
→ do not execute again

Approval REJECTED
→ do not resume action

Retry budget exhausted
→ block

Source version changed
→ reconcile
~~~

반면 다음은 Model 판단이 필요할 수 있다.

- 실패 원인 분석
- 대안 구현
- Conflict 해결 전략
- 새로운 Plan

이 분리는 Agent를 더 예측 가능하게 만든다.

### 작은 예: PR 생성 중 Crash

상황:

~~~text
Goal:
bug fix 완료 후 PR 생성

State:
tests passed

Action:
create_pull_request
~~~

Agent가 요청을 보낸 뒤 Network Timeout이 발생했다.

나쁜 Recovery:

~~~text
Restart
→ "PR 생성이 실패했다"
→ create_pull_request again
~~~

좋은 Recovery:

~~~text
tool.started
external_operation_id: op-77
response: unknown
        ↓
Restart
        ↓
Query GitHub for matching PR
        ├─ Found PR #220
        │    ↓
        │ mark tool.completed
        │
        └─ Not Found
             ↓
          safe retry with same logical operation
~~~

핵심은 Internal Error만 보고 External Reality를 추정하지 않는 것이다.

### Recovery는 State Plane의 품질을 드러낸다

Short Task에서는 State 설계가 약해도 문제가 잘 보이지 않는다.

Agent가 한 Process 안에서 끝나기 때문이다.

Crash, Approval, Long Pause가 들어오면 설계가 드러난다.

복구를 위해 매번 Conversation Transcript를 사람이 읽어야 한다면 Durable Execution 구조가 부족한 것이다.

### 이 장에서 가져갈 것

Agent Recovery의 핵심은 "다시 시작한다"가 아니다.

> **이미 일어난 일과 아직 일어나지 않은 일을 구분한 뒤, 현재 외부 상태에서 다음 안전한 Action을 결정하는 것**이다.

그래서 다음 경계를 유지한다.

~~~text
Replay
≠ Side-effect Re-execution

Retry
≠ Recovery

Internal Failure
≠ External Action Failure
~~~

다음 장에서는 더 긴 시간축을 본다.

Process가 한두 번 실패하는 수준을 넘어, 수십 분에서 수 시간 동안 많은 Item과 Milestone을 추적해야 할 때 Agent가 왜 Context와 Plan을 잃는지 살펴본다.

### Source Notes

- [S-TEMPORAL]
- [B-STATE-PLANE]

---

<!-- source-draft: chapters/10/draft.md -->

## 10장. Long-running Agent

짧은 Task에서는 Agent가 꽤 유능해 보인다.

파일 하나를 고친다. 테스트 하나를 실행한다. 문서 한 장을 만든다.

작업이 한 시간을 넘어가면 다른 문제가 나타난다.

Agent가 무엇을 하려 했는지 잊는다. 이미 확인한 항목을 다시 확인한다. 일부 Item만 처리하고 전체가 끝났다고 판단한다. Search와 준비 작업에 시간을 너무 많이 써 핵심 업무를 시작하지 못한다. 작업 도중 외부 상태가 바뀌었는데 처음 만든 Plan을 계속 따른다.

Long-running Agent의 문제는 단순히 더 오래 reasoning하는 문제가 아니다.

**시간이 길어질수록 상태와 목표를 잃지 않는 문제**다.

### Context Window가 크면 해결되는가

Context Window가 커지면 도움이 된다.

더 많은 History와 Artifact를 볼 수 있다.

하지만 다음 문제는 남는다.

- 오래된 State가 계속 남는다.
- External World가 바뀐다.
- 많은 Item을 누락 없이 추적해야 한다.
- 이미 완료한 Action과 Pending Action을 구분해야 한다.
- Context가 커져도 중요한 정보의 우선순위가 자동으로 생기지는 않는다.

따라서:

~~~text
Long Context
≠ Long-running Execution
~~~

이다.

### Long-running Task의 특징

장기 Task는 단순히 Step 수가 많다는 것 이상이다.

예를 들어 대학 행정 Agent가 여러 학생의 장학 심사 보조를 한다고 하자.

각 학생마다 다음 State가 다를 수 있다.

~~~text
Student A
- document complete
- advisor approval pending

Student B
- document missing

Student C
- approval complete
- final notification pending
~~~

Agent는 여러 Item의 State를 동시에 유지해야 한다.

중간에 새로운 문서가 들어올 수도 있다.

이런 문제는 단일 대화 Memory만으로 안정적으로 관리하기 어렵다.

### OSWorld 2.0에서 드러나는 문제

2026년 OSWorld 2.0은 기존 Desktop Agent Benchmark보다 훨씬 긴 Workflow를 포함한다.

사람이 수행해도 상당한 시간이 필요한 Task가 포함돼 있고, 많은 Tool/Action이 이어진다.

이 환경에서 중요한 Challenge로 다음이 드러난다.

- Implicit-state Inference
- Multi-item State Tracking
- Conflict Disambiguation
- Dynamic Environment
- Cross-source Reasoning

Agent Engineering 관점에서 보면 GUI Click Accuracy보다 State Management 문제가 전면에 나온다.

### Milestone

Long-running Goal을 하나의 자유로운 Loop로만 처리하면 Progress 판단이 어려워진다.

Milestone을 둘 수 있다.

예:

~~~text
Goal:
지원자 50명의 제출 자료를 확인하고 누락자를 정리

Milestone 1:
source 목록 확보

Milestone 2:
50명 state table 생성

Milestone 3:
각 지원자 검증

Milestone 4:
누락 목록 재검증

Milestone 5:
final artifact 생성
~~~

Milestone은 rigid planner가 모든 Step을 미리 정한다는 뜻이 아니다.

Completion Surface를 나눈다는 의미다.

### Working State Table

Multi-item Task에서는 자연어 Summary보다 구조화된 Working State가 유용하다.

예:

~~~text
id | status | source_version | blocker | verified
A  | ready  | 12             | -       | true
B  | wait   | 8              | doc     | false
C  | done   | 15             | -       | true
~~~

이 Table은 Context에 전부 넣을 필요가 없다.

State Plane에 두고 필요한 Slice만 Projection할 수 있다.

이 구조가 누락을 줄이는 데 도움이 된다.

### Hidden State

Long-running Task의 어려움 중 하나는 Task Instruction에 모든 정보가 없다는 것이다.

Agent는 다음을 찾아야 할 수 있다.

- 이전 승인
- 과거 Submission
- 다른 App의 Record
- 저장된 Draft
- 최신 Message

즉 Goal을 이해하려면 Environment 안의 Hidden State를 복구해야 한다.

이때 "사용자가 말한 것만 따르면 된다"는 접근으로는 부족하다.

Agent는 Source Registry와 Discovery Strategy가 필요할 수 있다.

### Phase Budget

장기 Agent는 준비 작업에 Horizon을 소진할 수 있다.

예를 들어 환불 처리 Task인데 Agent가:

- 관련 정책 검색
- 브라우저 설정
- 도움말 탐색
- 툴 사용법 조사

에 대부분의 Step을 쓰고 환불 시스템에는 늦게 접근할 수 있다.

이를 막기 위해 Phase Budget을 둘 수 있다.

~~~text
Discovery
→ 필요한 범위에서 제한

Execution
→ 핵심 작업에 충분한 budget 확보

Verification
→ 마지막까지 별도 reserve 유지
~~~

구체적인 비율은 Task와 비용 구조에 따라 달라진다. 핵심은 전체 Budget만 두지 말고 탐색, 실행, 검증이 서로의 자원을 소진하지 않게 관리하는 것이다.

### Verification Reserve

Agent가 마지막 Step까지 구현에만 사용하면 검증할 Budget이 없다.

그래서 Verification을 마지막에 "남으면 하는 일"로 두지 않는다.

~~~text
Total Budget
  ├─ Discovery
  ├─ Execution
  └─ Verification Reserve
~~~

특히 High-impact Task에서는 Verification Budget을 별도 확보하는 것이 유용하다.

### Premature Completion

Long-running Agent는 일부 Item이 끝났는데 전체 Goal이 끝났다고 판단할 수 있다.

예:

~~~text
50개 중 47개 처리
→ output file generated
→ "완료"
~~~

이 실패를 막으려면 Completion Condition이 Item Coverage와 연결돼야 한다.

~~~text
expected_items = 50
verified_items = 50
unresolved_items = 0
~~~

가능하면 Model의 감각보다 deterministic invariant를 사용한다.

### Progress Artifact

Session이 바뀌어도 다음 Agent가 이어받을 수 있는 Artifact를 남기는 패턴이 유용하다.

예:

- progress.json
- task checklist
- verified item table
- current plan
- test report

Anthropic의 Long-running Harness 사례에서도 Session 간 Continuity를 위해 incremental progress와 external artifact를 남기는 패턴이 사용됐다.

핵심은 형식이 아니라 **작업 상태를 Model Context 밖에도 남긴다는 점**이다.

### Clarification은 실패가 아니다

Autonomous Agent를 만들다 보면 질문하지 않는 Agent가 더 좋은 것처럼 보일 수 있다.

하지만 장기 업무에서는 불확실한 값을 추정하는 것이 더 위험할 수 있다.

예:

~~~text
배송 주소가 두 개 있음
최신 승인자가 불명확함
정책 문서 두 개가 충돌함
~~~

이때 올바른 Action은 사용자에게 질문하거나 Block하는 것일 수 있다.

~~~text
Autonomy
=
Act when justified
+
Stop when not justified
~~~

라고 보는 편이 낫다.

### Dynamic Environment

가장 중요한 문제 중 하나다.

Agent가 T0에 Source를 읽었다.

작업 중 T1에 새로운 Message가 도착했다.

초기 Plan은 더 이상 유효하지 않을 수 있다.

~~~text
T0
Read Source
→ Build Plan

T1
Source Changes

T2
Execute Old Plan
~~~

Long-running Agent가 실패하는 전형적인 패턴이다.

그래서 특정 Event나 Milestone에서 Source를 Refresh해야 한다.

이것이 다음 장의 External State Reconciliation이다.

### State Horizon

장기 Task 난이도를 단순 Action Count로만 볼 필요는 없다.

Task에서 중요한 State가 얼마나 오래 유지돼야 하고, 얼마나 많은 Transition을 거쳐 마지막 Decision까지 영향을 주는가도 중요하다.

2026년 공개된 preprint에서는 이런 관점을 Task-State Horizon으로 정의하고 별도 benchmark로 측정하려는 시도가 있다.

아직 일반적인 표준 Metric은 아니다.

하지만 "Step이 많다"보다 "오래된 State Dependency를 얼마나 오래 정확히 유지해야 하는가"를 보는 관점은 Agent 설계에 유용하다.

### 작은 예: 50개 요청 처리

Goal:

> 50개의 요청을 검토하고 승인 가능한 요청만 처리하라.

나쁜 구조:

~~~text
Conversation
→ 요청 하나씩 처리
→ Summary
→ 계속
~~~

문제:

- 몇 개 처리했는지 불명확
- 중복 처리 가능
- Source Update 누락
- Pending/Blocked Item 누락

더 나은 구조:

~~~text
Goal
 ↓
Item Registry
 ↓
Per-item State
 ↓
Milestone
 ↓
Action
 ↓
Verification
 ↓
Refresh Trigger
 ↓
Completion Invariant
~~~

이렇게 하면 Long-running Execution을 대화 지속 문제가 아니라 State Management 문제로 다룰 수 있다.

### 이 장에서 가져갈 것

Long-running Agent의 핵심은 Context Window를 크게 만드는 것이 아니다.

> **시간이 지나고 Environment가 변해도 Goal, Progress, Item State, Verification 기준을 잃지 않는 것**이다.

이를 위해:

- Milestone
- Working State
- Progress Artifact
- Phase Budget
- Verification Reserve
- Clarification
- Refresh Trigger

가 필요할 수 있다.

다음 장에서는 이 중 가장 중요한 Dynamic Environment 문제를 좁혀본다.

Agent가 과거 Snapshot을 기준으로 만든 Decision을 External Source가 바뀐 뒤에도 계속 실행해도 되는가.

External State Reconciliation을 다룬다.

### Source Notes

- [S-ANTHROPIC-HARNESS]
- [S-OSWORLD2]
- [S-TSH]

---

<!-- source-draft: chapters/11/draft.md -->

## 11장. External State Reconciliation

Agent가 오전 10시에 승인 상태를 읽었다.

~~~text
refund_limit = 100
~~~

오전 10시 20분에 정책이 바뀌었다.

~~~text
refund_limit = 50
~~~

Agent는 오전 10시의 State를 기준으로 80달러 환불 Action을 준비하고 있다.

이 Action을 그대로 실행해도 될까.

Long-running Agent에서 내부 Working State는 언제든 오래될 수 있다.

그래서 중요한 Action을 실행하기 전에 **현재 외부 상태와 내부 판단을 다시 맞추는 과정**이 필요하다.

이 책에서는 이를 External State Reconciliation이라고 부른다.

### Working State는 Snapshot이다

Agent가 External Source를 읽으면 내부 Projection을 만든다.

~~~text
External Source @ T0
        ↓
Working State
        ↓
Plan / Decision
~~~

문제는 T1에 External Source가 바뀔 수 있다는 것이다.

~~~text
T0 read
T1 source changed
T2 old decision executed
~~~

Working State는 Source of Truth가 아니다.

관찰 시점의 Snapshot이다.

### Refresh와 Reconciliation은 다르다

Refresh는 최신 Source를 다시 읽는 것이다.

Reconciliation은 읽은 최신 State가 기존 Decision에 어떤 영향을 주는지 판단하는 것이다.

~~~text
Refresh
= get current state

Reconcile
= compare current state
  + determine impact
  + update plan/action
~~~

Source가 바뀌었다고 항상 모든 작업을 다시 시작할 필요는 없다.

변경이 현재 Decision과 무관할 수 있기 때문이다.

### Version Conflict와 Decision Conflict

2026년 9월 공개된 Selective Revalidation preprint는 이 차이를 Version Conflict와 Decision Conflict로 구분한다.

#### Version Conflict

Agent가 읽었던 Source Version과 현재 Version이 다르다.

~~~text
observed_version = 41
current_version = 42
~~~

#### Decision Conflict

그 변경이 Pending Action의 정당성을 깨뜨린다.

예를 들어 Policy 문서의 오타가 수정됐다면 Version은 바뀌었지만 환불 Action은 여전히 유효할 수 있다.

반대로 refund_limit가 100에서 50으로 바뀌었다면 80달러 환불 Decision은 더 이상 유효하지 않다.

~~~text
Version Changed
≠ Decision Invalid
~~~

이 구분은 Reconciliation 비용을 줄이는 데 중요하다.

### Pending Decision의 조건을 남긴다

Selective Revalidation을 하려면 "왜 이 Action이 정당했는가"를 어느 정도 구조화할 필요가 있다.

예:

~~~text
Pending Action:
refund 80

Decision Conditions:
- request.status == approved
- refund_limit >= 80
- payment.status == settled
~~~

Source가 바뀌면 관련 Condition만 다시 검사한다.

~~~text
Changed:
refund_limit

Revalidate:
refund_limit >= 80

Result:
false

Action:
re-plan / block
~~~

이 방식은 변경과 무관한 판단까지 전부 다시 계산하지 않고 영향을 받은 조건만 재검증하는 구조를 제시한다. 해당 연구는 controlled feasibility를 보인 결과이며 production generality까지 입증한 것은 아니다.

### Source Registry

Long-running Agent는 자신이 어떤 External Source에 의존하는지 추적할 수 있다.

예:

~~~text
source: refund_policy
version: 41
authority: policy-service

source: payment_record
version: 812
authority: payment-db

source: user_request
version: 9
authority: ticket-system
~~~

이 정보가 State Plane에 있으면 Refresh 대상을 찾기 쉽다.

Memory에 값만 복사하는 것보다 Source Reference와 Version을 함께 가지는 이유다.

### Authority Ranking

여러 Source가 충돌할 수 있다.

예:

~~~text
Wiki:
refund limit = 100

Policy Service:
refund limit = 50
~~~

어떤 Source가 Canonical한지 미리 정해야 한다.

예:

~~~text
Current Policy Service
    >
Approved Policy PDF
    >
Internal Wiki
    >
Agent Memory
~~~

이 순서는 시스템마다 다르다.

핵심은 Model이 문장이 더 자연스럽다는 이유로 Authority를 정하지 않게 하는 것이다.

### Refresh Trigger

모든 Step마다 모든 Source를 다시 읽는 것은 비효율적이다.

Trigger를 정할 수 있다.

예:

- 일정 시간 경과
- Irreversible Action 직전
- Approval 후 Resume
- Long Pause 후 Resume
- Retry / Recovery
- Handoff
- External Event Notification
- Version Mismatch
- Final Completion 직전

High-risk Action일수록 Freshness 요구를 높일 수 있다.

### Optimistic Concurrency

External API가 Version이나 ETag를 지원한다면 stale mutation을 줄일 수 있다.

~~~text
Read version = 41

Prepare mutation

Write if version == 41
~~~

현재 Version이 42라면 Write를 거부한다.

~~~text
409 Conflict
→ refresh
→ reconcile
→ re-plan
~~~

이때 Conflict를 단순 Retry로 처리하면 안 된다.

같은 Mutation을 최신 Version에 다시 적용하는 것이 옳다는 보장이 없기 때문이다.

### Compare-and-Set과 Commit Boundary

Critical Action에서는 최종 Commit이 Revalidation과 연결돼야 한다.

개념적으로:

~~~text
Read
→ Decide
→ Revalidate Conditions
→ Commit if version/conditions still valid
~~~

가능하면 CAS나 Transaction 같은 Mechanism을 사용한다.

Agent가 Condition을 확인한 직후 Source가 다시 바뀌는 Race를 줄이기 위해서다.

### Selective Revalidation

전체 State를 매번 다시 읽는 대신 Pending Decision과 관련 있는 Source만 재검증할 수 있다.

~~~text
Changed Sources
      ↓
Dependency / Decision Conditions
      ↓
Affected Decisions
      ↓
Selective Revalidation
~~~

결과는 네 가지 정도로 나눌 수 있다.

~~~text
Still Valid
→ Continue

Metadata Changed Only
→ Refresh Projection

Decision Invalid
→ Re-plan

Unsafe / Duplicate Risk
→ Block
~~~

이 taxonomy 역시 시스템 설계용 예시다.

### Derived State Invalidity

Source 하나가 바뀌면 그 Source에서 파생된 State가 무효화될 수 있다.

예:

~~~text
Requirement changed
  ↓
Plan invalid
  ↓
Acceptance Criteria affected
  ↓
Implementation maybe invalid
~~~

따라서 State Plane에 Causation이나 Dependency를 남기면 선택적 Invalidation이 가능하다.

모든 Derived State를 항상 자동 계산할 필요는 없지만 "이 정보가 어디에서 왔는가"를 알 수 있어야 한다.

### OSWorld 2.0의 실패 패턴

Long-horizon benchmark에서는 Agent가 새로운 Approval이나 Message를 관찰했는데도 전체 Internal Table을 다시 맞추지 않아 오래된 Working State로 행동하는 사례가 나타난다.

전형적인 패턴은 다음과 같다.

~~~text
Observe Initial State
→ Build Internal Model
→ New Evidence Arrives
→ Patch One Local Item
→ Global Working State remains stale
→ Verify against stale internal model
→ False Completion
~~~

중요한 점은 Agent가 새로운 정보를 "봤다"는 사실만으로 충분하지 않다는 것이다.

Internal Projection 전체에서 어떤 항목이 무효화됐는지 반영해야 한다.

### Reconciliation과 Memory

Memory는 Discovery를 빠르게 하는 hint가 될 수 있지만 Final Authority가 아니다. Irreversible Action이나 Completion 검증에서는 현재 Authoritative Source를 다시 확인한다.

Memory가 오래됐을 때 어떻게 무효화하고 다시 쓰는지는 Part IV에서 별도로 다룬다.

### Reconciliation과 Approval

승인에도 Freshness가 있다.

예를 들어 사용자가 오전 10시에 "이 PR을 Merge해도 된다"고 승인했다.

오후 2시에 Base Branch와 Diff가 크게 바뀌었다.

오전의 Approval이 오후의 새로운 Diff에도 그대로 적용되는가.

Approval Object에는 Scope를 명확히 할 필요가 있다.

~~~text
approval:
  action: merge
  artifact_version: commit abc123
~~~

Artifact Version이 바뀌면 재승인이 필요할 수 있다.

### Reconciliation과 Handoff

Agent A가 Agent B로 Handoff할 때도 Source Version을 전달해야 할 수 있다.

단순 Summary:

~~~text
"정책 확인 완료"
~~~

보다:

~~~text
policy_source: policy-service
observed_version: 41
checked_at: 10:00
~~~

가 더 안전하다.

Agent B는 현재 Version과 비교할 수 있다.

### Final Verification은 External Reality를 본다

Agent가 Internal Checklist를 모두 완료했다고 하자.

그래도 최종 Completion 전에는 현재 Artifact와 Source를 확인한다.

~~~text
Internal Completion Claim
        ↓
Refresh Authoritative Sources
        ↓
Verify Current Acceptance
        ↓
Inspect Actual Artifact / Side Effect
        ↓
Complete
~~~

Long-running Agent에서 이 단계가 중요하다.

Internal Story가 Source of Truth가 되지 않게 한다.

### 작은 예: 코드 수정 중 main 변경

Coding Agent가 main@abc123을 기준으로 수정했다.

작업 중 main이 def456으로 바뀌었다.

Agent가 PR을 만들기 전에 다음을 할 수 있다.

~~~text
Observed Base:
abc123

Current Base:
def456

Changed Files:
UserService.java
AuthConfig.java
~~~

현재 Patch와 충돌 가능성이 있으면 Rebase/Refresh가 필요하다.

반대로 변경이 README뿐이라면 Decision Conflict가 아닐 수 있다.

Version Conflict만으로 항상 전체 구현을 버릴 필요는 없다.

### Task-State Horizon

Long-running 난이도를 Step 수만으로 설명하기 어렵다.

초기에 읽은 State가 수백 Action 뒤의 Final Decision에도 영향을 줄 수 있다.

2026년 공개된 Task-State Horizon preprint는 이런 Dependency Length를 별도 축으로 측정하는 접근을 제안한다.

아직 일반적인 표준 Metric은 아니다.

하지만 Agent가 "얼마나 오래 State를 기억해야 하는가"보다 "얼마나 오래 State를 유효하게 유지하고 다시 확인해야 하는가"를 생각하게 만든다.

### 이 장에서 가져갈 것

Long-running Agent의 Working State는 현재 현실 그 자체가 아니라 특정 시점에 관찰한 Snapshot이다.

그래서 중요한 Action 전에 다음 흐름이 필요하다.

~~~text
Detect Change
      ↓
Refresh
      ↓
Identify Affected Decisions
      ↓
Selective Revalidation
      ├─ Continue
      ├─ Refresh Projection
      ├─ Re-plan
      └─ Block
      ↓
Safe Commit
~~~

핵심 원칙은 간단하다.

> **변경됐는지를 보는 데서 끝나지 말고, 그 변경이 현재 Decision을 무효화하는지 확인한다.**

Part III에서는 State를 분리하고, Agent State Plane을 정의하고, Recovery와 Long-running, Reconciliation까지 연결했다.

다음 Part에서는 그중에서도 가장 오해가 많은 Long-term Memory를 별도로 다룬다.

무엇을 기억할 것인가보다 먼저, 무엇을 장기 Memory에 써도 되는지를 살펴본다.

### Source Notes

- [S-SELECTIVE-REVALIDATION]
- [S-TSH]
- [S-AGENTREWIND]
- [S-OSWORLD2]
