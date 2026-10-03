# 18장. Trace 없이는 Agent를 디버깅할 수 없다

에이전트가 실패했을 때 최종 출력만으로는 그 이유를 알기 어렵다. 잘못된 도구를 골랐는가. 올바른 도구를 잘못된 인자로 호출했는가. 도구는 성공했는데 결과를 잘못 해석했는가. 승인이 막혔는가. 실행 환경이 죽었는가. 오래된 상태를 사용했는가. 에이전트 시스템은 여러 계층이 이어져 결과를 만든다. 그래서 최종 출력만 보는 오류 원인 분석으로는 부족하다.

## Agent Failure는 경로를 따라 발생한다

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

## Trace란 무엇인가

이 책에서 실행 추적 기록(Trace)은 다음처럼 본다.

> **에이전트 실행에서 모델, 도구, 상태, 정책, 실행 환경의 주요 이벤트와 관계를 다시 구성할 수 있는 관찰 데이터다.**

Logging과 겹치지만 목적이 더 구조적이다. 단순 Text Log를 쌓는 것이 아니라 Execution Path와 원인 관계를 다시 구성하는 데 초점을 둔다. 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)의 이벤트 이력이 실행 추적 기록의 정보 원본이 될 수는 있지만 둘을 같은 저장소나 같은 유지 과정으로 만들 필요는 없다. 이벤트 이력은 recovery를 위한 durable fact에 가깝고, 실행 추적 기록은 diagnosis와 evaluation을 위한 관찰 view까지 포함할 수 있다.

## 최소 Trace 후보

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

## Correlation과 Causation

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

## Trace와 Chain-of-thought는 다르다

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

## Model Trace

모델 호출에는 다음 부가 정보가 유용할 수 있다.

- model/version
- input reference
- output reference
- latency
- token/cost
- structured output validity
- selected tools

Sensitive Context 전체를 무조건 저장하지 않는다. 참조나 Redaction을 사용할 수 있다.

## Tool Trace

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

## State Trace

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

## Policy Trace

정책이 행동을 막았다면 이유가 남아야 한다.

~~~text
decision: deny
policy: deploy-policy-v12
reason: approval_required
resource: prod-cluster-a
~~~

그렇지 않으면 에이전트는 같은 행동을 반복하거나 운영자가 거부 이유를 알기 어렵다.

## Runtime Trace

다음 실패는 모델과 무관할 수 있다.

- OOM
- Container startup failure
- Browser crash
- DNS failure
- Package registry outage

이런 이벤트를 Model Failure와 같은 Bucket에 넣지 않는다.

## Audit Trace와 Debug Trace

두 목적은 겹치지만 다르다.

### Audit

누가 무엇을 언제 했는가.

### Debug

왜 이 결과가 나왔는가. 감사에는 신원, 접근 대상 자원, Policy Result가 중요하다. Debug에는 Context Version, Tool Output, Failure Class가 더 중요할 수 있다. 모든 데이터를 한 Trace Store에 넣을 필요는 없지만 서로 연결할 수 있어야 한다.

## Privacy와 Sensitive Data

실행 추적 기록은 많은 정보를 담는다. 그래서 다음이 필요하다.

- Redaction
- Access Control
- Retention
- Sampling
- Encryption
- Secret Filtering

"디버깅을 위해 모두 저장한다"는 접근은 위험하다.

## Trace Sampling

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

## Trace가 Eval로 이어진다

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

## 작은 예: 잘못된 Tool 선택

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

## Trace Schema도 Versioning 대상이다

에이전트 설계 구조가 바뀌면 실행 추적 이벤트도 변한다.

예:

~~~text
tool.completed v1

tool.completed v2
+ external_operation_id
+ policy_version
~~~

이전 실행과 새 실행을 비교하려면 Schema Version을 남기는 것이 좋다.

## Trace Quality

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

## 이 장에서 가져갈 것

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

## 주요 근거

- OpenAI Agent Evals
- OpenAI Trace Grading
- Anthropic Agent Eval guidance
- research/topics/06-evaluation-observability.md
