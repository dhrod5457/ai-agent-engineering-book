# 17장. Risk-adaptive Policy

도구를 호출할 때마다 사람의 승인을 받으면 안전해 보인다. 하지만 실제 운영에서는 다른 문제가 생긴다. 에이전트가 파일을 읽을 때마다 묻고, 테스트를 실행할 때마다 묻고, 이슈를 조회할 때마다 묻는다. 사용자는 결국 내용을 읽지 않고 승인을 누르기 시작한다. 반대 극단도 있다. 승인 피로를 없애려고 에이전트에 넓은 권한을 한 번 주고 모두 자동화한다. 둘 다 좋은 기본값은 아니다. 작업의 위험에 따라 **어떤 통제를 얼마나 강하게 적용할지 다르게 설계**할 필요가 있다.

## 모든 Action의 Risk는 같지 않다

다음 행동을 비교해보자.

~~~text
README 읽기
Local Test 실행
GitHub Issue Comment 작성
Production Deploy
Payment 실행
~~~

모두 도구 호출이지만 Consequence가 다르다. 위험 판단에는 여러 Dimension이 있다.

- Read vs Write
- Local vs External
- Reversible vs Irreversible
- Data Sensitivity
- Production 여부
- Financial / Legal Consequence
- 인증 정보로 행사할 수 있는 권한 범위
- Arbitrary Code Execution
- Delegation Depth

따라서 단순 "도구 사용 가능/불가능"보다 통제 수단의 조합이 필요하다.

## R0~R4 Control Profile

이 책에서는 설명을 위해 R0~R4 예시를 사용한다. 외부 표준 Risk Taxonomy가 아니다.

### R0 — Offline Read

예:

- Local Document 분석
- Static Source 읽기

통제:

- 인증 정보(Credential) 없음
- External Write 없음
- 기본 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)

### R1 — Workspace Mutation

예:

- Repository File 수정
- Local Build/Test

통제:

- Workspace Scope
- 제한된 네트워크
- Production Credential 없음
- 정해진 규칙에 따른 검증

### R2 — External Read

예:

- GitHub Read
- Internal API Read

통제:

- Read-only Credential
- Endpoint Allowlist
- 감사

### R3 — Bounded External Write

예:

- PR 생성
- Issue Comment
- Slack Message

통제:

- Scoped Credential
- Target Validation
- 멱등성(Idempotency: 같은 요청을 반복해도 결과가 중복되지 않는 성질)
- 감사
- 조건부 승인

### R4 — High-impact / Irreversible

예:

- 운영 환경 배포
- Payment
- Security Policy 변경
- Production DB Mutation

통제:

- Stronger Isolation
- Short-lived Credential
- Explicit Policy Gate
- Independent Verification
- Human/Trusted 승인
- Rollback or Compensation Plan

이 분류의 목적은 Label 자체가 아니다. 위험에 따라 통제를 다르게 조합하는 사고방식이다.

## Risk Input은 하나의 Score가 아닐 수 있다

운영 정책은 여러 입력을 함께 본다.

~~~text
Action Risk
Resource Sensitivity
Reversibility
Originating User Authority
Agent Identity
Delegation Scope
Environment
Credential Scope
~~~

예를 들어 같은 add_comment 도구라도:

~~~text
public issue comment
vs
student disciplinary record comment
~~~

는 위험이 다를 수 있다. Tool Name만으로 위험을 결정하지 않는다.

## External Policy Evaluation

모델이 "이 행동은 안전하다"고 판단한 결과를 최종 권한 확인(Authorization)으로 사용하지 않는다. 특히 모델이 같은 untrusted input에 노출돼 있다면 risk classification 자체도 시스템이 정해진 규칙으로 적용하는 정책을 거쳐야 한다.

추천 구조:

~~~text
Agent proposes Action
        ↓
External Policy Engine
        ↓
Evaluate:
- user
- agent
- tool
- resource
- environment
- risk
        ↓
Control Profile
~~~

통제 수단의 조합은 다음을 결정할 수 있다.

- Allow/Deny
- Runtime Isolation
- 인증 정보로 행사할 수 있는 권한 범위
- 승인
- 검증 담당자
- Logging

## Human Approval은 Risk-tiered하게

AWS가 공개한 Agentic AI Lens에서는 모든 행동을 사람의 검토에 보내는 방식이 Approval Fatigue와 Rubber-stamp Review를 만들 수 있다고 지적한다. 이는 vendor guidance이며 업계 공통 표준으로 해석하지 않는다. 사람의 검토는 다음과 같이 판단 비용과 영향이 큰 행동에 집중하는 편이 낫다.

- High-impact
- Irreversible
- Sensitive Data
- Ambiguous Authority
- Policy Exception

Read-only Low-risk Action까지 같은 수준의 승인을 요구하면 Human Attention을 소모한다.

## Reviewer Context

Approval UI에는 "승인하시겠습니까?"만 보여주면 부족하다. 검토 담당자가 판단할 컨텍스트(Context: 모델에 전달하는 정보)가 필요하다.

예:

~~~text
Action:
Deploy release 1.4.2

Target:
production / cluster-a

Changes:
commit abc123 → def456

Verification:
integration pass
security scan pass

Rollback:
release 1.4.1

Requested by:
agent deploy-7 on behalf of user-10
~~~

Approval Quality는 검토 담당자에게 제공되는 근거 품질에 영향을 받는다.

## Originating User Authorization

Agent Chain이 길어져도 사용자 권한을 유지해야 한다.

~~~text
User
  ↓
Agent A
  ↓
Agent B
  ↓
Tool
~~~

에이전트 B의 Service Credential이 사용자보다 넓다고 해서 넓은 접근 대상 자원에 접근하게 두지 않는다. 정책은 Originating User와 Current Agent를 함께 볼 수 있다.

## Policy as Code

프롬프트 안의 자연어 규칙은 Guidance다. Critical Boundary는 Machine-enforceable Policy가 더 적합하다.

예:

~~~text
if environment == "production"
and action == "deploy"
then approval_required = true
~~~

또는:

~~~text
student_record.read
allowed only if
user.department == student.department
~~~

Policy Engine, IAM, 접근을 중개하는 게이트웨이 등 구현 방식은 다양하다. 핵심은 Enforcement가 Model Reasoning 밖에 있다는 점이다.

## Fail Closed

Critical Policy에서 Parsing Error나 Control Plane Failure가 발생했다고 하자.

위험한 기본값:

~~~text
policy unavailable
→ allow
~~~

더 안전한 기본값:

~~~text
policy unavailable
→ deny / pause
~~~

모든 Low-risk 작업까지 무조건 Fail Closed로 할 필요는 없을 수 있다. 하지만 High-impact Boundary는 permissive fallback을 피한다.

## Just-in-time Privilege

Standing Broad Permission 대신 필요한 시점에 잠깐 권한을 높일 수 있다.

예:

~~~text
Normal:
repo read/write

Deploy Step:
request temporary deploy privilege

After Step:
privilege expires
~~~

AWS의 Agentic AI Lens는 Dynamic Boundary와 Temporary Credential 같은 패턴을 권고한다. 이 역시 하나의 공개 운영 지침 사례로 사용한다. 에이전트의 전체 유지 기간 동안 High-risk 권한을 유지할 필요가 없다.

## Agent가 권한 확대를 제안할 수는 있다

최소 권한을 강하게 적용하면 에이전트가 필요한 행동에서 거부를 만날 수 있다. 두 가지 극단이 있다.

1. 모든 거부를 사람에게 넘긴다.
2. 에이전트가 자기 정책을 수정한다.

두 번째는 위험하다. 더 나은 구조는 다음과 같다.

~~~text
Deny
  ↓
Inspect
  ↓
Agent proposes minimal policy change
  ↓
Deterministic validation
  ↓
Risk analysis
  ↓
Review / Approval
  ↓
Apply versioned policy
  ↓
Retry
~~~

NVIDIA OpenShell의 Agent-driven Policy Management는 이런 방향의 한 사례다. 에이전트는 필요한 기능이나 최소 policy change를 제안할 수 있지만, Policy Authority와 실제 적용 권한은 외부에 남긴다.

## Effective Policy Manifest

에이전트가 현재 무엇을 할 수 있는지 전혀 모르면 Trial-and-error Deny를 반복할 수 있다. 따라서 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)에 현재 유효한 정책에서 필요한 정보를 골라 전달할 수 있다.

예:

~~~text
Allowed:
- repo read/write
- tests
- GitHub read

Requires Approval:
- create PR

Denied:
- production deploy
~~~

이 Manifest는 Planning을 돕는다. 하지만 Enforcement Source는 아니다.

~~~text
Policy Manifest
= model-facing projection

Policy Engine
= authority
~~~

컨텍스트와 상태의 관계와 비슷하다.

## Independent Verification

위험이 큰 행동은 실행 전/후에 별도 검증을 요구할 수 있다.

예:

~~~text
Deploy Candidate
      ↓
Independent Test
      ↓
Policy Check
      ↓
Approval
      ↓
Deploy
      ↓
Health Verification
~~~

검증 담당자가 실행 담당자와 완전히 다른 모델이어야 한다는 뜻은 아니다. 가능하면 정해진 규칙에 따른 검증을 우선한다.

## Rollback과 Compensation

되돌릴 수 없는 행동은 완전히 되돌릴 수 없을 수 있다. 그래도 Compensation Plan이 필요할 수 있다.

예:

- Deploy → previous release rollback
- Payment → refund
- Message send → correction message
- DB update → compensating update

Risk Policy는 행동 이전에 Recovery Surface도 확인할 수 있다.

## 작은 예: Coding Agent의 세 Task

### Task A: 코드 읽기

~~~text
Risk:
R0/R1

Controls:
workspace sandbox
no external write
no approval
~~~

### Task B: PR 생성

~~~text
Risk:
R3

Controls:
scoped GitHub credential
repo allowlist
idempotency
audit
approval optional by organization policy
~~~

### Task C: Production Deploy

~~~text
Risk:
R4

Controls:
strong isolation
short-lived deploy credential
artifact verification
explicit approval
rollback plan
post-deploy health check
~~~

같은 에이전트 실행 환경을 무조건 재사용할 필요도 없다.

## 이 장에서 가져갈 것

에이전트 보안을 하나의 "승인 여부"로 축약하지 않는다.

~~~text
Identity
= who

Authorization
= what

Containment
= where

Approval
= whether now
~~~

그리고 위험에 따라 이 통제의 강도를 다르게 한다. 핵심은 에이전트가 위험을 스스로 선언하는 것이 아니다. External Policy가 신원, 접근 대상 자원, 환경, Consequence를 바탕으로 통제 수단의 조합을 결정하는 것이다. Part V에서는 에이전트가 행동을 수행하기 위한 보안 경계를 완성했다. 다음 Part에서는 이 시스템이 제대로 동작하는지 어떻게 관찰하고 측정할 것인가를 다룬다. 실행 추적 기록(Trace), 평가, 회귀(Regression: 변경 뒤 기존 기능이 나빠지는 회귀), Harness Improvement로 넘어간다.

## 주요 근거

- AWS Agentic AI Lens: Tool Authorization
- AWS Agentic AI Lens: Human-in-the-loop for Critical Decisions
- AWS Agentic AI Lens: Dynamic Boundaries
- AWS Cedar multi-agent authorization
- NVIDIA OpenShell Security Policy
- Anthropic Claude Code Auto Mode
- research/topics/20-risk-adaptive-containment-policy.md
- research/targeted/17-risk-adaptive-policy.md
