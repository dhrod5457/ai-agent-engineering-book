# External State Reconciliation

기준일: 2026-10-02

## 핵심 문제

Agent는 작업 시작 시 외부 시스템을 읽고 internal working state를 만든다.

하지만 long-running task에서는 외부 상태가 계속 바뀔 수 있다.

~~~text
External Source at T0
       ↓
Agent Working State
       ↓
Long Running Work
       ↓
External Source changes at T1
       ↓
Agent continues with stale state
~~~

이 상태에서 최종 action을 실행하면 오래된 정보에 근거한 mutation이 발생한다.

## OSWorld 2.0의 교훈

장기 업무 benchmark에서는:

- late approval
- new message
- hidden prior state
- conflicting records
- multi-item tracking

이 반복적으로 문제가 됐다.

특히 Agent가 새 정보를 부분적으로 봤어도 자신의 전체 internal model을 다시 계산하지 않으면 stale decision이 남을 수 있다.

## Reconciliation Loop

추천 구조:

~~~text
Read Source
   ↓
Build Working Projection
   ↓
Plan / Act
   ↓
Refresh Trigger
   ↓
Read Current Source
   ↓
Compare
   ├─ No Change → Continue
   └─ Changed   → Reconcile
                    ↓
               Re-plan / Escalate
~~~

## Refresh Trigger

매 step마다 모든 source를 다시 읽는 것은 비효율적이다.

refresh trigger 후보:

- 일정 시간 경과
- irreversible action 직전
- approval 후 resume
- long pause 후 resume
- external event notification
- version mismatch
- conflicting observation
- task milestone
- retry/recovery
- handoff

## Optimistic Concurrency

가능한 API에서는 version/ETag/revision을 사용한다.

~~~text
Read version = 41
Modify based on 41
Write if version still 41
Else conflict
~~~

conflict가 발생하면 Agent가 최신 상태를 읽고 reconcile한다.

이 방식은 stale mutation을 줄인다.

## Source Registry

Long-running Agent는 자신이 어떤 외부 source에 의존하는지 명시적으로 관리하는 편이 좋다.

예:

~~~text
Source Registry
- Jira Issue #123, rev 7
- GitHub main, SHA abc123
- Approval Record A55, updated 10:42
- Price Quote Q9, valid until 15:00
~~~

Working memory에 사실만 복사하는 것보다 source ref + version을 함께 유지한다.

## Authority Ranking

여러 source가 충돌하면 어떤 source가 authoritative한지 미리 정의한다.

예:

~~~text
Production Config > Wiki
Approved Requirement > Chat Summary
Current Git HEAD > Memory
Signed Approval > Agent Note
~~~

Agent가 임의로 더 자연스러운 문장을 source of truth로 고르면 안 된다.

## Reconciliation Outcome

변화가 발견되면:

- update internal projection
- invalidate dependent assumptions
- recalculate plan
- re-run verifier
- request clarification
- pause for approval

중 하나를 선택한다.

## Derived State Invalidity

한 source 변경이 여러 derived state를 무효화할 수 있다.

~~~text
Requirement changed
  ↓
Plan invalid
  ↓
Acceptance criteria maybe invalid
  ↓
Current implementation may need rework
~~~

따라서 State Plane에 dependency/causation 정보가 있으면 selective invalidation이 가능하다.

## Final Verification

최종 검증은 Agent의 internal checklist만 보고 하지 않는다.

~~~text
Internal Completion Claim
        ↓
Refresh Authoritative Sources
        ↓
Evaluate Current Acceptance
        ↓
Inspect Actual Artifact / Side Effect
        ↓
Completion
~~~

## 책에 반영할 핵심 원칙

1. Working State는 External Source의 snapshot일 뿐이다.
2. Source reference와 version을 함께 저장한다.
3. Irreversible action 전에는 refresh/reconcile한다.
4. 가능한 곳에서는 optimistic concurrency를 사용한다.
5. conflict는 retry가 아니라 re-plan 신호일 수 있다.
6. source authority order를 명시한다.
7. source 변경은 dependent state를 invalidate할 수 있다.
8. final verification은 actual source/artifact를 기준으로 한다.

## 주요 근거

- OSWorld 2.0 long-horizon failure analysis
- Temporal event/update model
- Long-running agent harness studies
- Standard optimistic concurrency patterns in external APIs
