# Delegated Agent Identity and Zero Trust

기준일: 2026-10-02

## 핵심 문제

Agent가 인간을 대신해 행동할 때 단순히 User Token을 전달하면 되는가?

3차 조사에서는 Enterprise Identity 제품들이 Agent 자체를 first-class principal로 만들기 시작했다는 점이 확인됐다.

## Microsoft Entra Agent ID

Microsoft Entra Agent ID는 Agent Identity를 특수한 Service Principal로 모델링한다.

중요한 특징:

- 각 Agent를 구분 가능한 identity로 표현
- Agent Identity 자체에 credential을 직접 두지 않을 수 있음
- Blueprint가 Agent를 대신해 token을 획득
- interactive agent는 user-delegated token 사용 가능
- autonomous agent는 app token을 사용할 수 있음
- Agent별 audit와 policy 적용 가능

이 구조는 Agent와 Hosting Application을 같은 principal로 묶지 않는 방향이다.

## Actor Chain

Agent action에는 최소한 다음 관계를 남기는 것이 좋다.

~~~text
Human / Initiator
      ↓ delegates or requests
Application
      ↓ hosts
Agent Identity
      ↓ requests capability
Tool / Resource
      ↓ actual target
External System
~~~

Audit에서 단순히 service-account@example.com만 남으면 실제 actor chain을 복구하기 어렵다.

## Delegated Mode와 Autonomous Mode

### Delegated

~~~text
User
  ↓ consent
Agent
  ↓ on-behalf-of token
Resource
~~~

권한 상한은 user와 granted scope를 넘지 않아야 한다.

### Autonomous

~~~text
Scheduler / System
  ↓
Agent Workload Identity
  ↓ app/workload token
Resource
~~~

정기 점검, 모니터링, 자동 maintenance처럼 특정 user가 항상 존재하지 않는 작업에 적합하다.

두 mode를 한 credential model로 합치지 않는다.

## Blueprint / Class Policy

많은 Agent가 생기면 개별 policy만으로 관리하기 어렵다.

Blueprint 또는 Agent Class 단위로 다음을 상속할 수 있다.

- allowed resource family
- max privilege
- network zone
- sponsor / owner
- lifecycle
- audit policy
- default approval

하지만 개별 Agent의 effective permission은 별도로 추적한다.

## Tool Identity

Microsoft의 identity guidance는 User, Application, Workload, Agent, Tool, Resource identity를 구분한다.

Tool도 별도 credential context를 가질 수 있다.

예:

~~~text
Agent A
  ├─ GitHub Read Tool Identity
  ├─ Slack Write Tool Identity
  └─ Production DB Read-only Identity
~~~

한 개의 광범위한 service account로 모든 tool을 처리하는 것보다 blast radius를 줄일 수 있다.

## Token Exchange Boundary

Agent에게 raw user token을 장시간 보관시키기보다 gateway/identity broker가 action 시점에 short-lived token을 교환하는 구조가 낫다.

~~~text
Agent Intent
   ↓
Authorization Gateway
   ↓
Check:
- agent
- user/delegator
- scope
- tool
- resource
- risk
   ↓
Short-lived token
   ↓
External API
~~~

## Identity와 Memory

Memory write에서도 actor identity가 중요하다.

누가 기억을 만들었는지 알 수 없으면:

- poisoning source 추적
- tenant boundary
- user correction
- deletion
- audit

이 어렵다.

Memory provenance에 identity chain을 포함시킨다.

## Identity와 A2A

Remote Agent가 호출될 때도:

- caller agent
- originating user
- current delegation scope
- target task

를 구분해야 한다.

A2A capability discovery는 이러한 authorization을 대신하지 않는다.

## Zero Trust 원칙

Agent를 내부 서비스라고 자동 신뢰하지 않는다.

각 action마다 최소한 다음을 판단한다.

~~~text
Who?
Which Agent?
On behalf of whom?
Which Tool?
Which Resource?
Which Scope?
Which Environment?
Which Risk?
Is this still valid now?
~~~

## Agent Lifecycle

Agent identity에도 lifecycle이 필요하다.

- create
- sponsor
- activate
- scope change
- risk detection
- suspend
- revoke
- delete

Agent implementation이 삭제돼도 orphaned identity와 credential이 남지 않게 해야 한다.

## 책에 반영할 핵심 원칙

1. Agent는 first-class security principal로 볼 수 있어야 한다.
2. User / App / Agent / Tool / Resource identity를 구분한다.
3. Delegated와 Autonomous access를 분리한다.
4. Agent가 standing broad credential을 직접 보유하지 않게 한다.
5. action 시점에 short-lived token을 발급하는 구조를 우선 검토한다.
6. Audit에는 actor chain을 남긴다.
7. Agent identity에도 owner/sponsor와 lifecycle이 필요하다.
8. Memory provenance에도 actor identity를 포함한다.

## 주요 근거

- Microsoft Entra Agent ID
- Microsoft Agent Identity Platform
- Microsoft OAuth On-Behalf-Of Flow for Agents
- AWS AgentCore Identity
- A2A Authorization model
- NVIDIA OpenShell credential binding
