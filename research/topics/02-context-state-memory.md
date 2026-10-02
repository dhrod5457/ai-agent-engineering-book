# Context, State, Memory

## 핵심 문제

Agent는 여러 종류의 “기억”을 한 단어 Memory로 뭉치기 쉽다.

하지만 실제 설계에서는 최소한 다음을 분리해야 한다.

~~~text
Context
= 이번 model inference에 실제로 들어가는 token

Session State
= 현재 run/turn을 이어가기 위한 application state

Working Artifact
= file, DB row, plan, checkpoint 등 외부 작업 상태

Persistent Memory
= 다음 session에도 재사용할 장기 정보
~~~

## Context는 저장소가 아니다

Anthropic의 Context Engineering 자료는 context를 finite attention budget으로 본다.

따라서:

~~~text
More Context != Better Agent
~~~

대신 목표는 현재 decision에 필요한 high-signal information을 최소한으로 제공하는 것이다.

## Context Assembly

한 turn의 context 후보:

- system / developer instruction
- user input
- relevant conversation history
- selected tool schemas
- retrieved document
- previous tool result
- working state summary
- examples
- environment metadata

모든 데이터를 항상 넣는 대신 runtime에 맞춰 선택해야 한다.

## Compaction의 한계

Long-running Agent 자료에서는 context compaction만으로 장기 작업 continuity를 해결하지 못했다.

이유:

- 세부 결정이 summary에서 사라질 수 있음
- 실제 filesystem state와 summary가 불일치할 수 있음
- 다음 session이 현재 진행도를 과대/과소평가할 수 있음
- unfinished work의 경계가 사라질 수 있음

따라서 long-running 작업에서는 외부 artifact와 explicit progress state가 중요하다.

## Memory의 위험

Persistent memory가 늘어나면 다음 문제가 생긴다.

- stale assumption
- poisoned memory
- cross-task leakage
- privacy scope 위반
- 잘못된 generalization
- 삭제/정정 어려움

Memory는 무조건적인 capability enhancement가 아니라 lifecycle을 가진 data store로 취급해야 한다.

## 설계 원칙 후보

1. Context와 State를 분리한다.
2. State와 Memory를 분리한다.
3. Artifact를 Memory로 대체하지 않는다.
4. 가능한 한 canonical source를 다시 조회한다.
5. Context에는 current decision에 필요한 것만 projection한다.
6. Persistent memory에는 provenance와 scope가 필요하다.
7. Long-running continuity는 session summary + durable artifact 조합으로 설계한다.

## 관련 출처

- Anthropic Effective context engineering
- Anthropic Effective harnesses for long-running agents
- Anthropic Managed Agents
- OpenAI Running agents / Results and state
- Reflexion
