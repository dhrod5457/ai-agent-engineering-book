# Part I Structural Review

기준일: 2026-10-02
대상:
- chapters/01/draft.md
- chapters/02/draft.md
- chapters/03/draft.md

## 결과

Part I의 역할은 다음 세 질문으로 정리된다.

~~~text
1장: Agent는 Model과 무엇이 다른가?
2장: Agent는 어떻게 반복 실행되는가?
3장: 그 실행 Control을 어디에 둘 것인가?
~~~

세 장의 책임은 분리돼 있고 Part II Context로 자연스럽게 연결된다.

## 장별 역할

### 1장
책 전체의 문제와 boundary를 소개한다.

유지해야 할 핵심:
- Model Capability ≠ Agent Capability
- Framework ≠ Architecture
- Model / Harness / Runtime 1차 분리
- Agent State Plane은 preview 수준

주의:
State Plane, Memory, Identity를 너무 상세히 설명하면 뒤 장의 긴장을 약화시킨다. 현재는 개념 소개 수준으로 유지한다.

### 2장
Agent 실행의 최소 loop와 production control을 설명한다.

유지해야 할 핵심:
- Tool Call ≠ Actual Action
- Conversation Stop ≠ Task Completion
- Failure Classification
- Pause / Resume
- Retry와 State 연결

주의:
Retryable / Repairable / Blocked / Fatal taxonomy는 외부 표준이 아니라 설명용 예시임을 line review에서 한 번 더 표시한다.

### 3장
Harness를 독립 software layer로 고정한다.

유지해야 할 핵심:
- Framework ≠ Harness
- Harness component = hypothesis
- Disposable Runtime + Durable State
- Harness Debt
- Model upgrade → Harness audit

주의:
Harness Ablation 상세는 21장에 남기고 여기서는 원칙과 preview까지만 유지한다.

## 중복 점검

### 1장 ↔ 3장
Framework/Harness 경계가 양쪽에 등장한다.

현재 역할:
- 1장: Framework가 Architecture를 대신하지 않는다는 경고
- 3장: Harness의 구체적 책임과 lifecycle

따라서 완전 중복은 아니다.

Line Review에서 1장의 Framework 절이 길어지지 않도록 유지한다.

### 2장 ↔ 8~9장
Pause/Resume와 State가 예고된다.

현재는 "왜 durable state가 필요한가"를 만드는 수준이므로 허용한다.

Event History, Checkpoint, Idempotency 구현은 8~9장에 남긴다.

### 3장 ↔ 21장
Ablation이 예고된다.

3장:
- Harness component는 hypothesis
- model upgrade 시 재검증

21장:
- repeated trials
- variance
- ablation procedure
- Harness Debt 운영

책임 분리가 가능하다.

## 용어 점검

Part I에서 사용하는 핵심 용어:
- Model
- Agent
- Harness
- Runtime
- Context
- State
- Memory
- Tool
- Sandbox
- Trace
- Eval

planning/terminology.md와 충돌 없음.

## 흐름 점검

~~~text
1장
Model만으로 Agent를 설명할 수 없다
        ↓
2장
실제 Agent는 Loop와 Control을 가진다
        ↓
3장
그 Control을 Harness라는 software layer로 본다
        ↓
4장
Harness가 Model에 무엇을 보여줄 것인가: Context
~~~

연결 상태: PASS.

## 분량

현재 문자 수:
- 1장 약 7.5k
- 2장 약 7.0k
- 3장 약 7.8k

Part I 초고의 상대적 균형은 양호하다.

최종 원고에서는 source citation, 사례 확장, line editing 후 분량이 변할 수 있다.

## Structural Review 결론

PASS.

Phase 6 Part I Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part II 4~6장 Draft
2. Part II Structural Review
3. 전체 Draft 후 Line Review에서 Part I 반복 압축
