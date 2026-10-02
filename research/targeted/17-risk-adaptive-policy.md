# Targeted Research — Risk-adaptive Policy

기준일: 2026-10-02
대상: 17장 Risk-adaptive Policy

## 새로 확보한 근거

### AWS Agentic AI Lens — Human-in-the-loop for critical decisions
- Source: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html
- 핵심:
  - 모든 action을 human review에 보내면 rubber-stamp approval이 된다.
  - high-risk operation만 risk-tiered approval로 pause하는 것이 바람직하다.
  - reviewer에게 action, data source, consequence context를 제공해야 한다.

### AWS Agentic AI Lens — Tool Authorization
- Source: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec02-bp01.html
- 핵심:
  - tool invocation마다 external policy check
  - agent identity와 originating user context propagation
  - prompt-only authorization은 불충분
  - high-risk mutation은 human checkpoint

### AWS Agentic AI Lens — Dynamic Boundaries
- Source: https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec03-bp03.html
- 핵심:
  - temporary credential
  - contextual IAM condition
  - just-in-time elevated permission
  - runtime boundary를 task/data sensitivity에 따라 조정

### Multi-agent Cedar Authorization
- Source: https://aws.amazon.com/blogs/security/enforce-least-privilege-authorization-in-multi-agent-ai-chains-using-cedar/
- 핵심:
  - agent→tool
  - agent→agent delegation
  - originating user authorization
  를 별도 layer로 평가
- 의미:
  - 단일 risk score 하나보다 independent policy dimensions를 조합하는 것이 현실적

## R0~R4 모델 수정

기존 R0~R4는 유지하되 "표준 risk taxonomy"가 아니라 교육용 control profile로 명확히 표현한다.

risk 판단 입력은 단일 점수가 아니라:

~~~text
Action Risk
Resource Sensitivity
Reversibility
Originating User Authority
Agent Trust / Lifecycle
Delegation Depth
Environment
Credential Scope
~~~

의 조합으로 본다.

## 새 핵심 원칙

1. Human approval은 risk-tiered 해야 한다.
2. Approval 자체보다 reviewer context 품질이 중요하다.
3. Tool authorization은 model 밖 gateway에서 강제한다.
4. Originating user authorization을 delegation chain 끝까지 유지한다.
5. Elevated privilege는 standing permission보다 JIT/temporary 방식이 낫다.
6. Risk-adaptive policy는 "Agent가 스스로 판단"하는 구조가 아니라 external policy engine이 결정하는 구조가 기본이다.

## 17장 구조 보강

~~~text
Risk Inputs
   ↓
External Policy Evaluation
   ↓
Control Profile
   ├─ Runtime Isolation
   ├─ Tool Scope
   ├─ Credential Scope
   ├─ Approval
   └─ Independent Verification
~~~

R0~R4는 이 Control Profile의 예시로만 사용한다.
