# Security and Containment

## 기본 전제

Agent는 자연어를 읽고 실제 side effect를 수행한다.

따라서 공격 표면은 기존 application보다 넓다.

~~~text
User Input
External Web
Tool Result
MCP Server
Repository File
Persistent Memory
Document
Email / Message
~~~

이 모든 것이 model context를 오염시킬 수 있다.

## Model Safety와 System Safety

Anthropic containment 사례에서 가장 중요한 구분:

~~~text
Probabilistic Defense
- system prompt
- classifier
- model behavior

Deterministic Boundary
- sandbox
- filesystem mount
- network egress
- credential scope
- tool permission
- policy gate
~~~

둘 다 필요하지만 역할은 다르다.

Model이 잘 행동할 확률을 높이는 것과 잘못 행동해도 피해 범위를 제한하는 것은 다른 문제다.

## Approval의 한계

Human-in-the-loop는 중요하지만 모든 tool call에 approval을 요구하면 approval fatigue가 생긴다.

따라서:

- low-risk read
- bounded mutation
- irreversible side effect
- production access

등 risk에 따라 다르게 다뤄야 한다.

## Tool Boundary에서 검증

OpenAI의 guardrail 문서도 side effect에 가까운 위치에서 validation을 두는 구조를 강조한다.

예:

~~~text
Model proposes tool call
        ↓
Validate target / args / identity / scope
        ↓
Approval if required
        ↓
Execute in constrained runtime
        ↓
Validate / filter result
        ↓
Return observation
~~~

## Prompt Injection

AgentDojo와 production 사례가 보여주는 핵심:

- trusted tool이 반환한 데이터도 untrusted일 수 있음
- README, email, web page, issue text가 attack vector가 될 수 있음
- input text를 instruction인지 data인지 model이 항상 완벽히 구분할 수 없음

따라서 prompt injection 대책을 prompt에만 맡기면 안 된다.

## 최소 Security Architecture

1. Least privilege tool scopes
2. Isolated runtime
3. Filesystem boundary
4. Network egress control
5. Credential isolation
6. Tool argument validation
7. Sensitive action approval
8. Tool output trust labeling/filtering
9. Audit trace
10. Fail closed policy for critical boundary

## 추가 연구 질문

- Agent identity는 user principal을 그대로 상속해야 하는가.
- Agent 전용 service identity가 필요한가.
- Memory poisoning을 어떻게 탐지/정정하는가.
- MCP/A2A capability discovery와 authorization을 어떻게 결합하는가.
- approval 정책을 risk scoring과 어떻게 연결하는가.
