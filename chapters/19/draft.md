# 19장. Agent를 어떻게 평가할 것인가

에이전트가 최종 답변을 맞혔다. 그런데 중간에 허용되지 않은 도구를 세 번 호출했고, 운영 데이터를 불필요하게 읽었으며, 같은 행동을 두 번 실행했다. 이 에이전트를 성공했다고 볼 수 있을까. 따라서 에이전트를 평가할 때는 최종 출력뿐 아니라 그 결과에 이르는 과정도 살펴야 한다.

## Output Eval의 한계

일반 LLM 평가에서는 최종 응답 품질이 중요하다. 에이전트는 환경을 바꾼다. 따라서 다음도 평가 대상이 된다.

~~~text
Output
Trajectory
Tool Selection
Tool Arguments
State Handling
Policy Compliance
Environment Outcome
Reliability
Cost
Latency
Recovery
~~~

## Output Eval

최종 답변이나 산출물 자체를 평가한다.

예:

- 답변 정확성
- Report 품질
- 생성 파일 내용
- Structured Output Schema

필요하지만 충분하지 않다.

## Trajectory Eval

에이전트가 어떤 경로로 결과에 도달했는지 본다.

예:

- 올바른 도구를 선택했는가.
- 불필요한 도구를 반복했는가.
- 작업 인계가 적절했는가.
- Policy Violation 시도가 있었는가.
- 재시도가 합리적이었는가.

같은 출력이라도 실행 경로 품질이 다를 수 있다.

## Outcome Eval

가능하면 환경의 최종 상태를 본다.

코드 작업 에이전트:

~~~text
tests pass?
expected diff?
build succeeds?
~~~

Browser Agent:

~~~text
actual form submitted?
correct field values?
~~~

Database Agent:

~~~text
expected final row state?
~~~

Outcome Eval은 Proxy가 아니라 완료 자체에 가깝다.

## Deterministic Grader

가능하면 Machine-checkable한 실제 환경에서 확인한 결과를 우선한다.

예:

- unit test
- schema validation
- exact DB state
- checksum
- static analysis
- artifact inspection

장점:

- 반복 가능
- 빠름
- 비용 낮음
- 해석이 명확함

## Model Grader

모든 품질을 Code로 판정하기 어렵다.

예:

- 설명의 명확성
- 요구사항 충족 정도
- 문서 품질
- 전략 적절성

이때 Model Grader를 사용할 수 있다. 하지만 Model Grader도 버전과 프롬프트에 따라 달라질 수 있다. 따라서 채점기 자체를 Versioned Component로 본다.

## Human Grader

다음 상황에서는 사람이 필요할 수 있다.

- UX 품질
- 정책 Edge Case
- 고위험 Acceptance
- Model Grader Calibration

사람의 검토를 모든 사례에 쓰면 비용이 크다. Sample과 Calibration에 집중할 수 있다.

## Security Eval

에이전트가 작업을 성공해도 보안을 위반했다면 좋은 에이전트가 아니다.

예:

- 외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)에 속음
- 메모리에 악성 정보를 심는 공격(Memory Poisoning) 허용
- Unauthorized Tool 시도
- Sensitive Data 노출
- 승인 우회

Security Dataset을 별도로 유지할 수 있다.

## State Handling Eval

오래 실행되는 에이전트에서는 상태가 중요한 평가 대상이다.

예:

- stale source를 사용했는가.
- completed action을 중복 실행했는가.
- pending approval을 잊었는가.
- multi-item state를 누락했는가.
- checkpoint 후 정확히 resume했는가.

이 영역은 Output-only benchmark에서 잘 보이지 않을 수 있다.

## Repeated Reliability

에이전트는 같은 입력에도 결과가 달라질 수 있는할 수 있다. 한 번 성공했다고 안정적이라고 말하기 어렵다. 같은 작업을 여러 번 실행해야 할 수 있다.

~~~text
Trial 1: pass
Trial 2: pass
Trial 3: fail
Trial 4: pass
Trial 5: fail
~~~

여기서 평균 성공뿐 아니라 Consistency가 중요하다. tau-bench 계열에서는 반복 신뢰성을 보는 측정 지표도 제안돼 왔다.

## pass@k와 pass^k

두 측정 지표는 목적이 다르다. 아래 식은 직관을 설명하기 위한 것으로, 실제 benchmark마다 계산 정의는 다시 확인해야 한다.

개념적으로:

~~~text
pass@k
= k번 중 한 번이라도 성공

pass^k
= k번 모두 성공
~~~

에이전트 운영에서는 "한 번은 된다"와 "반복해서 된다"가 다르다. 운영 작업은 후자에 더 민감할 수 있다.

## Infrastructure Noise

Agentic Benchmark는 실행 환경 영향을 받는다.

예:

- CPU
- RAM
- 응답 시간 초과
- Browser Stability
- 네트워크
- Package Availability
- Container Startup

Anthropic의 Agentic Coding Eval 분석에서도 Infrastructure 설정이 결과에 유의미한 영향을 줄 수 있음을 보여준다. 따라서 작은 점수 차이를 모델 차이로 바로 해석하지 않는다.

## Benchmark Result는 System Result다

Agent Benchmark 결과를 다음처럼 시스템 전체의 결과로 보는 편이 낫다.

~~~text
Benchmark Result
=
Model
+ Harness
+ Tool Interface
+ Context Policy
+ State Strategy
+ Runtime
+ Environment
+ Grader
+ Noise
~~~

정확한 수학식은 아니다. Evaluation Boundary를 넓게 보자는 뜻이다.

## Benchmark Versioning

성능 비교 평가도 바뀐다.

- 작업 수정
- 채점기 수정
- 환경 수정
- 정책 수정
- 도구 수정

tau2-bench는 채점기 수정으로 동일한 실행 경로를 다시 평가해 점수가 바뀔 수 있는 사례를 공개했다. 따라서 결과에는 다음을 기록한다.

~~~text
benchmark_version
task_revision
grader_version
model_version
harness_version
environment_image
runtime_resource
trial_count
~~~

## Binary vs Partial

많은 단계에 걸친 작업에서는 Final Success만 보면 어디에서 실패했는지 알기 어렵다. Partial Checkpoint를 사용할 수 있다.

예:

~~~text
Milestone 1 pass
Milestone 2 pass
Milestone 3 fail
~~~

OSWorld 2.0 같은 Long-horizon Benchmark도 세밀한 체크포인트(Checkpoint: 실행을 이어가기 위한 상태 기록)를 활용한다. 하지만 Partial Score가 완료를 대신해서는 안 된다.

~~~text
Diagnostic Partial Score
≠ Product Completion
~~~

## Capability Slice

평균 점수 하나는 실패를 숨길 수 있다.

예:

~~~text
Overall 82%

Tool Routing 95%
State Recovery 52%
Security 91%
Long-horizon 48%
~~~

이 에이전트는 Short Task에는 강하지만 장시간 작업에는 약하다. 기능별 Slice가 필요한 이유다.

## Failure Corpus

초기 Eval Dataset은 거대할 필요가 없다. 운영에서 나온 실패 20~50개부터 시작할 수 있다.

예:

- wrong tool
- stale state
- premature completion
- duplicate mutation
- permission denial loop
- hallucinated success

운영 실패가 좋은 Eval Seed가 된다.

## Eval Case 구조

예:

~~~text
id
goal
initial_state
environment
allowed_tools
expected_outcome
grader
risk
repeat_count
source_failure
~~~

이 부가 정보가 있으면 Regression Dataset을 관리하기 쉽다.

## 작은 예: PR 작성 Agent

작업:

> 수정 후 테스트를 통과시키고 PR을 생성하라.

평가:

~~~text
Output:
PR URL exists

Trajectory:
no forbidden tool
no duplicate PR
reasonable retries

Outcome:
tests pass
PR diff correct

Security:
no secret access

Reliability:
5 repeated runs

Cost:
within budget
~~~

이렇게 해야 에이전트 품질을 더 잘 볼 수 있다.

## 이 장에서 가져갈 것

에이전트 평가는 "답을 맞혔는가"보다 넓다.

~~~text
Output
+
Trajectory
+
Outcome
+
Reliability
+
Security
+
Cost
~~~

그리고 Benchmark Score를 Model Score로 읽지 않는다. 다음 장에서는 이 평가를 개발 작업 흐름에 넣는다. 운영 실패를 회귀를 확인할 평가 사례로 만들고, PR / Nightly / Release Gate에 연결하는 개발 과정에 통합한 지속적 평가를 다룬다.

## 주요 근거

- OpenAI Agent Evals / Trace Grading
- Anthropic, Demystifying Evals for AI Agents
- Anthropic, Infrastructure Noise in Agentic Coding Evals
- OSWorld / OSWorld 2.0
- tau-bench / tau2-bench
- research/topics/06-evaluation-observability.md
- research/topics/16-benchmark-versioning-measurement.md
