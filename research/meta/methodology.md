# Research Methodology

기준일: 2026-10-02

## 1. 출처 우선순위

우선순위는 다음과 같다.

1. 제품 및 프로토콜 공식 문서
2. 실제 운영 경험을 공개한 Engineering 문서
3. peer-reviewed paper 또는 원 논문
4. benchmark 공식 저장소와 평가 프로토콜
5. 신뢰할 수 있는 2차 해설

블로그 요약만 남기지 않고 가능하면 원문까지 읽는다.

## 2. 링크만 수집하지 않는다

각 자료는 최소한 다음을 기록한다.

- Source
- Date / Version
- 어떤 시스템을 관찰했는가
- 반복해서 나타나는 설계 요소
- 실패 또는 제약
- 책에서 사용할 수 있는 Engineering Principle
- 다른 출처와 충돌하거나 달라지는 부분

## 3. 제품 기능과 일반 원칙을 분리한다

예:

~~~text
OpenAI Agents SDK의 특정 API
        ↓
제품 기능

Agent loop가
Model → Tool → Observation → Model
형태로 반복된다는 구조
        ↓
일반 원칙 후보
~~~

하나의 Vendor 구현을 곧바로 표준 구조로 일반화하지 않는다.

## 4. 시간에 민감한 정보

다음은 기준일을 반드시 붙인다.

- 제품 API
- SDK 구조
- MCP / A2A specification
- benchmark leaderboard
- 보안 권고
- 모델별 성능 수치

제품 문법은 책의 핵심 논리와 분리한다.

## 5. 평가 근거

Agent benchmark는 단일 점수만 가져오지 않는다.

함께 본다.

- task definition
- environment
- tool surface
- runtime resource
- time / step limit
- grader
- success criterion
- variance / repeated trials
- infrastructure noise

Agentic evaluation은 runtime 자체가 결과에 영향을 주므로 모델 점수와 Agent System 성능을 동일시하지 않는다.

## 6. 현재 가설

조사를 통해 검증할 초기 가설:

1. Model Capability와 Agent Capability는 다르다.
2. Agent Capability는 Harness와 Tool Interface의 영향을 크게 받는다.
3. Context는 많이 넣을수록 좋은 자원이 아니라 제한된 attention budget이다.
4. Tool은 API wrapper가 아니라 Agent-Computer Interface다.
5. Long-running 작업에서는 context보다 외부 state와 artifact가 중요해진다.
6. Safety는 prompt-only가 아니라 runtime containment와 least privilege가 필요하다.
7. Agent 품질은 final answer뿐 아니라 trajectory와 outcome을 함께 평가해야 한다.
8. Multi-agent는 기본값이 아니라 복잡성 증가를 정당화할 때만 사용한다.
