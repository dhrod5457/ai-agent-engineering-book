# 23장. Agent-as-Tool과 Handoff

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

이 장에서는 이를 Agent-as-Tool과 Handoff로 나눈다.

## Agent-as-Tool

Manager가 전체 Goal과 User Interaction을 계속 소유한다.

Specialist Agent는 bounded subtask를 수행하고 Result를 반환한다.

~~~text
Manager
  ├─ Research Agent
  ├─ Code Review Agent
  └─ Security Agent
~~~

Specialist는 Tool과 비슷한 역할을 한다.

## 장점

### Ownership이 명확하다

최종 Completion은 Manager가 판단한다.

### Context를 격리할 수 있다

Specialist에게 필요한 정보만 제공할 수 있다.

### Permission을 좁힐 수 있다

Research Agent는 read-only일 수 있다.

## 단점

### Manager Bottleneck

모든 Result가 Manager로 돌아온다.

### Context Concentration

Manager가 전체 State를 많이 들고 있어야 할 수 있다.

### Result Interpretation

Specialist Result를 Manager가 다시 해석해야 한다.

## Handoff

Handoff는 Work 또는 Interaction Ownership을 다른 Agent에게 넘긴다.

~~~text
Agent A
  ↓ handoff
Agent B
  ↓ owns next interaction
~~~

예를 들어 학생 상담 Agent가 장학 관련 문의를 Scholarship Agent로 넘긴다.

이후 Scholarship Agent가 사용자와 직접 Interaction할 수 있다.

## Handoff Contract

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

## Context Transfer

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

## Authority Transfer

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

Handoff에는 Work Ownership뿐 아니라 Effective Authorization 재평가가 필요하다.

## State Ownership

Handoff 후 Goal State를 누가 수정하는가.

두 Agent가 동시에 같은 Goal을 수정하면 Conflict가 생길 수 있다.

패턴:

### Single Owner

현재 Active Agent만 Goal을 수정.

### Shared State with Version

여러 Agent가 Versioned State를 수정.

### Parent/Child Goal

Manager Goal 아래 Specialist Subgoal을 둔다.

각 시스템에 맞게 선택한다.

## Result Contract

Agent-as-Tool에서는 Specialist Result Format이 중요하다.

예:

~~~text
status
findings
evidence_refs
uncertainties
recommended_next_action
~~~

"검토 완료"만 반환하면 Manager가 실제 내용을 알 수 없다.

## Independent Verifier

Executor Agent와 Verifier Agent를 분리할 수 있다.

~~~text
Executor
→ Artifact

Verifier
→ inspect Artifact
→ PASS / FAIL + evidence
~~~

하지만 독립성이 실제로 있어야 한다.

가능하면 Verifier가:

- 다른 Tool
- 다른 Evidence
- deterministic test

를 사용할 수 있다.

## Failure

Specialist가 실패하면 Parent가 어떻게 처리할지 정한다.

~~~text
Specialist Failed
  ├─ retry same specialist
  ├─ use alternative specialist
  ├─ resume in manager
  └─ escalate
~~~

Handoff 뒤 Failure가 발생하면 Ownership을 되돌릴지 정해야 한다.

## 작은 예: 코드 변경과 Security Review

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

## Local Subagent와 Remote Agent

같은 Process 안의 Subagent 호출과 독립 Service의 Agent 호출은 운영 경계가 다르다.

Remote Agent에는 다음이 필요할 수 있다.

- network
- authentication
- authorization
- task lifecycle
- async update
- artifact transfer

이 문제는 다음 장의 A2A와 연결된다.

## 이 장에서 가져갈 것

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

## 주요 근거

- OpenAI Agents SDK
- Google ADK
- research/topics/07-multi-agent-interoperability.md
