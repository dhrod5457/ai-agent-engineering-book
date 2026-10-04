# 공통 독서판 2026.10.04-preview.1

본문·코드·사례·인용·장 순서는 원고 커밋 `b6abea82394b54ce9e2058f95a9a11551d6be140`에서 보존했습니다. 새 디자인은 표지·목차·본문·코드·표·참고문헌·쪽번호 및 HTML 탐색을 공통화합니다. 원고의 검토 상태는 유지합니다.

[이 판의 PDF·EPUB·HTML](https://github.com/dhrod5457/ai-agent-engineering-book/releases/tag/2026.10.04-preview.1) · [여섯 권 보관소](https://github.com/dhrod5457/published-book/releases/tag/collection-2026-10-04.1).

`edition.json`에는 버전, 원고 파일 해시와 공통 스타일 해시가 있습니다. `python3 publication/common-reading/verify.py`로 보존 여부를 확인합니다. 실제 제작 기준은 형제 저장소 `published-book`의 `design` 및 `scripts/build_common_books.py`입니다. 기존 연구용 빌더와 과거 발행본은 보존합니다.

형제 `published-book`에서 `python3 scripts/build_common_books.py ai-agent-engineering-book`를 실행하고, `READING_OUT`을 설정해 `node scripts/build_reading_pdf.cjs ai-agent-engineering-book`를 실행합니다. `CHROME_PATH`, `PUPPETEER_MODULE`, `PYMUPDF_PATH`로 실행 도구 경로를 지정합니다. 검수 완료된 정확한 파일을 새 릴리스에 배포합니다.
