# 9장. 실패 후 이어가는 Agent

에이전트가 외부 API를 호출했고 요청은 성공했다. 그런데 그 직후 에이전트 프로세스가 종료됐다. 새 프로세스가 시작됐다. 마지막으로 저장된 컨텍스트(Context: 모델에 전달하는 정보)에는 API 성공 결과가 없다. 에이전트는 같은 행동을 다시 실행해야 할까. 이 질문은 오래 실행되는 에이전트에서 가장 위험한 복구 문제 중 하나다. 실행을 이어간다는 것은 이전 프롬프트를 다시 넣는 것과 다르다. 이미 일어난 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)와 아직 일어나지 않은 외부 상태 변화를 구분해야 한다.

## Recovery와 Retry는 다르다

재시도는 같은 논리 작업을 다시 시도하는 동작이다. 복구는 시스템이 중단된 뒤 **현재 상태를 다시 구성하고 안전한 다음 행동을 결정하는 과정**이며, 그 결과로 재시도를 선택할 수도 있다.

~~~text
Retry
= operation attempt again

Recovery
= reconstruct state
  + determine what already happened
  + decide next safe step
~~~

두 개념을 섞으면 중복 외부 상태 변화가 생길 수 있다.

## Replay는 재실행이 아니다

중단 뒤에도 이어갈 수 있는 실행 시스템에서는 이벤트 이력을 Replay해 Workflow State를 복구하는 방식이 널리 사용된다. 에이전트에 이 개념을 가져올 때 주의해야 한다. LLM Inference와 외부 도구를 무조건 다시 실행하면 안 된다.

~~~text
Replay
≠ Re-run Model
≠ Re-run External Side Effect
~~~

대신 과거 결과를 기록해두고 그 기록으로 상태를 재구성한다.

예:

~~~text
model.completed
tool.proposed
tool.authorized
tool.started
tool.completed
~~~

복구 시 tool.completed Event가 있다면 해당 작업 단위를 다시 실행할 필요가 없을 수 있다.

## 왜 Model Call도 그대로 Replay하지 않는가

LLM 호출은 같은 입력에서도 결과가 달라질 수 있고 모델 버전도 바뀔 수 있다. 따라서 과거 실행 상태를 복구할 때는 당시 Model Result를 다시 생성하려 하기보다 기록된 결과를 실행 이력의 사실로 사용하는 편이 안전하다.

~~~text
model.requested
model.completed:
  output_ref
  model_version
  context_ref
~~~

복구 후 새로운 판단이 필요하면 그것은 새로운 모델 호출이다. 과거 Call의 재현이 아니다.

## Side Effect는 가장 조심해야 한다

다음 도구를 생각해보자.

~~~text
send_email
create_issue
charge_payment
deploy_release
merge_pull_request
~~~

이들은 중복 실행 비용이 크다. 예를 들어 create_issue가 실제 서버에서는 성공했지만 클라이언트가 응답 시간 초과를 받았다. 에이전트는 실패라고 생각할 수 있다. 바로 재시도하면 같은 이슈가 두 개 만들어질 수 있다. 그래서 외부 상태 변경에는 가능한 한 멱등성(Idempotency: 같은 요청을 반복해도 결과가 중복되지 않는 성질)이 필요하다.

## Idempotency Key

논리적으로 같은 작업 단위에 같은 Key를 사용한다.

예:

~~~text
goal_id + operation_type + logical_operation_id
~~~

예를 들어:

~~~text
G-100:create_issue:bug-report-1
~~~

서버가 멱등성을 지원하면 같은 Key로 다시 요청해도 기존 결과를 반환할 수 있다. 서버가 지원하지 않는다면 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)가 External ID나 실행 기록을 확인해 중복 여부를 판단해야 한다. 에이전트 하네스만으로 exactly-once semantics를 쉽게 보장할 수 있다고 가정하지 않는다.

## Tool Execution State

External Tool Call은 최소한 다음 유지 과정을 기록할 수 있다.

~~~text
PROPOSED
AUTHORIZED
STARTED
COMPLETED
FAILED
UNKNOWN
~~~

UNKNOWN이 중요하다. 클라이언트가 응답 시간 초과됐는데 서버 결과를 모르는 상태다. 이때 단순 재시도보다 먼저 외부 시스템을 조회해야 할 수 있다.

~~~text
UNKNOWN
   ↓
Query External State
   ├─ Already Applied → mark COMPLETED
   └─ Not Applied → retry
~~~

## Crash Point를 생각한다

하나의 도구 호출에는 여러 Crash Point가 있다.

~~~text
1. before request
2. request sent
3. server applied action
4. response returned
5. event persisted
~~~

3과 5 사이에서 비정상 종료가 나면 가장 까다롭다. 외부 외부 상태 변화는 발생했지만 내부 상태는 기록되지 않았다. 이 문제를 완전히 없애기 어렵다.

그래서:

- idempotency
- external operation id
- reconciliation
- transaction/outbox pattern
- explicit UNKNOWN state

같은 기법이 필요해진다.

## Pause / Resume

복구는 비정상 종료만을 의미하지 않는다. 사람의 승인이나 User Input을 기다리는 일시 중지도 같은 구조를 사용한다.

~~~text
RUNNING
  ↓
approval.requested
  ↓
PAUSED
  ↓
approval.granted
  ↓
RESUMED
~~~

실행 재개 시점에는 다음을 다시 확인해야 할 수 있다.

- 승인 대상 행동이 여전히 유효한가.
- 외부 원본이 바뀌지 않았는가.
- 인증 정보로 행사할 수 있는 권한 범위가 아직 유효한가.
- 실행 환경을 새로 만들어야 하는가.

따라서 실행 재개는 "이전 다음 단계를 그대로 실행"하는 것이 아니다. 새로운 Current State에서 Pending Intent를 재검증한다.

## Retry Budget

복구 후에도 실패가 반복될 수 있다. 재시도 횟수를 상태에 저장해야 하는 이유다.

~~~text
operation: run_test
attempt: 3
last_failure: timeout
budget_remaining: 1
~~~

프로세스 메모리에만 재시도 횟수가 있으면 Restart할 때 다시 0으로 돌아가 무한 반복할 수 있다.

## Snapshot

이벤트 이력이 커지면 매번 처음부터 상태를 재구성하는 비용이 커진다. 상태 사본(Snapshot: 특정 시점의 상태 사본)을 사용할 수 있다.

~~~text
Snapshot @ event 500
+
Events 501..current
~~~

상태 사본에는 현재 투영을 저장한다.

예:

- 개별 실행 상태
- Goal Progress
- Pending Approval
- Artifact References
- Retry Counters

상태 사본이 있어도 중요한 이벤트 이력을 바로 삭제해야 하는 것은 아니다. Retention과 감사 요구에 따라 결정한다.

## Schema Versioning

에이전트 시스템이 발전하면 Event Schema도 바뀐다.

예:

~~~text
tool.completed v1
tool.completed v2
  + external_operation_id
~~~

이전 실행을 복구하려면 버전 호환이 필요하다. 이벤트에는 다음 부가 정보가 유용하다.

~~~text
event_type
event_version
event_id
run_id
timestamp
actor
causation_id
correlation_id
payload
harness_version
policy_version
~~~

모든 시스템이 같은 필드를 가져야 한다는 의미는 아니다. 복구와 감사에 필요한 최소 부가 정보를 설계해야 한다.

## Deterministic Rule과 Model Decision을 나눈다

복구에서는 가능한 한 알려진 규칙을 시스템이 처리한다.

예:

~~~text
Tool COMPLETED
→ do not execute again

Approval REJECTED
→ do not resume action

Retry budget exhausted
→ block

Source version changed
→ reconcile
~~~

반면 다음은 모델 판단이 필요할 수 있다.

- 실패 원인 분석
- 대안 구현
- 충돌 해결 전략
- 새로운 계획

이 분리는 에이전트를 더 예측 가능하게 만든다.

## 작은 예: PR 생성 중 Crash

상황:

~~~text
Goal:
bug fix 완료 후 PR 생성

State:
tests passed

Action:
create_pull_request
~~~

에이전트가 요청을 보낸 뒤 Network Timeout이 발생했다.

나쁜 복구:

~~~text
Restart
→ "PR 생성이 실패했다"
→ create_pull_request again
~~~

좋은 복구:

~~~text
tool.started
external_operation_id: op-77
response: unknown
        ↓
Restart
        ↓
Query GitHub for matching PR
        ├─ Found PR #220
        │    ↓
        │ mark tool.completed
        │
        └─ Not Found
             ↓
          safe retry with same logical operation
~~~

핵심은 Internal Error만 보고 External Reality를 추정하지 않는 것이다.

## Recovery는 State Plane의 품질을 드러낸다

Short Task에서는 상태 설계가 약해도 문제가 잘 보이지 않는다. 에이전트가 한 프로세스 안에서 끝나기 때문이다. 비정상 종료, 승인, Long Pause가 들어오면 설계가 드러난다. 복구를 위해 매번 Conversation Transcript를 사람이 읽어야 한다면 중단 뒤에도 이어갈 수 있는 실행 구조가 부족한 것이다.

## 이 장에서 가져갈 것

Agent Recovery의 핵심은 "다시 시작한다"가 아니다.

> **이미 일어난 일과 아직 일어나지 않은 일을 구분한 뒤, 현재 외부 상태에서 다음 안전한 행동을 결정하는 것**이다.

그래서 다음 경계를 유지한다.

~~~text
Replay
≠ Side-effect Re-execution

Retry
≠ Recovery

Internal Failure
≠ External Action Failure
~~~

다음 장에서는 더 긴 시간축을 본다. 프로세스가 한두 번 실패하는 수준을 넘어, 수십 분에서 수 시간 동안 많은 항목과 중간 완료 지점을 추적해야 할 때 에이전트가 왜 컨텍스트와 계획을 잃는지 살펴본다.

## 주요 근거

- Temporal Durable Execution
- Temporal Workflow replay model
- Anthropic Managed Agents
- research/topics/18-durable-state-event-log-replay.md
