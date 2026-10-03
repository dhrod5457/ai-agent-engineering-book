# Part I. Model에서 Agent로

Part I은 세 질문에서 시작한다.

~~~text
Model과 Agent는 무엇이 다른가?
Agent는 어떻게 반복 실행되는가?
그 실행 Control을 어디에 둘 것인가?
~~~

Model 자체의 성능보다 Model을 실제 행동으로 연결하는 실행 구조와 책임 경계를 먼저 고정한다.

<!-- source-draft: chapters/01/draft.md -->

## 1장. Model과 Agent는 무엇이 다른가

같은 모델을 사용했는데도 어떤 Agent는 일을 끝내고, 어떤 Agent는 같은 자리를 맴돈다.

둘 다 같은 LLM을 쓴다. 둘 다 Repository를 읽을 수 있고 Shell도 실행할 수 있다. 그런데 하나는 필요한 파일을 찾고, 테스트를 실행하고, 실패를 수정하고, 결과를 남긴다. 다른 하나는 이미 읽은 파일을 다시 읽고, 같은 명령을 반복하고, 마지막에는 "완료했다"고 말하지만 실제 테스트는 실패한 상태로 남아 있다.

차이는 모델 이름만으로 설명하기 어렵다.

이 책은 바로 이 차이를 다룬다.

### 모델이 좋아지면 Agent도 자동으로 좋아지는가

LLM을 사용할 때 가장 눈에 잘 띄는 변화는 모델 성능이다. 새로운 모델이 나오면 reasoning, coding, tool use benchmark가 올라간다. 자연스럽게 다음 결론으로 이어지기 쉽다.

> 더 좋은 모델을 사용하면 더 좋은 Agent가 된다.

일부는 맞다. 더 강한 모델은 복잡한 코드를 더 잘 읽고, 더 적절한 Tool을 선택하고, 긴 작업에서도 더 나은 판단을 할 수 있다.

하지만 이것만으로 실제 Agent의 능력을 설명할 수는 없다.

예를 들어 모델이 정확하게 다음 Tool 호출을 제안했다고 하자.

~~~text
delete_file("/tmp/build/result.json")
~~~

Agent 시스템에서는 그 뒤에 더 많은 일이 일어난다.

- 이 Tool을 현재 Agent가 사용할 권한이 있는가.
- 경로가 허용된 Sandbox 안에 있는가.
- 이 작업은 승인 없이 실행해도 되는가.
- Tool 실행이 실패하면 다시 시도할 것인가.
- 성공 결과를 다음 Context에 얼마나 넣을 것인가.
- 이 변경을 State에 기록할 것인가.
- 프로세스가 죽으면 이 Tool을 다시 실행해도 되는가.

모델은 Action을 제안할 수 있다. 실제 Action을 어떻게 실행하고 통제할지는 시스템의 책임이다.

이 책에서는 이 차이를 다음처럼 표현한다.

~~~text
Model Capability
≠ Agent Capability
~~~

이 식은 모델이 중요하지 않다는 뜻이 아니다.

Agent의 실제 능력을 모델 하나의 속성으로 축약하지 말자는 뜻이다.

### Agent는 Prompt + Model이 아니다

가장 단순한 LLM 애플리케이션은 다음과 같다.

~~~text
Prompt
  ↓
Model
  ↓
Response
~~~

여기에 Tool Calling을 붙이면 조금 달라진다.

~~~text
Prompt
  ↓
Model
  ↓
Tool Call
  ↓
Tool Result
  ↓
Model
  ↓
Response
~~~

여기서부터 Agent에 가까워진다.

Model이 외부 환경을 관찰하고 Action을 선택하며 결과를 다시 읽기 때문이다.

하지만 운영 환경에서 사용할 Agent는 이 반복만으로 충분하지 않다.

운영 시스템에서는 적어도 다음 질문이 생긴다.

~~~text
언제 멈출 것인가?
어떤 Tool을 노출할 것인가?
Tool 실패는 어떻게 처리할 것인가?
어떤 상태를 다음 Turn에 유지할 것인가?
Context가 넘치면 무엇을 버릴 것인가?
프로세스가 죽으면 어떻게 이어갈 것인가?
Credential은 누가 보유할 것인가?
위험한 Action은 누가 승인할 것인가?
완료는 누가 판정할 것인가?
~~~

이 질문들은 모델 내부의 문제가 아니다.

Agent를 둘러싼 실행 시스템의 문제다.

### Agent Capability를 구성하는 것

Agent Capability는 다음과 같은 함수로 생각할 수 있다.

~~~text
Agent Capability
≈ f(
  Model,
  Instruction,
  Context,
  Tool Interface,
  Harness,
  State,
  Memory,
  Runtime,
  Identity,
  Security Policy,
  Evaluation Feedback
)
~~~

정확한 수학식은 아니다.

Agent 성능에 영향을 주는 책임을 분리하기 위한 개념식이다.

각 항목은 서로 다른 실패를 만든다.

#### Model

현재 입력과 Tool 결과를 보고 다음 판단을 만든다.

모델이 약하면 복잡한 Repository를 이해하지 못하거나 잘못된 Tool을 선택할 수 있다.

#### Instruction

Agent가 따라야 할 역할과 제약을 전달한다.

하지만 Instruction은 권한 시스템이 아니다. "프로덕션 DB를 수정하지 마라"라는 자연어 문장이 실제 DB Credential을 제거해주지는 않는다.

#### Context

현재 Inference에서 모델이 볼 수 있는 정보다.

너무 적으면 필요한 사실을 놓친다. 너무 많으면 중요한 정보가 묻히거나 오래된 정보가 현재 사실처럼 남을 수 있다.

#### Tool Interface

Agent가 외부 세계에 Action을 수행하는 인터페이스다.

같은 API라도 Agent에게 어떤 이름, Schema, 결과 형태로 제공하는지에 따라 실제 사용성이 달라질 수 있다.

SWE-agent 연구는 이를 Agent-Computer Interface(ACI)라는 관점으로 다뤘다. 이 용어를 모든 Tool 시스템의 표준명으로 쓰려는 것은 아니다. 핵심은 같은 모델을 사용해도 컴퓨터와 상호작용하는 인터페이스 설계에 따라 실제 성능이 달라질 수 있다는 점이다.

#### Harness

모델을 반복 실행하는 제어 계층이다.

Context를 만들고, Tool을 Dispatch하고, Stop Condition을 판단하고, Retry와 Handoff를 처리한다.

#### State

현재 작업이 어디까지 진행됐는지 보존한다.

장시간 작업에서는 Context Window보다 State가 더 중요해지는 순간이 온다.

#### Memory

이전 실행에서 얻은 정보를 이후 작업에 재사용한다.

하지만 잘못된 Memory가 저장되면 미래 실행까지 오염될 수 있다.

#### Runtime

실제 Side Effect가 발생하는 환경이다.

Filesystem, Network, Browser, Shell, Container, VM 등이 여기에 속한다.

#### Identity와 Policy

누가 행동하는지, 어떤 권한으로 무엇을 할 수 있는지를 결정한다.

#### Evaluation

Agent 변경이 실제로 좋아졌는지 확인한다.

Harness를 바꾸거나 Model을 업그레이드했는데 Eval이 없다면 개선과 회귀를 구분하기 어렵다.

### 같은 모델, 다른 Agent

가상의 두 Coding Agent를 비교해보자.

Agent A는 다음 구조다.

~~~text
Strong Model
+ Repository 전체를 항상 Context에 넣음
+ Shell Tool 하나
+ Workspace 밖 접근 가능
+ Conversation History만 저장
+ Agent가 "완료"하면 종료
~~~

Agent B는 다음 구조다.

~~~text
Same Strong Model
+ 필요한 파일만 Progressive Context
+ Search / Read / Edit / Test Tool 분리
+ Workspace Sandbox
+ Goal / Progress State
+ Test Result 기반 Completion
+ Trace / Retry
~~~

두 시스템은 같은 Model을 사용한다.

하지만 실제 작업에서는 상당히 다른 행동을 보일 수 있다.

Agent A는 Tool Surface가 지나치게 넓고, Completion Authority가 모델 자신에게 있으며, Durable State가 없다.

Agent B는 행동 공간과 완료 판정을 시스템에서 더 명확하게 제한한다.

따라서 Agent A의 실패를 보고 "모델이 부족하다"고 결론 내리면 잘못된 문제를 고치게 된다.

모델을 바꿔도 같은 구조적 실패가 반복될 수 있다.

### Framework는 Architecture가 아니다

또 하나 자주 생기는 혼동이 있다.

어떤 Agent Framework를 선택하면 Agent Architecture가 정해졌다고 생각하는 것이다.

Framework는 유용하다.

예를 들어 어떤 SDK는 다음 기능을 제공할 수 있다.

- Tool Calling
- Handoff
- Session
- Guardrail
- Trace
- MCP Integration

하지만 이 기능이 존재한다고 해서 다음 설계가 자동으로 결정되지는 않는다.

- Session과 Long-term Memory를 어떻게 나눌 것인가.
- 어떤 Tool을 어떤 Identity가 호출할 수 있는가.
- 위험한 Mutation에 어떤 Approval을 둘 것인가.
- Crash 후 어떤 State를 복구할 것인가.
- Completion을 어떤 Evidence로 판정할 것인가.

Framework는 구현 도구다. Architecture는 책임의 배치다.

따라서 이 책은 특정 SDK의 기능 목록보다 각 책임을 어디에 둘지에 집중한다.

### Model, Harness, Runtime을 먼저 나눈다

Agent 구조를 처음 볼 때는 세 덩어리로 나누는 것이 유용하다.

~~~text
Model
- 판단한다
- Tool Call을 제안한다
- Structured Output을 만든다

Harness
- Context를 구성한다
- Loop를 실행한다
- Tool을 Dispatch한다
- Stop / Retry / Handoff를 처리한다
- State와 Trace를 연결한다

Runtime
- Process를 실행한다
- File을 수정한다
- Network에 연결한다
- Credential을 사용한다
- 실제 Side Effect를 만든다
~~~

이 구분만으로도 여러 잘못된 설계를 피할 수 있다.

예를 들어 "모델이 위험한 파일을 삭제하지 않도록 Prompt를 강화한다"는 대응은 Model/Harness 쪽 통제다.

반면 "해당 파일을 Sandbox에서 Mount하지 않는다"는 Runtime 통제다.

둘은 같은 문제가 아니다.

### Agent State Plane

장시간 작업에서는 현재 Goal과 Progress, 이미 실행한 Action, 생성한 Artifact, Pending Approval을 잃지 않아야 한다.

이 책에서는 이런 **한 Agent 실행의 연속성**을 담당하는 계층을 Agent State Plane이라고 부른다. 외부 표준 명칭이 아니라 여러 구현과 연구에서 반복되는 책임을 설명하기 위한 synthesis다.

핵심은 Context와 Durable State를 분리하는 것이다. 모델이 현재 Context에서 어떤 정보를 잊더라도 시스템까지 상태를 잃어서는 안 된다.

구성과 Recovery 방식은 Part III에서 자세히 다룬다.

### 더 많은 자율성이 먼저는 아니다

Agent 시스템은 Memory, Planner, Subagent 같은 눈에 띄는 기능부터 추가하기 쉽다. 하지만 운영에서 더 먼저 필요한 것은 대개 작은 Tool Surface, 통제된 Runtime, Verification, Trace다.

어떤 기능을 어떤 순서로 추가할지는 Task와 Risk에 따라 달라진다. 핵심은 기능 수를 Agent의 성숙도로 보지 않는 것이다. 실제 도입 순서는 25장에서 다시 정리한다.

### 이 책이 다루는 경계

Agent Engineering은 다른 세 영역과 맞닿아 있다.

첫째, Instruction Engineering이다.

CLAUDE.md, AGENTS.md, Skill, Rule, Hook을 어떻게 작성하고 검증할지는 별도의 문제다. 이 책에서는 그것들이 Agent Definition과 Context에 어떻게 들어오는지만 다룬다.

둘째, Cloud Agent다.

Agent를 Local에서 실행할지 Cloud Runner에서 실행할지, Git으로 어떻게 Handoff할지, Compute와 Token 비용을 어떻게 나눌지는 실행 위치의 문제다.

셋째, AI Software Factory다.

여러 Work Item과 Worker를 어떻게 Scheduling하고 Acceptance와 Delivery를 관리할지는 한 Agent 실행보다 상위 계층이다.

이 책은 그 경계를 다음처럼 유지한다.

~~~text
Agent State Plane
= 한 Agent 실행의 연속성

Software Factory Control Plane
= 여러 Work / Worker / Delivery의 연속성
~~~

### 이 장에서 가져갈 것

Model과 Agent를 같은 것으로 보면 실패 원인을 잘못 찾기 쉽다.

Agent가 일을 끝내는 능력은 Model뿐 아니라 Context, Tool, Harness, State, Runtime, Identity, Verification이 함께 만든다.

따라서 Agent Engineering의 첫 질문은 "어떤 모델을 쓸 것인가"가 아니다.

> 모델의 판단을 실제 행동으로 바꾸는 과정에서 어떤 책임을 어디에 둘 것인가?

다음 장에서는 이 구조의 가장 작은 실행 단위인 Agent Loop를 다룬다. Model이 Tool을 호출하고 Observation을 다시 읽는 단순 반복이 운영 환경에서 어떤 Control을 필요로 하는지 살펴본다.

### Source Notes

- [B-AGENT-CAPABILITY]
- [S-SWE-ACI]
- [S-OAI-AGENTS]
- [S-ANTHROPIC-AGENTS]

---

<!-- source-draft: chapters/02/draft.md -->

## 2장. Agent Loop를 설계한다

Agent를 가장 짧게 구현하면 몇 줄짜리 반복문이 될 수 있다.

모델에 메시지를 보낸다. Tool Call이 나오면 Tool을 실행한다. 결과를 다시 모델에 전달한다. 모델이 최종 답변을 내면 끝낸다.

개념을 이해하기에는 충분하다.

하지만 실제 시스템에서는 바로 질문이 생긴다.

Tool이 5분 동안 응답하지 않으면 어떻게 할까. 같은 Tool이 세 번 실패하면 계속 시도할까. 외부 API는 성공했는데 Agent 프로세스가 결과를 저장하기 전에 죽으면 어떻게 할까. 모델이 완료했다고 했지만 테스트가 실패하면 끝낼까.

Agent Loop는 단순한 반복문에서 시작하지만 운영 환경에서는 하나의 작은 실행 제어 시스템이 된다.

### 최소 Loop

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

### Tool Call이 Action은 아니다

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

### 운영 Loop가 추가로 가져야 하는 것

최소 Loop에는 보이지 않지만 실제 Agent에 필요한 책임이 있다.

#### Stop Condition

언제 끝낼 것인가.

#### Budget

얼마나 오래, 몇 번, 어느 비용까지 실행할 것인가.

#### Failure Classification

무엇을 다시 시도하고 무엇을 중단할 것인가.

#### Interruption

승인이나 사용자 입력이 필요할 때 어떻게 멈출 것인가.

#### Resume

다시 시작했을 때 어디서 이어갈 것인가.

#### Verification

모델의 완료 선언을 실제 완료로 인정할 것인가.

이 중 하나라도 없으면 Agent는 쉬운 데모에서는 동작해도 긴 작업에서는 불안정해질 수 있다.

### Stop Condition은 모델의 기분이 아니다

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

### Loop에는 Budget이 필요하다

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

### 모든 실패를 Retry하지 않는다

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

#### Retryable
- transient network error
- rate limit with retry-after
- temporary service unavailable

#### Repairable
- test failure
- invalid generated file
- schema validation failure

모델이 원인을 분석하고 변경한 뒤 다시 시도할 수 있다.

#### Blocked
- missing credential
- approval required
- missing user decision
- unavailable internal resource

#### Fatal
- invalid task contract
- prohibited action
- unrecoverable corrupted environment

실제 taxonomy는 시스템마다 다르다.

중요한 것은 Failure가 Boolean이 아니라는 점이다.

### Retry도 State를 가져야 한다

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

### Interruption은 정상 상태다

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

### Resume는 Prompt를 다시 보내는 것이 아니다

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

### Tool Failure와 Model Failure를 분리한다

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

### Handoff도 하나의 Transition이 될 수 있다

Multi-Agent 구조에서는 Tool Call 대신 다른 Agent로 ownership을 넘기는 Transition이 들어갈 수 있다. 다만 이 책에서는 이를 기본 Loop로 두지 않는다. 단일 Agent의 Loop와 State, Tool Boundary를 먼저 안정시킨 뒤 Part VII에서 Handoff를 별도로 다룬다.

### Loop와 State Machine

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

### 작은 예: 테스트 수정 Agent

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

### Loop는 어디까지 Harness 책임인가

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

### Source Notes

- [S-REACT]
- [S-OAI-AGENTS]
- [S-GOOGLE-ADK]

---

<!-- source-draft: chapters/03/draft.md -->

## 3장. Harness Engineering

Agent가 실패할 때마다 새로운 규칙을 하나 추가하는 것은 쉽다.

계획을 자주 잊으면 Planner를 붙인다. Context가 길어지면 Compaction을 붙인다. 완료를 너무 빨리 선언하면 Evaluator를 붙인다. 작업이 복잡하면 Subagent를 붙인다. 이전 실수를 반복하면 Memory를 붙인다.

몇 달 뒤에는 아무도 전체 구조를 정확히 설명하지 못하는 Agent가 만들어질 수 있다.

문제는 기능이 많다는 사실 자체가 아니다.

각 기능이 왜 존재하는지, 실제로 어떤 실패를 줄이는지 알 수 없다는 점이다.

Harness Engineering은 이 문제를 다룬다.

### Harness란 무엇인가

이 책에서 Harness는 다음과 같이 정의한다.

> **Harness는 Model을 반복 실행 가능한 Agent로 만들기 위해 Context, Tool, State, Control을 연결하는 실행 제어 계층이다.**

구성은 시스템마다 다를 수 있다.

대표적인 책임은 다음과 같다.

- Context Assembly
- Agent Loop
- Tool Dispatch
- Stop Condition
- Retry
- Budget
- Interruption / Resume
- Handoff
- Verification Hook
- Trace Emission

중요한 것은 특정 라이브러리 이름이 아니다.

OpenAI Agents SDK, Google ADK, 자체 Loop, 다른 Framework 중 무엇을 사용하더라도 이 책임은 어딘가에 존재해야 한다.

### Framework와 Harness는 다르다

Framework는 Harness를 구현하는 수단이 될 수 있다.

하지만 Framework를 선택했다고 Harness 설계가 끝나지는 않는다.

예를 들어 SDK가 Session 기능을 제공한다고 하자.

여전히 다음을 결정해야 한다.

- Session에 무엇을 저장할 것인가.
- Goal은 Session과 같은 lifecycle인가.
- External Tool 결과를 얼마나 저장할 것인가.
- Crash Recovery는 Session만으로 충분한가.
- Long-term Memory와 어떻게 분리할 것인가.

SDK가 Guardrail API를 제공해도 다음은 별도 문제다.

- 실제 File System 접근 범위
- Network Egress
- Credential Scope
- Production Mutation Approval

Harness Engineering은 API 목록을 조합하는 일이 아니다.

책임을 어디에 두고 무엇을 시스템이 강제할지 결정하는 일이다.

### Minimal Harness에서 시작한다

처음부터 많은 Component를 넣지 않는 편이 좋다.

최소 구조는 다음 정도로 시작할 수 있다.

~~~text
Input
 ↓
Context Builder
 ↓
Model
 ↓
Tool Dispatcher
 ↓
Observation
 ↺

+
Stop Condition
+
Deterministic Verification
+
Trace
~~~

이 구조로도 많은 Task를 처리할 수 있다.

여기서 반복되는 Failure를 관찰한 뒤 Component를 추가한다.

예를 들어 장시간 Coding Task에서 Model이 Context Limit에 가까워지면 Task를 조기 종료하는 문제가 반복된다고 하자.

그때 다음 Candidate를 검토할 수 있다.

- Context Reset
- Progress Artifact
- Goal State
- Session Continuation

중요한 것은 "Long-running Agent에는 Progress File이 필수다"라고 일반화하지 않는 것이다.

특정 Failure를 해결하기 위해 도입했으며, Model과 Task가 바뀌면 다시 검증해야 한다.

### Harness는 Model에 대한 가정을 담는다

Harness의 많은 기능은 사실 Model의 약점을 보완하기 위해 생긴다.

예를 들어:

~~~text
Planner
= Model이 큰 Task를 충분히 안정적으로 분해하지 못한다고 가정

Evaluator
= Model의 self-verification이 충분하지 않다고 가정

Memory
= 이전 lesson을 현재 Context만으로 복구하기 어렵다고 가정

Subagent
= 하나의 Context에서 모든 역할을 처리하는 것이 비효율적이라고 가정
~~~

이 가정은 영구적이지 않다.

모델이 좋아지면 일부 Scaffold는 가치가 줄어들 수 있다.

Anthropic이 Managed Agents와 Long-running Harness 관련 자료에서 강조하는 부분도 이 지점이다. Harness는 모델이 못한다고 가정하는 부분을 보완하지만, 모델이 발전하면 그 가정이 오래된 것이 될 수 있다.

따라서 Harness를 고정 인프라처럼 취급해서는 안 된다. Model이 바뀌면 기존 Scaffold의 필요성도 다시 측정해야 한다.

### Harness, Runtime, Durable State를 분리한다

운영 책임은 비유보다 실제 lifecycle로 나누는 편이 명확하다.

~~~text
Harness
= 실행 제어 로직

Runtime
= 실제 Tool과 Side Effect가 실행되는 환경

Durable State
= Process와 Runtime이 사라져도 남아야 하는 실행 정보
~~~

이렇게 분리하면 Runtime을 교체하거나 폐기해도 Goal과 Progress를 복구할 수 있다.

~~~text
Disposable Runtime
+
Durable State
~~~

이 조합은 Long-running Agent의 복구 구조를 단순하게 만든다. Session, Workspace, Goal, Memory의 세부 경계는 Part III에서 다시 정리한다.

### Harness가 너무 많은 일을 하면 생기는 문제

Agent가 실패할 때마다 Scaffold를 추가하면 복잡성이 증가한다.

~~~text
Failure
→ New Rule
→ New Planner
→ New Memory
→ New Evaluator
→ New Router
→ More Interaction
~~~

복잡성은 몇 가지 비용을 만든다.

#### Context Cost
각 Component가 Instruction, Tool Schema, Intermediate Result를 Context에 추가할 수 있다.

#### Latency
Planner → Executor → Reviewer 구조는 단일 실행보다 Turn과 Model Call이 늘어난다.

#### Coordination Failure
Component 사이에 다른 State가 생길 수 있다.

Planner는 완료됐다고 생각하지만 Executor는 다른 목표를 따를 수 있다.

#### Debugging Difficulty
최종 결과가 나빠졌을 때 어떤 Component가 원인인지 알기 어렵다.

#### Stale Assumption
예전 Model의 약점을 보완한 Rule이 새 Model의 좋은 행동을 방해할 수 있다.

이 책에서는 이런 누적을 **Harness Debt**라고 부른다.

이 역시 외부 표준 용어가 아니라 이 책의 synthesis다.

### Harness Component는 가설이다

Harness를 관리하는 가장 실용적인 방법은 각 Component를 하나의 가설로 보는 것이다.

예를 들어 Planner를 추가하려 한다.

가설:

> Long-horizon Task에서 upfront plan을 생성하면 Completion Rate가 올라간다.

그러면 검증 방법도 같이 필요하다.

~~~text
Baseline Harness
vs
Baseline + Planner
~~~

비교 대상:

- Task Success
- Cost
- Latency
- Human Intervention
- Security
- Repeated Reliability

예를 들어 Planner가 성공률을 조금 높이더라도 Latency와 Cost를 크게 늘린다면 모든 Task에 적용할 이유는 없다. 실제 판단은 반복 Eval과 Task별 효과를 보고 내려야 한다.

### Component Record

Harness가 커지면 각 Component가 어떤 Failure 때문에 들어왔고, 어떤 Eval이 효과를 확인했으며, 마지막으로 어느 Model에서 검증됐는지 기록하는 편이 좋다.

이 기록은 Model Upgrade 때 제거 후보를 찾고 "왜 이 Component가 존재하는가"를 Commit History에서 다시 추측하는 비용을 줄인다. 구체적인 Record와 Ablation 절차는 21장에서 다룬다.

### Harness와 State를 분리한다

Harness가 모든 상태를 Process Memory로 가지고 있으면 Crash Recovery가 어려워진다.

예를 들어:

~~~text
Harness Process
- current step
- approval pending
- completed tools
- generated artifact path
~~~

만 가지고 있다면 Process가 죽는 순간 정보가 사라진다.

따라서 장시간 Agent에서는 Harness와 State Store의 경계가 중요해진다.

~~~text
Harness
  ↔
Agent State Plane
~~~

Harness는 State를 읽고 Transition을 만든다.

State Plane은 Process Lifetime 밖에서 필요한 정보를 유지한다.

Agent State Plane은 Part III에서 이 구조를 자세히 다룬다.

### Harness와 Runtime도 분리한다

Harness가 Shell을 실행한다고 해서 Harness 자체가 Sandbox여야 하는 것은 아니다.

~~~text
Harness
  ↓ Action Request
Tool / Capability Gateway
  ↓
Execution Runtime
~~~

Runtime은 다음을 강제할 수 있다.

- File System Scope
- Network Scope
- Process Isolation
- Credential Injection

Harness의 자연어 Instruction보다 더 deterministic한 Boundary다.

이 분리를 유지하면 Model과 Harness를 바꾸더라도 Runtime Policy를 독립적으로 유지할 수 있다.

### Harness와 Verification

Harness의 중요한 책임 중 하나는 Completion Claim을 실제 Verification으로 연결하는 것이다.

예를 들어 Coding Agent에서:

~~~text
Model: "수정 완료"
        ↓
Harness
        ↓
Run Targeted Test
        ↓
PASS?
   ├─ Yes → Completion Candidate
   └─ No  → Continue / Fail
~~~

Verification을 Model에게 다시 물어보는 것과 실제 Test를 실행하는 것은 다르다.

가능한 한 deterministic한 검증이 있으면 그것을 우선한다.

### Harness 변경은 Versioning 대상이다

Agent 결과를 비교할 때 Model Version만 기록하면 부족하다.

Harness 변경 하나만으로도 행동이 달라질 수 있다.

예:

- Tool Description 수정
- Retry Count 변경
- Planner 추가
- Memory Retrieval 변경
- Context Compaction 변경
- Sandbox Policy 변경

따라서 뒤의 Eval 장에서는 AgentVersion을 Model보다 넓은 Tuple로 다룬다.

이 장에서는 최소한 다음 원칙만 기억하면 된다.

> Harness도 배포되는 Software다.

변경 이력과 Regression이 필요하다.

### Model Upgrade는 Harness Audit Trigger다

새 Model이 출시됐다고 기존 Harness를 그대로 유지해야 하는 것은 아니다. 먼저 기존 Harness와 단순한 Baseline을 비교하고, Planner·Memory·Evaluator 같은 Component가 여전히 필요한지 다시 측정한다.

이 책에서는 이런 검증을 Harness Ablation으로 다룬다. 반복 실행과 Variance를 포함한 구체적인 방법은 21장에서 설명한다.

### 지금 필요한 것만 남긴다

좋은 Harness는 기능이 가장 많은 Harness가 아니다.

현재 Task와 Model에서 필요한 책임을 명확히 가진 Harness다.

초기 운영 Agent라면 다음 정도로도 시작할 수 있다.

~~~text
Agent Definition
      ↓
Context Builder
      ↓
Agent Loop
      ↓
Small Tool Surface
      ↓
Controlled Runtime
      ↓
Verification
      ↓
Trace
~~~

Memory가 필요하다는 증거가 생기면 Memory를 추가한다.

Long-running Recovery가 필요하면 Durable State를 추가한다.

Specialist Isolation의 이득이 Coordination Cost보다 커지면 Multi-Agent를 검토한다.

Component는 유행이 아니라 반복해서 관찰된 요구와 실패에서 추가한다.

### Part I에서 남은 질문

1장에서 Model과 Agent를 분리했다.

2장에서 Agent Loop 주변에 필요한 Control을 살펴봤다.

이 장에서는 그 Control을 Harness라는 Software Layer로 묶었다.

하지만 아직 중요한 문제가 남아 있다.

Harness가 Model에게 다음 Turn을 요청할 때 무엇을 보여줘야 할까.

Conversation History 전체인가. Repository 전체인가. 모든 Tool Schema인가. 이전 실패 로그 전체인가.

Agent가 사용할 수 있는 정보는 많지만 Model의 Attention은 제한돼 있다.

다음 장에서는 **Context는 저장소가 아니다**라는 원칙에서 시작한다. Durable State와 현재 Inference Context를 분리하고, 필요한 정보만 Model에게 Projection하는 방법을 살펴본다.

### Source Notes

- [S-ANTHROPIC-HARNESS]
- [S-ANTHROPIC-MANAGED]
- [B-HARNESS-DEBT]
