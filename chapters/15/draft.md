# 15장. Credential을 Agent에서 분리한다

Agent Runtime에 다음 Environment Variable이 들어 있다고 하자.

~~~text
GITHUB_TOKEN=...
SLACK_TOKEN=...
PROD_DB_PASSWORD=...
~~~

Agent는 Tool을 통해서만 이 Credential을 사용하도록 설계돼 있다.

하지만 Runtime 안에서 Shell도 실행할 수 있다면 이야기가 달라진다.

Agent가 의도적으로 Secret을 읽지 않더라도 공격된 Tool Result나 잘못된 Command가 Credential을 노출할 수 있다.

Sandbox가 강하더라도 Runtime 안에 Broad Credential이 있으면 해당 Sandbox 안에서의 Blast Radius는 크다.

Credential Boundary를 별도 계층으로 보는 이유다.

## Standing Credential의 위험

장기 API Key나 Broad Service Account Credential을 Agent Runtime에 넣으면 몇 가지 문제가 생긴다.

- Agent가 직접 읽을 수 있다.
- Tool을 우회해 다른 API에 사용할 수 있다.
- Runtime compromise 시 노출된다.
- Scope가 Current Task보다 넓을 수 있다.
- Revocation과 Rotation이 어렵다.

특히 Agent가 Shell, Browser, Code Execution을 사용할수록 Raw Credential Exposure를 줄이는 것이 중요하다.

## Agent는 Intent를 만들고 Gateway가 Credential을 사용한다

추천할 수 있는 구조는 다음과 같다.

~~~text
Agent
  ↓ intent + arguments
Capability Gateway
  ↓ authentication / authorization
Credential Broker
  ↓ short-lived credential
External Service
~~~

Agent는 "무엇을 하려는지"를 제안한다.

Credential은 Action Boundary에서 주입된다.

이 구조에서는 Model Context에 Secret이 들어갈 이유가 줄어든다.

## Short-lived Credential

가능하면 Credential의 Lifetime을 줄인다.

~~~text
Long-lived Token
→ broad exposure window

Short-lived Token
→ smaller exposure window
~~~

Short-lived Token도 탈취될 수 있다.

하지만 Damage Window와 Revocation 부담을 줄일 수 있다.

특히 High-risk Action에서는 Action 직전에 Token을 발급하고 짧게 사용하는 방식이 유용하다.

## Delegated Token

사용자를 대신하는 Action이라면 User Scope가 반영된 Token을 사용한다.

개념적으로:

~~~text
User
  ↓ consent
Application / Agent
  ↓ on-behalf-of exchange
Short-lived Delegated Token
  ↓
Resource
~~~

Microsoft의 On-Behalf-Of Flow 같은 패턴이 이 문제를 다룬다.

핵심은 Agent가 User보다 더 강한 App Credential로 User 요청을 수행하지 않게 하는 것이다.

## Autonomous Workload Token

정기 작업에는 User가 없을 수 있다.

~~~text
Scheduler
→ Agent Workload Identity
→ App / Workload Token
→ Resource
~~~

이 Token에는 Autonomous Task에 필요한 최소 Scope만 둔다.

Delegated Token과 Autonomous Token을 같은 것으로 취급하지 않는다.

## Credential Broker

Credential Broker는 다음 책임을 가질 수 있다.

- Agent Identity 확인
- User Delegation 확인
- Tool Scope 확인
- Resource 확인
- Policy 적용
- Short-lived Token 발급
- Audit

Agent가 Raw Secret을 알 필요가 없다.

~~~text
Agent knows:
"GitHub PR 생성 권한이 필요하다"

Broker knows:
"어떤 Token을 어떤 Scope로 발급할지"
~~~

## Tool별 Credential

Agent 하나에 하나의 Broad Credential을 주는 대신 Tool별로 나눌 수 있다.

~~~text
GitHub Read Tool
→ repo:read

GitHub PR Tool
→ pull_request:write

Slack Send Tool
→ chat:write

Production DB Tool
→ read-only
~~~

이 구조는 Capability Boundary와 Credential Boundary를 맞춘다.

Tool이 compromise돼도 다른 Capability Credential까지 바로 노출되지 않게 할 수 있다.

## Credential Injection

NVIDIA OpenShell 같은 최신 Agent Sandbox 설계에서는 Agent Workload가 실제 Secret을 직접 보지 않고 Gateway가 승인된 Endpoint Request에 Credential을 붙이는 구조를 사용한다.

개념:

~~~text
Sandbox
  ↓ outbound request without secret
Policy Gateway
  ↓ validate destination / method / path
Credential Injection
  ↓
External Endpoint
~~~

이 구조는 Network Policy와 Credential Policy를 결합할 수 있다.

## Endpoint Scope

Credential Scope가 API 수준에서 충분히 좁지 않을 수 있다.

Gateway에서 추가로 제한할 수 있다.

예:

~~~text
host = api.github.com
method = POST
path = /repos/org/app/pulls
~~~

Agent에게 GitHub Token 전체를 주는 것과 특정 Endpoint Action만 허용하는 것은 다르다.

## Runtime Role도 Credential이다

Cloud Runtime이 IAM Role을 가진 경우 Agent가 직접 Secret 파일을 보지 않더라도 Runtime Metadata를 통해 Credential을 얻을 수 있다.

따라서 "Secret을 Environment Variable에 안 넣었다"만으로 충분하지 않다.

Runtime Execution Role도 Least Privilege가 필요하다.

예:

- per-agent role
- per-environment role
- per-task temporary policy
- restricted network
- short session

## Credential과 Sandbox

강한 Sandbox가 Credential Risk를 자동으로 해결하지 않는다.

MicroVM 안에 Broad Production Credential이 있다면 MicroVM Escape가 없어도 Agent가 그 Credential로 정상 API를 호출해 큰 Side Effect를 만들 수 있다.

따라서:

~~~text
Isolation
≠ Credential Scope
~~~

둘 다 필요하다.

## Credential과 Tool Result Injection

Prompt Injection이 Agent를 속여 Tool Call을 만들 수 있다.

Credential Gateway가 있으면 최소한 다음을 검사할 수 있다.

~~~text
Agent proposes:
send data to evil.example

Gateway:
destination not allowed

Result:
deny
~~~

Model이 속았더라도 Credential과 Network Boundary가 마지막 방어선이 된다.

## Audit

Credential 사용은 Actor Chain과 연결돼야 한다.

예:

~~~text
user: staff-10
agent: campus-agent-2
tool: message-send
credential: delegated-token-77
resource: student-44
policy: allow-19
result: success
~~~

"어떤 Token이 쓰였는가"보다 "누구를 대신해 어떤 Resource에 어떤 Scope로 사용됐는가"가 중요하다.

## Revocation

Agent가 Suspend되면 Credential도 함께 끊겨야 한다.

User가 Consent를 철회하면 Delegated Access가 중단돼야 한다.

Tool이 Disable되면 해당 Credential Path도 막혀야 한다.

Identity Lifecycle과 Credential Lifecycle을 연결한다.

## 작은 예: PR 작성 Agent

나쁜 구조:

~~~text
Agent Runtime
  ├─ GITHUB_TOKEN(repo full access)
  └─ shell
~~~

더 좁은 구조:

~~~text
Agent
  ↓ create_pull_request intent
Gateway
  ↓ verify:
     repo = org/app
     action = PR create
     user scope valid
Credential Broker
  ↓ short-lived PR token
GitHub
~~~

Agent가 Token 값을 직접 알 필요가 없다.

## 이 장에서 가져갈 것

Credential을 Agent에게 주는 것과 Agent가 Capability를 사용할 수 있게 하는 것은 같은 문제가 아니다.

가능하면 다음 구조를 우선 검토한다.

~~~text
Agent Intent
→ External Authorization
→ Short-lived Credential
→ Scoped Action
~~~

핵심 경계:

~~~text
Agent Identity
≠ Credential

Sandbox
≠ Credential Scope

Capability Discovery
≠ Credential Grant
~~~

다음 장에서는 Credential이 있든 없든 Agent가 실제 Runtime에서 접근할 수 있는 범위를 다룬다.

Filesystem, Process, Network를 어디까지 열어줄 것인가.

Sandbox와 Containment로 넘어간다.

## 주요 근거

- Microsoft Entra Agent ID / On-Behalf-Of Flow
- AWS AgentCore Identity
- NVIDIA OpenShell
- research/topics/19-delegated-agent-identity-zero-trust.md
