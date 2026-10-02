# Source Catalog

기준일: 2026-10-02

1차 리서치에서 원문을 확인한 핵심 자료다.

## A. Agent Runtime / Harness

### OpenAI — Agents SDK
- URL: https://developers.openai.com/api/docs/guides/agents/sdk
- 유형: 공식 문서
- 확인점:
  - Agent를 model, instructions, tools, guardrails, MCP, handoff 등의 구성으로 정의
  - SDK runner가 agent loop와 handoff를 실행
  - deployment, storage, approval, runtime integration은 application이 소유할 수 있음
- 중요성: Agent와 application runtime의 책임 분리를 보여준다.

### OpenAI — Running agents
- URL: https://developers.openai.com/api/docs/guides/agents/running-agents
- 유형: 공식 문서
- 확인점:
  - model 호출
  - tool call 실행
  - handoff 처리
  - final output까지 반복
- 중요성: Agent loop의 최소 실행 구조를 명시적으로 보여준다.

### Anthropic — Building effective agents
- URL: https://www.anthropic.com/engineering/building-effective-agents
- 게시: 2024-12-19
- 확인점:
  - 복잡한 framework보다 단순하고 조합 가능한 pattern을 우선
  - workflow와 agent를 구분
  - complexity는 필요할 때 증가
- 중요성: Multi-agent와 orchestration을 기본값으로 두지 않는 근거.

### Anthropic — Effective harnesses for long-running agents
- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 게시: 2025-11-26
- 확인점:
  - context window를 넘는 장기 작업에서 session 간 continuity가 문제
  - initializer + incremental coding session
  - 다음 session이 이어받을 artifact를 남김
  - compaction만으로는 충분하지 않음
- 중요성: long-running agent의 핵심을 외부 상태와 handoff artifact 관점으로 본다.

### Anthropic — Harness design for long-running application development
- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 게시: 2026-03-24
- 확인점:
  - harness가 성능을 크게 바꿀 수 있음
  - 강한 모델일수록 과도한 scaffolding이 오래된 가정이 될 수 있음
  - component ablation으로 load-bearing harness를 찾아야 함
- 중요성: Harness 자체도 평가와 감량 대상임을 보여준다.

### Anthropic — Scaling Managed Agents: Decoupling the brain from the hands
- URL: https://www.anthropic.com/engineering/managed-agents
- 게시: 2026-04-08
- 확인점:
  - brain(harness/model), hands(sandbox/tools), session(event log)을 분리
  - sandbox와 harness를 각각 교체 가능한 구성으로 설계
  - session log를 외부화하여 crash recovery를 단순화
- 중요성: Harness / Runtime / State를 분리해야 하는 운영 근거.

## B. Context / State

### Anthropic — Effective context engineering for AI agents
- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 게시: 2025-09-29
- 확인점:
  - context는 finite attention budget
  - system prompt, tools, examples, history, external data를 전체 context로 취급
  - high-signal minimal context를 지향
  - long-running loop에서 context는 지속적으로 재구성해야 함
- 중요성: Prompt Engineering보다 넓은 Context Engineering의 경계.

## C. Tools / Protocols

### Anthropic — Writing effective tools for agents
- URL: https://www.anthropic.com/engineering/writing-tools-for-agents
- 게시: 2025-09-11
- 확인점:
  - tool 구현 여부부터 평가해야 함
  - 명확한 namespace와 기능 경계가 중요
  - agent eval을 통해 tool description과 interface를 개선
- 중요성: Tool을 단순 API wrapper가 아니라 Agent Interface로 봄.

### SWE-agent — Agent-Computer Interfaces Enable Automated Software Engineering
- URL: https://arxiv.org/abs/2405.15793
- 게시: 2024
- 확인점:
  - Agent-Computer Interface 설계가 coding agent 성능을 크게 좌우
  - repository 탐색, 파일 편집, test 실행 interface를 agent에 맞게 설계
- 중요성: Model 성능과 Interface 성능을 분리하는 핵심 근거.

### Model Context Protocol 2026-07-28
- URL: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- 버전: 2026-07-28
- 확인점:
  - stateless protocol core
  - cacheable list results
  - authorization hardening
  - extensions framework
  - Tasks 등 확장
- 중요성: Tool/Context 연결을 Agent 내부 구현과 분리하는 표준화 흐름.

### Agent2Agent Protocol Specification
- URL: https://a2aproject.github.io/A2A/latest/specification/
- 확인점:
  - independent agent 간 capability discovery와 interaction
  - Message / Task / Artifact를 분리
  - remote agent 내부 memory/tools를 노출하지 않고 협업
- 중요성: Tool protocol(MCP)과 Agent-to-Agent protocol의 경계.

### Google Agent Development Kit
- URL: https://google.github.io/adk-docs/
- 확인점:
  - agents, tools, session/state, memory, eval, deployment를 별도 관심사로 제공
  - code execution은 sandbox runtime과 persistent session state를 분리하여 제공 가능
- 중요성: 여러 vendor 구현에서 반복되는 구성요소 확인.

## D. Security

### OpenAI — Guardrails and human review
- URL: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- 확인점:
  - input/output/tool guardrail 분리
  - side-effect tool은 approval interruption과 resumable state 사용
  - validation을 side effect가 발생하는 tool boundary 가까이에 배치
- 중요성: Agent-level prompt와 Tool-level enforcement의 차이.

### Anthropic — How we contain Claude across products
- URL: https://www.anthropic.com/engineering/how-we-contain-claude
- 게시: 2026-05-25
- 확인점:
  - model defense만으로는 충분하지 않음
  - environment containment, filesystem/network boundary, egress control
  - external tool output 자체가 prompt injection surface
  - human approval fatigue 문제
- 중요성: deterministic containment가 probabilistic model safety를 보완해야 함.

### AgentDojo
- URL: https://arxiv.org/abs/2406.13352
- 게시: NeurIPS 2024
- 확인점:
  - untrusted tool data를 통한 prompt injection을 동적 환경에서 평가
  - utility와 security를 동시에 측정
- 중요성: Agent security를 정적 prompt test가 아니라 tool-using environment에서 평가.

## E. Evaluation / Observability

### OpenAI — Evaluate agent workflows
- URL: https://developers.openai.com/api/docs/guides/agent-evals
- 확인점:
  - trace → grader → dataset → repeatable eval
  - tool choice, handoff, policy violation 등 workflow 행동을 평가
- 중요성: final answer만 평가하는 방식의 한계.

### OpenAI — Trace grading
- URL: https://developers.openai.com/api/docs/guides/trace-grading
- 확인점:
  - model calls, tool calls, orchestration trajectory를 구조적으로 평가
- 중요성: trajectory evaluation 근거.

### Anthropic — Demystifying evals for AI agents
- URL: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 게시: 2026-01-09
- 확인점:
  - multi-turn agent eval은 task, tools, environment, grader를 함께 정의
  - code grader, model grader, human grader를 조합
  - 초기 20~50개의 실제 실패 사례로 시작 가능
- 중요성: eval-driven agent development 근거.

### Anthropic — Quantifying infrastructure noise in agentic coding evals
- URL: https://www.anthropic.com/engineering/infrastructure-noise
- 게시: 2026-02-05
- 확인점:
  - CPU/RAM/timeout enforcement가 benchmark score에 유의미한 영향을 줌
  - agentic eval에서 runtime은 측정 대상의 일부
- 중요성: Model benchmark와 Agent System benchmark를 분리해야 함.

## F. Agent Architecture / Learning Patterns

### ReAct
- URL: https://arxiv.org/abs/2210.03629
- 게시: ICLR 2023
- 확인점: reasoning과 action을 interleave하고 observation으로 계획을 갱신.
- 중요성: Agent loop의 고전적 기반.

### Reflexion
- URL: https://arxiv.org/abs/2303.11366
- 게시: NeurIPS 2023
- 확인점: 환경 feedback과 reflective text를 episodic memory에 유지.
- 중요성: weight update 없는 feedback/memory loop 연구.

### Toolformer
- URL: https://arxiv.org/abs/2302.04761
- 게시: 2023
- 확인점: 어떤 tool을 언제 어떤 인자로 호출하고 결과를 어떻게 사용할지 학습.
- 중요성: Tool use가 별도 capability임을 보여준다.

## G. Benchmarks

### AgentBench
- URL: https://arxiv.org/abs/2308.03688
- 확인점: 여러 interactive environment에서 장기 reasoning, decision, instruction following 실패 관찰.

### GAIA
- URL: https://arxiv.org/abs/2311.12983
- 확인점: reasoning, browsing, multimodal, tool use를 함께 요구하는 real-world assistant benchmark.

### tau-bench
- URL: https://arxiv.org/abs/2406.12045
- 확인점:
  - user interaction + domain policy + API tool을 함께 평가
  - 반복 실행 신뢰성을 pass^k로 측정
- 주의: 공식 저장소는 최신 후속 benchmark 사용을 안내하고 있으므로 수치 인용 시 최신 버전 재확인.

### OSWorld
- URL: https://arxiv.org/abs/2404.07972
- 프로젝트: https://os-world.github.io/
- 확인점:
  - 실제 desktop environment
  - execution-based evaluator
  - task initial state와 environment가 명시적
- 중요성: Computer-use Agent에서 Runtime과 Eval Environment가 핵심임을 보여준다.


## H. 2차 조사 — State / Memory / Identity

### OpenAI Agents SDK — Sessions
- URL: https://openai.github.io/openai-agents-python/sessions/
- 확인점:
  - conversation history를 run 간 유지
  - client-managed session과 server-managed continuation을 구분
- 중요성: Session을 long-term memory와 분리하는 근거.

### OpenAI Agents SDK — Sandbox Agent Memory
- URL: https://openai.github.io/openai-agents-python/sandbox/memory/
- 확인점:
  - Session memory와 Agent memory를 명시적으로 분리
  - memory summary → index → rollout detail의 progressive disclosure
  - stale memory보다 current environment를 우선
  - agent별 memory layout isolation
- 중요성: Memory를 canonical source가 아닌 reusable guidance로 보는 근거.

### OpenAI — Using Goals in Codex
- URL: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- 게시: 2026-05-09
- 확인점:
  - Goal은 persisted thread state
  - objective, lifecycle, budget, evidence-based completion
  - global memory와 분리
- 중요성: Durable objective를 conversation과 별도 state로 관리하는 사례.

### Amazon Bedrock AgentCore Identity
- URL: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html
- 확인점:
  - Agent workload identity
  - user-delegated / autonomous access
  - credential management와 audit
- 중요성: Agent principal과 user principal을 분리하는 운영 사례.

## I. 2차 조사 — Runtime / Sandbox

### AWS AgentCore Runtime — microVMs
- URL: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html
- 확인점:
  - session별 dedicated microVM
  - CPU / memory / filesystem isolation
  - runtime session state는 ephemeral
- 중요성: Runtime state와 durable memory의 분리.

### gVisor Security Architecture
- URL: https://gvisor.dev/docs/architecture_guide/intro/
- 확인점:
  - userspace application kernel
  - host kernel syscall surface 축소
  - systrap / KVM platform
- 중요성: container와 VM 사이의 isolation 선택지.

### Firecracker Design
- URL: https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md
- 확인점:
  - KVM microVM boundary
  - seccomp, cgroup, namespace, jailer
- 중요성: hardware virtualization + defense-in-depth 사례.

### NVIDIA OpenShell
- URL: https://github.com/NVIDIA/OpenShell
- 확인점:
  - supervisor와 sandbox 분리
  - kernel-level file/syscall/network policy
  - credential을 approved endpoint에서만 주입
- 중요성: Agent runtime을 policy enforcement point로 확장한 최신 사례.

### Anthropic — Claude Code Sandboxing
- URL: https://www.anthropic.com/engineering/claude-code-sandboxing
- 게시: 2025-10-20
- 확인점:
  - filesystem + network isolation
  - permission fatigue 감소
- 중요성: local coding agent에서 OS-level isolation 적용 사례.

### Anthropic — Claude Code Auto Mode
- URL: https://www.anthropic.com/engineering/claude-code-auto-mode
- 게시: 2026-03-25
- 확인점:
  - prompt injection probe
  - action classifier
  - safe allowlist
  - subagent handoff gate
- 중요성: approval을 human click에서 policy/classifier pipeline으로 옮긴 사례.

## J. 2차 조사 — Protocol Boundary

### MCP 2026-07-28 Tasks Extension
- URL: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- 확인점:
  - protocol-level session 제거
  - Tasks는 extension으로 이동
  - tasks/get, tasks/update, tasks/cancel
- 중요성: Runtime Session과 Protocol Task를 분리해야 하는 근거.

### A2A Specification — Task / Artifact / Authorization
- URL: https://a2a-protocol.org/latest/specification/
- 확인점:
  - stateful remote Agent Task
  - input-required / auth-required 포함 lifecycle
  - Artifact를 Task output으로 분리
  - server-side authorization
- 중요성: MCP Task와 remote-agent work contract의 차이.

## K. 2차 조사 — Long-horizon / Eval

### OSWorld 2.0
- URL: https://osworld-v2.xlang.ai/
- 게시: 2026-06
- 확인점:
  - 108 long-horizon workflow
  - human median 약 1.6시간
  - hidden state, multi-item tracking, dynamic environment, conflict disambiguation
  - long horizon에서 성능 급락
- 중요성: Agent 장기 실패가 단순 GUI grounding 문제가 아니라 state/reconciliation 문제임을 보여준다.

### tau2-bench 1.0.1 Changelog
- URL: https://github.com/sierra-research/tau2-bench/blob/main/CHANGELOG.md
- 게시: 2026-07
- 확인점:
  - grader 수정으로 기존 trajectory 점수가 바뀜
  - release 이전/이후 score 직접 비교 금지 안내
- 중요성: benchmark와 grader도 version pinning이 필요함.

### OpenAI — Macro Evals for Agentic Systems
- URL: https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems
- 게시: 2026-05-19
- 확인점:
  - 개별 trace 평가를 넘어 population-level recurring failure를 찾음
- 중요성: Agent Eval CI에서 micro/macro eval을 분리하는 근거.

### OpenAI — Agent Improvement Loop
- URL: https://developers.openai.com/cookbook/topic/agents
- 게시: 2026-05 계열
- 확인점:
  - trace → feedback → eval → harness change
- 중요성: production feedback을 reusable regression으로 승격하는 패턴.
