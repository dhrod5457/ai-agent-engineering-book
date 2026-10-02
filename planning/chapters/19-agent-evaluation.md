# 19장. Agent를 어떻게 평가할 것인가

## Goal
독자가 Agent를 final answer 하나가 아니라 trajectory, outcome, reliability, security까지 포함해 평가할 수 있게 한다.

## Core Claims
- Agent Eval은 Output Eval보다 넓다.
- 가능한 한 실제 environment outcome에 가까운 grader를 우선한다.
- Nondeterminism 때문에 repeated evaluation이 필요하다.
- benchmark score는 model만의 성능이 아니다.

## Reader Questions
- 정답 문자열이 없는 Agent task는 어떻게 평가하는가?
- model grader를 얼마나 믿을 수 있는가?
- 한 번 성공하면 pass인가?

## Flow
1. output / trajectory / outcome
2. grader 종류
3. tool routing / args
4. state handling
5. security
6. repeated reliability
7. infra noise
8. benchmark versioning

## Example / Figure
- 같은 final answer인데 unsafe trajectory인 사례
- Figure: Eval layers

## Evidence
- research/topics/06-evaluation-observability.md
- research/topics/08-benchmarks.md
- research/topics/16-benchmark-versioning-measurement.md
- Anthropic Evals / Infra Noise
- OSWorld / tau2-bench

## Avoid
- leaderboard 중심 비교
- model grader 만능론

## Draft Exit Criteria
- Eval dimensions와 grader 선택 규칙이 있다.
