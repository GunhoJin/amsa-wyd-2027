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
