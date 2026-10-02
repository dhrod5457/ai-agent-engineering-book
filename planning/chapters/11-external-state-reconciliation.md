# 11장. External State Reconciliation

## Goal
독자가 long-running Agent의 내부 working state와 변화하는 authoritative source를 동기화하는 전략을 설계할 수 있게 한다.

## Core Claims
- Working State는 External Source의 snapshot일 뿐이다.
- irreversible action 전에 authoritative source를 refresh해야 한다.
- source reference와 version을 함께 추적하면 stale mutation을 줄일 수 있다.
- conflict는 단순 retry가 아니라 re-plan 신호일 수 있다.

## Reader Questions
- 언제 source를 다시 읽어야 하는가?
- 여러 source가 충돌하면 무엇을 믿어야 하는가?
- stale state를 자동으로 탐지할 수 있는가?

## Flow
1. stale internal story 실패
2. Source Registry
3. authority ranking
4. refresh trigger
5. version/ETag와 optimistic concurrency
6. dependent-state invalidation
7. re-plan / clarification
8. final verification

## Example / Figure
- 승인 상태가 뒤늦게 바뀐 구매 요청
- Figure: Read → Project → Act → Refresh → Reconcile

## Evidence
- research/topics/21-external-state-reconciliation.md
- research/topics/13-long-horizon-computer-use.md
- OSWorld 2.0
- optimistic concurrency patterns

## Targeted Research Before Draft
- state reconciliation을 isolated capability로 측정한 최근 Agent 연구 확인
- dynamic environment benchmark 사례 추가
- versioned API conflict handling 사례 1~2개 확보

## Avoid
- 모든 distributed consistency 이론
- database replication

## Draft Exit Criteria
- refresh trigger와 authority rule이 실제 설계 규칙으로 제시된다.
- synthesis 주장과 외부 근거를 구분한다.
