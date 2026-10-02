# Multi-agent and Interoperability

## 기본 입장

Multi-agent는 Agent Engineering의 시작점이 아니다.

먼저 하나의 Agent가 다음을 제대로 해야 한다.

- context 관리
- tool use
- state continuation
- security boundary
- trace
- eval

그 다음 complexity가 실제 이득을 줄 때 specialist를 추가한다.

## Multi-agent를 쓰는 이유

- context isolation
- specialist instruction
- independent tool permission
- parallelizable work
- independent review
- ownership handoff

## 비용

- duplicated context
- routing error
- handoff loss
- increased latency
- increased token usage
- harder trace
- conflicting state
- authority ambiguity

## 두 가지 대표 패턴

### Manager + Agent-as-Tool

~~~text
Manager
  ├─ Specialist A
  ├─ Specialist B
  └─ Specialist C
~~~

Manager가 user-facing ownership을 유지한다.

장점:
- central control
- consistent output ownership

단점:
- manager bottleneck
- context concentration

### Handoff

~~~text
Agent A
  ↓ transfer ownership
Agent B
~~~

새 specialist가 이후 interaction을 소유한다.

장점:
- clearer specialist autonomy

단점:
- state/context transfer contract가 중요

## A2A

A2A는 서로 다른 Agent system 간 interoperability 문제를 해결한다.

중요한 개념:

- capability discovery
- task
- message
- artifact
- task lifecycle
- streaming / asynchronous update

A2A를 사용한다고 내부 orchestration이 해결되는 것은 아니다.

## Multi-agent와 Software Factory 경계

이 책에서는 Agent 내부/인접 orchestration까지만 다룬다.

다음은 software-factory-book의 범위로 넘긴다.

- durable backlog
- task scheduling
- fleet
- worker lease
- repository delivery
- merge/deploy governance
- organization-level work selection

## 설계 원칙 후보

1. Single-agent first.
2. Agent 수보다 context/tool/permission boundary를 먼저 본다.
3. Handoff에는 ownership transfer contract가 필요하다.
4. Remote Agent와 local subagent를 같은 개념으로 취급하지 않는다.
5. Multi-agent 성능은 end-to-end eval로 검증한다.
