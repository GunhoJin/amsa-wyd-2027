// 사이트 수정 요청 접수 (/api/request)
// amsawyd.com/request 요청서 → 이 함수 → 구글 Apps Script 웹 앱(구글 시트 저장 + 담당자 접수 메일)
// 시트 내용은 돌려주지 않고 접수 결과(ok, 접수번호)만 응답합니다.
const INTAKE_URL = "https://script.google.com/macros/s/AKfycbx9PnuZlTNRb8Ff0DXXwmRhl7YvB0WqF3PVlVoxjkwcWwhPtOc5ZD1bZyhCXiaaFA80/exec";
const LIMIT = { name: 40, baptism: 40, phone: 30, team: 60, page: 60, content: 3000, website: 200 };

const json = (o, status = 200) => new Response(JSON.stringify(o), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});

export async function onRequestPost({ request }) {
  // 같은 사이트에서 온 요청만 받음
  const origin = request.headers.get("origin") || "";
  if (origin && !/^https:\/\/(amsawyd\.com|www\.amsawyd\.com|[a-z0-9-]+\.amsa-wyd-2027\.pages\.dev|amsa-wyd-2027\.pages\.dev)$/.test(origin)) {
    return json({ ok: false, error: "허용되지 않은 요청입니다." }, 403);
  }
  let d;
  try {
    const ct = request.headers.get("content-type") || "";
    d = ct.includes("application/json") ? await request.json() : Object.fromEntries(await request.formData());
  } catch (e) {
    return json({ ok: false, error: "요청 형식이 올바르지 않습니다." }, 400);
  }
  const v = {};
  for (const k in LIMIT) v[k] = String(d[k] ?? "").trim().slice(0, LIMIT[k]);
  if (v.website) return json({ ok: true });                 // 스팸 방지용 숨은 칸
  if (!v.name || !v.phone || !v.content) return json({ ok: false, error: "이름·연락처·수정 요청 내용을 적어 주세요." }, 400);

  try {
    const r = await fetch(INTAKE_URL, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(v).toString(),
      redirect: "follow",
    });
    const t = await r.text();
    let j; try { j = JSON.parse(t); } catch (e) { j = null; }
    if (!j) return json({ ok: false, error: "접수 서버 응답을 읽지 못했습니다. 잠시 후 다시 시도해 주세요." }, 502);
    return json({ ok: !!j.ok, id: j.id, error: j.error }, j.ok ? 200 : 400);
  } catch (e) {
    return json({ ok: false, error: "접수 서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요." }, 502);
  }
}

export async function onRequest() {
  return json({ ok: false, error: "POST로 보내 주세요." }, 405);
}
