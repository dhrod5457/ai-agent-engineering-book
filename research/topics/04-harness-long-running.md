# Harness and Long-running Agents

## Harness란 무엇인가

현재 조사에서 Harness는 다음을 묶는 실행 계층으로 보는 것이 가장 유용하다.

~~~text
Harness
- Agent loop
- Context assembly
- Tool dispatch
- State continuation
- Retry / interruption
- Stop condition
- Approval integration
- Tracing
- Model adaptation scaffolding
~~~

Harness는 Model도 아니고 Runtime도 아니다.

## Long-running에서 드러나는 문제

짧은 task에서는 좋은 prompt와 tool만으로도 Agent가 동작할 수 있다.

시간이 길어지면 다른 문제가 드러난다.

- context exhaustion
- premature completion
- forgotten decisions
- repeated work
- environment drift
- process crash
- tool/runtime failure
- incomplete handoff
- stale plan

이때 Agent 성능은 model 지능보다 continuity system의 품질에 크게 좌우된다.

## Anthropic 장기 작업 연구에서 얻는 패턴

### 1. Incremental progress

한 session에서 전부 끝내려 하지 않고 다음 session이 이어받을 수 있는 작은 진척을 남긴다.

### 2. Explicit artifacts

- progress file
- test state
- commit
- task list
- implementation artifact

등 외부 상태를 남긴다.

### 3. Initializer와 Worker 역할 분리

첫 run이 environment와 plan을 정리하고 후속 run이 incremental work를 수행하는 패턴이 유효했다.

### 4. Harness assumption은 노후화된다

새로운 model이 더 강해지면 예전 scaffolding이 필요 없거나 오히려 방해가 될 수 있다.

따라서 Harness도 다음 과정을 거쳐야 한다.

~~~text
Hypothesis
→ Eval
→ Add scaffold
→ Measure
→ Model upgrade
→ Re-evaluate
→ Remove unnecessary scaffold
~~~

## Brain / Hands / Session 분리

2026 Managed Agents 사례는 세 경계를 특히 명확히 보여준다.

~~~text
Brain
= model + harness

Hands
= sandbox + executable tools

Session
= durable event/state log
~~~

이 구조에서는 sandbox가 죽어도 재생성할 수 있고 harness가 죽어도 session log로 복구할 수 있다.

## 책의 중요한 후보 메시지

> Long-running Agent의 핵심은 context window를 크게 만드는 것이 아니라, 작업 상태를 model context 밖에서도 잃지 않게 만드는 것이다.

## 설계 원칙 후보

1. Harness는 versioned software component로 다룬다.
2. Harness 변경은 benchmark와 regression eval로 검증한다.
3. Runtime은 disposable하게 만들 수 있어야 한다.
4. Session state는 process lifetime과 분리한다.
5. 장기 작업은 incremental artifact를 남긴다.
6. stronger model이 나오면 scaffold를 다시 감사한다.
