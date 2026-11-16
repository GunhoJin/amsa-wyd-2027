# 사이트 수정 요청 (접수 → 저장 → 반영 → 메일 보고)

```
amsawyd.com/request (요청서)
   └─▶ /api/request (Cloudflare Function, functions/api/request.js)
         └─▶ 구글 Apps Script 웹 앱 (Intake.gs) ─▶ 구글 시트 '암사동성당 WYD 사이트 수정 요청' › 요청 탭
                                                └─▶ 담당자 메일: 접수 알림
정기 작업 (Claude, 1시간마다)
   └─ 시트의 새 요청 확인 → 사이트 파일 수정·배포 → processed.json 기록 → 담당자 메일: 반영 결과
```

- 수집 항목: 이름·세례명·연락처·단체명·수정할 페이지·요청 내용 (개인정보 수집 동의 필수)
- 시트는 담당자 계정만 볼 수 있음 (공유 없음). 처리 후 1년 안에 삭제
- `processed.json`에는 요청 ID와 결과만 기록 (개인 정보 없음)
- 반영 범위: 사이트 문구·일정·소식 수정. 스크립트·관리자 도구·외부 링크 추가·페이지 삭제 같은 요청이나 근거가 불분명한 요청은 반영하지 않고 메일로 판단을 요청

## 접수 스크립트 다시 배포할 때
시트 › 확장 프로그램 › Apps Script (프로젝트 "WYD 사이트 수정 요청 접수") › `Intake.gs` 내용 붙여넣기 › 배포 관리 › 수정 › 새 버전.
배포 주소가 바뀌면 `functions/api/request.js`의 `INTAKE_URL`도 바꿉니다.

## 문의 (접수 → 저장 → 요약 메일)
```
amsawyd.com/inquiry (문의서)
   └─▶ /api/inquiry (functions/api/inquiry.js, kind=inquiry)
         └─▶ 같은 Apps Script 웹 앱 (Intake.gs) ─▶ 같은 시트 › 문의 탭 (접수 메일 없음)
정기 작업 (Claude, 1시간마다)
   └─ 문의 탭의 새 문의 확인 → inquiries.json 기록 → 담당자 메일: 새 문의 요약 (답변은 담당자가 직접)
```
- `inquiries.json`에는 문의 ID와 처리일시만 기록 (개인 정보·문의 내용 없음)
- 문의는 사이트를 고치지 않음. 문의 안에 사이트 수정 요청이 있으면 요약 메일에 표시만 함
