# Evaluation and Observability

## Agent Eval은 Output Eval보다 넓다

Agent는 multi-turn으로 환경을 변경한다.

따라서 평가 대상도 여러 층으로 나뉜다.

~~~text
Final Output
Trajectory
Tool Selection
Tool Arguments
Policy Compliance
Environment Outcome
Latency
Cost
Reliability
Recovery
~~~

## Trace가 필요한 이유

OpenAI의 trace grading과 Anthropic agent eval 자료 모두 Agent 문제를 final answer만으로 진단하기 어렵다는 점을 보여준다.

예:

Final result가 실패했다면 원인은 다음 중 하나일 수 있다.

- 잘못된 retrieval
- 잘못된 tool 선택
- 올바른 tool + 잘못된 argument
- tool failure
- observation 해석 실패
- premature stop
- handoff 실패
- policy block
- runtime resource 부족

Trace 없이는 원인을 분리하기 어렵다.

## Grader 종류

### Deterministic / Code-based
- exact state
- unit/integration test
- schema validation
- static analysis
- DB final state
- artifact inspection

### Model-based
- instruction following
- quality
- relevance
- strategy critique

### Human
- subjective UX
- policy edge case
- grader calibration
- high-risk acceptance

가능하면 objective outcome에 가까운 grader를 우선한다.

## Eval Dataset

초기에는 거대한 benchmark보다 실제 실패를 수집하는 것이 유용하다.

Anthropic은 20~50개의 실제 task/failure로 시작하는 접근을 제시한다.

추천 구조:

~~~text
Capability Eval
Regression Eval
Security Eval
Performance Eval
Failure Corpus
Production Sample Review
~~~

## Repeated Reliability

Agent는 nondeterministic하므로 한 번 성공만으로 신뢰성을 판단하기 어렵다.

tau-bench의 pass^k와 같은 관점은 다음 질문을 강조한다.

> 같은 종류의 task를 반복했을 때 얼마나 일관되게 성공하는가?

## Infrastructure Noise

Agentic coding benchmark에서 CPU/RAM/time limit/container enforcement 차이가 점수에 영향을 줄 수 있다.

따라서 benchmark 기록에는 최소한 다음이 필요하다.

- model/version
- harness/version
- tool surface
- environment image
- CPU/RAM
- timeout
- max steps
- network policy
- retry policy
- grader
- random/repeat configuration

## 설계 원칙 후보

1. Agent trace는 운영 부가 기능이 아니라 개발 도구다.
2. Eval은 model만이 아니라 Agent System 전체를 version한다.
3. Production failure를 regression dataset으로 승격한다.
4. Outcome grader를 가능한 한 deterministic하게 만든다.
5. benchmark score의 작은 차이를 과도하게 해석하지 않는다.
