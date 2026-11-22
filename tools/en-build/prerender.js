// 검색엔진용 정적 본문 채우기 — program.html·join.html의 JS 데이터로 그린 결과를
// HTML 자리(<!--pre-->…<!--/pre-->)에 미리 넣는다. 화면은 JS가 다시 그리므로 동일.
// 사용 (저장소 루트에서): node tools/en-build/prerender.js [폴더]   — 한국어는 생략(.), 영문은 en. 데이터를 고친 뒤 매번 실행
const fs = require("fs"), path = require("path"), vm = require("vm");
const repo = process.argv[2] || path.join(__dirname, "..", "..");

const TARGETS = {
  "program.html": { marker: "const PROGRAMS", ids: ["l-now", "l-next", "l-past", "n-now", "n-next", "n-past"] },
  "join.html": { marker: "const JOINS", ids: ["jg"] },
};

for (const [file, { marker, ids }] of Object.entries(TARGETS)) {
  const fp = path.join(repo, file);
  let html = fs.readFileSync(fp, "utf8");
  const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(s => s.includes(marker));
  if (!code) throw new Error(file + ": 데이터 스크립트 없음");
  const out = {};
  const document = { getElementById: id => (out[id] ??= { innerHTML: "", textContent: "" }) };
  vm.runInNewContext(code, { document, Date, String, Number });
  for (const id of ids) {
    const el = out[id];
    if (!el) throw new Error(file + ": " + id + " 결과 없음");
    const val = el.innerHTML || String(el.textContent);
    // 빈 자리 또는 이전에 채운 자리를 모두 교체
    const re = new RegExp(`(id="${id}">)(?:<!--pre-->[\\s\\S]*?<!--/pre-->|\\d+)?(</(?:div|b)>)`);
    if (!re.test(html)) throw new Error(file + ": " + id + " 자리 못 찾음");
    const body = id.startsWith("n-") ? val : `<!--pre-->${val}<!--/pre-->`;
    html = html.replace(re, (_, a, b) => a + body + b);
  }
  fs.writeFileSync(fp, html);
  console.log(file, "OK", ids.map(i => i + ":" + (out[i].innerHTML || out[i].textContent).length).join(" "));
}
