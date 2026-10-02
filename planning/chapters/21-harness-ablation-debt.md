# 21장. Harness Ablation과 Debt

## Goal
독자가 Harness의 각 component가 실제로 필요한지 측정하고 오래된 scaffold를 제거할 수 있게 한다.

## Core Claims
- Harness component는 engineering hypothesis다.
- component는 known failure와 regression case에 연결돼야 한다.
- Model upgrade는 old scaffold assumption을 깨뜨릴 수 있다.
- Harness에도 dead code와 debt가 누적된다.

## Reader Questions
- Planner를 넣으면 정말 더 좋아지는가?
- memory/evaluator/subagent의 효과를 어떻게 분리하는가?
- 새 모델이 나오면 Harness를 어떻게 다시 검증하는가?

## Flow
1. scaffold accumulation
2. minimal baseline
3. component inventory
4. one-at-a-time ablation
5. capability/security slices
6. interaction effects
7. model upgrade audit
8. Harness Debt removal

## Example / Figure
- Planner on/off, Evaluator on/off 비교 matrix
- Figure: Baseline → Component → Eval → Keep/Remove

## Evidence
- research/topics/22-harness-ablation-and-minimalism.md
- Anthropic Harness Design
- Agent Eval practices

## Targeted Research Before Draft
- published/engineering harness ablation 사례 추가 수집
- model-upgrade 후 scaffold removal 실측 사례 확보
- multi-component interaction 실험 방법 보강

## Avoid
- 통계적 유의성 과장
- 한 benchmark 결과의 일반화

## Draft Exit Criteria
- ablation procedure가 reproducible하다.
- Harness Debt checklist가 있다.
