# 25장. Minimum Viable Production Agent

## Goal
독자가 책 전체를 실제 도입 순서로 압축하고 과도한 Agent Platform 구축 없이 최소 production architecture를 설계할 수 있게 한다.

## Core Claims
- 처음부터 Memory, Multi-Agent, Planner가 필요하지 않다.
- Control과 Verification을 Capability보다 먼저 만든다.
- 성숙도는 기능 수가 아니라 failure/recovery/control 능력으로 본다.
- Agent State Plane과 Factory Control Plane의 경계를 유지한다.

## Reader Questions
- 최소 production Agent에는 무엇이 꼭 필요한가?
- 무엇부터 추가해야 하는가?
- 언제 Software Factory 단계로 넘어가는가?

## Flow
1. minimal agent
2. small tool surface
3. controlled runtime
4. deterministic verification
5. trace/eval
6. durable state
7. identity/policy
8. memory/long-running
9. multi-agent
10. factory boundary

## Example / Figure
- 5단계 maturity roadmap
- Figure: Minimal Agent → Production Agent → Software Factory

## Evidence
- planning/concept.md
- planning/scope.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
- 전체 research

## Avoid
- 전체 Software Factory 설계 재설명
- maturity level을 인증 표준처럼 표현

## Draft Exit Criteria
- 독자가 자신의 시스템 현재 단계를 진단할 수 있다.
- 다음 책인 Software Factory로 경계가 자연스럽게 이어진다.
