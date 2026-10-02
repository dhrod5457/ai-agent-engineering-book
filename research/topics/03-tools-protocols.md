# Tools and Protocols

## Tool은 API 목록이 아니다

SWE-agent의 Agent-Computer Interface 연구와 Anthropic Tool Engineering 자료를 보면 Agent 성능은 model뿐 아니라 행동 공간을 어떻게 표현하는가에 크게 좌우된다.

좋은 Tool Interface는 다음 질문에 답해야 한다.

- 이 tool은 어떤 capability를 제공하는가.
- 언제 사용해야 하는가.
- 언제 사용하면 안 되는가.
- 입력 schema가 모호하지 않은가.
- 결과가 다음 decision에 필요한 형태인가.
- side effect가 있는가.
- 권한과 scope는 무엇인가.
- 실패가 machine-readable한가.

## Tool Surface가 너무 넓을 때

~~~text
Too Many Tools
→ selection ambiguity
→ schema/context cost
→ duplicate capability
→ permission expansion
→ larger injection surface
→ maintenance difficulty
~~~

따라서 tool 수보다 명확한 capability boundary가 중요하다.

## Tool Result도 Context다

Tool 결과는 곧바로 model context로 들어가기 때문에:

- 크기 제한
- summary/index
- structured output
- provenance
- trust level
- sensitive data redaction

이 필요하다.

특히 외부 tool이 반환한 자연어는 prompt injection input이 될 수 있다.

## MCP의 위치

MCP는 Agent 자체가 아니다.

~~~text
Agent Harness
    ↓
MCP Client
    ↓
MCP Server
    ↓
Tool / Resource / Prompt / Extension
~~~

2026-07-28 MCP는 stateless core, cache hints, authorization hardening, extension framework를 강화했다.

책에서는 MCP를 capability transport / integration boundary로 다루고, reasoning loop나 orchestration과 동일시하지 않는다.

## A2A의 위치

A2A는 MCP와 문제 영역이 다르다.

~~~text
MCP
Agent ↔ capability / context provider

A2A
Agent System ↔ independent Agent System
~~~

A2A의 Task / Message / Artifact 구조는 remote Agent가 내부 memory/tool을 공개하지 않고도 협업하도록 한다.

## Protocol을 사용해도 남는 책임

표준 protocol을 사용해도 application은 다음을 결정해야 한다.

- authorization
- tenant boundary
- tool allowlist
- approval
- data classification
- timeout
- retry
- idempotency
- audit
- result validation

Protocol은 trust policy를 대신하지 않는다.

## 설계 원칙 후보

1. Tool은 Agent-facing product interface다.
2. Tool name/description/schema는 eval 대상이다.
3. Side effect가 큰 tool일수록 좁은 contract를 가진다.
4. Tool output은 untrusted context로 취급할 수 있어야 한다.
5. MCP와 A2A를 Agent Architecture 전체로 오해하지 않는다.
6. Capability discovery와 authorization을 분리한다.
