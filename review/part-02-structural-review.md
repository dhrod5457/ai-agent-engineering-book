# Part II Structural Review

기준일: 2026-10-02
대상:
- chapters/04/draft.md
- chapters/05/draft.md
- chapters/06/draft.md

## Part II의 역할

Part II는 Agent의 양쪽 Interface를 나눈다.

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

그리고 MCP는 Tool/Resource Capability를 외부 Provider와 연결하는 Protocol Boundary로 배치한다.

세 장의 질문은 다음과 같다.

~~~text
4장: Model에게 무엇을 보여줄 것인가?
5장: Model의 Action을 어떤 Interface로 표현할 것인가?
6장: 그 Capability를 외부 Provider와 어떻게 연결할 것인가?
~~~

## 4장 검토

핵심 역할:
- Context = Current Inference Input
- Context ≠ Durable State
- State → Context Projection
- Progressive Context
- Compaction의 한계

좋은 점:
- Part I의 Harness에서 자연스럽게 이어진다.
- State Plane을 미리 설명하지만 구현 상세는 Part III에 남긴다.
- Tool Schema와 Tool Result가 Context를 소비한다는 점이 5장으로 연결된다.

주의:
- State Plane preview가 너무 길어지지 않게 유지한다.
- Retrieval/RAG 구현으로 확장하지 않는다.
- "More Context ≠ Better Agent"는 절대 명제가 아니라 설계 경고로 유지한다.

결론: PASS.

## 5장 검토

핵심 역할:
- API ≠ Agent Tool
- Tool = Agent-facing Action Interface
- Tool Surface와 Action Space
- Schema / Result / Error / Side Effect Contract
- Eligibility ≠ Authorization

좋은 점:
- Context 장과 반대 방향 Interface라는 구조가 명확하다.
- Tool Result의 trust/provenance가 Security와 Context를 연결한다.
- MCP를 별도 Protocol 장으로 넘길 경계가 명확하다.

주의:
- Shell Tool이 항상 나쁘다는 의미로 읽히지 않게 현재 trade-off 표현을 유지한다.
- Tool을 지나치게 세분화하는 것 역시 cost가 있다는 점을 line review에서 한 문장 보강할 수 있다.
- ACI는 SWE-agent 논문의 용어이고 모든 Tool 시스템의 공식 표준명은 아니라는 점을 유지한다.

결론: PASS.

## 6장 검토

핵심 역할:
- MCP = Capability / Context Integration Boundary
- MCP ≠ Agent Harness
- Protocol Session ≠ Runtime Session
- MCP Task ≠ Product / Factory Task
- Discovery ≠ Authorization
- MCP ≠ A2A

좋은 점:
- MCP를 책 전체 Architecture의 중심으로 두지 않는다.
- 2026-07-28 stateless core 변화는 State를 Protocol Connection에서 분리하는 논거로만 사용한다.
- A2A는 예고 수준으로 제한하고 Part VII에 상세를 남긴다.

주의:
- MCP specification 세부가 빠르게 변하므로 출간 직전 version 재검증 대상이다.
- Tool/Resource/Prompt 설명은 protocol tutorial로 확장하지 않는다.
- "MCP Server를 Trust Boundary로 본다"는 문장은 모든 MCP Server가 단일 trust boundary라는 뜻이 아니라 architecture상 중요한 enforcement point가 될 수 있다는 의미로 유지한다.

결론: PASS.

## 장 간 중복

### 4장 ↔ 5장
Tool Schema와 Tool Result가 양쪽에 등장한다.

역할:
- 4장: Context Cost / Context Safety 관점
- 5장: Tool Contract / Action Interface 관점

중복이 아니라 동일 객체를 양쪽 boundary에서 보는 구조로 유지한다.

### 5장 ↔ 6장
Tool Contract와 MCP Tool이 겹친다.

역할:
- 5장: Tool 자체의 설계 원칙
- 6장: 외부 Tool Provider와 Protocol 연결

MCP가 Tool Engineering을 대체하지 않는다고 명시했으므로 경계가 유지된다.

### 6장 ↔ 14~17장
Authorization / Credential / Policy가 예고된다.

현재는 "Protocol이 해결하지 않는 책임"을 보여주는 수준이다.
Identity와 Security 구현 원칙은 Part V에 남긴다.

## 용어 점검

planning/terminology.md와 충돌 없음.

특히 다음 경계가 유지된다.

~~~text
Context ≠ State
Tool ≠ Raw API
Eligibility ≠ Authorization
MCP ≠ Harness
Protocol Session ≠ Runtime Session
MCP Task ≠ Factory Task
MCP ≠ A2A
~~~

## 흐름 점검

~~~text
Part I
Model → Loop → Harness
        ↓
Part II
Context → Tool → MCP
        ↓
Part III
State Taxonomy → Agent State Plane
~~~

연결 상태: PASS.

## 분량

현재 문자 수:
- 4장 약 8.0k
- 5장 약 7.9k
- 6장 약 8.0k

상대적 균형은 양호하다.

## Structural Review 결론

PASS.

Part II Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part III 7~11장 Draft
2. 특히 8장 Agent State Plane을 책의 중심 장으로 충분히 전개
3. 11장에서는 targeted research의 selective revalidation 근거 반영
4. Part III Structural Review
