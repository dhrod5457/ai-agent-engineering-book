# 13장. Memory Write는 Side Effect다

## Goal
독자가 Persistent Memory를 보안·운영 측면의 privileged side effect로 취급하고 write/retrieval policy를 설계할 수 있게 한다.

## Core Claims
- Persistent Memory Write는 미래 behavior를 변경한다.
- provenance와 scope 없는 Memory는 poisoning과 leakage를 키운다.
- Write-time filter 하나로 compositional/dormant attack을 막기 어렵다.
- Memory에는 Accept / Review / Quarantine / Forget / Repair lifecycle이 필요하다.

## Reader Questions
- Agent가 알아서 memory를 저장하게 해도 되는가?
- 악성 memory는 어떻게 장기적으로 영향을 주는가?
- 잘못 저장된 memory는 삭제만 하면 끝나는가?

## Flow
1. one-shot injection vs persistent poisoning
2. Memory Candidate
3. provenance / scope
4. write gate
5. compositional attack
6. retrieval-time security
7. quarantine / repair / forget
8. audit events

## Example / Figure
- untrusted tool result가 memory로 승격돼 이후 action을 왜곡하는 사례
- Figure: Memory Write Gate

## Evidence
- research/topics/17-memory-security-write-policy.md
- Microsoft Memory Safety
- MPBench
- MemSecBench
- MemPoison
- MemSentry

## Avoid
- 모든 adversarial ML 공격
- memory database 제품 비교

## Draft Exit Criteria
- write와 retrieval 보안이 모두 설명된다.
- memory lifecycle과 audit event가 제시된다.
