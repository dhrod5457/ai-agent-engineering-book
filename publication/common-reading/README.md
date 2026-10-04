# 공통 독서 디자인 시안

이 책의 본문 기준은 `b6abea82394b54ce9e2058f95a9a11551d6be140`입니다. 원고는 수정하지 않았습니다.

`published-book/design`이 공통 스타일의 기준 원본입니다. 이 폴더의 CSS/JS는 동일한 파일의 검토용 사본이며, 기존 출판·연구 빌더와 원격 워크플로는 유지합니다.

공통 판형 176×250mm, PDF 본문 10pt/1.8, 화면 최대 42rem, 모바일 17px/1.8을 사용합니다. 표·코드는 화면에서 독립 가로 스크롤, PDF/EPUB에서는 긴 줄을 감쌉니다. 제목 계층과 장 순서, 본문·코드·사례·인용·검토 상태는 보존합니다.

여섯 권과 `published-book`의 `design/common-reading-20261004` 로컬 브랜치를 형제 폴더에 두고 `python3 publication/common-reading/preview.py`를 실행하면 고정 발행본에 디자인을 적용한 HTML·EPUB·PDF 시안을 생성합니다. 환경별 Chrome/Puppeteer 경로는 `CHROME_PATH`, `PUPPETEER_MODULE`로 지정합니다.

생성물은 `published-book/preview/common-reading-20261004/ai-agent-engineering-book/`에 있으며 기존 릴리스 파일을 덮어쓰지 않습니다. 발행에는 별도 승인과 검수 완료된 파일의 버전·해시 기록이 필요합니다.
