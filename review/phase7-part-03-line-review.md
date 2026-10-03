# Phase 7 Line Review — Part III

기준일: 2026-10-02
대상:
- chapters/07/draft.md
- chapters/08/draft.md
- chapters/09/draft.md
- chapters/10/draft.md
- chapters/11/draft.md

## 결과

PASS.

## 주요 수정

### 7장
- Goal / Task State를 Goal State로 단순화
- State taxonomy를 공식 표준이 아닌 working model로 명시
- Memory와 recovery state의 경계 표현 보정
- State Promotion을 이 책의 설명용 표현으로 명시

### 8장
- "최소 구성"을 "Reference 구성"으로 수정
- Agent State Plane 구성요소가 필수 Table/Service 목록으로 읽히지 않게 보정
- Conversation History ⊂ Execution History 식 제거
- Agent State Plane이 이 책의 synthesis임을 다시 명시

### 9장
- Retry와 Recovery 관계 정밀화
- Model replay를 재생성보다 recorded result 기반 recovery로 표현
- exactly-once를 Agent Harness 단독으로 보장할 수 있다는 오해 제거

### 10장
- Phase Budget의 임의 비율 제거
- Task-State Horizon을 2026년 preprint의 emerging concept로 명시
- OSWorld 2.0 설명 제목을 중립적으로 수정

### 11장
- Selective Revalidation을 2026-09 preprint로 명시
- controlled feasibility와 production generality를 구분
- Task-State Horizon도 preprint 상태를 명확히 표시
- 결론부 반복 문장 압축

## 유지한 핵심 경계

~~~text
Context ≠ Durable State
Session ≠ Goal
Workspace ≠ Checkpoint
Memory ≠ Source of Truth
Retry ≠ Recovery
Replay ≠ Side-effect Re-execution
Version Conflict ≠ Decision Conflict
Agent State Plane ≠ Factory Control Plane
~~~

## 다음 대상

Part IV~V.

우선 검토:
- Memory와 State Plane 중복
- Memory security 연구의 주장 강도
- Identity / Credential / Sandbox / Policy의 표기와 역할 중복
- R0~R4를 표준 taxonomy로 오해할 수 있는 표현
