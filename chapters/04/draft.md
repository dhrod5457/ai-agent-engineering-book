# 4장. Context는 저장소가 아니다

에이전트가 저장소를 잘 이해하지 못하면 가장 먼저 떠올리기 쉬운 해결책은 더 많은 정보를 넣는 것이다. README를 넣는다. 설계 구조 문서를 넣는다. 최근 커밋을 넣는다. 관련 이슈를 넣는다. 도구 설명을 전부 넣는다. 이전 대화도 가능한 한 많이 유지한다. 처음에는 좋아 보인다. 모델이 더 많은 사실을 볼 수 있으니 판단도 더 좋아질 것 같다. 하지만 오래 실행되는 에이전트에서는 이 방식이 빠르게 한계에 부딪힌다. 오래된 정보와 최신 정보가 섞이고, 중요한 사실이 긴 로그 안에 묻히고, 도구의 입력 형식만으로 상당한 컨텍스트(Context: 모델에 전달하는 정보)를 사용한다. 결국 모델이 필요한 정보를 "가지고는 있지만 제대로 사용하지 못하는" 상황이 생긴다.

컨텍스트 설계는 무엇을 더 넣을지보다 **지금 이 판단에 무엇이 필요한지 고르는 문제**에 가깝다.

## Context는 현재 Inference의 입력이다

이 책에서는 컨텍스트를 다음처럼 좁게 사용한다.

> **컨텍스트는 현재 한 번의 모델 실행에 실제로 들어가는 정보다.**

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

저장소 전체가 컨텍스트인 것은 아니다. Database 전체가 컨텍스트인 것도 아니다. 메모리 전체도 컨텍스트가 아니다. 그중 현재 판단에 필요한 일부만 모델 입력으로 들어간다. 이 구분이 중요한 이유는 컨텍스트 윈도(Context Window: 모델이 한 번에 입력받을 수 있는 정보의 범위)가 저장장치가 아니기 때문이다.

## More Context가 자동으로 Better Agent를 만들지는 않는다

컨텍스트가 너무 적으면 필요한 정보가 빠진다. 그렇다고 가능한 모든 정보를 넣으면 다른 문제가 생긴다.

### Attention Dilution

중요한 정보와 중요하지 않은 정보가 같은 입력 공간을 차지하려고 경쟁한다. 예를 들어 에이전트가 하나의 Java Service Method를 수정하려는데 다음을 모두 넣었다고 하자.

- 전체 300개 Source File
- 모든 Test Log
- 80개 도구의 입력 형식
- 최근 50개 커밋
- 200개의 이슈
- 전체 대화 기록

관련 정보가 컨텍스트 안에 존재한다는 사실만으로 판단 품질이 자동으로 높아지지는 않는다.

### Stale Context

컨텍스트 안에 들어간 정보는 입력 시점의 상태 사본(Snapshot: 특정 시점의 상태 사본)이다. 외부 정보 원본이 바뀌어도 기존 컨텍스트는 자동으로 갱신되지 않는다.

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

오래 실행되는 에이전트에서는 이 문제가 중요해진다.

### Conflicting Context

같은 사실에 대해 여러 버전이 동시에 들어올 수 있다.

예를 들어:

~~~text
Old README:
API endpoint = /v1/users

Current Source:
API endpoint = /v2/users
~~~

모델이 어떤 정보를 우선해야 하는지 명확하지 않다면 더 많은 컨텍스트가 오히려 혼란을 만든다.

### Context Cost

컨텍스트가 커지면 토큰 비용과 응답 지연 시간이 증가한다. 하지만 비용보다 중요한 것은 **불필요한 정보가 Agent Decision Surface를 넓힌다는 점**이다.

## Context는 State의 Projection이다

앞 장에서 하네스(Harness: 모델 실행과 도구 사용을 제어하는 계층)가 상태와 분리돼야 한다고 설명했다. 여기서 그 관계를 조금 더 구체화할 수 있다.

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

모델에게 이벤트 이력 전체를 매 차례 넣을 필요는 없다.

현재 필요한 정보가 다음과 같다면:

- 현재 목표
- 방금 실패한 도구 실행 결과
- 수정 대상 파일
- relevant Test
- 현재 승인 상태

그것만 필요한 정보를 골라 구성할 수 있다. 즉 상태는 실행이 끝나도 남도록 보존하고, 모델에 전달하는 정보는 현재 판단에 맞춰 일시적으로 구성한다. 이 원칙은 오래 실행되는 에이전트에서 특히 중요하다.

## Context Assembly는 하나의 Engine이다

단순 에이전트에서는 컨텍스트를 문자열을 이어 붙여 만들 수 있다. 운영 에이전트에서는 여러 정보 원본을 조합하게 된다.

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

이때 중요한 것은 "모두 넣는다"가 아니라 각 정보 원본마다 포함 기준을 가지는 것이다.

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

이런 선택 책임을 이 책에서는 컨텍스트 구성 계층이라는 개념으로 설명한다. 역시 특정 제품 이름이 아니라 책임을 설명하기 위한 용어다.

## Progressive Context

처음부터 모든 정보를 넣기보다 필요한 만큼 확장하는 방식이 유용하다. 예를 들어 코드 작업 에이전트가 처음에는 다음만 알 수 있다.

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

형태로 컨텍스트를 확장한다. 이 방식의 장점은 단순 토큰 절감이 아니다. 에이전트가 무엇을 필요로 했는지 실행 추적 기록(Trace)로 남기기 쉽다. 또 저장소가 커져도 컨텍스트 크기를 상대적으로 제어하기 쉽다.

## Tool Schema도 Context다

도구를 많이 제공하면 에이전트가 더 많은 기능을 얻는다. 하지만 각 도구는 대개 다음 정보를 컨텍스트에 추가한다.

- name
- description
- input schema
- output contract

도구가 5개일 때와 100개일 때 모델이 선택할 수 있는 행동의 범위는 다르다. 따라서 도구 목록 전체를 항상 노출하는 것이 최선이라고 가정하지 않는다. 작업과 정책에 따라 사용 가능한 도구 중 필요한 것만 골라 제공할 수 있다.

~~~text
All Capabilities
      ↓
Eligibility / Policy
      ↓
Relevant Tool Set
      ↓
Current Context
~~~

이 지점은 다음 장의 도구 설계와 직접 연결된다.

## Tool Result도 Context를 오염시킬 수 있다

도구는 신뢰된 코드일 수 있다. 하지만 도구가 읽어온 데이터까지 신뢰된 것은 아니다. 예를 들어 Web Tool이 외부 페이지를 읽었다면 결과 안에 다음이 포함될 수 있다.

- 오래된 정보
- 악성 외부 입력에 악성 지시를 끼워 넣는 공격(Prompt Injection)
- 과도하게 긴 HTML
- 사용자 데이터
- irrelevant navigation text

따라서 도구 실행 결과를 그대로 모델의 컨텍스트에 넣는 것이 항상 안전하지 않다. 필요할 수 있는 처리는 다음과 같다.

- size limit
- structured extraction
- redaction
- 출처와 생성 이력
- trust label
- summarization
- relevant section selection

도구 출력의 필터링은 컨텍스트 설계이면서 동시에 보안 경계가 될 수 있다.

## Conversation History는 State 전체가 아니다

대화형 에이전트에서는 대화 기록이 중심처럼 보인다. 그래서 모든 상태를 메시지로 표현하려는 설계가 생긴다.

예:

~~~text
assistant:
"Tool A 실행 완료"

assistant:
"Approval 대기 중"

assistant:
"File X 생성"
~~~

하지만 대화 기록만으로는 다음을 안정적으로 표현하기 어렵다.

- Tool Execution ID
- Idempotency Key
- Approval Object
- 산출물의 검증값
- 원본 버전
- Runtime Failure
- 재시도 횟수

이 정보는 모델이 읽을 수도 있지만 그보다 먼저 시스템이 정확하게 관리해야 한다. 따라서 대화 기록은 실행 상태 전체가 아니라 컨텍스트를 구성하는 정보 원본 중 하나로 보는 편이 낫다. 도구 실행 ID, 승인, 산출물의 검증값처럼 시스템이 정확하게 관리해야 하는 사실은 별도의 구조화된 상태로 유지한다.

## Compaction은 유용하지만 한계가 있다

오래 실행되는 에이전트에서는 컨텍스트가 계속 커진다. 가장 흔한 대응 중 하나가 컨텍스트 압축(Compaction: 입력 정보를 줄이는 압축)이다.

예를 들어:

~~~text
Turns 1~50
      ↓
Summary
      ↓
Turns 51~current
~~~

컨텍스트 압축은 필요한 기법이다. 하지만 영속 상태(Durable State: 실행이 끝나도 보존되는 상태)를 대체하지 않는다. 요약에는 세부 정보가 사라질 수 있다. 예를 들어 다음 정보가 요약에서 빠질 수 있다.

- 어떤 도구 호출이 실제 성공했는가.
- 정확히 어떤 파일이 수정됐는가.
- 어떤 승인이 아직 Pending인가.
- 어떤 원본 버전을 봤는가.
- 다음 실행에서 다시 하면 안 되는 외부 상태 변화(Side Effect: 외부 상태에 생기는 변화)는 무엇인가.

따라서:

~~~text
Compaction
= Context Optimization

Checkpoint / Event History
= Execution Continuity
~~~

로 분리한다.

## Context Reset이 필요할 때

컨텍스트를 계속 이어가는 것이 항상 좋은 것도 아니다. 다음 상황에서는 새로운 컨텍스트를 만드는 편이 나을 수 있다.

- Task Phase가 완전히 바뀜
- 이력이 너무 길어짐
- 오래된 가정이 많이 남음
- 다른 전문 역할의 에이전트로 작업 인계
- 모델 교체 / Session Restart
- 보안 경계 변경

이때 필요한 상태만 다시 필요한 정보를 골라 구성한다.

~~~text
Old Context
   ↓ discard

Durable State
   ↓ re-project

Fresh Context
~~~

이 구조가 가능하려면 중요한 정보가 컨텍스트 밖에도 존재해야 한다. 다시 에이전트 상태 관리 계층(Agent State Plane: 실행이 중단돼도 목표와 진행 상태를 보존하는 계층)과 연결된다.

## 작은 예: Repository 수정 Agent

목표:

> UserService의 timeout 처리 오류를 수정하라.

나쁜 컨텍스트 전략:

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

에이전트가 설정이 필요하다고 판단하면 그때 검색한다. 데이터베이스 구조가 필요하면 그때 읽는다. 즉 컨텍스트를 저장소의 복제본이 아니라 **현재 판단을 위한 현재 작업에 필요한 정보 묶음**으로 본다.

## Context Selection에도 실패가 있다

컨텍스트 구성 계층도 완벽하지 않다. 다음 실패가 가능하다.

### Missing Context

필요한 정보 원본을 가져오지 못함.

### Irrelevant Context

관련 없는 정보가 너무 많이 들어감.

### Stale Context

오래된 정보가 갱신되지 않음.

### Conflicting Context

서로 다른 버전이 동시에 들어옴.

### Unsafe Context

Untrusted Tool Result나 민감 데이터가 그대로 들어옴.

### Oversized Context

Attention과 비용을 불필요하게 사용. 따라서 컨텍스트 구성 정책도 평가 대상이 된다.

## Context는 Model에 대한 API다

도구를 Agent-Computer Interface라고 볼 수 있다면 컨텍스트 구성 계층은 반대 방향의 인터페이스라고 볼 수 있다.

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

컨텍스트 구성 계층은 외부 세계의 정보를 현재 판단에 필요한 형태로 필요한 정보를 골라 구성한다. 도구 인터페이스는 모델의 결정을 외부 행동으로 연결하고, 하네스는 이 두 인터페이스 사이의 반복 실행을 제어한다.

## 이 장에서 가져갈 것

컨텍스트를 많이 넣는 것은 저장을 잘하는 것과 다르다. 에이전트가 오래 실행될수록 컨텍스트와 영속 상태를 분리해야 한다.

~~~text
Durable State
      ↓
Relevant Projection
      ↓
Current Context
      ↓
Model Decision
~~~

컨텍스트 설계의 핵심 질문은 다음이다.

> 지금 이 판단을 위해 모델이 반드시 알아야 하는 것은 무엇인가?

다음 장에서는 반대 방향을 본다. 모델이 결정을 내린 뒤 실제 환경에 어떻게 행동을 표현할 것인가. 도구를 단순 API Wrapper가 아니라 Agent-Computer Interface로 설계하는 이유를 살펴본다.

## 주요 근거

- Anthropic, Effective Context Engineering for AI Agents
- Anthropic, Effective Harnesses for Long-running Agents
- OpenAI Agents SDK Sessions / Sandbox Memory
- research/topics/02-context-state-memory.md
- research/topics/09-state-memory-taxonomy.md
