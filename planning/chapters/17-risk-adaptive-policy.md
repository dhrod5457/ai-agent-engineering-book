# 17장. Risk-adaptive Policy

## Goal
독자가 Task risk와 identity context에 따라 Sandbox, Credential, Tool Scope, Approval, Verifier를 다르게 적용하는 policy model을 설계할 수 있게 한다.

## Core Claims
- 모든 Agent action에 같은 approval/sandbox를 적용하는 것은 비효율적이다.
- Authorization, Containment, Approval은 서로 다른 control이다.
- Human approval은 high-risk action에 risk-tiered하게 적용해야 한다.
- Tool authorization은 model 밖 gateway에서 강제해야 한다.
- Originating user authorization은 delegation chain을 따라 유지돼야 한다.
- Agent는 권한 확대를 제안할 수 있지만 스스로 적용하면 안 된다.

## Reader Questions
- 어떤 action은 자동화하고 어떤 action은 승인받아야 하는가?
- read와 write 외에 risk를 무엇으로 판단해야 하는가?
- reviewer에게 어떤 context를 보여줘야 하는가?
- deny가 반복될 때 Agent 권한을 자동으로 넓혀도 되는가?

## Flow
1. approval fatigue vs over-privilege
2. risk dimensions
3. originating user / agent / resource context
4. R0~R4 illustrative control profile
5. external tool authorization
6. temporary / JIT privilege
7. policy as code
8. fail closed
9. policy expansion lifecycle
10. independent verifier / rollback
11. policy manifest

## Example / Figure
- repository read, PR create, production deploy의 policy 차이
- Figure: Risk Inputs → External Policy Evaluation → Runtime / Tool / Credential / Approval Profile

## Evidence
- research/topics/20-risk-adaptive-containment-policy.md
- research/targeted/17-risk-adaptive-policy.md
- AWS Agentic AI Lens: tool authorization / HITL / dynamic boundaries
- AWS Cedar multi-agent authorization
- NVIDIA OpenShell policy
- Claude Code Auto Mode

## Avoid
- R0~R4를 외부 표준처럼 표현
- 법률/규제 compliance 전체
- model self-judgment을 authorization source로 사용

## Draft Exit Criteria
- risk model이 illustrative synthesis임을 명시한다.
- originating user와 Agent identity가 policy input에 포함된다.
- reviewer fatigue를 줄이는 risk-tiered approval 구조가 구체적이다.
