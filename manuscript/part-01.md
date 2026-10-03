# Part I. Model에서 Agent로

Part I은 세 질문에서 시작한다.

~~~text
Model과 Agent는 무엇이 다른가?
Agent는 어떻게 반복 실행되는가?
그 실행 Control을 어디에 둘 것인가?
~~~

모델 자체의 성능보다 모델을 실제 행동으로 연결하는 실행 구조와 책임 경계를 먼저 고정한다.

<!-- source-draft: chapters/01/draft.md -->

## 1장. Model과 Agent는 무엇이 다른가

같은 모델을 사용했는데도 어떤 에이전트는 일을 끝내고, 어떤 에이전트는 같은 자리를 맴돈다. 둘 다 같은 LLM을 쓴다. 둘 다 저장소를 읽을 수 있고 셸도 실행할 수 있다. 그런데 하나는 필요한 파일을 찾고, 테스트를 실행하고, 실패를 수정하고, 결과를 남긴다. 다른 하나는 이미 읽은 파일을 다시 읽고, 같은 명령을 반복하고, 마지막에는 "완료했다"고 말하지만 실제 테스트는 실패한 상태로 남아 있다. 이 차이는 모델 이름만으로 설명하기 어렵다. 이 책은 같은 모델을 쓰는 에이전트가 왜 서로 다른 결과를 내는지 다룬다.

### 모델이 좋아지면 Agent도 자동으로 좋아지는가

LLM을 사용할 때 가장 눈에 잘 띄는 변화는 모델 성능이다. 새로운 모델이 나오면 추론, 코딩, 도구 사용 능력을 비교하는 평가 점수가 올라간다. 자연스럽게 다음 결론으로 이어지기 쉽다.

> 더 좋은 모델을 사용하면 더 좋은 에이전트가 된다.

일부는 맞다. 더 강한 모델은 복잡한 코드를 더 잘 읽고, 더 적절한 도구를 선택하고, 긴 작업에서도 더 나은 판단을 할 수 있다. 하지만 이것만으로 실제 에이전트의 능력을 설명할 수는 없다. 예를 들어 모델이 정확하게 다음 도구 호출을 제안했다고 하자.

~~~text
delete_file("/tmp/build/result.json")
~~~

에이전트 시스템에서는 그 뒤에 더 많은 일이 일어난다.

- 이 도구를 현재 에이전트가 사용할 권한이 있는가.
- 경로가 허용된 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경) 안에 있는가.
- 이 작업은 승인 없이 실행해도 되는가.
- 도구 실행이 실패하면 다시 시도할 것인가.
- 성공 결과를 다음 컨텍스트(Context: 모델에 전달하는 정보)에 얼마나 넣을 것인가.
- 이 변경을 상태에 기록할 것인가.
- 프로세스가 죽으면 이 도구를 다시 실행해도 되는가.

모델은 행동을 제안할 수 있다. 실제 행동을 어떻게 실행하고 통제할지는 시스템의 책임이다. 이 책에서는 이 차이를 다음처럼 표현한다.

~~~text
Model Capability
≠ Agent Capability
~~~

이 식은 모델이 중요하지 않다는 뜻이 아니다. 에이전트의 실제 능력을 모델 하나의 속성으로 축약하지 말자는 뜻이다.

### Agent는 Prompt + Model이 아니다

가장 단순한 LLM 애플리케이션은 다음과 같다.

~~~text
Prompt
  ↓
Model
  ↓
Response
~~~

여기에 도구 호출 기능을 붙이면 조금 달라진다.

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

여기서부터 에이전트에 가까워진다. 모델이 외부 환경을 관찰하고 행동을 선택하며 결과를 다시 읽기 때문이다. 하지만 운영 환경에서 사용할 에이전트는 이 반복만으로 충분하지 않다. 운영 시스템에서는 적어도 다음 질문이 생긴다.

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

이 질문들은 모델 내부의 문제가 아니다. 에이전트를 둘러싼 실행 시스템의 문제다.

### Agent Capability를 구성하는 것

에이전트의 능력(Agent Capability: 에이전트가 실제로 할 수 있는 일)은 다음과 같은 함수로 생각할 수 있다.

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

정확한 수학식은 아니다. 에이전트 성능에 영향을 주는 책임을 분리하기 위한 개념식이다. 각 항목은 서로 다른 실패를 만든다.

#### Model

현재 입력과 도구 결과를 보고 다음 판단을 만든다. 모델이 약하면 복잡한 저장소를 이해하지 못하거나 잘못된 도구를 선택할 수 있다.

#### Instruction

에이전트가 따라야 할 역할과 제약을 전달한다. 하지만 지침 자체가 권한을 통제하는 시스템은 아니다. "프로덕션 DB를 수정하지 마라"라는 자연어 문장이 실제 DB 인증 정보를 제거해주지는 않는다.

#### Context

현재 한 번의 실행에서 모델이 볼 수 있는 정보다. 너무 적으면 필요한 사실을 놓친다. 너무 많으면 중요한 정보가 묻히거나 오래된 정보가 현재 사실처럼 남을 수 있다.

#### Tool Interface

에이전트가 외부 세계에 행동을 수행하는 인터페이스다. 같은 API라도 에이전트에게 어떤 이름, 데이터 형식, 결과 형태로 제공하는지에 따라 실제 사용성이 달라질 수 있다. SWE-agent 연구는 이를 에이전트와 컴퓨터가 상호작용하는 인터페이스(Agent-Computer Interface, ACI)라는 관점으로 다뤘다. 이 용어를 모든 도구 시스템의 표준명으로 쓰려는 것은 아니다. 핵심은 같은 모델을 사용해도 컴퓨터와 상호작용하는 인터페이스 설계에 따라 실제 성능이 달라질 수 있다는 점이다.

#### Harness

모델을 반복 실행하는 제어 계층이다. 모델에 전달할 정보를 구성하고, 도구를 실행할 곳에 보내며, 멈출 조건을 판단한다. 실패하면 다시 시도하거나 다른 실행 주체에게 작업을 넘기는 과정도 관리한다.

#### State

현재 작업이 어디까지 진행됐는지 보존한다. 장시간 작업에서는 컨텍스트 윈도(Context Window: 모델이 한 번에 입력받을 수 있는 정보의 범위)보다 상태가 더 중요해지는 순간이 온다.

#### Memory

이전 실행에서 얻은 정보를 이후 작업에 재사용한다. 하지만 잘못된 정보를 메모리에 저장하면 이후 실행에도 오류가 이어질 수 있다.

#### Runtime

실제 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)가 발생하는 환경이다. 파일 시스템, 네트워크, 브라우저, 셸, 컨테이너, VM 등이 여기에 속한다.

#### Identity와 Policy

누가 행동하는지, 어떤 권한으로 무엇을 할 수 있는지를 결정한다.

#### Evaluation

에이전트 변경이 실제로 좋아졌는지 확인한다. 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)를 바꾸거나 모델을 업그레이드했는데 평가가 없다면 개선과 회귀를 구분하기 어렵다.

### 같은 모델, 다른 Agent

가상의 두 코드 작업 에이전트를 비교해보자. 에이전트 A는 다음 구조다.

~~~text
Strong Model
+ Repository 전체를 항상 Context에 넣음
+ Shell Tool 하나
+ Workspace 밖 접근 가능
+ Conversation History만 저장
+ Agent가 "완료"하면 종료
~~~

에이전트 B는 다음 구조다.

~~~text
Same Strong Model
+ 필요한 파일만 Progressive Context
+ Search / Read / Edit / Test Tool 분리
+ Workspace Sandbox
+ Goal / Progress State
+ Test Result 기반 Completion
+ Trace / Retry
~~~

두 시스템은 같은 모델을 사용한다. 하지만 실제 작업에서는 상당히 다른 행동을 보일 수 있다. 에이전트 A는 사용 가능한 도구의 범위가 지나치게 넓고, 완료를 판정할 권한이 모델 자신에게 있으며, 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)가 없다. 에이전트 B는 행동 공간과 완료 판정을 시스템에서 더 명확하게 제한한다. 따라서 에이전트 A의 실패를 보고 "모델이 부족하다"고 결론 내리면 잘못된 문제를 고치게 된다. 모델을 바꿔도 같은 구조적 실패가 반복될 수 있다.

### Framework는 Architecture가 아니다

또 하나 자주 생기는 혼동이 있다. 어떤 에이전트 프레임워크를 선택하면 에이전트 설계 구조가 정해졌다고 생각하는 것이다. 프레임워크는 유용하다. 예를 들어 어떤 SDK는 다음 기능을 제공할 수 있다.

- 도구 호출 기능
- 작업 인계
- 세션
- Guardrail
- 실행 추적 기록(Trace)
- MCP Integration

하지만 이 기능이 존재한다고 해서 다음 설계가 자동으로 결정되지는 않는다.

- 세션과 장기 메모리를 어떻게 나눌 것인가.
- 어떤 도구를 어떤 신원이 호출할 수 있는가.
- 위험한 상태 변경에 어떤 승인을 둘 것인가.
- 비정상 종료 후 어떤 상태를 복구할 것인가.
- 완료를 어떤 근거로 판정할 것인가.

프레임워크는 구현을 돕는 도구다. 시스템 설계는 각 부분에 어떤 책임을 맡길지 정하는 일이다. 따라서 이 책은 특정 SDK의 기능 목록보다 각 책임을 어디에 둘지에 집중한다.

### Model, Harness, Runtime을 먼저 나눈다

에이전트 구조를 처음 볼 때는 세 덩어리로 나누는 것이 유용하다.

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

이 구분만으로도 여러 잘못된 설계를 피할 수 있다. 예를 들어 "모델이 위험한 파일을 삭제하지 않도록 프롬프트를 강화한다"는 대응은 Model/Harness 쪽 통제다. 반면 "해당 파일을 샌드박스에서 연결하지 않는다"는 실행 환경 통제다. 둘은 같은 문제가 아니다.

### Agent State Plane

장시간 작업에서는 현재 목표와 진행 상황, 이미 실행한 행동, 생성한 산출물, Pending Approval을 잃지 않아야 한다. 이 책에서는 이런 **한 에이전트 실행의 연속성**을 담당하는 계층을 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)이라고 부른다. 외부 표준 명칭이 아니라 여러 구현과 연구에서 반복되는 책임을 설명하기 위한 설명용 개념이다. 핵심은 컨텍스트와 영속 상태를 분리하는 것이다. 모델이 현재 컨텍스트에서 어떤 정보를 잊더라도 시스템까지 상태를 잃어서는 안 된다. 구성과 복구 방식은 Part III에서 자세히 다룬다.

### 더 많은 자율성이 먼저는 아니다

에이전트 시스템은 메모리, 계획기(Planner: 계획을 세우는 구성 요소), 하위 에이전트 같은 눈에 띄는 기능부터 추가하기 쉽다. 하지만 운영에서 더 먼저 필요한 것은 대개 작은 사용 가능한 도구의 범위, 통제된 실행 환경, 검증, 실행 추적 기록이다. 어떤 기능을 어떤 순서로 추가할지는 작업과 위험에 따라 달라진다. 핵심은 기능 수를 에이전트의 성숙도로 보지 않는 것이다. 실제 도입 순서는 25장에서 다시 정리한다.

### 이 책이 다루는 경계

에이전트 엔지니어링은 다른 세 영역과 맞닿아 있다. 첫째, Instruction Engineering이다. CLAUDE.md, AGENTS.md, Skill, 규칙, Hook을 어떻게 작성하고 검증할지는 별도의 문제다. 이 책에서는 그것들이 Agent Definition과 컨텍스트에 어떻게 들어오는지만 다룬다. 둘째, Cloud Agent다. 에이전트를 Local에서 실행할지 Cloud Runner에서 실행할지, Git으로 어떻게 작업 인계할지, Compute와 토큰 비용을 어떻게 나눌지는 실행 위치의 문제다. 셋째, AI Software Factory다. 여러 작업 항목과 작업 수행 주체를 어떻게 Scheduling하고 Acceptance와 Delivery를 관리할지는 한 에이전트 실행보다 상위 계층이다.

이 책은 그 경계를 다음처럼 유지한다.

~~~text
Agent State Plane
= 한 Agent 실행의 연속성

Software Factory Control Plane
= 여러 Work / Worker / Delivery의 연속성
~~~

### 이 장에서 가져갈 것

모델과 에이전트를 같은 것으로 보면 실패 원인을 잘못 찾기 쉽다. 에이전트가 일을 끝내는 능력은 모델뿐 아니라 컨텍스트, 도구, 하네스, 상태, 실행 환경, 신원, 검증이 함께 만든다. 따라서 에이전트 엔지니어링의 첫 질문은 "어떤 모델을 쓸 것인가"가 아니다.

> 모델의 판단을 실제 행동으로 바꾸는 과정에서 어떤 책임을 어디에 둘 것인가?

다음 장에서는 이 구조의 가장 작은 실행 단위인 에이전트의 실행 반복 과정을 다룬다. 모델이 도구를 호출하고 관찰 결과를 다시 읽는 단순 반복이 운영 환경에서 어떤 통제를 필요로 하는지 살펴본다.

### Source Notes

- [B-AGENT-CAPABILITY]
- [S-SWE-ACI]
- [S-OAI-AGENTS]
- [S-ANTHROPIC-AGENTS]

---

<!-- source-draft: chapters/02/draft.md -->

## 2장. Agent Loop를 설계한다

에이전트를 가장 짧게 구현하면 몇 줄짜리 반복문이 될 수 있다. 모델에 메시지를 보낸다. 도구 호출이 나오면 도구를 실행한다. 결과를 다시 모델에 전달한다. 모델이 최종 답변을 내면 끝낸다. 개념을 이해하기에는 충분하다. 하지만 실제 시스템에서는 바로 질문이 생긴다. 도구가 5분 동안 응답하지 않으면 어떻게 할까. 같은 도구가 세 번 실패하면 계속 시도할까. 외부 API는 성공했는데 에이전트 프로세스가 결과를 저장하기 전에 죽으면 어떻게 할까. 모델이 완료했다고 했지만 테스트가 실패하면 끝낼까. 에이전트의 실행 반복 과정은 단순한 반복문에서 시작하지만 운영 환경에서는 하나의 작은 실행 제어 시스템이 된다.

### 최소 Loop

에이전트의 최소 구조는 다음과 같이 표현할 수 있다.

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

ReAct 계열 연구에서 널리 알려진 것처럼 에이전트는 reasoning과 action을 번갈아 수행하며 환경의 observation을 다음 판단에 반영한다. 중요한 것은 추론을 적은 문장 자체보다, 환경과 상호작용하면서 다음 행동을 선택한다는 점이다.

### Tool Call이 Action은 아니다

모델이 도구 호출을 생성했다고 해서 행동이 이미 실행된 것은 아니다.

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

이 구분은 뒤의 보안 장에서 더 중요해진다. 모델은 다음 JSON을 만들 수 있다.

~~~text
{
  "tool": "create_pull_request",
  "base": "main",
  "head": "feature-x"
}
~~~

하지만 실제 시스템은 이 행동을 실행하기 전에 확인할 수 있다.

- 현재 에이전트에게 PR 생성 권한이 있는가.
- 대상 저장소가 허용 범위인가.
- 브랜치가 보호 규칙을 위반하지 않는가.
- 현재 작업이 상태 변경을 허용하는가.

즉 Model Decision과 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화) 사이에는 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)와 Policy Boundary가 존재한다.

### 운영 Loop가 추가로 가져야 하는 것

최소 반복 실행에는 보이지 않지만 실제 에이전트에 필요한 책임이 있다.

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

모델의 완료 선언을 실제 완료로 인정할 것인가. 이 중 하나라도 없으면 에이전트는 쉬운 데모에서는 동작해도 긴 작업에서는 불안정해질 수 있다.

### Stop Condition은 모델의 기분이 아니다

가장 단순한 에이전트는 모델이 final output을 반환하면 끝난다. 대화형 Assistant라면 충분할 수 있다. 하지만 작업형 에이전트는 다르다. 예를 들어 목표가 다음과 같다고 하자.

> failing test를 수정하라.

모델이 "수정했습니다"라고 답했더라도 테스트가 여전히 실패하면 작업은 끝나지 않았다. 따라서 멈출 조건을 둘로 나눠볼 수 있다.

~~~text
Conversation Stop
= 모델이 더 이상 Tool Call을 하지 않음

Task Completion
= 외부 Success Condition이 만족됨
~~~

둘은 다를 수 있다. 운영 에이전트에서는 가능하면 완료를 외부 근거에 연결한다.

예:

- Test Pass
- File Exists
- Expected DB State
- Browser State
- Artifact Validation

모델이 스스로 보고한 내용은 참고할 수 있지만, 그 보고만으로 완료를 판정하지는 않도록 한다.

### Loop에는 Budget이 필요하다

에이전트가 실패하면 흔히 "한 번 더 해보자"고 생각한다. 하지만 재시도가 무제한이면 같은 실패를 반복할 수 있다. 실행 한도는 여러 종류가 있다.

- Max Turn
- Max Tool Call
- Time
- 토큰
- 비용
- 재시도 횟수
- External API Quota

실행 한도의 목적은 비용 절약만이 아니다. 에이전트가 progress 없이 반복하는 상황을 정상적인 Failure State로 바꾸는 역할도 한다.

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

도구 실행 실패 하나를 생각해보자.

~~~text
git push
→ 403 Forbidden
~~~

이 실패를 다섯 번 재시도해도 해결되지 않을 가능성이 높다.

반면:

~~~text
HTTP 503
~~~

은 잠시 뒤 성공할 수 있다. 따라서 실패를 분류해야 한다.

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

실제 분류 방식은 시스템마다 다르다. 중요한 것은 실패를 참과 거짓, 두 값만으로 표현할 수 없다는 점이다.

### Retry도 State를 가져야 한다

같은 도구를 다시 호출하더라도 이전 시도와 무엇이 다른지 알아야 한다.

나쁜 재시도:

~~~text
Fail
→ Same Context
→ Same Action
→ Fail
→ Same Context
→ Same Action
~~~

좋은 재시도는 적어도 새로운 정보가 있어야 한다.

~~~text
Fail
→ Inspect Error
→ Update Hypothesis / Context / Input
→ Retry
~~~

또는 단순 transient error라면 exponential backoff 같은 시스템이 정해진 규칙으로 적용하는 정책이 모델 판단보다 낫다. 이미 알고 있는 규칙을 모델에게 매번 판단시키지 않는다.

### Interruption은 정상 상태다

에이전트가 모든 상황을 독립적으로 결정해야 할 필요는 없다.

예를 들어:

- 결제 승인
- 운영 환경 배포
- 개인정보 포함 데이터 전송
- 요구사항의 중요한 ambiguity

는 사람의 판단을 기다리는 것이 정상일 수 있다. 이때 에이전트를 실패 처리하는 대신 상태를 둔다.

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

중요한 것은 일시 중지 상태에서 프로세스를 계속 살려둘 필요가 없다는 점이다. 상태가 외부에 저장돼 있다면 실행 환경을 종료했다가 이후 다시 만들 수 있다. 이 지점에서 에이전트의 실행 반복 과정과 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)가 연결된다.

### Resume는 Prompt를 다시 보내는 것이 아니다

일시 중지 후 다음 날 사용자가 승인했다고 하자. 가장 단순한 구현은 이전 대화 요약을 새 모델에 넣고 "계속해"라고 말하는 것이다. 짧은 작업에서는 동작할 수 있다. 하지만 다음 정보가 중요하다면 부족하다.

- 이미 어떤 도구가 실행됐는가.
- 외부 상태 변경이 성공했는가.
- 어떤 산출물이 만들어졌는가.
- 어떤 버전의 정보 원본을 기준으로 판단했는가.
- 승인 대상 행동은 정확히 무엇이었는가.

실행 재개는 Conversation Continuation 이상의 문제다. 이 책에서 뒤에 다룰 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)이 필요한 이유다.

### Tool Failure와 Model Failure를 분리한다

에이전트 시스템에서는 여러 계층이 동시에 실패할 수 있다.

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

이들을 모두 "Agent Error" 하나로 기록하면 개선하기 어렵다. 실행 추적 기록(Trace)과 평가에서도 같은 분리가 필요하다.

### Handoff도 하나의 Transition이 될 수 있다

여러 에이전트의 협업 구조에서는 도구 호출 대신 다른 에이전트로 담당 책임을 넘기는 상태 전환이 들어갈 수 있다. 다만 이 책에서는 이를 기본 반복 실행으로 두지 않는다. 단일 에이전트의 반복 실행과 상태, 도구의 사용 경계를 먼저 안정시킨 뒤 Part VII에서 작업 인계를 별도로 다룬다.

### Loop와 State Machine

에이전트의 실행 반복 과정을 설명할 때 모든 것을 엄격한 State Machine으로 만들 필요는 없다. LLM 판단 자체는 열려 있다. 대신 시스템이 확실히 알고 있는 부분은 명시적 상태로 두는 편이 좋다.

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

이런 상태는 모델의 자유 텍스트보다 시스템의 Transition Rule로 관리하는 편이 낫다. 에이전트 엔지니어링에서는 불확실한 판단과 기계적으로 판정 가능한 규칙을 나눈다.

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

최소 반복 실행:

~~~text
Read Failure
→ Inspect Code
→ Edit
→ Run Test
→ PASS?
    ├─ Yes → Complete
    └─ No  → Inspect Failure → Retry
~~~

운영 반복 실행에서는 조금 더 필요하다.

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

여기서 중요한 것은 모델의 지능만이 아니라 반복 실행 주변의 통제 구조다.

### Loop는 어디까지 Harness 책임인가

에이전트의 실행 반복 과정을 운영 수준으로 만들면서 책임이 계속 추가됐다.

- 컨텍스트(Context: 모델에 전달하는 정보)
- 도구 호출 전달
- 재시도
- Stop
- 실행 한도
- 일시 중지 / 실행 재개
- 검증
- 실행 추적 기록

이 책임을 묶어 관리하는 계층이 필요하다. 이 책에서는 이를 하네스라고 부른다. 하네스는 특정 프레임워크 제품을 뜻하지 않는다. 모델을 실제 실행 가능한 에이전트로 만드는 Control Logic이다. 다음 장에서는 하네스가 어디까지 책임져야 하며, 왜 기능을 많이 넣는 것이 항상 좋은 하네스를 의미하지 않는지 살펴본다.

### Source Notes

- [S-REACT]
- [S-OAI-AGENTS]
- [S-GOOGLE-ADK]

---

<!-- source-draft: chapters/03/draft.md -->

## 3장. Harness Engineering

에이전트가 실패할 때마다 새로운 규칙을 하나 추가하는 것은 쉽다. 계획을 자주 잊으면 계획기(Planner: 계획을 세우는 구성 요소)를 붙인다. 컨텍스트(Context: 모델에 전달하는 정보)가 길어지면 컨텍스트 압축(Compaction: 입력 정보를 줄이는 압축)을 붙인다. 완료를 너무 빨리 선언하면 평가기(Evaluator: 결과를 평가하는 구성 요소)를 붙인다. 작업이 복잡하면 하위 에이전트를 붙인다. 이전 실수를 반복하면 메모리를 붙인다. 몇 달 뒤에는 아무도 전체 구조를 정확히 설명하지 못하는 에이전트가 만들어질 수 있다. 기능이 많다는 사실보다 더 큰 문제는 각 기능이 왜 존재하는지, 실제로 어떤 실패를 줄이는지 알 수 없다는 점이다. 하네스 설계는 이 문제를 다룬다.

### Harness란 무엇인가

이 책에서 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)는 다음과 같이 정의한다.

> **하네스는 모델을 반복 실행 가능한 에이전트로 만들기 위해 컨텍스트, 도구, 상태, 통제를 연결하는 실행 제어 계층이다.**

구성은 시스템마다 다를 수 있다. 대표적인 책임은 다음과 같다.

- Context Assembly
- 에이전트의 실행 반복 과정
- 도구 호출 전달
- 멈출 조건
- 재시도
- 실행 한도
- Interruption / 실행 재개
- 작업 인계
- Verification Hook
- Trace Emission

중요한 것은 특정 라이브러리 이름이 아니다. OpenAI Agents SDK, Google ADK, 자체 반복 실행, 다른 프레임워크 중 무엇을 사용하더라도 이 책임은 어딘가에 존재해야 한다.

### Framework와 Harness는 다르다

프레임워크는 하네스를 구현하는 수단이 될 수 있다. 하지만 프레임워크를 선택했다고 하네스 설계가 끝나지는 않는다. 예를 들어 SDK가 세션 기능을 제공한다고 하자. 여전히 다음을 결정해야 한다.

- 세션에 무엇을 저장할 것인가.
- 목표는 세션과 같은 유지 과정인가.
- 외부 도구 결과를 얼마나 저장할 것인가.
- 비정상 종료 뒤 복구는 세션만으로 충분한가.
- 장기 메모리와 어떻게 분리할 것인가.

SDK가 Guardrail API를 제공해도 다음은 별도 문제다.

- 실제 파일 시스템 접근 범위
- Network Egress
- 인증 정보로 행사할 수 있는 권한 범위
- Production Mutation Approval

하네스 설계는 API 목록을 조합하는 일이 아니다. 책임을 어디에 두고 무엇을 시스템이 강제할지 결정하는 일이다.

### Minimal Harness에서 시작한다

처음부터 많은 구성 요소를 넣지 않는 편이 좋다. 최소 구조는 다음 정도로 시작할 수 있다.

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

이 구조로도 많은 작업을 처리할 수 있다. 여기서 반복되는 실패를 관찰한 뒤 구성 요소를 추가한다. 예를 들어 장시간 코드 작업에서 모델이 Context Limit에 가까워지면 작업을 조기 종료하는 문제가 반복된다고 하자. 그때 다음 후보를 검토할 수 있다.

- Context Reset
- Progress Artifact
- Goal State
- Session Continuation

중요한 것은 "오래 실행되는 에이전트에는 Progress File이 필수다"라고 일반화하지 않는 것이다. 특정 실패를 해결하기 위해 도입했으며, 모델과 작업이 바뀌면 다시 검증해야 한다.

### Harness는 Model에 대한 가정을 담는다

하네스의 많은 기능은 사실 모델의 약점을 보완하기 위해 생긴다.

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

이 가정이 언제까지나 맞는 것은 아니다. 모델이 좋아지면 일부 모델의 약점을 보완하는 보조 장치는 가치가 줄어들 수 있다. Anthropic이 Managed Agents와 장시간 작업용 하네스 관련 자료에서 강조하는 부분도 이 지점이다. 하네스는 모델이 못한다고 가정하는 부분을 보완하지만, 모델이 발전하면 그 가정이 오래된 것이 될 수 있다. 따라서 하네스를 고정 인프라처럼 취급해서는 안 된다. 모델이 바뀌면 기존 모델의 약점을 보완하는 보조 장치의 필요성도 다시 측정해야 한다.

### Harness, Runtime, Durable State를 분리한다

운영 책임은 비유보다 실제 유지 과정으로 나누는 편이 명확하다.

~~~text
Harness
= 실행 제어 로직

Runtime
= 실제 Tool과 Side Effect가 실행되는 환경

Durable State
= Process와 Runtime이 사라져도 남아야 하는 실행 정보
~~~

이렇게 분리하면 실행 환경을 교체하거나 폐기해도 목표와 진행 상황을 복구할 수 있다.

~~~text
Disposable Runtime
+
Durable State
~~~

이 조합은 오래 실행되는 에이전트의 복구 구조를 단순하게 만든다. 세션, 작업 공간, 목표, 메모리의 세부 경계는 Part III에서 다시 정리한다.

### Harness가 너무 많은 일을 하면 생기는 문제

에이전트가 실패할 때마다 모델의 약점을 보완하는 보조 장치를 추가하면 복잡성이 증가한다.

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
각 구성 요소가 지침, 도구의 입력 형식, Intermediate Result를 컨텍스트에 추가할 수 있다.

#### Latency
계획기 → 실행 담당자 → 검토 담당자 구조는 단일 실행보다 차례와 모델 호출이 늘어난다.

#### Coordination Failure
구성 요소 사이에 다른 상태가 생길 수 있다.

계획기는 완료됐다고 생각하지만 실행 담당자는 다른 목표를 따를 수 있다.

#### Debugging Difficulty
최종 결과가 나빠졌을 때 어떤 구성 요소가 원인인지 알기 어렵다.

#### Stale Assumption
예전 모델의 약점을 보완한 규칙이 새 모델의 좋은 행동을 방해할 수 있다.

이 책에서는 이런 누적을 **Harness Debt**라고 부른다. 이 역시 외부 표준 용어가 아니라 이 책의 설명용 개념이다.

### Harness Component는 가설이다

하네스를 관리하는 가장 실용적인 방법은 각 구성 요소를 하나의 가설로 보는 것이다. 예를 들어 계획기를 추가하려 한다.

가설:

> 많은 단계에 걸친 작업에서 upfront plan을 생성하면 Completion Rate가 올라간다.

그러면 검증 방법도 같이 필요하다.

~~~text
Baseline Harness
vs
Baseline + Planner
~~~

비교 대상:

- Task Success
- 비용
- 응답 지연 시간
- Human Intervention
- 보안
- Repeated Reliability

예를 들어 계획기가 성공률을 조금 높이더라도 응답 지연 시간과 비용을 크게 늘린다면 모든 작업에 적용할 이유는 없다. 실제 판단은 반복 평가와 작업별 효과를 보고 내려야 한다.

### Component Record

하네스가 커지면 각 구성 요소가 어떤 실패 때문에 들어왔고, 어떤 평가가 효과를 확인했으며, 마지막으로 어느 모델에서 검증됐는지 기록하는 편이 좋다. 이 기록은 모델 교체 때 제거 후보를 찾고 "왜 이 구성 요소가 존재하는가"를 Commit History에서 다시 추측하는 비용을 줄인다. 구체적인 기록과 제거 비교 실험(Ablation: 구성 요소를 빼고 효과를 비교하는 실험) 절차는 21장에서 다룬다.

### Harness와 State를 분리한다

하네스가 모든 상태를 프로세스 메모리로 가지고 있으면 비정상 종료 뒤 복구가 어려워진다.

예를 들어:

~~~text
Harness Process
- current step
- approval pending
- completed tools
- generated artifact path
~~~

만 가지고 있다면 프로세스가 죽는 순간 정보가 사라진다. 따라서 장시간 에이전트에서는 하네스와 상태 저장소의 경계가 중요해진다.

~~~text
Harness
  ↔
Agent State Plane
~~~

하네스는 상태를 읽고 상태 전환을 만든다. 상태 관리 계층은 Process Lifetime 밖에서 필요한 정보를 유지한다. 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)은 Part III에서 이 구조를 자세히 다룬다.

### Harness와 Runtime도 분리한다

하네스가 셸을 실행한다고 해서 하네스 자체가 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)여야 하는 것은 아니다.

~~~text
Harness
  ↓ Action Request
Tool / Capability Gateway
  ↓
Execution Runtime
~~~

실행 환경은 다음을 강제할 수 있다.

- File System Scope
- Network Scope
- Process Isolation
- Credential Injection

하네스의 자연어 지침보다 더 deterministic한 경계다. 이 분리를 유지하면 모델과 하네스를 바꾸더라도 Runtime Policy를 독립적으로 유지할 수 있다.

### Harness와 Verification

하네스의 중요한 책임 중 하나는 완료했다는 주장을 실제 검증으로 연결하는 것이다.

예를 들어 코드 작업 에이전트에서:

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

검증을 모델에게 다시 물어보는 것과 실제 테스트를 실행하는 것은 다르다. 가능한 한 deterministic한 검증이 있으면 그것을 우선한다.

### Harness 변경은 Versioning 대상이다

에이전트 결과를 비교할 때 모델 버전만 기록하면 부족하다. 하네스 변경 하나만으로도 행동이 달라질 수 있다.

예:

- 도구 설명 수정
- 재시도 횟수 변경
- 계획기 추가
- Memory Retrieval 변경
- Context Compaction 변경
- Sandbox Policy 변경

따라서 뒤의 평가 장에서는 AgentVersion를 모델보다 넓은 Tuple로 다룬다. 이 장에서는 최소한 다음 원칙만 기억하면 된다.

> 하네스도 배포되는 Software다.

변경 이력과 회귀(Regression: 변경 뒤 기존 기능이 나빠지는 회귀)가 필요하다.

### Model Upgrade는 Harness Audit Trigger다

새 모델이 출시됐다고 기존 하네스를 그대로 유지해야 하는 것은 아니다. 먼저 기존 하네스와 단순한 비교 기준을 비교하고, 계획기·메모리·평가기 같은 구성 요소가 여전히 필요한지 다시 측정한다. 이 책에서는 이런 검증을 하네스 구성 요소의 제거 비교 실험으로 다룬다. 반복 실행과 Variance를 포함한 구체적인 방법은 21장에서 설명한다.

### 지금 필요한 것만 남긴다

좋은 하네스는 기능이 가장 많은 하네스가 아니다. 현재 작업과 모델에서 필요한 책임을 명확히 가진 하네스다. 초기 운영 에이전트라면 다음 정도로도 시작할 수 있다.

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

메모리가 필요하다는 증거가 생기면 메모리를 추가한다. Long-running Recovery가 필요하면 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)를 추가한다. Specialist Isolation의 이득이 Coordination Cost보다 커지면 여러 에이전트의 협업을 검토한다. 구성 요소는 유행이 아니라 반복해서 관찰된 요구와 실패에서 추가한다.

### Part I에서 남은 질문

1장에서 모델과 에이전트를 분리했다. 2장에서 에이전트의 실행 반복 과정 주변에 필요한 통제를 살펴봤다. 이 장에서는 그 통제를 하네스라는 Software Layer로 묶었다. 하지만 아직 중요한 문제가 남아 있다. 하네스가 모델에게 다음 차례를 요청할 때 무엇을 보여줘야 할까. 대화 기록 전체인가. 저장소 전체인가. 모든 도구의 입력 형식인가. 이전 실패 로그 전체인가. 에이전트가 사용할 수 있는 정보는 많지만 모델의 Attention은 제한돼 있다. 다음 장에서는 **컨텍스트는 저장소가 아니다**라는 원칙에서 시작한다. 영속 상태와 현재 Inference Context를 분리하고, 필요한 정보만 모델에게 투영하는 방법을 살펴본다.

### Source Notes

- [S-ANTHROPIC-HARNESS]
- [S-ANTHROPIC-MANAGED]
- [B-HARNESS-DEBT]
