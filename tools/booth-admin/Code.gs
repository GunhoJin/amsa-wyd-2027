/**
 * 성탄 홀리마켓 부스 신청 승인 (관리자 전용)
 * - 구글 폼 응답 시트에 붙여 쓰는 Apps Script 웹 앱
 * - 배포: 실행 계정 = "웹 앱에 액세스하는 사용자", 액세스 권한 = "Google 계정이 있는 모든 사용자"
 *   → 이 스프레드시트 편집 권한이 있는 사람만 열고 처리할 수 있습니다 (외부 비공개)
 * - 승인된 부스만 '공개현황' 탭에 구역·단체·아이템으로 정리 → 웹에 게시(CSV) → amsawyd.com/market 에 표시
 *   (연락처·단체장 등 개인 정보는 공개현황 탭에 들어가지 않습니다)
 */

// ── 설정 ─────────────────────────────────────────────
// 구역별 부스 수 (amsawyd.com/market 과 같게 유지)
const CAPS = { exp: 4, snack: 6, market: 10 };
// 같은 아이템 최대 부스 수
const MAX_SAME_ITEM = 2;
// 폼 밖에서 이미 확정한 부스 (amsawyd.com/market 의 BOOTHS 와 같게) — 자리 수·같은 아이템 계산에 포함
const RESERVED = { exp: [], snack: [], market: [] };
// 처리할 수 있는 사람 (비우면 이 시트 편집자 누구나)
const ADMINS = [];
// 공개 탭 이름
const PUBLIC_SHEET = '공개현황';

// 폼 질문 → 내부 키 (질문 문구의 앞부분으로 찾음)
const FIELDS = [
  ['ts',      '타임스탬프'],
  ['team',    '단체명'],
  ['partner', '연합 단체'],
  ['leader',  '단체장'],
  ['phone',   '담당자 연락처'],
  ['type',    '부스 유형'],
  ['item1',   '운영 아이템 (1순위'],
  ['item2',   '운영 아이템 (2순위'],
  ['staff',   '부스 운영 인원'],
  ['power',   '전기 사용 기기'],
  ['request', '요청 사항'],
];
// 관리용 열 (응답 시트 오른쪽에 자동 추가)
const ADMIN_COLS = ['처리상태', '배정아이템', '처리메모', '처리자', '처리일시'];
const ZONE_OF = t => /체험/.test(t) ? 'exp' : /식음료|간식/.test(t) ? 'snack' : /판매/.test(t) ? 'market' : '';
const ZONE_NAME = { exp: '체험존', snack: '간식존(식음료)', market: '판매존' };

// ── 웹 앱 ───────────────────────────────────────────
function doGet() {
  const t = HtmlService.createTemplateFromFile('Admin');
  return t.evaluate()
    .setTitle('홀리마켓 부스 승인')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.DEFAULT);
}

function whoAmI_() {
  const email = Session.getActiveUser().getEmail() || '';
  if (ADMINS.length && ADMINS.indexOf(email) < 0) throw new Error('처리 권한이 없는 계정입니다: ' + (email || '(알 수 없음)'));
  return email;
}

// ── 시트 접근 ───────────────────────────────────────
function responseSheet_() {
  const ss = SpreadsheetApp.getActive();
  const sh = ss.getSheets().find(s => {
    const lc = s.getLastColumn();
    if (!lc) return false;
    const head = s.getRange(1, 1, 1, lc).getValues()[0].join('|');
    return head.indexOf('단체명') >= 0 && head.indexOf('부스 유형') >= 0;
  });
  if (!sh) throw new Error('폼 응답 시트를 찾지 못했습니다. 폼 응답을 이 스프레드시트에 연결했는지 확인하세요.');
  return sh;
}

function columns_(sh) {
  let lc = sh.getLastColumn();
  let head = sh.getRange(1, 1, 1, lc).getValues()[0].map(String);
  // 관리용 열이 없으면 오른쪽에 추가
  const missing = ADMIN_COLS.filter(c => head.indexOf(c) < 0);
  if (missing.length) {
    sh.getRange(1, lc + 1, 1, missing.length).setValues([missing]).setFontWeight('bold').setBackground('#fff3cd');
    head = head.concat(missing);
  }
  const col = {};
  FIELDS.forEach(([k, label]) => { const i = head.findIndex(h => h.indexOf(label) === 0); if (i >= 0) col[k] = i; });
  ADMIN_COLS.forEach(c => { col[c] = head.indexOf(c); });
  return { head, col };
}

const norm_ = s => String(s || '').replace(/\s+/g, '').toLowerCase();

function readAll_() {
  const sh = responseSheet_();
  const { col } = columns_(sh);
  const n = sh.getLastRow() - 1;
  const width = sh.getLastColumn();
  const vals = n > 0 ? sh.getRange(2, 1, n, width).getValues() : [];
  const tz = Session.getScriptTimeZone();
  const fmt = d => d instanceof Date ? Utilities.formatDate(d, tz, 'MM.dd HH:mm:ss') : String(d || '');
  const rows = vals.map((r, i) => {
    const g = k => col[k] === undefined ? '' : r[col[k]];
    const ts = g('ts');
    return {
      row: i + 2,
      tsMs: ts instanceof Date ? ts.getTime() : 0,
      ts: fmt(ts),
      team: String(g('team')).trim(), partner: String(g('partner')).trim(),
      leader: String(g('leader')).trim(), phone: String(g('phone')).trim(),
      type: String(g('type')).trim(), zone: ZONE_OF(String(g('type'))),
      item1: String(g('item1')).trim(), item2: String(g('item2')).trim(),
      staff: String(g('staff')).trim(), power: String(g('power')).trim(), request: String(g('request')).trim(),
      status: String(g('처리상태') || '대기').trim() || '대기',
      assigned: String(g('배정아이템')).trim(), memo: String(g('처리메모')).trim(),
      by: String(g('처리자')).trim(), at: fmt(g('처리일시')),
    };
  }).filter(x => x.team);
  rows.sort((a, b) => a.tsMs - b.tsMs || a.row - b.row);
  rows.forEach((x, i) => x.order = i + 1);
  return { sh, col, rows };
}

function summary_(rows) {
  const used = { exp: 0, snack: 0, market: 0 };
  const items = {};
  Object.keys(RESERVED).forEach(z => RESERVED[z].forEach(b => {
    used[z]++;
    const k = norm_(b.item); if (k) items[k] = (items[k] || 0) + 1;
  }));
  rows.filter(x => x.status === '승인').forEach(x => {
    if (used[x.zone] !== undefined) used[x.zone]++;
    const k = norm_(x.assigned);
    if (k) items[k] = (items[k] || 0) + 1;
  });
  return { caps: CAPS, used, items, maxSame: MAX_SAME_ITEM, zoneName: ZONE_NAME, reserved: RESERVED };
}

// ── 클라이언트에서 부르는 함수 ───────────────────────
function getData() {
  const me = whoAmI_();
  const { rows } = readAll_();
  return { me, rows, sum: summary_(rows), now: new Date().toISOString() };
}

/**
 * action: '승인' | '반려' | '대기'
 * item: 승인 시 배정할 아이템 (1순위/2순위 또는 직접 입력)
 */
function decide(row, action, item, memo) {
  const me = whoAmI_();
  if (['승인', '반려', '대기'].indexOf(action) < 0) throw new Error('알 수 없는 처리: ' + action);
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const { sh, col, rows } = readAll_();
    const target = rows.find(x => x.row === Number(row));
    if (!target) throw new Error('신청을 찾지 못했습니다 (행 ' + row + ')');

    if (action === '승인') {
      if (!target.zone) throw new Error('부스 유형을 알 수 없습니다: ' + target.type);
      item = String(item || '').trim();
      if (!item) throw new Error('배정할 아이템을 정해 주세요.');
      const others = rows.filter(x => x.row !== target.row && x.status === '승인');
      const reserved = RESERVED[target.zone] || [];
      const zoneUsed = others.filter(x => x.zone === target.zone).length + reserved.length;
      if (zoneUsed >= CAPS[target.zone]) throw new Error(ZONE_NAME[target.zone] + ' 자리가 모두 찼습니다 (' + CAPS[target.zone] + '부스).');
      const allRes = [].concat(RESERVED.exp, RESERVED.snack, RESERVED.market);
      const same = others.filter(x => norm_(x.assigned) === norm_(item)).length + allRes.filter(b => norm_(b.item) === norm_(item)).length;
      if (same >= MAX_SAME_ITEM) throw new Error('"' + item + '" 아이템은 이미 ' + MAX_SAME_ITEM + '개 부스가 승인되었습니다. 2순위나 다른 아이템으로 배정하세요.');
    }
    if (action === '반려' && !String(memo || '').trim()) throw new Error('반려 사유를 적어 주세요.');

    const r = target.row;
    const set = (k, v) => sh.getRange(r, col[k] + 1).setValue(v);
    set('처리상태', action === '대기' ? '' : action);
    set('배정아이템', action === '승인' ? item : '');
    set('처리메모', String(memo || '').trim());
    set('처리자', action === '대기' ? '' : me);
    set('처리일시', action === '대기' ? '' : new Date());
    SpreadsheetApp.flush();
    rebuildPublic_();
  } finally {
    lock.releaseLock();
  }
  return getData();
}

// ── 공개 탭: 승인된 부스만 (개인 정보 없음) ───────────
function rebuildPublic_() {
  const ss = SpreadsheetApp.getActive();
  const { rows } = readAll_();
  let sh = ss.getSheetByName(PUBLIC_SHEET);
  if (!sh) sh = ss.insertSheet(PUBLIC_SHEET);
  const out = [['zone', 'team', 'partner', 'item', 'order', 'updated']];
  const stamp = Utilities.formatDate(new Date(), 'Asia/Seoul', "yyyy-MM-dd'T'HH:mm:ss'+09:00'");
  rows.filter(x => x.status === '승인' && x.zone).forEach(x => out.push([x.zone, x.team, x.partner, x.assigned, x.order, stamp]));
  if (out.length === 1) out.push(['', '', '', '', '', stamp]);   // 빈 목록도 갱신 시각은 남김
  sh.clearContents();
  sh.getRange(1, 1, out.length, out[0].length).setValues(out);
}

/** 처음 한 번 실행: 관리용 열·공개현황 탭을 만듭니다 (편집기에서 ▶ 실행) */
function setup() {
  columns_(responseSheet_());
  rebuildPublic_();
}
