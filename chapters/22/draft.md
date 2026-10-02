# 22장. Single-Agent First

Agent가 하나로 잘 안 되면 여러 개로 나누면 해결될 것처럼 보인다.

Planner Agent, Research Agent, Coding Agent, Reviewer Agent, Security Agent를 만든다.

역할은 깔끔해 보인다.

하지만 새로운 문제가 생긴다.

어떤 State를 누구에게 넘길지 정해야 하고, 같은 Context를 여러 번 복제하고, Agent 사이에 다른 사실이 생기고, 실패 원인을 찾기 어려워진다.

Multi-Agent는 복잡성을 없애지 않는다. Context, ownership, permission, coordination이라는 새로운 경계를 추가한다.

## Single-Agent Baseline

Multi-Agent를 검토하기 전에 하나의 Agent로 같은 Task를 수행한 Baseline이 필요하다.

~~~text
Single Agent
+ Clear Tool Surface
+ Controlled Runtime
+ Durable State
+ Verification
~~~

이 Baseline이 있어야 분리의 이득을 측정할 수 있다.

그렇지 않으면 Agent 수가 늘어난 효과인지, Tool Interface가 좋아진 효과인지 구분하기 어렵다.

## Multi-Agent가 해결하지 못하는 것

다음 문제가 Single-Agent에서 해결되지 않았다면 Multi-Agent가 자동으로 고쳐주지 않는다.

- Context가 stale함
- Tool Contract가 모호함
- Authorization이 없음
- Completion Verification이 약함
- State Recovery가 없음
- Runtime이 불안정함

오히려 여러 Agent가 같은 약점을 공유하게 될 수 있다.

## Agent를 나눌 이유

그렇다고 Multi-Agent가 필요 없다는 뜻은 아니다.

분리 이유가 명확할 때 가치가 있다.

### Context Isolation

한 Agent가 모든 Context를 들고 있지 않아도 된다.

예:

~~~text
Main Agent
  ↓
Security Specialist
  - security docs
  - security tools
~~~

### Permission Isolation

Specialist별로 Tool Scope를 다르게 둘 수 있다.

~~~text
Research Agent
→ read-only

Deployment Agent
→ deploy capability
~~~

### Independent Review

Executor와 Reviewer의 역할을 분리할 수 있다.

### Parallel Work

서로 독립적인 Task를 동시에 진행할 수 있다.

### Specialized Instruction

역할별로 다른 Instruction과 Tool Surface를 사용할 수 있다.

## Context Isolation의 비용

Context를 나누면 각 Agent가 덜 복잡한 입력을 받을 수 있다.

하지만 Handoff할 때 필요한 정보를 전달해야 한다.

너무 적게 전달하면 Specialist가 Context를 다시 탐색한다.

너무 많이 전달하면 Isolation 이점이 줄어든다.

그래서 Handoff Contract가 필요하다.

~~~text
Goal
Relevant State
Artifact References
Constraints
Expected Result
Authority
~~~

## Permission Isolation

Multi-Agent의 강한 장점 중 하나는 Permission Boundary를 분리할 수 있다는 점이다.

예:

~~~text
Planner
→ no mutation tools

Coder
→ workspace mutation

Reviewer
→ read + test

Deploy Agent
→ production deploy
~~~

이렇게 하면 한 Agent가 모든 Capability를 가질 필요가 없다.

하지만 Agent가 많아졌다는 이유만으로 권한이 줄어드는 것은 아니다.

Authorization System에서 Scope를 분리해야 한다.

## Independent Reviewer

Reviewer Agent를 추가했다고 독립 검증이 자동으로 되는 것은 아니다.

같은 Model, 같은 Context, 같은 잘못된 가정을 공유하면 같은 오류를 반복할 수 있다.

가능하면 Reviewer는 다음 중 일부가 달라야 한다.

- Verification Method
- Tool
- Evidence
- Instruction
- Permission

특히 Deterministic Test가 있다면 Reviewer Agent보다 우선한다.

## Parallelism

독립 Task는 병렬화하기 좋다.

예:

~~~text
Task A: API docs
Task B: test analysis
Task C: dependency check
~~~

반대로 같은 File이나 같은 State를 강하게 공유하는 작업은 Coordination Cost가 크다.

~~~text
Agent A edits UserService
Agent B edits UserService
Agent C reviews stale version
~~~

Merge와 State Conflict가 생긴다.

따라서 Agent 수보다 Work Independence를 먼저 본다.

## Coordination Cost

Agent가 늘면 새로운 비용이 생긴다.

- Context duplication
- routing
- handoff
- latency
- token
- state conflict
- tracing
- authority ambiguity

Multi-Agent Architecture는 이 비용보다 분리 이득이 커야 한다.

## 언제 분리할 것인가

다음 질문을 사용할 수 있다.

~~~text
Context를 분리하면 명확한 이득이 있는가?
Permission을 분리해야 하는가?
독립 검증이 필요한가?
병렬 가능한가?
역할별 Tool Surface가 크게 다른가?
~~~

대부분 NO라면 Single-Agent가 더 단순할 수 있다.

## 작은 예: Coding Agent

Single-Agent:

~~~text
Read
Edit
Test
PR
~~~

문제가 잘 해결된다면 굳이 네 Agent로 나눌 필요가 없다.

하지만 Production Deploy까지 포함된다면:

~~~text
Coding Agent
→ workspace only

Deployment Agent
→ deploy capability
→ explicit approval
~~~

처럼 Permission Boundary 때문에 분리할 이유가 생긴다.

## Multi-Agent를 성숙도 지표로 보지 않는다

다음 식은 성립하지 않는다.

~~~text
More Agents
= More Advanced System
~~~

운영적으로 성숙한 시스템이 하나의 Agent만 사용할 수도 있다.

판단 기준:

- Boundary
- State
- Verification
- Recovery
- Policy

다.

## 이 장에서 가져갈 것

Multi-Agent는 기본값이 아니다.

먼저 Single-Agent의 실행 구조를 안정시킨다.

그 다음 다음 이유가 명확할 때 분리한다.

~~~text
Context Isolation
Permission Isolation
Independent Review
Parallel Work
Specialization
~~~

다음 장에서는 Multi-Agent를 연결하는 두 패턴을 구분한다.

Agent를 Tool처럼 호출하는 경우와, Work Ownership 자체를 넘기는 Handoff는 같은 구조가 아니다.

## 주요 근거

- Anthropic, Building Effective Agents
- OpenAI Agents SDK
- Google ADK
- research/topics/07-multi-agent-interoperability.md
