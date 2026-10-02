# 21장. Harness Ablation과 Debt

Agent가 실패했다.

Planner를 추가했다.

다른 Failure가 생겼다.

Evaluator를 추가했다.

Context가 길어졌다.

Compaction을 추가했다.

이전 실수를 반복해서 Memory를 추가했다.

몇 달 뒤 Harness에는 많은 Component가 있지만 어떤 것이 필요한지 아무도 모른다.

Agent Harness에도 Debt가 생긴다.

## Harness Component는 가설이다

Planner 하나를 예로 들어보자.

Planner를 추가한다는 것은 사실 다음 가설을 넣는 것이다.

> upfront decomposition이 이 Task Distribution에서 Success를 높인다.

Evaluator:

> independent evaluation이 self-verification보다 Error를 더 잘 잡는다.

Memory:

> past lesson reuse가 stale/poisoning risk보다 더 큰 이득을 준다.

Subagent:

> context isolation benefit이 coordination cost보다 크다.

이 가설은 측정돼야 한다.

## Minimal Baseline

Ablation을 하려면 단순한 Baseline이 필요하다.

예:

~~~text
Model
+ essential instruction
+ required tools
+ deterministic verifier
~~~

여기에 Component를 하나씩 추가한다.

Baseline 자체가 복잡하면 어떤 Scaffold가 기여했는지 알기 어렵다.

## Component Inventory

현재 Harness에 무엇이 들어 있는지 목록화한다.

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

각 Component에 존재 이유를 연결한다.

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

이 Record가 있으면 Model Upgrade 때 Audit하기 쉽다.

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

하지만 Agent는 Nondeterministic하다.

한 번의 실행으로 결론 내리면 위험하다.

## Repeated Trials

Anthropic의 Automated Alignment Researchers 관련 Harness Ablation 사례에서도 Run-to-run variance가 Component 차이보다 클 수 있음을 지적한다.

따라서:

~~~text
Baseline
→ repeated trials

Ablated
→ repeated trials

Compare distribution
~~~

이 필요하다.

한 번 Pass/Fail로 Component 가치를 판단하지 않는다.

## Pin the Environment

Ablation 중 다른 변수를 바꾸면 해석이 어려워진다.

가능하면 다음을 고정한다.

- Model Version
- Tool Version
- Runtime
- Dataset
- Grader
- Policy
- Resource Limit

한 번에 하나의 주요 변수를 바꾼다.

## Capability Slice

평균 Score만 보면 Component 효과가 숨는다.

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

Component마다 다른 Trade-off가 있다.

그래서 Capability Slice를 본다.

## Safety Slice

Harness Component를 제거하면 Quality는 비슷하지만 Security가 나빠질 수 있다.

예:

~~~text
remove tool filter
→ success +1%
→ unauthorized action +8%
~~~

이 Component는 단순 Success 기준으로 제거하면 안 된다.

Ablation Metric에 Safety를 포함한다.

## Cost와 Latency

Evaluator가 Success를 조금 높이지만 모든 Turn에 추가 Model Call을 만들 수 있다.

예:

~~~text
Success:
+2%

Latency:
+35%

Cost:
+40%
~~~

이득이 모든 Task에 필요한지 판단해야 한다.

Conditional Component가 더 적합할 수 있다.

~~~text
Evaluator
→ only high-risk / uncertain tasks
~~~

## Interaction Effect

Component는 서로 독립적이지 않을 수 있다.

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

필요하면 2-way Interaction까지 본다.

모든 Combination을 Exhaustive하게 실험할 필요는 없지만 중요한 Dependency는 확인해야 한다.

## Model Upgrade는 Audit Trigger다

Harness는 Model Capability에 대한 가정을 포함한다.

Model이 좋아지면 오래된 Scaffold가 필요 없을 수 있다.

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

이 과정은 단순 Cost Cutting이 아니다.

오래된 Rule이 새로운 Model의 좋은 행동을 방해하는 것을 막는다.

## Stable Interface와 Mutable Harness

Anthropic Managed Agents 사례에서 중요한 관점 중 하나는 외부 Interface와 내부 Harness를 분리하는 것이다.

~~~text
Stable:
session / tool / runtime contract

Mutable:
planner / context strategy / model adaptation
~~~

이렇게 하면 Harness를 자주 실험해도 Application Integration 전체를 흔들지 않을 수 있다.

## Harness Debt

이 책에서는 다음 상태를 Harness Debt라고 부른다.

외부 표준 용어는 아니다.

증상:

- 왜 존재하는지 모르는 Rule
- 과거 Model Workaround
- 중복 Planner
- 중복 Evaluator
- 사용되지 않는 State Field
- obsolete Tool Wrapper
- 필요성 불명의 Memory
- 과도한 Subagent

일반 Software의 Dead Code와 비슷하다.

## Debt Review

정기적으로 Component를 묻는다.

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

현재 Harness:

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

각각 50회 반복했다고 하자.

결과:

~~~text
Long-horizon Success
A 82%
B 83%

Latency
A +28%

Cost
A +25%
~~~

이 조건이라면 Planner가 Load-bearing Component인지 의심할 수 있다.

물론 Dataset과 Variance를 확인해야 한다.

한 번의 결과만으로 제거하지 않는다.

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

이렇게 연결하면 나중에 Component를 제거할 때 영향도 확인할 수 있다.

## 이 장에서 가져갈 것

Harness는 시간이 지나며 자연스럽게 복잡해진다.

복잡성을 피할 수는 없지만 근거 없는 Scaffold를 계속 유지할 필요도 없다.

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

Part VI에서는 Trace에서 시작해 Eval, Eval CI, Harness Ablation까지 Improvement Loop를 완성했다.

이제 마지막 Part로 넘어간다.

Single-Agent가 안정된 뒤 언제 Multi-Agent를 도입할 것인가. Agent-as-Tool과 Handoff는 무엇이 다른가. Remote Agent와 A2A는 어디에 위치하는가.

## 주요 근거

- Anthropic, Harness Design for Long-running Application Development
- Anthropic, Managed Agents
- Anthropic, Automated Alignment Researchers
- AuditBench
- research/topics/22-harness-ablation-and-minimalism.md
- research/targeted/21-harness-ablation.md
