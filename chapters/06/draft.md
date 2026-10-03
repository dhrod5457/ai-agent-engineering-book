# 6장. MCP와 Capability Boundary

에이전트마다 GitHub 연결 프로그램, 데이터베이스 연결 프로그램, 브라우저 연결 모듈, 내부 API 연결 모듈을 따로 구현하기 시작하면 빠르게 중복이 생긴다. 다른 에이전트가 같은 기능을 쓰려면 다시 연결해야 한다. 도구의 이름과 데이터 형식도 각 애플리케이션 안에 갇힌다. MCP는 이런 통합 문제를 줄이기 위해 등장한 통신 규약 중 하나다. 하지만 MCP를 사용한다고 에이전트 설계 구조 전체가 해결되는 것은 아니다. MCP는 **에이전트와 기능 제공자 사이의 연결 경계**다.

## MCP가 해결하려는 문제

에이전트가 외부 기능을 사용하려면 몇 가지 공통 문제가 반복된다.

- Capability Discovery
- 도구의 입력 형식
- Resource Access
- Prompt/Template 제공
- Transport
- 권한 확인(Authorization) 연결
- Long-running Operation 표현

각 Agent Application이 이를 제각각 구현하면 Connector가 늘어난다. MCP는 공통 통신 규약을 제공한다. 개념적으로는 다음 구조다.

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

이 구조에서 MCP 서버는 에이전트 역할을 하는 것이 아니라, 에이전트가 사용할 기능을 제공한다.

## MCP는 Agent Loop를 대신하지 않는다

MCP를 붙여도 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)는 여전히 다음을 결정해야 한다.

- 어떤 기능을 현재 에이전트에게 보여줄 것인가.
- 어떤 도구 호출을 허용할 것인가.
- 결과를 컨텍스트(Context: 모델에 전달하는 정보)에 얼마나 넣을 것인가.
- 실패하면 재시도할 것인가.
- 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)에 승인이 필요한가.
- 장시간 실행 결과를 어떤 상태와 연결할 것인가.
- 완료를 어떻게 검증할 것인가.

MCP는 Tool Transport와 Discovery를 표준화할 수 있다. 에이전트의 목표와 반복 실행을 자동으로 설계하지는 않는다.

~~~text
MCP
≠ Agent Harness
~~~

이 구분이 중요하다.

## Tool과 Resource

MCP에서는 기능을 여러 형태로 표현할 수 있다. 이 책에서는 세부 API보다 책임을 본다.

### Tool

에이전트가 행동을 요청하는 인터페이스다.

예:

~~~text
create_issue
run_query
send_message
~~~

### Resource

에이전트가 읽을 수 있는 정보 원본을 표현할 수 있다.

예:

~~~text
repository://docs/architecture
database://schema
internal://policy
~~~

### Prompt

재사용 가능한 Prompt Template 또는 컨텍스트 관련 기능을 제공할 수 있다. 중요한 것은 이 세 가지가 에이전트 내부 상태와 같지 않다는 점이다. 접근 대상 자원을 읽었다고 Agent Memory가 되는 것은 아니다. 프롬프트를 제공한다고 Agent Instruction Architecture가 자동으로 해결되는 것도 아니다. 통신 규약의 객체와 Domain Object를 분리한다.

## 2026-07-28의 Stateless Core

2026-07-28 MCP base specification은 final 상태이며, 이 revision의 중요한 변화 중 하나는 protocol core를 stateless하게 만든 것이다. 기존처럼 protocol-level session에 의존하기보다 각 request가 필요한 protocol/client context를 함께 전달하는 방향으로 바뀌었다. 이 변화가 주는 설계상 교훈은 명확하다.

~~~text
Protocol Session
≠ Application Session
≠ Runtime Session
≠ Agent Goal
~~~

MCP Core가 Stateless하다고 해서 Agent Application이 상태를 가지면 안 된다는 뜻이 아니다. 오히려 Agent State를 Protocol Connection에 묶지 않는 편이 더 명확하다.

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

G-102와 R-77은 서로 다른 유지 과정을 가질 수 있다.

## Long-running Capability와 MCP Task

짧은 도구는 Request/Response로 충분하다. 하지만 다음 같은 작업은 오래 걸릴 수 있다.

- 대용량 분석
- 장시간 빌드
- External Job
- Batch Processing

MCP의 Tasks는 이런 Long-running Capability Invocation을 표현하기 위한 별도 extension이다. 2026-10-02 기준 base protocol revision은 final이지만 Tasks extension 문서는 Draft로 표시돼 있으므로, core protocol과 같은 안정성 수준으로 취급하지 않는다.

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

여기서 주의할 점이 있다. MCP Task는 Product Domain의 작업과 같지 않다. 이 책에서는 구분을 위해 다음처럼 본다.

~~~text
MCP Task
= Long-running Capability Invocation
~~~

예를 들어 "고객 환불 처리"라는 Product Task 하나가 여러 MCP Tool Call과 MCP Task를 포함할 수 있다.

## 같은 Task라는 이름의 함정

에이전트 시스템에는 작업이라는 이름이 너무 많이 등장한다.

- Agent Task
- MCP Task
- A2A Task
- Workflow Task
- Factory Task

이들을 하나의 내부 Entity로 합치면 유지 과정이 꼬일 수 있다. 예를 들어 Software Factory의 작업은 다음 정보를 가질 수 있다.

~~~text
Requirement
Owner
Acceptance
Worker Assignment
Delivery
~~~

MCP Task는 이런 조직 작업 항목 전체를 의미하지 않는다. 따라서 내부 Domain Model에서 통신 규약의 객체를 Adapter로 감싸는 편이 안전하다.

~~~text
Internal Work / Goal
      ↓
Protocol Adapter
      ↓
MCP Task
~~~

## Capability Discovery와 Authorization은 다르다

MCP 서버가 도구를 제공한다고 해서 현재 에이전트가 그 도구를 실행할 권한까지 얻는 것은 아니다.

~~~text
Discovery
= 어떤 Capability가 존재하는가

Authorization
= 현재 Principal이 그 Action을 실행할 수 있는가
~~~

통신 규약 수준의 Authentication/Authorization이 있어도 Application Policy는 남는다. 예를 들어 에이전트가 GitHub MCP Server에 정상적으로 인증됐다고 하자. 그 인증 정보(Credential)가 다음을 허용할 수 있다.

- Read Repository
- Create Issue
- Merge PR

하지만 현재 Agent Goal은 Documentation 조회뿐일 수 있다. 그렇다면 애플리케이션은 더 좁은 정책을 적용할 수 있다.

~~~text
Protocol Credential Scope
        ↓
Application Policy
        ↓
Current Effective Capability
~~~

최소 권한은 여러 계층에서 적용될 수 있다.

## MCP Result도 Context Boundary를 통과한다

MCP 서버가 반환한 도구 실행 결과는 모델에게 전달될 수 있다. 하지만 결과는 그대로 컨텍스트에 넣지 않을 수 있다.

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

특히 외부 Web, Email, Document를 읽는 MCP Tool은 Prompt Injection Source가 될 수 있다. 서버 자체를 신뢰한다고 반환 내용까지 모두 trusted instruction으로 취급하지 않는다.

## MCP가 Agent Architecture를 단순화하는 지점

MCP는 에이전트와 External Capability의 결합도를 줄이는 데 사용할 수 있다.

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

이런 구조는 Capability Integration을 재사용하기 쉽게 만든다. 하지만 shared integration이 shared authority를 의미하지는 않는다. 각 에이전트와 사용자의 Authorization Context는 별도로 유지해야 한다.

## MCP Server는 Enforcement Point가 될 수 있다

MCP 서버는 에이전트와 외부 시스템 사이의 Enforcement Point가 될 수 있다. 다만 모든 정책이 반드시 MCP 서버 하나에 모여야 하는 것은 아니다.

가능한 책임:

- Schema Validation
- Credential Handling
- Endpoint Restriction
- Result Normalization
- 감사
- Rate Limit

하지만 모든 정책을 서버 한 곳에 넣을 필요도 없다.

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

처럼 여러 계층이 존재할 수 있다. 중요한 것은 각 계층이 무엇을 강제하는지 분명히 하는 것이다.

## MCP와 A2A는 다른 문제를 푼다

MCP를 에이전트 간 통신 규약으로 생각하기 쉽다. 하지만 A2A는 다른 경계를 다룬다.

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

첫 번째는 Tool/Capability를 호출한다. 두 번째는 다른 에이전트 시스템에 업무를 위임한다. A2A는 Part VII에서 자세히 다룬다.

## 작은 예: 대학 행정 Agent

대학 행정 에이전트가 다음 기능을 사용한다고 하자.

- 학사 규정 검색
- 학생 정보 조회
- 담당자에게 메시지 전송

MCP를 이용해 세 기능을 제공할 수 있다.

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
- 에이전트가 학생에게 직접 메시지를 보낼 수 있는가.
- 메시지 전송 전 승인이 필요한가.
- 조회 결과를 메모리에 저장해도 되는가.

이것들은 신원, 정책, Memory Boundary의 문제다. 통신 규약을 도입해도 신원, 정책, 메모리 같은 애플리케이션 책임은 남는다.

## Protocol을 내부 Architecture의 중심으로 두지 않는다

통신 규약은 바뀔 수 있다. 버전도 바뀌고 Extension도 추가된다. 책 전체 설계 구조가 통신 규약의 객체에 직접 종속되면 변화에 취약해진다. 따라서 내부에서는 다음 책임을 먼저 정의한다.

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

이 접근은 다른 통신 규약이 추가돼도 내부 모델을 유지하기 쉽다.

## Part II에서 가져갈 것

Part II에서는 에이전트의 양쪽 인터페이스를 살펴봤다.

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

컨텍스트 구성 계층은 외부 세계에서 현재 판단에 필요한 정보를 골라 모델에게 전달한다. 도구 인터페이스는 모델이 제안한 행동을 검증 가능한 기능으로 바꾼다. MCP는 Tool/Resource 같은 기능을 외부 Provider와 연결하는 Protocol Boundary다. 하지만 아직 중요한 문제가 남는다. 에이전트가 여러 차례와 여러 실행 환경에 걸쳐 작업한다면 현재 목표와 진행 상황, 이미 실행한 행동을 어디에 보존해야 할까. Conversation Context만으로는 부족하다. Part III에서는 세션, 작업 공간, 목표, 메모리를 먼저 분리하고, 이 책의 중심 개념인 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)으로 들어간다.

## 주요 근거

- Model Context Protocol 2026-07-28
- MCP Specification / Tasks Extension
- research/topics/03-tools-protocols.md
- research/topics/12-mcp-a2a-task-boundary.md
