# 9장. 실패 후 이어가는 Agent

## Goal
독자가 crash, pause, approval, retry 이후 Agent를 안전하게 재개하는 recovery 구조를 설계할 수 있게 한다.

## Core Claims
- Replay는 Model/Tool Side Effect의 재실행이 아니다.
- 실행 결과를 event로 기록해야 recovery가 안전해진다.
- External mutation에는 idempotency가 필요하다.
- Conversation history만으로 recovery를 설계하면 부족하다.

## Reader Questions
- 프로세스가 죽으면 어디부터 다시 시작해야 하는가?
- 이전 tool call을 다시 실행해도 되는가?
- approval 중 멈춘 실행을 어떻게 이어가는가?

## Flow
1. restart-from-prompt의 위험
2. execution history
3. deterministic replay 가능한 것
4. 재실행하면 안 되는 것
5. idempotency
6. checkpoint / snapshot
7. pause/resume state

## Example / Figure
- PR 생성 tool 실행 직후 crash한 사례
- Figure: event history를 이용한 recovery

## Evidence
- research/topics/18-durable-state-event-log-replay.md
- Temporal Durable Execution
- Anthropic Managed Agents

## Avoid
- Workflow engine 내부 구현
- exactly-once 보장 과장

## Draft Exit Criteria
- duplicate side effect를 막는 원칙이 구체적이다.
- replay와 retry 차이가 명확하다.
