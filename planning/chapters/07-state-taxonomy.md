# 7장. Session, Workspace, Goal, Memory를 분리한다

## Goal
독자가 Agent에서 서로 다른 lifecycle의 상태를 구분하고 잘못된 단일 Memory 모델을 피할 수 있게 한다.

## Core Claims
- Context, Session, Workspace, Goal, Artifact, Memory, Source of Truth는 다르다.
- lifecycle과 authority가 다른 state를 한 저장소 의미로 합치면 recovery와 security가 꼬인다.
- Runtime Session은 Durable State가 아니다.
- Memory는 current Source of Truth를 대체하지 않는다.

## Reader Questions
- Session history가 곧 Memory인가?
- Workspace가 유지되면 checkpoint가 필요 없는가?
- Goal은 prompt에 적으면 충분한가?

## Flow
1. "Memory"라는 과도한 단어
2. state taxonomy
3. 각 state의 lifetime / owner / authority
4. state promotion
5. freshness / invalidation
6. taxonomy decision table

## Example / Figure
- 하나의 coding task에서 Session/Workspace/Goal/Artifact/Memory 분리
- Figure: State lifetime ladder

## Evidence
- research/topics/09-state-memory-taxonomy.md
- OpenAI Sessions / Sandbox Memory / Codex Goals
- AWS AgentCore Runtime

## Avoid
- State Plane 구현 상세
- memory security 상세

## Draft Exit Criteria
- 8개 state 개념이 겹치지 않는다.
- 다음 장 State Plane 필요성이 자연스럽게 도출된다.
