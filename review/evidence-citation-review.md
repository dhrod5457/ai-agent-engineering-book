# Evidence / Citation Review

기준일: 2026-10-02
대상: 25개 본장 + Epilogue

## 상태

PASS with freshness follow-up.

모든 본장은 최소 하나 이상의 공식 문서, protocol spec, primary research, engineering case 또는 명시적 book synthesis에 연결돼 있다.

출판 전 남은 문제는 "근거 부재"보다 "최신 상태 재검증"이다.

## Source Type 기준

~~~text
O  Official / Protocol
V  Vendor Engineering / Production Case
R  Research / Benchmark
P  Preprint / Emerging Research
S  Book Synthesis
~~~

## Chapter Classification

### Part I

1장 Model과 Agent
- O: OpenAI Agents SDK
- V: Anthropic Building Effective Agents / Managed Agents
- R: SWE-agent
- S: Agent Capability decomposition
- 상태: PASS

2장 Agent Loop
- O: OpenAI Running Agents / Google ADK
- R: ReAct
- 상태: PASS

3장 Harness Engineering
- V: Anthropic Harness / Managed Agents
- S: Harness Debt
- 상태: PASS

### Part II

4장 Context
- V: Anthropic Context Engineering
- O: OpenAI Session/Memory docs
- 상태: PASS

5장 Tool / ACI
- R: SWE-agent ACI
- V: Anthropic Tool Engineering
- 상태: PASS

6장 MCP
- O: MCP 2026-07-28 spec/release
- S: Protocol Task vs Domain Task boundary
- 상태: PASS, freshness required

### Part III

7장 State Taxonomy
- O/V: OpenAI / AWS / Google state implementations
- S: combined taxonomy
- 상태: PASS

8장 Agent State Plane
- O/V: Temporal / LangGraph / Agent SDK patterns
- S: Agent State Plane
- 상태: PASS
- 주의: 외부 표준명처럼 표현하지 않음

9장 Recovery / Replay
- O/V: Temporal Durable Execution / Managed Agents
- 상태: PASS

10장 Long-running Agent
- V: Anthropic long-running harness
- R: OSWorld 2.0
- P: Task-State Horizon 일부
- 상태: PASS

11장 Reconciliation
- R: OSWorld 2.0
- P: Selective Revalidation / Task-State Horizon / AgentRewind
- S: source registry / authority model integration
- 상태: PASS with preprint wording
- 조치: 본문에 preprint 표시 반영 완료

### Part IV

12장 Memory Boundary
- O: OpenAI Sandbox Memory
- S: memory lifecycle boundary
- 상태: PASS

13장 Memory Write Security
- V/O: Microsoft memory safety guidance
- P: MPBench / MemSecBench / MemPoison / MemSentry
- S: Memory Write Gate
- 상태: PASS
- 출간 전 preprint status 재확인 필요

### Part V

14장 Identity / Delegation
- O/V: Microsoft Entra Agent ID / AWS AgentCore Identity
- S: actor-chain presentation
- 상태: PASS, freshness required

15장 Credential Boundary
- O/V: Microsoft OBO / AWS / NVIDIA OpenShell
- 상태: PASS, freshness required

16장 Sandbox
- O/V: gVisor / Firecracker / AgentCore / Anthropic / OpenShell
- 상태: PASS
- 제품별 현재 구현은 freshness audit 대상

17장 Risk-adaptive Policy
- V/O: AWS Agentic AI Lens / Cedar / OpenShell / Claude Code Auto Mode
- S: R0~R4 illustrative control profile
- 상태: PASS
- 조치: vendor guidance임을 본문에 명시 완료

### Part VI

18장 Trace
- O: OpenAI Trace Grading / Agent Evals
- 상태: PASS

19장 Eval
- O/V/R: OpenAI / Anthropic / OSWorld / tau2
- 상태: PASS

20장 Eval CI
- O/V: OpenAI Agent Improvement Loop / Macro Evals
- S: AgentVersion tuple
- 상태: PASS

21장 Harness Ablation
- V/R: Anthropic harness experiments / AuditBench
- S: Harness Debt operations
- 상태: PASS
- 조치: run-to-run variance observation 범위를 본문에 명시 완료

### Part VII

22장 Single-Agent First
- V: Anthropic Building Effective Agents
- S: decision framework
- 상태: PASS

23장 Agent-as-Tool / Handoff
- O: OpenAI Agents SDK / Google ADK
- 상태: PASS

24장 A2A
- O: A2A Specification / MCP comparison
- 상태: PASS, freshness required

25장 Minimum Viable Production Agent
- S: whole-book synthesis
- evidence: prior 24 chapters
- 상태: PASS

Epilogue
- S: book thesis summary
- 상태: PASS

## Claim-strength Corrections Applied

### 11장
"최근 연구"를 "2026년 preprint"로 명시.
Selective Revalidation과 Task-State Horizon을 emerging research로 제한.

### 17장
AWS Agentic AI Lens를 vendor guidance로 명시.
업계 표준처럼 읽히는 표현 제거.

### 21장
Anthropic harness ablation의 run-to-run variance를 해당 실험 조건의 관찰로 제한.

## Publication-time Freshness Required

High priority:
1. MCP specification / Tasks extension
2. A2A specification
3. OpenAI Agents SDK Session / Memory / Goals
4. Microsoft Entra Agent ID
5. AWS AgentCore / Agentic AI Lens
6. NVIDIA OpenShell
7. Claude Code Sandbox / Auto Mode
8. OSWorld 2.0
9. tau2-bench
10. 2026 Memory Security preprints

## Citation Assembly Rule

Manuscript Assembly에서 각 장의 "주요 근거" 목록을 그대로 최종 참고문헌으로 사용하지 않는다.

다음 순서로 변환한다.

~~~text
Claim
→ Source Type
→ Primary Source
→ Scope / Limitation
→ Source Note ID
→ Chapter Reference
~~~

## 결론

Evidence Coverage: PASS.

다음 Phase:
- Publication-time Freshness Audit
- Manuscript Assembly
