# 23장. Agent-as-Tool과 Handoff

## Goal
독자가 specialist Agent를 호출하는 방식과 ownership을 넘기는 방식을 구분할 수 있게 한다.

## Core Claims
- Agent-as-Tool은 manager가 ownership을 유지한다.
- Handoff는 interaction/work ownership을 이전한다.
- Handoff에는 context와 authority transfer contract가 필요하다.
- independent verifier는 executor와 다른 권한/관점을 가질 수 있다.

## Reader Questions
- Subagent 호출과 Handoff는 무엇이 다른가?
- 어떤 state를 specialist에게 넘겨야 하는가?
- verifier Agent는 executor 결과를 그대로 믿어도 되는가?

## Flow
1. manager pattern
2. agent-as-tool
3. handoff
4. context transfer
5. authority transfer
6. result contract
7. verifier separation
8. failure/handoff recovery

## Example / Figure
- Manager → Researcher Tool
- Support Agent A → Billing Agent B ownership handoff

## Evidence
- research/topics/07-multi-agent-interoperability.md
- OpenAI Agents SDK
- Google ADK

## Avoid
- 조직 전체 scheduling
- A2A 상세는 다음 장

## Draft Exit Criteria
- 두 패턴의 ownership 차이가 명확하다.
