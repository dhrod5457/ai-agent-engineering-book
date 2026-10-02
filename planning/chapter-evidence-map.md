# Chapter Evidence Map

기준일: 2026-10-02
대상 TOC: planning/toc.md v0.1

각 장의 핵심 주장과 현재 확보된 근거를 연결한다.

## 1장. Model과 Agent는 무엇이 다른가
주요 근거:
- research/topics/01-agent-loop-runtime.md
- research/synthesis/agent-engineering-reference-model-v0.3.md
- OpenAI Agents SDK
- Anthropic Building Effective Agents

핵심 주장:
- Model Capability와 Agent Capability는 다르다.
- Agent는 실행 구조다.

## 2장. Agent Loop를 설계한다
주요 근거:
- topics/01-agent-loop-runtime.md
- ReAct
- OpenAI Running Agents
- Google ADK

## 3장. Harness Engineering
주요 근거:
- topics/04-harness-long-running.md
- topics/14-coding-agent-harness-comparison.md
- topics/22-harness-ablation-and-minimalism.md
- Anthropic Harness Design

## 4장. Context는 저장소가 아니다
주요 근거:
- topics/02-context-state-memory.md
- topics/09-state-memory-taxonomy.md
- Anthropic Context Engineering

## 5장. Tool은 Agent-Computer Interface다
주요 근거:
- topics/03-tools-protocols.md
- SWE-agent ACI
- Anthropic Tool Engineering

## 6장. MCP와 Capability Boundary
주요 근거:
- topics/03-tools-protocols.md
- topics/12-mcp-a2a-task-boundary.md
- MCP 2026-07-28

## 7장. Session, Workspace, Goal, Memory를 분리한다
주요 근거:
- topics/09-state-memory-taxonomy.md
- OpenAI Sessions
- OpenAI Sandbox Memory
- OpenAI Codex Goals
- AWS AgentCore Runtime

## 8장. Agent State Plane
주요 근거:
- synthesis/reference-model-v0.3
- topics/18-durable-state-event-log-replay.md
- Temporal
- LangGraph Persistence

주의:
- Agent State Plane은 이 책의 synthesis 용어다.
- 외부 표준 명칭처럼 표현하지 않는다.

## 9장. 실패 후 이어가는 Agent
주요 근거:
- topics/18-durable-state-event-log-replay.md
- Temporal Durable Execution
- Anthropic Managed Agents

## 10장. Long-running Agent
주요 근거:
- topics/04-harness-long-running.md
- topics/13-long-horizon-computer-use.md
- Anthropic Long-running Harness
- OSWorld 2.0

## 11장. External State Reconciliation
주요 근거:
- topics/21-external-state-reconciliation.md
- research/targeted/11-external-state-reconciliation.md
- OSWorld 2.0
- From Version Conflicts to Decision Conflicts
- Task-State Horizon research
- AgentRewind
- optimistic concurrency patterns

핵심 보강:
- version conflict와 decision conflict를 분리
- selective revalidation과 CAS/transaction commit

## 12장. Agent Memory의 실제 경계
주요 근거:
- topics/02-context-state-memory.md
- topics/09-state-memory-taxonomy.md
- OpenAI Sandbox Memory

## 13장. Memory Write는 Side Effect다
주요 근거:
- topics/17-memory-security-write-policy.md
- Microsoft Memory Safety
- MPBench
- MemSecBench
- MemPoison
- MemSentry

## 14장. Agent Identity와 Delegation
주요 근거:
- topics/10-agent-identity-authorization.md
- topics/19-delegated-agent-identity-zero-trust.md
- Microsoft Entra Agent ID
- AWS AgentCore Identity

## 15장. Credential을 Agent에서 분리한다
주요 근거:
- topics/19-delegated-agent-identity-zero-trust.md
- NVIDIA OpenShell
- Microsoft OBO
- AWS AgentCore Identity

## 16장. Sandbox와 Containment
주요 근거:
- topics/11-sandbox-runtime-isolation.md
- Claude Code Sandboxing
- gVisor
- Firecracker
- AgentCore
- OpenShell

## 17장. Risk-adaptive Policy
주요 근거:
- topics/20-risk-adaptive-containment-policy.md
- research/targeted/17-risk-adaptive-policy.md
- AWS Agentic AI Lens
- AWS Cedar multi-agent authorization
- OpenShell Policy
- Claude Code Auto Mode

주의:
- R0~R4는 illustrative synthesis이며 외부 표준이 아니다.
- risk-tiered approval, user-context propagation, external tool authorization 근거 확보.

## 18장. Trace 없이는 Agent를 디버깅할 수 없다
주요 근거:
- topics/06-evaluation-observability.md
- OpenAI Trace Grading
- OpenAI Agent Evals

## 19장. Agent를 어떻게 평가할 것인가
주요 근거:
- topics/06-evaluation-observability.md
- topics/08-benchmarks.md
- topics/16-benchmark-versioning-measurement.md
- Anthropic Evals
- Infrastructure Noise
- OSWorld
- tau2-bench

## 20장. Eval을 CI로 만든다
주요 근거:
- topics/15-eval-ci-regression.md
- OpenAI Agent Improvement Loop
- Macro Evals

## 21장. Harness Ablation과 Debt
주요 근거:
- topics/22-harness-ablation-and-minimalism.md
- research/targeted/21-harness-ablation.md
- Anthropic Harness Design
- Anthropic Managed Agents
- Automated Alignment Researchers harness ablation
- AuditBench

핵심 보강:
- repeated trials와 run-to-run variance
- capability-specific component value

## 22장. Single-Agent First
주요 근거:
- topics/07-multi-agent-interoperability.md
- Anthropic Building Effective Agents

## 23장. Agent-as-Tool과 Handoff
주요 근거:
- topics/07-multi-agent-interoperability.md
- OpenAI Agents SDK
- Google ADK

## 24장. A2A와 Remote Agent
주요 근거:
- topics/12-mcp-a2a-task-boundary.md
- A2A Specification

## 25장. Minimum Viable Production Agent
주요 근거:
- planning/concept.md
- planning/scope.md
- synthesis/reference-model-v0.3
- 전체 research synthesis

# Coverage Summary

현재 25개 장 모두 Chapter Plan과 최소 하나 이상의 1차 또는 공식 source group을 갖는다.

기존 보강 우선순위였던 11장, 17장, 21장도 targeted research를 완료했다.

현재 상태:

~~~text
Broad Research       완료
Concept              완료
Scope                완료
TOC v0.1             완료
Chapter Evidence     완료
Chapter Plan 1~25    완료
Epilogue Plan        완료
Targeted Research    11 / 17 / 21 완료
~~~

따라서 Part I부터 Draft 단계로 진입 가능하다.
