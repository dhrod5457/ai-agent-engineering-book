# 16장. Sandbox와 Containment

Agent에게 다음 Instruction을 줬다고 하자.

> Workspace 밖의 파일은 읽지 마라.

좋은 규칙이다.

하지만 실제 File System에는 사용자의 SSH Key와 Cloud Credential, 다른 Project Source가 Mount돼 있다.

Agent가 Prompt Injection에 속거나 Tool Bug가 생기면 Instruction만으로 Access를 막기 어렵다.

Sandbox의 역할은 Model을 더 순종적으로 만드는 것이 아니다.

**잘못 행동하더라도 도달 가능한 범위를 제한하는 것**이다.

## Containment

이 책에서 Containment는 다음 의미로 사용한다.

> Agent나 Tool이 잘못 행동하더라도 접근 가능한 Process, Filesystem, Network, Credential의 범위를 제한하는 Runtime Boundary.

즉:

~~~text
Model Safety
= 잘 행동할 가능성을 높인다

Containment
= 잘못 행동해도 피해 범위를 제한한다
~~~

둘 다 필요할 수 있다.

하지만 역할은 다르다.

## Sandbox와 Authorization

Sandbox가 있으면 Authorization이 필요 없다고 생각할 수 있다.

그렇지 않다.

~~~text
Containment
= WHERE can it reach?

Authorization
= WHAT can it do?

Approval
= SHOULD it do this now?
~~~

예를 들어 Agent가 Production API에 Network 접근은 가능하지만 read-only Credential만 가진 구조가 있을 수 있다.

Network Boundary와 Authorization이 함께 작동한다.

## Filesystem Boundary

Coding Agent는 File Access가 필요하다.

하지만 전체 Home Directory를 줄 이유는 없을 수 있다.

예:

~~~text
Allowed:
/workspace/repo
/tmp/build

Denied:
/home/user/.ssh
/home/user/.aws
/etc
other repositories
~~~

Read와 Write Scope를 다르게 둘 수도 있다.

~~~text
Repository
→ read/write

Dependency Cache
→ read-only

System Path
→ denied
~~~

## Network Boundary

Filesystem만 막고 Network를 모두 열면 Data Exfiltration 경로가 남는다.

반대로 Network만 막고 Secret File이 보이면 다른 Tool이나 이후 단계에서 노출될 수 있다.

그래서 Filesystem과 Network를 함께 본다.

Network Policy 예:

~~~text
allow:
- package registry
- github.com
- internal test API

deny:
- arbitrary internet
- production admin endpoint
~~~

더 세밀한 Gateway는 Method와 Path까지 제한할 수 있다.

## Process Boundary

Agent가 Shell을 실행한다면 Child Process Capability도 중요하다.

고려 대상:

- privilege
- syscall
- process namespace
- executable allow/deny
- resource limit
- fork bomb
- device access

모든 Agent에 Kernel 수준의 Policy가 필요한 것은 아니다.

Workload Risk에 따라 선택한다.

## Isolation Level

격리 기술은 여러 층이 있다.

개념적으로:

~~~text
OS Policy / Sandbox
        ↓
Container
        ↓
Userspace Kernel
        ↓
MicroVM
        ↓
Dedicated VM / Host
~~~

위로 갈수록 무조건 좋다는 뜻은 아니다.

Startup, Density, Compatibility, GPU, Debugging Cost가 달라진다.

## OS-level Sandbox

Local Coding Agent에서는 OS-level Sandbox가 실용적일 수 있다.

Anthropic Claude Code는 Linux의 bubblewrap 계열과 macOS Seatbelt 등을 사용해 Filesystem과 Network Boundary를 강화하는 접근을 공개했다.

장점:

- 빠른 Startup
- Local Workflow와 결합
- 필요한 Directory만 제한 가능

한계:

- Host Kernel 공유
- Policy 설계가 중요
- OS마다 Mechanism이 다름

## Container

Container는 Process/Filesystem/Resource Isolation에 익숙한 도구다.

하지만 기본 Container 설정만으로 Untrusted Agent Workload에 충분하다고 가정하지 않는다.

다음이 중요하다.

- privilege
- capability
- mount
- network
- seccomp
- AppArmor/SELinux
- namespace

"Container를 쓴다"보다 실제 Isolation Policy가 중요하다.

## gVisor

gVisor는 Userspace Application Kernel을 사용해 Application과 Host Kernel 사이의 Syscall Surface를 줄이는 접근이다.

일반 Container보다 Stronger Isolation을 원하면서 VM보다 가벼운 형태가 필요할 때 후보가 될 수 있다.

Trade-off:

- Compatibility
- Performance
- Operational Complexity

특정 Agent에 무조건 권장하는 기술은 아니다.

## MicroVM

Firecracker 같은 MicroVM은 KVM Hardware Virtualization Boundary를 사용한다.

AgentCore Runtime처럼 Session별 MicroVM을 사용해 CPU, Memory, Filesystem을 격리하는 Managed Runtime 사례도 있다.

장점:

- Guest Kernel 분리
- Multi-tenant 격리에 유리
- Runtime disposal이 명확

비용:

- Image 관리
- Virtualization Infrastructure
- Startup / Resource Overhead
- GPU/Device Complexity

## Disposable Runtime

Agent Runtime을 Durable State Store로 사용하지 않으면 격리와 Recovery가 쉬워진다.

~~~text
Durable State
      +
Disposable Runtime
~~~

Runtime이 손상되거나 Crash하면 새 Environment를 만들고 State Plane에서 Resume할 수 있다.

이 원칙은 Part III와 연결된다.

## Sandbox 안의 Credential

강한 Sandbox라도 Credential이 과도하면 위험하다.

~~~text
MicroVM
+ production-admin token
~~~

은 VM Escape 없이도 Production 전체를 수정할 수 있다.

Containment는 Credential Scope를 대체하지 않는다.

Part V의 흐름이 다음처럼 연결되는 이유다.

~~~text
Identity
→ Credential
→ Sandbox
→ Policy
~~~

## Tool Output과 Network

Agent가 외부 Web을 읽을 수 있으면 Prompt Injection Surface가 커진다.

Network Policy로 Source를 제한할 수 있다.

예:

~~~text
Research Agent
→ public web allowed

Repository Fix Agent
→ package registry + GitHub only
~~~

Agent 역할에 따라 Network Profile이 다를 수 있다.

## Resource Limit

Containment는 Security뿐 아니라 Reliability에도 필요하다.

예:

- CPU Limit
- Memory Limit
- Disk Limit
- Process Count
- Timeout

잘못된 Build나 Infinite Loop가 Host 전체를 영향을 주지 않게 한다.

## Runtime Session은 Durable State가 아니다

Managed Runtime이 Session을 제공한다고 하자.

그 Session 안에서 File이 유지될 수 있다.

하지만 그것을 Long-term State로 간주하면 안 된다.

~~~text
Runtime Session
= execution environment lifecycle

Agent State Plane
= execution continuity
~~~

Runtime이 종료돼도 Goal과 Artifact Reference, Approval State는 살아 있어야 할 수 있다.

## 작은 예: Repository Fix Agent

Risk가 낮은 Local Fix Task:

~~~text
Filesystem:
repo read/write

Network:
package registry + GitHub read

Credential:
none or read-only

Runtime:
OS sandbox / container
~~~

Production Deploy Task:

~~~text
Filesystem:
artifact only

Network:
deployment endpoint only

Credential:
short-lived deploy token

Runtime:
stronger isolated environment

Approval:
required
~~~

같은 Agent 제품이라도 Task Risk에 따라 Runtime Profile이 달라질 수 있다.

## Isolation 선택 기준

기술 이름보다 다음 질문이 먼저다.

- Untrusted Code를 실행하는가.
- Multi-tenant인가.
- Secret을 다루는가.
- Production Access가 있는가.
- Arbitrary Network가 필요한가.
- GPU/Device가 필요한가.
- Startup Latency가 중요한가.
- Workspace Persistence가 필요한가.
- Debugging이 얼마나 중요한가.

이 조건으로 Isolation Level을 선택한다.

## 이 장에서 가져갈 것

Sandbox는 Agent에게 "하지 마라"고 말하는 기능이 아니다.

잘못 행동했을 때도 실제로 갈 수 없는 경계를 만드는 기능이다.

~~~text
Instruction
→ behavioral guidance

Authorization
→ action permission

Containment
→ reachable boundary
~~~

세 계층을 분리한다.

다음 장에서는 이 통제를 모든 Task에 동일하게 적용하지 않는 방법을 다룬다.

Read-only 분석과 Production Deploy가 같은 Sandbox, Credential, Approval 정책을 가져야 할 이유는 없다.

Risk-adaptive Policy로 넘어간다.

## 주요 근거

- Anthropic, Claude Code Sandboxing
- Anthropic, How We Contain Claude Across Products
- gVisor Security Architecture
- Firecracker Design
- AWS AgentCore Runtime
- NVIDIA OpenShell
- research/topics/11-sandbox-runtime-isolation.md
