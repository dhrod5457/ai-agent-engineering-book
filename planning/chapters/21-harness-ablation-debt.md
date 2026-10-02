# 21장. Harness Ablation과 Debt

## Goal
독자가 Harness의 각 component가 실제로 필요한지 반복 실험으로 측정하고 오래된 scaffold를 제거할 수 있게 한다.

## Core Claims
- Harness component는 engineering hypothesis다.
- component는 known failure와 regression case에 연결돼야 한다.
- 한 번의 on/off 결과보다 repeated trial과 variance가 중요하다.
- component 효과는 capability/task/model에 따라 달라질 수 있다.
- Model upgrade는 old scaffold assumption을 깨뜨릴 수 있다.
- Harness에도 dead code와 debt가 누적된다.

## Reader Questions
- Planner를 넣으면 정말 더 좋아지는가?
- memory/evaluator/subagent의 효과를 어떻게 분리하는가?
- run-to-run variance가 크면 어떻게 판단하는가?
- 새 모델이 나오면 Harness를 어떻게 다시 검증하는가?

## Flow
1. scaffold accumulation
2. failure hypothesis
3. minimal baseline
4. component inventory
5. pin model/tools/runtime/eval
6. repeated baseline
7. one-at-a-time ablation
8. capability/security/cost slices
9. variance와 interaction effects
10. model upgrade audit
11. Harness Debt removal

## Example / Figure
- Planner on/off, Evaluator on/off 반복 실험 matrix
- Figure: Hypothesis → Baseline → Ablation → Repeated Eval → Keep / Remove / Redesign
- Harness Component Record 예시

## Evidence
- research/topics/22-harness-ablation-and-minimalism.md
- research/targeted/21-harness-ablation.md
- Anthropic Harness Design
- Anthropic Managed Agents
- Automated Alignment Researchers harness ablation
- AuditBench

## Avoid
- 한 번의 benchmark 결과 일반화
- 작은 delta를 variance 없이 해석
- 복잡한 Harness 자체를 성숙도 지표로 사용

## Draft Exit Criteria
- ablation procedure가 reproducible하다.
- repeated trials와 variance가 포함된다.
- Harness Component Record와 Debt checklist가 있다.
