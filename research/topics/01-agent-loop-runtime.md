# Agent Loop and Runtime

## 질문

> 무엇이 단순 LLM 호출을 Agent 실행으로 바꾸는가?

## 공통 구조

OpenAI Agents SDK, ReAct 계열 연구, Google ADK 문서를 교차하면 최소 실행 루프는 다음처럼 정리할 수 있다.

~~~text
Input
  ↓
Prepare Context
  ↓
Model Inference
  ↓
Decision
  ├─ Final Output → Stop
  ├─ Tool Call → Execute → Observation ─┐
  └─ Handoff → New Agent / Specialist ─┤
                                        ↓
                               Prepare Next Context
                                        ↺
~~~

중요한 점은 Agent가 “reasoning을 한다”는 사실보다 환경의 상태를 읽고 action을 만들고 그 결과를 다음 inference에 반영하는 반복 시스템이라는 점이다.

## Model과 Agent의 경계

~~~text
Model
- token inference
- tool call intent 생성
- structured output 생성

Agent Harness
- context 구성
- loop 진행
- tool 호출 dispatch
- stop condition
- retry / interruption
- handoff
- state 연결
- tracing

Runtime
- process
- sandbox
- filesystem
- network
- credential
- actual side effect
~~~

이 분리는 책의 핵심 후보이다.

## Runner는 단순 반복문이 아니다

실제 production runner에는 보통 다음 책임이 추가된다.

- max turn / budget
- timeout
- cancellation
- approval pause/resume
- serialization
- retry
- exception normalization
- trace emission
- tool result filtering

따라서 “Agent = while loop”라는 설명은 교육용 최소 모델에는 유효하지만 production 정의로는 부족하다.

## Stop Condition

Agent loop는 언제 끝날지 명시해야 한다.

후보:

- final answer
- expected structured result
- task success predicate
- step limit
- token / cost budget
- timeout
- unrecoverable error
- human escalation

명시되지 않은 loop는 자율성이 아니라 통제되지 않은 실행이다.

## 연구에 반영할 원칙

1. Model과 Runner를 분리한다.
2. Reasoning과 Side Effect를 분리한다.
3. Stop condition은 Harness 책임으로 본다.
4. Tool execution failure를 model failure와 같은 것으로 취급하지 않는다.
5. Runtime resource와 environment는 Agent Capability에 포함되는 외부 변수다.

## 주요 근거

- OpenAI Agents SDK / Running agents
- ReAct
- Google ADK
- Anthropic Managed Agents
