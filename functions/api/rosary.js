// 묵주기도 10억 단 봉헌 현황 프록시 (Cloudflare Pages Functions)
// 교구 봉헌통계(wyd.catholic.or.kr/status.asp)를 서버에서 읽어 JSON으로 돌려줍니다.
const SRC = "https://wyd.catholic.or.kr/status.asp";

function strip(html) {
  return html.replace(/<script[\s\S]*?<\/script>/gi, " ")
             .replace(/<style[\s\S]*?<\/style>/gi, " ")
             .replace(/<[^>]+>/g, " ")
             .replace(/&nbsp;/g, " ")
             .replace(/\s+/g, " ");
}

export async function onRequest(ctx) {
  const url = new URL(ctx.request.url);
  const debug = url.searchParams.has("debug");
  let html = "";
  try {
    const r = await fetch(SRC, {
      headers: { "User-Agent": "Mozilla/5.0 (compatible; amsawyd.com rosary widget)" },
      cf: { cacheTtl: 3600, cacheEverything: true },
    });
    html = await r.text();
    if (debug) {
      const text = strip(html);
      const cands = [];
      const re = /([0-9][0-9,]{3,})\s*(단|곳|개|%)/g;
      let m;
      while ((m = re.exec(text)) && cands.length < 60) {
        cands.push(text.slice(Math.max(0, m.index - 40), m.index + m[0].length + 10));
      }
      const urls = [...html.matchAll(/["'`]([^"'`\s]*?\.(?:asp|aspx|json|php)[^"'`\s]*)["'`]/gi)].map(x => x[1]).slice(0, 40);
      return new Response(JSON.stringify({ status: r.status, length: html.length, candidates: cands, urls }, null, 1), {
        headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
      });
    }
    return new Response(JSON.stringify({ ok: false, reason: "parser pending" }), {
      headers: { "content-type": "application/json; charset=utf-8" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: String(e) }), { status: 502, headers: { "content-type": "application/json" } });
  }
}
