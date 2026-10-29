<div align="center">

# ✝️ 암사동성당 WYD 2027

**서울에서, 세계의 청년과 함께.**

2027 서울 세계청년대회(World Youth Day)를 향한 1년 —<br>
암사동성당 공동체가 기도와 만남으로 함께 준비합니다.

[![사이트 바로가기](https://img.shields.io/badge/사이트-amsawyd.com-00A1DB?style=for-the-badge)](https://amsawyd.com/)
[![본대회](https://img.shields.io/badge/본대회-2027.8.3~8.8-FFD27A?style=for-the-badge&labelColor=101216)](https://wydseoul.org/)
[![홀리마켓](https://img.shields.io/badge/성탄_홀리마켓-2026.12.20-B9A6FF?style=for-the-badge&labelColor=101216)](https://amsawyd.com/market)

> “용기를 내어라! 내가 세상을 이겼다” (요한 16,33)

</div>

---

## 🌐 페이지

| 페이지 | 내용 | 주소 |
|---|---|---|
| **홈** | 회전 지구본(역대 WYD 개최지·서울 2027), D-day, 주제 성구, 바로가기, 참여하기 버튼, 공식 앱 내려받기 | [`/`](https://amsawyd.com/) |
| **소개** | 교황의 초대, 주제 성구, 로고와 공식 색, 수호성인 5위, 지구를 위한 WYD, 대회 발자취 | [`/about`](https://amsawyd.com/about) |
| **1년 일정** | 본당위원회(P.O.C.) 조직, 매월 반복 기도, 본대회 주간, WYD 십자가 순례, 월별 일정 | [`/plan`](https://amsawyd.com/plan) |
| **순례길** | 천주교 서울 순례길 3개 코스·24개 순례지 노선도, 북촌·서소문·한강 해설 도보관광(무료) 예약 | [`/pilgrim`](https://amsawyd.com/pilgrim) |
| **프로그램** | WYD를 향한 영적 순례 여정 — 지난·진행 중·예정 프로그램 (날짜로 자동 분류) | [`/program`](https://amsawyd.com/program) |
| **참여하기** | 본당위원회 봉사자 모집(구글 폼) · 순례길 참여 · 홈스테이 · 홀리마켓 부스 신청 | [`/join`](https://amsawyd.com/join) |
| └ **성탄 홀리마켓** | 12.20 대림 제4주일 — 12사도 부스 선점 현황, 본부석·WYD 홍보부스, 구역, 참여 원칙, 준비 일정 | [`/market`](https://amsawyd.com/market) |

모든 페이지는 우측 상단 메뉴로 이동합니다. 각 페이지는 처음 열 때 제목을 타이핑하는 인트로가 한 번 나옵니다.

## 📌 지금 진행 상황

| 항목 | 상태 |
|---|---|
| 두 번째 여정 「우리의 기도를 장미꽃으로」 | 진행 중 · 10.31까지 (11.1부터 자동으로 지난 프로그램) |
| 본당위원회(P.O.C.) 봉사자 | **모집 중** |
| 성탄 홀리마켓 단체 부스 | 모집 예정 · 11.8 선점 신청 시작 |
| 홀리마켓 판매존 외부 신청 | 모집 예정 · 11.15 ~ 11.22 |
| 홈스테이 가정 | 모집 예정 · 11월 시작 |
| 순례길 참여 | 모집 예정 |

## ✏️ 내용 고치기

자주 바꾸는 내용은 각 파일 안의 데이터 목록에 모여 있습니다.

| 바꿀 내용 | 파일 | 위치 |
|---|---|---|
| 홈 문구·주제 성구 | `index.html` | `const COPY` |
| 지구본의 역대 개최지 | `index.html` | `const HOSTS` |
| 월별 일정·영성기획팀 프로그램 | `plan.html` | `const MONTHS` |
| WYD 십자가 순례 일정 | `plan.html` | `const CROSS` |
| 준비 시작일·본대회 날짜 | `plan.html` | `START`, `WYD` |
| 순례길 코스·순례지 | `pilgrim.html` | `const COURSES` |
| 프로그램 추가·수정 | `program.html` | `const PROGRAMS` — `from`/`to` 날짜로 지난·진행 중·예정 자동 분류, `img`가 있으면 포스터 카드 |
| 신청 열기·마감 | `join.html` | `const JOINS` — `status`를 `soon`/`open`/`closed`로, `url`에 신청서 주소 |
| 홀리마켓 부스 선점 | `market.html` | `const BOOTHS` — 선점한 단체명을 `team`에 입력 (예: `team:"레지오"`) |
| 홀리마켓 준비 일정 | `market.html` | `const STEPS` — 지난 단계는 흐리게, 다음 단계는 금색으로 자동 표시 |
| 숨겨 둔 참여 버튼 | 모든 페이지 | `[data-join]{display:none!important}` 한 줄 삭제 시 표시 |

### 새 소식을 올릴 때

1. 해당 페이지의 데이터 목록을 고칩니다.
2. `rss.xml` 맨 위에 `<item>`을 하나 추가합니다 (제목·링크·설명·날짜·고유 guid).
3. 페이지를 새로 만들었다면 `sitemap.xml`에 주소를 추가하고, 각 페이지의 메뉴(`.mn nav`)에도 링크를 넣습니다.

## 🔎 검색 노출

| 항목 | 내용 |
|---|---|
| 페이지 정보 | 페이지마다 `title`·`description`·`canonical`(amsawyd.com 기준) |
| 링크 미리보기 | Open Graph·Twitter 카드, 이미지 `og.jpg` (1200×630) |
| 검색엔진 파일 | [`robots.txt`](https://amsawyd.com/robots.txt) · [`sitemap.xml`](https://amsawyd.com/sitemap.xml) · [`rss.xml`](https://amsawyd.com/rss.xml) |
| 구글 서치 콘솔 | 도메인 속성 등록(DNS 소유 확인), 사이트맵 제출 |
| 네이버 서치어드바이저 | 메타 태그 소유 확인(`index.html`), 사이트맵·RSS 제출 |

## 🗂 구성

```
.
├── index.html        # 홈 — 지구본·두 손·유리 카드 히어로, 공식 앱 버튼
├── about.html        # 소개
├── plan.html         # 1년 일정
├── pilgrim.html      # 순례길
├── program.html      # 프로그램 (영적 순례 여정)
├── join.html         # 참여하기 (봉사자·순례길·홈스테이·홀리마켓 신청 카드)
├── market.html       # 성탄 홀리마켓 세부
├── prog-*.jpg        # 프로그램 포스터·현장 사진
├── og.jpg            # 카카오톡·SNS 링크 미리보기 이미지
├── robots.txt        # 검색엔진 안내 (사이트맵 위치)
├── sitemap.xml       # 검색엔진용 페이지 목록
├── rss.xml           # 소식 피드 (새 소식은 맨 위에 item 추가)
├── bg*.png           # 배경 이미지 (휴대폰·태블릿·데스크톱)
├── hands.png         # 두 손 이미지
└── *-mask-*.svg      # 손 이미지 가장자리 마스크
```

빌드 과정이 없는 순수 HTML·CSS·JavaScript입니다. 파일을 고치고 `main`에 push하면 1분 안에 사이트에 반영됩니다.

## 🚀 배포

| 곳 | 주소 | 방식 |
|---|---|---|
| **공개 주소** | <https://amsawyd.com> | Cloudflare Pages 커스텀 도메인 (www 포함) |
| Cloudflare Pages | <https://amsa-wyd-2027.pages.dev> | `main` push 시 자동 배포 (빌드 명령 없음, 출력 `/`) |
| GitHub Pages | <https://gunhojin.github.io/amsa-wyd-2027/> | `main` 브랜치 루트 |

주보·QR·홍보물에는 **amsawyd.com**을 사용합니다.

로컬에서 미리 보기:

```bash
python -m http.server 8000
# http://localhost:8000
```

## 📚 자료 출처

- [2027 서울 세계청년대회 공식 홈페이지](https://wydseoul.org) — 대회 소개, 주제 성구, 로고·공식 색, 수호성인, 대회 발자취, WYD 십자가 순례 일정
- [내 손안에 서울](https://mediahub.seoul.go.kr/archives/1181240) — 천주교 서울 순례길 코스와 순례지
- [VISIT SEOUL 서울도보해설관광](https://korean.visitseoul.net/walking-tour) — 북촌·서소문·한강 순례길 해설 코스
- 암사동성당 WYD 본당위원회(P.O.C.) 기획안 — 본당 조직, 영성기획팀 월별 프로그램
- 암사동성당 영성기획팀 회의록 — 프로그램, 성탄 홀리마켓 기획
- 지구본 육지 데이터 — [Natural Earth](https://www.naturalearthdata.com/) (world-atlas)
- 히어로 레이아웃 — Originkit Hero 24, 타이핑 인트로 — Originkit Type Sequence

> 대회 명칭과 로고는 재단법인 2027 서울 WYD 조직위원회의 사용 안내에 따라 홍보·사목 목적으로만 사용합니다.

---

<div align="center">
<sub>암사동성당 영성기획 파트</sub>
</div>
