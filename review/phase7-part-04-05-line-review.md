# Phase 7 Line Review — Part IV~V

기준일: 2026-10-02
대상:
- chapters/12/draft.md
- chapters/13/draft.md
- chapters/14/draft.md
- chapters/15/draft.md
- chapters/16/draft.md
- chapters/17/draft.md

## 결과

PASS.

## 주요 수정

### 12장
- 변하기 쉬운 project fact를 "Long-term Relationship Context"로 부르던 표현 수정
- Memory progressive retrieval을 특정 vendor 기능이 아닌 일반 pattern으로 설명
- Memory가 항상 Agent Capability를 높인다는 인상을 제거

### 13장
- Memory poisoning을 2026년 preprint와 Microsoft guidance의 관찰로 한정
- MemPoison의 compositional / dormant attack 결과를 write-time defense 한계의 근거로 명시
- Accept / Review / Quarantine은 이 책의 설명용 policy model임을 명시

### 14장
- Microsoft Entra Agent ID를 agent identity의 한 구현 사례로 한정
- Entra의 special service principal model을 업계 표준으로 일반화하지 않도록 보정

### 15장
- Credential Gateway 구조를 권고안이 아니라 검토 가능한 기본 pattern으로 완화
- 특정 제품 기능을 architecture requirement로 오해하지 않도록 유지

### 16장
- OS Sandbox → Container → gVisor → MicroVM 도식을 절대적 보안 등급처럼 읽히지 않도록 수정
- isolation technology를 threat model과 운영 trade-off에 따라 선택하도록 정리
- Claude Code sandbox 구현 설명을 공식 Anthropic 공개 내용 수준으로 보정

### 17장
- risk classification을 같은 untrusted input에 노출된 Model 판단만으로 결정하지 않도록 명시
- Agent-driven policy change를 OpenShell의 한 사례로 한정
- Human Review를 영향과 판단 비용이 큰 action에 집중하도록 표현

## 핵심 경계

~~~text
Session ≠ Memory
Checkpoint ≠ Memory
Memory ≠ Source of Truth
Observation ≠ Trusted Memory

User Identity ≠ Agent Identity
Identity ≠ Credential
Credential Scope ≠ Sandbox
Sandbox ≠ Authorization
Authorization ≠ Approval
Policy Manifest ≠ Policy Authority
~~~

## 다음 대상

Part VI~VII + Epilogue.

우선 검토:
- Trace / Event History 중복
- Eval / Eval CI 중복
- Harness Ablation의 예시 수치
- Agent-as-Tool / Handoff를 제품별 고정 semantics로 오해할 표현
- A2A protocol 최신성
- 25장과 Epilogue 결론 중복
