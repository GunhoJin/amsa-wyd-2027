// 홀리마켓 부스 선점 현황 (/api/booths)
// 관리자 페이지(구글 Apps Script)에서 승인한 부스만 모인 '공개현황' 탭을 웹에 게시한 CSV를 읽어 JSON으로 돌려줍니다.
// 개인 정보(단체장·연락처)는 공개현황 탭에 없습니다.
// CSV 주소: 스프레드시트 > 파일 > 공유 > 웹에 게시 > '공개현황' 탭 · CSV  (Cloudflare 환경변수 BOOTHS_CSV 로도 지정 가능)
const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHsC9MFKyj2UK26AD-ZCll51KzxrzSRzf4jpTeIbayr5ywsjmd1gRdM33PR2eqOnxBB_2345XvQ0oK/pub?gid=679680621&single=true&output=csv";

function parseCSV(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; }
      else cur += c;
    } else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cur); rows.push(row); row = []; cur = "";
    } else cur += c;
  }
  if (cur !== "" || row.length) { row.push(cur); rows.push(row); }
  return rows;
}

export async function onRequestGet(context) {
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "access-control-allow-origin": "*",
    "cache-control": "public, max-age=120",
  };
  const url = (context.env && context.env.BOOTHS_CSV) || CSV_URL;
  if (!url) return new Response(JSON.stringify({ ok: false, reason: "not-configured" }), { headers });
  try {
    const r = await fetch(url, { cf: { cacheTtl: 60 } });
    if (!r.ok) throw new Error("upstream " + r.status);
    const rows = parseCSV(await r.text());
    const head = (rows.shift() || []).map(s => s.trim());
    const ix = k => head.indexOf(k);
    const booths = { exp: [], snack: [], market: [] };
    let updated = "";
    for (const c of rows) {
      const zone = (c[ix("zone")] || "").trim();
      updated = (c[ix("updated")] || updated).trim();
      if (!booths[zone]) continue;
      const team = (c[ix("team")] || "").trim();
      if (!team) continue;
      booths[zone].push({
        team,
        partner: (c[ix("partner")] || "").trim(),
        item: (c[ix("item")] || "").trim(),
        order: Number(c[ix("order")]) || 0,
      });
    }
    for (const z in booths) booths[z].sort((a, b) => a.order - b.order);
    return new Response(JSON.stringify({ ok: true, updated, booths }), { headers });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, reason: String(e.message || e) }), { status: 200, headers });
  }
}
