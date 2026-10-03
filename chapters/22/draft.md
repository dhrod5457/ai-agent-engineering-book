# 22장. Single-Agent First

에이전트가 하나로 잘 안 되면 여러 개로 나누면 해결될 것처럼 보인다. 계획 에이전트, 조사 에이전트, 코드 작업 에이전트, 검토 에이전트, 보안 에이전트를 만든다. 역할은 깔끔하게 나뉜 것처럼 보이지만, 새로운 문제가 생긴다. 어떤 상태를 누구에게 넘길지 정해야 하고, 같은 컨텍스트(Context: 모델에 전달하는 정보)를 여러 번 복제하고, 에이전트 사이에 다른 사실이 생기고, 실패 원인을 찾기 어려워진다. 여러 에이전트의 협업은 복잡성을 없애지 않는다. 컨텍스트, 담당 책임, 권한, 협업 조율이라는 새로운 경계를 추가한다.

## Single-Agent Baseline

여러 에이전트의 협업을 검토하기 전에 하나의 에이전트로 같은 작업을 수행한 비교 기준이 필요하다.

~~~text
Single Agent
+ Clear Tool Surface
+ Controlled Runtime
+ Durable State
+ Verification
~~~

이 비교 기준이 있어야 분리의 이득을 측정할 수 있다. 그렇지 않으면 에이전트 수가 늘어난 효과인지, 도구 인터페이스가 좋아진 효과인지 구분하기 어렵다.

## Multi-Agent가 해결하지 못하는 것

다음 문제가 단일 에이전트에서 해결되지 않았다면 여러 에이전트의 협업이 자동으로 고쳐주지 않는다.

- 컨텍스트가 stale함
- 도구 사용 계약(Tool Contract: 도구의 입력·출력·사용 조건)이 모호함
- 권한 확인(Authorization)이 없음
- Completion Verification이 약함
- State Recovery가 없음
- 실행 환경이 불안정함

오히려 여러 에이전트가 같은 약점을 공유하게 될 수 있다.

## Agent를 나눌 이유

그렇다고 여러 에이전트의 협업이 필요 없다는 뜻은 아니다. 분리 이유가 명확할 때 가치가 있다.

### Context Isolation

한 에이전트가 모든 컨텍스트를 들고 있지 않아도 된다.

예:

~~~text
Main Agent
  ↓
Security Specialist
  - security docs
  - security tools
~~~

### Permission Isolation

전문 역할의 에이전트별로 도구의 권한 범위를 다르게 둘 수 있다.

~~~text
Research Agent
→ read-only

Deployment Agent
→ deploy capability
~~~

### Independent Review

실행 담당자와 검토 담당자의 역할을 분리할 수 있다.

### Parallel Work

서로 독립적인 작업을 동시에 진행할 수 있다.

### Specialized Instruction

역할별로 다른 지침과 사용 가능한 도구의 범위를 사용할 수 있다.

## Context Isolation의 비용

컨텍스트를 나누면 각 에이전트가 덜 복잡한 입력을 받을 수 있다. 하지만 작업 인계할 때 필요한 정보를 전달해야 한다. 너무 적게 전달하면 전문 역할의 에이전트가 컨텍스트를 다시 탐색한다. 너무 많이 전달하면 Isolation 이점이 줄어든다. 그래서 Handoff Contract가 필요하다.

~~~text
Goal
Relevant State
Artifact References
Constraints
Expected Result
Authority
~~~

## Permission Isolation

여러 에이전트의 협업의 강한 장점 중 하나는 권한 경계를 분리할 수 있다는 점이다.

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

이렇게 하면 한 에이전트가 모든 기능을 가질 필요가 없다. 하지만 에이전트가 많아졌다는 이유만으로 권한이 줄어드는 것은 아니다. Authorization System에서 적용 범위를 분리해야 한다.

## Independent Reviewer

검토 에이전트를 추가했다고 독립 검증이 자동으로 되는 것은 아니다. 같은 모델, 같은 컨텍스트, 같은 잘못된 가정을 공유하면 같은 오류를 반복할 수 있다. 가능하면 검토 담당자는 다음 중 일부가 달라야 한다.

- Verification Method
- 도구
- 근거
- 지침
- 권한

특히 Deterministic Test가 있다면 검토 에이전트보다 우선한다.

## Parallelism

독립 작업은 병렬화하기 좋다.

예:

~~~text
Task A: API docs
Task B: test analysis
Task C: dependency check
~~~

반대로 같은 파일이나 같은 상태를 강하게 공유하는 작업은 Coordination Cost가 크다.

~~~text
Agent A edits UserService
Agent B edits UserService
Agent C reviews stale version
~~~

병합과 State Conflict가 생긴다. 따라서 에이전트 수보다 Work Independence를 먼저 본다.

## Coordination Cost

에이전트가 늘면 새로운 비용이 생긴다.

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

대부분 NO라면 단일 에이전트가 더 단순할 수 있다.

## 작은 예: Coding Agent

단일 에이전트:

~~~text
Read
Edit
Test
PR
~~~

문제가 잘 해결된다면 굳이 네 에이전트로 나눌 필요가 없다.

하지만 운영 환경 배포까지 포함된다면:

~~~text
Coding Agent
→ workspace only

Deployment Agent
→ deploy capability
→ explicit approval
~~~

처럼 권한 경계 때문에 분리할 이유가 생긴다.

## Multi-Agent를 성숙도 지표로 보지 않는다

다음 식은 성립하지 않는다.

~~~text
More Agents
= More Advanced System
~~~

운영이 충분히 안정된 시스템도 에이전트를 하나만 사용할 수 있다.

판단 기준:

- 경계
- 상태
- 검증
- 복구
- 정책

다.

## 이 장에서 가져갈 것

여러 에이전트의 협업은 기본값이 아니다. 먼저 단일 에이전트의 실행 구조를 안정시킨다. 그다음에는 아래와 같은 이유가 분명할 때 역할을 나눈다.

~~~text
Context Isolation
Permission Isolation
Independent Review
Parallel Work
Specialization
~~~

다음 장에서는 여러 에이전트의 협업을 연결하는 두 패턴을 구분한다. 에이전트를 도구처럼 호출하는 경우와, 업무를 책임지는 주체 자체를 넘기는 작업 인계는 같은 구조가 아니다.

## 주요 근거

- Anthropic, Building Effective Agents
- OpenAI Agents SDK
- Google ADK
- research/topics/07-multi-agent-interoperability.md
