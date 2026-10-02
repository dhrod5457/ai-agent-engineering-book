# Part VII Structural Review

기준일: 2026-10-02
대상:
- chapters/22/draft.md
- chapters/23/draft.md
- chapters/24/draft.md
- chapters/25/draft.md
- chapters/epilogue/draft.md

## Part VII의 역할

마지막 Part는 Agent Architecture를 더 복잡하게 만드는 시점과 상위 시스템으로 넘어가는 경계를 다룬다.

~~~text
22장
왜 Single-Agent에서 시작하는가?
        ↓
23장
여러 Agent를 어떤 ownership pattern으로 연결하는가?
        ↓
24장
독립 Remote Agent와 어떤 protocol boundary를 가지는가?
        ↓
25장
전체 책을 어떤 production 도입 순서로 압축하는가?
        ↓
Epilogue
오래 남을 원칙은 무엇인가?
~~~

## 22장 검토

핵심 역할:
- Single-Agent baseline
- Multi-Agent가 해결하지 못하는 문제
- Context / Permission Isolation
- Independent Review
- Parallelism과 Coordination Cost

좋은 점:
- Agent 수를 maturity로 보지 않는다.
- Multi-Agent 도입 이유를 boundary benefit으로 제한한다.
- Part I~VI에서 해결한 기본 문제를 전제로 한다.

결론: PASS.

## 23장 검토

핵심 역할:
- Agent-as-Tool과 Handoff의 ownership 차이
- Context Transfer
- Authority Transfer
- State Ownership
- Result Contract

좋은 점:
- Multi-Agent를 조직도 설명이 아니라 ownership semantics로 다룬다.
- Handoff에 Context뿐 아니라 Authority가 포함된다는 점이 명확하다.

주의:
- Parent/Child Goal, Shared State Pattern은 구현 선택지로만 유지한다.

결론: PASS.

## 24장 검토

핵심 역할:
- Remote Agent ≠ Tool
- MCP ↔ Capability Provider
- A2A ↔ Independent Agent System
- Message / Task / Artifact
- Authorization / Async Lifecycle
- Protocol Task와 내부 Task 경계

좋은 점:
- 6장의 MCP와 대칭 구조를 만든다.
- A2A를 전체 Agent Architecture로 확대하지 않는다.
- Remote Artifact도 Local Verification 대상이 될 수 있음을 명시한다.

주의:
- Protocol Version과 Lifecycle State는 출간 직전 최신 Specification 재검증.
- A2A를 mandatory architecture로 표현하지 않는다.

결론: PASS.

## 25장 검토

핵심 역할:
- 전체 책의 도입 순서 압축
- Minimal Agent
- Control before Autonomy
- Verification before Scale
- Agent State Plane → Factory Control Plane

좋은 점:
- 기능 목록이 아니라 필요가 생길 때 확장하는 구조다.
- Software Factory 책으로 자연스럽게 연결된다.

주의:
- 제시한 단계는 공식 maturity model이 아님을 현재처럼 명시한다.
- 실제 시스템은 Risk와 Domain에 따라 순서가 달라질 수 있다.

결론: PASS.

## Epilogue 검토

책 전체 주장을 다음으로 수렴한다.

> 좋은 Agent 시스템은 모델을 무조건 믿는 시스템이 아니라, 모델을 덜 믿어도 실제 일을 맡길 수 있는 시스템이다.

Concept와 일치한다.

25장과 일부 메시지가 반복되지만 25장은 실행 순서, Epilogue는 저자의 최종 관점이라는 역할 차이가 있다.

Line Review에서 중복 문장만 압축하면 된다.

## Part VII 핵심 경계

~~~text
Single-Agent ≠ Low Maturity
Agent-as-Tool ≠ Handoff
Remote Agent ≠ Tool
MCP Task ≠ A2A Task ≠ Factory Task
Agent State Plane ≠ Factory Control Plane
~~~

## 분량

현재 문자 수:
- 22장 약 4.0k
- 23장 약 3.9k
- 24장 약 4.3k
- 25장 약 5.1k
- Epilogue 약 3.1k

이전 Part보다 짧지만 마지막 Part는 새로운 low-level mechanism보다 앞선 구조를 조합하고 경계를 정리하는 역할이므로 현재 분량은 허용 가능하다.

## Structural Review 결론

PASS.

Part VII와 Epilogue Draft는 완료 상태다.
