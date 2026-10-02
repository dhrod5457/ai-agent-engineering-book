# Phase 7 Evidence / Citation Review

기준일: 2026-10-02
브랜치: review/phase7-line-edit

## 결과

PASS.

## 완료 작업

- planning/chapter-evidence-map.md → reviewed manuscript 기준 v2로 재작성
- planning/source-note-conventions.md → reviewed terminology와 일치하도록 수정
- planning/source-catalog.md → stable internal source id 정의
- chapter-level 주요 claim을 Evidence Class로 분류

## Evidence Class

~~~text
[O] Official / Protocol
[V] Vendor Engineering / Production Case
[R] Research / Benchmark
[P] Preprint / Emerging Research
[B] Book Synthesis
~~~

## 핵심 원칙

### Protocol Fact
version/date를 명시하고 publication-time freshness audit 대상에 둔다.

### Vendor Case
"업계가 이렇게 한다"가 아니라 "해당 공개 사례에서는 이렇게 구현했다" 수준으로 표현한다.

### Research
task/environment/benchmark 범위를 벗어나 일반화하지 않는다.

### Preprint
preprint 상태와 limitation을 본문에서 숨기지 않는다.

### Book Synthesis
외부 source가 직접 이름 붙인 개념처럼 표현하지 않는다.

현재 주요 synthesis:
- Agent State Plane
- Harness Debt
- Memory Write Gate
- AgentVersion
- R0~R4 control profile
- Agent-as-Tool / Handoff ownership distinction
- Agent State Plane / Factory Control Plane boundary

## Evidence Gap

현재 필수 신규 Research Gap은 없음.

출간 전 재검증 대상:
- MCP base revision / Tasks lifecycle
- A2A version / TaskState
- OSWorld 2.0 revision
- Selective Revalidation preprint status
- Task-State Horizon preprint status
- AgentRewind status
- Memory-security preprints
- Entra Agent ID product/lifecycle naming
- Claude Code sandbox implementation
- AWS Agentic AI Lens wording
- OpenShell behavior
- OpenAI / Anthropic eval product naming

## 다음 단계

Manuscript Assembly에서:
1. chapter-level "주요 근거"를 source id로 변환
2. claim-level source note 삽입
3. 장 끝 References 생성
4. bibliography/source appendix 생성
5. freshness marker가 있는 source는 publication-time gate와 연결

현재 Evidence / Citation Review 단계는 완료로 본다.
