# 12장. Agent Memory의 실제 경계

## Goal
독자가 Session/Working State와 Long-term Memory를 분리하고 Memory를 언제 써야 하는지 판단할 수 있게 한다.

## Core Claims
- Memory는 execution recovery를 위한 기본 저장소가 아니다.
- Memory는 미래 run에 재사용할 knowledge/lesson을 위한 선택적 subsystem이다.
- Memory는 stale할 수 있으므로 Source of Truth보다 우선하지 않는다.
- Retrieval은 relevance뿐 아니라 freshness, authorization, provenance를 고려해야 한다.

## Reader Questions
- Session history와 Memory는 무엇이 다른가?
- 모든 경험을 기억시키면 Agent가 더 좋아지는가?
- Memory가 틀렸을 때 무엇을 믿어야 하는가?

## Flow
1. Memory가 과도하게 쓰이는 이유
2. Session / Checkpoint / Memory 비교
3. Memory scope와 lifetime
4. retrieval
5. stale memory
6. source-of-truth precedence
7. memory가 필요한 경우와 필요 없는 경우

## Example / Figure
- repository endpoint 정보를 memory에 저장했다가 실제 환경 변경으로 stale해진 사례
- Figure: Session / State / Memory / Source of Truth 관계

## Evidence
- research/topics/02-context-state-memory.md
- research/topics/09-state-memory-taxonomy.md
- OpenAI Sandbox Agent Memory

## Avoid
- Vector DB 구현
- 인간 기억 이론

## Draft Exit Criteria
- Memory 사용 여부를 판단하는 decision rule을 제공한다.
- 다음 장의 write security 필요성이 자연스럽게 이어진다.
