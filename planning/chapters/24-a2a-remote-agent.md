# 24장. A2A와 Remote Agent

## Goal
독자가 local subagent와 independent remote Agent System을 구분하고 A2A의 Task/Artifact boundary를 이해할 수 있게 한다.

## Core Claims
- A2A는 Agent 내부 orchestration protocol이 아니라 independent Agent System 간 interoperability를 다룬다.
- Agent Card는 capability discovery이지 authorization이 아니다.
- A2A Task는 remote work contract이고 MCP Task와 다르다.
- Artifact는 remote work의 deliverable을 명시적으로 표현한다.

## Reader Questions
- MCP와 A2A를 언제 각각 쓰는가?
- remote Agent의 내부 memory/tool을 알아야 하는가?
- A2A Task를 Factory Task로 저장하면 되는가?

## Flow
1. local specialist vs remote Agent
2. Agent Card
3. Message / Task / Artifact
4. lifecycle
5. auth
6. MCP 비교
7. internal domain adapter
8. failure / async update

## Example / Figure
- Local Agent → A2A Remote Compliance Agent
- Figure: MCP vs A2A vs Factory Task

## Evidence
- research/topics/12-mcp-a2a-task-boundary.md
- A2A Specification

## Avoid
- A2A SDK 구현 전체
- 조직 workflow engine

## Draft Exit Criteria
- MCP/A2A/Factory Task 비교표가 있다.
