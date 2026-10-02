# 17장. Risk-adaptive Policy

## Goal
독자가 Task risk에 따라 Sandbox, Credential, Approval, Verifier를 다르게 적용하는 policy model을 설계할 수 있게 한다.

## Core Claims
- 모든 Agent action에 같은 approval/sandbox를 적용하는 것은 비효율적이다.
- Authorization, Containment, Approval은 서로 다른 control이다.
- Policy는 prompt보다 deterministic enforcement에 가까워야 한다.
- Agent는 권한 확대를 제안할 수 있지만 스스로 적용하면 안 된다.

## Reader Questions
- 어떤 action은 자동화하고 어떤 action은 승인받아야 하는가?
- read와 write 외에 risk를 무엇으로 판단해야 하는가?
- deny가 반복될 때 Agent 권한을 자동으로 넓혀도 되는가?

## Flow
1. approval fatigue vs over-privilege
2. risk dimensions
3. R0~R4 illustrative model
4. policy as code
5. fail closed
6. policy expansion lifecycle
7. independent verifier / rollback
8. policy manifest

## Example / Figure
- repository read, PR create, production deploy의 policy 차이
- Figure: Risk → Runtime/Credential/Approval matrix

## Evidence
- research/topics/20-risk-adaptive-containment-policy.md
- NVIDIA OpenShell policy
- Claude Code Auto Mode

## Targeted Research Before Draft
- NIST/OWASP/enterprise agent risk taxonomy와 현재 illustrative model 비교
- risk-adaptive authorization 최신 production 사례 추가
- high-impact action approval fatigue 관련 근거 추가

## Avoid
- R0~R4를 외부 표준처럼 표현
- 법률/규제 compliance 전체

## Draft Exit Criteria
- risk model이 illustrative synthesis임을 명시한다.
- 실제 control mapping이 구체적이다.
