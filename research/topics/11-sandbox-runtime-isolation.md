# Sandbox and Runtime Isolation

기준일: 2026-10-02

## 왜 Sandbox가 Agent Architecture의 핵심인가

Agent는 model output을 실제 process, filesystem, network action으로 변환한다.

따라서 Sandbox는 성능 보조 기능이 아니라 blast radius를 제한하는 security boundary다.

## Isolation Layer

대략 다음 계층을 구분할 수 있다.

~~~text
Process Policy
- seccomp
- Landlock
- AppArmor
- namespaces
- seatbelt / bubblewrap

Userspace Kernel
- gVisor

Container + Strong Policy
- namespace/cgroup + LSM + proxy

MicroVM
- Firecracker / KVM

Dedicated VM / Host
- strongest operational isolation, highest cost
~~~

실제 시스템은 여러 계층을 조합한다.

## OS-level Sandbox

Anthropic Claude Code sandboxing은 Linux bubblewrap과 macOS Seatbelt 등을 이용해 filesystem과 network boundary를 함께 둔다.

핵심 교훈:

- filesystem만 제한하면 exfiltration 위험이 남음
- network만 제한하면 host secret 접근 위험이 남음
- 둘을 함께 제한해야 함

장점:
- startup overhead가 낮음
- local coding workflow에 적합

제약:
- host kernel을 공유
- policy coverage를 정확히 설계해야 함

## gVisor

gVisor는 일반 container와 달리 userspace application kernel이 syscall interface를 구현한다.

host kernel에 직접 노출되는 syscall surface를 줄이는 방식이다.

특징:

- VM이 아님
- userspace kernel
- systrap 또는 KVM platform
- container ecosystem과 결합하기 쉬움

Agent workload에서 container보다 stronger isolation이 필요하지만 microVM보다 density/startup을 우선할 때 후보가 될 수 있다.

## Firecracker MicroVM

Firecracker는 KVM hardware virtualization boundary를 사용한다.

추가 defense-in-depth:

- seccomp
- cgroup
- namespace
- jailer
- privilege drop

장점:
- guest kernel 분리
- tenant/session 격리에 강함

제약:
- image/kernel lifecycle 관리 필요
- virtualization infrastructure 필요
- microVM 안에 credential을 넣으면 내부 compromise 시 해당 session credential은 노출 가능

## AWS AgentCore Runtime

AgentCore Runtime은 각 session을 전용 microVM으로 격리한다.

각 session은 다음을 독립적으로 가진다.

- CPU
- memory
- filesystem

기본 microVM compute의 memory와 local disk는 session compute lifecycle에 묶이며 microVM 종료 시 폐기된다.

2026-10-02 기준 AgentCore는 managed session storage(Preview)를 별도로 제공한다. 이 storage는 per-session filesystem을 stop/resume 사이에 복원할 수 있지만 idle expiry와 runtime version update 시 reset되는 lifecycle을 가진다. 구조화된 장기 정보에는 별도 AgentCore Memory를 사용할 수 있다.

중요한 경계:

> Session isolation, Workspace persistence, Long-term durability는 서로 다른 책임이다.

## NVIDIA OpenShell

OpenShell은 Agent workload 안과 밖의 supervisor를 분리한다.

주요 구조:

~~~text
Supervisor
- credential
- policy
- L7 proxy
- gateway relay

Sandbox
- process control
- seccomp listener
- Landlock

Agent Child
- no capabilities
- no_new_privs
- final syscall filter
~~~

network request는 policy gateway를 통과하고 credential은 approved endpoint에만 주입한다.

이 구조는 Sandbox를 단순 compute container가 아니라 policy enforcement point로 확장한 사례다.

## Isolation과 Policy

강한 VM boundary만으로 충분하지 않다.

Agent가 합법적인 credential로 production DB를 삭제하면 VM escape가 없어도 사고다.

따라서:

~~~text
Isolation
limits WHERE the agent can reach

Authorization / Policy
limits WHAT the agent can do

Verification / Approval
limits WHEN it may do it
~~~

세 가지가 모두 필요하다.

## 선택 기준

Sandbox 기술 선택 시:

- untrusted code 수준
- secret exposure
- multi-tenant 여부
- network requirement
- startup latency
- density
- kernel feature requirement
- GPU requirement
- session duration
- persistence requirement
- debugging requirement

을 함께 본다.

## 설계 원칙

1. Sandbox와 permission prompt를 동일시하지 않는다.
2. filesystem과 network boundary를 함께 설계한다.
3. credential을 sandbox 내부에 최소화한다.
4. multi-tenant Agent는 stronger isolation을 우선 검토한다.
5. Runtime compute는 교체 가능하게 설계하고, 필요한 Workspace persistence는 별도 storage lifecycle로 명시한다.
6. Sandbox policy도 version/eval/audit 대상이다.
7. isolation과 authorization을 별개 계층으로 유지한다.

## 주요 근거

- Anthropic Claude Code Sandboxing
- Anthropic Containment Engineering
- gVisor Security Architecture
- Firecracker Design / Jailer
- AWS AgentCore Runtime microVM
- NVIDIA OpenShell
