# 15장. Credential을 Agent에서 분리한다

에이전트 실행 환경에 다음 환경 변수가 들어 있다고 하자.

~~~text
GITHUB_TOKEN=...
SLACK_TOKEN=...
PROD_DB_PASSWORD=...
~~~

에이전트는 도구를 통해서만 이 인증 정보(Credential)를 사용하도록 설계돼 있다. 하지만 실행 환경 안에서 셸도 실행할 수 있다면 이야기가 달라진다. 에이전트가 의도적으로 비밀 정보를 읽지 않더라도 공격된 도구 실행 결과나 잘못된 Command가 인증 정보를 노출할 수 있다. 격리가 강력하더라도 실행 환경 안에 넓은 권한의 인증 정보가 있으면, 그 안에서 일으킬 수 있는 피해 범위는 여전히 크다. 인증 정보의 사용 경계를 별도 계층으로 보는 이유다.

## Standing Credential의 위험

장기 API Key나 Broad Service Account Credential을 에이전트 실행 환경에 넣으면 몇 가지 문제가 생긴다.

- 에이전트가 직접 읽을 수 있다.
- 도구를 우회해 다른 API에 사용할 수 있다.
- Runtime compromise 시 노출된다.
- 적용 범위가 현재 작업보다 넓을 수 있다.
- Revocation과 Rotation이 어렵다.

특히 에이전트가 셸, 브라우저, Code Execution을 사용할수록 Raw Credential Exposure를 줄이는 것이 중요하다.

## Agent는 Intent를 만들고 Gateway가 Credential을 사용한다

검토할 수 있는 기본 구조는 다음과 같다.

~~~text
Agent
  ↓ intent + arguments
Capability Gateway
  ↓ authentication / authorization
Credential Broker
  ↓ short-lived credential
External Service
~~~

에이전트는 "무엇을 하려는지"를 제안한다. 인증 정보는 Action Boundary에서 주입된다. 이 구조에서는 모델의 컨텍스트에 비밀 정보가 들어갈 이유가 줄어든다.

## Short-lived Credential

가능하면 인증 정보의 유지 기간을 줄인다.

~~~text
Long-lived Token
→ broad exposure window

Short-lived Token
→ smaller exposure window
~~~

Short-lived Token도 탈취될 수 있다. 하지만 Damage Window와 Revocation 부담을 줄일 수 있다. 특히 위험이 큰 행동에서는 행동 직전에 토큰을 발급하고 짧게 사용하는 방식이 유용하다.

## Delegated Token

사용자를 대신하는 행동이라면 사용자의 권한 범위가 반영된 토큰을 사용한다.

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

Microsoft의 On-Behalf-Of Flow 같은 패턴이 이 문제를 다룬다. 핵심은 에이전트가 사용자보다 더 강한 App Credential로 사용자 요청을 수행하지 않게 하는 것이다.

## Autonomous Workload Token

정기 작업에는 사용자가 없을 수 있다.

~~~text
Scheduler
→ Agent Workload Identity
→ App / Workload Token
→ Resource
~~~

이 토큰에는 Autonomous Task에 필요한 최소 적용 범위만 둔다. Delegated Token과 Autonomous Token을 같은 것으로 취급하지 않는다.

## Credential Broker

Credential Broker는 다음 책임을 가질 수 있다.

- 에이전트의 신원 확인
- User Delegation 확인
- 도구의 권한 범위 확인
- 접근 대상 자원 확인
- 정책 적용
- Short-lived Token 발급
- 감사

에이전트가 Raw Secret을 알 필요가 없다.

~~~text
Agent knows:
"GitHub PR 생성 권한이 필요하다"

Broker knows:
"어떤 Token을 어떤 Scope로 발급할지"
~~~

## Tool별 Credential

에이전트 하나에 하나의 권한 범위가 넓은 인증 정보를 주는 대신 도구별로 나눌 수 있다.

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

이 구조는 Capability Boundary와 인증 정보의 사용 경계를 맞춘다. 도구가 compromise돼도 다른 Capability Credential까지 바로 노출되지 않게 할 수 있다.

## Credential Injection

NVIDIA OpenShell 같은 최신 Agent Sandbox 설계에서는 Agent Workload가 비밀 정보를 직접 보지 않고 접근을 중개하는 게이트웨이가 승인된 Endpoint Request에 인증 정보를 붙이는 구조를 사용한다.

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

이 구조는 네트워크 정책과 Credential Policy를 결합할 수 있다.

## Endpoint Scope

인증 정보로 행사할 수 있는 권한 범위가 API 수준에서 충분히 좁지 않을 수 있다. 접근을 중개하는 게이트웨이에서 추가로 제한할 수 있다.

예:

~~~text
host = api.github.com
method = POST
path = /repos/org/app/pulls
~~~

에이전트에게 GitHub Token 전체를 주는 것과 특정 Endpoint Action만 허용하는 것은 다르다.

## Runtime Role도 Credential이다

Cloud Runtime이 IAM Role을 가진 경우 에이전트가 직접 비밀 정보 파일을 보지 않더라도 Runtime Metadata를 통해 인증 정보를 얻을 수 있다. 따라서 "비밀 정보를 환경 변수에 안 넣었다"만으로 충분하지 않다. Runtime Execution Role도 최소 권한이 필요하다.

예:

- per-agent role
- per-environment role
- per-task temporary policy
- restricted network
- short session

## Credential과 Sandbox

강한 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)가 Credential Risk를 자동으로 해결하지 않는다. 경량 가상 머신 안에 Broad Production Credential이 있다면 MicroVM Escape가 없어도 에이전트가 그 인증 정보로 정상 API를 호출해 큰 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)를 만들 수 있다.

따라서:

~~~text
Isolation
≠ Credential Scope
~~~

둘 다 필요하다.

## Credential과 Tool Result Injection

외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)이 에이전트를 속여 도구 호출을 만들 수 있다. Credential Gateway가 있으면 최소한 다음을 검사할 수 있다.

~~~text
Agent proposes:
send data to evil.example

Gateway:
destination not allowed

Result:
deny
~~~

모델이 속았더라도 인증 정보와 네트워크 접근 경계가 마지막 방어선이 된다.

## Audit

인증 정보 사용은 Actor Chain과 연결돼야 한다.

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

"어떤 토큰이 쓰였는가"보다 "누구를 대신해 어떤 접근 대상 자원에 어떤 적용 범위로 사용됐는가"가 중요하다.

## Revocation

에이전트가 Suspend되면 인증 정보도 함께 끊겨야 한다. 사용자가 Consent를 철회하면 Delegated Access가 중단돼야 한다. 도구가 Disable되면 해당 Credential Path도 막혀야 한다. Identity Lifecycle과 Credential Lifecycle을 연결한다.

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

에이전트가 토큰 값을 직접 알 필요가 없다.

## 이 장에서 가져갈 것

인증 정보를 에이전트에게 주는 것과 에이전트가 기능을 사용할 수 있게 하는 것은 같은 문제가 아니다. 가능하면 다음 구조를 우선 검토한다.

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

다음 장에서는 인증 정보가 있든 없든 에이전트가 실행 환경에서 접근할 수 있는 범위를 다룬다. 파일 시스템, 프로세스, 네트워크를 어디까지 열어줄 것인가. 샌드박스와 격리(Containment: 접근과 피해 범위를 제한하는 격리)로 넘어간다.

## 주요 근거

- Microsoft Entra Agent ID / On-Behalf-Of Flow
- AWS AgentCore Identity
- NVIDIA OpenShell
- research/topics/19-delegated-agent-identity-zero-trust.md
