# 1장. Model과 Agent는 무엇이 다른가

같은 모델을 사용했는데도 어떤 Agent는 일을 끝내고, 어떤 Agent는 같은 자리를 맴돈다.

둘 다 같은 LLM을 쓴다. 둘 다 Repository를 읽을 수 있고 Shell도 실행할 수 있다. 그런데 하나는 필요한 파일을 찾고, 테스트를 실행하고, 실패를 수정하고, 결과를 남긴다. 다른 하나는 이미 읽은 파일을 다시 읽고, 같은 명령을 반복하고, 마지막에는 "완료했다"고 말하지만 실제 테스트는 실패한 상태로 남아 있다.

차이는 모델 이름만으로 설명하기 어렵다.

이 책은 바로 이 차이를 다룬다.

## 모델이 좋아지면 Agent도 자동으로 좋아지는가

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

## Agent는 Prompt + Model이 아니다

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

하지만 production에서 사용할 Agent는 이 반복만으로 충분하지 않다.

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

## Agent Capability를 구성하는 것

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

### Model

현재 입력과 Tool 결과를 보고 다음 판단을 만든다.

모델이 약하면 복잡한 Repository를 이해하지 못하거나 잘못된 Tool을 선택할 수 있다.

### Instruction

Agent가 따라야 할 역할과 제약을 전달한다.

하지만 Instruction은 권한 시스템이 아니다. "프로덕션 DB를 수정하지 마라"라는 자연어 문장이 실제 DB Credential을 제거해주지는 않는다.

### Context

현재 Inference에서 모델이 볼 수 있는 정보다.

너무 적으면 필요한 사실을 놓친다. 너무 많으면 중요한 정보가 묻히거나 오래된 정보가 현재 사실처럼 남을 수 있다.

### Tool Interface

Agent가 외부 세계에 Action을 수행하는 인터페이스다.

같은 API라도 Agent에게 어떤 이름, Schema, 결과 형태로 제공하는지에 따라 실제 사용성이 달라질 수 있다.

SWE-agent는 이를 Agent-Computer Interface, ACI라는 관점으로 설명했다. 핵심은 모델이 같더라도 컴퓨터와 상호작용하는 인터페이스 설계가 성능에 영향을 준다는 것이다.

### Harness

모델을 반복 실행하는 제어 계층이다.

Context를 만들고, Tool을 Dispatch하고, Stop Condition을 판단하고, Retry와 Handoff를 처리한다.

### State

현재 작업이 어디까지 진행됐는지 보존한다.

장시간 작업에서는 Context Window보다 State가 더 중요해지는 순간이 온다.

### Memory

이전 실행에서 얻은 정보를 이후 작업에 재사용한다.

하지만 잘못된 Memory가 저장되면 미래 실행까지 오염될 수 있다.

### Runtime

실제 Side Effect가 발생하는 환경이다.

Filesystem, Network, Browser, Shell, Container, VM 등이 여기에 속한다.

### Identity와 Policy

누가 행동하는지, 어떤 권한으로 무엇을 할 수 있는지를 결정한다.

### Evaluation

Agent 변경이 실제로 좋아졌는지 확인한다.

Harness를 바꾸거나 Model을 업그레이드했는데 Eval이 없다면 개선과 회귀를 구분하기 어렵다.

## 같은 모델, 다른 Agent

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

## Framework는 Architecture가 아니다

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

Framework는 구현 도구다.

Architecture는 책임의 배치다.

이 책이 특정 SDK 사용법보다 Responsibility Boundary에 집중하는 이유다.

## Model, Harness, Runtime을 먼저 나눈다

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

## Agent State Plane

이 책에서 중요한 개념 하나를 미리 소개한다.

장시간 작업에서는 Agent가 다음 정보를 잃지 않아야 한다.

- 현재 Goal
- 어디까지 진행했는가
- 어떤 Tool이 이미 실행됐는가
- 어떤 Artifact가 만들어졌는가
- 어떤 Approval을 기다리고 있는가
- 어떤 외부 Source Version을 기준으로 판단했는가

이 책에서는 이런 실행 연속성을 담당하는 계층을 **Agent State Plane**이라고 부른다.

이 표현은 업계 표준 명칭이 아니라 이 책이 여러 구현과 연구를 설명하기 위해 사용하는 synthesis다.

~~~text
Agent State Plane
- Event History
- Checkpoint
- Goal / Progress
- Artifact
- Approval State
- Source Version
- Memory Reference
~~~

중요한 점은 이것이 Context와 다르다는 것이다.

~~~text
State Plane
   ↓ 필요한 정보만 Projection
Context Engine
   ↓
Model
~~~

모델이 모든 State를 항상 볼 필요는 없다.

반대로 모델이 현재 Context에서 잊었다고 해서 시스템까지 상태를 잃어서는 안 된다.

## 더 많은 자율성이 먼저는 아니다

Agent 시스템을 만들 때 눈에 잘 띄는 기능부터 추가하기 쉽다.

- Memory
- Planner
- Subagent
- Multi-Agent
- Browser
- Computer Use

하지만 production에서 더 먼저 필요한 것은 대개 Control과 Verification이다.

최소 Agent는 다음처럼 시작할 수 있다.

~~~text
Model
+ Clear Instruction
+ Small Tool Surface
+ Controlled Runtime
+ Deterministic Verification
+ Trace
~~~

그리고 필요할 때 확장한다.

~~~text
Minimal Agent
→ Tool Contract
→ Reproducible Runtime
→ Trace
→ Eval
→ Durable State
→ Identity / Policy
→ Memory
→ Long-running
→ Multi-Agent
~~~

이 순서가 유일한 정답은 아니다.

핵심은 Agent의 기능 수를 성숙도로 보지 않는 것이다.

## 이 책이 다루는 경계

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

## 이 장에서 가져갈 것

Model과 Agent를 같은 것으로 보면 실패 원인을 잘못 찾기 쉽다.

Agent가 일을 끝내는 능력은 Model뿐 아니라 Context, Tool, Harness, State, Runtime, Identity, Verification이 함께 만든다.

따라서 Agent Engineering의 첫 질문은 "어떤 모델을 쓸 것인가"가 아니다.

> 모델의 판단을 실제 행동으로 바꾸는 과정에서 어떤 책임을 어디에 둘 것인가?

다음 장에서는 이 구조의 가장 작은 실행 단위인 Agent Loop를 다룬다. Model이 Tool을 호출하고 Observation을 다시 읽는 단순 반복이 production 환경에서 어떤 Control을 필요로 하는지 살펴본다.

## 주요 근거

- OpenAI Agents SDK / Running Agents
- Anthropic, Building Effective Agents
- Anthropic, Scaling Managed Agents
- SWE-agent, Agent-Computer Interfaces Enable Automated Software Engineering
- research/topics/01-agent-loop-runtime.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
