# Risk-adaptive Containment and Policy

기준일: 2026-10-02

## 문제

모든 Agent Task를 같은 Sandbox와 같은 approval 정책으로 실행하면 두 극단이 생긴다.

- 너무 느리고 승인 요청이 많은 시스템
- 지나치게 넓은 권한을 가진 위험한 시스템

따라서 Task Risk에 따라 Runtime, Network, Credential, Approval을 조합하는 방식을 검토한다.

## 위험 요소

Task Risk를 평가할 때 후보:

- read vs write
- reversible vs irreversible
- local vs remote
- public vs confidential data
- credential 필요 여부
- production 여부
- financial / legal consequence
- arbitrary code execution
- external communication
- cross-tenant access
- network egress 범위

## 예시 Risk Tier

### R0 — Pure Read / Offline

예:
- local source analysis
- static document summarization

통제:
- no credential
- no external write
- basic sandbox

### R1 — Workspace Mutation

예:
- repository file edit
- local build/test

통제:
- isolated workspace
- write limited to workspace
- package/network allowlist
- no production credential

### R2 — External Read

예:
- GitHub read
- internal API read

통제:
- endpoint allowlist
- read-only credential
- network policy
- audit

### R3 — External Bounded Write

예:
- PR creation
- Slack draft/send
- issue update

통제:
- endpoint/method/path policy
- scoped credential
- idempotency
- target validation
- optional approval based on action

### R4 — High-impact / Irreversible

예:
- deploy
- payment
- production mutation
- security policy change

통제:
- stronger isolation
- explicit policy gate
- independent verifier
- human or trusted approval
- short-lived credential
- complete audit
- rollback / compensation plan

## Policy as Code

OpenShell은 filesystem, process, network, provider policy를 declarative하게 표현하고 runtime에서 강제한다.

특히 network policy는:

- destination
- port
- calling binary
- HTTP method
- path

까지 제한할 수 있다.

이런 정책은 system prompt보다 deterministic하다.

## Dynamic Policy Expansion

Agent가 필요한 access가 deny되었을 때 곧바로 권한을 넓히지 않는다.

OpenShell의 Agent-driven Policy Management는 다음 흐름을 사용한다.

~~~text
Deny
→ Inspect
→ Agent proposes narrow policy
→ Deterministic validation
→ Risk prover
→ Review / Approval
→ Hot reload
→ Retry
~~~

이 구조는 매우 중요한 패턴이다.

Agent가 자신의 권한 확대를 제안할 수는 있지만 최종 authority는 외부 control plane에 둔다.

## Capability Manifest

Agent가 허용된 capability를 미리 모르면 trial-and-error로 deny를 반복한다.

따라서 Harness에 current effective policy를 readable manifest로 제공하면:

- 불필요한 tool attempt 감소
- context/token 절감
- 더 현실적인 planning

이 가능하다.

단, manifest는 실제 enforcement source가 아니라 projection이다.

## Policy Change도 Side Effect다

Policy 변경은 future action surface를 바꾼다.

따라서 code/config mutation처럼:

- provenance
- diff
- validation
- risk analysis
- approval
- version
- rollback

이 필요하다.

## Fail Closed

보안 boundary에서:

- invalid policy
- malformed schema
- unknown field
- control plane disconnect

상황에 permissive fallback을 허용하면 위험하다.

OpenShell은 여러 지점에서 invalid update를 거부하고 last-known-good policy를 유지하는 방식을 사용한다.

## Isolation Selection

Task risk가 올라갈수록 다음을 강화할 수 있다.

~~~text
Process policy
→ OS sandbox
→ gVisor / stronger container
→ microVM
→ dedicated isolated environment
~~~

단, isolation strength만 높이고 credential scope를 그대로 두면 충분하지 않다.

## 책에 반영할 핵심 원칙

1. Sandbox level은 Task Risk에 따라 선택한다.
2. Authorization policy를 prompt와 분리한다.
3. Agent가 권한 확대를 직접 적용하지 못하게 한다.
4. Policy expansion은 propose → prove → approve → apply로 관리한다.
5. Network access는 host뿐 아니라 method/path까지 줄일 수 있다.
6. Current effective policy를 Agent가 읽을 수 있게 하되 enforcement와 분리한다.
7. Policy change도 versioned/audited side effect다.
8. Critical boundary는 fail closed가 기본이다.

## 주요 근거

- NVIDIA OpenShell Security Policy
- NVIDIA OpenShell Sandbox Architecture
- OpenShell Agent-driven Policy Management
- Anthropic Claude Code Sandboxing / Auto Mode
- AWS AgentCore Runtime Isolation
