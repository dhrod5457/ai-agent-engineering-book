# Part V. Identity, Security, Runtime

Part V는 에이전트 보안을 네 질문으로 나눈다.

~~~text
누가 행동하는가?
어떤 Credential로 행동하는가?
어디까지 도달할 수 있는가?
지금 이 Action을 실행해도 되는가?
~~~

신원, 인증 정보(Credential), 격리(Containment: 접근과 피해 범위를 제한하는 격리), 정책을 서로 다른 통제 계층으로 유지한다.

<!-- source-draft: chapters/14/draft.md -->

## 14장. Agent Identity와 Delegation

에이전트가 GitHub 이슈를 생성했다. 감사 로그에는 다음만 남아 있다.

~~~text
actor = service-account@company
~~~

그런데 질문은 더 많다. 누가 이 에이전트를 시작했는가. 어떤 애플리케이션이 에이전트를 Hosting했는가. 에이전트는 누구를 대신해 행동했는가. 어떤 Tool Identity가 실제 API를 호출했는가. 이 행동은 사용자의 권한에서 나온 것인가, Autonomous Workload 권한에서 나온 것인가. 에이전트가 업무를 수행하려면 **누가 행동하는가**를 먼저 분리해야 한다.

### Shared Service Account의 한계

초기 에이전트는 하나의 Service Account를 공유하기 쉽다.

~~~text
Agent A ─┐
Agent B ─┼→ shared-service-account
Agent C ─┘
~~~

구현은 단순하지만, 다음과 같은 문제가 생긴다.

- 어떤 에이전트가 행동을 수행했는지 구분하기 어렵다.
- 사용자 위임과 Autonomous Action을 분리하기 어렵다.
- 에이전트별 권한 축소가 어렵다.
- 하나의 인증 정보(Credential) 노출이 여러 에이전트에 영향을 준다.
- Agent lifecycle과 Credential lifecycle이 묶인다.

에이전트가 늘어날수록 신원을 별도 문제로 다뤄야 한다.

### Identity를 나눈다

이 책에서는 다음 신원을 구분한다.

~~~text
Human User Identity
Application Identity
Agent Identity
Workload Identity
Tool Identity
Resource Identity
~~~

모든 시스템이 여섯 개의 별도 권한을 부여받는 주체를 가져야 한다는 뜻은 아니다. 책임을 분리하기 위한 분류 체계다.

### Human User Identity

요청을 시작한 사용자다.

예:

- 교직원
- 개발자
- 운영자
- 고객

사용자가 에이전트에게 행동을 요청할 수 있다. 중요한 것은 에이전트가 사용자보다 넓은 권한을 자동으로 얻지 않는 것이다.

### Application Identity

에이전트를 Hosting하는 애플리케이션의 신원이다.

예:

~~~text
campus-assistant-web
coding-agent-service
operations-console
~~~

애플리케이션과 에이전트를 같은 신원으로 두면 어떤 에이전트가 어떤 권한을 썼는지 구분하기 어려울 수 있다.

### Agent Identity

특정 에이전트를 구분하는 권한을 부여받는 주체이다. Microsoft Entra Agent ID는 에이전트를 별도 identity construct로 다루는 한 구현 사례다. Entra에서는 agent identity를 특수한 service principal로 표현하지만, 이를 모든 에이전트 시스템의 표준 identity model로 일반화하지 않는다. 에이전트의 신원에는 다음 부가 정보가 연결될 수 있다.

- owner / sponsor
- purpose
- allowed capability class
- 유지 과정
- environment
- risk profile

핵심은 에이전트가 단순 코드 객체를 넘어 독립적인 Security Principal로 관리될 수 있다는 점이다.

### Workload Identity

Autonomous Agent가 특정 사용자 없이 실행될 수 있다.

예:

- Nightly Repository Check
- Security Scan
- Scheduled Report
- Maintenance Task

이때 특정 User Token을 빌리는 것보다 Workload Identity가 더 적합할 수 있다.

~~~text
Scheduler
  ↓
Agent Workload Identity
  ↓
Resource
~~~

### Tool Identity

한 에이전트 안에서도 도구별로 인증 정보로 행사할 수 있는 권한 범위를 분리할 수 있다.

예:

~~~text
Agent
  ├─ GitHub Read Tool
  ├─ Slack Write Tool
  └─ Production DB Read-only Tool
~~~

모든 도구가 같은 권한 범위가 넓은 인증 정보를 공유할 필요는 없다. Tool Identity는 다음 장의 인증 정보의 사용 경계와 연결된다.

### Resource Identity

행동의 대상도 신원이나 Resource Identifier를 가진다.

예:

- Repository A
- Slack Channel B
- Student Record C
- Production Cluster D

권한 확인(Authorization)은 "에이전트가 도구를 호출할 수 있는가"만 보는 것이 아니라 어떤 접근 대상 자원에 적용되는지도 봐야 한다.

### Delegated Access

사용자를 대신해 에이전트가 행동하는 경우다.

~~~text
User
  ↓ consent / scope
Agent
  ↓ delegated token
Resource
~~~

예를 들어 교직원이 자신의 권한 안에서 학생 정보를 조회하도록 에이전트에게 요청할 수 있다. 이때 에이전트는 사용자보다 더 넓은 학생 범위를 볼 수 없어야 한다. Delegated Mode에서는 User Context가 Authorization Input으로 남아야 한다.

### Autonomous Access

특정 사용자가 없는 실행도 있다.

~~~text
System / Scheduler
  ↓
Agent Workload Identity
  ↓
Resource
~~~

예:

- 새벽 로그 분석
- Repository Dependency Check
- 정기 운영 리포트

이 경우 User Delegation Token보다 Application/Workload 인증 정보가 적합하다. Delegated와 Autonomous Mode를 한 인증 정보 모델로 합치지 않는다.

### Actor Chain

Agent Action의 전체 Chain을 남기는 것이 중요하다.

~~~text
Human / Initiator
      ↓
Application
      ↓
Agent
      ↓
Tool
      ↓
Resource
~~~

예:

~~~text
User: staff-101
Application: campus-admin
Agent: student-record-agent
Tool: student-read
Resource: student-2024001
~~~

이 정보가 있으면 감사에서 "누가 무엇을 왜 읽었는가"를 더 정확히 복구할 수 있다.

### Discovery는 Authorization이 아니다

에이전트가 어떤 기능이 존재한다는 것을 알게 됐다고 하자. MCP Tool Catalog나 A2A Agent Card를 통해 기능을 발견할 수 있다.

하지만:

~~~text
Discovery
≠ Authentication
≠ Authorization
≠ Approval
~~~

이다.

#### Discovery
무엇이 존재하는가.

#### Authentication
누가 요청했는가.

#### Authorization
이 권한을 부여받는 주체가 해당 Action/Resource를 사용할 수 있는가.

#### Approval
권한이 있어도 이번 행동을 지금 실행해도 되는가.

이 네 단계를 섞으면 Capability Catalog가 Permission List처럼 사용될 수 있다.

### Originating User Context

여러 에이전트의 협업이나 Tool Chain이 길어지면 처음 사용자 정보가 사라질 수 있다.

~~~text
User
  ↓
Agent A
  ↓
Agent B
  ↓
Tool
~~~

에이전트 B가 자신의 Service Identity만 사용하면 사용자의 권한 범위보다 넓은 행동을 할 수 있다. 가능한 시스템에서는 Originating User Context를 Delegation Chain에 유지한다. 권한 확인은 다음을 함께 볼 수 있다.

~~~text
originating_user
current_agent
delegation_scope
tool
resource
action
~~~

### Agent Lifecycle

에이전트의 신원은 만들기만 하면 끝나지 않는다. 유지 과정이 필요하다.

~~~text
create
→ activate
→ scope change
→ suspend
→ revoke
→ delete
~~~

에이전트 구현이 삭제됐는데 신원과 인증 정보가 남으면 Orphaned Privilege가 생긴다. Owner/Sponsor도 중요하다. "이 에이전트는 누가 책임지는가"가 명확해야 한다.

### Identity와 Memory

메모리에도 Actor가 있다.

메모리가 만들어질 때:

- 어떤 사용자가 Origin이었는가.
- 어떤 에이전트가 요약했는가.
- 어느 작업에서 생성됐는가.

를 남길 수 있다. 잘못된 메모리가 발견됐을 때 정보 원본을 추적하는 데 도움이 된다.

### Identity와 Audit

Audit Event에 단순 도구 이름만 남기면 부족할 수 있다.

예:

~~~text
action: add_issue_comment
actor: agent-42
on_behalf_of: user-7
tool_identity: github-commenter
resource: repo/app#123
policy: allow-v18
~~~

이 정도의 Actor Chain이 있으면 Incident 분석과 Access Review가 쉬워진다.

### 작은 예: 대학 학생정보 Agent

교직원 A가 학생 B의 정보를 조회한다.

~~~text
Human User:
staff-A

Application:
campus-admin

Agent:
student-record-agent

Tool:
student-record-read

Resource:
student-B
~~~

권한 확인은 다음을 볼 수 있다.

- staff-A가 student-B를 조회할 업무 권한이 있는가.
- 에이전트가 student record capability를 사용할 수 있는가.
- 도구는 read-only인가.
- Sensitive Field는 Masking이 필요한가.

에이전트라는 이유로 User Authorization을 건너뛰지 않는다.

### Identity를 Agent Prompt에 넣는 것과 Enforcement는 다르다

System Prompt에 다음을 넣을 수 있다.

> 당신은 staff-A를 대신해 동작한다.

컨텍스트(Context: 모델에 전달하는 정보)에는 도움이 된다. 하지만 Resource Access는 외부 권한 확인이 강제해야 한다.

~~~text
Identity Context
→ Model behavior hint

Authorization System
→ actual enforcement
~~~

둘을 구분한다.

### 이 장에서 가져갈 것

에이전트가 업무를 수행하면 "누가 행동을 했는가"를 하나의 Service Account로 축약하기 어렵다. 다음 경계를 유지한다.

~~~text
User
≠ Application
≠ Agent
≠ Tool
≠ Resource
~~~

그리고:

~~~text
Delegated Access
≠ Autonomous Access
~~~

신원을 분리하면 다음 질문이 생긴다. 각 신원이 외부 API에 접근할 때 인증 정보를 어디에 둘 것인가. 에이전트 실행 환경 안에 장기 API Key를 넣어둘 것인가. 다음 장에서는 인증 정보를 Agent Context와 실행 환경에서 가능한 한 분리하는 구조를 다룬다.

### Source Notes

- [S-ENTRA-AGENT-ID]
- [S-MS-OBO]
- [S-AWS-AGENTCORE-ID]

---

<!-- source-draft: chapters/15/draft.md -->

## 15장. Credential을 Agent에서 분리한다

에이전트 실행 환경에 다음 환경 변수가 들어 있다고 하자.

~~~text
GITHUB_TOKEN=...
SLACK_TOKEN=...
PROD_DB_PASSWORD=...
~~~

에이전트는 도구를 통해서만 이 인증 정보(Credential)를 사용하도록 설계돼 있다. 하지만 실행 환경 안에서 셸도 실행할 수 있다면 이야기가 달라진다. 에이전트가 의도적으로 비밀 정보를 읽지 않더라도 공격된 도구 실행 결과나 잘못된 Command가 인증 정보를 노출할 수 있다. 격리가 강력하더라도 실행 환경 안에 넓은 권한의 인증 정보가 있으면, 그 안에서 일으킬 수 있는 피해 범위는 여전히 크다. 인증 정보의 사용 경계를 별도 계층으로 보는 이유다.

### Standing Credential의 위험

장기 API Key나 Broad Service Account Credential을 에이전트 실행 환경에 넣으면 몇 가지 문제가 생긴다.

- 에이전트가 직접 읽을 수 있다.
- 도구를 우회해 다른 API에 사용할 수 있다.
- Runtime compromise 시 노출된다.
- 적용 범위가 현재 작업보다 넓을 수 있다.
- Revocation과 Rotation이 어렵다.

특히 에이전트가 셸, 브라우저, Code Execution을 사용할수록 Raw Credential Exposure를 줄이는 것이 중요하다.

### Agent는 Intent를 만들고 Gateway가 Credential을 사용한다

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

### Short-lived Credential

가능하면 인증 정보의 유지 기간을 줄인다.

~~~text
Long-lived Token
→ broad exposure window

Short-lived Token
→ smaller exposure window
~~~

Short-lived Token도 탈취될 수 있다. 하지만 Damage Window와 Revocation 부담을 줄일 수 있다. 특히 위험이 큰 행동에서는 행동 직전에 토큰을 발급하고 짧게 사용하는 방식이 유용하다.

### Delegated Token

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

### Autonomous Workload Token

정기 작업에는 사용자가 없을 수 있다.

~~~text
Scheduler
→ Agent Workload Identity
→ App / Workload Token
→ Resource
~~~

이 토큰에는 Autonomous Task에 필요한 최소 적용 범위만 둔다. Delegated Token과 Autonomous Token을 같은 것으로 취급하지 않는다.

### Credential Broker

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

### Tool별 Credential

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

### Credential Injection

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

### Endpoint Scope

인증 정보로 행사할 수 있는 권한 범위가 API 수준에서 충분히 좁지 않을 수 있다. 접근을 중개하는 게이트웨이에서 추가로 제한할 수 있다.

예:

~~~text
host = api.github.com
method = POST
path = /repos/org/app/pulls
~~~

에이전트에게 GitHub Token 전체를 주는 것과 특정 Endpoint Action만 허용하는 것은 다르다.

### Runtime Role도 Credential이다

Cloud Runtime이 IAM Role을 가진 경우 에이전트가 직접 비밀 정보 파일을 보지 않더라도 Runtime Metadata를 통해 인증 정보를 얻을 수 있다. 따라서 "비밀 정보를 환경 변수에 안 넣었다"만으로 충분하지 않다. Runtime Execution Role도 최소 권한이 필요하다.

예:

- per-agent role
- per-environment role
- per-task temporary policy
- restricted network
- short session

### Credential과 Sandbox

강한 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)가 Credential Risk를 자동으로 해결하지 않는다. 경량 가상 머신 안에 Broad Production Credential이 있다면 MicroVM Escape가 없어도 에이전트가 그 인증 정보로 정상 API를 호출해 큰 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)를 만들 수 있다.

따라서:

~~~text
Isolation
≠ Credential Scope
~~~

둘 다 필요하다.

### Credential과 Tool Result Injection

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

### Audit

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

### Revocation

에이전트가 Suspend되면 인증 정보도 함께 끊겨야 한다. 사용자가 Consent를 철회하면 Delegated Access가 중단돼야 한다. 도구가 Disable되면 해당 Credential Path도 막혀야 한다. Identity Lifecycle과 Credential Lifecycle을 연결한다.

### 작은 예: PR 작성 Agent

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

### 이 장에서 가져갈 것

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

### Source Notes

- [S-MS-OBO]
- [S-AWS-AGENTCORE-ID]
- [S-OPENSHELL]

---

<!-- source-draft: chapters/16/draft.md -->

## 16장. Sandbox와 Containment

에이전트에게 다음 지침을 줬다고 하자.

> 작업 공간 밖의 파일은 읽지 마라.

좋은 규칙이다. 하지만 호스트 파일 시스템에는 사용자의 SSH 키와 클라우드 인증 정보, 다른 프로젝트 소스 코드가 연결돼 있다. 에이전트가 외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)에 속거나 도구의 오류가 생기면 지침만으로 접근을 막기 어렵다. 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)의 역할은 모델을 더 순종적으로 만드는 것이 아니다.

**잘못 행동하더라도 도달 가능한 범위를 제한하는 것**이다.

### Containment

이 책에서 격리(Containment: 접근과 피해 범위를 제한하는 격리)는 다음 의미로 사용한다.

> 에이전트나 도구가 잘못 행동하더라도 접근 가능한 프로세스, 파일 시스템, 네트워크, 인증 정보(Credential)의 범위를 제한하는 Runtime Boundary.

즉:

~~~text
Model Safety
= 잘 행동할 가능성을 높인다

Containment
= 잘못 행동해도 피해 범위를 제한한다
~~~

둘 다 필요할 수 있다. 하지만 역할은 다르다.

### Sandbox와 Authorization

샌드박스가 있으면 권한 확인(Authorization)이 필요 없다고 생각할 수 있다. 그렇지 않다.

~~~text
Containment
= WHERE can it reach?

Authorization
= WHAT can it do?

Approval
= SHOULD it do this now?
~~~

예를 들어 에이전트가 Production API에 네트워크 접근은 가능하지만 read-only Credential만 가진 구조가 있을 수 있다. 네트워크 접근 경계와 권한 확인이 함께 작동한다.

### Filesystem Boundary

코드 작업 에이전트는 File Access가 필요하다. 하지만 전체 Home Directory를 줄 이유는 없을 수 있다.

예:

~~~text
Allowed:
/workspace/repo
/tmp/build

Denied:
/home/user/.ssh
/home/user/.aws
/etc
other repositories
~~~

Read와 Write Scope를 다르게 둘 수도 있다.

~~~text
Repository
→ read/write

Dependency Cache
→ read-only

System Path
→ denied
~~~

### Network Boundary

파일 시스템만 막고 네트워크를 모두 열면 Data Exfiltration 경로가 남는다. 반대로 네트워크만 막고 Secret File이 보이면 다른 도구이나 이후 단계에서 노출될 수 있다. 그래서 파일 시스템과 네트워크를 함께 본다.

네트워크 정책 예:

~~~text
allow:
- package registry
- github.com
- internal test API

deny:
- arbitrary internet
- production admin endpoint
~~~

더 세밀한 접근을 중개하는 게이트웨이는 Method와 Path까지 제한할 수 있다.

### Process Boundary

에이전트가 셸을 실행한다면 Child Process Capability도 중요하다.

고려 대상:

- privilege
- syscall
- process namespace
- executable allow/deny
- resource limit
- fork bomb
- device access

모든 에이전트에 Kernel 수준의 정책이 필요한 것은 아니다. Workload Risk에 따라 선택한다.

### Isolation 접근은 서로 다른 Trade-off를 가진다

에이전트 실행 환경에 사용할 수 있는 격리 접근은 여러 가지다.

~~~text
OS Policy / Sandbox
Container
Userspace Kernel
MicroVM
Dedicated VM / Host
~~~

이 순서를 절대적인 보안 등급으로 읽어서는 안 된다. 실제 선택은 Threat Model, 시작, Density, 호환성, GPU, Debugging Cost에 따라 달라진다.

### OS-level Sandbox

Local Coding Agent에서는 OS-level Sandbox가 실용적일 수 있다. Anthropic은 Claude Code의 Bash sandbox에 Linux bubblewrap과 macOS Seatbelt 같은 OS primitive를 사용하는 방식을 공개했다.

장점:

- 빠른 시작
- Local Workflow와 결합
- 필요한 Directory만 제한 가능

한계:

- Host Kernel 공유
- 정책 설계가 중요
- OS마다 작동 방식이 다름

### Container

컨테이너는 Process/Filesystem/Resource Isolation에 익숙한 도구다. 하지만 기본 컨테이너 설정만으로 Untrusted Agent Workload에 충분하다고 가정하지 않는다. 다음이 중요하다.

- privilege
- capability
- mount
- network
- seccomp
- AppArmor/SELinux
- namespace

"컨테이너를 쓴다"보다 적용된 Isolation Policy가 중요하다.

### gVisor

gVisor는 Userspace Application Kernel을 사용해 애플리케이션과 Host Kernel 사이의 Syscall Surface를 줄이는 접근이다. 일반 컨테이너보다 Stronger Isolation을 원하면서 VM보다 가벼운 형태가 필요할 때 후보가 될 수 있다.

얻는 점과 감수할 점:

- 호환성
- Performance
- Operational Complexity

특정 에이전트에 무조건 권장하는 기술은 아니다.

### MicroVM

Firecracker 같은 경량 가상 머신은 KVM Hardware Virtualization Boundary를 사용한다. AgentCore Runtime처럼 세션별 경량 가상 머신을 사용해 CPU, 메모리, 파일 시스템을 격리하는 Managed Runtime 사례도 있다.

장점:

- Guest Kernel 분리
- Multi-tenant 격리에 유리
- Runtime disposal이 명확

비용:

- Image 관리
- Virtualization Infrastructure
- 시작 / Resource Overhead
- GPU/Device Complexity

### Disposable Runtime

에이전트 실행 환경을 Durable State Store로 사용하지 않으면 격리와 복구가 쉬워진다.

~~~text
Durable State
      +
Disposable Runtime
~~~

실행 환경이 손상되거나 비정상 종료하면 새 환경을 만들고 상태 관리 계층에서 실행 재개할 수 있다. 이 원칙은 Part III와 연결된다.

### Sandbox 안의 Credential

강한 샌드박스라도 인증 정보가 과도하면 위험하다.

~~~text
MicroVM
+ production-admin token
~~~

은 VM Escape 없이도 Production 전체를 수정할 수 있다. 격리는 인증 정보로 행사할 수 있는 권한 범위를 대체하지 않는다. Part V의 흐름이 다음처럼 연결되는 이유다.

~~~text
Identity
→ Credential
→ Sandbox
→ Policy
~~~

### Tool Output과 Network

에이전트가 외부 Web을 읽을 수 있으면 Prompt Injection Surface가 커진다. 네트워크 정책으로 정보 원본을 제한할 수 있다.

예:

~~~text
Research Agent
→ public web allowed

Repository Fix Agent
→ package registry + GitHub only
~~~

에이전트 역할에 따라 Network Profile이 다를 수 있다.

### Resource Limit

격리는 보안뿐 아니라 반복 실행의 신뢰성에도 필요하다.

예:

- CPU Limit
- Memory Limit
- Disk Limit
- Process Count
- 응답 시간 초과

잘못된 빌드나 무한 반복이 호스트 전체에 영향을 주지 않도록 한다.

### Runtime Session은 Durable State가 아니다

Managed Runtime이 세션을 제공한다고 하자. 기본 compute의 memory와 local disk는 Runtime lifecycle에 묶일 수 있다. 반대로 AgentCore의 managed session storage처럼 stop/resume 사이에 작업 공간 파일을 복원하는 기능도 존재한다. 중요한 것은 "실행 환경이 항상 ephemeral인가"가 아니라 **Workspace Persistence와 Agent Execution State의 책임을 분리하는 것**이다.

~~~text
Runtime / Session Storage
= execution workspace lifecycle

Agent State Plane
= execution continuity
~~~

작업 공간이 복원되더라도 목표와 Artifact Reference, 승인 상태, 이미 실행한 External Side Effect는 별도 상태에서 확인할 수 있어야 한다.

### 작은 예: Repository Fix Agent

위험이 낮은 Local Fix Task:

~~~text
Filesystem:
repo read/write

Network:
package registry + GitHub read

Credential:
none or read-only

Runtime:
OS sandbox / container
~~~

Production Deploy Task:

~~~text
Filesystem:
artifact only

Network:
deployment endpoint only

Credential:
short-lived deploy token

Runtime:
stronger isolated environment

Approval:
required
~~~

같은 에이전트 제품이라도 작업의 위험에 따라 Runtime Profile이 달라질 수 있다.

### Isolation 선택 기준

기술 이름보다 다음 질문이 먼저다.

- Untrusted Code를 실행하는가.
- Multi-tenant인가.
- 비밀 정보를 다루는가.
- Production Access가 있는가.
- Arbitrary Network가 필요한가.
- GPU/Device가 필요한가.
- Startup Latency가 중요한가.
- Workspace Persistence가 필요한가.
- 오류 원인 분석이 얼마나 중요한가.

이 조건으로 Isolation Level을 선택한다.

### 이 장에서 가져갈 것

샌드박스는 에이전트에게 "하지 마라"고 말하는 기능이 아니다. 잘못 행동했을 때도 접근할 수 없는 경계를 만드는 기능이다.

~~~text
Instruction
→ behavioral guidance

Authorization
→ action permission

Containment
→ reachable boundary
~~~

세 계층을 분리한다. 다음 장에서는 이 통제를 모든 작업에 동일하게 적용하지 않는 방법을 다룬다. Read-only 분석과 운영 환경 배포가 같은 샌드박스, 인증 정보, 승인 정책을 가져야 할 이유는 없다. Risk-adaptive Policy로 넘어간다.

### Source Notes

- [S-CLAUDE-SANDBOX]
- [S-GVISOR]
- [S-FIRECRACKER]
- [S-AWS-AGENTCORE-RUNTIME]
- [S-OPENSHELL]

---

<!-- source-draft: chapters/17/draft.md -->

## 17장. Risk-adaptive Policy

도구를 호출할 때마다 사람의 승인을 받으면 안전해 보인다. 하지만 실제 운영에서는 다른 문제가 생긴다. 에이전트가 파일을 읽을 때마다 묻고, 테스트를 실행할 때마다 묻고, 이슈를 조회할 때마다 묻는다. 사용자는 결국 내용을 읽지 않고 승인을 누르기 시작한다. 반대 극단도 있다. 승인 피로를 없애려고 에이전트에 넓은 권한을 한 번 주고 모두 자동화한다. 둘 다 좋은 기본값은 아니다. 작업의 위험에 따라 **어떤 통제를 얼마나 강하게 적용할지 다르게 설계**할 필요가 있다.

### 모든 Action의 Risk는 같지 않다

다음 행동을 비교해보자.

~~~text
README 읽기
Local Test 실행
GitHub Issue Comment 작성
Production Deploy
Payment 실행
~~~

모두 도구 호출이지만 Consequence가 다르다. 위험 판단에는 여러 Dimension이 있다.

- Read vs Write
- Local vs External
- Reversible vs Irreversible
- Data Sensitivity
- Production 여부
- Financial / Legal Consequence
- 인증 정보로 행사할 수 있는 권한 범위
- Arbitrary Code Execution
- Delegation Depth

따라서 단순 "도구 사용 가능/불가능"보다 통제 수단의 조합이 필요하다.

### R0~R4 Control Profile

이 책에서는 설명을 위해 R0~R4 예시를 사용한다. 외부 표준 Risk Taxonomy가 아니다.

#### R0 — Offline Read

예:

- Local Document 분석
- Static Source 읽기

통제:

- 인증 정보(Credential) 없음
- External Write 없음
- 기본 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)

#### R1 — Workspace Mutation

예:

- Repository File 수정
- Local Build/Test

통제:

- Workspace Scope
- 제한된 네트워크
- Production Credential 없음
- 정해진 규칙에 따른 검증

#### R2 — External Read

예:

- GitHub Read
- Internal API Read

통제:

- Read-only Credential
- Endpoint Allowlist
- 감사

#### R3 — Bounded External Write

예:

- PR 생성
- Issue Comment
- Slack Message

통제:

- Scoped Credential
- Target Validation
- 멱등성(Idempotency: 같은 요청을 반복해도 결과가 중복되지 않는 성질)
- 감사
- 조건부 승인

#### R4 — High-impact / Irreversible

예:

- 운영 환경 배포
- Payment
- Security Policy 변경
- Production DB Mutation

통제:

- Stronger Isolation
- Short-lived Credential
- Explicit Policy Gate
- Independent Verification
- Human/Trusted 승인
- Rollback or Compensation Plan

이 분류의 목적은 Label 자체가 아니다. 위험에 따라 통제를 다르게 조합하는 사고방식이다.

### Risk Input은 하나의 Score가 아닐 수 있다

운영 정책은 여러 입력을 함께 본다.

~~~text
Action Risk
Resource Sensitivity
Reversibility
Originating User Authority
Agent Identity
Delegation Scope
Environment
Credential Scope
~~~

예를 들어 같은 add_comment 도구이라도:

~~~text
public issue comment
vs
student disciplinary record comment
~~~

는 위험이 다를 수 있다. Tool Name만으로 위험을 결정하지 않는다.

### External Policy Evaluation

모델이 "이 행동은 안전하다"고 판단한 결과를 최종 권한 확인(Authorization)으로 사용하지 않는다. 특히 모델이 같은 untrusted input에 노출돼 있다면 risk classification 자체도 시스템이 정해진 규칙으로 적용하는 정책을 거쳐야 한다.

추천 구조:

~~~text
Agent proposes Action
        ↓
External Policy Engine
        ↓
Evaluate:
- user
- agent
- tool
- resource
- environment
- risk
        ↓
Control Profile
~~~

통제 수단의 조합은 다음을 결정할 수 있다.

- Allow/Deny
- Runtime Isolation
- 인증 정보로 행사할 수 있는 권한 범위
- 승인
- 검증 담당자
- Logging

### Human Approval은 Risk-tiered하게

AWS가 공개한 Agentic AI Lens에서는 모든 행동을 사람의 검토에 보내는 방식이 Approval Fatigue와 Rubber-stamp Review를 만들 수 있다고 지적한다. 이는 vendor guidance이며 업계 공통 표준으로 해석하지 않는다. 사람의 검토는 다음과 같이 판단 비용과 영향이 큰 행동에 집중하는 편이 낫다.

- High-impact
- Irreversible
- Sensitive Data
- Ambiguous Authority
- Policy Exception

Read-only Low-risk Action까지 같은 수준의 승인을 요구하면 Human Attention을 소모한다.

### Reviewer Context

Approval UI에는 "승인하시겠습니까?"만 보여주면 부족하다. 검토 담당자가 판단할 컨텍스트(Context: 모델에 전달하는 정보)가 필요하다.

예:

~~~text
Action:
Deploy release 1.4.2

Target:
production / cluster-a

Changes:
commit abc123 → def456

Verification:
integration pass
security scan pass

Rollback:
release 1.4.1

Requested by:
agent deploy-7 on behalf of user-10
~~~

Approval Quality는 검토 담당자에게 제공되는 근거 품질에 영향을 받는다.

### Originating User Authorization

Agent Chain이 길어져도 사용자 권한을 유지해야 한다.

~~~text
User
  ↓
Agent A
  ↓
Agent B
  ↓
Tool
~~~

에이전트 B의 Service Credential이 사용자보다 넓다고 해서 넓은 접근 대상 자원에 접근하게 두지 않는다. 정책은 Originating User와 Current Agent를 함께 볼 수 있다.

### Policy as Code

프롬프트 안의 자연어 규칙은 Guidance다. Critical Boundary는 Machine-enforceable Policy가 더 적합하다.

예:

~~~text
if environment == "production"
and action == "deploy"
then approval_required = true
~~~

또는:

~~~text
student_record.read
allowed only if
user.department == student.department
~~~

Policy Engine, IAM, 접근을 중개하는 게이트웨이 등 구현 방식은 다양하다. 핵심은 Enforcement가 Model Reasoning 밖에 있다는 점이다.

### Fail Closed

Critical Policy에서 Parsing Error나 Control Plane Failure가 발생했다고 하자.

위험한 기본값:

~~~text
policy unavailable
→ allow
~~~

더 안전한 기본값:

~~~text
policy unavailable
→ deny / pause
~~~

모든 Low-risk 작업까지 무조건 Fail Closed로 할 필요는 없을 수 있다. 하지만 High-impact Boundary는 permissive fallback을 피한다.

### Just-in-time Privilege

Standing Broad Permission 대신 필요한 시점에 잠깐 권한을 높일 수 있다.

예:

~~~text
Normal:
repo read/write

Deploy Step:
request temporary deploy privilege

After Step:
privilege expires
~~~

AWS의 Agentic AI Lens는 Dynamic Boundary와 Temporary Credential 같은 패턴을 권고한다. 이 역시 하나의 공개 운영 지침 사례로 사용한다. 에이전트의 전체 유지 기간 동안 High-risk 권한을 유지할 필요가 없다.

### Agent가 권한 확대를 제안할 수는 있다

최소 권한을 강하게 적용하면 에이전트가 필요한 행동에서 거부를 만날 수 있다. 두 가지 극단이 있다.

1. 모든 거부를 사람에게 넘긴다.
2. 에이전트가 자기 정책을 수정한다.

두 번째는 위험하다. 더 나은 구조는 다음과 같다.

~~~text
Deny
  ↓
Inspect
  ↓
Agent proposes minimal policy change
  ↓
Deterministic validation
  ↓
Risk analysis
  ↓
Review / Approval
  ↓
Apply versioned policy
  ↓
Retry
~~~

NVIDIA OpenShell의 Agent-driven Policy Management는 이런 방향의 한 사례다. 에이전트는 필요한 기능이나 최소 policy change를 제안할 수 있지만, Policy Authority와 실제 적용 권한은 외부에 남긴다.

### Effective Policy Manifest

에이전트가 현재 무엇을 할 수 있는지 전혀 모르면 Trial-and-error Deny를 반복할 수 있다. 따라서 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)에 Current Effective Policy를 필요한 정보를 골라 구성할 수 있다.

예:

~~~text
Allowed:
- repo read/write
- tests
- GitHub read

Requires Approval:
- create PR

Denied:
- production deploy
~~~

이 Manifest는 Planning을 돕는다. 하지만 Enforcement Source는 아니다.

~~~text
Policy Manifest
= model-facing projection

Policy Engine
= authority
~~~

컨텍스트와 상태의 관계와 비슷하다.

### Independent Verification

위험이 큰 행동은 실행 전/후에 별도 검증을 요구할 수 있다.

예:

~~~text
Deploy Candidate
      ↓
Independent Test
      ↓
Policy Check
      ↓
Approval
      ↓
Deploy
      ↓
Health Verification
~~~

검증 담당자가 실행 담당자와 완전히 다른 모델이어야 한다는 뜻은 아니다. 가능하면 정해진 규칙에 따른 검증을 우선한다.

### Rollback과 Compensation

되돌릴 수 없는 행동은 완전히 되돌릴 수 없을 수 있다. 그래도 Compensation Plan이 필요할 수 있다.

예:

- Deploy → previous release rollback
- Payment → refund
- Message send → correction message
- DB update → compensating update

Risk Policy는 행동 이전에 Recovery Surface도 확인할 수 있다.

### 작은 예: Coding Agent의 세 Task

#### Task A: 코드 읽기

~~~text
Risk:
R0/R1

Controls:
workspace sandbox
no external write
no approval
~~~

#### Task B: PR 생성

~~~text
Risk:
R3

Controls:
scoped GitHub credential
repo allowlist
idempotency
audit
approval optional by organization policy
~~~

#### Task C: Production Deploy

~~~text
Risk:
R4

Controls:
strong isolation
short-lived deploy credential
artifact verification
explicit approval
rollback plan
post-deploy health check
~~~

같은 에이전트 실행 환경을 무조건 재사용할 필요도 없다.

### 이 장에서 가져갈 것

에이전트 보안을 하나의 "승인 여부"로 축약하지 않는다.

~~~text
Identity
= who

Authorization
= what

Containment
= where

Approval
= whether now
~~~

그리고 위험에 따라 이 통제의 강도를 다르게 한다. 핵심은 에이전트가 위험을 스스로 선언하는 것이 아니다. External Policy가 신원, 접근 대상 자원, 환경, Consequence를 바탕으로 통제 수단의 조합을 결정하는 것이다. Part V에서는 에이전트가 행동을 수행하기 위한 보안 경계를 완성했다. 다음 Part에서는 이 시스템이 제대로 동작하는지 어떻게 관찰하고 측정할 것인가를 다룬다. 실행 추적 기록(Trace), 평가, 회귀(Regression: 변경 뒤 기존 기능이 나빠지는 회귀), Harness Improvement로 넘어간다.

### Source Notes

- [S-AWS-AGENTIC-LENS]
- [S-AWS-CEDAR]
- [S-OPENSHELL]
- [B-RISK-PROFILE]
