# Phase 7 Line Review — Part VI~VII + Epilogue

기준일: 2026-10-02
대상:
- chapters/18/draft.md
- chapters/19/draft.md
- chapters/20/draft.md
- chapters/21/draft.md
- chapters/22/draft.md
- chapters/23/draft.md
- chapters/24/draft.md
- chapters/25/draft.md
- chapters/epilogue/draft.md

## 결과

PASS.

## 주요 수정

### 18장
- Agent State Plane Event History와 Observability Trace의 목적 차이 명시
- Trace를 private reasoning 저장량과 동일시하지 않도록 표현 수정

### 19장
- pass@k / pass^k 식은 직관용이며 benchmark마다 정확한 정의를 확인해야 한다고 명시
- Benchmark Score를 Model 단독 점수가 아니라 Agent system 결과로 표현

### 20장
- Eval CI의 범위를 Agent behavior regression gate로 한정
- Software Factory의 delivery pipeline 설명과 중복되지 않게 정리

### 21장
- hypothetical ablation 수치 제거
- Anthropic AAR harness ablation을 suggestive case로 한정
- single-run condition과 run-to-run variance 한계를 본문에 반영

### 22장
- Multi-Agent가 complexity를 제거하는 것이 아니라 새로운 boundary를 추가한다는 표현으로 보정
- Agent 수와 maturity를 분리

### 23장
- Agent-as-Tool / Handoff를 framework-independent conceptual pattern으로 명시
- Handoff 시 receiving Agent authorization 재평가 필요성 강화

### 24장
- A2A 최신 공식 spec 0.3.0의 TaskState 목록 반영
- protocol version에 따라 exact states가 달라질 수 있음을 명시
- Remote Agent interoperability 범위를 discovery / message / task / artifact 중심으로 정리

### 25장
- "Capability Maturity" 제목을 "확장 순서의 한 예"로 변경
- 제시 순서가 공식 maturity model이나 단일 권장 순서가 아님을 강화

### Epilogue
- 22·25장과 겹치는 Multi-Agent 문단 제거
- 결론부 반복 표현 압축

## 핵심 경계

~~~text
Event History ≠ Observability Trace
Eval ≠ Final Output Score
Eval CI ≠ Delivery Pipeline
Harness Component ≠ Permanent Requirement
Single-Agent ≠ Low Maturity
Agent-as-Tool ≠ Handoff
Remote Agent ≠ Tool
MCP Task ≠ A2A Task ≠ Factory Task
~~~

## 다음 단계

전체 Manuscript 단위:
1. Terminology Review
2. Cross-chapter Deduplication
3. Evidence / Citation Map 정리
4. Publication-time Freshness checklist 통합
5. Manuscript Assembly
