# 18장. Trace 없이는 Agent를 디버깅할 수 없다

Agent가 실패했다.

최종 출력만 보면 이유를 알기 어렵다.

잘못된 Tool을 골랐는가. 올바른 Tool을 잘못된 Argument로 호출했는가. Tool은 성공했는데 Result를 잘못 해석했는가. Approval이 막혔는가. Runtime이 죽었는가. 오래된 State를 사용했는가.

Agent 시스템은 여러 Layer가 이어져 결과를 만든다.

그래서 Final Output만 보는 Debugging으로는 부족하다.

## Agent Failure는 경로를 따라 발생한다

예를 들어 다음 Goal이 있다.

> 특정 Issue를 읽고 필요한 Code 수정 후 PR을 만들어라.

최종 결과는 "PR 생성 실패"일 수 있다.

가능한 원인은 많다.

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

## Trace란 무엇인가

이 책에서 Trace는 다음처럼 본다.

> **Agent 실행에서 Model, Tool, State, Policy, Runtime의 주요 Event와 관계를 다시 구성할 수 있는 관찰 데이터.**

Logging과 겹치지만 목적이 더 구조적이다. 단순 Text Log를 쌓는 것이 아니라 Execution Path와 원인 관계를 다시 구성하는 데 초점을 둔다.

Agent State Plane의 Event History가 Trace의 Source가 될 수는 있지만 둘을 같은 저장소나 같은 lifecycle로 만들 필요는 없다. Event History는 recovery를 위한 durable fact에 가깝고, Trace는 diagnosis와 evaluation을 위한 관찰 view까지 포함할 수 있다.

## 최소 Trace 후보

다음 Event를 남길 수 있다.

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

모든 시스템이 이 Event 이름을 그대로 써야 하는 것은 아니다.

핵심은 Layer 간 Causation을 추적할 수 있게 하는 것이다.

## Correlation과 Causation

한 Tool Call이 어떤 Model Decision에서 나왔는지 연결해야 한다.

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

이 관계가 있으면 Tool 실패가 어떤 Decision에서 시작됐는지 찾을 수 있다.

## Trace와 Chain-of-thought는 다르다

Agent Debugging을 위해 Model의 private reasoning text 전체를 저장해야 하는 것은 아니다.

오히려 다음처럼 구조화된 Decision Surface가 더 유용할 수 있다.

~~~text
selected_tool
tool_args
state_refs
policy_result
output_contract
failure_class
~~~

Trace의 목표는 private reasoning을 최대한 많이 저장하는 것이 아니라 **실제 시스템 행동과 결정에 사용된 외부 근거를 재구성하는 것**이다.

## Model Trace

Model Call에는 다음 Metadata가 유용할 수 있다.

- model/version
- input reference
- output reference
- latency
- token/cost
- structured output validity
- selected tools

Sensitive Context 전체를 무조건 저장하지 않는다.

Reference나 Redaction을 사용할 수 있다.

## Tool Trace

Tool Call에는 다음이 중요하다.

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

특히 External Mutation에서는 Idempotency와 Recovery에 Trace가 직접 사용될 수 있다.

## State Trace

Agent State Plane의 변경도 Trace와 연결할 수 있다.

예:

~~~text
goal.updated
approval.pending
source.version_changed
artifact.verified
memory.retrieved
~~~

이렇게 하면 "왜 Model에게 이 Context가 들어갔는가"도 추적할 수 있다.

## Policy Trace

Policy가 Action을 막았다면 이유가 남아야 한다.

~~~text
decision: deny
policy: deploy-policy-v12
reason: approval_required
resource: prod-cluster-a
~~~

그렇지 않으면 Agent는 같은 Action을 반복하거나 운영자가 Deny 이유를 알기 어렵다.

## Runtime Trace

다음 실패는 Model과 무관할 수 있다.

- OOM
- Container startup failure
- Browser crash
- DNS failure
- Package registry outage

이런 Event를 Model Failure와 같은 Bucket에 넣지 않는다.

## Audit Trace와 Debug Trace

두 목적은 겹치지만 다르다.

### Audit

누가 무엇을 언제 했는가.

### Debug

왜 이 결과가 나왔는가.

Audit에는 Identity, Resource, Policy Result가 중요하다.

Debug에는 Context Version, Tool Output, Failure Class가 더 중요할 수 있다.

모든 데이터를 한 Trace Store에 넣을 필요는 없지만 서로 연결할 수 있어야 한다.

## Privacy와 Sensitive Data

Trace는 많은 정보를 담는다.

그래서 다음이 필요하다.

- Redaction
- Access Control
- Retention
- Sampling
- Encryption
- Secret Filtering

"디버깅을 위해 모두 저장한다"는 접근은 위험하다.

## Trace Sampling

모든 Run의 모든 Event를 장기 보존하면 비용이 커질 수 있다.

다음 전략을 쓸 수 있다.

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

## Trace가 Eval로 이어진다

Trace는 단순 운영 로그가 아니다.

실패 Run을 Eval Case로 승격할 수 있다.

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

## 작은 예: 잘못된 Tool 선택

최종 결과:

~~~text
Task failed
~~~

Trace:

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

원인은 Model 자체일 수도 있지만 Tool Surface와 Retry Policy 문제일 수도 있다.

Trace가 없으면 "모델이 멍청했다"로 끝날 수 있다.

## Trace Schema도 Versioning 대상이다

Agent Architecture가 바뀌면 Trace Event도 변한다.

예:

~~~text
tool.completed v1

tool.completed v2
+ external_operation_id
+ policy_version
~~~

Old Run과 New Run을 비교하려면 Schema Version을 남기는 것이 좋다.

## Trace Quality

Trace가 있다고 Debugging이 자동으로 쉬워지는 것은 아니다.

나쁜 Trace:

~~~text
Agent started
Agent thinking
Tool used
Error
Retrying
Done
~~~

좋은 Trace:

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

구조화된 Identifier가 있어야 Relation을 따라갈 수 있다.

## 이 장에서 가져갈 것

Agent는 여러 Layer의 상호작용으로 결과를 만든다.

Final Output만 보면 실패 원인을 구분하기 어렵다.

~~~text
Model
Context
Tool
State
Policy
Runtime
Verification
~~~

이 경로를 다시 구성할 수 있게 하는 것이 Trace다.

다음 장에서는 Trace를 보고 "왜 실패했는가"를 넘어서 "이 Agent가 얼마나 잘하는가"를 측정한다.

Output, Trajectory, Outcome, Reliability를 함께 보는 Agent Evaluation으로 넘어간다.

## 주요 근거

- OpenAI Agent Evals
- OpenAI Trace Grading
- Anthropic Agent Eval guidance
- research/topics/06-evaluation-observability.md
