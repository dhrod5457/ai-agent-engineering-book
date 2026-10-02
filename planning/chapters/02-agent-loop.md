# 2장. Agent Loop를 설계한다

## Goal
독자가 Agent의 최소 실행 루프와 production loop에 추가돼야 할 control을 설계할 수 있게 한다.

## Core Claims
- Agent의 핵심은 Observation → Decision → Action → Observation의 반복이다.
- Stop Condition은 모델이 아니라 Harness 책임이다.
- Retry, budget, interruption, failure classification이 없으면 production loop가 아니다.
- Tool failure와 model failure를 분리해야 한다.

## Reader Questions
- Agent loop는 단순 while 문과 무엇이 다른가?
- 언제 멈춰야 하는가?
- 실패하면 같은 요청을 다시 던지면 되는가?

## Flow
1. ReAct식 최소 loop
2. final output / tool call / handoff
3. stop condition
4. timeout / budget / max turn
5. retryable vs blocked vs unrecoverable
6. pause / resume
7. production loop checklist

## Example / Figure
- 파일 수정 Agent가 test 실패 후 재시도하는 작은 loop
- Figure: 최소 Loop vs Production Loop

## Evidence
- research/topics/01-agent-loop-runtime.md
- ReAct
- OpenAI Running Agents
- Google ADK

## Avoid
- Durable multi-task scheduler
- full workflow engine 구현

## Draft Exit Criteria
- 최소 loop와 production loop를 구분한다.
- stop/failure state가 명시된다.
- 다음 장 Harness로 자연스럽게 연결된다.
