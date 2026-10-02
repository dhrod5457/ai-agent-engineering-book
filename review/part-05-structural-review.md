# Part V Structural Review

기준일: 2026-10-02
대상:
- chapters/14/draft.md
- chapters/15/draft.md
- chapters/16/draft.md
- chapters/17/draft.md

## Part V의 역할

Part V는 Agent Security를 네 개의 서로 다른 질문으로 나눈다.

~~~text
14장
누가 행동하는가?
        ↓
15장
어떤 Credential로 행동하는가?
        ↓
16장
실제로 어디까지 도달할 수 있는가?
        ↓
17장
지금 이 Action을 실행해도 되는가?
~~~

이 구분이 Part V의 핵심이다.

## 14장 검토

핵심 역할:
- User / Application / Agent / Workload / Tool / Resource Identity
- Delegated vs Autonomous
- Actor Chain
- Discovery ≠ Authentication ≠ Authorization ≠ Approval
- Agent Lifecycle

좋은 점:
- Agent를 독립 Principal로 보는 흐름이 명확하다.
- A2A와 Multi-Agent로 확장될 기반을 만든다.
- Credential 상세를 15장으로 넘긴다.

주의:
- 모든 시스템이 별도 Agent Identity를 반드시 가져야 한다는 의미로 쓰지 않는다.
- Microsoft Entra Agent ID를 업계 표준으로 일반화하지 않는다.

결론: PASS.

## 15장 검토

핵심 역할:
- Standing Credential 위험
- Short-lived Credential
- Delegated / Autonomous Token
- Credential Broker / Gateway Injection
- Tool별 Credential Scope
- Runtime Role도 Credential Boundary라는 점

좋은 점:
- Identity와 Credential을 분리한다.
- Sandbox가 Credential Scope를 대체하지 않는다고 명시한다.
- Prompt Injection 대응을 Gateway Enforcement와 연결한다.

주의:
- 특정 OAuth Flow를 유일한 구현처럼 표현하지 않는다.
- Short-lived Token도 여전히 탈취될 수 있으므로 만능 해결책처럼 쓰지 않는다.

결론: PASS.

## 16장 검토

핵심 역할:
- Containment 정의
- Filesystem / Network / Process Boundary
- OS Sandbox / Container / gVisor / MicroVM
- Disposable Runtime
- Runtime Session ≠ Durable State

좋은 점:
- Sandbox를 permission prompt와 분리한다.
- 기술 이름보다 선택 기준을 먼저 제시한다.
- Part III의 Durable State와 연결된다.

주의:
- Isolation ladder를 절대적 보안 순위처럼 읽히지 않게 유지한다.
- 기술별 성능 수치는 출간 직전 재검증한다.

결론: PASS.

## 17장 검토

핵심 역할:
- Risk Inputs
- R0~R4 illustrative control profile
- External Policy Evaluation
- Risk-tiered Human Approval
- JIT Privilege
- Policy Expansion
- Effective Policy Manifest
- Independent Verification / Rollback

좋은 점:
- targeted research의 risk-tiered approval과 originating user context를 반영했다.
- Agent self-authorization을 허용하지 않는다.
- R0~R4를 표준 taxonomy가 아니라 설명용 profile로 명확히 제한한다.

주의:
- 모든 조직이 R0~R4를 그대로 도입해야 한다는 표현 금지.
- Human Approval이 항상 필요한 Control이라는 의미로 읽히지 않게 risk-tiered 원칙을 유지한다.

결론: PASS.

## 장 간 중복

### 14장 ↔ 15장
Identity와 Credential이 연결되지만 역할이 다르다.

~~~text
Identity
= who

Credential
= proof/capability used to access
~~~

현재 분리 적절.

### 15장 ↔ 16장
Credential Injection과 Sandbox가 겹친다.

15장:
- secret/token exposure와 issuance

16장:
- runtime reachability와 containment

경계 유지됨.

### 16장 ↔ 17장
Sandbox Level과 Risk Profile이 연결된다.

16장:
- isolation technology / runtime boundary

17장:
- risk에 따라 어떤 control profile을 선택하는가

구조상 적절.

## Part V 핵심 경계

~~~text
Identity ≠ Credential
Credential Scope ≠ Sandbox
Sandbox ≠ Authorization
Authorization ≠ Approval
Policy Manifest ≠ Policy Authority
~~~

## 분량

현재 문자 수:
- 14장 약 6.3k
- 15장 약 5.5k
- 16장 약 6.0k
- 17장 약 7.4k

17장이 통제 모델을 종합하는 장이라 가장 긴 편이며 적절하다.

15장은 최종 Line Review에서 실제 credential broker 예시를 조금 보강할 수 있지만 Structural Gap은 없다.

## Structural Review 결론

PASS.

Part V Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part VI 18~21장 Draft
2. Trace → Eval → Eval CI → Harness Ablation 흐름 유지
3. 21장에 targeted research의 repeated trials / variance 근거 반영
4. Part VI Structural Review
