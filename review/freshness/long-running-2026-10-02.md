# Long-running Agent Research Freshness Audit

기준일: 2026-10-02

대상:
- chapters/10/draft.md
- chapters/11/draft.md

## OSWorld 2.0

Source:
https://arxiv.org/abs/2606.29537

상태:
- 2026-06 공개 preprint
- long-horizon real-world computer-use benchmark
- dynamic environment, implicit-state inference, cross-source reasoning 등을 challenge로 포함

본문에서는 특정 성능 수치를 핵심 주장으로 사용하지 않고, long-running state management 문제의 사례 근거로만 사용한다.

## Selective Revalidation

Source:
https://arxiv.org/abs/2609.08015

상태:
- 2026-09 공개 preprint

핵심:
- version conflict와 decision conflict 구분
- pending action의 justification condition을 선택적으로 재검증
- target-side transaction / compare-and-set과 결합 가능

주의:
논문 자체가 controlled feasibility를 보였을 뿐 production generality나 condition 자동 추출을 입증한 것은 아니라고 명시한다.

## Task-State Horizon

Source:
https://arxiv.org/abs/2608.08036

상태:
- 2026-08 공개 preprint

핵심:
- action sequence length와 별도로 task-relevant state transition span을 평가 축으로 제안

주의:
업계 표준 Metric으로 표현하지 않는다.

## AgentRewind

Source:
https://arxiv.org/abs/2608.14380

상태:
- 2026-08 공개 preprint

핵심:
- agent context와 controlled environment checkpoint를 정렬해 recovery
- long-horizon engineering assignment에서 completion과 partial progress 평가

본문에서는 Agent State Plane의 필수 구현 근거가 아니라 recovery architecture 사례로만 사용한다.

## 출간 전 재검증

- 논문 후속 peer review / version
- benchmark revision
- 공개 implementation 상태
- 용어가 업계 표준으로 정착했는지 여부
