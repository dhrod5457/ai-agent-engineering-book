# 16장. Sandbox와 Containment

## Goal
독자가 Agent Runtime 격리 수준을 위험도와 workload 특성에 따라 선택할 수 있게 한다.

## Core Claims
- Sandbox는 permission prompt가 아니다.
- Filesystem과 Network boundary를 함께 설계해야 한다.
- Container, userspace kernel, microVM은 서로 다른 isolation trade-off를 가진다.
- Runtime state는 Durable State가 아니다.

## Reader Questions
- Container면 충분한가?
- gVisor와 microVM은 무엇이 다른가?
- Sandbox가 있으면 authorization은 없어도 되는가?

## Flow
1. agent side effect와 blast radius
2. filesystem/network/process
3. OS sandbox
4. gVisor
5. strong container
6. microVM
7. credential relation
8. runtime lifecycle

## Example / Figure
- 동일 Agent를 R1/R4 task에서 다른 runtime에 배치
- Figure: isolation ladder

## Evidence
- research/topics/11-sandbox-runtime-isolation.md
- Claude Code Sandboxing
- gVisor
- Firecracker
- AWS AgentCore
- NVIDIA OpenShell

## Avoid
- kernel internals
- 성능 benchmark의 과도한 비교

## Draft Exit Criteria
- isolation 선택 기준표가 있다.
- Authorization과 Containment 차이가 반복 확인된다.
