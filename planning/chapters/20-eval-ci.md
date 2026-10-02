# 20장. Eval을 CI로 만든다

## Goal
독자가 production failure와 Agent 변경을 repeatable regression loop로 연결할 수 있게 한다.

## Core Claims
- Eval은 일회성 benchmark가 아니라 개발 lifecycle 일부여야 한다.
- Production failure를 reusable case로 승격해야 한다.
- PR / Nightly / Release / Shadow gate의 비용과 역할이 다르다.
- AgentVersion은 model뿐 아니라 harness/tools/runtime/policy/grader를 포함한다.

## Reader Questions
- Eval을 언제 돌려야 하는가?
- 너무 비싼 Agent eval을 CI에 어떻게 넣는가?
- Model upgrade는 어떻게 검증하는가?

## Flow
1. failure corpus
2. regression dataset
3. fast PR gate
4. nightly / release
5. shadow / canary
6. version tuple
7. promotion rule
8. risk-weighted no-regression

## Example / Figure
- production review correction → regression test
- Figure: Trace → Feedback → Eval → Promotion

## Evidence
- research/topics/15-eval-ci-regression.md
- OpenAI Agent Improvement Loop
- Macro Evals
- Anthropic Evals

## Avoid
- CI 제품 사용법
- 평균 점수 하나로 promotion

## Draft Exit Criteria
- 실제 운영 가능한 cadence가 제시된다.
