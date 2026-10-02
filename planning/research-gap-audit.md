# Research Coverage Gap Audit

기준일: 2026-10-02

## 목적

1~3차 조사 결과가 concept/scope를 고정하기에 충분한지 확인하고, 남은 공백을 "집필 전 필수"와 "집필 중 보강"으로 나눈다.

## 현재 충분히 확보된 영역

### Agent Loop / Harness
근거:
- OpenAI Agents SDK
- Anthropic Building Effective Agents
- Anthropic Harness studies
- Google ADK
- SWE-agent

판단:
- concept 작성에 충분
- 제품별 API 추가 수집은 불필요

### Context
근거:
- Anthropic Context Engineering
- OpenAI session/memory 자료
- long-running harness 자료

판단:
- 핵심 원칙 확정 가능

### State / Memory Taxonomy
근거:
- OpenAI Session / Goal / Memory
- LangGraph checkpoint/store
- Temporal durable execution
- OSWorld 2.0
- AgentCore runtime lifecycle

판단:
- 책의 독자적 중심 축으로 발전시킬 수 있음
- 실제 schema 사례는 집필 중 보강

### Tool / ACI
근거:
- SWE-agent
- Anthropic Tool Engineering
- MCP
- A2A

판단:
- 충분

### Runtime / Sandbox
근거:
- Anthropic sandbox
- gVisor
- Firecracker
- AgentCore
- OpenShell

판단:
- 원칙 설명에 충분
- 내부 kernel 상세는 범위 밖

### Identity / Authorization
근거:
- AWS AgentCore Identity
- Microsoft Entra Agent ID
- OBO flow
- OpenShell credential gateway
- A2A authorization

판단:
- 핵심 구조 설명에 충분

### Security / Memory Poisoning
근거:
- AgentDojo
- Microsoft memory safety
- MPBench
- MemSecBench
- MemPoison
- MemSentry

판단:
- 핵심 논점 확보

### Eval / Benchmark
근거:
- OpenAI Agent Evals / Trace Grading
- Anthropic Evals / Infra Noise
- OSWorld
- tau/tau2-bench

판단:
- 충분

## 집필 전 추가 확인이 필요한 영역

### 1. Agent State Plane 구현 비교

현재 개념 근거는 충분하지만 실제 구현 형태가 여러 가지다.

추가 후보:
- OpenAI session storage internals 공개 범위
- LangGraph checkpoint schema
- Temporal event history semantics
- managed agent session log implementations

필요도: 중간

목적:
책에서 특정 DB/event sourcing 구현을 과도하게 표준처럼 제시하지 않도록 비교.

### 2. Memory Repair / Lineage

Poisoning과 write gate 자료는 충분하지만 실제 selective repair 구현은 초기 단계다.

필요도: 낮음~중간

목적:
본문에서는 원칙만 다루고 구현 세부는 Advanced Topic으로 남길 수 있음.

### 3. Risk Scoring

R0~R4는 현재 synthesis에서 만든 설명 모델이다.

필요도: 중간

주의:
공식 표준인 것처럼 쓰면 안 됨.

책에서는 illustrative model이라고 명시한다.

### 4. Identity Propagation across MCP/A2A

현재 identity와 protocol 각각의 자료는 충분하다.

하지만 end-to-end user delegation propagation은 빠르게 변하는 영역이다.

필요도: 중간

대응:
본문에서는 원칙 중심, protocol syntax는 appendix/research로 분리.

### 5. State Reconciliation Benchmark

OSWorld 2.0이 강한 근거를 제공하지만 reconciliation 자체를 isolated capability로 측정하는 benchmark는 더 조사할 가치가 있다.

필요도: 낮음

집필 중 targeted research로 충분.

## 현재 불필요한 추가 수집

- Agent framework 기능표 대량 수집
- 모든 MCP server 사례
- 모든 Multi-Agent framework 비교
- vector DB 제품 비교
- 모든 sandbox 제품 benchmark
- LLM leaderboard 수집
- prompt engineering 사례집

이들은 책의 중심 개념을 더 선명하게 하지 않는다.

## Source Balance

현재 source 유형:

- Vendor official engineering docs: 충분
- Open protocol specs: 충분
- Academic papers: 충분
- Benchmarks: 충분
- Production failure studies: 중상
- Independent operational postmortem: 상대적으로 부족

보강 가치가 가장 높은 자료는 새로운 framework 소개가 아니라 실제 production incident / failure / recovery 사례다.

## 현재 판단

Concept와 Scope를 고정하기에는 충분한 evidence가 모였다.

남은 gap은 대부분:

- 특정 구현 선택
- 수치
- 최신 protocol syntax
- advanced security

에 해당한다.

따라서 Research Phase를 무기한 계속하지 않는다.

~~~text
Broad Research
→ 종료 가능

Targeted Research
→ 집필 중 필요할 때 수행
~~~

## 다음 단계

1. Terminology 고정
2. Chapter candidate clustering
3. TOC 설계
4. 각 장별 evidence map 작성
5. Draft 시작 전 source gap 재확인
