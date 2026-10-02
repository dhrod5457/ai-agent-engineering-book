# 7장. Session, Workspace, Goal, Memory를 분리한다

Agent를 오래 실행하기 시작하면 거의 모든 문제가 "상태"라는 이름 아래 모인다.

대화 기록도 상태다. 현재 작업 디렉터리도 상태다. 완료해야 할 목표도 상태다. 생성한 파일도 상태다. 이전 실행에서 배운 내용도 상태다.

문제는 이들을 같은 것으로 취급할 때 생긴다.

Session을 지우면 Goal이 사라지고, Runtime이 종료되면 Progress가 사라지고, 오래된 Memory가 현재 사실보다 우선하고, Conversation Summary가 실행 이력을 대신하게 된다.

Long-running Agent를 설계하려면 먼저 **서로 다른 수명과 권한을 가진 상태를 분리해야 한다.**

## "Memory"라는 단어가 너무 많은 것을 가린다

Agent 제품에서는 다음 기능을 모두 Memory라고 부르는 경우가 있다.

- Conversation History
- User Preference
- Current Task Progress
- Previous Tool Result
- Workspace File
- Long-term Lesson
- Retrieved Document

사용자 경험 관점에서는 이해하기 쉬운 표현일 수 있다.

Architecture에서는 위험하다.

각 항목의 수명과 신뢰도가 다르기 때문이다.

이 책에서는 다음을 구분한다.

~~~text
Inference Context
Conversation / Session State
Run State
Workspace State
Goal / Task State
Artifact State
Long-term Memory
External Source of Truth
~~~

이 taxonomy는 업계 표준 분류가 아니라 여러 SDK와 Runtime 구현에서 반복되는 차이를 설명하기 위한 이 책의 정리다.

## Inference Context

Context는 현재 한 번의 Model Inference에 들어가는 정보다.

앞 장에서 본 것처럼 Context는 Projection이다.

~~~text
State / Sources
      ↓
Context Selection
      ↓
Inference Context
~~~

Context는 일시적이다.

다음 Turn에는 다른 정보가 들어갈 수 있다.

## Conversation / Session State

Session은 여러 Turn의 대화 연속성을 유지한다.

예:

~~~text
User Message
Assistant Message
Tool Call
Tool Result
User Correction
~~~

Session은 매우 유용하다.

하지만 Session이 Goal이나 Runtime State 전체를 의미하지는 않는다.

예를 들어 사용자와 20 Turn을 대화했다고 해서 현재 Goal의 Completion Condition이 명확하게 구조화돼 있다는 보장은 없다.

Session History에는 "테스트가 통과했다"고 적혀 있어도 Artifact나 Test Result가 현재 유효한지는 별도 확인해야 한다.

## Run State

Run State는 현재 실행의 lifecycle을 표현한다.

예:

~~~text
READY
RUNNING
AWAITING_INPUT
AWAITING_APPROVAL
VERIFYING
COMPLETED
FAILED
~~~

Run State는 Conversation보다 시스템 제어에 가깝다.

모델이 자연어로 "승인 대기 중입니다"라고 말하는 것과 시스템 상태가 AWAITING_APPROVAL인 것은 다르다.

후자는 Scheduler나 API가 deterministic하게 처리할 수 있다.

## Workspace State

Workspace는 실행환경의 상태다.

예:

- checked-out repository
- modified file
- installed package
- browser tab
- temporary build artifact
- local cache

Workspace는 편리하지만 durable하다고 가정하면 안 된다.

Cloud Runtime, Container, MicroVM은 종료될 수 있다.

~~~text
Workspace Exists
≠ Durable State Exists
~~~

AWS AgentCore 같은 Runtime 사례도 Session별 격리 환경을 제공하지만 그 Runtime State를 장기 durability와 동일하게 취급하지 않는다.

Workspace는 사라져도 다시 만들 수 있게 설계하는 편이 복구에 유리하다.

## Goal / Task State

Goal은 Agent가 무엇을 완료해야 하는지 표현한다.

예:

~~~text
objective
scope
constraints
budget
completion condition
verification requirement
~~~

Goal을 단순 User Prompt와 동일시하지 않는다.

사용자 Prompt가 다음과 같다고 하자.

> 로그인 오류 좀 고쳐줘.

실행 Goal은 더 구체적이어야 할 수 있다.

~~~text
Objective:
OAuth callback 오류 수정

Scope:
auth module only

Verification:
targeted test + integration test pass

Do not:
change public API

Budget:
max 30 tool turns
~~~

Goal은 현재 실행의 Completion Contract다.

## Artifact State

Artifact는 Agent가 만든 결과물이다.

예:

- file
- commit
- report
- screenshot
- generated document
- structured output

Artifact는 "완료했다"는 말과 다르다.

Artifact에는 다음 Metadata가 필요할 수 있다.

- location
- checksum
- created_at
- source run
- verification state
- version

특히 장기 Agent에서는 Artifact가 다음 Session의 Handoff 역할도 한다.

## Long-term Memory

Memory는 미래 실행에서 재사용할 정보를 보존한다.

예:

- 사용자의 선호
- 특정 Repository의 반복되는 작업 규칙
- 이전 해결에서 얻은 Lesson
- Agent가 자주 실수하는 Pattern

Memory는 현재 실행을 복구하기 위한 기본 저장소가 아니다.

~~~text
Checkpoint
= 현재 실행을 이어가기 위한 것

Memory
= 미래 실행에 재사용할 것
~~~

둘은 목적이 다르다.

## External Source of Truth

가장 중요한 상태가 Agent 내부에 없을 수도 있다.

예:

- 현재 Git HEAD
- Production Configuration
- Approved Requirement
- Current DB Record
- 최신 승인 상태
- 현재 가격
- 실제 배포 상태

이런 정보는 Agent가 소유하지 않는다.

Agent가 내부 State나 Memory에 복사해 둘 수는 있지만 복사본이 Canonical Source가 되지는 않는다.

~~~text
Working Copy
≠ Source of Truth
~~~

이 구분은 11장의 External State Reconciliation에서 중요해진다.

## 같은 정보도 수명이 다르다

하나의 정보가 여러 형태로 존재할 수 있다.

예를 들어 "현재 Branch는 feature/auth-fix"라는 사실을 생각해보자.

~~~text
Workspace:
git branch에서 실제 확인한 현재 값

Run State:
이 Run이 feature/auth-fix에서 시작했다고 기록

Context:
현재 Turn에서 Model에게 branch 정보를 제공

Memory:
"이 Repository는 feature branch를 사용한다"라는 과거 Lesson
~~~

시간이 지나 Branch가 바뀌면 이 값들은 서로 달라질 수 있다.

그래서 State에는 단순 Value뿐 아니라 다음 Metadata가 중요하다.

- source
- version
- timestamp
- owner
- scope
- freshness
- invalidation condition

## State Promotion

모든 Observation을 Durable State로 저장할 필요는 없다.

예를 들어 Shell Tool이 출력한 수천 줄 Log를 영구 저장하는 것은 과할 수 있다.

State를 단계적으로 승격한다고 생각할 수 있다.

~~~text
Ephemeral Observation
        ↓
Working State
        ↓
Checkpoint-worthy State
        ↓
Durable Goal / Artifact
        ↓
Optional Long-term Memory
~~~

Promotion 기준은 다음과 같을 수 있다.

- Recovery에 필요한가.
- Audit에 필요한가.
- Completion 판단에 필요한가.
- 다시 계산하기 비싼가.
- 다음 Session에서도 필요할 가능성이 높은가.
- 사용자의 명시적 Correction인가.

이 기준이 없으면 Agent System은 모든 것을 저장하거나 중요한 것을 놓치는 두 극단으로 가기 쉽다.

## Freshness와 Validity

State는 저장돼 있다고 유효한 것이 아니다.

예를 들어 다음 Memory가 있다고 하자.

~~~text
Production DB host = db-prod-1
~~~

몇 달 뒤 실제 환경은 db-prod-2로 바뀌었다.

Memory가 존재한다는 사실은 정확성을 보장하지 않는다.

따라서 State는 가능한 한 freshness와 invalidation rule을 가져야 한다.

예:

~~~text
source: infra-config
observed_version: 184
observed_at: 2026-10-02T10:20
valid_until: unknown
refresh_before: production_mutation
~~~

## Session을 Goal로 사용하면 생기는 문제

Goal을 Conversation에만 의존하면 다음 일이 생긴다.

사용자가 처음에 요구한다.

> 테스트를 고쳐줘.

중간에 다음 Correction을 준다.

> public API는 바꾸지 마.

Agent가 Compaction을 수행하면서 두 번째 조건이 Summary에서 약해질 수 있다.

Goal이 별도 구조라면 Constraint를 명시적으로 유지할 수 있다.

~~~text
Goal
objective: fix failing test
constraint:
  - public API must not change
~~~

Conversation은 Goal을 수정하는 Input이 될 수 있다.

Goal 자체와 동일하지 않다.

## Workspace를 Checkpoint로 사용하면 생기는 문제

Agent가 Local File을 수정했다.

프로세스가 죽었다.

Workspace가 유지돼 있다면 운 좋게 이어갈 수 있다.

하지만 다음 정보를 알 수 없을 수 있다.

- 수정이 완료된 것인가.
- Test는 실행했는가.
- 어떤 Tool Result를 기준으로 수정했는가.
- External Mutation은 이미 했는가.
- 다음 Step은 무엇인가.

Workspace는 실제 변경을 담지만 Execution Intent를 설명하지 않는다.

그래서 Durable State가 따로 필요하다.

## Memory를 Source of Truth로 사용하면 생기는 문제

Memory는 과거의 압축된 정보다.

Source of Truth는 현재의 Canonical Data다.

이 둘의 충돌에서 기본 원칙은 다음과 같다.

~~~text
Current Authoritative Source
        >
Stale Internal Memory
~~~

물론 Source 자체가 신뢰할 수 없는 경우도 있다.

그때는 Authority Ranking과 Reconciliation Rule이 필요하다.

하지만 "Memory가 있으니 다시 조회하지 않는다"는 기본값은 위험하다.

## 작은 예: Coding Agent의 State

하나의 Coding Task를 분해해보자.

~~~text
Goal
- UserService timeout bug 수정
- 관련 test pass

Session
- 사용자와의 대화
- 추가 요구사항

Run State
- RUNNING

Workspace
- branch feature/timeout-fix
- modified UserService.java

Artifact
- commit candidate
- test report

Memory
- 이 Repository는 integration test가 느리다는 과거 Lesson

External Source
- current remote main HEAD
- current CI configuration
~~~

이 분리를 하면 어떤 State를 어디에서 복구해야 하는지 선명해진다.

## 이 장에서 가져갈 것

Agent에서 "State"라는 단어 하나로 모든 것을 설명하면 Lifecycle과 Trust Boundary가 섞인다.

최소한 다음 경계를 유지한다.

~~~text
Context
≠ Session
≠ Run
≠ Workspace
≠ Goal
≠ Artifact
≠ Memory
≠ Source of Truth
~~~

다음 질문은 자연스럽다.

이렇게 분리한 상태를 어디에서 관리할 것인가.

프로세스가 죽고 Runtime이 교체돼도 Goal과 Progress, Approval과 Artifact를 잃지 않으려면 어떤 계층이 필요할까.

다음 장에서는 이 책의 핵심 synthesis인 Agent State Plane을 다룬다.

## 주요 근거

- OpenAI Agents SDK Sessions
- OpenAI Sandbox Agent Memory
- OpenAI Codex Goals
- AWS AgentCore Runtime Sessions
- Google ADK Session / Event model
- research/topics/09-state-memory-taxonomy.md
