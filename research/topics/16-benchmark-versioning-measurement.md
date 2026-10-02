# Benchmark Versioning and Measurement Hygiene

기준일: 2026-10-02

## Benchmark도 Software다

Agent benchmark는 고정된 시험지가 아니다.

다음이 계속 바뀐다.

- task
- policy
- grader
- environment
- user simulator
- tool implementation
- resource limit
- leaderboard rule

따라서 benchmark 이름만 기록하면 충분하지 않다.

## tau2-bench 사례

2026-07-15의 tau2-bench 1.0.1은 banking_knowledge grading 수정으로 같은 trajectory를 재평가해도 점수가 바뀔 수 있음을 명시했다.

일부 model은 grading fix만으로 pass^1가 여러 point 상승했다.

즉:

~~~text
Same Agent Trajectory
+ New Grader
= Different Score
~~~

이 사례는 benchmark version pinning의 필요성을 보여준다.

## Task Validity

Community issue에서도 특정 domain의 scoring이 실제 transactional capability를 충분히 요구하지 않을 수 있다는 문제 제기가 있었다.

Benchmark는 이름이 현실적인 것과 실제 construct validity가 높은 것이 다르다.

질문해야 한다.

- 성공하려면 실제 side effect가 필요한가.
- communicate만 잘해도 통과 가능한가.
- grader가 intended skill을 측정하는가.
- shortcut이 존재하는가.

## OSWorld 2.0의 개선 방향

OSWorld 2.0은 binary completion 외에 partial checkpoint를 많이 두고 long-horizon failure를 분석한다.

이 접근은 장기 workflow에서 useful하다.

왜냐하면:

~~~text
Final Fail
~~~

만으로는 500-step trajectory 중 어디에서 실패했는지 알 수 없기 때문이다.

checkpoint는 progress와 failure location을 더 잘 보여준다.

## Measurement Tuple

Agent benchmark 결과는 다음을 함께 기록한다.

~~~text
BenchmarkResult = (
  benchmark_version,
  task_revision,
  grader_version,
  model_version,
  harness_version,
  tool_version,
  environment_image,
  cpu_ram,
  timeout,
  step_limit,
  network,
  retry_policy,
  trial_count
)
~~~

## Infra Failure 분리

다음은 Agent reasoning failure와 구분해야 한다.

- service timeout
- package registry outage
- environment setup fail
- disk full
- browser crash
- VM startup fail
- rate limit

그렇지 않으면 system reliability와 model capability가 혼합된다.

## Binary vs Partial

### Binary
실제 outcome 달성 여부에 적합.

### Partial
long-horizon diagnosis와 learning signal에 적합.

두 metric을 모두 사용할 수 있지만 최종 product acceptance에서는 proxy partial score가 실제 완료를 대신하면 안 된다.

## Benchmark Drift

정기적으로 확인한다.

- task가 모델 학습 데이터에 노출됐는가.
- 최신 product behavior와 맞는가.
- tool/API가 바뀌었는가.
- grader가 여전히 valid한가.
- benchmark가 너무 쉬워졌는가.
- benchmark-specific optimization이 과도해졌는가.

## 책에 반영할 원칙

1. Benchmark 이름이 아니라 versioned environment를 기록한다.
2. Grader도 versioned software로 본다.
3. task validity를 정기 감사한다.
4. infrastructure failure를 model failure와 분리한다.
5. long-horizon에서는 checkpoint/partial signal을 진단에 활용한다.
6. 최종 completion은 실제 outcome으로 판정한다.
7. leaderboard delta가 작을수록 measurement noise를 먼저 의심한다.

## 주요 근거

- tau2-bench changelog 1.0.1
- tau2-bench leaderboard submission rules
- tau2-bench issue discussions
- OSWorld 2.0
- Anthropic Infrastructure Noise
