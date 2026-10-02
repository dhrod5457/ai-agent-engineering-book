# 5장. Tool은 Agent-Computer Interface다

## Goal
독자가 Tool을 API wrapper가 아니라 Agent의 행동 공간을 설계하는 interface로 볼 수 있게 한다.

## Core Claims
- Tool Interface는 Agent Capability의 일부다.
- name, description, schema, output shape가 성능에 영향을 준다.
- 큰 Tool Surface는 selection ambiguity와 security surface를 늘린다.
- Tool Result도 untrusted context가 될 수 있다.

## Reader Questions
- 기존 REST API를 그대로 Tool로 노출하면 왜 문제가 생기는가?
- Tool을 얼마나 잘게 나눠야 하는가?
- Tool output은 얼마나 반환해야 하는가?

## Flow
1. API와 ACI의 차이
2. capability boundary
3. naming / schema
4. side effect와 error contract
5. result filtering
6. trust/provenance
7. tool eval

## Example / Figure
- generic shell tool vs bounded repository tools 비교
- Figure: Agent → Tool Contract → External API

## Evidence
- research/topics/03-tools-protocols.md
- SWE-agent ACI
- Anthropic Tool Engineering

## Avoid
- 특정 API SDK 구현
- Tool registry 제품 비교

## Draft Exit Criteria
- 좋은 Tool Contract checklist가 있다.
- Tool Result trust 문제가 포함된다.
- MCP 장으로 자연스럽게 이어진다.
