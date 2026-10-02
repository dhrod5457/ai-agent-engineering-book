# Part VII. Multi-Agent와 Production Boundary

Part VII는 Agent를 더 많이 만드는 방법보다 **언제 분리할 가치가 있는가**를 먼저 묻는다.

Single-Agent baseline에서 시작해 Agent-as-Tool, Handoff, Remote Agent의 ownership과 protocol boundary를 구분하고, 마지막으로 Software Factory로 넘어가는 경계를 정리한다.

<!-- source-draft: chapters/22/draft.md -->

## 22장. Single-Agent First

Agent가 하나로 잘 안 되면 여러 개로 나누면 해결될 것처럼 보인다.

Planner Agent, Research Agent, Coding Agent, Reviewer Agent, Security Agent를 만든다.

역할은 깔끔해 보인다.

하지만 새로운 문제가 생긴다.

어떤 State를 누구에게 넘길지 정해야 하고, 같은 Context를 여러 번 복제하고, Agent 사이에 다른 사실이 생기고, 실패 원인을 찾기 어려워진다.

Multi-Agent는 복잡성을 없애지 않는다. Context, ownership, permission, coordination이라는 새로운 경계를 추가한다.

### Single-Agent Baseline

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

### Multi-Agent가 해결하지 못하는 것

다음 문제가 Single-Agent에서 해결되지 않았다면 Multi-Agent가 자동으로 고쳐주지 않는다.

- Context가 stale함
- Tool Contract가 모호함
- Authorization이 없음
- Completion Verification이 약함
- State Recovery가 없음
- Runtime이 불안정함

오히려 여러 Agent가 같은 약점을 공유하게 될 수 있다.

### Agent를 나눌 이유

그렇다고 Multi-Agent가 필요 없다는 뜻은 아니다.

분리 이유가 명확할 때 가치가 있다.

#### Context Isolation

한 Agent가 모든 Context를 들고 있지 않아도 된다.

예:

~~~text
Main Agent
  ↓
Security Specialist
  - security docs
  - security tools
~~~

#### Permission Isolation

Specialist별로 Tool Scope를 다르게 둘 수 있다.

~~~text
Research Agent
→ read-only

Deployment Agent
→ deploy capability
~~~

#### Independent Review

Executor와 Reviewer의 역할을 분리할 수 있다.

#### Parallel Work

서로 독립적인 Task를 동시에 진행할 수 있다.

#### Specialized Instruction

역할별로 다른 Instruction과 Tool Surface를 사용할 수 있다.

### Context Isolation의 비용

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

### Permission Isolation

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

### Independent Reviewer

Reviewer Agent를 추가했다고 독립 검증이 자동으로 되는 것은 아니다.

같은 Model, 같은 Context, 같은 잘못된 가정을 공유하면 같은 오류를 반복할 수 있다.

가능하면 Reviewer는 다음 중 일부가 달라야 한다.

- Verification Method
- Tool
- Evidence
- Instruction
- Permission

특히 Deterministic Test가 있다면 Reviewer Agent보다 우선한다.

### Parallelism

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

### Coordination Cost

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

### 언제 분리할 것인가

다음 질문을 사용할 수 있다.

~~~text
Context를 분리하면 명확한 이득이 있는가?
Permission을 분리해야 하는가?
독립 검증이 필요한가?
병렬 가능한가?
역할별 Tool Surface가 크게 다른가?
~~~

대부분 NO라면 Single-Agent가 더 단순할 수 있다.

### 작은 예: Coding Agent

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

### Multi-Agent를 성숙도 지표로 보지 않는다

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

### 이 장에서 가져갈 것

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

### Source Notes

- [S-ANTHROPIC-AGENTS]

---

<!-- source-draft: chapters/23/draft.md -->

## 23장. Agent-as-Tool과 Handoff

두 Agent가 협업한다고 하자.

첫 번째 구조:

~~~text
Manager Agent
  ↓ ask
Research Agent
  ↓ result
Manager Agent
  ↓ continue
~~~

두 번째 구조:

~~~text
Support Agent
  ↓ transfer ownership
Billing Agent
  ↓ continue with user
~~~

둘 다 Agent 사이의 호출처럼 보인다.

하지만 Ownership이 다르다.

이 장에서는 설명을 위해 이를 Agent-as-Tool과 Handoff라는 두 pattern으로 나눈다. 제품과 Framework마다 용어와 세부 semantics는 다를 수 있으므로 이름보다 ownership 차이에 집중한다.

### Agent-as-Tool

Manager가 전체 Goal과 User Interaction을 계속 소유한다.

Specialist Agent는 bounded subtask를 수행하고 Result를 반환한다.

~~~text
Manager
  ├─ Research Agent
  ├─ Code Review Agent
  └─ Security Agent
~~~

Specialist는 Tool과 비슷한 역할을 한다.

### 장점

#### Ownership이 명확하다

최종 Completion은 Manager가 판단한다.

#### Context를 격리할 수 있다

Specialist에게 필요한 정보만 제공할 수 있다.

#### Permission을 좁힐 수 있다

Research Agent는 read-only일 수 있다.

### 단점

#### Manager Bottleneck

모든 Result가 Manager로 돌아온다.

#### Context Concentration

Manager가 전체 State를 많이 들고 있어야 할 수 있다.

#### Result Interpretation

Specialist Result를 Manager가 다시 해석해야 한다.

### Handoff

Handoff는 Work 또는 Interaction Ownership을 다른 Agent에게 넘긴다.

~~~text
Agent A
  ↓ handoff
Agent B
  ↓ owns next interaction
~~~

예를 들어 학생 상담 Agent가 장학 관련 문의를 Scholarship Agent로 넘긴다.

이후 Scholarship Agent가 사용자와 직접 Interaction할 수 있다.

### Handoff Contract

Ownership을 넘길 때 무엇을 전달할지 명확해야 한다.

최소 후보:

~~~text
Goal
Current State
Relevant History
Artifacts
Constraints
Pending Questions
Authority / Permission Context
~~~

Conversation Summary 하나만 넘기면 중요한 State가 빠질 수 있다.

### Context Transfer

Handoff는 모든 Context를 복제하는 것이 아니다.

Agent B가 필요한 Context만 Projection한다.

~~~text
State Plane
   ↓
Handoff Projection
   ↓
Agent B Context
~~~

이 구조는 Part II Context Engineering과 연결된다.

### Authority Transfer

가장 중요한 문제 중 하나다.

Agent A가 가진 권한이 Agent B에게 자동으로 전달되는가.

항상 그렇지 않다.

예:

~~~text
Agent A
→ read student record

Agent B
→ scholarship decision support
~~~

Agent B는 다른 Tool Scope를 가질 수 있다.

Handoff에는 Work Ownership 전달뿐 아니라 receiving Agent의 Effective Authorization 재평가가 필요하다.

### State Ownership

Handoff 후 Goal State를 누가 수정하는가.

두 Agent가 동시에 같은 Goal을 수정하면 Conflict가 생길 수 있다.

패턴:

#### Single Owner

현재 Active Agent만 Goal을 수정.

#### Shared State with Version

여러 Agent가 Versioned State를 수정.

#### Parent/Child Goal

Manager Goal 아래 Specialist Subgoal을 둔다.

각 시스템에 맞게 선택한다.

### Result Contract

Agent-as-Tool에서는 Specialist Result Format이 중요하다.

예:

~~~text
status
findings
evidence_refs
uncertainties
recommended_next_action
~~~

"검토 완료"만 반환하면 Manager가 검토 내용을 알 수 없다.

### Independent Verifier

Executor Agent와 Verifier Agent를 분리할 수 있다.

~~~text
Executor
→ Artifact

Verifier
→ inspect Artifact
→ PASS / FAIL + evidence
~~~

하지만 독립성이 구조적으로 보장돼야 한다.

가능하면 Verifier가:

- 다른 Tool
- 다른 Evidence
- deterministic test

를 사용할 수 있다.

### Failure

Specialist가 실패하면 Parent가 어떻게 처리할지 정한다.

~~~text
Specialist Failed
  ├─ retry same specialist
  ├─ use alternative specialist
  ├─ resume in manager
  └─ escalate
~~~

Handoff 뒤 Failure가 발생하면 Ownership을 되돌릴지 정해야 한다.

### 작은 예: 코드 변경과 Security Review

Manager Coding Agent:

~~~text
Goal:
auth bug fix
~~~

작업 후 Security Reviewer를 Agent-as-Tool로 호출한다.

~~~text
Input:
diff
security-relevant files
acceptance criteria

Output:
findings
severity
evidence
~~~

Manager가 수정 여부를 결정하고 Completion을 유지한다.

여기서는 Handoff보다 Agent-as-Tool이 자연스럽다.

반면 Customer Support에서 Billing 문제를 전문 Agent에게 넘긴다면 Handoff가 더 자연스러울 수 있다.

### Local Subagent와 Remote Agent

같은 Process 안의 Subagent 호출과 독립 Service의 Agent 호출은 운영 경계가 다르다.

Remote Agent에는 다음이 필요할 수 있다.

- network
- authentication
- authorization
- task lifecycle
- async update
- artifact transfer

이 문제는 다음 장의 A2A와 연결된다.

### 이 장에서 가져갈 것

두 패턴을 구분한다.

~~~text
Agent-as-Tool
= Manager keeps ownership

Handoff
= Ownership transfers
~~~

그리고 Handoff에서는 Context뿐 아니라 State와 Authority도 전달 경계를 가져야 한다.

다음 장에서는 이 협업이 같은 Application 내부가 아니라 독립 Agent System 사이에서 일어날 때 필요한 Protocol Boundary를 본다.

A2A와 Remote Agent를 다룬다.

### Source Notes

- [S-OAI-AGENTS]
- [S-GOOGLE-ADK]
- [B-OWNERSHIP]

---

<!-- source-draft: chapters/24/draft.md -->

## 24장. A2A와 Remote Agent

한 Application 안에서 Subagent를 호출하는 것은 비교적 단순하다.

같은 Runtime, 같은 State Store, 같은 Authentication Context를 공유할 수 있다.

다른 조직이나 다른 Service가 운영하는 Agent를 호출하면 이야기가 달라진다.

상대 Agent의 내부 Tool과 Memory를 직접 알 수 없고, Network Boundary가 있으며, Authentication과 Task Lifecycle이 필요하다.

A2A는 이런 독립 Agent System 사이의 discovery, message exchange, task lifecycle, artifact 전달 같은 상호운용 문제를 다룬다.

2026-10-02 기준 A2A의 최신 정식 Specification은 1.0.0이다. 이 장에서는 버전별 JSON 표현보다 1.0에서도 유지되는 Agent Card, Message, Task, Artifact, Authorization의 책임 경계에 집중한다.

### Remote Agent는 Tool과 다르다

Tool은 bounded capability를 제공한다.

Remote Agent는 자체적으로 다음을 가질 수 있다.

- Model
- Harness
- Tools
- State
- Policy
- Long-running Task

따라서:

~~~text
Tool Call
≠ Remote Agent Delegation
~~~

Remote Agent는 단순 함수 호출보다 더 긴 Lifecycle을 가질 수 있다.

### A2A의 위치

이 책에서는 다음처럼 구분한다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

MCP가 Tool/Resource Integration을 다룬다면 A2A는 Agent 단위 Work Collaboration을 다룬다.

### Agent Card

Remote Agent가 어떤 Capability를 제공하는지 Discover할 수 있다.

예:

~~~text
Compliance Review Agent
- policy review
- evidence analysis
- compliance report
~~~

하지만 Agent Card는 Authorization이 아니다.

Capability가 존재한다고 누구나 호출할 수 있는 것은 아니다.

### Message

Agent 사이 Interaction은 Message로 표현될 수 있다.

Message는 단순 String보다 구조화된 Content를 가질 수 있다.

중요한 것은 Protocol Message와 내부 Conversation State를 동일시하지 않는 것이다.

### A2A Task

Remote Agent에 위임한 Work는 Task Lifecycle을 가질 수 있다.

2026-10-02 기준 A2A 0.3.0에는 다음 Task state가 정의돼 있다. 정확한 state 목록은 protocol version에 따라 달라질 수 있으므로 출간 전 다시 확인한다.

~~~text
submitted
working
input-required
completed
canceled
failed
rejected
auth-required
unknown
~~~

이 Task는 MCP Task와 다르다.

~~~text
MCP Task
= Long-running Capability Invocation

A2A Task
= remote Agent work contract
~~~

또 Software Factory Task와도 다르다.

~~~text
Factory Task
  ↓
Agent Run
  ├─ MCP Task
  └─ A2A Task
~~~

상위 Work Item이 여러 Protocol Task를 포함할 수 있다.

### Artifact

A2A에서는 Remote Agent가 결과를 Artifact로 전달할 수 있다.

예:

- report
- generated file
- analysis result
- structured data

Artifact는 Message와 다르다.

Message는 Interaction이고 Artifact는 Deliverable에 가깝다.

### Input Required

Remote Agent가 추가 정보가 필요할 수 있다.

~~~text
working
  ↓
input-required
  ↓
client provides info
  ↓
working
~~~

Long-running Agent의 Pause/Resume와 유사하다.

Protocol Lifecycle이 내부 State Plane과 연결될 수 있다.

### Auth Required

Remote Agent가 추가 Authorization을 요구할 수도 있다.

이 경우 Caller Identity와 Originating User Context를 어떻게 전달할지 중요해진다.

~~~text
User
→ Local Agent
→ Remote Agent
→ Remote Tool
~~~

Remote Agent가 자신의 broad Service Credential만 사용해 User Scope를 초과하지 않도록 한다.

### Capability Discovery와 Authorization

다시 같은 원칙이 나온다.

~~~text
Agent Card
= what is available

Authorization
= can this caller use it
~~~

Remote Agent Server가 최종 Access Policy를 강제해야 한다. A2A 1.0의 AUTH_REQUIRED 상태 자체도 특정 Action을 승인했다는 뜻은 아니며, 실제 Authorization Scope와 Credential 의미는 구현이나 Credential Issuer가 별도로 정의해야 한다.

### Async Work

Remote Agent는 즉시 결과를 반환하지 않을 수 있다.

Long-running Task라면:

- status query
- streaming
- notification
- artifact update

가 필요하다.

이때 Local Agent는 Remote Task State를 자신의 Internal Goal State와 연결할 수 있다.

~~~text
Local Goal G-100
  ↓ delegates
A2A Task T-55
  ↓ completed
Artifact A-7
  ↓
Local Goal resumes
~~~

두 Task ID를 같은 것으로 만들지 않는다.

### Remote Failure

Remote Agent가 실패하면 Local Agent가 판단해야 한다.

예:

~~~text
A2A Task failed
  ├─ retry
  ├─ alternative agent
  ├─ continue locally
  └─ escalate
~~~

Protocol Error와 Domain Failure를 구분하는 것이 중요하다.

### Trust

Remote Agent가 반환한 Artifact를 자동으로 Trusted Result로 보지 않는다.

필요하면 Local Verification을 한다.

~~~text
Remote Agent
→ Artifact
→ Local Verifier
→ Accept
~~~

특히 다른 Organization이나 Trust Domain의 Agent라면 중요하다.

### A2A와 Internal Domain

Protocol Object를 내부 Domain Model에 직접 종속시키지 않는 원칙은 MCP와 같다.

~~~text
Internal Delegation Model
        ↓
A2A Adapter
        ↓
Remote Agent
~~~

Protocol Version이 바뀌어도 내부 Goal과 Artifact Model을 유지하기 쉽다.

### 작은 예: 대학 규정 검토 Agent

Campus Agent가 외부 Legal Review Agent에 규정 변경 검토를 요청한다.

~~~text
Campus Agent
  ↓
A2A Task:
review regulation change

Remote Legal Agent
  ↓
Artifact:
risk report
~~~

Campus Agent는 결과를 그대로 적용하지 않는다.

~~~text
Artifact
→ local policy check
→ human review
→ accept
~~~

Remote Agent는 Specialist이지만 최종 Authority는 아닐 수 있다.

### 이 장에서 가져갈 것

Remote Agent를 Tool처럼 단순화하면 Lifecycle과 Authority를 놓칠 수 있다.

다음 경계를 유지한다.

~~~text
MCP Task
≠ A2A Task
≠ Factory Task

Remote Agent
≠ Local Subagent
~~~

A2A는 independent Agent System 간 Collaboration Boundary다.

이제 책의 마지막 장에서 지금까지의 내용을 도입 순서로 압축한다.

처음부터 Memory, Multi-Agent, MicroVM을 모두 넣지 않고 Minimum Viable 운영 Agent에서 어떻게 시작할 것인가.

### Source Notes

- [S-A2A-0.3]
- [S-MCP-2026-07]

---

<!-- source-draft: chapters/25/draft.md -->

## 25장. Minimum Viable Production Agent

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

### Minimum Viable Agent

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

### 1단계: Clear Tool Contract

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

### 2단계: Controlled Runtime

Agent가 잘못 행동해도 피해가 제한되도록 한다.

예:

- Workspace Scope
- Network Allowlist
- Resource Limit
- No Production Credential

Capability보다 Boundary를 먼저 만든다.

### 3단계: Deterministic Verification

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

### 4단계: Trace

실패했을 때 이유를 볼 수 있어야 한다.

처음부터 거대한 Observability Platform이 필요하지 않다.

최소한:

- model call
- tool call
- result
- failure
- verification

을 연결할 수 있게 한다.

### 5단계: Eval

운영 실패를 모아 Regression Case를 만든다.

~~~text
Failure
→ Eval Case
→ Fix
→ Re-run
~~~

Agent를 "감으로 개선"하지 않는다.

### 6단계: Durable State

Task가 한 Process를 넘어가기 시작하면 State Plane이 필요해진다.

Trigger:

- Approval 대기
- Long-running
- Crash Recovery
- External Mutation
- Multi-step Goal

이때 Event History, Goal, Artifact, Approval State를 도입한다.

### 7단계: Identity와 Policy

External System에 접근하기 시작하면:

- User / Agent Identity
- Credential Scope
- Authorization
- Sandbox
- Approval

을 분리한다.

Risk가 올라갈수록 Control을 강화한다.

### 8단계: Memory

반복 Task에서 이득이 확인될 때 추가한다.

Memory를 넣기 전 질문:

~~~text
무엇을 반복해서 다시 찾고 있는가?
어떤 Lesson이 재사용 가능한가?
Source of Truth로 다시 읽을 수 없는가?
Memory Risk를 감당할 가치가 있는가?
~~~

필요성이 없으면 넣지 않아도 된다.

### 9단계: Long-running

Task가 길어지면:

- Milestone
- Progress State
- Phase Budget
- Reconciliation
- Verification Reserve

를 추가한다.

Long Context만 늘리는 것으로 해결하지 않는다.

### 10단계: Multi-Agent

Single-Agent Baseline이 안정된 뒤에도 Context·Permission 분리, 독립 검증, 병렬화에서 명확한 이득이 있을 때만 Multi-Agent를 추가한다. 판단 기준 자체는 22장에서 다뤘으므로 여기서는 확장 순서의 마지막 선택지로만 둔다.

### 확장 순서의 한 예

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

### Control before Autonomy

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

### Verification before Scale

한 Agent가 Task를 안정적으로 끝내지 못하는데 Agent 수를 늘리면 Failure도 병렬화될 수 있다.

~~~text
Single Agent
→ verify

Then
→ parallelize independent work
~~~

Software Factory로 가기 전에도 같은 원칙이 중요하다.

### Example: Repository Fix Agent

#### V0

~~~text
Model
+ read/edit/test tools
+ workspace sandbox
+ targeted test
+ trace
~~~

#### V1

Approval이 필요해졌다.

~~~text
+ durable goal state
+ approval pause/resume
~~~

#### V2

GitHub Mutation을 한다.

~~~text
+ agent identity
+ scoped credential
+ PR policy
~~~

#### V3

Long-running Task가 생겼다.

~~~text
+ milestone
+ progress
+ source reconciliation
~~~

#### V4

반복되는 Repository Knowledge가 많아졌다.

~~~text
+ scoped memory
+ write policy
~~~

#### V5

Security Review를 분리할 이득이 생겼다.

~~~text
+ specialist agent
~~~

필요에 따라 확장한다.

### Agent State Plane과 Factory Control Plane

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

### 언제 Factory로 넘어가는가

다음 문제가 커지면 Agent-level Architecture만으로는 부족해진다.

- Backlog가 많다.
- 여러 Worker가 있다.
- Task Dependency가 있다.
- Assignment가 필요하다.
- Acceptance Authority가 필요하다.
- Merge/Deploy Delivery가 필요하다.
- Retry/Reassignment가 조직 수준에서 필요하다.

이때 Software Factory Control Plane이 등장한다.

### Production Readiness Checklist

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

### 이 장에서 가져갈 것

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

### Source Notes

- [B-AGENT-CAPABILITY]
- [B-STATE-PLANE]
- [B-FACTORY-BOUNDARY]
