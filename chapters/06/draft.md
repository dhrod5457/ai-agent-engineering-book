# 6장. MCP와 Capability Boundary

Agent마다 GitHub Client, Database Client, Browser Adapter, Internal API Wrapper를 따로 만들기 시작하면 빠르게 중복이 생긴다.

다른 Agent가 같은 기능을 쓰려면 다시 연결해야 하고, Tool 이름과 Schema도 각 Application 안에 갇힌다.

MCP는 이런 문제를 줄이기 위한 Protocol이다.

이 장에서 기억할 핵심은 하나다.

> **MCP는 Agent Architecture 전체가 아니라, Agent와 외부 Capability 사이의 표준화된 경계다.**

## 왜 MCP가 필요한가

여러 Agent가 GitHub를 사용한다고 하자.

MCP가 없다면 각 Agent가 GitHub 연결을 따로 구현할 수 있다.

~~~text
Agent A → GitHub Adapter A
Agent B → GitHub Adapter B
Agent C → GitHub Adapter C
~~~

같은 인증 방식, 같은 API, 비슷한 Schema를 여러 번 구현하게 된다.

MCP를 사용하면 공통 Capability Provider를 둘 수 있다.

~~~text
Agent A ─┐
Agent B ─┼→ MCP Client → GitHub MCP Server → GitHub
Agent C ─┘
~~~

Agent는 GitHub API 자체보다 MCP가 제공하는 Capability Contract를 사용한다.

이렇게 하면 Capability Integration을 여러 Agent에서 재사용하기 쉬워진다.

## MCP가 해주는 것

Agent가 외부 기능을 사용하려면 반복해서 필요한 것이 있다.

- 어떤 Capability가 있는지 찾기
- Tool의 입력과 출력 Schema 알기
- Tool 호출하기
- Resource 읽기
- 재사용 가능한 Prompt 제공받기
- 결과 받기
- 필요한 경우 오래 걸리는 호출의 상태 추적하기

MCP는 이런 통합 방식을 공통 Protocol로 만든다.

개념적으로는 다음과 같다.

~~~text
Agent Harness
    ↓
MCP Client
    ↓
MCP Server
    ↓
Tool / Resource / Prompt
    ↓
External Capability
~~~

여기서 MCP Server는 Agent가 아니다.

외부 기능을 Agent가 사용할 수 있는 형태로 제공하는 **Capability Provider**다.

## MCP가 해주지 않는 것

MCP를 연결했다고 Agent의 실행 구조가 완성되는 것은 아니다.

Harness는 여전히 다음을 결정해야 한다.

- 현재 Agent에게 어떤 Capability를 보여줄 것인가.
- 어떤 Tool Call을 허용할 것인가.
- 실패하면 다시 시도할 것인가.
- Side Effect가 있는 Action에 승인이 필요한가.
- Tool Result를 Context에 얼마나 넣을 것인가.
- 현재 Goal과 Progress를 어디에 저장할 것인가.
- 작업 완료를 어떻게 검증할 것인가.

MCP는 Capability를 연결한다.

Agent의 Goal, Loop, State, Approval, Completion Policy까지 대신 설계하지는 않는다.

~~~text
MCP
≠ Agent Harness
~~~

이 구분이 이 장에서 가장 중요하다.

## Tool, Resource, Prompt

MCP는 Capability를 여러 형태로 표현할 수 있다.

세부 API보다 각각의 책임을 이해하는 편이 중요하다.

### Tool

Agent가 외부에 Action을 요청하는 Interface다.

예:

~~~text
create_issue
run_query
send_message
~~~

### Resource

Agent가 읽을 수 있는 정보 Source다.

예:

~~~text
repository://docs/architecture
database://schema
internal://policy
~~~

### Prompt

재사용 가능한 Prompt Template이나 Context 구성 요소를 제공할 수 있다.

하지만 이 객체들을 Agent 내부 State와 같은 것으로 보면 안 된다.

Resource를 읽었다고 자동으로 Memory가 되는 것은 아니다.

Prompt가 제공된다고 Agent의 Instruction Architecture가 자동으로 해결되는 것도 아니다.

MCP는 Protocol Object를 제공하고, Agent Application은 자신의 Domain Model을 별도로 가진다.

## 상태를 MCP 연결에 맡기지 않는다

MCP의 Protocol 상태와 Agent의 작업 상태는 같은 것이 아니다.

예를 들어 Agent가 하나의 작업을 수행하는 동안 MCP 연결이 끊겼다가 다시 만들어질 수 있다.

그렇다고 Agent의 Goal까지 새로 만들어져야 하는 것은 아니다.

~~~text
Agent Goal
   ↓
MCP Tool Call
   ↓
External Capability
~~~

Agent의 Goal과 Progress는 Application이 관리하고, MCP는 Capability 호출을 위한 경계로 두는 편이 명확하다.

최근 MCP Core가 Protocol-level Session 의존도를 줄이는 방향으로 단순화된 것도 같은 설계 원칙과 잘 맞는다.

Protocol Connection의 Lifecycle과 Agent Work의 Lifecycle을 결합하지 않는다.

## MCP Task는 업무 Task가 아니다

짧은 Tool 호출은 일반적인 Request/Response로 처리할 수 있다.

하지만 Build, 대용량 분석, Batch Job처럼 오래 걸리는 작업도 있다.

MCP의 Task는 이런 Long-running Capability Invocation을 추적하는 데 사용할 수 있다.

~~~text
Tool Call
   ↓
MCP Task
   ↓
Status / Result / Cancel
~~~

여기서 MCP Task를 제품이나 조직의 업무 Task와 같은 Entity로 만들지 않는 것이 중요하다.

예를 들어 Software Factory에서 다음 업무가 있다고 하자.

~~~text
"로그인 장애 수정"
~~~

이 업무 하나를 처리하면서 다음과 같은 여러 외부 호출이 발생할 수 있다.

~~~text
로그인 장애 수정
   ├─ Repository 분석
   ├─ Build 실행 → MCP Task
   └─ Security Scan → MCP Task
~~~

위의 "로그인 장애 수정"은 내부 Work Item이다.

MCP Task는 그 Work를 수행하는 과정에서 생긴 Long-running Capability Invocation이다.

Lifecycle이 다르므로 내부 Domain Model에서는 분리하는 편이 안전하다.

## Tool이 보인다고 실행해도 되는 것은 아니다

Capability Discovery와 Authorization은 다른 문제다.

MCP Server가 어떤 Tool을 제공하고, 현재 Credential이 그 Tool을 호출할 수 있다고 하자.

그래도 현재 Agent에게 그 Action을 허용하지 않을 수 있다.

예를 들어 GitHub Credential이 다음 권한을 가진다고 하자.

- Repository 읽기
- Issue 생성
- PR Merge

현재 Agent의 역할이 문서 조사라면 Application은 Repository 읽기만 허용할 수 있다.

~~~text
Available Capability
        ↓
Credential Scope
        ↓
Application Policy
        ↓
Effective Capability
~~~

즉, shared integration이 shared authority를 의미하지 않는다.

MCP Server는 Schema Validation, Credential Handling, Endpoint Restriction, Audit 같은 Enforcement Point가 될 수 있다.

하지만 모든 Policy를 MCP Server 하나에 넣을 필요는 없다.

Agent Harness, Application Policy, MCP Server, External System이 각자 다른 수준의 제약을 강제할 수 있다.

중요한 것은 어느 Layer가 무엇을 허용하고 막는지 분명히 하는 것이다.

Identity, Delegation, Approval은 Part V에서 다시 다룬다.

## MCP Result도 그대로 신뢰하지 않는다

MCP Tool Result는 Model의 Context로 들어갈 수 있다.

하지만 외부에서 왔다는 사실은 변하지 않는다.

특히 Web, Email, Document를 읽은 결과에는 잘못된 정보나 Prompt Injection이 포함될 수 있다.

따라서 Tool Result를 그대로 trusted instruction으로 취급하지 않는다.

~~~text
MCP Result
   ↓
Normalize
   ↓
Trust / Provenance
   ↓
Redaction / Size Limit
   ↓
Context Projection
   ↓
Model
~~~

MCP Server를 신뢰하는 것과 MCP Server가 읽어 온 외부 Content를 신뢰하는 것은 다른 문제다.

이 원칙은 앞에서 다룬 Context Boundary와 이어진다.

## MCP와 A2A는 다른 문제를 푼다

MCP를 Agent 간 통신 Protocol로 생각하기 쉽다.

하지만 MCP와 A2A는 경계가 다르다.

~~~text
MCP
Agent → Capability

A2A
Agent → Agent
~~~

예를 들어 Coding Agent가 GitHub에 Issue를 만들거나 Repository를 읽는 것은 Capability 호출이다.

~~~text
Coding Agent
   ↓ MCP
GitHub
~~~

반면 별도의 Security Review Agent에게 코드 검토를 맡기는 것은 독립된 Agent System에 Work를 위임하는 문제다.

~~~text
Coding Agent
   ↓ A2A
Security Review Agent
~~~

MCP는 Tool과 Resource를 연결하는 데 초점이 있고, A2A는 독립적인 Agent System 사이의 위임과 협업을 다룬다.

A2A는 Part VII에서 자세히 다룬다.

## 작은 예: 대학 행정 Agent

대학 행정 Agent가 다음 기능을 사용한다고 하자.

- 학사 규정 검색
- 학생 정보 조회
- 담당자에게 메시지 전송

각 기능을 MCP Server로 제공할 수 있다.

~~~text
Campus Agent
   ↓
MCP Client
   ├─ Regulation Search Server
   ├─ Student Read Server
   └─ Messaging Server
~~~

이 구조는 세 Capability를 Agent에 연결하는 문제를 해결한다.

하지만 다음 질문은 여전히 Application이 결정해야 한다.

- 어떤 교직원이 어떤 학생 정보를 볼 수 있는가.
- Agent가 학생에게 직접 메시지를 보낼 수 있는가.
- 메시지 전송 전에 승인이 필요한가.
- 조회 결과를 Memory에 저장해도 되는가.

Protocol을 도입했다고 Governance 문제가 사라지는 것은 아니다.

MCP는 연결을 표준화한다.

권한과 정책까지 대신 결정하지는 않는다.

## Protocol을 Architecture의 중심에 두지 않는다

Protocol은 바뀔 수 있다.

Version이 바뀌고 새로운 Extension이 추가될 수도 있다.

내부 Architecture가 MCP의 Protocol Object에 직접 종속되면 이런 변화가 Domain Model까지 퍼질 수 있다.

따라서 내부에서는 먼저 자신의 책임을 정의한다.

~~~text
Capability
Authorization
Execution
State
Artifact
Goal
~~~

그리고 MCP를 Adapter로 연결한다.

~~~text
Internal Capability Model
        ↓
MCP Adapter
        ↓
MCP Server
~~~

이렇게 하면 MCP가 발전하거나 다른 Protocol이 추가되어도 내부 Model을 유지하기 쉽다.

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

MCP는 이런 Capability를 외부 Provider와 연결하는 Protocol Boundary다.

여기까지 이해하면 MCP의 위치는 단순하다.

> **MCP는 Agent 자체가 아니라 Agent가 외부 기능을 사용하는 표준 연결 방식이다.**

하지만 Agent가 여러 Turn과 여러 Runtime에 걸쳐 작업한다면 다른 문제가 생긴다.

현재 Goal과 Progress, 이미 실행한 Action을 어디에 보존해야 할까.

Conversation Context만으로는 부족하다.

Part III에서는 Session, Workspace, Goal, Memory를 분리하고 이 책의 중심 개념인 Agent State Plane으로 들어간다.

## 주요 근거

- Model Context Protocol 2026-07-28
- MCP Specification / Tasks Extension
- research/topics/03-tools-protocols.md
- research/topics/12-mcp-a2a-task-boundary.md
