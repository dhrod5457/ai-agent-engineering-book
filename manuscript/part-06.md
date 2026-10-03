# Part VI. Agent를 관찰하고 개선한다

Part VI는 Agent improvement loop를 닫는다.

~~~text
Trace
→ Failure Classification
→ Eval
→ Regression
→ Harness Audit
~~~

최종 출력만 보지 않고 실행 경로, 실제 실제 환경에서 확인한 결과, 반복 반복 실행의 신뢰성, 구성 요소의 marginal value를 함께 본다.

<!-- source-draft: chapters/18/draft.md -->

## 18장. Trace 없이는 Agent를 디버깅할 수 없다

에이전트가 실패했을 때 최종 출력만으로는 그 이유를 알기 어렵다. 잘못된 도구를 골랐는가. 올바른 도구를 잘못된 인자로 호출했는가. 도구는 성공했는데 결과를 잘못 해석했는가. 승인이 막혔는가. 실행 환경이 죽었는가. 오래된 상태를 사용했는가. 에이전트 시스템은 여러 계층이 이어져 결과를 만든다. 그래서 최종 출력만 보는 오류 원인 분석으로는 부족하다.

### Agent Failure는 경로를 따라 발생한다

예를 들어 다음 목표가 있다.

> 특정 이슈를 읽고 필요한 Code 수정 후 PR을 만들어라.

최종 결과는 "PR 생성 실패"일 수 있다. 가능한 원인은 많다.

~~~text
Context Error
→ wrong issue selected

Model Error
→ wrong file chosen

Tool Error
→ invalid patch

Policy Denial
→ PR creation blocked

Runtime Error
→ test process crashed

State Error
→ stale branch

Verification Error
→ failed test not detected
~~~

이 경로를 볼 수 있어야 원인을 찾을 수 있다.

### Trace란 무엇인가

이 책에서 실행 추적 기록(Trace)은 다음처럼 본다.

> **에이전트 실행에서 모델, 도구, 상태, 정책, 실행 환경의 주요 이벤트와 관계를 다시 구성할 수 있는 관찰 데이터다.**

Logging과 겹치지만 목적이 더 구조적이다. 단순 Text Log를 쌓는 것이 아니라 Execution Path와 원인 관계를 다시 구성하는 데 초점을 둔다. 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)의 이벤트 이력이 실행 추적 기록의 정보 원본이 될 수는 있지만 둘을 같은 저장소나 같은 유지 과정으로 만들 필요는 없다. 이벤트 이력은 recovery를 위한 durable fact에 가깝고, 실행 추적 기록은 diagnosis와 evaluation을 위한 관찰 view까지 포함할 수 있다.

### 최소 Trace 후보

다음 이벤트를 남길 수 있다.

~~~text
run.started

context.built

model.requested
model.completed

tool.proposed
tool.authorized
tool.started
tool.completed
tool.failed

approval.requested
approval.granted

state.updated
artifact.created
artifact.verified

handoff.started
handoff.completed

run.completed
run.failed
~~~

모든 시스템이 이 이벤트 이름을 그대로 써야 하는 것은 아니다. 핵심은 계층 간 Causation을 추적할 수 있게 하는 것이다.

### Correlation과 Causation

한 도구 호출이 어떤 Model Decision에서 나왔는지 연결해야 한다.

예:

~~~text
model.completed
id: m-10

tool.proposed
id: t-20
caused_by: m-10

tool.completed
id: t-21
caused_by: t-20
~~~

이 관계가 있으면 도구 실패가 어떤 판단에서 시작됐는지 찾을 수 있다.

### Trace와 Chain-of-thought는 다르다

Agent Debugging을 위해 모델의 private reasoning text 전체를 저장해야 하는 것은 아니다. 오히려 다음처럼 구조화된 Decision Surface가 더 유용할 수 있다.

~~~text
selected_tool
tool_args
state_refs
policy_result
output_contract
failure_class
~~~

실행 추적 기록의 목표는 private reasoning을 최대한 많이 저장하는 것이 아니라 **실제 시스템 행동과 결정에 사용된 외부 근거를 재구성하는 것**이다.

### Model Trace

모델 호출에는 다음 부가 정보가 유용할 수 있다.

- model/version
- input reference
- output reference
- latency
- token/cost
- structured output validity
- selected tools

Sensitive Context 전체를 무조건 저장하지 않는다. 참조나 Redaction을 사용할 수 있다.

### Tool Trace

도구 호출에는 다음이 중요하다.

~~~text
tool
arguments
authorization
execution_id
status
external_operation_id
latency
result_ref
retryable
~~~

특히 외부 상태 변경에서는 멱등성(Idempotency: 같은 요청을 반복해도 결과가 중복되지 않는 성질)과 복구에 실행 추적 기록이 직접 사용될 수 있다.

### State Trace

에이전트 상태 관리 계층의 변경도 실행 추적 기록과 연결할 수 있다.

예:

~~~text
goal.updated
approval.pending
source.version_changed
artifact.verified
memory.retrieved
~~~

이렇게 하면 "왜 모델에게 이 컨텍스트(Context: 모델에 전달하는 정보)가 들어갔는가"도 추적할 수 있다.

### Policy Trace

정책이 행동을 막았다면 이유가 남아야 한다.

~~~text
decision: deny
policy: deploy-policy-v12
reason: approval_required
resource: prod-cluster-a
~~~

그렇지 않으면 에이전트는 같은 행동을 반복하거나 운영자가 거부 이유를 알기 어렵다.

### Runtime Trace

다음 실패는 모델과 무관할 수 있다.

- OOM
- Container startup failure
- Browser crash
- DNS failure
- Package registry outage

이런 이벤트를 Model Failure와 같은 Bucket에 넣지 않는다.

### Audit Trace와 Debug Trace

두 목적은 겹치지만 다르다.

#### Audit

누가 무엇을 언제 했는가.

#### Debug

왜 이 결과가 나왔는가. 감사에는 신원, 접근 대상 자원, Policy Result가 중요하다. Debug에는 Context Version, Tool Output, Failure Class가 더 중요할 수 있다. 모든 데이터를 한 Trace Store에 넣을 필요는 없지만 서로 연결할 수 있어야 한다.

### Privacy와 Sensitive Data

실행 추적 기록은 많은 정보를 담는다. 그래서 다음이 필요하다.

- Redaction
- Access Control
- Retention
- Sampling
- Encryption
- Secret Filtering

"디버깅을 위해 모두 저장한다"는 접근은 위험하다.

### Trace Sampling

모든 개별 실행의 모든 이벤트를 장기 보존하면 비용이 커질 수 있다. 다음 전략을 쓸 수 있다.

~~~text
All Runs
→ lightweight trace

Failed Runs
→ detailed trace

High-risk Runs
→ full audit trace

Sampled Successful Runs
→ quality analysis
~~~

목적에 따라 Level을 나눈다.

### Trace가 Eval로 이어진다

실행 추적 기록은 단순 운영 로그가 아니다. 실패한 개별 실행을 평가 사례로 승격할 수 있다.

~~~text
Production Failure
      ↓
Trace Inspection
      ↓
Failure Classification
      ↓
Reusable Eval Case
~~~

이 구조가 다음 두 장의 기반이다.

### 작은 예: 잘못된 Tool 선택

최종 결과:

~~~text
Task failed
~~~

실행 추적 기록:

~~~text
context.built
selected_tools:
- generic_shell
- read_file

model.completed
selected_tool: generic_shell

tool.proposed
command: "grep ..."

tool.failed
reason: command unavailable

model.completed
selected_tool: generic_shell

tool.failed
same reason
~~~

원인은 모델 자체일 수도 있지만 사용 가능한 도구의 범위와 재시도 정책 문제일 수도 있다. 실행 추적 기록이 없으면 "모델이 멍청했다"로 끝날 수 있다.

### Trace Schema도 Versioning 대상이다

에이전트 설계 구조가 바뀌면 실행 추적 이벤트도 변한다.

예:

~~~text
tool.completed v1

tool.completed v2
+ external_operation_id
+ policy_version
~~~

이전 실행과 새 실행을 비교하려면 Schema Version을 남기는 것이 좋다.

### Trace Quality

실행 추적 기록이 있다고 오류 원인 분석이 자동으로 쉬워지는 것은 아니다.

나쁜 실행 추적 기록:

~~~text
Agent started
Agent thinking
Tool used
Error
Retrying
Done
~~~

좋은 실행 추적 기록:

~~~text
run_id
goal_id
model_call_id
tool_call_id
policy_decision_id
artifact_id
source_version
failure_class
~~~

구조화된 식별자가 있어야 각 기록 사이의 관계를 따라갈 수 있다.

### 이 장에서 가져갈 것

에이전트는 여러 계층의 상호작용으로 결과를 만든다. 최종 출력만 보면 실패 원인을 구분하기 어렵다.

~~~text
Model
Context
Tool
State
Policy
Runtime
Verification
~~~

이 경로를 다시 구성할 수 있게 하는 것이 실행 추적 기록이다. 다음 장에서는 실행 추적 기록을 보고 "왜 실패했는가"를 넘어서 "이 에이전트가 얼마나 잘하는가"를 측정한다. 출력, 실행 경로, 실제 환경에서 확인한 결과, 반복 실행의 신뢰성을 함께 보는 에이전트 평가로 넘어간다.

### Source Notes

- [S-OAI-EVALS]

---

<!-- source-draft: chapters/19/draft.md -->

## 19장. Agent를 어떻게 평가할 것인가

에이전트가 최종 답변을 맞혔다. 그런데 중간에 허용되지 않은 도구를 세 번 호출했고, 운영 데이터를 불필요하게 읽었으며, 같은 행동을 두 번 실행했다. 이 에이전트를 성공했다고 볼 수 있을까. 따라서 에이전트를 평가할 때는 최종 출력뿐 아니라 그 결과에 이르는 과정도 살펴야 한다.

### Output Eval의 한계

일반 LLM 평가에서는 최종 응답 품질이 중요하다. 에이전트는 환경을 바꾼다. 따라서 다음도 평가 대상이 된다.

~~~text
Output
Trajectory
Tool Selection
Tool Arguments
State Handling
Policy Compliance
Environment Outcome
Reliability
Cost
Latency
Recovery
~~~

### Output Eval

최종 답변이나 산출물 자체를 평가한다.

예:

- 답변 정확성
- Report 품질
- 생성 파일 내용
- Structured Output Schema

필요하지만 충분하지 않다.

### Trajectory Eval

에이전트가 어떤 경로로 결과에 도달했는지 본다.

예:

- 올바른 도구를 선택했는가.
- 불필요한 도구를 반복했는가.
- 작업 인계가 적절했는가.
- Policy Violation 시도가 있었는가.
- 재시도가 합리적이었는가.

같은 출력이라도 실행 경로 품질이 다를 수 있다.

### Outcome Eval

가능하면 환경의 최종 상태를 본다.

코드 작업 에이전트:

~~~text
tests pass?
expected diff?
build succeeds?
~~~

Browser Agent:

~~~text
actual form submitted?
correct field values?
~~~

Database Agent:

~~~text
expected final row state?
~~~

Outcome Eval은 Proxy가 아니라 완료 자체에 가깝다.

### Deterministic Grader

가능하면 Machine-checkable한 실제 환경에서 확인한 결과를 우선한다.

예:

- unit test
- schema validation
- exact DB state
- checksum
- static analysis
- artifact inspection

장점:

- 반복 가능
- 빠름
- 비용 낮음
- 해석이 명확함

### Model Grader

모든 품질을 Code로 판정하기 어렵다.

예:

- 설명의 명확성
- 요구사항 충족 정도
- 문서 품질
- 전략 적절성

이때 Model Grader를 사용할 수 있다. 하지만 Model Grader도 버전과 프롬프트에 따라 달라질 수 있다. 따라서 채점기 자체를 Versioned Component로 본다.

### Human Grader

다음 상황에서는 사람이 필요할 수 있다.

- UX 품질
- 정책 Edge Case
- 고위험 Acceptance
- Model Grader Calibration

사람의 검토를 모든 사례에 쓰면 비용이 크다. Sample과 Calibration에 집중할 수 있다.

### Security Eval

에이전트가 작업을 성공해도 보안을 위반했다면 좋은 에이전트가 아니다.

예:

- 외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)에 속음
- 메모리에 악성 정보를 심는 공격(Memory Poisoning) 허용
- Unauthorized Tool 시도
- Sensitive Data 노출
- 승인 우회

Security Dataset을 별도로 유지할 수 있다.

### State Handling Eval

오래 실행되는 에이전트에서는 상태가 중요한 평가 대상이다.

예:

- stale source를 사용했는가.
- completed action을 중복 실행했는가.
- pending approval을 잊었는가.
- multi-item state를 누락했는가.
- checkpoint 후 정확히 resume했는가.

이 영역은 Output-only benchmark에서 잘 보이지 않을 수 있다.

### Repeated Reliability

에이전트는 같은 입력에도 결과가 달라질 수 있다. 한 번 성공했다고 안정적이라고 말하기 어렵다. 같은 작업을 여러 번 실행해야 할 수 있다.

~~~text
Trial 1: pass
Trial 2: pass
Trial 3: fail
Trial 4: pass
Trial 5: fail
~~~

여기서 평균 성공뿐 아니라 Consistency가 중요하다. tau-bench 계열에서는 반복 신뢰성을 보는 측정 지표도 제안돼 왔다.

### pass@k와 pass^k

두 측정 지표는 목적이 다르다. 아래 식은 직관을 설명하기 위한 것으로, 실제 benchmark마다 계산 정의는 다시 확인해야 한다.

개념적으로:

~~~text
pass@k
= k번 중 한 번이라도 성공

pass^k
= k번 모두 성공
~~~

에이전트 운영에서는 "한 번은 된다"와 "반복해서 된다"가 다르다. 운영 작업은 후자에 더 민감할 수 있다.

### Infrastructure Noise

Agentic Benchmark는 실행 환경 영향을 받는다.

예:

- CPU
- RAM
- 응답 시간 초과
- Browser Stability
- 네트워크
- Package Availability
- Container Startup

Anthropic의 Agentic Coding Eval 분석에서도 Infrastructure 설정이 결과에 유의미한 영향을 줄 수 있음을 보여준다. 따라서 작은 점수 차이를 모델 차이로 바로 해석하지 않는다.

### Benchmark Result는 System Result다

Agent Benchmark 결과를 다음처럼 시스템 전체의 결과로 보는 편이 낫다.

~~~text
Benchmark Result
=
Model
+ Harness
+ Tool Interface
+ Context Policy
+ State Strategy
+ Runtime
+ Environment
+ Grader
+ Noise
~~~

정확한 수학식은 아니다. Evaluation Boundary를 넓게 보자는 뜻이다.

### Benchmark Versioning

성능 비교 평가도 바뀐다.

- 작업 수정
- 채점기 수정
- 환경 수정
- 정책 수정
- 도구 수정

tau2-bench는 채점기 수정으로 동일한 실행 경로를 다시 평가해 점수가 바뀔 수 있는 사례를 공개했다. 따라서 결과에는 다음을 기록한다.

~~~text
benchmark_version
task_revision
grader_version
model_version
harness_version
environment_image
runtime_resource
trial_count
~~~

### Binary vs Partial

많은 단계에 걸친 작업에서는 Final Success만 보면 어디에서 실패했는지 알기 어렵다. Partial Checkpoint를 사용할 수 있다.

예:

~~~text
Milestone 1 pass
Milestone 2 pass
Milestone 3 fail
~~~

OSWorld 2.0처럼 여러 단계에 걸친 작업을 평가하는 벤치마크도 중간 진행을 평가하는 세밀한 확인 지점(Checkpoint)을 활용한다. 하지만 Partial Score가 완료를 대신해서는 안 된다.

~~~text
Diagnostic Partial Score
≠ Product Completion
~~~

### Capability Slice

평균 점수 하나는 실패를 숨길 수 있다.

예:

~~~text
Overall 82%

Tool Routing 95%
State Recovery 52%
Security 91%
Long-horizon 48%
~~~

이 에이전트는 Short Task에는 강하지만 장시간 작업에는 약하다. 기능별 Slice가 필요한 이유다.

### Failure Corpus

초기 Eval Dataset은 거대할 필요가 없다. 운영에서 나온 실패 20~50개부터 시작할 수 있다.

예:

- wrong tool
- stale state
- premature completion
- duplicate mutation
- permission denial loop
- hallucinated success

운영 실패가 좋은 Eval Seed가 된다.

### Eval Case 구조

예:

~~~text
id
goal
initial_state
environment
allowed_tools
expected_outcome
grader
risk
repeat_count
source_failure
~~~

이 부가 정보가 있으면 Regression Dataset을 관리하기 쉽다.

### 작은 예: PR 작성 Agent

작업:

> 수정 후 테스트를 통과시키고 PR을 생성하라.

평가:

~~~text
Output:
PR URL exists

Trajectory:
no forbidden tool
no duplicate PR
reasonable retries

Outcome:
tests pass
PR diff correct

Security:
no secret access

Reliability:
5 repeated runs

Cost:
within budget
~~~

이렇게 해야 에이전트 품질을 더 잘 볼 수 있다.

### 이 장에서 가져갈 것

에이전트 평가는 "답을 맞혔는가"보다 넓다.

~~~text
Output
+
Trajectory
+
Outcome
+
Reliability
+
Security
+
Cost
~~~

그리고 Benchmark Score를 Model Score로 읽지 않는다. 다음 장에서는 이 평가를 개발 작업 흐름에 넣는다. 운영 실패를 회귀를 확인할 평가 사례로 만들고, PR / Nightly / Release Gate에 연결하는 개발 과정에 통합한 지속적 평가를 다룬다.

### Source Notes

- [S-OAI-EVALS]
- [S-ANTHROPIC-EVALS]
- [S-ANTHROPIC-INFRA-NOISE]
- [S-TAU2]
- [S-OSWORLD2]

---

<!-- source-draft: chapters/20/draft.md -->

## 20장. Eval을 CI로 만든다

에이전트가 운영 환경에서 같은 실수를 두 번 했다. 첫 번째에도, 두 번째에도 운영자가 고쳤다. 이 시스템은 기록을 남겼지만, 그 기록으로 같은 실수를 줄이는 개선 과정은 갖추지 못했다. 에이전트 개선을 사람의 기억에 의존해 운영하기는 어렵다. 의미 있는 실패를 다시 실행 가능한 평가 사례로 승격해야 한다. 이 장에서 말하는 개발 과정에 통합한 지속적 평가는 배포 자동 처리 절차 전체를 설명하려는 것이 아니다. 에이전트 행동 변경에 대한 기존 기능의 악화를 막는 검증 단계를 개발 과정에 넣는 데 초점을 둔다.

### Eval은 Release 전 행사만이 아니다

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

### 운영 실패를 Regression으로 만든다

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

### Failure Triage

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

### Eval Dataset을 나눈다

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

### PR Gate

모든 Pull Request마다 전체 Agent Benchmark를 돌리면 비싸고 느리다. PR Gate에는 빠르고 중요한 사례를 둔다.

예:

- Schema Validation
- Tool Contract Regression
- 핵심 20개 Agent Case
- Security Critical Case
- deterministic verifier

목표는 빠른 회귀 차단이다.

### Nightly

비용이 큰 평가는 Nightly로 돌릴 수 있다.

예:

- 100+ multi-turn cases
- 반복 실험
- long-horizon
- browser environment
- security attack set

결과를 Trend로 본다.

### Release Gate

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

### Shadow

운영 Traffic과 유사한 입력을 Candidate Agent에 넣되 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)는 실행하지 않는 방식이다.

~~~text
Production Input
   ├─ Current Agent → real action
   └─ Candidate Agent → shadow only
~~~

운영 분포에서 Behavior를 비교할 수 있다.

### Canary

일부 Low-risk Traffic에 후보를 적용한다. 문제가 없으면 확대한다. 에이전트 시스템은 같은 입력에도 결과가 달라질 수 있고 Environment Interaction이 있기 때문에 Offline Eval만으로 모든 것을 확인하기 어렵다.

### AgentVersion

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

### Grader도 Version한다

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

### Nondeterminism

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

### Promotion Rule

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

### Model Upgrade Audit

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

### Eval CI와 비용

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

### Eval Case Ownership

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

### Dataset Drift

Eval Dataset도 현실과 멀어질 수 있다.

확인할 것:

- 최근 운영 실패를 여전히 반영하는가.
- Tool/API가 바뀌었는가.
- 너무 쉬워졌는가.
- 모델이 Benchmark-specific pattern을 학습했는가.
- 채점기가 여전히 올바른가.

평가도 유지보수가 필요하다.

### 작은 예: Memory Regression

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

### 이 장에서 가져갈 것

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

### Source Notes

- [S-OAI-EVALS]
- [B-AGENT-VERSION]

---

<!-- source-draft: chapters/21/draft.md -->

## 21장. Harness Ablation과 Debt

에이전트가 실패하자 계획을 세우는 기능을 추가했다. 다른 실패가 생기자 평가 기능을 붙였고, 모델에 전달할 정보가 길어지자 이를 압축하는 기능을 넣었다. 이전 실수를 반복하자 메모리도 추가했다. 몇 달 뒤 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)에는 많은 구성 요소가 있지만 어떤 것이 필요한지 아무도 모른다. 에이전트 하네스에도 유지보수 부담이 생긴다.

### Harness Component는 가설이다

계획기(Planner: 계획을 세우는 구성 요소) 하나를 예로 들어보자. 계획기를 추가한다는 것은 사실 다음 가설을 넣는 것이다.

> 작업을 시작하기 전에 세부 단계로 나누면 이 작업 분포에서 성공률이 높아진다.

평가기(Evaluator: 결과를 평가하는 구성 요소):

> 독립된 평가가 스스로 검증하는 것보다 오류를 더 잘 잡는다.

메모리:

> 과거 교훈의 재사용이 오래되거나 오염된 정보를 쓰는 위험보다 더 큰 이득을 준다.

하위 에이전트:

> 컨텍스트를 분리해 얻는 이득이 협업 조율 비용보다 크다.

이 가설은 측정돼야 한다.

### Minimal Baseline

제거 비교 실험(Ablation: 구성 요소를 빼고 효과를 비교하는 실험)을 하려면 단순한 비교 기준이 필요하다.

예:

~~~text
Model
+ essential instruction
+ required tools
+ deterministic verifier
~~~

여기에 구성 요소를 하나씩 추가한다. 비교 기준 자체가 복잡하면 어떤 모델의 약점을 보완하는 보조 장치가 기여했는지 알기 어렵다.

### Component Inventory

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

### Harness Component Record

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

### Ablation

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

하지만 에이전트는 같은 입력에도 결과가 달라질 수 있다. 한 번의 실행으로 결론 내리면 위험하다.

### Repeated Trials

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

### Pin the Environment

제거 비교 실험 중 다른 변수를 바꾸면 해석이 어려워진다. 가능하면 다음을 고정한다.

- 모델 버전
- Tool Version
- 실행 환경
- 평가 데이터 모음
- 채점기
- 정책
- Resource Limit

한 번에 하나의 주요 변수를 바꾼다.

### Capability Slice

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

### Safety Slice

하네스 구성 요소를 제거하면 Quality는 비슷하지만 보안이 나빠질 수 있다.

예:

~~~text
remove tool filter
→ success +1%
→ unauthorized action +8%
~~~

이 구성 요소는 단순 성공 기준으로 제거하면 안 된다. Ablation Metric에 Safety를 포함한다.

### Cost와 Latency

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

### Interaction Effect

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

### Model Upgrade는 Audit Trigger다

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

### Stable Interface와 Mutable Harness

Anthropic Managed Agents 사례에서 중요한 관점 중 하나는 외부 인터페이스와 내부 하네스를 분리하는 것이다.

~~~text
Stable:
session / tool / runtime contract

Mutable:
planner / context strategy / model adaptation
~~~

이렇게 하면 하네스를 자주 실험해도 Application Integration 전체를 흔들지 않을 수 있다.

### Harness Debt

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

### Debt Review

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

### 작은 예: Planner 제거

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

### Component가 해결한 Failure를 기록한다

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

### 이 장에서 가져갈 것

하네스는 시간이 지나며 자연스럽게 복잡해진다. 복잡성을 피할 수는 없지만 효과를 뒷받침할 근거가 없는 보조 장치를 계속 유지할 필요도 없다.

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

### Source Notes

- [S-ANTHROPIC-AAR]
- [S-ANTHROPIC-HARNESS]
- [B-HARNESS-DEBT]
