# 10장. Long-running Agent

## Goal
독자가 context window보다 긴 작업에서 milestone, progress, horizon budget을 설계할 수 있게 한다.

## Core Claims
- Long-running 문제는 긴 context만으로 해결되지 않는다.
- hidden state, multi-item tracking, horizon exhaustion이 주요 실패 원인이다.
- incremental artifact와 progress state가 필요하다.
- 준비 작업이 실제 작업 horizon을 소진하지 않도록 phase budget을 둬야 한다.

## Reader Questions
- Context window가 커지면 장기 Agent 문제가 사라지는가?
- 한 번의 run에서 끝내야 하는가?
- Agent가 일찍 "완료"했다고 판단하는 문제를 어떻게 막는가?

## Flow
1. short task와 long task 차이
2. session boundary
3. milestone / progress
4. hidden/multi-item state
5. phase budget
6. horizon exhaustion
7. blocker / clarification

## Example / Figure
- 2시간짜리 procurement workflow
- Figure: Goal → Milestone → Checkpoint → Verification

## Evidence
- research/topics/04-harness-long-running.md
- research/topics/13-long-horizon-computer-use.md
- Anthropic Long-running Harness
- OSWorld 2.0

## Avoid
- Factory-level scheduling
- 무조건적인 autonomous continuation

## Draft Exit Criteria
- 장기 task 전용 control이 short task와 구분된다.
- 다음 장 reconciliation 필요성이 도출된다.
