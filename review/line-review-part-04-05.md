# Line Review — Part IV~V

기준일: 2026-10-02
대상:
- chapters/12/draft.md
- chapters/13/draft.md
- chapters/14/draft.md
- chapters/15/draft.md
- chapters/16/draft.md
- chapters/17/draft.md

## 상태

PASS.

Memory와 State, Identity와 Credential, Sandbox와 Policy의 역할을 섞지 않는 것을 우선했다. 문장 수준에서는 "실제"와 Production 표현의 불필요한 반복을 줄였다.

## Part IV

### 12장
- Production Agent → 운영 Agent
- Memory를 기본 Component처럼 보이게 할 수 있는 문장을 "필요가 확인될 때 추가"로 정리
- Memory ≠ Source of Truth 메시지는 유지

### 13장
- Production Mutation 표현을 운영 환경 수정으로 자연스럽게 정리
- "실제 이득" 등 불필요한 강조 제거
- Memory Write Gate, provenance, scope, quarantine, repair의 핵심 구조는 유지

### Part IV Dedup
- 12장: Memory의 목적과 경계
- 13장: Memory write/retrieval security
- 7/11장: State taxonomy와 source reconciliation

같은 "Memory ≠ Source of Truth" 식은 spine 역할이므로 유지하되, 세부 사례는 각 장 책임에 맞게 제한한다.

## Part V

### 14장
- "실제" 반복을 줄이고 Actor Chain 설명을 직접화
- Human / App / Agent / Tool / Resource identity 구분 유지

### 15장
- Credential Gateway 사례에서 불필요한 강조 축소
- Credential과 Runtime 접근 경계를 다음 장으로 명확하게 연결

### 16장
- "실제 File System" → "호스트 File System"
- Container 이름보다 적용된 Isolation Policy가 중요하다는 식으로 표현 정리
- Containment ≠ Authorization 메시지 유지

### 17장
- "실제 운영/Policy/Enforcement" 같은 반복을 줄임
- R0~R4는 illustrative control profile임을 유지
- Agent self-authorization 금지와 external policy enforcement를 core message로 유지

## Cross-chapter Boundary

~~~text
14장 Identity
= Who is acting?

15장 Credential
= What token/secret reaches the resource?

16장 Sandbox
= Where can the workload physically reach?

17장 Policy
= What action is allowed now, under which conditions?
~~~

이 네 질문이 중복 없이 유지된다.

## 유지할 핵심 식

~~~text
Memory ≠ Source of Truth
Discovery ≠ Authentication ≠ Authorization ≠ Approval
Sandbox ≠ Authorization
Approval ≠ Containment
Credential Scope ≠ Runtime Isolation
~~~

## 결론

Part IV~V Line Review: PASS.

다음:
1. Part VI~VII + Epilogue Line Review
2. Terminology Review
3. Cross-chapter Deduplication
