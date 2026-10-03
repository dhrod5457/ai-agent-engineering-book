# AI Agent Engineering

## LLM을 실제 작업 가능한 Agent로 만드는 설계 원칙

상태: Manuscript Assembly v0.1
기준일: 2026-10-02

## 이 책의 질문

이 책은 "어떤 에이전트 프레임워크를 쓸 것인가"보다 다음 질문을 다룬다.

~~~text
Model의 판단을 실제 행동으로 바꿀 때
어떤 책임을 어디에 둘 것인가?
~~~

핵심 범위:

- 에이전트의 실행 반복 과정과 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)
- 컨텍스트(Context: 모델에 전달하는 정보)와 도구 인터페이스
- 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)와 복구
- 장시간 실행
- 메모리와 Memory Security
- 신원 / 인증 정보(Credential) / 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경) / 정책
- 실행 추적 기록(Trace) / 평가 / Harness Improvement
- 여러 에이전트의 협업과 Remote Agent Boundary

## 핵심 경계

~~~text
Model ≠ Agent
Context ≠ Durable State
Session ≠ Goal
Memory ≠ Source of Truth
Harness ≠ Runtime
Sandbox ≠ Authorization
Completion Claim ≠ Completion Authority
MCP Task ≠ A2A Task ≠ Factory Task
Agent State Plane ≠ Factory Control Plane
~~~

## Source Note

원고의 `[S-*]`는 외부 Source ID, `[B-*]`는 이 책의 synthesis ID다.

정의:
- planning/source-catalog.md
- planning/source-note-conventions.md

Protocol, product, preprint처럼 변경 가능성이 높은 사실은 `review/freshness/`의 publication-time gate에서 다시 검증한다.
