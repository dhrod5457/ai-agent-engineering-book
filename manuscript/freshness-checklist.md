# Freshness Checklist

기준일: 2026-10-02
상태: publication-time recheck required

Canonical gate:
- ../review/freshness/index.md

## Protocol
- [ ] MCP latest base revision 재확인
- [ ] MCP Tasks extension lifecycle 재확인
- [ ] A2A latest stable version 재확인
- [ ] A2A TaskState / Agent Card 재확인

## Long-running research
- [ ] OSWorld 2.0 revision / venue
- [ ] Selective Revalidation revision / venue
- [ ] Task-State Horizon revision / venue
- [ ] AgentRewind revision / venue

## Memory / Security
- [ ] memory-security preprints revision / venue
- [ ] Microsoft Entra Agent ID terminology / lifecycle
- [ ] Claude Code sandbox implementation
- [ ] AWS Agentic AI Lens wording
- [ ] OpenShell credential / policy model

## Eval
- [ ] OpenAI Agent Evals naming / feature changes
- [ ] Anthropic Eval guidance changes
- [ ] tau / tau2-bench revision

## Stable Principle Check
다음은 제품/version 변화와 무관하게 본문 논리 일관성을 다시 검사한다.

- [ ] Context ≠ Durable State
- [ ] Memory ≠ Source of Truth
- [ ] Replay ≠ Side-effect re-execution
- [ ] Identity ≠ Credential
- [ ] Sandbox ≠ Authorization
- [ ] Completion Claim ≠ Completion Authority
- [ ] Agent State Plane ≠ Factory Control Plane
