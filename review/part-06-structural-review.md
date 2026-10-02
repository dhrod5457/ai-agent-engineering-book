# Part VI Structural Review

기준일: 2026-10-02
대상:
- chapters/18/draft.md
- chapters/19/draft.md
- chapters/20/draft.md
- chapters/21/draft.md

## Part VI의 역할

Part VI는 Agent Improvement Loop를 완성한다.

~~~text
18장
무슨 일이 일어났는가?
        ↓
19장
얼마나 잘했는가?
        ↓
20장
같은 실패를 어떻게 회귀 시험으로 막는가?
        ↓
21장
Harness 변화의 실제 기여도를 어떻게 측정하는가?
~~~

## 18장 검토

핵심 역할:
- Trace 정의
- Model / Tool / State / Policy / Runtime Event
- Correlation / Causation
- Audit vs Debug
- Trace → Eval

좋은 점:
- private reasoning 저장과 structured trace를 구분한다.
- Agent State Plane의 Event History와 Observability Trace가 연결된다.
- Failure 원인을 Layer별로 분리한다.

주의:
- Trace에 민감 Context 전체를 저장하는 것을 권장하지 않는다.
- Event History와 Trace가 같은 저장소여야 한다는 의미로 읽히지 않게 한다.

결론: PASS.

## 19장 검토

핵심 역할:
- Output / Trajectory / Outcome
- Deterministic / Model / Human Grader
- Security / State Handling
- Repeated Reliability
- Infrastructure Noise
- Benchmark Versioning

좋은 점:
- Agent score를 Model score로 축약하지 않는다.
- Partial Checkpoint를 진단용으로만 사용하고 Product Completion과 분리한다.

주의:
- pass@k / pass^k 설명은 구현에 따라 정의를 재확인하고 출간 직전 검증한다.
- Vendor benchmark 수치는 본문 장식으로 추가하지 않는다.

결론: PASS.

## 20장 검토

핵심 역할:
- Production Failure → Regression
- PR / Nightly / Release / Shadow / Canary
- AgentVersion
- Promotion Rule
- Dataset Drift

좋은 점:
- Eval이 별도 연구 행사가 아니라 CI/CD와 연결된다.
- Model Upgrade와 Harness Audit을 연결한다.

주의:
- 기존 Software Factory 책의 CI/CD/Delivery 설명을 반복하지 않는다.
- 여기서는 Agent-level behavioral regression에 집중한다.

결론: PASS.

## 21장 검토

핵심 역할:
- Harness Component = Hypothesis
- Minimal Baseline
- Repeated Ablation
- Variance
- Capability / Safety / Cost Slice
- Harness Debt

좋은 점:
- targeted research의 repeated trials와 run-to-run variance를 반영했다.
- 복잡한 Harness를 성숙도로 보지 않는다.
- Part I 3장의 preview를 실제 운영 방법으로 확장한다.

주의:
- 작은 실험 차이를 일반화하지 않는다.
- 통계적 방법론 전체로 확장하지 않는다.

결론: PASS.

## 장 간 중복

### 18장 ↔ 8장
Event가 양쪽에 등장한다.

8장:
- durable execution state

18장:
- observability / diagnosis

같은 Event를 공유할 수 있지만 목적이 다르다.

### 19장 ↔ 20장
Eval 개념과 Eval 운영이 연결된다.

19장:
- 무엇을 측정할 것인가

20장:
- 언제 어떤 cadence로 측정하고 promotion에 연결할 것인가

경계 유지됨.

### 3장 ↔ 21장
3장은 Harness Engineering의 원칙과 preview.
21장은 repeated ablation과 Debt 운영.

중복 허용 범위.

## Part VI 핵심 흐름

~~~text
Trace
→ Failure Classification
→ Eval
→ Regression Dataset
→ Candidate Change
→ Harness Ablation
→ Promotion
~~~

Improvement Loop가 닫힌다.

## 분량

현재 문자 수:
- 18장 약 5.2k
- 19장 약 5.4k
- 20장 약 5.3k
- 21장 약 5.6k

Part III~V보다 짧지만 각 장의 범위가 집중돼 있어 Structural Gap은 없다.

## Structural Review 결론

PASS.

Part VI Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part VII 22~25장 Draft
2. Epilogue Draft
3. Part VII Structural Review
4. 전체 Manuscript Structural Review
