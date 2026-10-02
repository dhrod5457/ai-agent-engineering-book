# 4장. Context는 저장소가 아니다

## Goal
독자가 Context를 durable storage로 사용하지 않고 현재 decision을 위한 projection으로 설계할 수 있게 한다.

## Core Claims
- Context는 finite attention budget이다.
- More Context는 자동으로 Better Agent를 의미하지 않는다.
- Context는 Durable State의 projection이다.
- Compaction은 storage/recovery를 대체하지 못한다.

## Reader Questions
- 가능한 정보를 다 넣는 것이 왜 나쁜가?
- conversation history를 계속 유지하면 memory가 되는가?
- compaction만으로 long-running task가 가능한가?

## Flow
1. Context window의 잘못된 사용
2. high-signal context
3. history / retrieval / tool schema / state projection
4. progressive disclosure
5. compaction
6. stale context와 pollution
7. context assembly checklist

## Example / Figure
- 100개 tool schema를 모두 노출한 Agent vs 필요한 8개만 노출한 Agent
- Figure: State Plane → Context Projection → Inference

## Evidence
- research/topics/02-context-state-memory.md
- research/topics/09-state-memory-taxonomy.md
- Anthropic Context Engineering

## Avoid
- RAG 제품 구축
- Vector DB 비교

## Draft Exit Criteria
- Context와 State 차이를 명확히 설명한다.
- Context assembly input을 분류한다.
- Compaction의 한계를 실제 failure로 보여준다.
