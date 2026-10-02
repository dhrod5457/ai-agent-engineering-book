# 6장. MCP와 Capability Boundary

## Goal
독자가 MCP가 해결하는 문제와 해결하지 않는 문제를 구분하고 내부 Agent Architecture와 protocol object를 분리할 수 있게 한다.

## Core Claims
- MCP는 Agent 자체가 아니라 capability/context integration boundary다.
- 2026-07-28 MCP core는 stateless 방향으로 이동했다.
- MCP Task는 long-running capability invocation이며 Product/Factory Task와 다르다.
- Capability Discovery와 Authorization은 별도다.

## Reader Questions
- MCP를 쓰면 Tool architecture가 해결되는가?
- MCP Task와 내부 Task를 같은 객체로 써도 되는가?
- protocol session과 runtime session은 같은가?

## Flow
1. MCP가 해결하는 integration 문제
2. Tool / Resource / Prompt
3. stateless core
4. Tasks extension
5. authorization boundary
6. internal domain model과 adapter
7. A2A와 비교 예고

## Example / Figure
- Agent Harness → MCP Client → MCP Server → Capability
- Figure: Protocol Task vs Internal Task

## Evidence
- research/topics/03-tools-protocols.md
- research/topics/12-mcp-a2a-task-boundary.md
- MCP 2026-07-28 specification/release

## Avoid
- MCP SDK 전체 API
- 서버 구현 튜토리얼

## Draft Exit Criteria
- MCP의 정확한 위치가 한 그림으로 설명된다.
- Task/Session 명칭 충돌을 명확히 경고한다.
