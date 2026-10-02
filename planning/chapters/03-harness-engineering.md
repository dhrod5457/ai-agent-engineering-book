# 3장. Harness Engineering

## Goal
독자가 Harness를 Framework 이름이 아니라 Agent 실행을 제어하는 software layer로 이해하고 최소 책임을 정의할 수 있게 한다.

## Core Claims
- Harness는 Model과 Runtime 사이의 control logic이다.
- Harness component는 검증 가능한 engineering hypothesis다.
- 복잡한 scaffold가 항상 성능을 높이지 않는다.
- Harness는 versioning, regression, ablation 대상이다.

## Reader Questions
- Harness와 Agent Framework는 같은가?
- planner, evaluator, memory는 항상 필요한가?
- Model upgrade 후 기존 Harness를 그대로 써도 되는가?

## Flow
1. Harness가 생기는 이유
2. responsibility inventory
3. minimal harness
4. common scaffold
5. long-running에서 추가되는 책임
6. versioning
7. ablation 개념 예고

## Example / Figure
- Minimal Harness와 Over-scaffolded Harness 비교
- Figure: Agent Definition / Harness / Runtime boundary

## Evidence
- research/topics/04-harness-long-running.md
- research/topics/14-coding-agent-harness-comparison.md
- research/topics/22-harness-ablation-and-minimalism.md
- Anthropic Harness Design

## Avoid
- 특정 SDK 튜토리얼
- 모든 orchestration pattern 소개

## Draft Exit Criteria
- Harness 책임 목록이 명확하다.
- Framework와 구분된다.
- Part II의 Context/Tool이 Harness 내부에서 어디에 붙는지 설명한다.
