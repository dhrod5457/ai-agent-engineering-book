# Publication-time Freshness Gate

기준일: 2026-10-02

출간 직전 변경 가능성이 높은 사실만 다시 확인하기 위한 index다.

## Protocol

### MCP
Audit:
- review/freshness/mcp-2026-10-02.md

Recheck:
- latest base revision
- stateless core semantics
- Tasks extension lifecycle
- supported task methods
- SDK implementation status

### A2A
Audit:
- review/freshness/a2a-2026-10-02.md

Recheck:
- latest stable version
- TaskState enum
- Agent Card
- auth guidance
- supported bindings/transports

## Long-running Research

Audit:
- review/freshness/long-running-2026-10-02.md

Recheck:
- OSWorld 2.0 revision / venue
- Selective Revalidation revision / venue
- Task-State Horizon revision / venue
- AgentRewind revision / venue
- released implementations / benchmark corrections

## Security

Audit:
- review/freshness/security-2026-10-02.md

Recheck:
- memory-security preprints
- Microsoft Entra Agent ID terminology / lifecycle
- Claude Code sandbox implementation
- AWS Agentic AI Lens recommendations
- OpenShell policy / credential model

## Low-volatility Principles

다음은 version freshness보다 wording consistency를 확인한다.

- idempotency
- optimistic concurrency
- least privilege
- separation of authentication / authorization / approval
- deterministic verification
- durable execution
- replay vs side-effect re-execution

## Rule

Freshness Audit에서 새로운 제품/버전 사실이 바뀌더라도 본문 Architecture의 핵심 논리가 바뀌지 않도록 한다.

~~~text
volatile fact
→ source note / appendix

stable principle
→ main narrative
~~~
