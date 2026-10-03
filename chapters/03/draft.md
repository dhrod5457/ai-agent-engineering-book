# 3장. Harness Engineering

Agent가 실패할 때마다 새로운 규칙을 하나 추가하는 것은 쉽다.

계획을 자주 잊으면 Planner를 붙인다. Context가 길어지면 Compaction을 붙인다. 완료를 너무 빨리 선언하면 Evaluator를 붙인다. 작업이 복잡하면 Subagent를 붙인다. 이전 실수를 반복하면 Memory를 붙인다.

몇 달 뒤에는 아무도 전체 구조를 정확히 설명하지 못하는 Agent가 만들어질 수 있다.

문제는 기능이 많다는 사실 자체가 아니다.

각 기능이 왜 존재하는지, 실제로 어떤 실패를 줄이는지 알 수 없다는 점이다.

Harness Engineering은 이 문제를 다룬다.

## Harness란 무엇인가

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

## Framework와 Harness는 다르다

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

## Minimal Harness에서 시작한다

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

## Harness는 Model에 대한 가정을 담는다

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

## Harness, Runtime, Durable State를 분리한다

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

## Harness가 너무 많은 일을 하면 생기는 문제

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

### Context Cost
각 Component가 Instruction, Tool Schema, Intermediate Result를 Context에 추가할 수 있다.

### Latency
Planner → Executor → Reviewer 구조는 단일 실행보다 Turn과 Model Call이 늘어난다.

### Coordination Failure
Component 사이에 다른 State가 생길 수 있다.

Planner는 완료됐다고 생각하지만 Executor는 다른 목표를 따를 수 있다.

### Debugging Difficulty
최종 결과가 나빠졌을 때 어떤 Component가 원인인지 알기 어렵다.

### Stale Assumption
예전 Model의 약점을 보완한 Rule이 새 Model의 좋은 행동을 방해할 수 있다.

이 책에서는 이런 누적을 **Harness Debt**라고 부른다.

이 역시 외부 표준 용어가 아니라 이 책의 synthesis다.

## Harness Component는 가설이다

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

## Component Record

Harness가 커지면 각 Component가 어떤 Failure 때문에 들어왔고, 어떤 Eval이 효과를 확인했으며, 마지막으로 어느 Model에서 검증됐는지 기록하는 편이 좋다.

이 기록은 Model Upgrade 때 제거 후보를 찾고 "왜 이 Component가 존재하는가"를 Commit History에서 다시 추측하는 비용을 줄인다. 구체적인 Record와 Ablation 절차는 21장에서 다룬다.

## Harness와 State를 분리한다

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

## Harness와 Runtime도 분리한다

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

## Harness와 Verification

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

## Harness 변경은 Versioning 대상이다

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

## Model Upgrade는 Harness Audit Trigger다

새 Model이 출시됐다고 기존 Harness를 그대로 유지해야 하는 것은 아니다. 먼저 기존 Harness와 단순한 Baseline을 비교하고, Planner·Memory·Evaluator 같은 Component가 여전히 필요한지 다시 측정한다.

이 책에서는 이런 검증을 Harness Ablation으로 다룬다. 반복 실행과 Variance를 포함한 구체적인 방법은 21장에서 설명한다.

## 지금 필요한 것만 남긴다

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

## Part I에서 남은 질문

1장에서 Model과 Agent를 분리했다.

2장에서 Agent Loop 주변에 필요한 Control을 살펴봤다.

이 장에서는 그 Control을 Harness라는 Software Layer로 묶었다.

하지만 아직 중요한 문제가 남아 있다.

Harness가 Model에게 다음 Turn을 요청할 때 무엇을 보여줘야 할까.

Conversation History 전체인가. Repository 전체인가. 모든 Tool Schema인가. 이전 실패 로그 전체인가.

Agent가 사용할 수 있는 정보는 많지만 Model의 Attention은 제한돼 있다.

다음 장에서는 **Context는 저장소가 아니다**라는 원칙에서 시작한다. Durable State와 현재 Inference Context를 분리하고, 필요한 정보만 Model에게 Projection하는 방법을 살펴본다.

## 주요 근거

- Anthropic, Building Effective Agents
- Anthropic, Effective Harnesses for Long-running Agents
- Anthropic, Harness Design for Long-running Application Development
- Anthropic, Scaling Managed Agents
- OpenAI Agents SDK
- research/topics/04-harness-Long-running.md
- research/topics/14-coding-agent-harness-comparison.md
- research/topics/22-harness-ablation-and-minimalism.md
