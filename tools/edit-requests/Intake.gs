/**
 * 암사동성당 WYD 사이트 — 수정 요청 접수 (구글 스프레드시트에 붙여 쓰는 Apps Script 웹 앱)
 * - amsawyd.com/request 의 신청서 → /api/request (Cloudflare) → 이 웹 앱(doPost) → 시트에 한 줄 저장 + 담당자에게 접수 메일
 * - 배포: 실행 계정 = "나", 액세스 권한 = "모든 사용자"  (요청을 받기만 하고, 시트 내용은 돌려주지 않음)
 * - 저장된 요청은 정기 작업이 읽어서 사이트에 반영하고, 반영 결과를 담당자 메일로 보냅니다.
 * - 문의(kind=inquiry): amsawyd.com/inquiry → /api/inquiry → 같은 웹 앱 → '문의' 탭에 저장
 *   (접수 메일은 보내지 않음. 정기 작업이 새 문의를 모아 요약 메일로 보냄)
 */

const SHEET = '요청';
const HEAD = ['ID', '접수일시', '이름', '세례명', '연락처', '단체명', '페이지', '요청내용'];
const Q_SHEET = '문의';
const Q_HEAD = ['ID', '접수일시', '이름', '세례명', '연락처', '단체명', '분류', '문의내용'];
const LIMIT = { name: 40, baptism: 40, phone: 30, team: 60, page: 60, topic: 60, content: 3000 };

function sheet_(name, head) {
  name = name || SHEET; head = head || HEAD;
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = name === SHEET ? ss.getSheets()[0] : ss.insertSheet(name);
    sh.setName(name);
  }
  if (sh.getLastRow() === 0 || String(sh.getRange(1, 1).getValue()) !== 'ID') {
    sh.clear();
    sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}

const out_ = o => ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
const clip_ = (s, n) => String(s || '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim().slice(0, n);

function doPost(e) {
  try {
    const p = (e && e.parameter) || {};
    if (p.website) return out_({ ok: true });                       // 스팸 방지용 숨은 칸
    const inquiry = p.kind === 'inquiry';
    const v = {
      name: clip_(p.name, LIMIT.name), baptism: clip_(p.baptism, LIMIT.baptism),
      phone: clip_(p.phone, LIMIT.phone), team: clip_(p.team, LIMIT.team),
      page: clip_(p.page, LIMIT.page), topic: clip_(p.topic, LIMIT.topic), content: clip_(p.content, LIMIT.content),
    };
    if (!v.name || !v.phone || !v.content) return out_({ ok: false, error: inquiry ? '이름·연락처·문의 내용은 꼭 적어 주세요.' : '이름·연락처·요청 내용은 꼭 적어 주세요.' });

    // 짧은 시간에 몰리는 요청 막기 (1분에 10건)
    const cache = CacheService.getScriptCache();
    const n = Number(cache.get('rate') || 0);
    if (n >= 10) return out_({ ok: false, error: '요청이 많습니다. 잠시 후 다시 보내 주세요.' });
    cache.put('rate', String(n + 1), 60);

    const lock = LockService.getScriptLock();
    lock.waitLock(15000);
    let id;
    try {
      const sh = inquiry ? sheet_(Q_SHEET, Q_HEAD) : sheet_();
      const now = new Date();
      id = (inquiry ? 'Q' : 'R') + Utilities.formatDate(now, 'Asia/Seoul', 'yyMMdd-HHmmss') + '-' + Math.floor(Math.random() * 900 + 100);
      // 시트 수식으로 해석되지 않도록 앞에 ' 를 붙임
      const safe = s => /^[=+\-@]/.test(s) ? "'" + s : s;
      sh.appendRow([id, now, safe(v.name), safe(v.baptism), safe(v.phone), safe(v.team), safe(inquiry ? v.topic : v.page), safe(v.content)]);
    } finally {
      lock.releaseLock();
    }

    if (inquiry) return out_({ ok: true, id: id });                 // 문의는 정기 작업이 요약 메일로 보고

    // 담당자(이 스크립트 소유자)에게 접수 알림
    try {
      MailApp.sendEmail({
        to: Session.getEffectiveUser().getEmail(),
        subject: '[암사동성당 WYD] 수정 요청 접수 ' + id,
        body: [
          '수정 요청이 접수되었습니다. 정기 작업이 확인 후 반영하고 결과를 다시 보내 드립니다.', '',
          'ID: ' + id, '이름: ' + v.name + (v.baptism ? ' ' + v.baptism : ''), '연락처: ' + v.phone,
          '단체: ' + (v.team || '-'), '페이지: ' + (v.page || '-'), '', '요청 내용:', v.content,
        ].join('\n'),
      });
    } catch (err) { /* 메일 실패해도 접수는 유지 */ }

    return out_({ ok: true, id: id });
  } catch (err) {
    return out_({ ok: false, error: '접수 중 문제가 생겼습니다. 잠시 후 다시 시도해 주세요.' });
  }
}

function doGet() {
  return out_({ ok: true, service: 'amsawyd edit requests' });
}

/** 처음 한 번 실행: 시트 머리글을 만들고 메일 권한을 승인합니다 (편집기에서 ▶ 실행) */
function setup() {
  sheet_();
  sheet_(Q_SHEET, Q_HEAD);
  MailApp.getRemainingDailyQuota();
}
