# Part III Structural Review

기준일: 2026-10-02
대상:
- chapters/07/draft.md
- chapters/08/draft.md
- chapters/09/draft.md
- chapters/10/draft.md
- chapters/11/draft.md

## Part III의 역할

Part III는 책의 중심부다.

질문 흐름은 다음과 같다.

~~~text
7장
어떤 State를 서로 분리해야 하는가?
        ↓
8장
그 State를 어떤 실행 계층에서 유지할 것인가?
        ↓
9장
실패 후 어떻게 안전하게 이어갈 것인가?
        ↓
10장
시간이 길어지면 어떤 새로운 실패가 생기는가?
        ↓
11장
변화하는 External State와 어떻게 다시 맞출 것인가?
~~~

## 7장 검토

핵심 역할:
- Context / Session / Run / Workspace / Goal / Artifact / Memory / Source of Truth 분리
- 각 State의 lifetime과 authority를 다르게 보기
- State Promotion과 Freshness

좋은 점:
- Memory를 과도한 상위 개념으로 사용하지 않는다.
- 8장 State Plane 필요성이 자연스럽게 도출된다.
- Part IV Memory 상세와 경계가 유지된다.

주의:
- Memory security/poisoning은 13장으로 남긴다.
- State taxonomy가 공식 표준처럼 읽히지 않도록 synthesis임을 유지한다.

결론: PASS.

## 8장 검토

핵심 역할:
- Agent State Plane 정의
- Event History
- Projection
- Goal / Progress
- Artifact / Approval / Source Version / Memory Reference
- Runtime/Harness/Factory Control Plane 경계

이 장은 책 전체의 기준 장이다.

좋은 점:
- "하나의 DB"가 아니라 responsibility layer로 정의했다.
- Context = Projection이라는 Part II 메시지와 연결된다.
- Factory Control Plane과 경계를 명시했다.

주의:
- Event Sourcing을 필수 구현으로 읽히지 않게 현재 경고를 유지한다.
- State Plane이라는 표현이 저자의 synthesis임을 계속 표시한다.
- 향후 장에서 State Plane 전체 정의를 반복하지 않고 필요한 부분만 참조한다.

결론: PASS.

## 9장 검토

핵심 역할:
- Retry ≠ Recovery
- Replay ≠ Re-run
- UNKNOWN execution state
- Idempotency
- Pause / Resume
- Snapshot / Schema versioning

좋은 점:
- 8장의 State 구조를 실제 Failure Recovery에 적용한다.
- duplicate side effect 문제가 구체적이다.

주의:
- Exactly-once를 보장할 수 있다는 인상을 주지 않는다.
- Temporal을 Agent 구현 표준처럼 표현하지 않는다.

결론: PASS.

## 10장 검토

핵심 역할:
- Long Context ≠ Long-running Execution
- Milestone / Working State
- Hidden State / Multi-item State
- Phase Budget / Verification Reserve
- Dynamic Environment

좋은 점:
- 9장의 crash recovery와 다른 문제를 다룬다.
- long-running을 단순 context window 문제로 축약하지 않는다.
- 11장 Reconciliation으로 연결된다.

주의:
- 예시 Phase Budget 비율은 표준 수치가 아니며 설명용임을 유지한다.
- Task-State Horizon은 emerging research임을 명시한 현재 표현을 유지한다.

결론: PASS.

## 11장 검토

핵심 역할:
- Working State = Snapshot
- Refresh ≠ Reconciliation
- Version Conflict ≠ Decision Conflict
- Selective Revalidation
- Authority Ranking
- CAS / optimistic concurrency
- Final Verification

좋은 점:
- targeted research가 기존 synthesis를 보강했다.
- 단순 "항상 다시 읽어라"가 아니라 selective revalidation으로 발전했다.
- State Plane의 Source Version이 실제 활용된다.

주의:
- Selective Revalidation 연구는 최근 연구이므로 일반적인 production standard처럼 단정하지 않는다.
- CAS/transaction이 모든 외부 시스템에 가능하다고 가정하지 않는다.

결론: PASS.

## 장 간 중복

### 7장 ↔ 8장
7장은 taxonomy, 8장은 durable execution layer다.

역할이 분명하다.

### 8장 ↔ 9장
8장은 State Plane의 구조, 9장은 recovery mechanics다.

Event History가 양쪽에 등장하지만 필요 중복이다.

### 9장 ↔ 11장
9장은 crash/duplicate side effect recovery.
11장은 external state freshness/conflict.

UNKNOWN external operation 조회와 source refresh가 일부 닮았지만 failure trigger가 다르다.

### 10장 ↔ 11장
10장은 dynamic environment를 문제로 제시.
11장은 이를 해결하는 reconciliation mechanics.

구조상 적절하다.

## Part III 핵심 경계

다음 식들이 유지된다.

~~~text
Context ≠ Durable State
Session ≠ Goal
Workspace ≠ Checkpoint
Memory ≠ Source of Truth
Replay ≠ Side-effect Re-execution
Version Conflict ≠ Decision Conflict
Agent State Plane ≠ Factory Control Plane
~~~

## 분량

현재 문자 수:
- 7장 약 7.2k
- 8장 약 8.0k
- 9장 약 6.0k
- 10장 약 6.0k
- 11장 약 7.6k

8장이 Part의 중심 장으로 가장 긴 편이며 구조상 적절하다.

9~10장은 Line Review 또는 사례 보강 과정에서 0.5~1.0k 정도 늘어날 여지가 있지만 Structural Gap은 없다.

## Structural Review 결론

PASS.

Part III Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part IV 12~13장 Draft
2. Memory와 State Plane 중복 최소화
3. Memory Write Security를 core message로 강화
4. Part IV Structural Review
