// 묵주기도 10억 단 봉헌 현황 (Cloudflare Pages Functions)
// 교구 봉헌통계(wyd.catholic.or.kr/status.asp)를 서버에서 읽어 숫자만 JSON으로 돌려줍니다.
// 교구 사이트 구조가 바뀌어 숫자를 못 찾으면 ok:false → 페이지는 기준일 숫자를 그대로 보여 줍니다.
const SRC = "https://wyd.catholic.or.kr/status.asp";
const GOAL = 1000000000;

const num = s => (s == null ? null : Number(String(s).replace(/,/g, "")));

function parse(html) {
  const t = html.replace(/<script[\s\S]*?<\/script>/gi, " ")
                .replace(/<style[\s\S]*?<\/style>/gi, " ")
                .replace(/<[^>]+>/g, " ")
                .replace(/&nbsp;/g, " ")
                .replace(/\s+/g, " ");
  // 일자별 누적 표의 첫 줄: "2026-11-01 (일) 📅 Today 701,799 단 625,632,529 단"
  const row = t.match(/(\d{4}-\d{2}-\d{2})\s*\([^)]*\)[^0-9]*?([\d,]+)\s*단\s*([\d,]+)\s*단/);
  const parishes = t.match(/참여\s*본당\s*([\d,]+)/);
  const orgs = t.match(/참여\s*기관\s*\/?\s*단체\s*([\d,]+)/);
  const pct = t.match(/진행률\s*([\d.]+)\s*%/);
  if (!row) return null;
  const total = num(row[3]);
  if (!total || total < 1e6 || total > 2e9) return null;
  return {
    date: row[1],
    today: num(row[2]),
    total,
    goal: GOAL,
    percent: pct ? Number(pct[1]) : Math.round((total / GOAL) * 10000) / 100,
    parishes: parishes ? num(parishes[1]) : null,
    orgs: orgs ? num(orgs[1]) : null,
  };
}

export async function onRequest() {
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "access-control-allow-origin": "*",
    "cache-control": "public, max-age=1800",
  };
  try {
    const r = await fetch(SRC, {
      headers: { "User-Agent": "Mozilla/5.0 (compatible; amsawyd.com rosary widget)" },
      cf: { cacheTtl: 1800, cacheEverything: true },
    });
    if (!r.ok) throw new Error("source " + r.status);
    const data = parse(await r.text());
    if (!data) return new Response(JSON.stringify({ ok: false, reason: "parse" }), { headers });
    return new Response(JSON.stringify({ ok: true, ...data, source: SRC, fetchedAt: new Date().toISOString() }), { headers });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, reason: String(e) }), { status: 200, headers });
  }
}
