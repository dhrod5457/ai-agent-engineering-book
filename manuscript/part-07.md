# Part VII. Multi-Agent와 Production Boundary

Part VII는 에이전트를 더 많이 만드는 방법보다 **언제 분리할 가치가 있는가**를 먼저 묻는다. Single-Agent baseline에서 시작해 Agent-as-Tool, 작업 인계, 원격 에이전트의 담당 책임과 protocol boundary를 구분하고, 마지막으로 Software Factory로 넘어가는 경계를 정리한다.

<!-- source-draft: chapters/22/draft.md -->

## 22장. Single-Agent First

에이전트가 하나로 잘 안 되면 여러 개로 나누면 해결될 것처럼 보인다. 계획 에이전트, 조사 에이전트, 코드 작업 에이전트, 검토 에이전트, 보안 에이전트를 만든다. 역할은 깔끔하게 나뉜 것처럼 보이지만, 새로운 문제가 생긴다. 어떤 상태를 누구에게 넘길지 정해야 하고, 같은 컨텍스트(Context: 모델에 전달하는 정보)를 여러 번 복제하고, 에이전트 사이에 다른 사실이 생기고, 실패 원인을 찾기 어려워진다. 여러 에이전트의 협업은 복잡성을 없애지 않는다. 컨텍스트, 담당 책임, 권한, 협업 조율이라는 새로운 경계를 추가한다.

### Single-Agent Baseline

여러 에이전트의 협업을 검토하기 전에 하나의 에이전트로 같은 작업을 수행한 비교 기준이 필요하다.

~~~text
Single Agent
+ Clear Tool Surface
+ Controlled Runtime
+ Durable State
+ Verification
~~~

이 비교 기준이 있어야 분리의 이득을 측정할 수 있다. 그렇지 않으면 에이전트 수가 늘어난 효과인지, 도구 인터페이스가 좋아진 효과인지 구분하기 어렵다.

### Multi-Agent가 해결하지 못하는 것

다음 문제가 단일 에이전트에서 해결되지 않았다면 여러 에이전트의 협업이 자동으로 고쳐주지 않는다.

- 컨텍스트가 stale함
- 도구 사용 계약(Tool Contract: 도구의 입력·출력·사용 조건)이 모호함
- 권한 확인(Authorization)이 없음
- Completion Verification이 약함
- State Recovery가 없음
- 실행 환경이 불안정함

오히려 여러 에이전트가 같은 약점을 공유하게 될 수 있다.

### Agent를 나눌 이유

그렇다고 여러 에이전트의 협업이 필요 없다는 뜻은 아니다. 분리 이유가 명확할 때 가치가 있다.

#### Context Isolation

한 에이전트가 모든 컨텍스트를 들고 있지 않아도 된다.

예:

~~~text
Main Agent
  ↓
Security Specialist
  - security docs
  - security tools
~~~

#### Permission Isolation

전문 역할의 에이전트별로 도구의 권한 범위를 다르게 둘 수 있다.

~~~text
Research Agent
→ read-only

Deployment Agent
→ deploy capability
~~~

#### Independent Review

실행 담당자와 검토 담당자의 역할을 분리할 수 있다.

#### Parallel Work

서로 독립적인 작업을 동시에 진행할 수 있다.

#### Specialized Instruction

역할별로 다른 지침과 사용 가능한 도구의 범위를 사용할 수 있다.

### Context Isolation의 비용

컨텍스트를 나누면 각 에이전트가 덜 복잡한 입력을 받을 수 있다. 하지만 작업 인계할 때 필요한 정보를 전달해야 한다. 너무 적게 전달하면 전문 역할의 에이전트가 컨텍스트를 다시 탐색한다. 너무 많이 전달하면 Isolation 이점이 줄어든다. 그래서 Handoff Contract가 필요하다.

~~~text
Goal
Relevant State
Artifact References
Constraints
Expected Result
Authority
~~~

### Permission Isolation

여러 에이전트 협업의 큰 장점 중 하나는 권한 경계를 분리할 수 있다는 점이다.

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

### Independent Reviewer

검토 에이전트를 추가했다고 독립 검증이 자동으로 되는 것은 아니다. 같은 모델, 같은 컨텍스트, 같은 잘못된 가정을 공유하면 같은 오류를 반복할 수 있다. 가능하면 검토 담당자는 다음 중 일부가 달라야 한다.

- Verification Method
- 도구
- 근거
- 지침
- 권한

특히 Deterministic Test가 있다면 검토 에이전트보다 우선한다.

### Parallelism

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

### Coordination Cost

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

### 언제 분리할 것인가

다음 질문을 사용할 수 있다.

~~~text
Context를 분리하면 명확한 이득이 있는가?
Permission을 분리해야 하는가?
독립 검증이 필요한가?
병렬 가능한가?
역할별 Tool Surface가 크게 다른가?
~~~

대부분 NO라면 단일 에이전트가 더 단순할 수 있다.

### 작은 예: Coding Agent

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

### Multi-Agent를 성숙도 지표로 보지 않는다

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

### 이 장에서 가져갈 것

여러 에이전트의 협업은 기본값이 아니다. 먼저 단일 에이전트의 실행 구조를 안정시킨다. 그다음에는 아래와 같은 이유가 분명할 때 역할을 나눈다.

~~~text
Context Isolation
Permission Isolation
Independent Review
Parallel Work
Specialization
~~~

다음 장에서는 여러 에이전트의 협업을 연결하는 두 패턴을 구분한다. 에이전트를 도구처럼 호출하는 경우와, 업무를 책임지는 주체 자체를 넘기는 작업 인계는 같은 구조가 아니다.

### Source Notes

- [S-ANTHROPIC-AGENTS]

---

<!-- source-draft: chapters/23/draft.md -->

## 23장. Agent-as-Tool과 Handoff

두 에이전트가 협업한다고 하자.

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

둘 다 에이전트 사이의 호출처럼 보이지만, 작업을 책임지는 주체가 다르다. 이 장에서는 설명을 위해 이를 Agent-as-Tool과 작업 인계라는 두 pattern으로 나눈다. 제품과 프레임워크마다 용어와 세부 semantics는 다를 수 있으므로 이름보다 담당 책임 차이에 집중한다.

### Agent-as-Tool

전체 작업을 관리하는 에이전트가 전체 목표와 User Interaction을 계속 소유한다. Specialist Agent는 bounded subtask를 수행하고 결과를 반환한다.

~~~text
Manager
  ├─ Research Agent
  ├─ Code Review Agent
  └─ Security Agent
~~~

전문 역할의 에이전트는 도구와 비슷한 역할을 한다.

### 장점

#### Ownership이 명확하다

최종 완료는 전체 작업을 관리하는 에이전트가 판단한다.

#### Context를 격리할 수 있다

전문 역할의 에이전트에게 필요한 정보만 제공할 수 있다.

#### Permission을 좁힐 수 있다

조사 에이전트는 read-only일 수 있다.

### 단점

#### Manager Bottleneck

모든 결과가 전체 작업을 관리하는 에이전트로 돌아온다.

#### Context Concentration

전체 작업을 관리하는 에이전트가 전체 상태를 많이 들고 있어야 할 수 있다.

#### Result Interpretation

Specialist Result를 전체 작업을 관리하는 에이전트가 다시 해석해야 한다.

### Handoff

작업 인계는 업무 또는 Interaction Ownership을 다른 에이전트에게 넘긴다.

~~~text
Agent A
  ↓ handoff
Agent B
  ↓ owns next interaction
~~~

예를 들어 학생 상담 에이전트가 장학 관련 문의를 Scholarship Agent로 넘긴다. 이후 Scholarship Agent가 사용자와 직접 Interaction할 수 있다.

### Handoff Contract

담당 책임을 넘길 때 무엇을 전달할지 명확해야 한다.

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

대화 요약 하나만 넘기면 중요한 상태가 빠질 수 있다.

### Context Transfer

작업 인계는 모든 컨텍스트(Context: 모델에 전달하는 정보)를 복제하는 것이 아니다. 에이전트 B에게 필요한 정보만 골라 컨텍스트를 구성한다.

~~~text
State Plane
   ↓
Handoff Projection
   ↓
Agent B Context
~~~

이 구조는 Part II Context Engineering과 연결된다.

### Authority Transfer

가장 중요한 문제 중 하나다. 에이전트 A가 가진 권한이 에이전트 B에게 자동으로 전달되는가. 항상 그렇지 않다.

예:

~~~text
Agent A
→ read student record

Agent B
→ scholarship decision support
~~~

에이전트 B는 다른 도구의 권한 범위를 가질 수 있다. 작업 인계에는 업무를 책임지는 주체 전달뿐 아니라 receiving Agent의 실제로 적용되는 권한 재평가가 필요하다.

### State Ownership

작업 인계 후 Goal State를 누가 수정하는가. 두 에이전트가 동시에 같은 목표를 수정하면 충돌이 생길 수 있다.

패턴:

#### Single Owner

현재 Active Agent만 목표를 수정.

#### Shared State with Version

여러 에이전트가 Versioned State를 수정.

#### Parent/Child Goal

Manager Goal 아래 Specialist Subgoal을 둔다. 각 시스템에 맞게 선택한다.

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

"검토 완료"만 반환하면 전체 작업을 관리하는 에이전트가 검토 내용을 알 수 없다.

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

가능하면 검증 담당자가:

- 다른 도구
- 다른 근거
- deterministic test

를 사용할 수 있다.

### Failure

전문 역할의 에이전트가 실패하면 Parent가 어떻게 처리할지 정한다.

~~~text
Specialist Failed
  ├─ retry same specialist
  ├─ use alternative specialist
  ├─ resume in manager
  └─ escalate
~~~

작업 인계 뒤 실패가 발생하면 담당 책임을 되돌릴지 정해야 한다.

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

전체 작업을 관리하는 에이전트가 수정 여부를 결정하고 완료를 유지한다. 여기서는 작업 인계보다 Agent-as-Tool이 자연스럽다. 반면 Customer Support에서 Billing 문제를 전문 에이전트에게 넘긴다면 작업 인계가 더 자연스러울 수 있다.

### Local Subagent와 Remote Agent

같은 프로세스 안의 하위 에이전트 호출과 독립 서비스의 에이전트 호출은 운영 경계가 다르다. 원격 에이전트에는 다음이 필요할 수 있다.

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

그리고 작업 인계에서는 컨텍스트뿐 아니라 상태와 판단하거나 실행할 권한도 전달 경계를 가져야 한다. 다음 장에서는 이 협업이 같은 애플리케이션 내부가 아니라 독립 에이전트 시스템 사이에서 일어날 때 필요한 Protocol Boundary를 본다. A2A와 원격 에이전트를 다룬다.

### Source Notes

- [S-OAI-AGENTS]
- [S-GOOGLE-ADK]
- [B-OWNERSHIP]

---

<!-- source-draft: chapters/24/draft.md -->

## 24장. A2A와 Remote Agent

한 애플리케이션 안에서 하위 에이전트를 호출하는 것은 비교적 단순하다. 같은 실행 환경, 같은 상태 저장소, 같은 인증 정보를 공유할 수 있다. 다른 조직이나 다른 서비스가 운영하는 에이전트를 호출하면 이야기가 달라진다. 상대 에이전트의 내부 도구와 메모리를 직접 알 수 없고, 네트워크 접근 경계가 있으며, 인증(Authentication)과 작업의 시작부터 종료까지의 과정이 필요하다. A2A는 이처럼 독립된 에이전트 시스템들이 서로를 찾고 메시지를 교환하며, 작업의 시작부터 종료까지를 관리하고 산출물을 전달하는 등 함께 동작하는 데 필요한 문제를 다룬다.

2026-10-02 기준 A2A의 최신 정식 명세는 1.0.0이다. 이 장에서는 버전별 JSON 표현보다 1.0에서도 유지되는 Agent Card, 메시지, 작업, 산출물, 권한 확인(Authorization)의 책임 경계에 집중한다.

### Remote Agent는 Tool과 다르다

도구는 bounded capability를 제공한다. 원격 에이전트는 자체적으로 다음을 가질 수 있다.

- 모델
- 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)
- Tools
- 상태
- 정책
- 장시간 작업

따라서:

~~~text
Tool Call
≠ Remote Agent Delegation
~~~

원격 에이전트는 단순 함수 호출보다 더 긴 유지 과정을 가질 수 있다.

### A2A의 위치

이 책에서는 다음처럼 구분한다.

~~~text
MCP
Agent ↔ Capability Provider

A2A
Agent System ↔ Independent Agent System
~~~

MCP가 Tool/Resource Integration을 다룬다면 A2A는 에이전트 단위 Work Collaboration을 다룬다.

### Agent Card

원격 에이전트가 어떤 기능을 제공하는지 Discover할 수 있다.

예:

~~~text
Compliance Review Agent
- policy review
- evidence analysis
- compliance report
~~~

하지만 Agent Card는 권한 확인이 아니다. 기능이 존재한다고 누구나 호출할 수 있는 것은 아니다.

### Message

에이전트 사이 Interaction은 메시지로 표현될 수 있다. 메시지는 단순 String보다 구조화된 내용을 가질 수 있다. 중요한 것은 Protocol Message와 내부 Conversation State를 동일시하지 않는 것이다.

### A2A Task

원격 에이전트에 위임한 업무는 작업의 시작부터 종료까지의 과정을 가질 수 있다. 2026-10-02 기준 A2A 0.3.0에는 다음 Task state가 정의돼 있다. 정확한 state 목록은 protocol version에 따라 달라질 수 있으므로 출간 전 다시 확인한다.

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

이 작업은 MCP Task와 다르다.

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

상위 작업 항목이 여러 Protocol Task를 포함할 수 있다.

### Artifact

A2A에서는 원격 에이전트가 결과를 산출물로 전달할 수 있다.

예:

- report
- generated file
- analysis result
- structured data

산출물은 메시지와 다르다. 메시지가 서로 주고받는 대화나 상호작용을 나타낸다면, 산출물은 전달할 결과물에 가깝다.

### Input Required

원격 에이전트가 추가 정보가 필요할 수 있다.

~~~text
working
  ↓
input-required
  ↓
client provides info
  ↓
working
~~~

오래 실행되는 에이전트의 Pause/Resume와 유사하다. Protocol Lifecycle이 내부 상태 관리 계층과 연결될 수 있다.

### Auth Required

원격 에이전트가 추가 권한 확인을 요구할 수도 있다. 이 경우 Caller Identity와 Originating User Context를 어떻게 전달할지 중요해진다.

~~~text
User
→ Local Agent
→ Remote Agent
→ Remote Tool
~~~

원격 에이전트가 자신의 broad Service Credential만 사용해 사용자의 권한 범위를 초과하지 않도록 한다.

### Capability Discovery와 Authorization

다시 같은 원칙이 나온다.

~~~text
Agent Card
= what is available

Authorization
= can this caller use it
~~~

Remote Agent Server가 최종 Access Policy를 강제해야 한다. A2A 1.0의 AUTH_REQUIRED 상태 자체도 특정 행동을 승인했다는 뜻은 아니며, 실제 Authorization Scope와 인증 정보(Credential) 의미는 구현이나 Credential Issuer가 별도로 정의해야 한다.

### Async Work

원격 에이전트는 즉시 결과를 반환하지 않을 수 있다.

장시간 작업이라면:

- status query
- streaming
- notification
- artifact update

가 필요하다. 이때 Local Agent는 Remote Task State를 자신의 Internal Goal State와 연결할 수 있다.

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

원격 에이전트가 실패하면 Local Agent가 판단해야 한다.

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

원격 에이전트가 반환한 산출물을 자동으로 Trusted Result로 보지 않는다. 필요하면 Local Verification을 한다.

~~~text
Remote Agent
→ Artifact
→ Local Verifier
→ Accept
~~~

특히 다른 Organization이나 Trust Domain의 에이전트라면 중요하다.

### A2A와 Internal Domain

통신 규약의 객체를 내부 Domain Model에 직접 종속시키지 않는 원칙은 MCP와 같다.

~~~text
Internal Delegation Model
        ↓
A2A Adapter
        ↓
Remote Agent
~~~

Protocol Version이 바뀌어도 내부 목표와 Artifact Model을 유지하기 쉽다.

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

원격 에이전트는 전문 역할을 맡더라도 최종 판단·실행 권한을 가진 주체는 아닐 수 있다.

### 이 장에서 가져갈 것

원격 에이전트를 도구처럼 단순화하면 유지 과정과 판단하거나 실행할 권한을 놓칠 수 있다. 다음 경계를 유지한다.

~~~text
MCP Task
≠ A2A Task
≠ Factory Task

Remote Agent
≠ Local Subagent
~~~

A2A는 independent Agent System 간 Collaboration Boundary다. 이제 책의 마지막 장에서 지금까지의 내용을 도입 순서로 압축한다. 처음부터 메모리, 여러 에이전트의 협업, 경량 가상 머신을 모두 넣지 않고 Minimum Viable 운영 에이전트에서 어떻게 시작할 것인가.

### Source Notes

- [S-A2A-0.3]
- [S-MCP-2026-07]

---

<!-- source-draft: chapters/25/draft.md -->

## 25장. Minimum Viable Production Agent

여기까지 읽으면 에이전트 시스템에 넣을 수 있는 기능이 매우 많아 보인다.

- 메모리
- 상태 관리 계층
- 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)
- 신원
- Credential Broker
- Policy Engine
- 평가
- 여러 에이전트의 협업
- MCP
- A2A

처음부터 모두 만들 필요는 없다. 그렇게 시작하면 에이전트보다 이를 뒷받침할 플랫폼을 먼저 만들게 될 수 있다. 실제 운영에 쓸 에이전트도 더 작은 구조에서 출발할 수 있다.

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

이 구조가 작업을 끝낼 수 있는지 먼저 본다.

### 1단계: Clear Tool Contract

에이전트가 어떤 행동을 할 수 있는지 좁힌다.

예:

~~~text
read_file
edit_file
run_test
git_diff
~~~

처음부터 Generic Shell + Full Network + 권한 범위가 넓은 인증 정보를 줄 이유는 없다. 도구 사용 계약(Tool Contract: 도구의 입력·출력·사용 조건)과 Error Model을 먼저 만든다.

### 2단계: Controlled Runtime

에이전트가 잘못 행동해도 피해가 제한되도록 한다.

예:

- Workspace Scope
- Network Allowlist
- Resource Limit
- No Production Credential

기능보다 경계를 먼저 만든다.

### 3단계: Deterministic Verification

완료했다는 주장을 모델에게 맡기지 않는다.

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

실패했을 때 이유를 볼 수 있어야 한다. 처음부터 거대한 Observability Platform이 필요하지 않다.

최소한:

- model call
- tool call
- result
- failure
- verification

을 연결할 수 있게 한다.

### 5단계: Eval

운영 실패를 모아 회귀를 확인할 평가 사례를 만든다.

~~~text
Failure
→ Eval Case
→ Fix
→ Re-run
~~~

에이전트를 "감으로 개선"하지 않는다.

### 6단계: Durable State

작업이 한 프로세스를 넘어가기 시작하면 상태 관리 계층이 필요해진다.

Trigger:

- 승인 대기
- 장시간 실행
- 비정상 종료 뒤 복구
- 외부 상태 변경
- Multi-step Goal

이때 이벤트 이력, 목표, 산출물, 승인 상태를 도입한다.

### 7단계: Identity와 Policy

외부 시스템에 접근하기 시작하면:

- 사용자 / 에이전트의 신원
- 인증 정보로 행사할 수 있는 권한 범위
- 권한 확인(Authorization)
- 샌드박스
- 승인

을 분리한다. 위험이 올라갈수록 통제를 강화한다.

### 8단계: Memory

반복 작업에서 이득이 확인될 때 추가한다.

메모리를 넣기 전 질문:

~~~text
무엇을 반복해서 다시 찾고 있는가?
어떤 Lesson이 재사용 가능한가?
Source of Truth로 다시 읽을 수 없는가?
Memory Risk를 감당할 가치가 있는가?
~~~

필요성이 없으면 넣지 않아도 된다.

### 9단계: Long-running

작업이 길어지면:

- 중간 완료 지점
- Progress State
- 단계별 실행 한도
- 상태 재조정(Reconciliation: 현재 외부 상태와 내부 판단을 다시 맞추는 과정)
- Verification Reserve

를 추가한다. 긴 컨텍스트만 늘리는 것으로 해결하지 않는다.

### 10단계: Multi-Agent

Single-Agent Baseline이 안정된 뒤에도 컨텍스트(Context: 모델에 전달하는 정보)·권한 분리, 독립 검증, 병렬화에서 명확한 이득이 있을 때만 여러 에이전트의 협업을 추가한다. 판단 기준 자체는 22장에서 다뤘으므로 여기서는 확장 순서의 마지막 선택지로만 둔다.

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

공식 Maturity Model이나 권장 순서를 뜻하지 않는다. 시스템의 위험과 업무 특성에 따라 순서는 달라질 수 있으며, 필요한 문제가 생길 때 어떤 구조를 추가할지 보여주는 참조다.

### Control before Autonomy

에이전트 엔지니어링에서 자주 반대로 진행한다.

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

즉 에이전트에게 더 많은 기능을 주기 전에 실패를 감당할 구조를 만든다.

### Verification before Scale

한 에이전트가 작업을 안정적으로 끝내지 못하는데 에이전트 수를 늘리면 실패도 병렬화될 수 있다.

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

승인이 필요해졌다.

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

장시간 작업이 생겼다.

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

에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층):

~~~text
one Agent execution
one Goal
events
progress
approval
artifact
recovery
~~~

소프트웨어 팩토리의 제어 계층:

~~~text
many work items
worker fleet
scheduling
assignment
acceptance
delivery
feedback
~~~

에이전트 엔지니어링이 한 작업 수행 주체를 신뢰할 수 있게 만드는 문제라면 Software Factory Engineering은 많은 업무를 시스템적으로 흘리는 문제다.

### 언제 Factory로 넘어가는가

다음 문제가 커지면 Agent-level Architecture만으로는 부족해진다.

- Backlog가 많다.
- 여러 작업 수행 주체가 있다.
- Task Dependency가 있다.
- Assignment가 필요하다.
- Acceptance Authority가 필요하다.
- Merge/Deploy Delivery가 필요하다.
- Retry/Reassignment가 조직 수준에서 필요하다.

이때 소프트웨어 팩토리의 제어 계층이 등장한다.

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

각 항목의 필요 수준은 시스템 위험에 따라 달라진다. 중요한 것은 기능 목록을 채우는 것이 아니라 이 질문에 명시적으로 답할 수 있는가이다.

### 이 장에서 가져갈 것

운영 에이전트는 기능 수로 정의되지 않는다. 더 중요한 것은 다음이다.

~~~text
Can it act?
Can it be constrained?
Can it be observed?
Can it recover?
Can it prove completion?
~~~

에이전트 엔지니어링의 목표는 에이전트를 최대한 자유롭게 만드는 것이 아니다. 필요한 자유를 주면서도 업무를 맡길 수 있는 구조를 만드는 것이다. 이 책의 마지막에는 하나의 원칙이 남는다.

> 모델을 더 믿는 것이 아니라, 모델을 덜 믿어도 일을 맡길 수 있는 시스템을 만든다.

Epilogue에서 이 관점을 다시 정리한다.

### Source Notes

- [B-AGENT-CAPABILITY]
- [B-STATE-PLANE]
- [B-FACTORY-BOUNDARY]
