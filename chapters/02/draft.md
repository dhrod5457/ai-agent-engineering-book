# 2장. Agent Loop를 설계한다

Agent를 가장 짧게 구현하면 몇 줄짜리 반복문이 될 수 있다.

모델에 메시지를 보낸다. Tool Call이 나오면 Tool을 실행한다. 결과를 다시 모델에 전달한다. 모델이 최종 답변을 내면 끝낸다.

개념을 이해하기에는 충분하다.

하지만 실제 시스템에서는 바로 질문이 생긴다.

Tool이 5분 동안 응답하지 않으면 어떻게 할까. 같은 Tool이 세 번 실패하면 계속 시도할까. 외부 API는 성공했는데 Agent 프로세스가 결과를 저장하기 전에 죽으면 어떻게 할까. 모델이 완료했다고 했지만 테스트가 실패하면 끝낼까.

Agent Loop는 단순한 반복문에서 시작하지만 운영 환경에서는 하나의 작은 실행 제어 시스템이 된다.

## 최소 Loop

Agent의 최소 구조는 다음과 같이 표현할 수 있다.

~~~text
Input
  ↓
Prepare Context
  ↓
Model
  ↓
Decision
  ├─ Final Output → Stop
  └─ Tool Call
         ↓
      Execute
         ↓
     Observation
         ↓
   Next Context
         ↺
~~~

ReAct 계열 연구에서 널리 알려진 것처럼 Agent는 reasoning과 action을 번갈아 수행하며 환경의 observation을 다음 판단에 반영한다.

중요한 것은 reasoning text 자체가 아니다.

환경과 상호작용하면서 다음 행동을 선택한다는 점이다.

## Tool Call이 Action은 아니다

모델이 Tool Call을 생성했다고 해서 Action이 이미 실행된 것은 아니다.

~~~text
Model
  ↓
Proposed Action
  ↓
Validation / Authorization
  ↓
Execution
  ↓
Actual Result
~~~

이 구분은 뒤의 Security 장에서 더 중요해진다.

모델은 다음 JSON을 만들 수 있다.

~~~text
{
  "tool": "create_pull_request",
  "base": "main",
  "head": "feature-x"
}
~~~

하지만 실제 시스템은 이 Action을 실행하기 전에 확인할 수 있다.

- 현재 Agent에게 PR 생성 권한이 있는가.
- 대상 Repository가 허용 범위인가.
- Branch가 보호 규칙을 위반하지 않는가.
- 현재 Task가 Mutation을 허용하는가.

즉 Model Decision과 Side Effect 사이에는 Harness와 Policy Boundary가 존재한다.

## 운영 Loop가 추가로 가져야 하는 것

최소 Loop에는 보이지 않지만 실제 Agent에 필요한 책임이 있다.

### Stop Condition

언제 끝낼 것인가.

### Budget

얼마나 오래, 몇 번, 어느 비용까지 실행할 것인가.

### Failure Classification

무엇을 다시 시도하고 무엇을 중단할 것인가.

### Interruption

승인이나 사용자 입력이 필요할 때 어떻게 멈출 것인가.

### Resume

다시 시작했을 때 어디서 이어갈 것인가.

### Verification

모델의 완료 선언을 실제 완료로 인정할 것인가.

이 중 하나라도 없으면 Agent는 쉬운 데모에서는 동작해도 긴 작업에서는 불안정해질 수 있다.

## Stop Condition은 모델의 기분이 아니다

가장 단순한 Agent는 모델이 final output을 반환하면 끝난다.

대화형 Assistant라면 충분할 수 있다.

하지만 작업형 Agent는 다르다.

예를 들어 목표가 다음과 같다고 하자.

> failing test를 수정하라.

모델이 "수정했습니다"라고 답했더라도 테스트가 여전히 실패하면 Task는 끝나지 않았다.

따라서 Stop Condition을 둘로 나눠볼 수 있다.

~~~text
Conversation Stop
= 모델이 더 이상 Tool Call을 하지 않음

Task Completion
= 외부 Success Condition이 만족됨
~~~

둘은 다를 수 있다.

운영 Agent에서는 가능하면 Completion을 외부 Evidence에 연결한다.

예:

- Test Pass
- File Exists
- Expected DB State
- Browser State
- Artifact Validation

모델의 self-report는 참고 정보일 수 있지만 Completion Authority가 되지 않게 한다.

## Loop에는 Budget이 필요하다

Agent가 실패하면 흔히 "한 번 더 해보자"고 생각한다.

하지만 Retry가 무제한이면 같은 실패를 반복할 수 있다.

Budget은 여러 종류가 있다.

- Max Turn
- Max Tool Call
- Time
- Token
- Cost
- Retry Count
- External API Quota

Budget의 목적은 비용 절약만이 아니다.

Agent가 progress 없이 반복하는 상황을 정상적인 Failure State로 바꾸는 역할도 한다.

~~~text
Progress
  ↓
Continue

No Progress + Retry Budget Remaining
  ↓
Retry / Alternative

No Progress + Budget Exhausted
  ↓
Block / Escalate
~~~

## 모든 실패를 Retry하지 않는다

Tool 실행 실패 하나를 생각해보자.

~~~text
git push
→ 403 Forbidden
~~~

이 실패를 다섯 번 재시도해도 해결되지 않을 가능성이 높다.

반면:

~~~text
HTTP 503
~~~

은 잠시 뒤 성공할 수 있다.

따라서 실패를 분류해야 한다.

예시:

### Retryable
- transient network error
- rate limit with retry-after
- temporary service unavailable

### Repairable
- test failure
- invalid generated file
- schema validation failure

모델이 원인을 분석하고 변경한 뒤 다시 시도할 수 있다.

### Blocked
- missing credential
- approval required
- missing user decision
- unavailable internal resource

### Fatal
- invalid task contract
- prohibited action
- unrecoverable corrupted environment

실제 taxonomy는 시스템마다 다르다.

중요한 것은 Failure가 Boolean이 아니라는 점이다.

## Retry도 State를 가져야 한다

같은 Tool을 다시 호출하더라도 이전 시도와 무엇이 다른지 알아야 한다.

나쁜 Retry:

~~~text
Fail
→ Same Context
→ Same Action
→ Fail
→ Same Context
→ Same Action
~~~

좋은 Retry는 적어도 새로운 정보가 있어야 한다.

~~~text
Fail
→ Inspect Error
→ Update Hypothesis / Context / Input
→ Retry
~~~

또는 단순 transient error라면 exponential backoff 같은 deterministic policy가 모델 판단보다 낫다.

이미 알고 있는 규칙을 모델에게 매번 판단시키지 않는다.

## Interruption은 정상 상태다

Agent가 모든 상황을 독립적으로 결정해야 할 필요는 없다.

예를 들어:

- 결제 승인
- Production Deploy
- 개인정보 포함 데이터 전송
- 요구사항의 중요한 ambiguity

는 사람의 판단을 기다리는 것이 정상일 수 있다.

이때 Agent를 실패 처리하는 대신 상태를 둔다.

~~~text
RUNNING
  ↓
AWAITING_APPROVAL
  ↓
RESUME
~~~

또는:

~~~text
RUNNING
  ↓
AWAITING_INPUT
  ↓
RESUME
~~~

중요한 것은 Pause 상태에서 Process를 계속 살려둘 필요가 없다는 점이다.

상태가 외부에 저장돼 있다면 Runtime을 종료했다가 이후 다시 만들 수 있다.

이 지점에서 Agent Loop와 Durable State가 연결된다.

## Resume는 Prompt를 다시 보내는 것이 아니다

Pause 후 다음 날 사용자가 승인했다고 하자.

가장 단순한 구현은 이전 Conversation Summary를 새 모델에 넣고 "계속해"라고 말하는 것이다.

짧은 Task에서는 동작할 수 있다.

하지만 다음 정보가 중요하다면 부족하다.

- 이미 어떤 Tool이 실행됐는가.
- External Mutation이 성공했는가.
- 어떤 Artifact가 만들어졌는가.
- 어떤 Version의 Source를 기준으로 판단했는가.
- 승인 대상 Action은 정확히 무엇이었는가.

Resume는 Conversation Continuation 이상의 문제다.

이 책에서 뒤에 다룰 Agent State Plane이 필요한 이유다.

## Tool Failure와 Model Failure를 분리한다

Agent 시스템에서는 여러 계층이 동시에 실패할 수 있다.

~~~text
Model Failure
- invalid structured output
- poor decision
- premature completion

Harness Failure
- wrong routing
- state bug
- retry bug

Tool Failure
- API error
- command error
- schema mismatch

Runtime Failure
- process crash
- OOM
- browser crash
- network unavailable

Policy Failure / Denial
- forbidden tool
- insufficient scope
- approval missing
~~~

이들을 모두 "Agent Error" 하나로 기록하면 개선하기 어렵다.

Trace와 Eval에서도 같은 분리가 필요하다.

## Handoff도 하나의 Transition이 될 수 있다

Multi-Agent 구조에서는 Tool Call 대신 다른 Agent로 ownership을 넘기는 Transition이 들어갈 수 있다. 다만 이 책에서는 이를 기본 Loop로 두지 않는다. 단일 Agent의 Loop와 State, Tool Boundary를 먼저 안정시킨 뒤 Part VII에서 Handoff를 별도로 다룬다.

## Loop와 State Machine

Agent Loop를 설명할 때 모든 것을 엄격한 State Machine으로 만들 필요는 없다.

LLM 판단 자체는 열려 있다.

대신 시스템이 확실히 알고 있는 부분은 명시적 State로 두는 편이 좋다.

예:

~~~text
READY
RUNNING
AWAITING_INPUT
AWAITING_APPROVAL
VERIFYING
COMPLETED
FAILED
~~~

이런 State는 모델의 자유 텍스트보다 시스템의 Transition Rule로 관리하는 편이 낫다.

Agent Engineering에서는 불확실한 판단과 기계적으로 판정 가능한 규칙을 나눈다.

~~~text
Open-ended Diagnosis
→ Model

Retry Count
→ System

Approval Required
→ Policy

Test Pass
→ Verifier
~~~

## 작은 예: 테스트 수정 Agent

다음 목표를 생각해보자.

> UserServiceTest의 실패를 수정하고 전체 관련 테스트를 통과시켜라.

최소 Loop:

~~~text
Read Failure
→ Inspect Code
→ Edit
→ Run Test
→ PASS?
    ├─ Yes → Complete
    └─ No  → Inspect Failure → Retry
~~~

운영 Loop에서는 조금 더 필요하다.

~~~text
Goal
 ↓
Load Relevant Context
 ↓
Model Decision
 ↓
Tool Proposal
 ↓
Policy Check
 ↓
Execute
 ↓
Record Event
 ↓
Observe
 ↓
Progress?
 ├─ Yes → Continue
 └─ No
      ↓
   Failure Class
      ├─ Retryable → Retry
      ├─ Repairable → Re-plan
      ├─ Blocked → Pause
      └─ Fatal → Fail
 ↓
Verification
 ↓
PASS → Complete
~~~

여기서 중요한 것은 모델의 지능만이 아니라 Loop 주변의 통제 구조다.

## Loop는 어디까지 Harness 책임인가

Agent Loop를 운영 수준으로 만들면서 책임이 계속 추가됐다.

- Context
- Tool Dispatch
- Retry
- Stop
- Budget
- Pause / Resume
- Verification
- Trace

이 책임을 묶어 관리하는 계층이 필요하다.

이 책에서는 이를 Harness라고 부른다.

Harness는 특정 Framework 제품을 뜻하지 않는다. Model을 실제 실행 가능한 Agent로 만드는 Control Logic이다.

다음 장에서는 Harness가 어디까지 책임져야 하며, 왜 기능을 많이 넣는 것이 항상 좋은 Harness를 의미하지 않는지 살펴본다.

## 주요 근거

- ReAct
- OpenAI Agents SDK, Running Agents
- Google Agent Development Kit
- research/topics/01-agent-loop-runtime.md
