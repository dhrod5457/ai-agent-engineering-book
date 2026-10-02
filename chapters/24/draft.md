# 24장. A2A와 Remote Agent

한 Application 안에서 Subagent를 호출하는 것은 비교적 단순하다.

같은 Runtime, 같은 State Store, 같은 Authentication Context를 공유할 수 있다.

다른 조직이나 다른 Service가 운영하는 Agent를 호출하면 이야기가 달라진다.

상대 Agent의 내부 Tool과 Memory를 직접 알 수 없고, Network Boundary가 있으며, Authentication과 Task Lifecycle이 필요하다.

A2A는 이런 독립 Agent System 사이의 상호운용 문제를 다룬다.

## Remote Agent는 Tool과 다르다

Tool은 bounded capability를 제공한다.

Remote Agent는 자체적으로 다음을 가질 수 있다.

- Model
- Harness
- Tools
- State
- Policy
- Long-running Task

따라서:

~~~text
Tool Call
≠ Remote Agent Delegation
~~~

Remote Agent는 단순 함수 호출보다 더 긴 Lifecycle을 가질 수 있다.

## A2A의 위치

이 책에서는 다음처럼 구분한다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

MCP가 Tool/Resource Integration을 다룬다면 A2A는 Agent 단위 Work Collaboration을 다룬다.

## Agent Card

Remote Agent가 어떤 Capability를 제공하는지 Discover할 수 있다.

예:

~~~text
Compliance Review Agent
- policy review
- evidence analysis
- compliance report
~~~

하지만 Agent Card는 Authorization이 아니다.

Capability가 존재한다고 누구나 호출할 수 있는 것은 아니다.

## Message

Agent 사이 Interaction은 Message로 표현될 수 있다.

Message는 단순 String보다 구조화된 Content를 가질 수 있다.

중요한 것은 Protocol Message와 내부 Conversation State를 동일시하지 않는 것이다.

## A2A Task

Remote Agent에 위임한 Work는 Task Lifecycle을 가질 수 있다.

예:

~~~text
submitted
working
input-required
auth-required
completed
failed
canceled
~~~

이 Task는 MCP Task와 다르다.

~~~text
MCP Task
= long-running capability invocation

A2A Task
= remote Agent work contract
~~~

또 Software Factory Task와도 다르다.

~~~text
Factory Task
  ↓
Agent Run
  ├─ MCP Task
  └─ A2A Task
~~~

상위 Work Item이 여러 Protocol Task를 포함할 수 있다.

## Artifact

A2A에서는 Remote Agent가 결과를 Artifact로 전달할 수 있다.

예:

- report
- generated file
- analysis result
- structured data

Artifact는 Message와 다르다.

Message는 Interaction이고 Artifact는 Deliverable에 가깝다.

## Input Required

Remote Agent가 추가 정보가 필요할 수 있다.

~~~text
working
  ↓
input-required
  ↓
client provides info
  ↓
working
~~~

Long-running Agent의 Pause/Resume와 유사하다.

Protocol Lifecycle이 내부 State Plane과 연결될 수 있다.

## Auth Required

Remote Agent가 추가 Authorization을 요구할 수도 있다.

이 경우 Caller Identity와 Originating User Context를 어떻게 전달할지 중요해진다.

~~~text
User
→ Local Agent
→ Remote Agent
→ Remote Tool
~~~

Remote Agent가 자신의 broad Service Credential만 사용해 User Scope를 초과하지 않도록 한다.

## Capability Discovery와 Authorization

다시 같은 원칙이 나온다.

~~~text
Agent Card
= what is available

Authorization
= can this caller use it
~~~

Remote Agent Server가 최종 Access Policy를 강제해야 한다.

## Async Work

Remote Agent는 즉시 결과를 반환하지 않을 수 있다.

Long-running Task라면:

- status query
- streaming
- notification
- artifact update

가 필요하다.

이때 Local Agent는 Remote Task State를 자신의 Internal Goal State와 연결할 수 있다.

~~~text
Local Goal G-100
  ↓ delegates
A2A Task T-55
  ↓ completed
Artifact A-7
  ↓
Local Goal resumes
~~~

두 Task ID를 같은 것으로 만들지 않는다.

## Remote Failure

Remote Agent가 실패하면 Local Agent가 판단해야 한다.

예:

~~~text
A2A Task failed
  ├─ retry
  ├─ alternative agent
  ├─ continue locally
  └─ escalate
~~~

Protocol Error와 Domain Failure를 구분하는 것이 중요하다.

## Trust

Remote Agent가 반환한 Artifact를 자동으로 Trusted Result로 보지 않는다.

필요하면 Local Verification을 한다.

~~~text
Remote Agent
→ Artifact
→ Local Verifier
→ Accept
~~~

특히 다른 Organization이나 Trust Domain의 Agent라면 중요하다.

## A2A와 Internal Domain

Protocol Object를 내부 Domain Model에 직접 종속시키지 않는 원칙은 MCP와 같다.

~~~text
Internal Delegation Model
        ↓
A2A Adapter
        ↓
Remote Agent
~~~

Protocol Version이 바뀌어도 내부 Goal과 Artifact Model을 유지하기 쉽다.

## 작은 예: 대학 규정 검토 Agent

Campus Agent가 외부 Legal Review Agent에 규정 변경 검토를 요청한다.

~~~text
Campus Agent
  ↓
A2A Task:
review regulation change

Remote Legal Agent
  ↓
Artifact:
risk report
~~~

Campus Agent는 결과를 그대로 적용하지 않는다.

~~~text
Artifact
→ local policy check
→ human review
→ accept
~~~

Remote Agent는 Specialist이지만 최종 Authority는 아닐 수 있다.

## 이 장에서 가져갈 것

Remote Agent를 Tool처럼 단순화하면 Lifecycle과 Authority를 놓칠 수 있다.

다음 경계를 유지한다.

~~~text
MCP Task
≠ A2A Task
≠ Factory Task

Remote Agent
≠ Local Subagent
~~~

A2A는 independent Agent System 간 Collaboration Boundary다.

이제 책의 마지막 장에서 지금까지의 내용을 도입 순서로 압축한다.

처음부터 Memory, Multi-Agent, MicroVM을 모두 넣지 않고 Minimum Viable Production Agent에서 어떻게 시작할 것인가.

## 주요 근거

- A2A Protocol Specification
- MCP 2026-07-28
- research/topics/12-mcp-a2a-task-boundary.md
- research/topics/07-multi-agent-interoperability.md
