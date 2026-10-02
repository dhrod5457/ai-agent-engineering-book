# State and Memory Taxonomy

기준일: 2026-10-02

## 왜 다시 나누어야 하는가

1차 조사에서는 Context / State / Memory를 구분했다.

2차 조사에서는 이 구분만으로도 부족하다는 점이 확인됐다. 실제 Agent SDK와 Runtime은 서로 다른 수명과 책임을 가진 상태를 별도 자원으로 관리한다.

## 제안 taxonomy

~~~text
Inference Context
= 현재 한 번의 model inference에 들어가는 정보

Conversation / Session State
= 여러 turn을 이어가기 위한 message/event history

Run State
= 현재 실행의 interruption, approval, retry, current agent 등

Workspace State
= filesystem, installed package, browser state, generated file 등 실행환경의 상태

Goal / Task State
= 완료 조건, progress, budget, lifecycle 등 작업 목표의 durable state

Artifact State
= 검증하거나 전달할 결과물

Long-term Memory
= 미래 run에 재사용할 압축된 경험, preference, lesson

External Source of Truth
= DB, repository, issue, external record처럼 Agent가 소유하지 않는 canonical state
~~~

## OpenAI에서 확인되는 분리

OpenAI Agents SDK는 Session memory를 conversation history persistence로 다룬다.

반면 Sandbox Agent의 Memory는 미래 run이 이전 run의 lesson을 재사용하기 위한 별도 capability다.

즉:

~~~text
Session
≠ Long-term Memory
~~~

Sandbox Memory는 summary와 index를 먼저 제공하고 필요한 경우 과거 rollout을 progressive하게 조회한다.

또 stale memory가 존재할 수 있으므로 memory보다 current environment를 우선하도록 설계한다.

이 점은 Memory를 canonical source가 아니라 advisory cache로 보는 근거가 된다.

## Workspace State

Agent Runtime의 sandbox는 파일과 process state를 session 동안 유지할 수 있다.

AWS AgentCore의 기본 microVM compute state는 ephemeral이다. 다만 2026-10-02 기준 managed session storage를 구성하면 stop/resume 사이에 filesystem을 durable storage에서 복원할 수 있다. 이 storage는 per-session이며 idle expiry와 runtime version update 같은 lifecycle 제약이 있다.

따라서 Workspace persistence를 지원하는 Runtime이라도 Goal/Approval/Long-term Memory 같은 Durable State와 동일한 개념으로 보지 않는다.

따라서:

~~~text
Workspace Persistence
≠ Durable Memory
≠ Durable Task State
~~~

## Goal State

Codex Goals 사례는 task objective를 일반 conversation memory와 별도 thread-scoped state로 둔다.

Goal은 다음을 가진다.

- objective
- lifecycle
- budget
- progress
- completion condition
- evidence requirement

중요한 점은 Goal이 global memory가 아니라 current thread에 붙는 completion contract라는 점이다.

## External Source of Truth

OSWorld 2.0의 실패 사례에서 Agent는 late message, approval, spreadsheet, hidden record 등 외부 source를 오래된 internal state보다 다시 확인해야 했다.

장기 Agent는 다음 패턴을 가져야 한다.

~~~text
Internal Working State
        ↓
Before irreversible action
        ↓
Reconcile with External Source of Truth
        ↓
Execute
        ↓
Verify actual outcome
~~~

## State Promotion

모든 상태를 durable하게 저장할 필요는 없다.

추천 단계:

~~~text
Ephemeral Observation
→ Working State
→ Checkpoint-worthy State
→ Durable Artifact / Goal State
→ Optional Long-term Memory
~~~

Promotion 기준 후보:

- 다음 session에서 반드시 필요
- recovery에 필요
- audit에 필요
- completion 판단에 필요
- expensive to reconstruct
- user correction을 보존해야 함

## State Invalidity

상태는 존재 여부뿐 아니라 freshness가 중요하다.

각 state에는 가능한 한 다음 metadata가 필요하다.

- scope
- owner
- created_at
- updated_at
- source
- freshness / version
- confidence
- invalidation condition

## 설계 원칙

1. Context, Session, Workspace, Goal, Artifact, Memory를 분리한다.
2. Runtime session을 durable state로 오해하지 않는다.
3. Memory는 current source보다 우선하지 않는다.
4. Irreversible action 전에는 authoritative source를 재검증한다.
5. Long-running Agent에는 explicit Goal/Progress state가 필요하다.
6. 모든 상태를 context에 넣지 말고 필요한 projection만 넣는다.

## 주요 근거

- OpenAI Agents SDK Sessions
- OpenAI Sandbox Agent Memory
- OpenAI Codex Goals
- AWS AgentCore Runtime Sessions
- Google ADK Session/Event model
- OSWorld 2.0
