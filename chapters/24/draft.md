# 24장. A2A와 Remote Agent

한 애플리케이션 안에서 하위 에이전트를 호출하는 것은 비교적 단순하다. 같은 실행 환경, 같은 상태 저장소, 같은 인증 정보를 공유할 수 있다. 다른 조직이나 다른 서비스가 운영하는 에이전트를 호출하면 이야기가 달라진다. 상대 에이전트의 내부 도구와 메모리를 직접 알 수 없고, 네트워크 접근 경계가 있으며, 인증(Authentication)과 작업의 시작부터 종료까지의 과정이 필요하다. A2A는 이처럼 독립된 에이전트 시스템들이 서로를 찾고 메시지를 교환하며, 작업의 시작부터 종료까지를 관리하고 산출물을 전달하는 등 함께 동작하는 데 필요한 문제를 다룬다.

2026-10-02 기준 A2A의 최신 정식 명세는 1.0.0이다. 이 장에서는 버전별 JSON 표현보다 1.0에서도 유지되는 Agent Card, 메시지, 작업, 산출물, 권한 확인(Authorization)의 책임 경계에 집중한다.

## Remote Agent는 Tool과 다르다

도구는 bounded capability를 제공한다. 원격 에이전트는 자체적으로 다음을 가질 수 있다.

- 모델
- 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)
- Tools
- 상태
- 정책
- 장시간 작업

따라서:

~~~text
Tool Call
≠ Remote Agent Delegation
~~~

원격 에이전트는 단순 함수 호출보다 더 긴 유지 과정을 가질 수 있다.

## A2A의 위치

이 책에서는 다음처럼 구분한다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

MCP가 Tool/Resource Integration을 다룬다면 A2A는 에이전트 단위 Work Collaboration을 다룬다.

## Agent Card

원격 에이전트가 어떤 기능을 제공하는지 Discover할 수 있다.

예:

~~~text
Compliance Review Agent
- policy review
- evidence analysis
- compliance report
~~~

하지만 Agent Card는 권한 확인이 아니다. 기능이 존재한다고 누구나 호출할 수 있는 것은 아니다.

## Message

에이전트 사이 Interaction은 메시지로 표현될 수 있다. 메시지는 단순 String보다 구조화된 내용을 가질 수 있다. 중요한 것은 Protocol Message와 내부 Conversation State를 동일시하지 않는 것이다.

## A2A Task

원격 에이전트에 위임한 업무는 작업의 시작부터 종료까지의 과정을 가질 수 있다. 2026-10-02 기준 A2A 0.3.0에는 다음 Task state가 정의돼 있다. 정확한 state 목록은 protocol version에 따라 달라질 수 있으므로 출간 전 다시 확인한다.

~~~text
submitted
working
input-required
completed
canceled
failed
rejected
auth-required
unknown
~~~

이 작업은 MCP Task와 다르다.

~~~text
MCP Task
= Long-running Capability Invocation

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

상위 작업 항목이 여러 Protocol Task를 포함할 수 있다.

## Artifact

A2A에서는 원격 에이전트가 결과를 산출물로 전달할 수 있다.

예:

- report
- generated file
- analysis result
- structured data

산출물은 메시지와 다르다. 메시지가 서로 주고받는 대화나 상호작용을 나타낸다면, 산출물은 전달할 결과물에 가깝다.

## Input Required

원격 에이전트가 추가 정보가 필요할 수 있다.

~~~text
working
  ↓
input-required
  ↓
client provides info
  ↓
working
~~~

오래 실행되는 에이전트의 Pause/Resume와 유사하다. Protocol Lifecycle이 내부 상태 관리 계층과 연결될 수 있다.

## Auth Required

원격 에이전트가 추가 권한 확인을 요구할 수도 있다. 이 경우 Caller Identity와 Originating User Context를 어떻게 전달할지 중요해진다.

~~~text
User
→ Local Agent
→ Remote Agent
→ Remote Tool
~~~

원격 에이전트가 자신의 broad Service Credential만 사용해 사용자의 권한 범위를 초과하지 않도록 한다.

## Capability Discovery와 Authorization

다시 같은 원칙이 나온다.

~~~text
Agent Card
= what is available

Authorization
= can this caller use it
~~~

Remote Agent Server가 최종 Access Policy를 강제해야 한다. A2A 1.0의 AUTH_REQUIRED 상태 자체도 특정 행동을 승인했다는 뜻은 아니며, 실제 Authorization Scope와 인증 정보(Credential) 의미는 구현이나 Credential Issuer가 별도로 정의해야 한다.

## Async Work

원격 에이전트는 즉시 결과를 반환하지 않을 수 있다.

장시간 작업라면:

- status query
- streaming
- notification
- artifact update

가 필요하다. 이때 Local Agent는 Remote Task State를 자신의 Internal Goal State와 연결할 수 있다.

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

원격 에이전트가 실패하면 Local Agent가 판단해야 한다.

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

원격 에이전트가 반환한 산출물을 자동으로 Trusted Result로 보지 않는다. 필요하면 Local Verification을 한다.

~~~text
Remote Agent
→ Artifact
→ Local Verifier
→ Accept
~~~

특히 다른 Organization이나 Trust Domain의 에이전트라면 중요하다.

## A2A와 Internal Domain

통신 규약의 객체를 내부 Domain Model에 직접 종속시키지 않는 원칙은 MCP와 같다.

~~~text
Internal Delegation Model
        ↓
A2A Adapter
        ↓
Remote Agent
~~~

Protocol Version이 바뀌어도 내부 목표와 Artifact Model을 유지하기 쉽다.

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

원격 에이전트는 전문 역할의 에이전트이지만 최종 판단하거나 실행할 권한은 아닐 수 있다.

## 이 장에서 가져갈 것

원격 에이전트를 도구처럼 단순화하면 유지 과정과 판단하거나 실행할 권한을 놓칠 수 있다. 다음 경계를 유지한다.

~~~text
MCP Task
≠ A2A Task
≠ Factory Task

Remote Agent
≠ Local Subagent
~~~

A2A는 independent Agent System 간 Collaboration Boundary다. 이제 책의 마지막 장에서 지금까지의 내용을 도입 순서로 압축한다. 처음부터 메모리, 여러 에이전트의 협업, 경량 가상 머신을 모두 넣지 않고 Minimum Viable 운영 에이전트에서 어떻게 시작할 것인가.

## 주요 근거

- A2A Protocol Specification 1.0.0 (2026-10-02 기준)
- MCP 2026-07-28
- research/topics/12-mcp-a2a-task-boundary.md
- research/topics/07-multi-agent-interoperability.md
