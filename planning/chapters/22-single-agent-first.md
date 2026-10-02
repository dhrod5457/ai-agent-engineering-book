# 22장. Single-Agent First

## Goal
독자가 Multi-Agent를 기본값으로 선택하지 않고 실제 boundary benefit이 있을 때만 도입하도록 판단할 수 있게 한다.

## Core Claims
- Multi-Agent는 broken state/tool/security를 해결하지 않는다.
- Context, Permission, Ownership boundary가 명확할 때 specialist 분리가 가치 있다.
- Agent 수가 늘면 coordination, context duplication, latency, tracing 비용도 늘어난다.
- 병렬화는 독립 work에 적합하다.

## Reader Questions
- Agent를 여러 개 쓰면 항상 더 잘하나?
- specialist는 언제 분리해야 하는가?
- reviewer Agent를 추가하면 신뢰성이 올라가는가?

## Flow
1. multi-agent hype
2. single-agent baseline
3. 분리 이유
4. context isolation
5. permission isolation
6. parallel work
7. coordination cost
8. decision checklist

## Example / Figure
- 하나의 Agent vs specialist split 두 사례
- Figure: benefit/cost boundary

## Evidence
- research/topics/07-multi-agent-interoperability.md
- Anthropic Building Effective Agents

## Avoid
- 가상 Agent 조직도
- Agent 수 자체를 성숙도 지표로 사용

## Draft Exit Criteria
- Multi-Agent 도입 decision table이 있다.
