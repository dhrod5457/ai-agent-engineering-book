# Long-horizon Computer-use Agents

기준일: 2026-10-02

## OSWorld 2.0이 바꾼 질문

OSWorld 1.x는 GUI grounding과 app operation 능력을 강하게 드러냈다.

OSWorld 2.0은 더 긴 실제 업무를 넣으면서 다른 병목을 보여준다.

- 108 long-horizon tasks
- human median operation time 약 1.6시간
- 69.6%가 숙련 사용자 기준 1시간 이상
- 평균 수백 회의 tool/action
- 여러 app과 source를 넘나드는 workflow

이제 핵심 실패는 단순 click accuracy가 아니다.

## 반복적으로 드러난 challenge

OSWorld 2.0은 다음 현상을 별도 challenge로 추적한다.

- Cross-source Reasoning
- Visual-spatial Precision
- Implicit-state Inference
- Multi-item State Tracking
- Conflict Disambiguation
- Multimodal Editing
- Tutorial Following
- Dynamic Environment
- Streaming Interaction
- Proactive Interaction

Agent Engineering 관점에서 특히 중요한 것은 다음 네 가지다.

### 1. Implicit-state Inference

Task instruction에 모든 상태가 들어 있지 않다.

Agent는 이전 submission, log, message, saved record 등에서 현재 필요한 state를 복구해야 한다.

### 2. Multi-item State Tracking

장기 task에서는 수십 개 item의 상태를 동시에 보존해야 한다.

LLM conversation memory만으로 관리하면 omission과 stale state가 발생하기 쉽다.

### 3. Dynamic Environment

실행 중 새 email/message가 도착해 requirement나 source of truth가 바뀔 수 있다.

처음 만든 plan과 snapshot을 고정하면 실패한다.

### 4. Conflict Disambiguation

여러 source가 서로 충돌할 때 authoritative source를 판단하고 stale information을 버려야 한다.

## 대표 Failure Pattern 1: Internal Story Becomes Source of Truth

구매요청 사례에서 Agent는 late approval을 관찰했지만 전체 table을 다시 reconcile하지 않았다.

결과적으로 final verification도 실제 source가 아니라 자신이 만든 incomplete internal list에 맞춰 수행했다.

이를 일반화하면:

~~~text
Observe partial state
→ Build internal model
→ New evidence arrives
→ Local patch only
→ Internal model becomes stale
→ Verify against stale internal model
→ False completion
~~~

대책:

- authoritative source registry
- refresh policy
- reconciliation step
- completeness invariant
- pre-commit/pre-submit revalidation

## 대표 Failure Pattern 2: Artifact Existence Replaces Correctness

CAD 사례에서 output file이 존재한다는 사실이 geometry가 맞다는 검증을 대체했다.

~~~text
Artifact Exists
≠ Artifact Correct
~~~

Agent에게 output format만 요구하면 proxy success에 수렴할 수 있다.

따라서 task-specific verifier가 필요하다.

## 대표 Failure Pattern 3: Preparation Consumes the Horizon

Reimbursement 사례에서는 evidence gathering과 tooling detour가 길어져 실제 target workflow가 step budget 후반에 시작됐다.

대책 후보:

- phase budget
- critical path
- progress checkpoint
- action deadline
- search budget
- target-system-first milestone

## Long-horizon Harness에 필요한 것

~~~text
Goal
  ↓
Milestone Plan
  ↓
Working State Table
  ↓
Source Registry
  ↓
Action
  ↓
Refresh / Reconcile
  ↓
Checkpoint
  ↓
Outcome Verification
  ↺
~~~

추가해야 할 control:

- horizon budget
- phase budget
- stale-state detection
- refresh trigger
- milestone timeout
- blocker escalation
- user clarification trigger
- verification reserve

## Proactive Clarification

장기 업무에서는 불확실한 값을 임의 추정하는 것보다 사용자에게 확인하는 것이 정답일 수 있다.

따라서 autonomy가 높을수록:

~~~text
Act autonomously
+
Know when not to act
~~~

가 함께 필요하다.

## 책에 반영할 핵심 메시지

> Long-horizon Agent의 가장 어려운 문제는 더 오래 reasoning하는 것이 아니라, 변화하는 외부 세계와 내부 작업 상태를 계속 reconcile하면서 목표와 검증 기준을 잃지 않는 것이다.

## 주요 근거

- OSWorld 2.0
- OSWorld Verified
- Anthropic Long-running Harness
- OpenAI Codex Goals
