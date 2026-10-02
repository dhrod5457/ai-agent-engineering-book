# 8장. Agent State Plane

## Goal
독자가 하나의 Agent execution continuity를 위한 state layer를 설계하고 Factory Control Plane과 구분할 수 있게 한다.

## Core Claims
- Agent State Plane은 이 책의 synthesis 개념이다.
- 목적은 process/context/runtime 손실 이후 실행 continuity를 복구하는 것이다.
- Event History, Checkpoint, Goal, Artifact, Approval, Source Version을 목적별 projection으로 관리한다.
- Context는 State Plane의 projection이다.

## Reader Questions
- 어떤 상태를 durable하게 만들어야 하는가?
- DB 하나면 되는가?
- Conversation log만 보존하면 recovery가 가능한가?

## Flow
1. 장기 실행에서 state loss 문제
2. Agent State Plane 정의
3. 최소 구성요소
4. event vs projection
5. context projection
6. Factory Control Plane과 경계
7. minimal architecture

## Example / Figure
- coding agent가 중간 crash 후 재개하는 state flow
- Figure: Event History → Projections → Context

## Evidence
- research/synthesis/agent-engineering-reference-model-v0.3.md
- research/topics/18-durable-state-event-log-replay.md
- Temporal
- LangGraph Persistence

## Avoid
- "Agent State Plane"을 업계 표준 용어처럼 표현
- 분산 event store 구현 튜토리얼

## Draft Exit Criteria
- 독자에게 synthesis 용어임을 명시한다.
- 최소 state architecture와 경계가 설명된다.
