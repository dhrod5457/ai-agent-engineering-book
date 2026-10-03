# 12장. Agent Memory의 실제 경계

에이전트에 메모리를 붙이면 더 똑똑해질 것처럼 보인다. 이전 대화를 기억하고, 과거 실수를 기억하고, 사용자의 선호를 기억하고, 저장소 구조도 기억한다. 하지만 무엇을 기억할지보다 먼저 물어야 할 질문이 있다.

> 이 정보는 정말 장기 메모리에 들어가야 하는가?

에이전트 시스템에서 메모리는 자주 과도하게 사용된다. 세션 이력도 메모리라고 부르고, 현재 진행 상황도 메모리라고 부르고, 벡터 데이터베이스도 메모리라고 부른다. 이렇게 되면 실행 복구와 장기 학습, 사용자 선호와 외부 사실이 한 저장소에 섞인다. 이 장에서는 메모리의 범위를 좁힌다.

## Memory는 Execution State가 아니다

앞 Part에서 다음을 분리했다.

~~~text
Session
Run State
Workspace
Goal
Artifact
External Source
~~~

이 정보들은 현재 실행을 이해하고 복구하는 데 필요한 상태를 나타낸다. 장기 메모리는 목적이 다르다. 이 책에서는 메모리를 다음처럼 정의한다.

> **메모리는 현재 개별 실행을 넘어 미래 실행에서 재사용하기 위해 보존하는 정보다.**

예:

- 사용자가 선호하는 출력 형식
- 반복적으로 등장하는 저장소 규칙
- 이전 작업에서 얻은 유용한 교훈
- 자주 발생하는 Failure Pattern

반대로 다음은 메모리가 아니라 다른 상태에 더 가깝다.

~~~text
현재 Tool Retry Count
→ Run State

승인 대기 여부
→ Approval State

현재 수정 중인 File
→ Workspace State

이번 Goal의 완료 조건
→ Goal State
~~~

모든 정보를 메모리에 넣으면 각 정보를 언제 유지하고 갱신하거나 버려야 하는지 구분하기 어려워진다.

## Session과 Memory

세션은 대화의 연속성을 위한 것이다.

~~~text
Turn 1
Turn 2
Tool Result
User Correction
Turn 3
~~~

메모리는 세션을 넘어 재사용될 수 있다.

~~~text
Session A
  ↓ learned preference
Memory
  ↓ retrieved later
Session B
~~~

따라서:

~~~text
Session
≠ Memory
~~~

이다. 세션을 오래 보존한다고 자동으로 좋은 메모리가 되는 것도 아니다. 대화에는 일시적 가정과 잘못된 추측도 섞여 있다.

## Checkpoint와 Memory

체크포인트(Checkpoint: 실행을 이어가기 위한 상태 기록)는 현재 실행을 이어가기 위한 상태다.

예:

~~~text
Goal G-100
step: verify integration test
pending: create PR
~~~

메모리는 미래 작업에서 재사용하기 위한 것이다.

예:

~~~text
This repository requires integration tests
for auth module changes.
~~~

둘은 비슷해 보이지만 사용 목적이 다르다.

~~~text
Checkpoint
= Resume this execution

Memory
= Improve future execution
~~~

이 구분이 명확하면 Recovery State와 Learning State를 섞지 않을 수 있다.

## Memory가 유용한 경우

메모리는 다음 상황에서 가치가 있다.

### 반복되는 사용자 선호

~~~text
사용자는 결과를 Markdown 표보다 간단한 목록으로 선호한다.
~~~

### 반복되는 Repository Convention

~~~text
auth package 수정 시 integration test를 반드시 실행한다.
~~~

### 반복되는 Failure Lesson

~~~text
이 시스템에서는 package install 실패 시 proxy config를 먼저 확인한다.
~~~

### 반복되는 프로젝트 맥락

~~~text
이 프로젝트는 기본적으로 develop branch에서 작업한다.
~~~

다만 이런 사실은 외부에서 바뀔 수 있다. 메모리는 탐색의 출발점으로 쓸 수 있지만 실제 행동 전에는 현재 기준이 되는 원본을 다시 확인해야 한다.

## Memory가 필요하지 않은 경우

다음은 메모리보다 다른 작동 방식이 적합할 수 있다.

### 현재 Task Progress

상태 관리 계층.

### Canonical Configuration

Config Service / 저장소.

### 정책 문서

접근 대상 자원 / Knowledge Base.

### 대용량 Raw Log

Artifact Storage.

### 일회성 Observation

현재 컨텍스트(Context: 모델에 전달하는 정보) 또는 개별 실행 상태. 메모리를 만능 저장소로 만들지 않는다.

## Memory Scope

메모리는 누구에게 적용되는지 명확해야 한다.

예:

~~~text
User-private
Project
Repository
Team
Agent-specific
Organization
Global
~~~

가능하면 가장 좁은 적용 범위를 사용한다. 예를 들어 특정 저장소의 빌드 규칙을 Global Memory로 저장하면 다른 저장소에서 잘못 적용될 수 있다.

~~~text
repo-A rule
→ global memory
→ repo-B에 잘못 적용
~~~

적용 범위는 정확성과 보안 모두에 영향을 준다.

## Memory Freshness

메모리에는 시간이 지나도 유효한 정보와 빠르게 변하는 정보가 있다.

상대적으로 오래 유지되는 정보:

- 사용자의 문체 선호
- 저장소의 오래된 설계 원칙
- 반복되는 Troubleshooting Lesson

빠르게 변할 수 있는 정보:

- API Endpoint
- 현재 브랜치
- 운영 서버
- 권한 정책
- 가격
- 담당자

따라서 메모리의 부가 정보에 다음을 둘 수 있다.

~~~text
source
created_at
updated_at
scope
confidence
expires_at
refresh_before
~~~

모든 메모리에 TTL이 필요한 것은 아니다. 하지만 "언제 다시 확인해야 하는가"라는 질문은 필요하다.

## Memory는 Source of Truth가 아니다

메모리가 다음을 가지고 있다고 하자.

~~~text
Production host = prod-01
~~~

현재 Infrastructure Source는 다음이다.

~~~text
Production host = prod-02
~~~

External Action을 실행할 때 메모리를 우선하면 안 된다.

~~~text
Memory
→ candidate context / hint

Current Source
→ authority
~~~

메모리는 Discovery Cost를 줄일 수 있다. 하지만 External Reality를 고정하지 않는다.

## Retrieval은 단순 검색이 아니다

Memory System을 구현하면 흔히 Similarity Search부터 생각한다.

~~~text
query
→ vector search
→ top-k memories
~~~

하지만 운영 에이전트에서는 저장된 정보 검색 자체가 Policy Decision일 수 있다. 다음 질문이 필요하다.

- 현재 작업과 관련 있는가.
- 현재 User/Agent가 읽어도 되는 적용 범위인가.
- 정보 원본이 아직 유효한가.
- 더 최신 메모리나 외부 원본이 있는가.
- 서로 충돌하는 메모리가 있는가.
- Sensitive Information인가.

따라서:

~~~text
Memory Retrieval
≠ Blind Similarity Search
~~~

이다.

## Progressive Memory Retrieval

과거 실행을 모두 컨텍스트에 넣을 필요는 없다. Memory Summary와 Index를 먼저 제공하고 필요할 때 상세 기록을 조회하는 방식이 가능하다. 일부 Agent memory 구현에서도 이런 progressive retrieval 패턴을 사용한다.

개념적으로:

~~~text
Memory Summary
      ↓
Relevant Index
      ↓
Selected Detail
      ↓
Context
~~~

이 방식은 메모리 자체에도 Progressive Disclosure를 적용한다. Context Cost와 Stale Detail 노출을 줄일 수 있다.

## Contradictory Memory

메모리가 서로 충돌할 수 있다.

~~~text
Memory A:
run integration tests for auth changes

Memory B:
integration tests are disabled for auth module
~~~

어느 것이 최신인지 모른다면 단순 top-k retrieval로 해결되지 않는다.

필요한 정보:

- created_at
- source
- supersedes
- confidence
- validity scope

Memory Store도 버전과 Lineage를 가질 수 있다.

## Memory와 User Correction

사용자가 이전 메모리를 수정할 수 있어야 한다.

예:

~~~text
Memory:
사용자는 CSV 출력을 선호함

User:
이제부터 JSON으로 줘
~~~

새 메모리를 추가할 뿐 아니라 이전 메모리가 Superseded됐다는 관계를 남길 수 있다.

~~~text
mem-10
status: superseded
by: mem-22
~~~

이렇게 하면 충돌 해결이 쉬워진다.

## Memory가 항상 Agent Capability를 높이는 것은 아니다

메모리를 추가하면 과거 경험을 재사용할 수 있다. 동시에 새로운 위험이 생긴다.

- stale assumption
- poisoning
- privacy leakage
- cross-task contamination
- retrieval cost
- conflict resolution

그래서 메모리는 기본 구성 요소가 아니라 필요가 확인될 때 추가하는 편이 낫다.

~~~text
No Memory
→ observe repeated failure / repeated context cost
→ define memory purpose
→ add scoped memory
→ evaluate
~~~

하네스 구성 요소와 같은 방식으로 접근할 수 있다.

## 작은 예: Coding Agent의 Repository Memory

좋은 후보:

~~~text
scope: repository/app-a
memory:
auth module 변경 시
integration/auth 테스트를 실행해야 한다.

source:
repository instruction + repeated validation

freshness:
review on instruction change
~~~

나쁜 후보:

~~~text
scope: global
memory:
all Java projects require integration/auth tests
~~~

첫 번째는 적용 범위와 정보 원본이 명확하다. 두 번째는 과도하게 일반화됐다.

## Memory Read에도 Audit이 필요할 수 있다

민감한 메모리가 Agent Decision에 영향을 준다면 어떤 메모리가 읽혔는지 추적할 가치가 있다.

예:

~~~text
memory.retrieved
memory_id: mem-101
run_id: G-100
reason: repository_convention
~~~

이 기록을 남기면 나중에 잘못된 판단이 어떤 정보에서 비롯됐는지 분석하는 데 도움이 된다. 특히 메모리에 악성 정보를 심는 공격(Memory Poisoning) 사고에서 중요하다.

## 이 장에서 가져갈 것

메모리는 에이전트가 가진 모든 상태의 이름이 아니다. 이 책에서는 메모리를 미래 실행에서 재사용하기 위한 장기 보존 정보으로 좁힌다. 그래서 다음 경계를 유지한다.

~~~text
Session
≠ Checkpoint
≠ Memory
≠ Source of Truth
~~~

메모리를 추가할 때는 다음을 묻는다.

- 왜 저장하는가.
- 어느 적용 범위인가.
- 얼마나 오래 유효한가.
- 정보 원본은 무엇인가.
- 누가 읽을 수 있는가.
- 더 최신 정보 원본과 충돌하면 무엇을 우선할 것인가.

다음 장에서는 한 단계 더 위험한 질문으로 간다. 메모리를 읽는 것보다 먼저, **누가 어떤 정보를 장기 메모리에 쓸 수 있어야 하는가.** 메모리 기록을 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)로 다룬다.

## 주요 근거

- OpenAI Agents SDK Sessions
- OpenAI Sandbox Agent Memory
- research/topics/02-context-state-memory.md
- research/topics/09-state-memory-taxonomy.md
