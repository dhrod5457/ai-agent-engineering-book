# 1장. Model과 Agent는 무엇이 다른가

## Goal
독자가 Model benchmark와 실제 Agent capability를 구분하고, Agent를 하나의 실행 시스템으로 볼 수 있게 한다.

## Core Claims
- Model Capability와 Agent Capability는 다르다.
- Agent는 Prompt + Model + Tool 목록이 아니다.
- 실제 Agent 성능에는 Harness, Tool Interface, State, Runtime, Policy가 함께 영향을 준다.
- Agent 설계는 모델 선택보다 responsibility boundary에서 시작해야 한다.

## Reader Questions
- Tool calling이 가능하면 Agent인가?
- 더 강한 모델로 바꾸면 Agent 구조 문제도 해결되는가?
- Agent Framework가 곧 Agent Architecture인가?

## Flow
1. 단일 LLM 호출과 Agent 실행 비교
2. Prompt wrapper가 깨지는 지점
3. Model / Harness / Runtime / State 분리
4. Agent Capability 식
5. 책 전체 Reference Model 소개
6. 이후 장의 경계 안내

## Example / Figure
- 같은 모델을 두 개의 다른 Harness에 넣었을 때 결과가 달라지는 개념 사례
- Figure: Model → Agent System 확장도

## Evidence
- research/topics/01-agent-loop-runtime.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
- OpenAI Agents SDK
- Anthropic Building Effective Agents

## Avoid
- LLM 내부 architecture
- benchmark 순위 비교
- 특정 Framework 추천

## Draft Exit Criteria
- Model과 Agent의 차이를 독자가 한 문장으로 설명할 수 있다.
- 책 전체 component boundary가 처음 등장한다.
- 이후 장에서 반복할 핵심 용어가 정의된다.
