# MCP Tasks and A2A Task Boundary

기준일: 2026-10-02

## 문제

2026년에는 MCP와 A2A 모두 Task라는 개념을 사용한다.

이름이 같지만 책임은 다르다.

## MCP 2026-07-28

MCP core는 stateless protocol로 변경됐다.

주요 변화:

- initialize / initialized handshake 제거
- protocol session 제거
- request가 self-describing
- HTTP header 기반 routing 가능
- list result caching
- authorization hardening
- extension framework

Tasks는 core가 아니라 io.modelcontextprotocol/tasks extension으로 이동했다.

## MCP Task

MCP Task는 long-running capability call을 비동기로 추적하기 위한 mechanism에 가깝다.

대표 lifecycle:

~~~text
tools/call
   ↓
server decides async work is needed
   ↓
task handle
   ↓
tasks/get
tasks/update
tasks/cancel
~~~

즉 중심은:

> capability invocation을 long-running operation으로 표현

이다.

MCP Task creation은 server-directed라는 점도 중요하다.

## A2A Task

2026-10-02 기준 최신 정식 A2A Specification은 1.0.0이다.

A2A Task는 remote Agent가 client를 위해 수행하는 stateful unit of work다.

Task에는:

- unique id
- context id
- status
- message history
- artifact collection
- metadata

가 포함될 수 있다.

상태에는:

- submitted
- working
- input-required
- auth-required
- completed
- canceled
- failed
- rejected

등이 있다.

즉 중심은:

> independent Agent System과의 work contract

다.

## Artifact 차이

A2A에서는 Artifact가 Task의 명시적 output object다.

MCP는 capability/tool result transport가 중심이고 A2A처럼 remote agent의 deliverable lifecycle 전체를 표준화하는 것이 핵심은 아니다.

## 핵심 비교

~~~text
MCP Task
scope: capability execution
owner: MCP server
purpose: long-running tool/resource style work
relationship: Agent ↔ Capability Provider

A2A Task
scope: delegated agent work
owner: remote Agent System
purpose: stateful collaboration and artifact delivery
relationship: Agent System ↔ Agent System
~~~

## Session과 Task를 혼동하지 않는다

MCP 2026-07-28은 protocol-level session을 제거했다.

그러나 application/runtime이 session을 가질 수 없는 것은 아니다.

예를 들어 AWS AgentCore는 MCP transport를 사용하면서도 별도의 runtimeSessionId/microVM lifecycle을 관리할 수 있다.

즉:

~~~text
Protocol Session
≠ Runtime Session
≠ Task
≠ Conversation
~~~

## Software Factory Task와도 다르다

software-factory-book의 Durable Task는 조직의 software work record다.

MCP/A2A Task와 1:1 동일하지 않다.

예:

~~~text
Factory Task
  ├─ local Agent Run
  ├─ MCP long-running Task
  └─ A2A delegated Task
~~~

상위 work record가 여러 protocol operation을 포함할 수 있다.

## 설계 원칙

1. 같은 Task라는 이름만 보고 domain object를 합치지 않는다.
2. Protocol Task와 Business/Factory Task를 분리한다.
3. MCP Task는 long-running capability invocation으로 본다.
4. A2A Task는 remote Agent work contract로 본다.
5. Runtime session은 protocol task와 독립적으로 관리한다.
6. protocol object를 내부 domain model에 직접 종속시키지 않는다.

## 주요 근거

- MCP 2026-07-28 Specification release
- MCP 2026-07-28 Release Candidate
- A2A Protocol Specification 1.0.0
- AWS AgentCore Runtime sessions
