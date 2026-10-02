# Agent Identity and Authorization

기준일: 2026-10-02

## 핵심 질문

> Agent가 외부 시스템에 접근할 때 누구의 권한으로 행동하는가?

Tool permission만으로는 충분하지 않다.

Production Agent에서는 최소한 다음 identity를 분리해야 한다.

~~~text
Human User Identity
Application Identity
Agent Workload Identity
Tool / Service Identity
Delegated User Credential
Runtime Execution Role
~~~

## Inbound와 Outbound를 분리한다

### Inbound Auth

누가 Agent를 호출할 수 있는가.

예:
- end user
- internal service
- scheduler
- webhook

### Outbound Auth

Agent가 누구를 대신해 외부 resource에 접근할 수 있는가.

예:
- GitHub
- Slack
- Google Workspace
- DB
- cloud resource
- payment API

이 두 문제는 별도다.

## Workload Identity

AWS AgentCore Identity는 Agent를 workload identity로 모델링한다.

이 접근의 장점:

- Agent process 자체의 identity를 추적
- credential을 model context에 직접 노출하지 않음
- user delegation과 autonomous workload access를 구분 가능
- audit trail 유지

따라서 Agent에게 장기 API key를 그대로 environment variable로 주는 구조보다 별도 credential broker가 안전하다.

## Delegation

User-delegated action은 다음 관계가 명확해야 한다.

~~~text
User
  ↓ consent
Agent / Application
  ↓ delegated credential
External Service
~~~

Agent가 user보다 더 넓은 권한을 얻으면 안 된다.

반대로 fully autonomous maintenance agent라면 user token이 아니라 별도 workload role이 더 적합할 수 있다.

## Capability Discovery와 Authorization 분리

A2A Agent Card나 MCP tool catalog가 capability를 알려준다고 해서 호출 권한까지 의미하지 않는다.

~~~text
Discovery
= 무엇을 할 수 있다고 광고하는가

Authentication
= 누가 요청했는가

Authorization
= 이 principal이 이 action을 할 수 있는가

Approval
= 이번 action을 지금 실행해도 되는가
~~~

이 네 층을 분리한다.

## Credential Boundary

Agent runtime 안에 raw credential이 있으면 tool을 우회해 직접 사용할 수 있다.

따라서 가능한 구조:

~~~text
Agent
  ↓ intent / tool args
Credential-aware Gateway
  ↓ policy check
Inject credential at boundary
  ↓
External Service
~~~

NVIDIA OpenShell 역시 Agent가 real credential을 직접 보지 않고 approved endpoint로 나가는 request에 gateway가 credential을 붙이는 패턴을 사용한다.

## Runtime Role의 함정

AWS AgentCore는 microVM 내부 코드가 metadata service를 통해 execution role credential에 접근할 수 있음을 명시한다.

즉 VM isolation이 있어도 role 자체가 과도하면 blast radius가 크다.

그래서:

- per-agent role
- per-environment role
- minimal scope
- short-lived token
- endpoint-specific credential

이 필요하다.

## Authorization Input

정책 판단 후보:

- authenticated user
- agent identity
- requested capability
- tool/action
- target resource
- environment
- risk level
- current task
- approval status

## Agent-to-Agent

A2A는 remote agent가 task를 수행할 때 서버가 authenticated client/user identity에 따라 skill, action, data access policy를 자체적으로 authorization해야 한다고 명시한다.

따라서 remote Agent는 caller의 모든 권한을 암묵적으로 상속하지 않는다.

## 설계 원칙

1. User identity와 Agent workload identity를 분리한다.
2. Inbound auth와 Outbound auth를 분리한다.
3. Capability discovery는 authorization이 아니다.
4. Credential을 model context에 넣지 않는다.
5. 가능한 한 credential을 gateway boundary에서 주입한다.
6. Runtime role도 least privilege로 제한한다.
7. Delegated credential에는 explicit scope와 consent가 필요하다.
8. 모든 side effect에는 actor / principal / target audit가 남아야 한다.

## 주요 근거

- Amazon Bedrock AgentCore Identity
- AgentCore Runtime Security Best Practices
- A2A Specification Authorization
- NVIDIA OpenShell credential gateway architecture
