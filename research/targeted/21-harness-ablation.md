# Targeted Research — Harness Ablation

기준일: 2026-10-02
대상: 21장 Harness Ablation과 Debt

## 새로 확보한 근거

### Anthropic Managed Agents
- Source: https://www.anthropic.com/engineering/managed-agents
- 핵심:
  - Harness는 model이 못한다고 가정한 부분을 scaffold로 보완한다.
  - Model이 좋아지면 그 가정이 stale해질 수 있다.
  - stable interface와 mutable harness를 분리해야 한다.

### Automated Alignment Researchers — Harness Ablation
- Source: https://alignment.anthropic.com/2026/automated-alignment-researchers/
- 핵심:
  - harness component를 하나씩 제거하는 ablation 수행
  - shared finding forum 제거, internet 제거, cached literature review 유지 등 component별 효과를 비교
  - 단일 run 간 변동성이 component 차이보다 클 수 있어 반복 실험 필요성을 명시
- 의미:
  - Harness ablation은 실제 운영/연구 system에서도 유효한 방법
  - "한 번의 on/off 결과"로 component 가치를 확정하면 안 됨

### AuditBench
- Source: https://alignment.anthropic.com/2026/auditbench/
- 핵심:
  - scaffolded black-box tool이 default agent보다 높은 성공률을 보이는 경우가 있음
  - 동시에 tool/scaffold 효과가 task/model training method에 따라 다름
- 의미:
  - Harness component 효과는 capability-specific이며 universal하지 않다.

## Ablation 방법 보강

기존:
~~~text
Remove One Component
→ Eval
→ Keep / Remove
~~~

보강:
~~~text
Define Failure Hypothesis
        ↓
Pin Model / Tools / Runtime / Eval
        ↓
Baseline Repeated Trials
        ↓
Remove One Component
        ↓
Repeated Trials
        ↓
Compare Capability + Safety + Cost
        ↓
Estimate Variance
        ↓
Keep / Remove / Redesign
~~~

## 새 핵심 원칙

1. Harness ablation에는 repeated trials가 필요하다.
2. Run-to-run variance가 component delta보다 클 수 있다.
3. component value는 평균 점수 하나가 아니라 capability slice별로 본다.
4. stable interface와 mutable scaffold를 분리한다.
5. Model upgrade는 scaffold audit trigger다.
6. Harness component에는 "왜 존재하는가 / 어떤 failure를 막는가 / 어떤 eval이 증명하는가"를 기록한다.

## Harness Component Record 후보

~~~text
component
introduced_for
expected_effect
risk
eval_cases
owner
introduced_model
last_verified_model
removal_candidate
~~~

이 metadata를 Harness Debt 관리에 활용한다.
