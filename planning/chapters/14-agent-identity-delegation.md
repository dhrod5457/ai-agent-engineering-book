# 14장. Agent Identity와 Delegation

## Goal
독자가 Human, Application, Agent, Tool, Resource identity를 분리하고 delegated/autonomous access 모델을 설계할 수 있게 한다.

## Core Claims
- Agent는 별도 security principal로 다룰 가치가 있다.
- Delegated access와 Autonomous access는 credential 모델이 다르다.
- Capability discovery는 authorization이 아니다.
- audit에는 actor chain이 남아야 한다.

## Reader Questions
- Agent는 사용자의 identity를 그대로 쓰면 되는가?
- autonomous maintenance agent는 누구의 권한으로 움직이는가?
- remote Agent가 capability를 광고하면 바로 호출할 수 있는가?

## Flow
1. shared service account의 한계
2. identity taxonomy
3. delegated mode
4. autonomous mode
5. actor chain
6. agent lifecycle / sponsor
7. A2A에서 identity

## Example / Figure
- User → App → Agent → Tool → Resource actor chain
- Figure: Delegated vs Autonomous

## Evidence
- research/topics/10-agent-identity-authorization.md
- research/topics/19-delegated-agent-identity-zero-trust.md
- Microsoft Entra Agent ID
- AWS AgentCore Identity

## Avoid
- IAM 제품 전체 비교
- OAuth/OIDC 전체 교과서

## Draft Exit Criteria
- actor chain이 명확하다.
- credential 장으로 넘어갈 경계가 분명하다.
