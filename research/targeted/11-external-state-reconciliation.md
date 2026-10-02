# Targeted Research — External State Reconciliation

기준일: 2026-10-02
대상: 11장 External State Reconciliation

## 새로 확보한 근거

### Selective Revalidation for Long-running AI Agents
- Source: https://arxiv.org/abs/2609.08015
- 핵심 구분:
  - Version Conflict: 읽었던 state의 version이 바뀜
  - Decision Conflict: 그 변화가 pending action의 정당성을 깨뜨림
- 제안 방식:
  - pending action을 정당화하는 executable condition을 기록
  - 변경된 state와 관련 있는 condition만 재검증
  - 결과에 따라 retain / refresh metadata / re-plan / block
  - 최종 commit은 target-side compare-and-set 또는 transaction으로 묶음
- 의미:
  - 단순 version mismatch마다 전체 task를 재시작할 필요는 없음
  - 중요한 것은 "변경됐는가"보다 "변경이 의사결정을 무효화했는가"

### Task-State Horizon
- Source: https://arxiv.org/abs/2608.08036
- 핵심:
  - long-horizon difficulty를 action count만으로 설명하지 않고 task-relevant state transition span으로 측정
  - unexpected failure와 intervention까지 state dependency에 포함
- 의미:
  - Long-running Agent 품질을 state tracking/reconciliation capability로 별도 평가할 근거

### AgentRewind
- Source: https://arxiv.org/abs/2608.14380
- 핵심:
  - Agent context와 controlled environment checkpoint를 정렬해 recovery
  - long-horizon engineering task에서 partial progress와 completion을 함께 측정
- 의미:
  - State Plane과 environment recovery가 분리되지 않고 함께 다뤄질 수 있는 사례

## 11장에 반영할 수정

기존:
~~~text
Refresh
→ Compare
→ Reconcile
→ Re-plan
~~~

보강:
~~~text
Detect Version Change
       ↓
Identify Affected Decision Conditions
       ↓
Selective Revalidation
       ├─ Still Valid → Continue
       ├─ Metadata Only → Refresh Projection
       ├─ Invalidated → Re-plan
       └─ Unsafe / Duplicate → Block
       ↓
Atomic / CAS Commit
~~~

## 새 핵심 원칙

1. 모든 version change가 decision conflict는 아니다.
2. Reconciliation은 whole-state refresh보다 selective revalidation으로 최적화할 수 있다.
3. Pending action에는 justification condition을 남길 가치가 있다.
4. Commit 직전 authoritative state와 bind하는 CAS/transaction이 중요하다.
5. Long-horizon difficulty는 action horizon뿐 아니라 task-state horizon으로도 본다.

## 장에서 주의할 점

Selective Revalidation 연구 결과를 production generality로 과장하지 않는다. controlled feasibility와 architecture pattern 근거로 사용한다.
