# 영문판 생성 도구

한국어 페이지(`<page>.html`)에서 영문판(`en/<page>.html`)을 만든다. `en/*.html`은 직접 고치지 않는다.

한국어 문구를 고친 뒤 (저장소 루트에서):

1. `python tools/en-build/build.py --check` — 번역표에 없는 한국어 문구가 나오면
2. `tools/en-build/tr/<page>.json`에 `"한국어 문구": "English"`를 추가 (바뀐 옛 문구 줄은 지워도 됨). 영어에는 ASCII 따옴표 대신 ‘ ’ “ ”를 쓴다.
3. `python tools/en-build/build.py` — 영문판 생성. 모든 페이지가 `OK`이고 "남은 한국어"가 없어야 한다.
4. `node tools/en-build/prerender.js` 와 `node tools/en-build/prerender.js en` — 프로그램·참여하기의 미리 채운 본문 갱신.

- 작은따옴표 문자열·CSS `content:` 안의 한국어는 `tr/<page>.raw.json`(번역 전에 통째로 바꿈)에 넣는다.
- 한국어를 일부러 남길 코드(예: 순례길 네이버 지도 검색 이름)는 `tr/<page>.post.json`.
- 언어 전환 스위치(한/EN)·hreflang: `python tools/en-build/lang.py` (디자인은 `lsw.py`).
- 폼 선택지 값은 영문판에서도 한국어로 보낸다(접수 시트·정기 작업 호환).
- 화면 테마(라이트·다크·시스템, 기본은 기기 설정): `python tools/en-build/theme.py` 후 `build.py`. 다크 전용으로 적힌 색(흰색·반투명 흰색·금색 등)을 테마 변수로 바꾸고 라이트 색표·메뉴 안 테마 선택을 넣는다. 홈 첫 화면은 라이트에서 사진·손·지구본의 명암을 뒤집어 밝게 보인다. 페이지별 라이트 색표(홀리마켓 크리스마스 색 등)는 `PAGE_LIGHT`, 라이트에서도 어둡게 둘 부분은 `SCOPES`.
- 테마 주의: 색은 `var(--fg)`·`rgba(var(--fg-rgb),.5)`·`var(--gold)` 같은 변수로 쓴다. 쉼표로 묶은 선택자에 테마 조건을 붙일 땐 `pre()`로 모두에 붙인다(첫 선택자만 붙으면 라이트 전용 효과가 다크에 걸림). 홈(`index.html`)은 `</body>`가 없어 스크립트를 파일 끝에 붙인다.
- 줄바꿈 정리: 영문판도 한국어판의 「줄바꿈 정리」 스크립트를 그대로 물려받는다. 묶음 태그는 `<nw-x>`(다른 `span` 스타일과 겹치지 않게).
- 확인: 바꾼 뒤 라이트·다크 둘 다 휴대폰(390)·PC(1280) 폭에서 JS 오류·가로 넘침·글자 대비를 본다. 다크는 이전 커밋과 화면이 같아야 한다.
- 순서: 한국어 페이지 수정 → (`lang.py` · `theme.py`는 구조를 바꿀 때만) → `build.py` → `prerender.js` 두 번.
