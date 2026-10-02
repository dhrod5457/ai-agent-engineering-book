# Harness Ablation and Minimalism

기준일: 2026-10-02

## 문제

Agent가 실패할 때마다 Harness에 새 rule, planner, verifier, memory, subagent를 추가하기 쉽다.

시간이 지나면:

~~~text
More Failure
→ More Scaffold
→ More Complexity
→ More Context
→ More Hidden Interaction
→ Harder Evaluation
~~~

이 된다.

강한 model이 출시되어도 과거 scaffold가 그대로 남으면 오히려 성능을 제한할 수 있다.

## Harness는 가설의 집합이다

각 component는 다음 가설을 구현한다.

예:

~~~text
Planner
= upfront decomposition이 success rate를 높인다

Progress File
= cross-session continuity를 높인다

Evaluator Agent
= self-verification보다 독립 평가가 낫다

Memory
= past lesson reuse가 future task를 개선한다

Subagent
= context isolation이 coordination cost보다 이득이다
~~~

이 가설은 측정돼야 한다.

## Component Inventory

Harness component를 명시적으로 목록화한다.

예:

- system instruction
- context selector
- planner
- task list artifact
- compaction
- memory
- tool router
- permission layer
- retry
- evaluator
- subagent
- progress checkpoint
- completion verifier

component가 많아질수록 implicit dependency가 늘어난다.

## Ablation

기본 방법:

~~~text
Baseline Harness
      ↓
Remove / Disable One Component
      ↓
Run Same Eval Set
      ↓
Compare:
- success
- safety
- cost
- latency
- intervention
- reliability
      ↓
Keep / Remove / Redesign
~~~

한 번에 여러 component를 바꾸면 원인을 알기 어렵다.

## Model Upgrade Audit

Anthropic은 long-running harness 연구에서 model capability가 변하면 old scaffolding assumption도 재검증해야 함을 보여준다.

추천 절차:

~~~text
New Model
  ↓
Run Old Harness
  ↓
Minimal Baseline
  ↓
Component-by-component Restore
  ↓
Measure Marginal Value
  ↓
Keep Only Load-bearing Components
~~~

## Minimal Baseline

비교 기준에는 가능한 단순한 Agent가 필요하다.

~~~text
Model
+ essential instruction
+ required tools
+ deterministic verifier
~~~

여기에 component를 추가했을 때 실제 이득을 측정한다.

baseline 자체가 복잡하면 scaffold의 기여를 알 수 없다.

## Capability별 효과

하나의 평균 점수만 보면 component가 특정 capability를 개선하고 다른 capability를 망치는 것을 놓칠 수 있다.

예:

~~~text
Planner
+ long-horizon completion
- short task latency

Memory
+ repeated task efficiency
- poisoning risk

Evaluator
+ quality
- cost / latency
~~~

그래서 eval slice를 나눈다.

## Security Ablation

Harness component 제거가 quality뿐 아니라 security boundary를 약화할 수 있다.

따라서 ablation metric에는 반드시:

- unsafe action
- permission violation
- prompt injection resilience
- memory poisoning
- credential exposure

를 포함한다.

## Interaction Effect

Ablation은 단일 component 독립 효과만 보는 것이 아니다.

예:

~~~text
Memory alone: neutral
Memory + Retrieval Filter: positive

Planner alone: negative
Planner + Long Task: positive
~~~

필요하면 2-way interaction까지 본다.

## Scaffold Debt

오래된 Harness component는 Instruction Debt와 비슷한 부채가 된다.

증상:

- 왜 존재하는지 아무도 모름
- 특정 model version workaround
- 중복 verifier
- conflicting instruction
- unused state field
- obsolete tool wrapper

정기적으로 제거 후보를 만든다.

## Promotion Rule

Harness component는 다음을 만족할 때만 core에 남긴다.

- measurable benefit
- known failure class를 해결
- regression test 존재
- security impact 이해
- maintenance owner 존재

## 책에 반영할 핵심 원칙

1. Harness component는 검증 가능한 가설이다.
2. Scaffold를 추가한 이유와 해결할 failure를 기록한다.
3. Minimal baseline과 비교한다.
4. Model upgrade마다 harness ablation을 수행한다.
5. 평균 점수뿐 아니라 capability/security slice를 본다.
6. 더 복잡한 Harness가 항상 더 좋은 Agent를 만들지 않는다.
7. Harness에도 debt와 dead code가 존재한다.
8. load-bearing component만 core에 남긴다.

## 주요 근거

- Anthropic Harness Design for Long-running Application Development
- Anthropic Effective Harnesses for Long-running Agents
- OpenAI Agent Improvement Loop
- Agent Eval / Trace Grading practices
