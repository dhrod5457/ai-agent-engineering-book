# Coding Agent Harness Comparison

기준일: 2026-10-02

## 목적

Claude Code, Codex, SWE-agent 등 제품의 우열을 비교하려는 문서가 아니다.

서로 다른 Coding Agent 구현에서 반복되는 Harness 구성요소를 찾는다.

## 공통 최소 구조

~~~text
Repository / Workspace
        ↓
Instruction Loading
        ↓
Context Discovery
        ↓
Agent Loop
        ↓
File / Shell / Search Tools
        ↓
Build / Test / Validation
        ↓
Result / Artifact
~~~

하지만 production-grade coding harness는 여기에 다음을 더한다.

- sandbox / permission
- task or goal state
- compaction / memory
- retry / continuation
- verification
- trace
- subagent / delegation
- budget / stop condition

## Claude Code 계열에서 확인되는 패턴

### Repository-aware execution

Agent가 repository를 탐색하고 파일을 수정하고 shell command를 실행한다.

### Permission + Sandbox

기존 permission prompt 외에 filesystem/network sandbox를 사용하여 allowed boundary 안에서는 자율 실행을 늘린다.

### Auto Mode

2026 Auto Mode는 모든 action을 human에게 묻는 대신:

- safe allow rule
- prompt injection probe
- action classifier
- recursive subagent gate

등으로 approval을 자동화한다.

이는 permission system도 harness component임을 보여준다.

### Long-running Harness

Anthropic의 장기 application 연구는:

- initializer
- incremental worker
- progress artifact
- test-driven completion

패턴을 사용한다.

### Harness Ablation

강한 model이 나오면 과거 scaffold가 오히려 성능을 제한할 수 있으므로 harness component를 제거하며 측정해야 한다는 접근이 중요하다.

## Codex 계열에서 확인되는 패턴

### Goal

Goal은 thread-scoped completion contract다.

- measurable outcome
- verification surface
- constraints
- budget
- blocked condition
- lifecycle

단순 prompt 반복이 아니라 durable objective를 Harness state로 올린 것이다.

### Evidence-driven Continuation

Goal이 active하더라도:

- thread idle
- no pending user input
- within budget
- continuation allowed

일 때만 다음 turn을 시작한다.

completion 역시 concrete evidence로 판정한다.

### Development Workflow as Artifacts

OpenAI의 Codex workflow 자료는 AGENTS.md 외에도 goal/plan/context/harness artifact를 분리하는 방향을 보여준다.

## SWE-agent에서 확인되는 패턴

SWE-agent 연구의 핵심은 ACI, 즉 Agent-Computer Interface다.

- repository navigation
- file edit
- search
- command execution

을 model이 쓰기 좋은 action space로 설계하면 성능이 달라진다.

이는 coding harness가 단순 prompt wrapper가 아니라 interface design 문제임을 보여준다.

## 공통점

~~~text
Coding Agent Capability
=
Model
+ Repository Legibility
+ Instruction
+ ACI / Tool Surface
+ Harness Loop
+ Runtime
+ Verification
+ State
~~~

## 중요한 차이 축

제품/구현 비교는 feature count보다 다음 축으로 해야 한다.

### Context
- repository map
- progressive discovery
- compaction
- memory

### Action Interface
- shell 중심
- structured file tools
- editor abstraction
- browser/computer

### State
- one-shot
- session
- goal
- checkpoint
- long-term memory

### Safety
- prompt permission
- allowlist
- classifier
- sandbox
- credential gateway

### Verification
- self-report
- command result
- test
- artifact verifier
- goal evidence

### Continuation
- user-driven
- automatic retry
- goal-driven
- event-driven
- multi-session

## Harness Smell

다음은 나쁜 harness 징후 후보다.

- 지나치게 긴 static instruction
- 모든 tool을 항상 context에 노출
- model이 이미 잘하는 일을 rigid planner가 강제
- completion을 self-report로 판정
- workspace state와 task state를 구분하지 않음
- retry마다 전체 context 재주입
- permission prompt를 security architecture로 착각
- model upgrade 후 scaffold 재검증 안 함

## 책에 반영할 원칙

1. Coding Agent를 제품별 command 목록으로 설명하지 않는다.
2. Harness를 versioned software로 본다.
3. ACI/tool surface를 model과 독립적으로 평가한다.
4. Goal/Task state를 conversation과 분리한다.
5. Verification은 Harness의 핵심 책임이다.
6. model upgrade 시 harness ablation을 수행한다.
7. autonomy 향상은 permission 제거가 아니라 stronger boundary와 함께 간다.

## 주요 근거

- Anthropic Claude Code Sandboxing
- Anthropic Claude Code Auto Mode
- Anthropic Long-running Harness
- Anthropic Harness Design
- OpenAI Codex Goals
- OpenAI Codex development workflow cookbook
- SWE-agent ACI paper
