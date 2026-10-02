# 11장. External State Reconciliation

## Goal
독자가 long-running Agent의 내부 working state와 변화하는 authoritative source를 동기화하고, 변경이 실제 pending decision을 무효화하는지 선택적으로 재검증하는 전략을 설계할 수 있게 한다.

## Core Claims
- Working State는 External Source의 snapshot일 뿐이다.
- 모든 version change가 decision conflict는 아니다.
- irreversible action 전에 authoritative source를 refresh하고 pending decision의 정당성을 재검증해야 한다.
- source reference와 version을 함께 추적하면 stale mutation을 줄일 수 있다.
- conflict는 단순 retry가 아니라 refresh, re-plan, block 중 하나를 선택해야 하는 신호다.

## Reader Questions
- 언제 source를 다시 읽어야 하는가?
- version이 바뀌면 항상 전체 작업을 다시 해야 하는가?
- 여러 source가 충돌하면 무엇을 믿어야 하는가?
- stale state를 자동으로 탐지할 수 있는가?

## Flow
1. stale internal story 실패
2. Source Registry
3. authority ranking
4. refresh trigger
5. version conflict vs decision conflict
6. selective revalidation
7. version/ETag와 optimistic concurrency
8. dependent-state invalidation
9. re-plan / clarification / block
10. final verification과 atomic/CAS commit

## Example / Figure
- 승인 한도 변경 전후의 환불 action
- Figure: Detect Change → Revalidate Decision Conditions → Continue / Refresh / Re-plan / Block

## Evidence
- research/topics/21-external-state-reconciliation.md
- research/topics/13-long-horizon-computer-use.md
- research/targeted/11-external-state-reconciliation.md
- OSWorld 2.0
- From Version Conflicts to Decision Conflicts
- Task-State Horizon research
- AgentRewind
- optimistic concurrency patterns

## Avoid
- 모든 distributed consistency 이론
- database replication
- selective revalidation 연구 결과를 production generality로 과장

## Draft Exit Criteria
- refresh trigger와 authority rule이 실제 설계 규칙으로 제시된다.
- version conflict와 decision conflict를 구분한다.
- synthesis 주장과 외부 근거를 구분한다.
