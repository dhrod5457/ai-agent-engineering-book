# 25장. Minimum Viable Production Agent

여기까지 읽으면 Agent 시스템에 넣을 수 있는 기능이 매우 많아 보인다.

- Memory
- State Plane
- Sandbox
- Identity
- Credential Broker
- Policy Engine
- Eval
- Multi-Agent
- MCP
- A2A

처음부터 모두 만들 필요는 없다.

오히려 그렇게 시작하면 Agent를 만들기 전에 Platform부터 만들어질 수 있다.

운영 Agent의 출발점은 더 작게 잡을 수 있다.

## Minimum Viable Agent

가장 작은 형태는 다음 정도다.

~~~text
Model
+ Clear Instruction
+ Small Tool Surface
+ Controlled Runtime
+ Deterministic Verification
+ Trace
~~~

이 구조가 Task를 끝낼 수 있는지 먼저 본다.

## 1단계: Clear Tool Contract

Agent가 어떤 Action을 할 수 있는지 좁힌다.

예:

~~~text
read_file
edit_file
run_test
git_diff
~~~

처음부터 Generic Shell + Full Network + Broad Credential을 줄 이유는 없다.

Tool Contract와 Error Model을 먼저 만든다.

## 2단계: Controlled Runtime

Agent가 잘못 행동해도 피해가 제한되도록 한다.

예:

- Workspace Scope
- Network Allowlist
- Resource Limit
- No Production Credential

Capability보다 Boundary를 먼저 만든다.

## 3단계: Deterministic Verification

Completion Claim을 Model에게 맡기지 않는다.

~~~text
Model:
"완료"

System:
test pass?
schema valid?
artifact correct?
~~~

가능한 Verification Surface가 있다면 초기에 붙인다.

## 4단계: Trace

실패했을 때 이유를 볼 수 있어야 한다.

처음부터 거대한 Observability Platform이 필요하지 않다.

최소한:

- model call
- tool call
- result
- failure
- verification

을 연결할 수 있게 한다.

## 5단계: Eval

운영 실패를 모아 Regression Case를 만든다.

~~~text
Failure
→ Eval Case
→ Fix
→ Re-run
~~~

Agent를 "감으로 개선"하지 않는다.

## 6단계: Durable State

Task가 한 Process를 넘어가기 시작하면 State Plane이 필요해진다.

Trigger:

- Approval 대기
- Long-running
- Crash Recovery
- External Mutation
- Multi-step Goal

이때 Event History, Goal, Artifact, Approval State를 도입한다.

## 7단계: Identity와 Policy

External System에 접근하기 시작하면:

- User / Agent Identity
- Credential Scope
- Authorization
- Sandbox
- Approval

을 분리한다.

Risk가 올라갈수록 Control을 강화한다.

## 8단계: Memory

반복 Task에서 이득이 확인될 때 추가한다.

Memory를 넣기 전 질문:

~~~text
무엇을 반복해서 다시 찾고 있는가?
어떤 Lesson이 재사용 가능한가?
Source of Truth로 다시 읽을 수 없는가?
Memory Risk를 감당할 가치가 있는가?
~~~

필요성이 없으면 넣지 않아도 된다.

## 9단계: Long-running

Task가 길어지면:

- Milestone
- Progress State
- Phase Budget
- Reconciliation
- Verification Reserve

를 추가한다.

Long Context만 늘리는 것으로 해결하지 않는다.

## 10단계: Multi-Agent

Single-Agent Baseline이 안정된 후:

- Context Isolation
- Permission Isolation
- Independent Review
- Parallel Work

이득이 명확할 때 추가한다.

Agent 수를 먼저 늘리지 않는다.

## 확장 순서의 한 예

이 책에서는 설명을 위해 다음 흐름을 사용한다.

~~~text
Minimal Agent
→ Tool Contract
→ Controlled Runtime
→ Trace
→ Eval
→ Durable State
→ Identity / Policy
→ Memory
→ Long-running
→ Multi-Agent
~~~

공식 Maturity Model이나 권장 순서를 뜻하지 않는다. 시스템의 Risk와 업무 특성에 따라 순서는 달라질 수 있으며, 필요한 문제가 생길 때 어떤 구조를 추가할지 보여주는 Reference다.

## Control before Autonomy

Agent Engineering에서 자주 반대로 진행한다.

~~~text
More Autonomy
→ problem occurs
→ add control
~~~

이 책은 가능하면 다음 순서를 권한다.

~~~text
Boundary
→ Verification
→ Observability
→ Autonomy
~~~

즉 Agent에게 더 많은 Capability를 주기 전에 실패를 감당할 구조를 만든다.

## Verification before Scale

한 Agent가 Task를 안정적으로 끝내지 못하는데 Agent 수를 늘리면 Failure도 병렬화될 수 있다.

~~~text
Single Agent
→ verify

Then
→ parallelize independent work
~~~

Software Factory로 가기 전에도 같은 원칙이 중요하다.

## Example: Repository Fix Agent

### V0

~~~text
Model
+ read/edit/test tools
+ workspace sandbox
+ targeted test
+ trace
~~~

### V1

Approval이 필요해졌다.

~~~text
+ durable goal state
+ approval pause/resume
~~~

### V2

GitHub Mutation을 한다.

~~~text
+ agent identity
+ scoped credential
+ PR policy
~~~

### V3

Long-running Task가 생겼다.

~~~text
+ milestone
+ progress
+ source reconciliation
~~~

### V4

반복되는 Repository Knowledge가 많아졌다.

~~~text
+ scoped memory
+ write policy
~~~

### V5

Security Review를 분리할 이득이 생겼다.

~~~text
+ specialist agent
~~~

필요에 따라 확장한다.

## Agent State Plane과 Factory Control Plane

이 책의 마지막 경계를 다시 확인한다.

Agent State Plane:

~~~text
one Agent execution
one Goal
events
progress
approval
artifact
recovery
~~~

Software Factory Control Plane:

~~~text
many work items
worker fleet
scheduling
assignment
acceptance
delivery
feedback
~~~

Agent Engineering이 한 Worker를 신뢰할 수 있게 만드는 문제라면 Software Factory Engineering은 많은 Work를 시스템적으로 흘리는 문제다.

## 언제 Factory로 넘어가는가

다음 문제가 커지면 Agent-level Architecture만으로는 부족해진다.

- Backlog가 많다.
- 여러 Worker가 있다.
- Task Dependency가 있다.
- Assignment가 필요하다.
- Acceptance Authority가 필요하다.
- Merge/Deploy Delivery가 필요하다.
- Retry/Reassignment가 조직 수준에서 필요하다.

이때 Software Factory Control Plane이 등장한다.

## Production Readiness Checklist

최소 질문:

~~~text
Agent Goal이 명확한가?
Tool Surface가 필요한 만큼만 열려 있는가?
Side Effect가 검증되는가?
Runtime Boundary가 있는가?
실패를 Trace할 수 있는가?
Completion을 외부 Evidence로 판정하는가?
Crash 후 이어갈 수 있는가?
Identity와 Credential이 분리돼 있는가?
High-risk Action에 Policy가 있는가?
Regression Eval이 있는가?
~~~

각 항목의 필요 수준은 시스템 Risk에 따라 달라진다. 중요한 것은 기능 목록을 채우는 것이 아니라 이 질문에 명시적으로 답할 수 있는가이다.

## 이 장에서 가져갈 것

운영 Agent는 기능 수로 정의되지 않는다.

더 중요한 것은 다음이다.

~~~text
Can it act?
Can it be constrained?
Can it be observed?
Can it recover?
Can it prove completion?
~~~

Agent Engineering의 목표는 Agent를 최대한 자유롭게 만드는 것이 아니다.

필요한 자유를 주면서도 업무를 맡길 수 있는 구조를 만드는 것이다.

이 책의 마지막에는 하나의 원칙이 남는다.

> 모델을 더 믿는 것이 아니라, 모델을 덜 믿어도 일을 맡길 수 있는 시스템을 만든다.

Epilogue에서 이 관점을 다시 정리한다.

## 주요 근거

- planning/concept.md
- planning/scope.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
- 본문 전체
