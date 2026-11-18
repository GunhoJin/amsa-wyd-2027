# PC 감시 (새 수정요청·문의 즉시 처리, Windows)

```
PC 감시 스크립트 (1분마다)
   └─ 접수 웹 앱(Intake.gs, kind=watch, op=latest) ─ 최신 ID만 확인 (개인정보 없음)
        새 글 있으면 ─▶ op=rows 로 시트 받기 (.watch/rows.json, 처리 후 삭제)
                     ─▶ Claude Code (파일 읽기·쓰기만 허용) 가 PROMPT.md 대로 수정·기록
                     ─▶ 허용 파일 외 변경은 되돌림 → 커밋·push (Cloudflare 자동 배포)
                     ─▶ op=report 로 결과 메일 (담당자 본인에게만)
```

## 설치 (한 번)
1. **Git, Claude Code 설치**: Git for Windows 설치 후, PowerShell에서 `irm https://claude.ai/install.ps1 | iex` → `claude` 실행해 로그인.
2. **저장소 클론**: `git clone https://github.com/GunhoJin/amsa-wyd-2027.git` (push 할 수 있게 GitHub 로그인. 처음 push 때 창이 뜨면 로그인)
3. **감시 등록**: `cd amsa-wyd-2027\tools\pc-watcher` → `powershell -ExecutionPolicy Bypass -File .\install.ps1` → 화면에 나온 **키 복사**
4. **Apps Script 갱신**: 시트 › 확장 프로그램 › Apps Script
   - `Intake.gs` 내용을 저장소의 새 버전으로 바꿔 붙여넣기
   - 프로젝트 설정(⚙) › 스크립트 속성 › `WATCH_KEY` = 3번 키
   - 배포 › 배포 관리 › 수정(연필) › 버전: 새 버전 › 배포 (주소는 그대로)
5. **확인**: `.\watch.ps1 -Test` → `연결 확인: {"ok":true,...}` 이면 성공 → `Start-ScheduledTask -TaskName 'AmsaWYD 사이트 감시'`

## 운영
- 기록: `.watch\watch.log` (저장소 폴더 안, git 제외)
- 지금 한 번 처리: `.\watch.ps1 -Once`
- 끄기: `.\install.ps1 -Remove`
- PC가 꺼져 있을 때는 클라우드 예약 작업이 예비로 처리 (같은 기록 파일로 중복 방지)
- 실패하면 30분 뒤 다시 시도. 허용되지 않은 파일이 바뀌면 되돌리고 "자동 처리 중단" 메일을 보냄
