<div align="center">

# ✝️ 암사동성당 WYD 2027

**서울에서, 세계의 청년과 함께.**

2027 서울 세계청년대회(World Youth Day)를 향한 1년 —<br>
암사동성당 청년과 중고등부가 기도와 만남으로 함께 준비합니다.

[![사이트 바로가기](https://img.shields.io/badge/사이트-amsa--wyd--2027.pages.dev-00A1DB?style=for-the-badge)](https://amsa-wyd-2027.pages.dev/)
[![본대회](https://img.shields.io/badge/본대회-2027.8.3~8.8-FFD27A?style=for-the-badge&labelColor=101216)](https://wydseoul.org/)

> “용기를 내어라! 내가 세상을 이겼다” (요한 16,33)

</div>

---

## 🌐 페이지

| 페이지 | 내용 | 주소 |
|---|---|---|
| **홈** | 회전 지구본(역대 WYD 개최지·서울 2027), D-day, 주제 성구, 공식 앱 내려받기 | [`/`](https://amsa-wyd-2027.pages.dev/) |
| **소개** | 교황의 초대, 주제 성구, 로고와 공식 색, 수호성인 5위, 지구를 위한 WYD, 대회 발자취 | [`/about`](https://amsa-wyd-2027.pages.dev/about) |
| **1년 일정** | 본당위원회(P.O.C.) 조직, 매월 반복 기도, 본대회 주간, WYD 십자가 순례, 월별 일정 | [`/plan`](https://amsa-wyd-2027.pages.dev/plan) |
| **프로그램** | WYD를 향한 영적 순례 여정 — 지난·진행 중·예정 프로그램 (날짜로 자동 분류) | [`/program`](https://amsa-wyd-2027.pages.dev/program) |
| **홀리마켓** | 12.27 성탄 홀리마켓 — 12사도 부스 선점 현황, 참여 원칙, 준비 일정 | [`/market`](https://amsa-wyd-2027.pages.dev/market) |
| **참여하기** | 순례길 참여 · 홈스테이 신청 (모집 상태별 신청 버튼) | [`/join`](https://amsa-wyd-2027.pages.dev/join) |
| **순례길** | 천주교 서울 순례길 3개 코스·24개 순례지 노선도, 순례지별 지도 링크 | [`/pilgrim`](https://amsa-wyd-2027.pages.dev/pilgrim) |

같은 내용이 GitHub Pages에도 배포됩니다 → <https://gunhojin.github.io/amsa-wyd-2027/>

## 🗂 구성

```
.
├── index.html        # 홈 — 지구본·두 손·유리 카드 히어로, 공식 앱 버튼
├── about.html        # 소개
├── plan.html         # 1년 일정
├── pilgrim.html      # 순례길
├── program.html      # 프로그램 (영적 순례 여정)
├── market.html       # 성탄 홀리마켓
├── join.html         # 참여하기 (순례길 참여·홈스테이 신청)
├── prog-*.jpg        # 프로그램 포스터
├── bg*.png           # 배경 이미지 (휴대폰·태블릿·데스크톱)
├── hands.png         # 두 손 이미지
└── *-mask-*.svg      # 손 이미지 가장자리 마스크
```

빌드 과정이 없는 순수 HTML·CSS·JavaScript입니다. 파일을 고치고 `main`에 push하면 1분 안에 사이트에 반영됩니다.

## ✏️ 내용 고치기

자주 바꾸는 내용은 각 파일 안의 데이터 목록에 모여 있습니다.

| 바꿀 내용 | 파일 | 위치 |
|---|---|---|
| 월별 일정·영성기획팀 프로그램 | `plan.html` | `const MONTHS` |
| WYD 십자가 순례 일정 | `plan.html` | `const CROSS` |
| 준비 시작일·본대회 날짜 | `plan.html` | `START`, `WYD` |
| 지구본의 역대 개최지 | `index.html` | `const HOSTS` |
| 홈 문구·주제 성구 | `index.html` | `const COPY` |
| 프로그램 추가·수정 | `program.html` | `const PROGRAMS` (from/to 날짜로 지난·진행 중·예정 자동 분류) |
| 순례길 코스·순례지 | `pilgrim.html` | `const COURSES` |
| 홀리마켓 부스 선점·일정 | `market.html` | `const BOOTHS` (team에 단체명), `const STEPS` |
| 신청 열기·마감 | `join.html` | `const JOINS` — `status`를 `open`/`closed`로, `url`에 신청서 주소 |

## 🚀 배포

| 곳 | 주소 | 방식 |
|---|---|---|
| Cloudflare Pages | <https://amsa-wyd-2027.pages.dev> | `main` push 시 자동 배포 (빌드 명령 없음, 출력 `/`) |
| GitHub Pages | <https://gunhojin.github.io/amsa-wyd-2027/> | `main` 브랜치 루트 |

로컬에서 미리 보기:

```bash
python -m http.server 8000
# http://localhost:8000
```

## 📚 자료 출처

- [2027 서울 세계청년대회 공식 홈페이지](https://wydseoul.org) — 대회 소개, 주제 성구, 로고·공식 색, 수호성인, 대회 발자취, WYD 십자가 순례 일정
- [내 손안에 서울](https://mediahub.seoul.go.kr/archives/1181240) — 천주교 서울 순례길 코스와 순례지
- 암사동성당 WYD 본당위원회(P.O.C.) 기획안 — 본당 조직, 영성기획팀 월별 프로그램
- 지구본 육지 데이터 — [Natural Earth](https://www.naturalearthdata.com/) (world-atlas)
- 히어로 레이아웃 — Originkit Hero 24, 타이핑 인트로 — Originkit Type Sequence

> 대회 명칭과 로고는 재단법인 2027 서울 WYD 조직위원회의 사용 안내에 따라 홍보·사목 목적으로만 사용합니다.

---

<div align="center">
<sub>암사동성당 영성기획 파트</sub>
</div>
