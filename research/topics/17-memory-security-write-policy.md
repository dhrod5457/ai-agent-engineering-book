# Memory Security and Write Policy

기준일: 2026-10-02

## 핵심 질문

> Agent가 무엇을 기억할 수 있는가보다, 누가 어떤 정보를 어떤 조건에서 장기 기억으로 승격할 수 있는가가 더 중요하지 않은가?

3차 조사에서는 이 질문에 대한 근거가 강하게 확인됐다.

Persistent Memory는 단순한 편의 기능이 아니라 미래 Agent 행동에 영향을 주는 보안 경계다.

## Memory Poisoning의 구조

일반적인 공격 흐름:

~~~text
Untrusted Input
    ↓
Agent interprets as useful information
    ↓
Persistent Memory Write
    ↓
Original context disappears
    ↓
Later Retrieval
    ↓
Future Decision / Tool Call
    ↓
Persistent Consequence
~~~

일회성 prompt injection과 달리 공격 영향이 session을 넘어 지속될 수 있다.

2026년 연구들은 memory poisoning을 단순 입력 필터링 문제로 보기 어렵다는 점을 반복해서 보여준다.

## 최근 연구에서 확인된 점

### MPBench

From Untrusted Input to Trusted Memory 연구는:

- 여러 memory write channel
- 구조적 취약점
- 다양한 poisoning class

를 분리했다.

특히 memory를 적극적으로 쓰고 적극적으로 retrieve하는 Agent일수록 공격 표면이 커질 수 있음을 보였다.

핵심:

> More Memory != Safer or Better Agent

### MemSecBench

MemSecBench는 poisoning을 lifecycle 전체로 추적한다.

~~~text
Write
→ Persist
→ Retrieve
→ Execute
→ Consequence
→ Forget / Repair
~~~

중요한 점은 단순히 malicious record가 저장됐는지만 보지 않고 실제 downstream behavior와 selective repair까지 측정한다는 것이다.

### MemPoison

2026년 MemPoison은 write-time consistency check만으로는 compositional attack과 dormant trigger를 충분히 막기 어렵다고 보고한다.

즉:

~~~text
Safe-looking Memory A
+
Safe-looking Memory B
+
Specific Context
=
Unsafe Combined Behavior
~~~

가 가능하다.

따라서 Memory Security는 write-time filter 하나로 끝나지 않는다.

## Memory Write는 Side Effect다

Agent가 장기 기억에 쓰는 행위는 다음 run의 행동을 바꾼다.

따라서 memory.write는 일반 log append가 아니라 privileged side effect로 봐야 한다.

추천 구조:

~~~text
Observation
    ↓
Memory Candidate
    ↓
Provenance Check
    ↓
Scope Check
    ↓
Security / Privacy Classification
    ↓
Contradiction Check
    ↓
Write Policy
    ├─ Accept
    ├─ Review
    └─ Quarantine
    ↓
Versioned Memory Store
~~~

## Write Policy에 필요한 정보

Memory candidate metadata 후보:

- source
- source trust
- originating user / agent
- timestamp
- session / task
- target scope
- expected lifetime
- sensitivity
- confidence
- contradiction set
- write reason
- model / harness version
- approval state

Memory content와 provenance를 분리하지 않는다.

## Memory Scope

장기 기억은 최소한 다음 scope를 구분해야 한다.

~~~text
User-private
Team / Organization
Repository / Project
Task-specific
Agent-specific
Global
~~~

가능한 한 가장 좁은 scope로 저장한다.

Task에서만 필요한 내용을 Global Memory로 승격하면 cross-task contamination 위험이 생긴다.

## Retrieval도 Security Decision이다

안전한 write만으로 충분하지 않다.

retrieval 시점에도 다음을 평가해야 한다.

- 현재 task와 관련 있는가
- source가 아직 valid한가
- 더 최신 canonical source가 있는가
- sensitivity가 현재 principal에게 허용되는가
- 서로 충돌하는 memory가 있는가
- 현재 context에서 결합될 때 위험해지는가

따라서:

~~~text
Memory Read
≠ Blind Vector Similarity Search
~~~

이다.

## Memory와 Source of Truth

Memory는 외부 사실을 복제한 cache가 될 수 있지만 canonical source를 대체하면 안 된다.

예:

~~~text
Memory:
"프로덕션 DB는 db-prod-1이다"

Current Infra Source:
"db-prod-2로 전환됨"
~~~

irreversible action 전에 external source를 재검증해야 한다.

## Forget / Repair

Memory system에는 write와 read뿐 아니라 다음 lifecycle이 필요하다.

- expire
- invalidate
- supersede
- quarantine
- delete
- repair
- rollback
- provenance trace

Poisoned memory 하나를 삭제하더라도 그 memory로부터 파생된 secondary memory가 남을 수 있다.

따라서 repair는 record 단위 삭제보다 lineage-aware 방식이 필요할 수 있다.

## Audit

Microsoft의 2026 memory safety guidance는 memory CRUD에 provenance를 남기고 poisoning, leakage, cross-context risk를 별도 운영 지표로 관리하는 방향을 제시한다.

Memory operation은 first-class security event로 본다.

감사 이벤트 후보:

~~~text
memory.proposed
memory.accepted
memory.rejected
memory.quarantined
memory.retrieved
memory.superseded
memory.deleted
memory.repaired
~~~

## 책에 반영할 핵심 원칙

1. Persistent Memory Write는 privileged side effect다.
2. Memory에는 provenance와 scope가 필수다.
3. Write-time filtering만으로 충분하지 않다.
4. Retrieval도 authorization / trust decision이다.
5. Memory는 canonical source가 아니다.
6. Cross-memory composition risk를 고려한다.
7. Forgetting과 selective repair를 설계한다.
8. Memory CRUD를 audit event로 남긴다.
9. 자동 memory write는 default allow보다 gated write가 안전하다.

## 주요 근거

- Microsoft Security — Guarding AI memory
- Microsoft Zero Trust — Manage AI memory safety in agentic systems
- From Untrusted Input to Trusted Memory: MPBench
- MemSecBench
- MemPoison
- MemSentry
- OWASP AISVS Memory and Embeddings research
