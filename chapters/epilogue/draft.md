# Epilogue. Agent를 더 똑똑하게 만드는 것보다 시스템을 더 믿을 수 있게 만든다

이 책은 Model 이야기로 시작했다.

같은 Model을 사용해도 Agent의 실제 능력은 달라질 수 있다고 했다.

마지막까지 오면 그 이유가 분명해진다.

Agent는 Model 하나가 아니다.

~~~text
Model
+ Context
+ Tool
+ Harness
+ State
+ Memory
+ Runtime
+ Identity
+ Policy
+ Verification
+ Eval
~~~

이 구성요소가 함께 실제 행동을 만든다.

## Model은 계속 바뀐다

Model Capability는 빠르게 좋아진다.

어제 필요했던 Planner가 내일은 불필요할 수 있다.

Context Compression을 위해 만든 복잡한 Rule이 더 큰 Context Window와 더 좋은 Model에서는 방해가 될 수도 있다.

그래서 Harness를 고정된 진리처럼 만들면 안 된다.

Harness는 현재 Model과 Task Distribution에 대한 Engineering Hypothesis다.

측정하고, 줄이고, 다시 만든다.

## 하지만 없어지지 않는 질문이 있다

Model이 아무리 좋아져도 다음 질문은 남는다.

~~~text
누가 행동하는가?
어떤 Tool을 사용할 수 있는가?
어떤 State가 Canonical한가?
이미 실행한 Side Effect는 무엇인가?
Credential은 어디에 있는가?
Runtime은 어디까지 접근할 수 있는가?
완료를 누가 판정하는가?
실패 후 어떻게 복구하는가?
~~~

Model Capability가 높아질수록 일부 Control은 단순해질 수 있다.

하지만 Responsibility Boundary 자체가 사라지는 것은 아니다.

## Agent State Plane이 남기는 것

이 책에서 가장 중요한 synthesis 중 하나는 Agent State Plane이었다.

~~~text
Context
≠ Durable State
~~~

Model이 현재 Context에서 잊어도 시스템이 Goal과 Progress를 잃어서는 안 된다.

Runtime이 사라져도 이미 실행한 Action과 Artifact를 잃어서는 안 된다.

Memory가 오래됐다고 External Source보다 우선해서는 안 된다.

Agent가 오래 일할수록 Intelligence만큼 State Discipline이 중요해진다.

## Security는 Model Trust의 문제가 아니다

좋은 Agent Security를 "모델이 공격을 잘 거절하는가"만으로 정의하지 않았다.

~~~text
Identity
Authorization
Credential
Containment
Approval
Verification
~~~

을 분리했다.

이 구조의 목적은 단순하다.

Model이 잘못 판단해도 피해 범위를 줄인다.

더 강한 Model은 유용하다.

하지만 더 강한 Boundary도 여전히 필요하다.

## Completion은 말이 아니라 Evidence다

Agent가 "완료했습니다"라고 말하는 것은 Completion Claim이다.

실제 Completion은 다른 문제다.

~~~text
Claim
→ Artifact
→ External State
→ Verification
→ Acceptance
~~~

가능하면 Deterministic Evidence를 사용한다.

이 원칙은 Coding Agent뿐 아니라 업무 Agent에도 같다.

## Multi-Agent보다 먼저 Boundary

Agent를 여러 개 만드는 것은 쉽다.

좋은 Collaboration Boundary를 만드는 것은 어렵다.

Single-Agent의 State, Tool, Identity, Verification이 불안정한 상태에서 Multi-Agent를 추가하면 Failure Surface가 커질 수 있다.

Agent 수는 Architecture 품질의 지표가 아니다.

## Agent Engineering에서 Software Factory로

이 책은 하나의 Agent 실행에 집중했다.

~~~text
Agent State Plane
= execution continuity
~~~

조직에서 Agent를 실제 생산 시스템으로 운영하기 시작하면 상위 문제가 생긴다.

~~~text
Which work should run?
Which worker owns it?
What is accepted?
What is delivered?
What happens after failure?
~~~

이것은 Software Factory Control Plane의 문제다.

~~~text
Software Factory Control Plane
= work-system continuity
~~~

한 Agent를 신뢰할 수 있게 만드는 것과 여러 Agent Worker를 생산 시스템으로 운영하는 것은 연결되지만 같은 문제는 아니다.

## 오래 남을 원칙

제품 이름과 Protocol Version은 바뀐다.

Model도 바뀐다.

하지만 다음 질문은 오래 남을 가능성이 높다.

~~~text
What is the goal?
What state is durable?
What context is relevant now?
What actions are possible?
Who is authorized?
Where can it execute?
What evidence proves completion?
How does it recover?
How do we know a change improved it?
~~~

Agent Engineering은 이 질문에 대한 Software Engineering이다.

## 마지막 원칙

Agent에게 일을 맡긴다는 것은 Model을 완전히 신뢰한다는 뜻이 아니다.

오히려 반대에 가깝다.

불확실한 판단을 하는 Component를 실제 시스템 안에 넣되:

- 권한을 제한하고
- 상태를 보존하고
- 실행을 격리하고
- 결과를 검증하고
- 실패를 복구하고
- 개선을 측정한다.

그래서 이 책의 마지막 문장은 다음으로 남긴다.

> **좋은 Agent 시스템은 모델을 무조건 믿는 시스템이 아니라, 모델을 덜 믿어도 실제 일을 맡길 수 있는 시스템이다.**
