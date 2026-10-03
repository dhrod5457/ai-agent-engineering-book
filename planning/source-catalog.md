# Source Catalog

기준일: 2026-10-02

Manuscript Assembly에서 claim-level source note에 사용할 stable source id를 정의한다.

ID는 source의 영구 identifier가 아니라 이 저장소 내부 reference다.

## Agent / Harness

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-REACT | R | ReAct | Agent loop / observation-action |
| S-SWE-ACI | R | SWE-agent, Agent-Computer Interfaces | Tool / ACI |
| S-OAI-AGENTS | V | OpenAI Agents SDK / Running Agents | Agent loop, session, trace, eval |
| S-ANTHROPIC-AGENTS | V | Anthropic, Building Effective Agents | simple agent / multi-agent boundary |
| S-ANTHROPIC-HARNESS | V | Anthropic long-running harness material | long-running, harness, progress |
| S-ANTHROPIC-MANAGED | V | Anthropic managed agent material | harness/runtime/state boundary |
| S-GOOGLE-ADK | V | Google Agent Development Kit | loop / session / handoff |

## Context / Protocol

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-ANTHROPIC-CONTEXT | V | Anthropic Context Engineering | context selection / progressive context |
| S-ANTHROPIC-TOOLS | V | Anthropic Tool Engineering | tool naming / schema / result contract |
| S-MCP-2026-07 | O | Model Context Protocol 2026-07-28 | MCP base protocol |
| S-MCP-TASKS-DRAFT | O | MCP Tasks extension, 2026-07-28 Draft | long-running capability invocation |
| S-A2A-0.3 | O | A2A Protocol 0.3.0 | remote agent interoperability |

Freshness:
- S-MCP-2026-07 / S-MCP-TASKS-DRAFT → review/freshness/mcp-2026-10-02.md
- S-A2A-0.3 → review/freshness/a2a-2026-10-02.md

## Durable State / Long-running

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-TEMPORAL | R | Temporal Durable Execution / replay semantics | event history / replay / recovery |
| S-LANGGRAPH-PERSIST | V | LangGraph Persistence | checkpoint / state implementation example |
| S-AWS-AGENTCORE-RUNTIME | V | AWS AgentCore Runtime | runtime/session isolation example |
| S-OSWORLD2 | P | OSWorld 2.0 | long-horizon dynamic state |
| S-SELECTIVE-REVALIDATION | P | From Version Conflicts to Decision Conflicts | decision conflict / selective revalidation |
| S-TSH | P | Task-State Horizon | state dependency horizon |
| S-AGENTREWIND | P | AgentRewind | checkpoint-aligned agent recovery |

Freshness:
- review/freshness/long-running-2026-10-02.md

## Memory Security

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-MS-MEMORY | V | Microsoft, Guarding AI Memory | persistent memory safety |
| S-MPBENCH | P | MPBench | memory poisoning evaluation |
| S-MEMSECBENCH | P | MemSecBench | memory security evaluation |
| S-MEMPOISON | P | MemPoison | compositional / dormant memory attacks |
| S-MEMSENTRY | P | MemSentry | memory defense / repair |

Freshness:
- review/freshness/security-2026-10-02.md

## Identity / Credential / Sandbox / Policy

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-ENTRA-AGENT-ID | V | Microsoft Entra Agent ID | agent identity / delegated vs autonomous |
| S-MS-OBO | V | Microsoft On-Behalf-Of flow | delegated credential |
| S-AWS-AGENTCORE-ID | V | AWS AgentCore Identity | workload identity / credential |
| S-CLAUDE-SANDBOX | V | Anthropic Claude Code Sandboxing | filesystem/network containment |
| S-GVISOR | V | gVisor security architecture | userspace-kernel isolation example |
| S-FIRECRACKER | V | Firecracker | microVM isolation example |
| S-OPENSHELL | V | NVIDIA OpenShell | gateway / policy / credential injection |
| S-AWS-AGENTIC-LENS | V | AWS Agentic AI Lens | risk-tiered approval / authorization |
| S-AWS-CEDAR | V | AWS Cedar agent authorization examples | external authorization policy |

Freshness:
- review/freshness/security-2026-10-02.md

## Trace / Eval / Improvement

| ID | Class | Source | Primary use |
| --- | --- | --- | --- |
| S-OAI-EVALS | V | OpenAI Agent Evals / Trace Grading | trace / trajectory eval |
| S-ANTHROPIC-EVALS | V | Anthropic Agent Eval guidance | eval methodology |
| S-ANTHROPIC-INFRA-NOISE | V | Anthropic agentic eval infrastructure analysis | runtime noise |
| S-TAU | R | tau-bench | agent reliability |
| S-TAU2 | R | tau2-bench | benchmark / grader revision |
| S-ANTHROPIC-AAR | V | Anthropic Automated Alignment Researchers | harness ablation / variance |

## Book Synthesis IDs

Book synthesis에는 외부 citation id 대신 B-* id를 사용해 source fact와 저자의 framework를 분리한다.

| ID | Concept |
| --- | --- |
| B-AGENT-CAPABILITY | Model Capability ≠ Agent Capability |
| B-STATE-PLANE | Agent State Plane |
| B-CONTEXT-PROJECTION | Durable State → Context Projection |
| B-MEMORY-WRITE-GATE | Memory Write Gate |
| B-RISK-PROFILE | R0~R4 illustrative control profile |
| B-AGENT-VERSION | AgentVersion |
| B-HARNESS-DEBT | Harness Debt |
| B-OWNERSHIP | Agent-as-Tool / Handoff ownership distinction |
| B-FACTORY-BOUNDARY | Agent State Plane ≠ Factory Control Plane |

## Citation Strength

~~~text
O
Protocol / official fact
→ direct factual source note

R
Established research / benchmark
→ task/environment scope note

V
Vendor engineering / production case
→ "사례/구현/관찰" language

P
Preprint / emerging research
→ explicit preprint marker + limitation

B
Book synthesis
→ "이 책에서는 ..." language
~~~

## Publication-time Gate

출간 직전에 반드시 재검증:
- O: protocol version / lifecycle
- V: product / feature / architecture naming
- P: revision / peer-review / benchmark corrections

다시 검증할 필요가 상대적으로 적은 것:
- B: framework wording 자체
- established software patterns such as idempotency / optimistic concurrency

단, B concept이 외부 표준처럼 변형되지 않았는지는 전체 manuscript에서 다시 검사한다.
