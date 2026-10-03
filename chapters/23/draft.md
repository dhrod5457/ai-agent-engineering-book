# 23장. Agent-as-Tool과 Handoff

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

## Agent-as-Tool

전체 작업을 관리하는 에이전트가 전체 목표와 User Interaction을 계속 소유한다. Specialist Agent는 bounded subtask를 수행하고 결과를 반환한다.

~~~text
Manager
  ├─ Research Agent
  ├─ Code Review Agent
  └─ Security Agent
~~~

전문 역할의 에이전트는 도구와 비슷한 역할을 한다.

## 장점

### Ownership이 명확하다

최종 완료는 전체 작업을 관리하는 에이전트가 판단한다.

### Context를 격리할 수 있다

전문 역할의 에이전트에게 필요한 정보만 제공할 수 있다.

### Permission을 좁힐 수 있다

조사 에이전트는 read-only일 수 있다.

## 단점

### Manager Bottleneck

모든 결과가 전체 작업을 관리하는 에이전트로 돌아온다.

### Context Concentration

전체 작업을 관리하는 에이전트가 전체 상태를 많이 들고 있어야 할 수 있다.

### Result Interpretation

Specialist Result를 전체 작업을 관리하는 에이전트가 다시 해석해야 한다.

## Handoff

작업 인계는 업무 또는 Interaction Ownership을 다른 에이전트에게 넘긴다.

~~~text
Agent A
  ↓ handoff
Agent B
  ↓ owns next interaction
~~~

예를 들어 학생 상담 에이전트가 장학 관련 문의를 Scholarship Agent로 넘긴다. 이후 Scholarship Agent가 사용자와 직접 Interaction할 수 있다.

## Handoff Contract

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

## Context Transfer

작업 인계는 모든 컨텍스트(Context: 모델에 전달하는 정보)를 복제하는 것이 아니다. 에이전트 B에게 필요한 정보만 골라 컨텍스트를 구성한다.

~~~text
State Plane
   ↓
Handoff Projection
   ↓
Agent B Context
~~~

이 구조는 Part II Context Engineering과 연결된다.

## Authority Transfer

가장 중요한 문제 중 하나다. 에이전트 A가 가진 권한이 에이전트 B에게 자동으로 전달되는가. 항상 그렇지 않다.

예:

~~~text
Agent A
→ read student record

Agent B
→ scholarship decision support
~~~

에이전트 B는 다른 도구의 권한 범위를 가질 수 있다. 작업 인계에는 업무를 책임지는 주체 전달뿐 아니라 receiving Agent의 실제로 적용되는 권한 재평가가 필요하다.

## State Ownership

작업 인계 후 Goal State를 누가 수정하는가. 두 에이전트가 동시에 같은 목표를 수정하면 충돌이 생길 수 있다.

패턴:

### Single Owner

현재 Active Agent만 목표를 수정.

### Shared State with Version

여러 에이전트가 Versioned State를 수정.

### Parent/Child Goal

Manager Goal 아래 Specialist Subgoal을 둔다. 각 시스템에 맞게 선택한다.

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

"검토 완료"만 반환하면 전체 작업을 관리하는 에이전트가 검토 내용을 알 수 없다.

## Independent Verifier

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

## Failure

전문 역할의 에이전트가 실패하면 Parent가 어떻게 처리할지 정한다.

~~~text
Specialist Failed
  ├─ retry same specialist
  ├─ use alternative specialist
  ├─ resume in manager
  └─ escalate
~~~

작업 인계 뒤 실패가 발생하면 담당 책임을 되돌릴지 정해야 한다.

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

전체 작업을 관리하는 에이전트가 수정 여부를 결정하고 완료를 유지한다. 여기서는 작업 인계보다 Agent-as-Tool이 자연스럽다. 반면 Customer Support에서 Billing 문제를 전문 에이전트에게 넘긴다면 작업 인계가 더 자연스러울 수 있다.

## Local Subagent와 Remote Agent

같은 프로세스 안의 하위 에이전트 호출과 독립 서비스의 에이전트 호출은 운영 경계가 다르다. 원격 에이전트에는 다음이 필요할 수 있다.

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

그리고 작업 인계에서는 컨텍스트뿐 아니라 상태와 판단하거나 실행할 권한도 전달 경계를 가져야 한다. 다음 장에서는 이 협업이 같은 애플리케이션 내부가 아니라 독립 에이전트 시스템 사이에서 일어날 때 필요한 Protocol Boundary를 본다. A2A와 원격 에이전트를 다룬다.

## 주요 근거

- OpenAI Agents SDK
- Google ADK
- research/topics/07-multi-agent-interoperability.md
