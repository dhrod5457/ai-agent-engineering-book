# 21장. Harness Ablation과 Debt

에이전트가 실패하자 계획을 세우는 기능을 추가했다. 다른 실패가 생기자 평가 기능을 붙였고, 모델에 전달할 정보가 길어지자 이를 압축하는 기능을 넣었다. 이전 실수를 반복하자 메모리도 추가했다. 몇 달 뒤 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)에는 많은 구성 요소가 있지만 어떤 것이 필요한지 아무도 모른다. 에이전트 하네스에도 유지보수 부담이 생긴다.

## Harness Component는 가설이다

계획기(Planner: 계획을 세우는 구성 요소) 하나를 예로 들어보자. 계획기를 추가한다는 것은 사실 다음 가설을 넣는 것이다.

> 작업을 시작하기 전에 세부 단계로 나누면 이 작업 분포에서 성공률이 높아진다.

평가기(Evaluator: 결과를 평가하는 구성 요소):

> 독립된 평가가 스스로 검증하는 것보다 오류를 더 잘 잡는다.

메모리:

> 과거 교훈의 재사용이 오래되거나 오염된 정보를 쓰는 위험보다 더 큰 이득을 준다.

하위 에이전트:

> 컨텍스트를 분리해 얻는 이득이 협업 조율 비용보다 크다.

이 가설은 측정돼야 한다.

## Minimal Baseline

제거 비교 실험(Ablation: 구성 요소를 빼고 효과를 비교하는 실험)을 하려면 단순한 비교 기준이 필요하다.

예:

~~~text
Model
+ essential instruction
+ required tools
+ deterministic verifier
~~~

여기에 구성 요소를 하나씩 추가한다. 비교 기준 자체가 복잡하면 어떤 모델의 약점을 보완하는 보조 장치가 기여했는지 알기 어렵다.

## Component Inventory

현재 하네스에 무엇이 들어 있는지 목록화한다.

예:

- system instruction
- context selector
- planner
- compaction
- memory
- tool router
- retry
- evaluator
- subagent
- progress artifact
- completion verifier

각 구성 요소에 존재 이유를 연결한다.

## Harness Component Record

예:

~~~text
component: planner-v3
introduced_for: long_horizon_omission
expected_effect: improve task decomposition
eval_cases:
- LH-12
- LH-33
introduced_model: model-A
last_verified_model: model-C
owner: agent-platform
~~~

이 기록이 있으면 모델 교체 때 감사하기 쉽다.

## Ablation

기본 방법은 간단하다.

~~~text
Baseline
      ↓
Remove One Component
      ↓
Run Same Eval Set
      ↓
Compare
~~~

하지만 에이전트는 같은 입력에도 결과가 달라질 수 있는하다. 한 번의 실행으로 결론 내리면 위험하다.

## Repeated Trials

Anthropic이 공개한 Automated Alignment Researchers harness ablation에서는 일부 조건을 한 번씩 비교했고, 저자들은 반복 조건에서 관찰한 실행마다 달라지는 결과의 편차가 조건 간 차이보다 클 수 있어 결과를 확정적 결론이 아닌 시사점으로 해석한다고 밝힌다. 이 사례를 일반 법칙으로 확장하지 않고, 오히려 반복 실험이 필요한 근거로 사용한다.

따라서:

~~~text
Baseline
→ repeated trials

Ablated
→ repeated trials

Compare distribution
~~~

이 필요하다. 한 번 Pass/Fail로 구성 요소 가치를 판단하지 않는다.

## Pin the Environment

제거 비교 실험 중 다른 변수를 바꾸면 해석이 어려워진다. 가능하면 다음을 고정한다.

- 모델 버전
- Tool Version
- 실행 환경
- 평가 데이터 모음
- 채점기
- 정책
- Resource Limit

한 번에 하나의 주요 변수를 바꾼다.

## Capability Slice

평균 점수만으로는 구성 요소가 어떤 작업에 도움이 되는지 드러나지 않을 수 있다.

예:

~~~text
Planner:
+ long_horizon
- short_task_latency
0 security

Memory:
+ repeated_task
- poisoning_resilience
+ context_efficiency
~~~

구성 요소마다 다른 얻는 점과 감수할 점이 있다. 그래서 Capability Slice를 본다.

## Safety Slice

하네스 구성 요소를 제거하면 Quality는 비슷하지만 보안이 나빠질 수 있다.

예:

~~~text
remove tool filter
→ success +1%
→ unauthorized action +8%
~~~

이 구성 요소는 단순 성공 기준으로 제거하면 안 된다. Ablation Metric에 Safety를 포함한다.

## Cost와 Latency

평가기가 성공을 조금 높이지만 모든 차례에 추가 모델 호출을 만들 수 있다.

예:

~~~text
Success:
+2%

Latency:
+35%

Cost:
+40%
~~~

이득이 모든 작업에 필요한지 판단해야 한다. Conditional Component가 더 적합할 수 있다.

~~~text
Evaluator
→ only high-risk / uncertain tasks
~~~

## Interaction Effect

구성 요소는 서로 독립적이지 않을 수 있다.

예:

~~~text
Memory alone:
neutral

Memory + retrieval filter:
positive
~~~

또는:

~~~text
Planner alone:
negative

Planner + long-horizon task:
positive
~~~

필요하면 두 요소가 함께 작용할 때의 효과(2-way Interaction)까지 살펴본다. 가능한 모든 조합을 빠짐없이 실험할 필요는 없지만, 중요한 의존 관계는 확인해야 한다.

## Model Upgrade는 Audit Trigger다

하네스는 모델의 능력에 대한 가정을 포함한다. 모델이 좋아지면 오래된 모델의 약점을 보완하는 보조 장치가 필요 없을 수 있다.

추천 절차:

~~~text
New Model
  ↓
Old Harness
  ↓
Minimal Baseline
  ↓
Restore Components One by One
  ↓
Measure Marginal Value
  ↓
Keep Load-bearing Components
~~~

이 과정은 단순 Cost Cutting이 아니다. 오래된 규칙이 새로운 모델의 좋은 행동을 방해하는 것을 막는다.

## Stable Interface와 Mutable Harness

Anthropic Managed Agents 사례에서 중요한 관점 중 하나는 외부 인터페이스와 내부 하네스를 분리하는 것이다.

~~~text
Stable:
session / tool / runtime contract

Mutable:
planner / context strategy / model adaptation
~~~

이렇게 하면 하네스를 자주 실험해도 Application Integration 전체를 흔들지 않을 수 있다.

## Harness Debt

이 책에서는 다음 상태를 Harness Debt라고 부른다. 외부 표준 용어는 아니다.

증상:

- 왜 존재하는지 모르는 규칙
- 과거 Model Workaround
- 중복 계획기
- 중복 평가기
- 사용되지 않는 State Field
- obsolete Tool Wrapper
- 필요성 불명의 메모리
- 과도한 하위 에이전트

일반 Software의 Dead Code와 비슷하다.

## Debt Review

정기적으로 구성 요소를 묻는다.

~~~text
왜 존재하는가?
어떤 Failure를 막는가?
어떤 Eval이 증명하는가?
현재 Model에서도 필요한가?
Security Impact는 무엇인가?
Owner는 누구인가?
제거 Candidate인가?
~~~

답을 못하면 Audit Candidate다.

## 작은 예: Planner 제거

현재 하네스:

~~~text
Planner
→ Executor
→ Evaluator
~~~

New Model에서 실험:

~~~text
A:
Planner + Executor + Evaluator

B:
Executor + Evaluator
~~~

반복 실행에서 성공 차이는 거의 없는데 계획기가 응답 지연 시간과 비용을 일관되게 늘린다고 하자. 이 경우 계획기가 현재 모델과 작업 분포에서 꼭 필요한 구성 요소인지 다시 검토할 수 있다. 다만 평가 데이터 모음과 실행마다 달라지는 결과의 편차를 함께 확인해야 한다. 한 번의 결과만으로 제거하지 않는다.

## Component가 해결한 Failure를 기록한다

좋은 Harness Change는 다음 세트를 가진다.

~~~text
Failure
→ Component
→ Eval Case
→ Improvement Evidence
~~~

예:

~~~text
Failure:
premature completion

Component:
progress invariant

Eval:
LH-12, LH-33

Evidence:
failure rate reduced
~~~

이렇게 연결하면 나중에 구성 요소를 제거할 때 영향도 확인할 수 있다.

## 이 장에서 가져갈 것

하네스는 시간이 지나며 자연스럽게 복잡해진다. 복잡성을 피할 수는 없지만 근거 없는 모델의 약점을 보완하는 보조 장치를 계속 유지할 필요도 없다.

핵심 원칙:

~~~text
Harness Component
= Engineering Hypothesis
~~~

그리고:

~~~text
Add
→ Measure
→ Re-evaluate
→ Remove if no longer load-bearing
~~~

Part VI에서는 실행 추적 기록(Trace)에서 시작해 평가, 개발 과정에 통합한 지속적 평가, 하네스 구성 요소의 제거 비교 실험까지 Improvement Loop를 완성했다. 이제 마지막 Part로 넘어간다. 단일 에이전트가 안정된 뒤 언제 여러 에이전트의 협업을 도입할 것인가. Agent-as-Tool과 작업 인계는 무엇이 다른가. 원격 에이전트와 A2A는 어디에 위치하는가.

## 주요 근거

- Anthropic, Harness Design for Long-running Application Development
- Anthropic, Managed Agents
- Anthropic, Automated Alignment Researchers
- AuditBench
- research/topics/22-harness-ablation-and-minimalism.md
- research/targeted/21-harness-ablation.md
