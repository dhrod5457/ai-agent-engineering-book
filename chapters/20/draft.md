# 20장. Eval을 CI로 만든다

에이전트가 운영 환경에서 같은 실수를 두 번 했다. 첫 번째에도, 두 번째에도 운영자가 고쳤다. 이 시스템은 기록을 남겼지만, 그 기록으로 같은 실수를 줄이는 개선 과정은 갖추지 못했다. 에이전트 개선을 사람의 기억에 의존해 운영하기는 어렵다. 의미 있는 실패를 다시 실행 가능한 평가 사례로 승격해야 한다. 이 장에서 말하는 개발 과정에 통합한 지속적 평가는 배포 자동 처리 절차 전체를 설명하려는 것이 아니다. 에이전트 행동 변경에 대한 기존 기능의 악화를 막는 검증 단계를 개발 과정에 넣는 데 초점을 둔다.

## Eval은 Release 전 행사만이 아니다

일회성 성능 비교 평가는 현재 상태를 확인하는 데 도움이 된다. 운영 에이전트는 계속 바뀐다.

- 모델 교체
- 도구 설명 변경
- 컨텍스트 구성 정책 변경
- 메모리 추가
- 재시도 변경
- Sandbox Policy 변경
- 채점기 변경

그래서 평가도 Development Lifecycle 안에 들어와야 한다.

~~~text
Change
→ Eval
→ Compare
→ Promote
~~~

## 운영 실패를 Regression으로 만든다

좋은 Feedback Loop는 다음과 같다.

~~~text
Production Trace
      ↓
Triage
      ↓
Failure Class
      ↓
Reusable Eval Case
      ↓
Regression Dataset
      ↓
Candidate Fix
      ↓
Re-run
~~~

같은 실패를 사람 기억에만 남기지 않는다.

## Failure Triage

모든 운영 실패를 평가 사례로 만들 필요는 없다. 다음 질문을 본다.

- 반복 가능성이 있는가.
- 중요도가 높은가.
- 구조적 실패인가.
- 재현 가능한가.
- 회귀(Regression: 변경 뒤 기존 기능이 나빠지는 회귀)를 막을 가치가 있는가.

예:

~~~text
one-time external outage
→ maybe operational incident only

stale-state bug
→ regression case

unsafe tool routing
→ security regression case
~~~

## Eval Dataset을 나눈다

하나의 거대한 평가 데이터 모음보다 목적별로 나눌 수 있다.

~~~text
evals/
  capability/
  regression/
  security/
  long_horizon/
  tool_routing/
  recovery/
  cost_latency/
~~~

각 Suite는 다른 Cadence로 실행할 수 있다.

## PR Gate

모든 Pull Request마다 전체 Agent Benchmark를 돌리면 비싸고 느리다. PR Gate에는 빠르고 중요한 사례를 둔다.

예:

- Schema Validation
- Tool Contract Regression
- 핵심 20개 Agent Case
- Security Critical Case
- deterministic verifier

목표는 빠른 회귀 차단이다.

## Nightly

비용이 큰 평가는 Nightly로 돌릴 수 있다.

예:

- 100+ multi-turn cases
- 반복 실험
- long-horizon
- browser environment
- security attack set

결과를 Trend로 본다.

## Release Gate

Model/Harness Release 전에는 더 넓게 검증한다.

예:

~~~text
Candidate Version
vs
Current Production Version
~~~

비교:

- 성공
- Safety
- 비용
- 응답 지연 시간
- Intervention
- 복구

특히 Critical Capability의 회귀를 막는다.

## Shadow

운영 Traffic과 유사한 입력을 Candidate Agent에 넣되 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)는 실행하지 않는 방식이다.

~~~text
Production Input
   ├─ Current Agent → real action
   └─ Candidate Agent → shadow only
~~~

운영 분포에서 Behavior를 비교할 수 있다.

## Canary

일부 Low-risk Traffic에 후보를 적용한다. 문제가 없으면 확대한다. 에이전트 시스템은 같은 입력에도 결과가 달라질 수 있고 Environment Interaction이 있기 때문에 Offline Eval만으로 모든 것을 확인하기 어렵다.

## AgentVersion

모델 버전만 기록하면 회귀 원인을 찾기 어렵다. 이 책에서는 설명을 위해 AgentVersion를 다음 Tuple로 본다.

~~~text
AgentVersion = (
  model,
  instruction,
  context_policy,
  harness,
  state_schema,
  memory_policy,
  tools,
  identity_policy,
  runtime,
  sandbox_policy,
  grader
)
~~~

외부 표준은 아니다. Agent Behavior에 영향을 주는 Version Boundary를 설명하기 위한 설명용 개념이다.

## Grader도 Version한다

채점기가 바뀌면 같은 실행 경로 점수가 바뀔 수 있다.

따라서:

~~~text
Agent Candidate
+ Grader v1
~~~

와:

~~~text
Agent Candidate
+ Grader v2
~~~

는 직접 비교 시 주의해야 한다. Benchmark Versioning이 중요한 이유다.

## Nondeterminism

에이전트 평가를 한 번만 실행하면 Noise가 클 수 있다. Repeat Count를 정의한다.

예:

~~~text
critical recovery cases:
5 trials

expensive browser cases:
3 trials

deterministic tool contract:
1 trial
~~~

위험과 비용에 따라 조정한다.

## Promotion Rule

평균 점수가 올라갔다고 바로 Promotion하지 않는다.

예:

~~~text
must_not_regress:
- security
- critical data integrity
- duplicate Side Effect
- production authorization

optimize:
- task success
- latency
- cost
- human intervention
~~~

Risk-weighted Gate가 필요하다.

## Model Upgrade Audit

새 모델이 나왔다. 기존 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)에 넣고 점수만 확인하면 부족하다.

~~~text
New Model
  ↓
Old Harness Eval
  ↓
Minimal Baseline
  ↓
Harness Component Audit
  ↓
Security Regression
  ↓
Long-horizon Regression
  ↓
Promotion
~~~

모델이 좋아졌다면 오래된 모델의 약점을 보완하는 보조 장치를 제거할 기회일 수 있다. 다음 장의 하네스 구성 요소의 제거 비교 실험으로 연결된다.

## Eval CI와 비용

에이전트 평가는 비쌀 수 있다. 그래서 모든 사례를 모든 커밋에서 돌리지 않는다.

예:

~~~text
PR
→ fast critical set

Nightly
→ broad regression

Release
→ full comparison

Production
→ sampled trace / shadow
~~~

일반적인 Test Suite와 마찬가지로 비용과 실행 시간에 따라 Eval cadence를 계층화할 수 있다.

## Eval Case Ownership

사례도 관리가 필요하다.

부가 정보 후보:

~~~text
id
owner
source_failure
introduced_at
risk
required_tools
environment
grader
repeat_count
fixed_by
last_run
~~~

담당자가 없으면 오래된 사례가 쌓이고 의미가 사라질 수 있다.

## Dataset Drift

Eval Dataset도 현실과 멀어질 수 있다.

확인할 것:

- 최근 운영 실패를 여전히 반영하는가.
- Tool/API가 바뀌었는가.
- 너무 쉬워졌는가.
- 모델이 Benchmark-specific pattern을 학습했는가.
- 채점기가 여전히 올바른가.

평가도 유지보수가 필요하다.

## 작은 예: Memory Regression

Production Failure:

~~~text
Agent used stale memory
→ wrong production endpoint
~~~

회귀를 확인할 평가 사례:

~~~text
Memory contains old endpoint
Current source contains new endpoint

Expected:
refresh source before action
~~~

Candidate Fix:

~~~text
add refresh_before=external_write
~~~

CI:

~~~text
PR gate
→ stale-memory regression test
~~~

이렇게 실패가 시스템 지식으로 전환된다.

## 이 장에서 가져갈 것

에이전트 평가를 보고서용 점수로만 사용하지 않는다. Development Loop에 연결한다.

~~~text
Trace
→ Failure
→ Eval Case
→ Candidate Change
→ Regression
→ Promotion
~~~

이 구조가 있어야 에이전트가 운영 과정에서 개선된다. 다음 장에서는 Candidate Change 중에서도 가장 자주 쌓이는 하네스 구성 요소를 다룬다. 계획기(Planner: 계획을 세우는 구성 요소), 메모리, 평가기(Evaluator: 결과를 평가하는 구성 요소), 하위 에이전트가 도움이 되는지 어떻게 측정하고 제거할 것인가. 하네스 구성 요소의 제거 비교 실험과 유지보수 부담으로 넘어간다.

## 주요 근거

- OpenAI Agent Improvement Loop
- OpenAI Macro Evals for Agentic Systems
- Anthropic Agent Eval guidance
- research/topics/15-eval-ci-regression.md
