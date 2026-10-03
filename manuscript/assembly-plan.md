# Manuscript Assembly Plan

기준일: 2026-10-02

## 목표

현재 `chapters/*/draft.md`를 출판 원고 구조로 조립한다.

Draft 원본을 바로 삭제하거나 덮어쓰지 않는다.

## 구조

~~~text
manuscript/
  README.md
  frontmatter.md
  part-01.md
  part-02.md
  part-03.md
  part-04.md
  part-05.md
  part-06.md
  part-07.md
  epilogue.md
  references.md
  freshness-checklist.md
~~~

## Assembly 원칙

### 1. Draft는 Source
`chapters/*/draft.md`를 source manuscript로 유지한다.

### 2. Part 파일은 Publication View
Part 파일에서는 다음을 추가한다.
- Part opening
- chapter ordering
- source note
- cross-reference
- references

### 3. Claim-level Source Note
planning/source-catalog.md의 source id를 사용한다.

예:

~~~text
Model Capability와 Agent Capability는 동일하지 않다. [B-AGENT-CAPABILITY]

SWE-agent는 Agent-Computer Interface 설계가 coding-agent 성능에 영향을 줄 수 있음을 보였다. [S-SWE-ACI]
~~~

### 4. Book Synthesis를 Citation처럼 위장하지 않는다
B-* id는 외부 evidence가 아니라 저자의 framework임을 명확히 한다.

### 5. Publication-time Marker
변동성이 높은 문장에는 다음 marker를 둘 수 있다.

~~~text
<!-- freshness: S-MCP-2026-07 -->
~~~

출간 전 자동/수동 검토에서 제거한다.

## 조립 순서

1. Frontmatter
2. Part I~III
3. Part IV~V
4. Part VI~VII
5. Epilogue
6. References
7. Freshness checklist
8. 전체 cross-reference 검증

## 완료 기준

- 25개 장 + Epilogue 포함
- 모든 "주요 근거"가 source id로 연결됨
- B-* synthesis와 외부 evidence 분리
- Part 간 cross-reference 정상
- freshness marker 목록화
- Draft와 Manuscript 간 누락 chapter 없음
