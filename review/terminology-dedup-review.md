# Terminology and Cross-chapter Deduplication Review

기준일: 2026-10-02

## 상태

PASS.

전체 25장 + Epilogue의 Line Review 이후, 핵심 용어 표기와 반복 설명을 다시 점검했다.

## Canonical Terminology

정의된 Architecture 개념은 영문 Title Case를 유지한다.

- Agent
- Model
- Harness
- Context
- Tool
- State
- Memory
- Runtime
- Sandbox
- Trace
- Eval
- Goal
- Artifact
- Identity
- Authorization
- Approval
- Completion
- Side Effect
- Long-running
- MCP
- A2A

고유 synthesis는 정확한 이름을 유지한다.

- Agent State Plane
- Harness Debt
- Memory Write Gate
- AgentVersion
- Factory Control Plane

일반 서술에서 production은 가능한 한 "운영"으로 쓴다.

예외:
- Minimum Viable Production Agent
- Production Readiness Checklist
- Production DB / Production Cluster 같은 예시 label
- environment == "production" 같은 literal value
- source title / quoted phrase

## 적용한 Terminology 수정

- 1장 production 서술 → 운영 환경
- 6·24장 long-running capability invocation → Long-running Capability Invocation
- 9·20장 duplicate side effect → 중복/duplicate Side Effect
- 19장 Long-running → Long-running Task
- 25장 일반 서술의 Production Agent → 운영 Agent

## Deduplication 적용

### 1장 → 8장
1장의 Agent State Plane preview를 압축했다.

1장에는:
- one-agent execution continuity
- Context와 Durable State의 차이
- Part III 예고

만 남겼다.

Event History / Checkpoint / Projection 상세는 8장에 둔다.

### 3장 → 21장
3장의 Harness Ablation 절차를 축소했다.

3장:
- Model upgrade가 Harness audit trigger라는 원칙

21장:
- repeated trials
- variance
- capability/security slices
- component record
- debt removal

로 역할을 분리했다.

### 6장 → 14·17장
MCP 장의 Authorization 설명을 preview 수준으로 줄였다.

6장:
- Discovery ≠ Authorization
- Protocol auth 이후에도 application policy가 남음

14·17장:
- Actor Chain
- Delegation
- Tool Authorization
- Approval
- Risk-adaptive Policy

를 상세히 다룬다.

### 7·11장 → 12장
Memory ≠ Source of Truth 설명을 압축했다.

7장:
- taxonomy / authority rule

11장:
- reconciliation에서 current source 우선

12장:
- Memory lifecycle, freshness, retrieval, Source of Truth 관계의 상세 설명

으로 나눴다.

## 의도적으로 유지한 반복

다음 문장은 책의 spine이므로 여러 Part에서 반복을 허용한다.

~~~text
Model Capability ≠ Agent Capability
Context ≠ Durable State
Memory ≠ Source of Truth
Sandbox ≠ Authorization
Completion Claim ≠ Completion Authority
Agent State Plane ≠ Factory Control Plane
~~~

동일 문장을 반복하더라도 주변 설명 문단은 각 장의 책임에 맞게 다르게 유지한다.

## 다음 Review

1. Evidence / Citation Review
2. Publication-time Freshness Audit
3. Manuscript Assembly
