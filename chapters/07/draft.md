# 7장. Session, Workspace, Goal, Memory를 분리한다

에이전트를 오래 실행하기 시작하면 거의 모든 문제가 "상태"라는 이름 아래 모인다. 대화 기록도 상태다. 현재 작업 디렉터리도 상태다. 완료해야 할 목표도 상태다. 생성한 파일도 상태다. 이전 실행에서 배운 내용도 상태다. 문제는 이들을 같은 것으로 취급할 때 생긴다. 세션을 지우면 목표가 사라지고, 실행 환경이 종료되면 진행 상황이 사라지고, 오래된 메모리가 현재 사실보다 우선하고, 대화 요약이 실행 이력을 대신하게 된다. 오래 실행되는 에이전트를 설계하려면 먼저 **서로 다른 수명과 권한을 가진 상태를 분리해야 한다.**

## "Memory"라는 단어가 너무 많은 것을 가린다

에이전트 제품에서는 다음 기능을 모두 메모리라고 부르는 경우가 있다.

- 대화 기록
- User Preference
- Current Task Progress
- Previous Tool Result
- Workspace File
- Long-term Lesson
- Retrieved Document

사용자에게는 이해하기 쉬운 표현일 수 있다. 하지만 시스템을 설계할 때는 주의해야 한다. 각 항목이 유지되는 기간과 신뢰할 수 있는 정도가 다르기 때문이다. 이 책에서는 다음을 구분한다.

~~~text
Inference Context
Conversation / Session State
Run State
Workspace State
Goal State
Artifact State
Long-term Memory
External Source of Truth
~~~

이 분류 체계는 업계 표준이 아니라 여러 SDK와 실행 환경 구현에서 반복되는 유지 과정과 authority 차이를 설명하기 위한 working model이다.

## Inference Context

컨텍스트(Context: 모델에 전달하는 정보)는 현재 한 번의 모델 실행에 들어가는 정보다. 앞 장에서 본 것처럼 컨텍스트는 필요한 정보만 골라 구성한 것이다.

~~~text
State / Sources
      ↓
Context Selection
      ↓
Inference Context
~~~

컨텍스트는 일시적이다. 다음 차례에는 다른 정보가 들어갈 수 있다.

## Conversation / Session State

세션은 여러 차례의 대화 연속성을 유지한다.

예:

~~~text
User Message
Assistant Message
Tool Call
Tool Result
User Correction
~~~

세션은 매우 유용하다. 하지만 세션이 목표나 실행 환경의 상태 전체를 의미하지는 않는다. 예를 들어 사용자와 20 차례를 대화했다고 해서 현재 목표의 완료 조건이 명확하게 구조화돼 있다는 보장은 없다. 세션 이력에는 "테스트가 통과했다"고 적혀 있어도 산출물이나 테스트 결과가 현재 유효한지는 별도 확인해야 한다.

## Run State

개별 실행 상태는 현재 실행의 유지 과정을 표현한다.

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

개별 실행 상태는 대화보다 시스템 제어에 가깝다. 모델이 자연어로 "승인 대기 중입니다"라고 말하는 것과 시스템 상태가 AWAITING_APPROVAL인 것은 다르다. 후자는 스케줄러나 API가 정해진 규칙에 따라 처리할 수 있다.

## Workspace State

작업 공간은 실행환경의 상태다.

예:

- checked-out repository
- modified file
- installed package
- browser tab
- temporary build artifact
- local cache

작업 공간은 편리하지만 durable하다고 가정하면 안 된다. Cloud Runtime, 컨테이너, 경량 가상 머신은 종료될 수 있다.

~~~text
Workspace Exists
≠ Durable State Exists
~~~

AWS AgentCore 같은 실행 환경 사례도 세션별 격리 환경을 제공한다. 기본 microVM의 memory와 local disk는 compute lifecycle에 묶이지만, 2026-10-02 기준 별도 managed session storage를 구성하면 stop/resume 사이에 filesystem을 복원할 수 있다. 다만 이 storage도 session lifecycle과 runtime version에 제약을 받으므로 목표, 승인, 장기 메모리 같은 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)와 동일하게 취급하지 않는다. 따라서 작업 공간이 유지될 수 있더라도 실행 연속성의 유일한 근거로 삼지 않는 편이 복구에 유리하다.

## Goal State

목표는 에이전트가 무엇을 완료해야 하는지 표현한다.

예:

~~~text
objective
scope
constraints
budget
completion condition
verification requirement
~~~

목표를 단순 User Prompt와 동일시하지 않는다. 사용자 프롬프트가 다음과 같다고 하자.

> 로그인 오류 좀 고쳐줘.

실행 목표는 더 구체적이어야 할 수 있다.

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

목표는 현재 실행의 완료를 인정할 조건이다.

## Artifact State

산출물은 에이전트가 만든 결과물이다.

예:

- file
- commit
- report
- screenshot
- generated document
- structured output

산출물은 "완료했다"는 말과 다르다. 산출물에는 다음 부가 정보가 필요할 수 있다.

- location
- checksum
- created_at
- source run
- verification state
- version

특히 장기 에이전트에서는 산출물이 다음 세션의 작업 인계 역할도 한다.

## Long-term Memory

메모리는 미래 실행에서 재사용할 정보를 보존한다.

예:

- 사용자의 선호
- 특정 저장소의 반복되는 작업 규칙
- 이전 해결에서 얻은 교훈
- 에이전트가 자주 실수하는 패턴

메모리는 현재 실행의 복구 상태를 담는 기본 저장소로 보지 않는다.

~~~text
Checkpoint
= 현재 실행을 이어가기 위한 것

Memory
= 미래 실행에 재사용할 것
~~~

둘은 목적이 다르다.

## External Source of Truth

가장 중요한 상태가 에이전트 내부에 없을 수도 있다.

예:

- 현재 Git HEAD
- Production Configuration
- Approved Requirement
- Current DB Record
- 최신 승인 상태
- 현재 가격
- 실제 배포 상태

이런 정보는 에이전트가 소유하지 않는다. 에이전트가 내부 상태나 메모리에 복사해 둘 수는 있지만 복사본이 기준 원본이 되지는 않는다.

~~~text
Working Copy
≠ Source of Truth
~~~

이 구분은 11장의 외부 상태와 내부 판단의 재조정에서 중요해진다.

## 같은 정보도 수명이 다르다

하나의 정보가 여러 형태로 존재할 수 있다. 예를 들어 "현재 브랜치는 feature/auth-fix"라는 사실을 생각해보자.

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

시간이 지나 브랜치가 바뀌면 이 값들은 서로 달라질 수 있다. 그래서 상태에는 단순 Value뿐 아니라 다음 부가 정보가 중요하다.

- source
- version
- timestamp
- owner
- scope
- 정보가 최신인지 여부
- invalidation condition

## State Promotion

모든 관찰 결과를 영속 상태로 저장할 필요는 없다. 예를 들어 Shell Tool이 출력한 수천 줄 로그를 영구 저장하는 것은 과할 수 있다. 여기서는 편의상 관찰 결과를 더 오래 유지되는 상태로 옮기는 과정을 State Promotion이라고 부른다.

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

- 복구에 필요한가.
- 감사에 필요한가.
- 완료 판단에 필요한가.
- 다시 계산하기 비싼가.
- 다음 세션에서도 필요할 가능성이 높은가.
- 사용자의 명시적 Correction인가.

이 기준이 없으면 에이전트 시스템은 모든 것을 저장하거나 중요한 것을 놓치는 두 극단으로 가기 쉽다.

## Freshness와 Validity

상태는 저장돼 있다고 유효한 것이 아니다. 예를 들어 다음 메모리가 있다고 하자.

~~~text
Production DB host = db-prod-1
~~~

몇 달 뒤 실제 환경은 db-prod-2로 바뀌었다. 메모리가 존재한다는 사실은 정확성을 보장하지 않는다. 따라서 상태는 가능한 한 정보가 최신인지 여부와 invalidation rule을 가져야 한다.

예:

~~~text
source: infra-config
observed_version: 184
observed_at: 2026-10-02T10:20
valid_until: unknown
refresh_before: production_mutation
~~~

## Session을 Goal로 사용하면 생기는 문제

목표를 대화에만 의존하면 다음 일이 생긴다. 사용자가 처음에 요구한다.

> 테스트를 고쳐줘.

중간에 다음 Correction을 준다.

> public API는 바꾸지 마.

에이전트가 컨텍스트 압축(Compaction: 입력 정보를 줄이는 압축)을 수행하면서 두 번째 조건이 요약에서 약해질 수 있다. 목표가 별도 구조라면 제약 조건을 명시적으로 유지할 수 있다.

~~~text
Goal
objective: fix failing test
constraint:
  - public API must not change
~~~

대화는 목표를 수정하는 입력이 될 수 있다. 목표 자체와 동일하지 않다.

## Workspace를 Checkpoint로 사용하면 생기는 문제

에이전트가 Local File을 수정했다. 프로세스가 죽었다. 작업 공간이 유지돼 있다면 운 좋게 이어갈 수 있다. 하지만 다음 정보를 알 수 없을 수 있다.

- 수정이 완료된 것인가.
- 테스트는 실행했는가.
- 어떤 도구 실행 결과를 기준으로 수정했는가.
- 외부 상태 변경은 이미 했는가.
- 다음 단계는 무엇인가.

작업 공간은 실제 변경을 담지만 실행 의도를 설명하지 않는다. 그래서 영속 상태가 따로 필요하다.

## Memory를 Source of Truth로 사용하면 생기는 문제

메모리는 과거 정보를 재사용하기 위한 내부 데이터이고, 외부의 기준 원본은 현재의 기준 데이터다. 둘이 충돌하면 기본적으로 최신 공식 기준 원본을 다시 확인해야 한다. 이 원칙의 운영 측면은 11장의 상태 재조정(Reconciliation: 현재 외부 상태와 내부 판단을 다시 맞추는 과정)에서, 메모리 자체의 유지 과정과 security는 Part IV에서 자세히 다룬다.

## 작은 예: Coding Agent의 State

하나의 코드 작업을 분해해보자.

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

이 분리를 하면 어떤 상태를 어디에서 복구해야 하는지 선명해진다.

## 이 장에서 가져갈 것

에이전트에서 "상태"라는 단어 하나로 모든 것을 설명하면 유지 과정과 신뢰 경계가 섞인다. 최소한 다음 경계를 유지한다.

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

다음 질문은 자연스럽다. 이렇게 분리한 상태를 어디에서 관리할 것인가. 프로세스가 죽고 실행 환경이 교체돼도 목표와 진행 상황, 승인과 산출물을 잃지 않으려면 어떤 계층이 필요할까. 다음 장에서는 이 책의 핵심 설명용 개념인 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)을 다룬다.

## 주요 근거

- OpenAI Agents SDK Sessions
- OpenAI Sandbox Agent Memory
- OpenAI Codex Goals
- AWS AgentCore Runtime Sessions
- Google ADK Session / Event model
- research/topics/09-state-memory-taxonomy.md
