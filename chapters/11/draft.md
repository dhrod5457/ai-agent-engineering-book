# 11장. External State Reconciliation

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

## Working State는 Snapshot이다

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

## Refresh와 Reconciliation은 다르다

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

## Version Conflict와 Decision Conflict

최근 Selective Revalidation 연구에서는 이 차이를 명확하게 구분한다.

### Version Conflict

Agent가 읽었던 Source Version과 현재 Version이 다르다.

~~~text
observed_version = 41
current_version = 42
~~~

### Decision Conflict

그 변경이 Pending Action의 정당성을 깨뜨린다.

예를 들어 Policy 문서의 오타가 수정됐다면 Version은 바뀌었지만 환불 Action은 여전히 유효할 수 있다.

반대로 refund_limit가 100에서 50으로 바뀌었다면 80달러 환불 Decision은 더 이상 유효하지 않다.

~~~text
Version Changed
≠ Decision Invalid
~~~

이 구분은 Reconciliation 비용을 줄이는 데 중요하다.

## Pending Decision의 조건을 남긴다

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

이 방식은 모든 Context를 처음부터 다시 계산하는 것보다 선택적으로 대응할 수 있다.

## Source Registry

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

## Authority Ranking

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

## Refresh Trigger

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

## Optimistic Concurrency

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

## Compare-and-Set과 Commit Boundary

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

## Selective Revalidation

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

## Derived State Invalidity

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

## OSWorld 2.0의 실패 패턴

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

## Reconciliation과 Memory

Memory는 Discovery를 빠르게 하는 hint가 될 수 있지만 Final Authority가 아니다. Irreversible Action이나 Completion 검증에서는 현재 Authoritative Source를 다시 확인한다.

Memory가 오래됐을 때 어떻게 무효화하고 다시 쓰는지는 Part IV에서 별도로 다룬다.

## Reconciliation과 Approval

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

## Reconciliation과 Handoff

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

## Final Verification은 External Reality를 본다

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

## 작은 예: 코드 수정 중 main 변경

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

## Task-State Horizon

Long-running 난이도를 Step 수만으로 설명하기 어렵다.

초기에 읽은 State가 수백 Action 뒤의 Final Decision에도 영향을 줄 수 있다.

최근 연구에서는 이런 Dependency Length를 Task-State Horizon으로 측정하려는 접근이 있다.

아직 일반적인 표준 Metric은 아니다.

하지만 Agent가 "얼마나 오래 State를 기억해야 하는가"보다 "얼마나 오래 State를 유효하게 유지하고 다시 확인해야 하는가"를 생각하게 만든다.

## 이 장에서 가져갈 것

Long-running Agent의 Working State는 현재 현실 그 자체가 아니다.

Snapshot이다.

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

## 주요 근거

- OSWorld 2.0
- From Version Conflicts to Decision Conflicts: Selective Revalidation for Long-running AI Agents
- Task-State Horizon research
- AgentRewind
- research/topics/21-external-state-reconciliation.md
- research/targeted/11-external-state-reconciliation.md
