# Epilogue. Agent를 더 똑똑하게 만드는 것보다 시스템을 더 믿을 수 있게 만든다

이 책은 같은 모델을 사용해도 에이전트가 실제로 할 수 있는 일은 달라질 수 있다는 이야기로 시작했다. 마지막까지 살펴보면 그 이유가 분명해진다. 에이전트는 모델 하나로 이루어지지 않기 때문이다.

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

이 구성요소가 함께 행동을 만든다.

## Model은 계속 바뀐다

모델의 능력은 빠르게 좋아진다. 어제 필요했던 계획기(Planner: 계획을 세우는 구성 요소)가 내일은 불필요할 수 있다. Context Compression을 위해 만든 복잡한 규칙이 더 큰 컨텍스트 윈도(Context Window: 모델이 한 번에 입력받을 수 있는 정보의 범위)와 더 좋은 모델에서는 방해가 될 수도 있다. 그래서 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)를 고정된 진리처럼 만들면 안 된다. 하네스는 현재 모델과 작업 분포에서 무엇이 효과가 있을지에 대한 설계 가설이다. 측정하고, 줄이고, 다시 만든다.

## 하지만 없어지지 않는 질문이 있다

모델이 아무리 좋아져도 다음 질문은 남는다.

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

모델의 능력이 높아질수록 일부 통제는 단순해질 수 있다. 하지만 책임 경계 자체가 사라지는 것은 아니다.

## Agent State Plane이 남기는 것

이 책에서 가장 중요한 설명용 개념 중 하나는 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)이었다.

~~~text
Context
≠ Durable State
~~~

모델이 현재 컨텍스트(Context: 모델에 전달하는 정보)에서 잊어도 시스템이 목표와 진행 상황을 잃어서는 안 된다. 실행 환경이 사라져도 이미 수행한 행동의 기록과 만들어 낸 산출물을 잃어서는 안 된다. 메모리가 오래됐다고 외부 원본보다 우선해서는 안 된다. 에이전트가 오래 일할수록 지능만큼이나 상태를 일관되게 관리하는 일이 중요해진다.

## Security는 Model Trust의 문제가 아니다

좋은 에이전트 보안을 "모델이 공격을 잘 거절하는가"만으로 정의하지 않았다.

~~~text
Identity
Authorization
Credential
Containment
Approval
Verification
~~~

을 분리했다. 이 구조의 목적은 단순하다. 모델이 잘못 판단해도 피해 범위를 줄인다. 더 강한 모델은 유용하지만, 실제 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)를 다루는 경계와 검증 책임까지 자동으로 사라지지는 않는다.

## Completion은 말이 아니라 Evidence다

에이전트가 "완료했습니다"라고 말하는 것은 완료했다는 주장이다. 완료는 다른 문제다.

~~~text
Claim
→ Artifact
→ External State
→ Verification
→ Acceptance
~~~

가능하면 정해진 규칙으로 확인할 수 있는 근거를 사용한다. 이 원칙은 코드 작업 에이전트뿐 아니라 업무 에이전트에도 같다.

## Agent Engineering에서 Software Factory로

이 책은 하나의 에이전트 실행에 집중했다.

~~~text
Agent State Plane
= execution continuity
~~~

조직에서 에이전트를 생산 시스템으로 운영하기 시작하면 상위 문제가 생긴다.

~~~text
Which work should run?
Which worker owns it?
What is accepted?
What is delivered?
What happens after failure?
~~~

이것은 소프트웨어 팩토리의 제어 계층의 문제다.

~~~text
Software Factory Control Plane
= work-system continuity
~~~

한 에이전트를 신뢰할 수 있게 만드는 것과 여러 Agent Worker를 생산 시스템으로 운영하는 것은 연결되지만 같은 문제는 아니다.

## 오래 남을 원칙

제품 이름과 Protocol Version은 바뀐다. 모델도 바뀐다. 하지만 다음 질문은 오래 남을 가능성이 높다.

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

에이전트 엔지니어링은 이 질문에 대한 Software Engineering이다.

## 마지막 원칙

에이전트에게 일을 맡긴다는 것은 모델을 완전히 신뢰한다는 뜻이 아니다.

불확실한 판단을 하는 구성 요소를 운영 시스템 안에 넣되:

- 권한을 제한하고
- 상태를 보존하고
- 실행을 격리하고
- 결과를 검증하고
- 실패를 복구하고
- 개선을 측정한다.

그래서 이 책의 마지막 문장은 다음으로 남긴다.

> **좋은 에이전트 시스템은 모델을 무조건 믿는 시스템이 아니라, 모델을 덜 믿어도 실제 일을 맡길 수 있는 시스템이다.**
