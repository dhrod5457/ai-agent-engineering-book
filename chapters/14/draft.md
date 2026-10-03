# 14장. Agent Identity와 Delegation

에이전트가 GitHub 이슈를 생성했다. 감사 로그에는 다음만 남아 있다.

~~~text
actor = service-account@company
~~~

그런데 질문은 더 많다. 누가 이 에이전트를 시작했는가. 어떤 애플리케이션이 에이전트를 Hosting했는가. 에이전트는 누구를 대신해 행동했는가. 어떤 Tool Identity가 실제 API를 호출했는가. 이 행동은 사용자의 권한에서 나온 것인가, Autonomous Workload 권한에서 나온 것인가. 에이전트가 업무를 수행하려면 **누가 행동하는가**를 먼저 분리해야 한다.

## Shared Service Account의 한계

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

## Identity를 나눈다

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

## Human User Identity

요청을 시작한 사용자다.

예:

- 교직원
- 개발자
- 운영자
- 고객

사용자가 에이전트에게 행동을 요청할 수 있다. 중요한 것은 에이전트가 사용자보다 넓은 권한을 자동으로 얻지 않는 것이다.

## Application Identity

에이전트를 Hosting하는 애플리케이션의 신원이다.

예:

~~~text
campus-assistant-web
coding-agent-service
operations-console
~~~

애플리케이션과 에이전트를 같은 신원으로 두면 어떤 에이전트가 어떤 권한을 썼는지 구분하기 어려울 수 있다.

## Agent Identity

특정 에이전트를 구분하는 권한을 부여받는 주체이다. Microsoft Entra Agent ID는 에이전트를 별도 identity construct로 다루는 한 구현 사례다. Entra에서는 agent identity를 특수한 service principal로 표현하지만, 이를 모든 에이전트 시스템의 표준 identity model로 일반화하지 않는다. 에이전트의 신원에는 다음 부가 정보가 연결될 수 있다.

- owner / sponsor
- purpose
- allowed capability class
- 유지 과정
- environment
- risk profile

핵심은 에이전트가 단순 코드 객체를 넘어 독립적인 Security Principal로 관리될 수 있다는 점이다.

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

한 에이전트 안에서도 도구별로 인증 정보로 행사할 수 있는 권한 범위를 분리할 수 있다.

예:

~~~text
Agent
  ├─ GitHub Read Tool
  ├─ Slack Write Tool
  └─ Production DB Read-only Tool
~~~

모든 도구가 동일한 고권한 인증 정보를 공유할 필요는 없다. Tool Identity는 다음 장의 인증 정보의 사용 경계와 연결된다.

## Resource Identity

행동의 대상도 신원이나 Resource Identifier를 가진다.

예:

- Repository A
- Slack Channel B
- Student Record C
- Production Cluster D

권한 확인(Authorization)은 "에이전트가 도구를 호출할 수 있는가"만 보는 것이 아니라 어떤 접근 대상 자원에 적용되는지도 봐야 한다.

## Delegated Access

사용자를 대신해 에이전트가 행동하는 경우다.

~~~text
User
  ↓ consent / scope
Agent
  ↓ delegated token
Resource
~~~

예를 들어 교직원이 자신의 권한 안에서 학생 정보를 조회하도록 에이전트에게 요청할 수 있다. 이때 에이전트는 사용자보다 더 넓은 학생 범위를 볼 수 없어야 한다. Delegated Mode에서는 User Context가 Authorization Input으로 남아야 한다.

## Autonomous Access

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

이 정보가 있으면 감사에서 "누가 무엇을 왜 읽었는가"를 더 정확히 복구할 수 있다.

## Discovery는 Authorization이 아니다

에이전트가 어떤 기능이 존재한다는 것을 알게 됐다고 하자. MCP Tool Catalog나 A2A Agent Card를 통해 기능을 발견할 수 있다.

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
이 권한을 부여받는 주체가 해당 Action/Resource를 사용할 수 있는가.

### Approval
권한이 있어도 이번 행동을 지금 실행해도 되는가.

이 네 단계를 섞으면 Capability Catalog가 Permission List처럼 사용될 수 있다.

## Originating User Context

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

## Agent Lifecycle

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

## Identity와 Memory

메모리에도 Actor가 있다.

메모리가 만들어질 때:

- 어떤 사용자가 Origin이었는가.
- 어떤 에이전트가 요약했는가.
- 어느 작업에서 생성됐는가.

를 남길 수 있다. 잘못된 메모리가 발견됐을 때 정보 원본을 추적하는 데 도움이 된다.

## Identity와 Audit

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

권한 확인은 다음을 볼 수 있다.

- staff-A가 student-B를 조회할 업무 권한이 있는가.
- 에이전트가 student record capability를 사용할 수 있는가.
- 도구는 read-only인가.
- Sensitive Field는 Masking이 필요한가.

에이전트라는 이유로 User Authorization을 건너뛰지 않는다.

## Identity를 Agent Prompt에 넣는 것과 Enforcement는 다르다

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

## 이 장에서 가져갈 것

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

## 주요 근거

- Microsoft Entra Agent ID
- Microsoft Identity Fundamentals for AI Agents
- Microsoft Agent On-Behalf-Of Flow
- AWS AgentCore Identity
- A2A Authorization model
- research/topics/10-agent-identity-authorization.md
- research/topics/19-delegated-agent-identity-zero-trust.md
