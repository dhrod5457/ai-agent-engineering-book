# Source Note Conventions

기준일: 2026-10-02

출판 원고에서 Source를 단순 참고문헌 목록으로만 두지 않고, 주장 성격에 따라 표현을 구분한다.

## 1. Protocol / Official Documentation

표현 예:

> MCP 2026-07-28 specification에서는 protocol-level session을 제거하고 Tasks를 extension으로 분리했다.

기준:
- version/date를 함께 적는다.
- 출간 직전 freshness audit 대상이다.
- protocol fact를 일반 Agent Architecture 원칙으로 곧바로 확대하지 않는다.

## 2. Vendor Engineering / Production Case

표현 예:

> Anthropic이 공개한 long-running agent 사례에서는 session 간 progress artifact와 runtime continuity를 별도 engineering concern으로 다뤘다.

기준:
- "Anthropic은 이렇게 한다"보다 "공개 사례에서 관찰됐다"를 우선한다.
- vendor 내부 workload를 업계 일반 수치나 한계로 확대하지 않는다.
- product feature와 engineering principle을 분리한다.

## 3. Peer-reviewed / Established Research

표현 예:

> SWE-agent 연구는 ACI 설계가 coding agent 성능에 영향을 줄 수 있음을 보였다.

기준:
- task/environment를 함께 본다.
- benchmark result를 product-wide capability로 일반화하지 않는다.

## 4. Preprint / Emerging Research

표현 예:

> 2026년 preprint에서는 Version Conflict와 Decision Conflict를 구분하는 Selective Revalidation을 제안했다.

기준:
- 본문에서 preprint임을 명시한다.
- "증명했다"보다 "제안했다", "관찰했다", "보고했다"를 사용한다.
- controlled setting의 결과를 production standard로 표현하지 않는다.

## 5. Book Synthesis

표현 예:

> 이 책에서는 이러한 실행 연속성 책임을 Agent State Plane이라고 부른다.

기준:
- 외부 표준처럼 쓰지 않는다.
- 최소 2개 이상의 독립 source family에서 반복되는 responsibility를 종합한 경우에만 핵심 synthesis로 사용한다.
- synthesis와 source fact 사이에 문장 경계를 둔다.

현재 주요 synthesis:
- Agent State Plane
- Harness Debt
- Memory Write Gate
- AgentVersion
- R0~R4 illustrative control profile
- Agent-as-Tool / Handoff ownership distinction

## 6. Example / Thought Experiment

가상 예시는 실제 사례처럼 보이지 않게 한다.

표현:
- "가상의 두 Coding Agent를 비교해보자."
- "예를 들어 다음 구조를 생각해보자."

실제 incident처럼 단정하지 않는다.

## 7. Numeric Claims

숫자는 다음을 함께 기록한다.

- source date
- benchmark/release version
- task/environment
- metric
- sample / repeat count
- limitation

숫자만 떼어 일반 원칙의 근거로 쓰지 않는다.

## 8. Chapter End Sources

현재 각 장의 "주요 근거"는 Research Pointer다.

Manuscript Assembly 단계에서는:
- 절/문장별 source note
- 장 끝 References
를 연결할 수 있게 source id를 부여한다.

예:

~~~text
[S-MCP-2026-07]
[S-OSWORLD2]
[S-MEMPOISON]
[S-ANTHROPIC-HARNESS-2026]
~~~

최종 표기 형식은 Manuscript Assembly에서 고정한다.
