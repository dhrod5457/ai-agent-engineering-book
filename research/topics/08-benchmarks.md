# Agent Benchmark Landscape

## 왜 별도 정리가 필요한가

Agent benchmark는 서로 다른 능력을 측정한다.

하나의 leaderboard를 Agent 전체 능력으로 일반화하면 안 된다.

## AgentBench

- Source: https://arxiv.org/abs/2308.03688
- 초점: 다양한 interactive environment
- 보는 능력:
  - long-horizon reasoning
  - decision making
  - instruction following

의미:
초기 LLM Agent의 일반적 실패 유형을 폭넓게 확인하는 자료.

## GAIA

- Source: https://arxiv.org/abs/2311.12983
- 초점: real-world assistant
- 요구:
  - reasoning
  - web
  - multimodal
  - tool use

의미:
단일 NLP 능력이 아니라 여러 capability를 조합해야 하는 실제형 task.

## SWE-agent / SWE-bench 계열

- SWE-agent: https://arxiv.org/abs/2405.15793
- 초점: repository 기반 software engineering
- 중요점:
  - ACI 설계 효과
  - test와 repository interaction
  - environment가 성능에 직접 관여

의미:
Coding Agent 성능을 model만으로 설명하기 어렵다는 대표 사례.

## tau-bench

- Source: https://arxiv.org/abs/2406.12045
- 초점:
  - user interaction
  - policy following
  - API tools
  - final DB state
- 특징: 반복 reliability를 보기 위한 pass^k

주의:
공식 저장소는 후속 benchmark로 이동 중이므로 실제 수치 인용 전 최신 버전 확인.

## AgentDojo

- Source: https://arxiv.org/abs/2406.13352
- 초점:
  - tool-using agent security
  - prompt injection
  - utility/security tradeoff

의미:
Agent security eval을 실제 tool interaction 안에서 수행.

## OSWorld

- Source: https://arxiv.org/abs/2404.07972
- Current project: https://os-world.github.io/
- 초점:
  - desktop computer use
  - cross-app workflow
  - execution-based outcome evaluation

의미:
GUI Agent에서는 grounding뿐 아니라 environment setup과 deterministic evaluator가 핵심.

## Benchmark를 읽는 체크리스트

~~~text
What is the task?
What is the environment?
What tools/actions are allowed?
What is the initial state?
What is the max step/time?
What runtime resources exist?
What counts as success?
Is success outcome-based or transcript-based?
How many repeated trials?
What harness is used?
Are infra failures separated?
~~~

## 현재 결론

~~~text
Benchmark Score
≠ Model Capability alone

Benchmark Score
= Model
+ Harness
+ Tool Interface
+ Runtime
+ Context
+ Policy
+ Eval Environment
+ Noise
~~~

이 식은 책의 중요한 논점 후보이다.
