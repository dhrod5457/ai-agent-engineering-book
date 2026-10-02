# 10장. Long-running Agent

짧은 Task에서는 Agent가 꽤 유능해 보인다.

파일 하나를 고친다. 테스트 하나를 실행한다. 문서 한 장을 만든다.

작업이 한 시간을 넘어가면 다른 문제가 나타난다.

Agent가 무엇을 하려 했는지 잊는다. 이미 확인한 항목을 다시 확인한다. 일부 Item만 처리하고 전체가 끝났다고 판단한다. Search와 준비 작업에 시간을 너무 많이 써 핵심 업무를 시작하지 못한다. 작업 도중 외부 상태가 바뀌었는데 처음 만든 Plan을 계속 따른다.

Long-running Agent의 문제는 단순히 더 오래 reasoning하는 문제가 아니다.

**시간이 길어질수록 상태와 목표를 잃지 않는 문제**다.

## Context Window가 크면 해결되는가

Context Window가 커지면 도움이 된다.

더 많은 History와 Artifact를 볼 수 있다.

하지만 다음 문제는 남는다.

- 오래된 State가 계속 남는다.
- External World가 바뀐다.
- 많은 Item을 누락 없이 추적해야 한다.
- 이미 완료한 Action과 Pending Action을 구분해야 한다.
- Context가 커져도 중요한 정보의 우선순위가 자동으로 생기지는 않는다.

따라서:

~~~text
Long Context
≠ Long-running Execution
~~~

이다.

## Long-running Task의 특징

장기 Task는 단순히 Step 수가 많다는 것 이상이다.

예를 들어 대학 행정 Agent가 여러 학생의 장학 심사 보조를 한다고 하자.

각 학생마다 다음 State가 다를 수 있다.

~~~text
Student A
- document complete
- advisor approval pending

Student B
- document missing

Student C
- approval complete
- final notification pending
~~~

Agent는 여러 Item의 State를 동시에 유지해야 한다.

중간에 새로운 문서가 들어올 수도 있다.

이런 문제는 단일 대화 Memory만으로 안정적으로 관리하기 어렵다.

## OSWorld 2.0에서 드러나는 문제

2026년 OSWorld 2.0은 기존 Desktop Agent Benchmark보다 훨씬 긴 Workflow를 포함한다.

사람이 수행해도 상당한 시간이 필요한 Task가 포함돼 있고, 많은 Tool/Action이 이어진다.

이 환경에서 중요한 Challenge로 다음이 드러난다.

- Implicit-state Inference
- Multi-item State Tracking
- Conflict Disambiguation
- Dynamic Environment
- Cross-source Reasoning

Agent Engineering 관점에서 보면 GUI Click Accuracy보다 State Management 문제가 전면에 나온다.

## Milestone

Long-running Goal을 하나의 자유로운 Loop로만 처리하면 Progress 판단이 어려워진다.

Milestone을 둘 수 있다.

예:

~~~text
Goal:
지원자 50명의 제출 자료를 확인하고 누락자를 정리

Milestone 1:
source 목록 확보

Milestone 2:
50명 state table 생성

Milestone 3:
각 지원자 검증

Milestone 4:
누락 목록 재검증

Milestone 5:
final artifact 생성
~~~

Milestone은 rigid planner가 모든 Step을 미리 정한다는 뜻이 아니다.

Completion Surface를 나눈다는 의미다.

## Working State Table

Multi-item Task에서는 자연어 Summary보다 구조화된 Working State가 유용하다.

예:

~~~text
id | status | source_version | blocker | verified
A  | ready  | 12             | -       | true
B  | wait   | 8              | doc     | false
C  | done   | 15             | -       | true
~~~

이 Table은 Context에 전부 넣을 필요가 없다.

State Plane에 두고 필요한 Slice만 Projection할 수 있다.

이 구조가 누락을 줄이는 데 도움이 된다.

## Hidden State

Long-running Task의 어려움 중 하나는 Task Instruction에 모든 정보가 없다는 것이다.

Agent는 다음을 찾아야 할 수 있다.

- 이전 승인
- 과거 Submission
- 다른 App의 Record
- 저장된 Draft
- 최신 Message

즉 Goal을 이해하려면 Environment 안의 Hidden State를 복구해야 한다.

이때 "사용자가 말한 것만 따르면 된다"는 접근으로는 부족하다.

Agent는 Source Registry와 Discovery Strategy가 필요할 수 있다.

## Phase Budget

장기 Agent는 준비 작업에 Horizon을 소진할 수 있다.

예를 들어 환불 처리 Task인데 Agent가:

- 관련 정책 검색
- 브라우저 설정
- 도움말 탐색
- 툴 사용법 조사

에 대부분의 Step을 쓰고 환불 시스템에는 늦게 접근할 수 있다.

이를 막기 위해 Phase Budget을 둘 수 있다.

~~~text
Discovery
→ 필요한 범위에서 제한

Execution
→ 핵심 작업에 충분한 budget 확보

Verification
→ 마지막까지 별도 reserve 유지
~~~

구체적인 비율은 Task와 비용 구조에 따라 달라진다. 핵심은 전체 Budget만 두지 말고 탐색, 실행, 검증이 서로의 자원을 소진하지 않게 관리하는 것이다.

## Verification Reserve

Agent가 마지막 Step까지 구현에만 사용하면 검증할 Budget이 없다.

그래서 Verification을 마지막에 "남으면 하는 일"로 두지 않는다.

~~~text
Total Budget
  ├─ Discovery
  ├─ Execution
  └─ Verification Reserve
~~~

특히 High-impact Task에서는 Verification Budget을 별도 확보하는 것이 유용하다.

## Premature Completion

Long-running Agent는 일부 Item이 끝났는데 전체 Goal이 끝났다고 판단할 수 있다.

예:

~~~text
50개 중 47개 처리
→ output file generated
→ "완료"
~~~

이 실패를 막으려면 Completion Condition이 Item Coverage와 연결돼야 한다.

~~~text
expected_items = 50
verified_items = 50
unresolved_items = 0
~~~

가능하면 Model의 감각보다 deterministic invariant를 사용한다.

## Progress Artifact

Session이 바뀌어도 다음 Agent가 이어받을 수 있는 Artifact를 남기는 패턴이 유용하다.

예:

- progress.json
- task checklist
- verified item table
- current plan
- test report

Anthropic의 Long-running Harness 사례에서도 Session 간 Continuity를 위해 incremental progress와 external artifact를 남기는 패턴이 사용됐다.

핵심은 형식이 아니라 **작업 상태를 Model Context 밖에도 남긴다는 점**이다.

## Clarification은 실패가 아니다

Autonomous Agent를 만들다 보면 질문하지 않는 Agent가 더 좋은 것처럼 보일 수 있다.

하지만 장기 업무에서는 불확실한 값을 추정하는 것이 더 위험할 수 있다.

예:

~~~text
배송 주소가 두 개 있음
최신 승인자가 불명확함
정책 문서 두 개가 충돌함
~~~

이때 올바른 Action은 사용자에게 질문하거나 Block하는 것일 수 있다.

~~~text
Autonomy
=
Act when justified
+
Stop when not justified
~~~

라고 보는 편이 낫다.

## Dynamic Environment

가장 중요한 문제 중 하나다.

Agent가 T0에 Source를 읽었다.

작업 중 T1에 새로운 Message가 도착했다.

초기 Plan은 더 이상 유효하지 않을 수 있다.

~~~text
T0
Read Source
→ Build Plan

T1
Source Changes

T2
Execute Old Plan
~~~

Long-running Agent가 실패하는 전형적인 패턴이다.

그래서 특정 Event나 Milestone에서 Source를 Refresh해야 한다.

이것이 다음 장의 External State Reconciliation이다.

## State Horizon

장기 Task 난이도를 단순 Action Count로만 볼 필요는 없다.

Task에서 중요한 State가 얼마나 오래 유지돼야 하고, 얼마나 많은 Transition을 거쳐 마지막 Decision까지 영향을 주는가도 중요하다.

2026년 공개된 preprint에서는 이런 관점을 Task-State Horizon으로 정의하고 별도 benchmark로 측정하려는 시도가 있다.

아직 일반적인 표준 Metric은 아니다.

하지만 "Step이 많다"보다 "오래된 State Dependency를 얼마나 오래 정확히 유지해야 하는가"를 보는 관점은 Agent 설계에 유용하다.

## 작은 예: 50개 요청 처리

Goal:

> 50개의 요청을 검토하고 승인 가능한 요청만 처리하라.

나쁜 구조:

~~~text
Conversation
→ 요청 하나씩 처리
→ Summary
→ 계속
~~~

문제:

- 몇 개 처리했는지 불명확
- 중복 처리 가능
- Source Update 누락
- Pending/Blocked Item 누락

더 나은 구조:

~~~text
Goal
 ↓
Item Registry
 ↓
Per-item State
 ↓
Milestone
 ↓
Action
 ↓
Verification
 ↓
Refresh Trigger
 ↓
Completion Invariant
~~~

이렇게 하면 Long-running Execution을 대화 지속 문제가 아니라 State Management 문제로 다룰 수 있다.

## 이 장에서 가져갈 것

Long-running Agent의 핵심은 Context Window를 크게 만드는 것이 아니다.

> **시간이 지나고 Environment가 변해도 Goal, Progress, Item State, Verification 기준을 잃지 않는 것**이다.

이를 위해:

- Milestone
- Working State
- Progress Artifact
- Phase Budget
- Verification Reserve
- Clarification
- Refresh Trigger

가 필요할 수 있다.

다음 장에서는 이 중 가장 중요한 Dynamic Environment 문제를 좁혀본다.

Agent가 과거 Snapshot을 기준으로 만든 Decision을 External Source가 바뀐 뒤에도 계속 실행해도 되는가.

External State Reconciliation을 다룬다.

## 주요 근거

- Anthropic, Effective Harnesses for Long-running Agents
- Anthropic, Harness Design for Long-running Application Development
- OSWorld 2.0
- Task-State Horizon research
- research/topics/04-harness-long-running.md
- research/topics/13-long-horizon-computer-use.md
