# Part V. Identity, Security, Runtime

# 14장. Agent Identity와 Delegation

Agent가 GitHub Issue를 생성했다.

Audit Log에는 다음만 남아 있다.

~~~text
actor = service-account@company
~~~

그런데 질문은 더 많다.

누가 이 Agent를 시작했는가. 어떤 Application이 Agent를 Hosting했는가. Agent는 누구를 대신해 행동했는가. 어떤 Tool Identity가 실제 API를 호출했는가. 이 Action은 사용자의 권한에서 나온 것인가, Autonomous Workload 권한에서 나온 것인가.

Agent가 업무를 수행하려면 **누가 행동하는가**를 먼저 분리해야 한다.

## Shared Service Account의 한계

초기 Agent는 하나의 Service Account를 공유하기 쉽다.

~~~text
Agent A ─┐
Agent B ─┼→ shared-service-account
Agent C ─┘
~~~

구현은 단순하다.

하지만 다음 문제가 생긴다.

- 어떤 Agent가 Action을 수행했는지 구분하기 어렵다.
- 사용자 위임과 Autonomous Action을 분리하기 어렵다.
- Agent별 권한 축소가 어렵다.
- 하나의 Credential 노출이 여러 Agent에 영향을 준다.
- Agent lifecycle과 Credential lifecycle이 묶인다.

Agent가 늘어날수록 Identity를 별도 문제로 다뤄야 한다.

## Identity를 나눈다

이 책에서는 다음 Identity를 구분한다.

~~~text
Human User Identity
Application Identity
Agent Identity
Workload Identity
Tool Identity
Resource Identity
~~~

모든 시스템이 여섯 개의 별도 Principal을 가져야 한다는 뜻은 아니다.

책임을 분리하기 위한 taxonomy다.

## Human User Identity

요청을 시작한 사용자다.

예:

- 교직원
- 개발자
- 운영자
- 고객

User가 Agent에게 Action을 요청할 수 있다.

중요한 것은 Agent가 User보다 넓은 권한을 자동으로 얻지 않는 것이다.

## Application Identity

Agent를 Hosting하는 Application의 Identity다.

예:

~~~text
campus-assistant-web
coding-agent-service
operations-console
~~~

Application과 Agent를 같은 Identity로 두면 어떤 Agent가 어떤 권한을 썼는지 구분하기 어려울 수 있다.

## Agent Identity

특정 Agent를 구분하는 Principal이다.

Microsoft Entra Agent ID 같은 최신 Identity 제품은 Agent를 별도 Service Principal 계열로 다루는 방향을 보여준다.

Agent Identity에는 다음 Metadata가 연결될 수 있다.

- owner / sponsor
- purpose
- allowed capability class
- lifecycle
- environment
- risk profile

Agent가 코드 객체이기만 한 것이 아니라 Security Principal이 되는 셈이다.

## Workload Identity

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

## Tool Identity

한 Agent 안에서도 Tool별로 Credential Scope를 분리할 수 있다.

예:

~~~text
Agent
  ├─ GitHub Read Tool
  ├─ Slack Write Tool
  └─ Production DB Read-only Tool
~~~

모든 Tool이 같은 Broad Credential을 공유할 필요는 없다.

Tool Identity는 다음 장의 Credential Boundary와 연결된다.

## Resource Identity

Action의 대상도 Identity나 Resource Identifier를 가진다.

예:

- Repository A
- Slack Channel B
- Student Record C
- Production Cluster D

Authorization은 "Agent가 Tool을 호출할 수 있는가"만 보는 것이 아니라 어떤 Resource에 적용되는지도 봐야 한다.

## Delegated Access

사용자를 대신해 Agent가 행동하는 경우다.

~~~text
User
  ↓ consent / scope
Agent
  ↓ delegated token
Resource
~~~

예를 들어 교직원이 자신의 권한 안에서 학생 정보를 조회하도록 Agent에게 요청할 수 있다.

이때 Agent는 User보다 더 넓은 학생 범위를 볼 수 없어야 한다.

Delegated Mode에서는 User Context가 Authorization Input으로 남아야 한다.

## Autonomous Access

특정 User가 없는 실행도 있다.

~~~text
System / Scheduler
  ↓
Agent Workload Identity
  ↓
Resource
~~~

예:

- 새벽 Log 분석
- Repository Dependency Check
- 정기 운영 리포트

이 경우 User Delegation Token보다 Application/Workload Credential이 적합하다.

Delegated와 Autonomous Mode를 한 Credential 모델로 합치지 않는다.

## Actor Chain

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

이 정보가 있으면 Audit에서 "누가 무엇을 왜 읽었는가"를 더 정확히 복구할 수 있다.

## Discovery는 Authorization이 아니다

Agent가 어떤 Capability가 존재한다는 것을 알게 됐다고 하자.

MCP Tool Catalog나 A2A Agent Card를 통해 Capability를 발견할 수 있다.

하지만:

~~~text
Discovery
≠ Authentication
≠ Authorization
≠ Approval
~~~

이다.

### Discovery
무엇이 존재하는가.

### Authentication
누가 요청했는가.

### Authorization
이 Principal이 해당 Action/Resource를 사용할 수 있는가.

### Approval
권한이 있어도 이번 Action을 지금 실행해도 되는가.

이 네 단계를 섞으면 Capability Catalog가 Permission List처럼 사용될 수 있다.

## Originating User Context

Multi-Agent나 Tool Chain이 길어지면 처음 User 정보가 사라질 수 있다.

~~~text
User
  ↓
Agent A
  ↓
Agent B
  ↓
Tool
~~~

Agent B가 자신의 Service Identity만 사용하면 User Scope보다 넓은 Action을 할 수 있다.

가능한 시스템에서는 Originating User Context를 Delegation Chain에 유지한다.

Authorization은 다음을 함께 볼 수 있다.

~~~text
originating_user
current_agent
delegation_scope
tool
resource
action
~~~

## Agent Lifecycle

Agent Identity는 만들기만 하면 끝나지 않는다.

Lifecycle이 필요하다.

~~~text
create
→ activate
→ scope change
→ suspend
→ revoke
→ delete
~~~

Agent 구현이 삭제됐는데 Identity와 Credential이 남으면 Orphaned Privilege가 생긴다.

Owner/Sponsor도 중요하다.

"이 Agent는 누가 책임지는가"가 명확해야 한다.

## Identity와 Memory

Memory에도 Actor가 있다.

Memory가 만들어질 때:

- 어떤 User가 Origin이었는가.
- 어떤 Agent가 Summary했는가.
- 어느 Task에서 생성됐는가.

를 남길 수 있다.

잘못된 Memory가 발견됐을 때 Source를 추적하는 데 도움이 된다.

## Identity와 Audit

Audit Event에 단순 Tool 이름만 남기면 부족할 수 있다.

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

## 작은 예: 대학 학생정보 Agent

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

Authorization은 다음을 볼 수 있다.

- staff-A가 student-B를 조회할 업무 권한이 있는가.
- Agent가 student record capability를 사용할 수 있는가.
- Tool은 read-only인가.
- Sensitive Field는 Masking이 필요한가.

Agent라는 이유로 User Authorization을 건너뛰지 않는다.

## Identity를 Agent Prompt에 넣는 것과 Enforcement는 다르다

System Prompt에 다음을 넣을 수 있다.

> 당신은 staff-A를 대신해 동작한다.

Context에는 도움이 된다.

하지만 Resource Access는 외부 Authorization이 강제해야 한다.

~~~text
Identity Context
→ Model behavior hint

Authorization System
→ actual enforcement
~~~

둘을 구분한다.

## 이 장에서 가져갈 것

Agent가 업무를 수행하면 "누가 Action을 했는가"를 하나의 Service Account로 축약하기 어렵다.

다음 경계를 유지한다.

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

Identity를 분리하면 다음 질문이 생긴다.

각 Identity가 External API에 접근할 때 Credential을 어디에 둘 것인가.

Agent Runtime 안에 장기 API Key를 넣어둘 것인가.

다음 장에서는 Credential을 Agent Context와 Runtime에서 가능한 한 분리하는 구조를 다룬다.

## 주요 근거

- Microsoft Entra Agent ID
- Microsoft Identity Fundamentals for AI Agents
- Microsoft Agent On-Behalf-Of Flow
- AWS AgentCore Identity
- A2A Authorization model
- research/topics/10-agent-identity-authorization.md
- research/topics/19-delegated-agent-identity-zero-trust.md


---

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

NVIDIA OpenShell 같은 최신 Agent Sandbox 설계에서는 Agent Workload가 Secret을 직접 보지 않고 Gateway가 승인된 Endpoint Request에 Credential을 붙이는 구조를 사용한다.

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

다음 장에서는 Credential이 있든 없든 Agent가 Runtime에서 접근할 수 있는 범위를 다룬다.

Filesystem, Process, Network를 어디까지 열어줄 것인가.

Sandbox와 Containment로 넘어간다.

## 주요 근거

- Microsoft Entra Agent ID / On-Behalf-Of Flow
- AWS AgentCore Identity
- NVIDIA OpenShell
- research/topics/19-delegated-agent-identity-zero-trust.md


---

# 16장. Sandbox와 Containment

Agent에게 다음 Instruction을 줬다고 하자.

> Workspace 밖의 파일은 읽지 마라.

좋은 규칙이다.

하지만 호스트 File System에는 사용자의 SSH Key와 Cloud Credential, 다른 Project Source가 Mount돼 있다.

Agent가 Prompt Injection에 속거나 Tool Bug가 생기면 Instruction만으로 Access를 막기 어렵다.

Sandbox의 역할은 Model을 더 순종적으로 만드는 것이 아니다.

**잘못 행동하더라도 도달 가능한 범위를 제한하는 것**이다.

## Containment

이 책에서 Containment는 다음 의미로 사용한다.

> Agent나 Tool이 잘못 행동하더라도 접근 가능한 Process, Filesystem, Network, Credential의 범위를 제한하는 Runtime Boundary.

즉:

~~~text
Model Safety
= 잘 행동할 가능성을 높인다

Containment
= 잘못 행동해도 피해 범위를 제한한다
~~~

둘 다 필요할 수 있다.

하지만 역할은 다르다.

## Sandbox와 Authorization

Sandbox가 있으면 Authorization이 필요 없다고 생각할 수 있다.

그렇지 않다.

~~~text
Containment
= WHERE can it reach?

Authorization
= WHAT can it do?

Approval
= SHOULD it do this now?
~~~

예를 들어 Agent가 Production API에 Network 접근은 가능하지만 read-only Credential만 가진 구조가 있을 수 있다.

Network Boundary와 Authorization이 함께 작동한다.

## Filesystem Boundary

Coding Agent는 File Access가 필요하다.

하지만 전체 Home Directory를 줄 이유는 없을 수 있다.

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

## Network Boundary

Filesystem만 막고 Network를 모두 열면 Data Exfiltration 경로가 남는다.

반대로 Network만 막고 Secret File이 보이면 다른 Tool이나 이후 단계에서 노출될 수 있다.

그래서 Filesystem과 Network를 함께 본다.

Network Policy 예:

~~~text
allow:
- package registry
- github.com
- internal test API

deny:
- arbitrary internet
- production admin endpoint
~~~

더 세밀한 Gateway는 Method와 Path까지 제한할 수 있다.

## Process Boundary

Agent가 Shell을 실행한다면 Child Process Capability도 중요하다.

고려 대상:

- privilege
- syscall
- process namespace
- executable allow/deny
- resource limit
- fork bomb
- device access

모든 Agent에 Kernel 수준의 Policy가 필요한 것은 아니다.

Workload Risk에 따라 선택한다.

## Isolation Level

격리 기술은 여러 층이 있다.

개념적으로:

~~~text
OS Policy / Sandbox
        ↓
Container
        ↓
Userspace Kernel
        ↓
MicroVM
        ↓
Dedicated VM / Host
~~~

위로 갈수록 무조건 좋다는 뜻은 아니다.

Startup, Density, Compatibility, GPU, Debugging Cost가 달라진다.

## OS-level Sandbox

Local Coding Agent에서는 OS-level Sandbox가 실용적일 수 있다.

Anthropic Claude Code는 Linux의 bubblewrap 계열과 macOS Seatbelt 등을 사용해 Filesystem과 Network Boundary를 강화하는 접근을 공개했다.

장점:

- 빠른 Startup
- Local Workflow와 결합
- 필요한 Directory만 제한 가능

한계:

- Host Kernel 공유
- Policy 설계가 중요
- OS마다 Mechanism이 다름

## Container

Container는 Process/Filesystem/Resource Isolation에 익숙한 도구다.

하지만 기본 Container 설정만으로 Untrusted Agent Workload에 충분하다고 가정하지 않는다.

다음이 중요하다.

- privilege
- capability
- mount
- network
- seccomp
- AppArmor/SELinux
- namespace

"Container를 쓴다"보다 적용된 Isolation Policy가 중요하다.

## gVisor

gVisor는 Userspace Application Kernel을 사용해 Application과 Host Kernel 사이의 Syscall Surface를 줄이는 접근이다.

일반 Container보다 Stronger Isolation을 원하면서 VM보다 가벼운 형태가 필요할 때 후보가 될 수 있다.

Trade-off:

- Compatibility
- Performance
- Operational Complexity

특정 Agent에 무조건 권장하는 기술은 아니다.

## MicroVM

Firecracker 같은 MicroVM은 KVM Hardware Virtualization Boundary를 사용한다.

AgentCore Runtime처럼 Session별 MicroVM을 사용해 CPU, Memory, Filesystem을 격리하는 Managed Runtime 사례도 있다.

장점:

- Guest Kernel 분리
- Multi-tenant 격리에 유리
- Runtime disposal이 명확

비용:

- Image 관리
- Virtualization Infrastructure
- Startup / Resource Overhead
- GPU/Device Complexity

## Disposable Runtime

Agent Runtime을 Durable State Store로 사용하지 않으면 격리와 Recovery가 쉬워진다.

~~~text
Durable State
      +
Disposable Runtime
~~~

Runtime이 손상되거나 Crash하면 새 Environment를 만들고 State Plane에서 Resume할 수 있다.

이 원칙은 Part III와 연결된다.

## Sandbox 안의 Credential

강한 Sandbox라도 Credential이 과도하면 위험하다.

~~~text
MicroVM
+ production-admin token
~~~

은 VM Escape 없이도 Production 전체를 수정할 수 있다.

Containment는 Credential Scope를 대체하지 않는다.

Part V의 흐름이 다음처럼 연결되는 이유다.

~~~text
Identity
→ Credential
→ Sandbox
→ Policy
~~~

## Tool Output과 Network

Agent가 외부 Web을 읽을 수 있으면 Prompt Injection Surface가 커진다.

Network Policy로 Source를 제한할 수 있다.

예:

~~~text
Research Agent
→ public web allowed

Repository Fix Agent
→ package registry + GitHub only
~~~

Agent 역할에 따라 Network Profile이 다를 수 있다.

## Resource Limit

Containment는 Security뿐 아니라 Reliability에도 필요하다.

예:

- CPU Limit
- Memory Limit
- Disk Limit
- Process Count
- Timeout

잘못된 Build나 Infinite Loop가 Host 전체를 영향을 주지 않게 한다.

## Runtime Session은 Durable State가 아니다

Managed Runtime이 Session을 제공한다고 하자.

기본 compute의 memory와 local disk는 Runtime lifecycle에 묶일 수 있다. 반대로 AgentCore의 managed session storage처럼 stop/resume 사이에 Workspace 파일을 복원하는 기능도 존재한다.

중요한 것은 "Runtime이 항상 ephemeral인가"가 아니라 **Workspace Persistence와 Agent Execution State의 책임을 분리하는 것**이다.

~~~text
Runtime / Session Storage
= execution workspace lifecycle

Agent State Plane
= execution continuity
~~~

Workspace가 복원되더라도 Goal과 Artifact Reference, Approval State, 이미 실행한 External Side Effect는 별도 State에서 확인할 수 있어야 한다.

## 작은 예: Repository Fix Agent

Risk가 낮은 Local Fix Task:

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

같은 Agent 제품이라도 Task Risk에 따라 Runtime Profile이 달라질 수 있다.

## Isolation 선택 기준

기술 이름보다 다음 질문이 먼저다.

- Untrusted Code를 실행하는가.
- Multi-tenant인가.
- Secret을 다루는가.
- Production Access가 있는가.
- Arbitrary Network가 필요한가.
- GPU/Device가 필요한가.
- Startup Latency가 중요한가.
- Workspace Persistence가 필요한가.
- Debugging이 얼마나 중요한가.

이 조건으로 Isolation Level을 선택한다.

## 이 장에서 가져갈 것

Sandbox는 Agent에게 "하지 마라"고 말하는 기능이 아니다.

잘못 행동했을 때도 접근할 수 없는 경계를 만드는 기능이다.

~~~text
Instruction
→ behavioral guidance

Authorization
→ action permission

Containment
→ reachable boundary
~~~

세 계층을 분리한다.

다음 장에서는 이 통제를 모든 Task에 동일하게 적용하지 않는 방법을 다룬다.

Read-only 분석과 Production Deploy가 같은 Sandbox, Credential, Approval 정책을 가져야 할 이유는 없다.

Risk-adaptive Policy로 넘어간다.

## 주요 근거

- Anthropic, Claude Code Sandboxing
- Anthropic, How We Contain Claude Across Products
- gVisor Security Architecture
- Firecracker Design
- AWS AgentCore Runtime
- NVIDIA OpenShell
- research/topics/11-sandbox-runtime-isolation.md


---

# 17장. Risk-adaptive Policy

모든 Tool Call마다 사람에게 승인받도록 만들면 안전해 보인다.

운영에서는 다른 문제가 생긴다.

Agent가 File을 읽을 때마다 묻고, Test를 실행할 때마다 묻고, Issue를 조회할 때마다 묻는다.

사용자는 결국 내용을 읽지 않고 Approve를 누르기 시작한다.

반대 극단도 있다.

승인 피로를 없애려고 Agent에 넓은 권한을 한 번 주고 모두 자동화한다.

둘 다 좋은 기본값은 아니다.

Task Risk에 따라 **어떤 Control을 얼마나 강하게 적용할지 다르게 설계**할 필요가 있다.

## 모든 Action의 Risk는 같지 않다

다음 Action을 비교해보자.

~~~text
README 읽기
Local Test 실행
GitHub Issue Comment 작성
Production Deploy
Payment 실행
~~~

모두 Tool Call이지만 Consequence가 다르다.

Risk 판단에는 여러 Dimension이 있다.

- Read vs Write
- Local vs External
- Reversible vs Irreversible
- Data Sensitivity
- Production 여부
- Financial / Legal Consequence
- Credential Scope
- Arbitrary Code Execution
- Delegation Depth

따라서 단순 "Tool 사용 가능/불가능"보다 Control Profile이 필요하다.

## R0~R4 Control Profile

이 책에서는 설명을 위해 R0~R4 예시를 사용한다.

외부 표준 Risk Taxonomy가 아니다.

### R0 — Offline Read

예:

- Local Document 분석
- Static Source 읽기

Control:

- Credential 없음
- External Write 없음
- 기본 Sandbox

### R1 — Workspace Mutation

예:

- Repository File 수정
- Local Build/Test

Control:

- Workspace Scope
- 제한된 Network
- Production Credential 없음
- Deterministic Verification

### R2 — External Read

예:

- GitHub Read
- Internal API Read

Control:

- Read-only Credential
- Endpoint Allowlist
- Audit

### R3 — Bounded External Write

예:

- PR 생성
- Issue Comment
- Slack Message

Control:

- Scoped Credential
- Target Validation
- Idempotency
- Audit
- 조건부 Approval

### R4 — High-impact / Irreversible

예:

- Production Deploy
- Payment
- Security Policy 변경
- Production DB Mutation

Control:

- Stronger Isolation
- Short-lived Credential
- Explicit Policy Gate
- Independent Verification
- Human/Trusted Approval
- Rollback or Compensation Plan

이 분류의 목적은 Label 자체가 아니다.

Risk에 따라 Control을 다르게 조합하는 사고방식이다.

## Risk Input은 하나의 Score가 아닐 수 있다

운영 Policy는 여러 입력을 함께 본다.

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

예를 들어 같은 add_comment Tool이라도:

~~~text
public issue comment
vs
student disciplinary record comment
~~~

는 Risk가 다를 수 있다.

Tool Name만으로 Risk를 결정하지 않는다.

## External Policy Evaluation

Model이 "이 Action은 안전하다"고 판단하는 것을 최종 Authorization으로 사용하지 않는다.

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

Control Profile은 다음을 결정할 수 있다.

- Allow/Deny
- Runtime Isolation
- Credential Scope
- Approval
- Verifier
- Logging

## Human Approval은 Risk-tiered하게

AWS가 공개한 Agentic AI Lens에서는 모든 Action을 Human Review에 보내는 방식이 Approval Fatigue와 Rubber-stamp Review를 만들 수 있다고 지적한다. 이는 vendor guidance이며 업계 공통 표준으로 해석하지 않는다.

Human은 다음 Action에 집중하는 편이 낫다.

- High-impact
- Irreversible
- Sensitive Data
- Ambiguous Authority
- Policy Exception

Read-only Low-risk Action까지 같은 수준의 Approval을 요구하면 Human Attention을 소모한다.

## Reviewer Context

Approval UI에는 "승인하시겠습니까?"만 보여주면 부족하다.

Reviewer가 판단할 Context가 필요하다.

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

Approval Quality는 Reviewer에게 제공되는 Evidence 품질에 영향을 받는다.

## Originating User Authorization

Agent Chain이 길어져도 User 권한을 유지해야 한다.

~~~text
User
  ↓
Agent A
  ↓
Agent B
  ↓
Tool
~~~

Agent B의 Service Credential이 User보다 넓다고 해서 넓은 Resource에 접근하게 두지 않는다.

Policy는 Originating User와 Current Agent를 함께 볼 수 있다.

## Policy as Code

Prompt 안의 자연어 Rule은 Guidance다.

Critical Boundary는 Machine-enforceable Policy가 더 적합하다.

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

Policy Engine, IAM, Gateway 등 구현 방식은 다양하다.

핵심은 Enforcement가 Model Reasoning 밖에 있다는 점이다.

## Fail Closed

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

모든 Low-risk 작업까지 무조건 Fail Closed로 할 필요는 없을 수 있다.

하지만 High-impact Boundary는 permissive fallback을 피한다.

## Just-in-time Privilege

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

AWS의 Agentic AI Lens는 Dynamic Boundary와 Temporary Credential 같은 패턴을 권고한다. 이 역시 하나의 공개 운영 지침 사례로 사용한다.

Agent의 전체 Lifetime 동안 High-risk 권한을 유지할 필요가 없다.

## Agent가 권한 확대를 제안할 수는 있다

Least Privilege를 강하게 적용하면 Agent가 필요한 Action에서 Deny를 만날 수 있다.

두 가지 극단이 있다.

1. 모든 Deny를 사람에게 넘긴다.
2. Agent가 자기 Policy를 수정한다.

두 번째는 위험하다.

더 나은 구조는 다음과 같다.

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

NVIDIA OpenShell의 Agent-driven Policy Management는 이런 방향의 사례를 보여준다.

Agent는 필요한 Capability를 설명할 수 있다.

Policy Authority는 외부에 남긴다.

## Effective Policy Manifest

Agent가 현재 무엇을 할 수 있는지 전혀 모르면 Trial-and-error Deny를 반복할 수 있다.

따라서 Harness에 Current Effective Policy를 Projection할 수 있다.

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

이 Manifest는 Planning을 돕는다.

하지만 Enforcement Source는 아니다.

~~~text
Policy Manifest
= model-facing projection

Policy Engine
= authority
~~~

Context와 State의 관계와 비슷하다.

## Independent Verification

High-risk Action은 실행 전/후에 별도 Verification을 요구할 수 있다.

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

Verifier가 Executor와 완전히 다른 Model이어야 한다는 뜻은 아니다.

가능하면 Deterministic Verification을 우선한다.

## Rollback과 Compensation

Irreversible Action은 완전히 되돌릴 수 없을 수 있다.

그래도 Compensation Plan이 필요할 수 있다.

예:

- Deploy → previous release rollback
- Payment → refund
- Message send → correction message
- DB update → compensating update

Risk Policy는 Action 이전에 Recovery Surface도 확인할 수 있다.

## 작은 예: Coding Agent의 세 Task

### Task A: 코드 읽기

~~~text
Risk:
R0/R1

Controls:
workspace sandbox
no external write
no approval
~~~

### Task B: PR 생성

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

### Task C: Production Deploy

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

같은 Agent Runtime을 무조건 재사용할 필요도 없다.

## 이 장에서 가져갈 것

Agent Security를 하나의 "승인 여부"로 축약하지 않는다.

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

그리고 Risk에 따라 이 Control의 강도를 다르게 한다.

핵심은 Agent가 Risk를 스스로 선언하는 것이 아니다.

External Policy가 Identity, Resource, Environment, Consequence를 바탕으로 Control Profile을 결정하는 것이다.

Part V에서는 Agent가 Action을 수행하기 위한 Security Boundary를 완성했다.

다음 Part에서는 이 시스템이 제대로 동작하는지 어떻게 관찰하고 측정할 것인가를 다룬다.

Trace, Eval, Regression, Harness Improvement로 넘어간다.

## 주요 근거

- AWS Agentic AI Lens: Tool Authorization
- AWS Agentic AI Lens: Human-in-the-loop for Critical Decisions
- AWS Agentic AI Lens: Dynamic Boundaries
- AWS Cedar multi-agent authorization
- NVIDIA OpenShell Security Policy
- Anthropic Claude Code Auto Mode
- research/topics/20-risk-adaptive-containment-policy.md
- research/targeted/17-risk-adaptive-policy.md

