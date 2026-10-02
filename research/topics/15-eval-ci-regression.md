# Eval CI and Regression

기준일: 2026-10-02

## 문제

Agent system은 다음 중 하나만 바뀌어도 behavior가 달라질 수 있다.

- model
- instruction
- tool description
- tool implementation
- harness
- context retrieval
- memory
- sandbox
- permission policy
- dependency
- environment image

따라서 Agent Eval을 일회성 benchmark로 두면 운영 품질을 유지하기 어렵다.

## Agent Eval을 CI로 올린다

기본 구조:

~~~text
Production Trace / Failure
        ↓
Triage
        ↓
Reusable Eval Case
        ↓
Regression Dataset
        ↓
Candidate Harness Change
        ↓
Offline Eval
        ↓
Compare
        ↓
Shadow / Canary
        ↓
Promote
~~~

## Trace → Feedback → Eval

OpenAI의 Agent Improvement Loop 자료는 다음 flywheel을 제시한다.

~~~text
Trace
→ Human / Model Feedback
→ Eval
→ Harness Change Candidate
→ Re-run
~~~

핵심은 한 번의 feedback을 재사용 가능한 test case로 승격하는 것이다.

## Micro Eval과 Macro Eval

### Micro Eval

개별 failure를 재현한다.

예:
- wrong tool
- missing argument
- stale state
- bad handoff
- unsafe action

### Macro Eval

많은 trace에서 recurring pattern을 본다.

예:
- 특정 specialist가 반복적으로 늦게 호출됨
- 같은 policy를 여러 run에서 놓침
- 특정 class에서 review가 과도하게 발생

개별 pass/fail만으로 system-level 구조 문제를 놓칠 수 있다.

## Eval Gate 종류

### Pull Request Gate
빠르고 deterministic한 작은 regression set.

### Nightly
비용이 큰 multi-turn set, repeated trial, security set.

### Release Gate
candidate model/harness 전체 비교.

### Production Shadow
실제 traffic과 유사한 input에서 side effect 없이 비교.

## Dataset Layer

추천 구조:

~~~text
evals/
  capability/
  regression/
  security/
  long-horizon/
  tool-routing/
  recovery/
  cost-latency/
~~~

각 case metadata 후보:

- id
- source
- failure class
- environment version
- required tools
- expected outcome
- grader
- risk
- repeat count
- introduced_at
- fixed_by
- owner

## Baseline Versioning

Agent Eval 결과는 최소 다음 tuple과 함께 저장해야 한다.

~~~text
AgentVersion = (
  model,
  instruction,
  harness,
  tools,
  runtime,
  environment,
  policy,
  memory/config,
  grader
)
~~~

model 이름만 남기면 재현이 어렵다.

## Nondeterminism

Agent regression은 한 번의 실행으로 판단하기 어려울 수 있다.

대응:

- repeated trials
- confidence interval
- pass^k / pass@k 목적 구분
- deterministic outcome grader
- random seed where applicable
- infra error separate accounting

## Promotion Rule

단순 평균 점수 상승만으로 promotion하지 않는다.

예:

~~~text
must_not_regress:
- safety
- critical task
- data integrity

optimize:
- task success
- latency
- cost
- human intervention
~~~

risk-weighted gate가 필요하다.

## Model Upgrade Audit

새 model은 기존 harness와 상호작용이 달라질 수 있다.

따라서:

~~~text
New Model
→ Existing Harness Eval
→ Scaffold Ablation
→ Tool Re-tuning
→ Security Regression
→ Long-horizon Regression
→ Promote
~~~

가 필요하다.

## Production Failure의 승격

좋은 운영 규칙:

> 같은 종류의 실패를 두 번 사람 기억에만 의존하지 않는다.

incident/review correction이 의미 있으면 regression case로 만든다.

## Eval CI의 목표

Eval CI는 Agent를 deterministic하게 만드는 것이 아니다.

목표는:

- 변화의 영향을 측정
- known failure 재발 방지
- risk regression 차단
- improvement evidence 축적
- model/harness dependency 가시화

이다.

## 주요 근거

- OpenAI Agent Evals / Trace Grading
- OpenAI Agent Improvement Loop
- OpenAI Macro Evals
- Anthropic Demystifying Evals
- Anthropic Infrastructure Noise
- tau-bench repeated evaluation
