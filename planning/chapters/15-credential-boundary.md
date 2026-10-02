# 15장. Credential을 Agent에서 분리한다

## Goal
독자가 raw credential을 Agent context/runtime에 장기 노출하지 않고 gateway 기반 최소권한 접근을 설계할 수 있게 한다.

## Core Claims
- Agent가 standing broad credential을 직접 보유하는 것은 blast radius를 키운다.
- action 시점의 short-lived credential injection이 더 안전한 기본값이다.
- Tool별 credential scope 분리가 유용하다.
- runtime isolation이 강해도 credential scope가 넓으면 위험하다.

## Reader Questions
- 환경변수에 API key를 넣어두면 왜 부족한가?
- User delegation token과 workload token을 어떻게 나눠야 하는가?
- Tool마다 별도 identity가 필요한가?

## Flow
1. credential exposure
2. credential broker / gateway
3. delegated token exchange
4. autonomous workload token
5. tool identity
6. short-lived / scoped token
7. audit / revocation

## Example / Figure
- Agent intent → AuthZ Gateway → token injection → external API
- Figure: credential-free Agent runtime

## Evidence
- research/topics/19-delegated-agent-identity-zero-trust.md
- Microsoft OBO
- AWS AgentCore Identity
- NVIDIA OpenShell

## Avoid
- OAuth grant type 세부 구현
- secret manager 제품 비교

## Draft Exit Criteria
- credential boundary architecture가 재사용 가능한 형태로 제시된다.
