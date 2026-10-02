# Writing Style Guide

기준일: 2026-10-02

이 문서는 AI Agent Engineering 본문 Draft의 공통 문체 기준이다.

software-factory-book의 집필 원칙을 계승하되, 이 책의 핵심인 Agent Harness / State / Runtime / Security 경계를 추가한다.

# 1. 독자

주 독자는 실무 경험이 있는 Software Engineer / Backend Engineer / Platform Engineer / Tech Lead / Architect다.

LLM이나 API의 기초 설명은 최소화한다.

Agent Engineering에서 새롭게 등장하는 개념은 기존 Software Engineering 개념과 연결해 설명한다.

# 2. 기본 문체

목표:

> 실무 개발자가 동료 개발자에게 Agent 시스템의 설계 판단을 설명하는 문체.

사용:
- 짧고 명확한 문장
- 실제 개발 상황
- failure case
- 구조도
- trade-off
- 검증 방법

피함:
- AI 찬양
- 과도한 미래 예측
- 제품 마케팅 문구
- 필요 없는 형용사
- 개념을 늘리기 위한 개념

# 3. 주장 순서

가능하면 다음 순서를 사용한다.

~~~text
문제
→ 실제 실패
→ 왜 단순한 방식으로 부족한가
→ 책임 경계
→ 설계 원칙
→ 구현 선택지
→ 검증 방법
→ 한계
~~~

# 4. 핵심 구분을 반복해서 지킨다

책 전체에서 다음 경계를 흐리지 않는다.

~~~text
Model ≠ Agent
Context ≠ Durable State
Session ≠ Goal
Workspace ≠ Memory
Memory ≠ Source of Truth
Harness ≠ Runtime
Sandbox ≠ Authorization
Approval ≠ Containment
MCP Task ≠ A2A Task ≠ Factory Task
Agent State Plane ≠ Factory Control Plane
~~~

# 5. 이 책의 synthesis 용어

다음은 외부 표준이 아니라 이 책이 설명을 위해 정리한 synthesis다.

- Agent State Plane
- Harness Debt
- Risk R0~R4 control profile
- AgentVersion tuple
- Memory Write Gate

처음 등장할 때 반드시 이 성격을 밝힌다.

# 6. Vendor 사례

제품이 Chapter의 주어가 되지 않게 한다.

Bad:
> OpenAI는 Session을 제공한다. AWS는 microVM을 제공한다.

Better:
> Session과 Runtime State를 분리해야 하는 이유를 설명한 뒤, OpenAI와 AWS 구현을 서로 다른 사례로 사용한다.

Vendor 자료는:

~~~text
관찰
→ 조건
→ 일반화 한계
→ 설계 원칙
~~~

순서로 해석한다.

# 7. 연구와 숫자

숫자는 장식으로 사용하지 않는다.

항상:
- 기준일
- benchmark/version
- task/environment
- grader
- 연구 한계

를 함께 본다.

Preprint는 preprint임을 숨기지 않는다.

# 8. 코드보다 구조

이 책은 Framework tutorial이 아니다.

코드가 필요하면:
- 최소 pseudo-code
- 작은 schema
- event example
- policy fragment

정도만 사용한다.

긴 SDK 사용법은 피한다.

# 9. 도식

도식은 responsibility boundary나 state transition을 설명할 때 사용한다.

좋은 예:

~~~text
State Plane
   ↓ projection
Context Engine
   ↓
Model
~~~

장식용 화살표는 피한다.

# 10. 실패를 정상 상태로 다룬다

Agent가 실패하지 않는다는 전제로 쓰지 않는다.

각 장에서 가능하면:
- 실패 종류
- 감지 방법
- recovery
- verification

을 포함한다.

# 11. Security

Security를 별도 마지막 절로 붙이지 않는다.

Tool, Memory, State, Runtime, Identity를 설명할 때 해당 boundary의 security implication을 같이 설명한다.

Prompt-only safety를 system-level enforcement와 같은 수준으로 표현하지 않는다.

# 12. Memory

Memory를 지능의 상징처럼 표현하지 않는다.

항상:
- write authority
- scope
- provenance
- freshness
- invalidation
- retrieval policy

를 고려한다.

# 13. Multi-Agent

Agent 수를 maturity로 표현하지 않는다.

Single-Agent baseline 없이 Multi-Agent 장점을 주장하지 않는다.

# 14. Chapter 시작

현실적인 실패 또는 질문에서 시작한다.

긴 정의나 역사부터 시작하지 않는다.

# 15. Chapter 종료

같은 내용을 요약해서 반복하기보다 다음 장에서 필요한 질문으로 연결한다.

# 16. 목록

논리를 목록만으로 전달하지 않는다.

목록은:
- 구성요소
- 상태
- 비교
- checklist

에 사용한다.

# 17. 영어 용어

실무에서 일반적인 용어는 영어를 유지할 수 있다.

예:
- Agent
- Model
- Harness
- Runtime
- Context
- State
- Memory
- Tool
- Sandbox
- Trace
- Eval
- MCP
- A2A

하지만 같은 개념은 한 장 안에서 표기를 바꾸지 않는다.

# 18. 장별 완료 기준

초고는 Chapter Plan의 다음 요소를 모두 만족해야 한다.

- Goal
- Core Claims
- 최소 하나의 concrete failure
- 책임 경계
- 설계 원칙
- Evidence
- Avoid 범위 준수
- 다음 장 연결

# 19. 출간 직전 재검증

다음은 publication-time recheck 대상이다.

- protocol version
- product feature name
- model name
- preview / GA status
- benchmark revision
- vendor architecture
- security guidance

본문 핵심 논리는 이 값이 바뀌어도 유지되게 작성한다.
