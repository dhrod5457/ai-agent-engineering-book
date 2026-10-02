# 6장. MCP와 Capability Boundary

Agent마다 GitHub Client, Database Client, Browser Adapter, Internal API Wrapper를 따로 구현하기 시작하면 빠르게 중복이 생긴다.

다른 Agent가 같은 Capability를 쓰려면 다시 연결해야 한다.

Tool의 이름과 Schema도 각 Application 안에 갇힌다.

MCP는 이런 통합 문제를 줄이기 위해 등장한 Protocol 중 하나다.

하지만 MCP를 사용한다고 Agent Architecture 전체가 해결되는 것은 아니다.

MCP는 **Agent와 Capability Provider 사이의 Integration Boundary**다.

## MCP가 해결하려는 문제

Agent가 외부 Capability를 사용하려면 몇 가지 공통 문제가 반복된다.

- Capability Discovery
- Tool Schema
- Resource Access
- Prompt/Template 제공
- Transport
- Authorization 연결
- Long-running Operation 표현

각 Agent Application이 이를 제각각 구현하면 Connector가 늘어난다.

MCP는 공통 Protocol을 제공한다.

개념적으로는 다음 구조다.

~~~text
Agent Harness
    ↓
MCP Client
    ↓
MCP Server
    ↓
Tool / Resource / Prompt / Extension
    ↓
External Capability
~~~

이 구조에서 중요한 점은 MCP Server가 Agent가 아니라는 것이다.

Capability Provider다.

## MCP는 Agent Loop를 대신하지 않는다

MCP를 붙여도 Harness는 여전히 다음을 결정해야 한다.

- 어떤 Capability를 현재 Agent에게 보여줄 것인가.
- 어떤 Tool Call을 허용할 것인가.
- 결과를 Context에 얼마나 넣을 것인가.
- 실패하면 Retry할 것인가.
- Side Effect에 Approval이 필요한가.
- Long-running 결과를 어떤 State와 연결할 것인가.
- Completion을 어떻게 검증할 것인가.

MCP는 Tool Transport와 Discovery를 표준화할 수 있다.

Agent의 Goal과 Loop를 자동으로 설계하지는 않는다.

~~~text
MCP
≠ Agent Harness
~~~

이 구분이 중요하다.

## Tool과 Resource

MCP에서는 Capability를 여러 형태로 표현할 수 있다.

이 책에서는 세부 API보다 책임을 본다.

### Tool

Agent가 Action을 요청하는 Interface다.

예:

~~~text
create_issue
run_query
send_message
~~~

### Resource

Agent가 읽을 수 있는 정보 Source를 표현할 수 있다.

예:

~~~text
repository://docs/architecture
database://schema
internal://policy
~~~

### Prompt

재사용 가능한 Prompt Template 또는 Context 관련 기능을 제공할 수 있다.

중요한 것은 이 세 가지가 Agent 내부 State와 같지 않다는 점이다.

Resource를 읽었다고 Agent Memory가 되는 것은 아니다.

Prompt를 제공한다고 Agent Instruction Architecture가 자동으로 해결되는 것도 아니다.

Protocol Object와 Domain Object를 분리한다.

## 2026-07-28의 Stateless Core

2026년 7월 MCP Specification 변화에서 중요한 방향 중 하나는 Protocol Core를 Stateless하게 단순화한 것이다.

Protocol-level Session에 의존하는 대신 각 Request가 더 self-describing한 구조로 이동했다.

이 변화가 주는 설계상 교훈은 명확하다.

~~~text
Protocol Session
≠ Application Session
≠ Runtime Session
≠ Agent Goal
~~~

MCP Core가 Stateless하다고 해서 Agent Application이 상태를 가지면 안 된다는 뜻이 아니다.

오히려 Agent State를 Protocol Connection에 묶지 않는 편이 더 명확하다.

예를 들어:

~~~text
Agent Goal G-102
      ↓
MCP Tool Call
      ↓
Runtime Session R-77
      ↓
MCP Response
~~~

G-102와 R-77은 서로 다른 Lifecycle을 가질 수 있다.

## Long-running Capability와 MCP Task

짧은 Tool은 Request/Response로 충분하다.

하지만 다음 같은 작업은 오래 걸릴 수 있다.

- 대용량 분석
- 장시간 Build
- External Job
- Batch Processing

MCP의 Task 확장은 이런 Long-running Capability Invocation을 표현하는 데 사용될 수 있다.

개념적으로:

~~~text
tools/call
   ↓
Server decides asynchronous execution
   ↓
Task Handle
   ↓
tasks/get
tasks/update
tasks/cancel
~~~

여기서 주의할 점이 있다.

MCP Task는 Product Domain의 Task와 같지 않다.

이 책에서는 구분을 위해 다음처럼 본다.

~~~text
MCP Task
= Long-running Capability Invocation
~~~

예를 들어 "고객 환불 처리"라는 Product Task 하나가 여러 MCP Tool Call과 MCP Task를 포함할 수 있다.

## 같은 Task라는 이름의 함정

Agent 시스템에는 Task라는 이름이 너무 많이 등장한다.

- Agent Task
- MCP Task
- A2A Task
- Workflow Task
- Factory Task

이들을 하나의 내부 Entity로 합치면 Lifecycle이 꼬일 수 있다.

예를 들어 Software Factory의 Task는 다음 정보를 가질 수 있다.

~~~text
Requirement
Owner
Acceptance
Worker Assignment
Delivery
~~~

MCP Task는 이런 조직 Work Item 전체를 의미하지 않는다.

따라서 내부 Domain Model에서 Protocol Object를 Adapter로 감싸는 편이 안전하다.

~~~text
Internal Work / Goal
      ↓
Protocol Adapter
      ↓
MCP Task
~~~

## Capability Discovery와 Authorization은 다르다

MCP Server가 Tool을 제공한다고 해서 현재 Agent가 그 Tool을 실행할 권한까지 얻는 것은 아니다.

~~~text
Discovery
= 어떤 Capability가 존재하는가

Authorization
= 현재 Principal이 그 Action을 실행할 수 있는가
~~~

Protocol 수준의 인증과 별개로 Application은 현재 Goal과 User/Agent Scope에 더 좁은 Policy를 적용할 수 있다. Identity, Delegation, Approval의 구체적인 설계는 Part V에서 다룬다.

## Protocol Authorization과 Application Policy

Protocol 수준의 Authentication/Authorization이 있어도 Application Policy는 남는다.

예를 들어 Agent가 GitHub MCP Server에 정상적으로 인증됐다고 하자.

그 Credential이 다음을 허용할 수 있다.

- Read Repository
- Create Issue
- Merge PR

하지만 현재 Agent Goal은 Documentation 조회뿐일 수 있다.

그렇다면 Application은 더 좁은 Policy를 적용할 수 있다.

~~~text
Protocol Credential Scope
        ↓
Application Policy
        ↓
Current Effective Capability
~~~

Least Privilege는 여러 Layer에서 적용될 수 있다.

## MCP Result도 Context Boundary를 통과한다

MCP Server가 반환한 Tool Result는 Model에게 전달될 수 있다.

하지만 결과는 그대로 Context에 넣지 않을 수 있다.

예:

~~~text
MCP Result
   ↓
Normalize
   ↓
Trust / Provenance Label
   ↓
Size Limit / Redaction
   ↓
Context Projection
   ↓
Model
~~~

특히 외부 Web, Email, Document를 읽는 MCP Tool은 Prompt Injection Source가 될 수 있다.

Server 자체를 신뢰한다고 반환 Content까지 모두 trusted instruction으로 취급하지 않는다.

## Cache와 Capability List

Stateless Protocol에서는 Capability List 같은 정보가 매 요청마다 바뀌지 않는 경우 Cache가 중요해질 수 있다.

하지만 Cache에도 Version 문제가 있다.

~~~text
Cached Tool List
        ↓
Server Capability Changed
        ↓
Stale Client View
~~~

따라서 Cache는 Authority가 아니라 Optimization이다.

중요한 Operation 직전에는 실제 Authorization/Validation을 다시 한다.

이 원칙은 뒤의 External State Reconciliation과 닮아 있다.

## MCP가 Agent Architecture를 단순화하는 지점

MCP는 Agent와 External Capability의 결합도를 줄이는 데 사용할 수 있다.

~~~text
Before

Agent A → GitHub Adapter A
Agent B → GitHub Adapter B
Agent C → GitHub Adapter C

After

Agent A ─┐
Agent B ─┼→ MCP Client → GitHub MCP Server
Agent C ─┘
~~~

이런 구조는 Capability Integration을 재사용하기 쉽게 만든다.

하지만 shared integration이 shared authority를 의미하지는 않는다.

각 Agent와 User의 Authorization Context는 별도로 유지해야 한다.

## MCP Server는 Enforcement Point가 될 수 있다

MCP Server는 Agent와 External System 사이에서 중요한 Enforcement Point가 될 수 있다. 다만 모든 Policy가 반드시 MCP Server 하나에 모여야 한다는 뜻은 아니다.

가능한 책임:

- Schema Validation
- Credential Handling
- Endpoint Restriction
- Result Normalization
- Audit
- Rate Limit

하지만 모든 Policy를 Server 한 곳에 넣을 필요도 없다.

예를 들어:

~~~text
Agent Harness
- task context

Application Policy Gateway
- user/agent authorization

MCP Server
- capability contract

External System
- resource-level authorization
~~~

처럼 여러 Layer가 존재할 수 있다.

중요한 것은 각 Layer가 무엇을 강제하는지 분명히 하는 것이다.

## MCP와 A2A는 다른 문제를 푼다

MCP를 Agent 간 통신 Protocol로 생각하기 쉽다.

하지만 A2A는 다른 경계를 다룬다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

예를 들어:

~~~text
Coding Agent
  ↓ MCP
GitHub Capability

Coding Agent
  ↓ A2A
Remote Security Review Agent
~~~

첫 번째는 Tool/Capability를 호출한다.

두 번째는 다른 Agent System에 Work를 위임한다.

A2A는 Part VII에서 자세히 다룬다.

## 작은 예: 대학 행정 Agent

대학 행정 Agent가 다음 Capability를 사용한다고 하자.

- 학사 규정 검색
- 학생 정보 조회
- 담당자에게 메시지 전송

MCP를 이용해 세 Capability를 제공할 수 있다.

~~~text
Campus Agent
   ↓
MCP Client
   ├─ Regulation Search Server
   ├─ Student Read Server
   └─ Messaging Server
~~~

하지만 다음 정책은 MCP 연결 자체가 결정하지 않는다.

- 어떤 교직원이 어떤 학생 정보를 볼 수 있는가.
- Agent가 학생에게 직접 메시지를 보낼 수 있는가.
- 메시지 전송 전 승인이 필요한가.
- 조회 결과를 Memory에 저장해도 되는가.

이것들은 Identity, Policy, Memory Boundary의 문제다.

Protocol을 도입했다고 Governance가 사라지지 않는다.

## Protocol을 내부 Architecture의 중심으로 두지 않는다

Protocol은 바뀔 수 있다.

Version도 바뀌고 Extension도 추가된다.

책 전체 Architecture가 Protocol Object에 직접 종속되면 변화에 취약해진다.

따라서 내부에서는 다음 책임을 먼저 정의한다.

~~~text
Capability
Authorization
Execution
State
Artifact
Goal
~~~

그리고 MCP는 Adapter로 연결한다.

~~~text
Internal Capability Model
        ↓
MCP Adapter
        ↓
MCP Server
~~~

이 접근은 다른 Protocol이 추가돼도 내부 Model을 유지하기 쉽다.

## Part II에서 가져갈 것

Part II에서는 Agent의 양쪽 Interface를 살펴봤다.

~~~text
External World
      ↓
Context Engine
      ↓
Model
      ↓
Tool Interface
      ↓
External World
~~~

Context Engine은 외부 세계에서 현재 판단에 필요한 정보를 Model에게 Projection한다.

Tool Interface는 Model이 제안한 Action을 검증 가능한 Capability로 바꾼다.

MCP는 Tool/Resource 같은 Capability를 외부 Provider와 연결하는 Protocol Boundary다.

하지만 아직 중요한 문제가 남는다.

Agent가 여러 Turn과 여러 Runtime에 걸쳐 작업한다면 현재 Goal과 Progress, 이미 실행한 Action을 어디에 보존해야 할까.

Conversation Context만으로는 부족하다.

Part III에서는 Session, Workspace, Goal, Memory를 먼저 분리하고, 이 책의 중심 개념인 Agent State Plane으로 들어간다.

## 주요 근거

- Model Context Protocol 2026-07-28
- MCP Specification / Tasks Extension
- research/topics/03-tools-protocols.md
- research/topics/12-mcp-a2a-task-boundary.md
