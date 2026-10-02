# Part IV Structural Review

기준일: 2026-10-02
대상:
- chapters/12/draft.md
- chapters/13/draft.md

## Part IV의 역할

Part IV는 Memory를 두 질문으로 분리한다.

~~~text
12장
Memory는 무엇이며 언제 써야 하는가?
        ↓
13장
누가 무엇을 어떤 조건에서 Memory에 써도 되는가?
~~~

## 12장 검토

핵심 역할:
- Session / Checkpoint / Memory / Source of Truth 경계
- Memory Scope / Freshness / Retrieval
- Memory가 필요한 경우와 필요하지 않은 경우
- Memory를 Source of Truth로 사용하지 않기

좋은 점:
- Part III State Plane의 Recovery State와 Memory를 분리한다.
- Vector DB 중심 설명으로 빠지지 않는다.
- Retrieval을 relevance 외에도 scope/freshness/provenance 관점에서 본다.

주의:
- Memory가 항상 optional이라는 표현은 제품 요구에 따라 달라질 수 있으므로 절대 명제로 쓰지 않는다.
- Repository convention 예시는 canonical source가 존재할 때 refresh rule을 유지한다.

결론: PASS.

## 13장 검토

핵심 역할:
- Persistent Memory Write = privileged side effect
- Poisoning / compositional attack / dormant trigger
- Provenance / Scope / Privacy / Contradiction
- Accept / Review / Quarantine
- Retrieval-time policy
- Forget / Repair / Lineage / Audit

좋은 점:
- Memory Security를 Prompt Injection의 하위 절로 축소하지 않는다.
- Write와 Retrieval을 모두 security decision으로 본다.
- Agent가 Summary했다고 source trust가 올라가는 것이 아니라는 경계가 명확하다.

주의:
- 최근 Memory Security 연구는 빠르게 변하는 영역이므로 출간 직전 재검증 대상이다.
- Memory Lineage는 모든 시스템의 필수 구현처럼 표현하지 않고 high-risk case에서 유용한 선택지로 유지한다.

결론: PASS.

## 장 간 중복

### 12장 ↔ 13장
Scope, Freshness, Source of Truth가 양쪽에 등장한다.

역할:
- 12장: Memory의 lifecycle과 사용 경계
- 13장: Memory write/retrieval security enforcement

중복이 아니라 use semantics와 write authority를 나누는 구조다.

### 13장 ↔ Part V Security
Prompt Injection, Authorization이 일부 예고된다.

13장은 Memory-specific security만 다룬다.
Identity, Credential, Sandbox, Risk Policy는 Part V에 남긴다.

## Part IV 핵심 경계

~~~text
Session ≠ Memory
Checkpoint ≠ Memory
Memory ≠ Source of Truth
Observation ≠ Trusted Memory
Stored ≠ Valid Forever
Retrieved ≠ Authorized to Use
~~~

## 분량

현재 문자 수:
- 12장 약 6.6k
- 13장 약 7.1k

균형은 양호하다.

## Structural Review 결론

PASS.

Part IV Draft는 완료 상태로 둘 수 있다.

다음 작업:
1. Part V 14~17장 Draft
2. Identity / Credential / Sandbox / Policy 경계 유지
3. 17장에 targeted research의 risk-tiered approval 근거 반영
4. Part V Structural Review
