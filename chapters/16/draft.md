# 16장. Sandbox와 Containment

에이전트에게 다음 지침을 줬다고 하자.

> 작업 공간 밖의 파일은 읽지 마라.

좋은 규칙이다. 하지만 호스트 파일 시스템에는 사용자의 SSH 키와 클라우드 인증 정보, 다른 프로젝트 소스 코드가 연결돼 있다. 에이전트가 외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)에 속거나 도구의 오류가 생기면 지침만으로 접근을 막기 어렵다. 샌드박스(Sandbox: 접근할 수 있는 범위를 제한하는 환경)의 역할은 모델을 더 순종적으로 만드는 것이 아니다.

**잘못 행동하더라도 도달 가능한 범위를 제한하는 것**이다.

## Containment

이 책에서 격리(Containment: 접근과 피해 범위를 제한하는 격리)는 다음 의미로 사용한다.

> 에이전트나 도구가 잘못 행동하더라도 접근 가능한 프로세스, 파일 시스템, 네트워크, 인증 정보(Credential)의 범위를 제한하는 Runtime Boundary.

즉:

~~~text
Model Safety
= 잘 행동할 가능성을 높인다

Containment
= 잘못 행동해도 피해 범위를 제한한다
~~~

둘 다 필요할 수 있다. 하지만 역할은 다르다.

## Sandbox와 Authorization

샌드박스가 있으면 권한 확인(Authorization)이 필요 없다고 생각할 수 있다. 그렇지 않다.

~~~text
Containment
= WHERE can it reach?

Authorization
= WHAT can it do?

Approval
= SHOULD it do this now?
~~~

예를 들어 에이전트가 Production API에 네트워크 접근은 가능하지만 read-only Credential만 가진 구조가 있을 수 있다. 네트워크 접근 경계와 권한 확인이 함께 작동한다.

## Filesystem Boundary

코드 작업 에이전트는 File Access가 필요하다. 하지만 전체 Home Directory를 줄 이유는 없을 수 있다.

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

파일 시스템만 막고 네트워크를 모두 열면 Data Exfiltration 경로가 남는다. 반대로 네트워크만 막고 Secret File이 보이면 다른 도구이나 이후 단계에서 노출될 수 있다. 그래서 파일 시스템과 네트워크를 함께 본다.

네트워크 정책 예:

~~~text
allow:
- package registry
- github.com
- internal test API

deny:
- arbitrary internet
- production admin endpoint
~~~

더 세밀한 접근을 중개하는 게이트웨이는 Method와 Path까지 제한할 수 있다.

## Process Boundary

에이전트가 셸을 실행한다면 Child Process Capability도 중요하다.

고려 대상:

- privilege
- syscall
- process namespace
- executable allow/deny
- resource limit
- fork bomb
- device access

모든 에이전트에 Kernel 수준의 정책이 필요한 것은 아니다. Workload Risk에 따라 선택한다.

## Isolation 접근은 서로 다른 Trade-off를 가진다

에이전트 실행 환경에 사용할 수 있는 격리 접근은 여러 가지다.

~~~text
OS Policy / Sandbox
Container
Userspace Kernel
MicroVM
Dedicated VM / Host
~~~

이 순서를 절대적인 보안 등급으로 읽어서는 안 된다. 실제 선택은 Threat Model, 시작, Density, 호환성, GPU, Debugging Cost에 따라 달라진다.

## OS-level Sandbox

Local Coding Agent에서는 OS-level Sandbox가 실용적일 수 있다. Anthropic은 Claude Code의 Bash sandbox에 Linux bubblewrap과 macOS Seatbelt 같은 OS primitive를 사용하는 방식을 공개했다.

장점:

- 빠른 시작
- Local Workflow와 결합
- 필요한 Directory만 제한 가능

한계:

- Host Kernel 공유
- 정책 설계가 중요
- OS마다 작동 방식이 다름

## Container

컨테이너는 Process/Filesystem/Resource Isolation에 익숙한 도구다. 하지만 기본 컨테이너 설정만으로 Untrusted Agent Workload에 충분하다고 가정하지 않는다. 다음이 중요하다.

- privilege
- capability
- mount
- network
- seccomp
- AppArmor/SELinux
- namespace

"컨테이너를 쓴다"보다 적용된 Isolation Policy가 중요하다.

## gVisor

gVisor는 Userspace Application Kernel을 사용해 애플리케이션과 Host Kernel 사이의 Syscall Surface를 줄이는 접근이다. 일반 컨테이너보다 Stronger Isolation을 원하면서 VM보다 가벼운 형태가 필요할 때 후보가 될 수 있다.

얻는 점과 감수할 점:

- 호환성
- Performance
- Operational Complexity

특정 에이전트에 무조건 권장하는 기술은 아니다.

## MicroVM

Firecracker 같은 경량 가상 머신은 KVM Hardware Virtualization Boundary를 사용한다. AgentCore Runtime처럼 세션별 경량 가상 머신을 사용해 CPU, 메모리, 파일 시스템을 격리하는 Managed Runtime 사례도 있다.

장점:

- Guest Kernel 분리
- Multi-tenant 격리에 유리
- Runtime disposal이 명확

비용:

- Image 관리
- Virtualization Infrastructure
- 시작 / Resource Overhead
- GPU/Device Complexity

## Disposable Runtime

에이전트 실행 환경을 Durable State Store로 사용하지 않으면 격리와 복구가 쉬워진다.

~~~text
Durable State
      +
Disposable Runtime
~~~

실행 환경이 손상되거나 비정상 종료하면 새 환경을 만들고 상태 관리 계층에서 실행 재개할 수 있다. 이 원칙은 Part III와 연결된다.

## Sandbox 안의 Credential

강한 샌드박스라도 인증 정보가 과도하면 위험하다.

~~~text
MicroVM
+ production-admin token
~~~

은 VM Escape 없이도 Production 전체를 수정할 수 있다. 격리는 인증 정보로 행사할 수 있는 권한 범위를 대체하지 않는다. Part V의 흐름이 다음처럼 연결되는 이유다.

~~~text
Identity
→ Credential
→ Sandbox
→ Policy
~~~

## Tool Output과 Network

에이전트가 외부 Web을 읽을 수 있으면 Prompt Injection Surface가 커진다. 네트워크 정책으로 정보 원본을 제한할 수 있다.

예:

~~~text
Research Agent
→ public web allowed

Repository Fix Agent
→ package registry + GitHub only
~~~

에이전트 역할에 따라 Network Profile이 다를 수 있다.

## Resource Limit

격리는 보안뿐 아니라 반복 실행의 신뢰성에도 필요하다.

예:

- CPU Limit
- Memory Limit
- Disk Limit
- Process Count
- 응답 시간 초과

잘못된 빌드나 무한 반복이 호스트 전체에 영향을 주지 않도록 한다.

## Runtime Session은 Durable State가 아니다

Managed Runtime이 세션을 제공한다고 하자. 기본 compute의 memory와 local disk는 Runtime lifecycle에 묶일 수 있다. 반대로 AgentCore의 managed session storage처럼 stop/resume 사이에 작업 공간 파일을 복원하는 기능도 존재한다. 중요한 것은 "실행 환경이 항상 ephemeral인가"가 아니라 **Workspace Persistence와 Agent Execution State의 책임을 분리하는 것**이다.

~~~text
Runtime / Session Storage
= execution workspace lifecycle

Agent State Plane
= execution continuity
~~~

작업 공간이 복원되더라도 목표와 Artifact Reference, 승인 상태, 이미 실행한 External Side Effect는 별도 상태에서 확인할 수 있어야 한다.

## 작은 예: Repository Fix Agent

위험이 낮은 Local Fix Task:

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

같은 에이전트 제품이라도 작업의 위험에 따라 Runtime Profile이 달라질 수 있다.

## Isolation 선택 기준

기술 이름보다 다음 질문이 먼저다.

- Untrusted Code를 실행하는가.
- Multi-tenant인가.
- 비밀 정보를 다루는가.
- Production Access가 있는가.
- Arbitrary Network가 필요한가.
- GPU/Device가 필요한가.
- Startup Latency가 중요한가.
- Workspace Persistence가 필요한가.
- 오류 원인 분석이 얼마나 중요한가.

이 조건으로 Isolation Level을 선택한다.

## 이 장에서 가져갈 것

샌드박스는 에이전트에게 "하지 마라"고 말하는 기능이 아니다. 잘못 행동했을 때도 접근할 수 없는 경계를 만드는 기능이다.

~~~text
Instruction
→ behavioral guidance

Authorization
→ action permission

Containment
→ reachable boundary
~~~

세 계층을 분리한다. 다음 장에서는 이 통제를 모든 작업에 동일하게 적용하지 않는 방법을 다룬다. Read-only 분석과 운영 환경 배포가 같은 샌드박스, 인증 정보, 승인 정책을 가져야 할 이유는 없다. Risk-adaptive Policy로 넘어간다.

## 주요 근거

- Anthropic, Claude Code Sandboxing
- Anthropic, How We Contain Claude Across Products
- gVisor Security Architecture
- Firecracker Design
- AWS AgentCore Runtime
- NVIDIA OpenShell
- research/topics/11-sandbox-runtime-isolation.md
