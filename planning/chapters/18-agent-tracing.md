# 18장. Trace 없이는 Agent를 디버깅할 수 없다

## Goal
독자가 final output만 보지 않고 Agent execution을 재구성할 수 있는 trace model을 설계할 수 있게 한다.

## Core Claims
- Agent failure는 output만으로 원인을 분리하기 어렵다.
- model/tool/state/policy event를 연결해야 한다.
- Audit Trace와 Debug Trace는 목적이 다를 수 있다.
- Trace는 Eval과 regression의 원천 데이터다.

## Reader Questions
- 무엇을 기록해야 하는가?
- chain-of-thought를 저장해야 하는가?
- 로그와 trace는 무엇이 다른가?

## Flow
1. output-only debugging의 한계
2. trace span/event
3. model/tool/state/policy
4. correlation / causation
5. audit vs debug
6. privacy / sensitive data
7. cost/latency
8. trace → eval

## Example / Figure
- wrong tool selection이 최종 failure로 이어지는 trace
- Figure: end-to-end Agent Trace

## Evidence
- research/topics/06-evaluation-observability.md
- OpenAI Trace Grading
- OpenAI Agent Evals

## Avoid
- private chain-of-thought 저장을 필수로 주장
- observability vendor 비교

## Draft Exit Criteria
- trace schema 후보가 제시된다.
- 다음 Eval 장에 바로 사용할 수 있다.
