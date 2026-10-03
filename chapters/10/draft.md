# 10장. Long-running Agent

짧은 작업에서는 에이전트가 꽤 유능해 보인다. 파일 하나를 고친다. 테스트 하나를 실행한다. 문서 한 장을 만든다. 작업이 한 시간을 넘어가면 다른 문제가 나타난다. 에이전트가 무엇을 하려 했는지 잊는다. 이미 확인한 항목을 다시 확인한다. 일부 항목만 처리하고 전체가 끝났다고 판단한다. 검색과 준비 작업에 시간을 너무 많이 써 핵심 업무를 시작하지 못한다. 작업 도중 외부 상태가 바뀌었는데 처음 만든 계획을 계속 따른다. 오래 실행되는 에이전트를 만들려면 단순히 더 오래 추론하게 하는 것만으로는 부족하다. **시간이 길어져도 상태와 목표를 잃지 않아야 한다.**

## Context Window가 크면 해결되는가

컨텍스트 윈도(Context Window: 모델이 한 번에 입력받을 수 있는 정보의 범위)가 커지면 도움이 된다. 더 많은 이력과 산출물을 볼 수 있다. 하지만 다음 문제는 남는다.

- 오래된 상태가 계속 남는다.
- 외부 환경이 바뀐다.
- 많은 항목을 누락 없이 추적해야 한다.
- 이미 완료한 행동과 대기 중인 행동을 구분해야 한다.
- 컨텍스트(Context: 모델에 전달하는 정보)가 커져도 중요한 정보의 우선순위가 자동으로 생기지는 않는다.

따라서:

~~~text
Long Context
≠ Long-running Execution
~~~

이다.

## Long-running Task의 특징

장기 작업은 단순히 단계 수가 많다는 것 이상이다. 예를 들어 대학 행정 에이전트가 여러 학생의 장학 심사 보조를 한다고 하자. 각 학생마다 다음 상태가 다를 수 있다.

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

에이전트는 여러 항목의 상태를 동시에 유지해야 한다. 중간에 새로운 문서가 들어올 수도 있다. 이런 문제는 단일 대화 메모리만으로 안정적으로 관리하기 어렵다.

## OSWorld 2.0에서 드러나는 문제

2026년 OSWorld 2.0은 기존 Desktop Agent Benchmark보다 훨씬 긴 작업 흐름을 포함한다. 사람이 수행해도 상당한 시간이 필요한 작업이 포함돼 있고, 많은 Tool/Action이 이어진다. 이 환경에서 중요한 어려움으로 다음이 드러난다.

- Implicit-state Inference
- Multi-item State Tracking
- Conflict Disambiguation
- 변화하는 환경
- Cross-source Reasoning

에이전트 엔지니어링 관점에서 보면 GUI Click Accuracy보다 상태 관리 문제가 전면에 나온다.

## Milestone

Long-running Goal을 하나의 자유로운 반복 실행으로만 처리하면 진행 상황 판단이 어려워진다. 중간 완료 지점을 둘 수 있다.

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

중간 완료 지점을 둔다고 해서 고정된 계획기가 모든 단계를 미리 정한다는 뜻은 아니다. 어디까지 완료했는지 확인할 범위를 나눈다는 의미다.

## Working State Table

Multi-item Task에서는 자연어 요약보다 구조화된 작업 상태(Working State: 작업 중 관리하는 상태)가 유용하다.

예:

~~~text
id | status | source_version | blocker | verified
A  | ready  | 12             | -       | true
B  | wait   | 8              | doc     | false
C  | done   | 15             | -       | true
~~~

이 Table은 컨텍스트에 전부 넣을 필요가 없다. 상태 관리 계층에 두고 필요한 Slice만 필요한 정보를 골라 구성할 수 있다. 이 구조가 누락을 줄이는 데 도움이 된다.

## Hidden State

장시간 작업의 어려움 중 하나는 작업 지침에 모든 정보가 없다는 것이다. 에이전트는 다음을 찾아야 할 수 있다.

- 이전 승인
- 과거 Submission
- 다른 App의 기록
- 저장된 Draft
- 최신 메시지

즉 목표를 이해하려면 환경 안의 겉으로 드러나지 않은 상태를 복구해야 한다. 이때 "사용자가 말한 것만 따르면 된다"는 접근으로는 부족하다. 에이전트는 정보 원본 목록과 정보 탐색 전략이 필요할 수 있다.

## Phase Budget

장기 에이전트는 준비 작업에 Horizon을 소진할 수 있다.

예를 들어 환불 처리 작업인데 에이전트가:

- 관련 정책 검색
- 브라우저 설정
- 도움말 탐색
- 툴 사용법 조사

에 대부분의 단계를 쓰고 환불 시스템에는 늦게 접근할 수 있다. 이를 막기 위해 단계별 실행 한도를 둘 수 있다.

~~~text
Discovery
→ 필요한 범위에서 제한

Execution
→ 핵심 작업에 충분한 budget 확보

Verification
→ 마지막까지 별도 reserve 유지
~~~

구체적인 비율은 작업과 비용 구조에 따라 달라진다. 핵심은 전체 실행 한도만 두지 말고 탐색, 실행, 검증이 서로의 자원을 소진하지 않게 관리하는 것이다.

## Verification Reserve

에이전트가 마지막 단계까지 구현에만 사용하면 검증할 실행 한도가 없다. 그래서 검증을 마지막에 "남으면 하는 일"로 두지 않는다.

~~~text
Total Budget
  ├─ Discovery
  ├─ Execution
  └─ Verification Reserve
~~~

특히 영향이 큰 작업에서는 검증에 쓸 시간과 비용을 별도로 확보하는 것이 유용하다.

## Premature Completion

오래 실행되는 에이전트는 일부 항목이 끝났는데 전체 목표가 끝났다고 판단할 수 있다.

예:

~~~text
50개 중 47개 처리
→ output file generated
→ "완료"
~~~

이 실패를 막으려면 완료 조건이 항목을 빠짐없이 처리했는지 여부와 연결돼야 한다.

~~~text
expected_items = 50
verified_items = 50
unresolved_items = 0
~~~

가능하면 모델의 감각보다 시스템이 정해진 규칙으로 확인할 수 있는 불변 조건을 사용한다.

## Progress Artifact

세션이 바뀌어도 다음 에이전트가 이어받을 수 있는 산출물을 남기는 패턴이 유용하다.

예:

- progress.json
- task checklist
- verified item table
- current plan
- test report

Anthropic의 장시간 작업용 하네스 사례에서도 세션 사이에 작업을 이어가기 위해 조금씩 이룬 진행 상황과 외부 산출물을 남기는 방식을 사용했다. 핵심은 형식이 아니라 **작업 상태를 모델의 컨텍스트 밖에도 남긴다는 점**이다.

## Clarification은 실패가 아니다

Autonomous Agent를 만들다 보면 질문하지 않는 에이전트가 더 좋은 것처럼 보일 수 있다. 하지만 장기 업무에서는 불확실한 값을 추정하는 것이 더 위험할 수 있다.

예:

~~~text
배송 주소가 두 개 있음
최신 승인자가 불명확함
정책 문서 두 개가 충돌함
~~~

이때 올바른 행동은 사용자에게 질문하거나 Block하는 것일 수 있다.

~~~text
Autonomy
=
Act when justified
+
Stop when not justified
~~~

라고 보는 편이 낫다.

## Dynamic Environment

가장 중요한 문제 중 하나다. 에이전트가 T0에 정보 원본을 읽었다. 작업 중 T1에 새로운 메시지가 도착했다. 초기 계획은 더 이상 유효하지 않을 수 있다.

~~~text
T0
Read Source
→ Build Plan

T1
Source Changes

T2
Execute Old Plan
~~~

오래 실행되는 에이전트가 실패하는 전형적인 패턴이다. 그래서 특정 이벤트나 중간 완료 지점에서 정보 원본을 최신 정보 다시 읽기해야 한다. 이것이 다음 장의 외부 상태와 내부 판단의 재조정이다.

## State Horizon

장기 작업 난이도를 단순 Action Count로만 볼 필요는 없다. 작업에서 중요한 상태가 얼마나 오래 유지돼야 하고, 얼마나 많은 상태 전환을 거쳐 마지막 판단까지 영향을 주는가도 중요하다. 2026년 공개된 preprint에서는 이런 관점을 Task-State Horizon으로 정의하고 별도 benchmark로 측정하려는 시도가 있다. 아직 일반적인 표준 측정 지표는 아니다. 하지만 "단계가 많다"보다 "오래된 상태 사이의 의존 관계를 얼마나 오래 정확히 유지해야 하는가"를 보는 관점은 에이전트 설계에 유용하다.

## 작은 예: 50개 요청 처리

목표:

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
- Pending/Blocked 항목 누락

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

이렇게 하면 장시간 실행을 대화 지속 문제가 아니라 상태 관리 문제로 다룰 수 있다.

## 이 장에서 가져갈 것

오래 실행되는 에이전트의 핵심은 컨텍스트 윈도를 크게 만드는 것이 아니다.

> **시간이 지나고 환경이 변해도 목표, 진행 상황, 항목별 상태, 검증 기준을 잃지 않는 것**이다.

이를 위해:

- 중간 완료 지점
- 작업 상태
- Progress Artifact
- 단계별 실행 한도
- Verification Reserve
- Clarification
- Refresh Trigger

가 필요할 수 있다. 다음 장에서는 이 중 가장 중요한 변화하는 환경 문제를 좁혀본다. 에이전트가 과거 상태 사본(Snapshot: 특정 시점의 상태 사본)을 기준으로 만든 판단을 외부 원본이 바뀐 뒤에도 계속 실행해도 되는가. 외부 상태와 내부 판단의 재조정을 다룬다.

## 주요 근거

- Anthropic, Effective Harnesses for Long-running Agents
- Anthropic, Harness Design for Long-running Application Development
- OSWorld 2.0
- Task-State Horizon research
- research/topics/04-harness-Long-running.md
- research/topics/13-long-horizon-computer-use.md
