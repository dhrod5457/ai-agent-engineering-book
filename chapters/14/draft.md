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

Microsoft Entra Agent ID는 Agent를 별도 identity construct로 다루는 한 구현 사례다. Entra에서는 agent identity를 특수한 service principal로 표현하지만, 이를 모든 Agent 시스템의 표준 identity model로 일반화하지 않는다.

Agent Identity에는 다음 Metadata가 연결될 수 있다.

- owner / sponsor
- purpose
- allowed capability class
- lifecycle
- environment
- risk profile

핵심은 Agent가 단순 코드 객체를 넘어 독립적인 Security Principal로 관리될 수 있다는 점이다.

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
