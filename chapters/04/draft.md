# 4장. Context는 저장소가 아니다

Agent가 Repository를 잘 이해하지 못하면 가장 먼저 떠올리기 쉬운 해결책은 더 많은 정보를 넣는 것이다.

README를 넣는다. Architecture 문서를 넣는다. 최근 Commit을 넣는다. 관련 Issue를 넣는다. Tool 설명을 전부 넣는다. 이전 대화도 가능한 한 많이 유지한다.

처음에는 좋아 보인다.

모델이 더 많은 사실을 볼 수 있으니 판단도 더 좋아질 것 같다.

하지만 Long-running Agent에서는 이 방식이 빠르게 한계에 부딪힌다. 오래된 정보와 최신 정보가 섞이고, 중요한 사실이 긴 로그 안에 묻히고, Tool Schema만으로 상당한 Context를 사용한다. 결국 모델이 필요한 정보를 "가지고는 있지만 제대로 사용하지 못하는" 상황이 생긴다.

Context Engineering은 무엇을 더 넣을지보다 **지금 이 판단에 무엇이 필요한지 고르는 문제**에 가깝다.

## Context는 현재 Inference의 입력이다

이 책에서는 Context를 다음처럼 좁게 사용한다.

> **Context는 현재 한 번의 Model Inference에 실제로 들어가는 정보다.**

이 정의를 쓰면 여러 개념이 분리된다.

~~~text
Repository
Database
Conversation History
Agent State Plane
Long-term Memory
Tool Catalog
External API
        ↓
Context Selection / Projection
        ↓
Current Context
        ↓
Model
~~~

Repository 전체가 Context인 것은 아니다.

Database 전체가 Context인 것도 아니다.

Memory 전체도 Context가 아니다.

그중 현재 판단에 필요한 일부만 Model Input으로 들어간다.

이 구분이 중요한 이유는 Context Window가 저장장치가 아니기 때문이다.

## More Context는 Better Agent가 아니다

Context가 너무 적으면 필요한 정보가 빠진다.

그렇다고 가능한 모든 정보를 넣으면 다른 문제가 생긴다.

### Attention Dilution

중요한 정보와 중요하지 않은 정보가 같은 입력 공간을 경쟁한다.

예를 들어 Agent가 하나의 Java Service Method를 수정하려는데 다음을 모두 넣었다고 하자.

- 전체 300개 Source File
- 모든 Test Log
- 80개 Tool Schema
- 최근 50개 Commit
- 200개의 Issue
- 전체 Conversation History

관련 정보가 Context 안에 존재하더라도 실제 판단에 사용될 확률이 높아진다고 단정할 수 없다.

### Stale Context

Context 안에 들어간 정보는 입력 시점의 Snapshot이다.

외부 Source가 바뀌어도 기존 Context는 자동으로 갱신되지 않는다.

~~~text
T0
Repository HEAD = abc123
        ↓
Context 생성

T1
Repository HEAD = def456
        ↓
Old Context still contains abc123
~~~

Long-running Agent에서는 이 문제가 중요해진다.

### Conflicting Context

같은 사실에 대해 여러 버전이 동시에 들어올 수 있다.

예를 들어:

~~~text
Old README:
API endpoint = /v1/users

Current Source:
API endpoint = /v2/users
~~~

모델이 어떤 정보를 우선해야 하는지 명확하지 않다면 더 많은 Context가 오히려 혼란을 만든다.

### Context Cost

Context가 커지면 Token Cost와 Latency가 증가한다.

하지만 비용보다 중요한 것은 **불필요한 정보가 Agent Decision Surface를 넓힌다는 점**이다.

## Context는 State의 Projection이다

앞 장에서 Harness가 State와 분리돼야 한다고 설명했다.

여기서 그 관계를 조금 더 구체화할 수 있다.

~~~text
Agent State Plane
- Goal
- Progress
- Event History
- Artifact
- Approval
- Source Version
        ↓
Context Projection
        ↓
Current Inference
~~~

Model에게 Event History 전체를 매 Turn 넣을 필요는 없다.

현재 필요한 정보가 다음과 같다면:

- 현재 Goal
- 방금 실패한 Tool Result
- 수정 대상 File
- relevant Test
- 현재 Approval State

그것만 Projection할 수 있다.

즉 State는 durable하게 보존하고 Context는 ephemeral하게 구성한다.

이 원칙은 Long-running Agent에서 특히 중요하다.

## Context Assembly는 하나의 Engine이다

단순 Agent에서는 Context를 문자열을 이어 붙여 만들 수 있다.

Production Agent에서는 여러 Source를 조합하게 된다.

예:

~~~text
System Instruction
+ User Input
+ Goal
+ Relevant History
+ Selected Tool Schemas
+ Retrieved Documents
+ Current Workspace Summary
+ Recent Tool Results
+ Policy / Environment Metadata
~~~

이때 중요한 것은 "모두 넣는다"가 아니라 각 Source마다 포함 기준을 가지는 것이다.

예를 들어:

~~~text
Conversation History
→ 최근 Turn 전체 + 과거 Relevant Summary

Tool Catalog
→ 현재 Task에서 허용된 Capability만

Repository
→ 관련 File / Symbol / Diff만

Event History
→ 현재 Decision에 필요한 Projection만

Memory
→ scope/freshness 검사를 통과한 항목만
~~~

이런 선택 책임을 이 책에서는 Context Engine이라는 개념으로 설명한다.

역시 특정 제품 이름이 아니라 책임을 설명하기 위한 용어다.

## Progressive Context

처음부터 모든 정보를 넣기보다 필요한 만큼 확장하는 방식이 유용하다.

예를 들어 Coding Agent가 처음에는 다음만 알 수 있다.

~~~text
Goal
Repository Map
Relevant Directory
Available Search Tools
~~~

그다음 필요할 때:

~~~text
Search Symbol
  ↓
Read File
  ↓
Read Related Test
  ↓
Read Specific Config
~~~

형태로 Context를 확장한다.

이 방식의 장점은 단순 Token 절감이 아니다.

Agent가 실제로 무엇을 필요로 했는지 Trace로 남기기 쉽다.

또 Repository가 커져도 Context 크기를 상대적으로 제어하기 쉽다.

## Tool Schema도 Context다

Tool을 많이 제공하면 Agent가 더 많은 Capability를 얻는다.

하지만 각 Tool은 대개 다음 정보를 Context에 추가한다.

- name
- description
- input schema
- output contract

Tool이 5개일 때와 100개일 때 Model이 선택해야 하는 Action Space는 다르다.

따라서 Tool Catalog 전체를 항상 노출하는 것이 최선이라고 가정하지 않는다.

Task와 Policy에 따라 Tool Surface를 Projection할 수 있다.

~~~text
All Capabilities
      ↓
Eligibility / Policy
      ↓
Relevant Tool Set
      ↓
Current Context
~~~

이 지점은 다음 장의 Tool Engineering과 직접 연결된다.

## Tool Result도 Context를 오염시킬 수 있다

Tool은 신뢰된 코드일 수 있다.

하지만 Tool이 읽어온 데이터까지 신뢰된 것은 아니다.

예를 들어 Web Tool이 외부 페이지를 읽었다면 결과 안에 다음이 포함될 수 있다.

- 오래된 정보
- 악성 Prompt Injection
- 과도하게 긴 HTML
- 사용자 데이터
- irrelevant navigation text

따라서 Tool Result를 그대로 Model Context에 넣는 것이 항상 안전하지 않다.

필요할 수 있는 처리는 다음과 같다.

- size limit
- structured extraction
- redaction
- provenance
- trust label
- summarization
- relevant section selection

Tool Output Filtering은 Context Engineering이자 Security Boundary다.

## Conversation History는 State 전체가 아니다

대화형 Agent에서는 Conversation History가 중심처럼 보인다.

그래서 모든 State를 Message로 표현하려는 설계가 생긴다.

예:

~~~text
assistant:
"Tool A 실행 완료"

assistant:
"Approval 대기 중"

assistant:
"File X 생성"
~~~

하지만 Conversation History만으로는 다음을 안정적으로 표현하기 어렵다.

- Tool Execution ID
- Idempotency Key
- Approval Object
- Artifact Checksum
- Source Version
- Runtime Failure
- Retry Count

이 정보는 Model이 읽을 수도 있지만 그보다 먼저 시스템이 정확하게 관리해야 한다.

따라서:

~~~text
Conversation History
⊂ Execution State
~~~

로 보는 편이 낫다.

Conversation은 Context Source 중 하나다.

State Store 전체가 아니다.

## Compaction은 유용하지만 한계가 있다

Long-running Agent에서는 Context가 계속 커진다.

가장 흔한 대응 중 하나가 Compaction이다.

예를 들어:

~~~text
Turns 1~50
      ↓
Summary
      ↓
Turns 51~current
~~~

Compaction은 필요한 기법이다.

하지만 Durable State를 대체하지 않는다.

Summary에는 세부 정보가 사라질 수 있다.

예를 들어 다음 정보가 요약에서 빠질 수 있다.

- 어떤 Tool Call이 실제 성공했는가.
- 정확히 어떤 File이 수정됐는가.
- 어떤 Approval이 아직 Pending인가.
- 어떤 Source Version을 봤는가.
- 다음 실행에서 다시 하면 안 되는 Side Effect는 무엇인가.

따라서:

~~~text
Compaction
= Context Optimization

Checkpoint / Event History
= Execution Continuity
~~~

로 분리한다.

## Context Reset이 필요할 때

Context를 계속 이어가는 것이 항상 좋은 것도 아니다.

다음 상황에서는 새로운 Context를 만드는 편이 나을 수 있다.

- Task Phase가 완전히 바뀜
- History가 너무 길어짐
- 오래된 가정이 많이 남음
- 다른 Specialist로 Handoff
- Model Upgrade / Session Restart
- Security Boundary 변경

이때 필요한 State만 다시 Projection한다.

~~~text
Old Context
   ↓ discard

Durable State
   ↓ re-project

Fresh Context
~~~

이 구조가 가능하려면 중요한 정보가 Context 밖에도 존재해야 한다.

다시 Agent State Plane과 연결된다.

## 작은 예: Repository 수정 Agent

목표:

> UserService의 timeout 처리 오류를 수정하라.

나쁜 Context 전략:

~~~text
전체 Repository
+ 최근 CI Log 전체
+ 모든 Tool Schema
+ 전체 Conversation
+ 모든 Issue
~~~

더 나은 시작점은 다음과 같을 수 있다.

~~~text
Goal
+ Repository Map
+ UserService 관련 Search Result
+ 관련 Test
+ 현재 Branch / HEAD
+ 필요한 Tool 6개
~~~

Agent가 Config가 필요하다고 판단하면 그때 검색한다.

DB Schema가 필요하면 그때 읽는다.

즉 Context를 저장소의 Mirror가 아니라 **현재 판단을 위한 Working Set**으로 본다.

## Context Selection에도 실패가 있다

Context Engine도 완벽하지 않다.

다음 실패가 가능하다.

### Missing Context

필요한 Source를 가져오지 못함.

### Irrelevant Context

관련 없는 정보가 너무 많이 들어감.

### Stale Context

오래된 정보가 갱신되지 않음.

### Conflicting Context

서로 다른 Version이 동시에 들어옴.

### Unsafe Context

Untrusted Tool Result나 민감 데이터가 그대로 들어옴.

### Oversized Context

Attention과 Cost를 불필요하게 사용.

따라서 Context Policy도 Eval 대상이 된다.

## Context는 Model에 대한 API다

Tool을 Agent-Computer Interface라고 볼 수 있다면 Context Engine은 반대 방향의 Interface라고 볼 수 있다.

~~~text
External World
      ↓
Context Engine
      ↓
Model
      ↓
Tool Interface
      ↓
External World
~~~

Context Engine은 외부 세계를 Model이 판단 가능한 형태로 Projection한다.

Tool Interface는 Model의 결정을 외부 세계의 Action으로 변환한다.

Agent Harness는 이 두 Interface 사이의 Loop를 제어한다.

## 이 장에서 가져갈 것

Context를 많이 넣는 것은 저장을 잘하는 것과 다르다.

Agent가 오래 실행될수록 Context와 Durable State를 분리해야 한다.

~~~text
Durable State
      ↓
Relevant Projection
      ↓
Current Context
      ↓
Model Decision
~~~

Context Engineering의 핵심 질문은 다음이다.

> 지금 이 Decision을 위해 Model이 반드시 알아야 하는 것은 무엇인가?

다음 장에서는 반대 방향을 본다.

Model이 결정을 내린 뒤 실제 환경에 어떻게 Action을 표현할 것인가. Tool을 단순 API Wrapper가 아니라 Agent-Computer Interface로 설계하는 이유를 살펴본다.

## 주요 근거

- Anthropic, Effective Context Engineering for AI Agents
- Anthropic, Effective Harnesses for Long-running Agents
- OpenAI Agents SDK Sessions / Sandbox Memory
- research/topics/02-context-state-memory.md
- research/topics/09-state-memory-taxonomy.md
