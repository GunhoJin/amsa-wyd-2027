# 화면 테마(라이트·다크·시스템) 넣기/갱신 — 한국어 페이지에 실행하면 영문판은 build.py가 그대로 따라감
# 사용: python tools/en-build/theme.py   (저장소 루트에서, 여러 번 실행해도 같은 결과)
# 기본값은 기기 설정(시스템). 메뉴 안 「화면 테마」에서 바꾸면 이 브라우저에 기억.
# 홈(index) 첫 화면은 라이트에서 사진·손·지구본의 명암을 뒤집어 밝게 보임(PAGE_LIGHT).
import re, io, os, sys
repo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PAGES = "about plan pilgrim program join market homestay rosary donate contact request inquiry".split()

LIGHT = ("--ink:#f5f6f8;--ink-rgb:245,246,248;--panel:#ffffff;--panel-2:#eef0f3;--fg:#151a21;--fg-rgb:21,26,33;"
         "--accent:#0079a8;--accent-rgb:0,121,168;--gold:#946000;--gold-rgb:148,96,0;"
         "--fg-3:rgba(21,26,33,.62);--btn-light:#151a21;--btn-ink:#ffffff;--field:#ffffff;color-scheme:light")
EXTRA = [".head::before{opacity:.1!important}", ".lsw{--lsw-hi:#0a9d84}",
         "#snow{filter:brightness(.55) sepia(1) hue-rotate(165deg) saturate(2.5)}"]
# 라이트에서도 어두운 배경을 유지하는 부분 (그 안의 글자색은 다크 값으로)
DARK_VARS = ("--fg:#ffffff;--fg-rgb:255,255,255;--fg-2:rgba(255,255,255,.72);--fg-3:rgba(255,255,255,.48);"
             "--line:rgba(255,255,255,.1);--line-2:rgba(255,255,255,.18);--ink:#101216;--ink-rgb:16,18,22;"
             "--gold:#FFD27A;--gold-rgb:255,210,122;color:var(--fg)")
SCOPES = {"market": [".head"], "program": [".pg-verse"]}
# 페이지별 라이트 색표 (기본 라이트 위에 덮어씀) — 홀리마켓은 크리스마스 색: 아이보리 바탕, 와인 레드·상록 그린·골드
PAGE_LIGHT = {
    # 1년 일정: 대상별 색(전 신자·청년·본당)을 밝은 바탕에서 읽히게
    "plan": ("--all:#1f6fb8;--youth:#0d7a6e;--parish:#6346c2", []),
    # 순례길: 코스 색과 이어지는 코스 표시
    "pilgrim": ("--c1:#0079a8;--c2:#8c5a00;--c3:#6346c2", [".st .tag{background:var(--fg)}"]),
    # 프로그램: 대림(보라)·성탄(빨강) 카드의 번호·링크 색
    "program": ("", [".pg-card.advent .pg-no,.pg-card.advent .steps .n,.pg-card.advent .plink a{color:#6346c2}",
                     ".pg-card.xmas .pg-no,.pg-card.xmas .steps .n{color:#b8262f}"]),
    # 홈 첫 화면: 사진·손·지구본을 명암만 뒤집어(색조 유지) 밝은 판으로
    "index": ("--fg-dim:rgba(21,26,33,.72);--seoul:#946000;--btn:#e8ebef",
              [".bd,.clip img,[data-globe]{filter:invert(1) hue-rotate(180deg) brightness(1.04)}",
               ".glass{background:rgba(255,255,255,.55)}", ".menu,.mn-btn{color:var(--fg)!important}"]),
    "market": ("--ink:#fbf6ee;--ink-rgb:251,246,238;--panel:#fffdf8;--fg:#2b1719;--fg-rgb:43,23,25;"
               "--accent:#b8262f;--accent-rgb:184,38,47;--xr:#b8262f;--xg:#1f6e43;--xg2:#1d7346;"
               "--gold:#8c5a00;--gold-rgb:140,90,0;--line:rgba(120,30,40,.14);--line-2:rgba(120,30,40,.24)",
               ["#snow{filter:brightness(.78) sepia(1) saturate(2.4) hue-rotate(-8deg)}", ".zone:nth-child(3) .k,.ow:nth-child(3) .k{color:#b35f00}", ".zone:nth-child(3),.ow:nth-child(3){border-top-color:#d9821e}"]),
}

def pre(prefix, rule):
    """규칙의 모든 선택자 앞에 테마 조건을 붙임 (쉼표로 묶인 선택자 각각)"""
    sel, body = rule.split("{", 1)
    return ",".join(prefix + " " + x.strip() for x in sel.split(",")) + "{" + body

SYS = ":root:not([data-theme=dark])"
PICK = ":root[data-theme=light]"
CSS = ("/* theme:start — 라이트 테마 (기본은 기기 설정, 메뉴에서 선택) */\n"
       "@media (prefers-color-scheme:light){" + SYS + "{" + LIGHT + "}" + "".join(pre(SYS, x) for x in EXTRA) + "}\n"
       + PICK + "{" + LIGHT + "}" + "".join(pre(PICK, x) for x in EXTRA) + "\n"
       "/* theme:end */\n")
THM_CSS = ("/* thm:start */\n"
           ".thm{display:flex;gap:6px;margin-top:10px}"
           ".thm button{flex:1;padding:10px 0;border-radius:10px;border:1px solid var(--line-2,rgba(255,255,255,.18));background:transparent;"
           "color:var(--fg-2,rgba(255,255,255,.72));font:inherit;font-size:14px;cursor:pointer}"
           ".thm button[aria-checked=true]{background:var(--fg,#fff);color:var(--ink,#101216);border-color:var(--fg,#fff)}"
           ".thm button:focus-visible{outline:2px solid #00A1DB;outline-offset:2px}"
           ".thm-k{margin:28px 0 0;font-size:12px;letter-spacing:.08em;color:var(--fg-3,rgba(255,255,255,.48))}\n"
           "/* thm:end */\n")
HEAD = ('<script>/* 화면 테마: 저장된 선택을 먼저 적용(깜빡임 방지) */'
        'try{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>\n')
TOGGLE = ('<p class="thm-k">화면 테마</p><div class="thm" role="radiogroup" aria-label="화면 테마">'
          '<button type="button" role="radio" data-theme-set="light">라이트</button>'
          '<button type="button" role="radio" data-theme-set="dark">다크</button>'
          '<button type="button" role="radio" data-theme-set="system">시스템</button></div>')
JS = ('<script>/* 화면 테마 선택 */\n(function(){var r=document.documentElement;'
      'function cur(){try{return localStorage.getItem("theme")||"system"}catch(e){return "system"}}'
      'function show(){var c=cur();document.querySelectorAll("[data-theme-set]").forEach(function(b){b.setAttribute("aria-checked",b.getAttribute("data-theme-set")===c?"true":"false")})}'
      'document.addEventListener("click",function(e){var b=e.target.closest("[data-theme-set]");if(!b)return;var v=b.getAttribute("data-theme-set");'
      'try{v==="system"?localStorage.removeItem("theme"):localStorage.setItem("theme",v)}catch(e){}'
      'v==="system"?r.removeAttribute("data-theme"):r.setAttribute("data-theme",v);show()});show()})();\n</script>\n')

def common(t):
    t = re.sub(r'rgba\(\s*255\s*,\s*255\s*,\s*255\s*,', 'rgba(var(--fg-rgb),', t)
    t = re.sub(r'rgba\(\s*16\s*,\s*18\s*,\s*22\s*,', 'rgba(var(--ink-rgb),', t)
    t = re.sub(r'rgba\(\s*255\s*,\s*210\s*,\s*122\s*,', 'rgba(var(--gold-rgb),', t)
    t = re.sub(r'rgba\(\s*0\s*,\s*161\s*,\s*219\s*,', 'rgba(var(--accent-rgb),', t)
    return t

MARK = "@@%s@@"

def tokenize(css):
    """다크 전용으로 적힌 색을 테마 변수로 (한 번 바꾸면 다시 걸리지 않음).
    :root 블록의 색 정의와 언어 스위치 블록(자체 대체값 있음)은 건드리지 않음."""
    held = []
    def hold(x):
        held.append(x); return MARK % (len(held) - 1)
    css = re.sub(r'/\* lsw:start \*/[\s\S]*?/\* lsw:end \*/\n', lambda m: hold(m.group(0)), css)
    first = [True]
    def root(m):
        r = common(m.group(0))
        if first[0] and "--gold:" not in r:
            r = r.replace("--fg:#ffffff;", "--fg:#ffffff; --gold:#FFD27A; --panel:#16191f;", 1)
        if first[0] and "--fg-rgb:" not in r:
            r = r.replace("--fg:#ffffff;", "--fg:#ffffff; --fg-rgb:255,255,255; --ink-rgb:16,18,22; --gold-rgb:255,210,122; --accent-rgb:0,161,219; --field:#0c0e12;", 1)
        first[0] = False
        return hold(r)
    css = re.sub(r':root\{[^}]*\}', root, css)
    css = common(css)
    css = re.sub(r'background:#fff\b', 'background:#FFFFFF', css)   # 로고 흰 바탕 등은 그대로
    css = re.sub(r'#fff(?:fff)?\b', 'var(--fg)', css)
    css = css.replace('background:#FFFFFF', 'background:#fff')
    css = re.sub(r'#101216\b', 'var(--ink)', css, flags=re.I)
    css = re.sub(r'#16191f\b', 'var(--panel)', css, flags=re.I)
    css = re.sub(r'#0c0e12\b', 'var(--field)', css, flags=re.I)
    css = re.sub(r'#ffd27a\b', 'var(--gold)', css, flags=re.I)
    css = re.sub(r'(?<!solid )#00a1db\b', 'var(--accent)', css, flags=re.I)
    return re.sub(r'@@(\d+)@@', lambda m: held[int(m.group(1))], css)

def apply(s, full=True, page=""):
    s = re.sub(r'<script>/\* 화면 테마: 저장된 선택[\s\S]*?</script>\n', '', s)
    s = re.sub(r'<script>/\* 화면 테마 선택 \*/[\s\S]*?</script>\n', '', s)
    s = re.sub(r'<p class="thm-k">[\s\S]*?</div>', '', s)
    s = re.sub(r'/\* theme:start[\s\S]*?/\* theme:end \*/\n', '', s)
    s = re.sub(r'/\* thm:start[\s\S]*?/\* thm:end \*/\n', '', s)
    s = s.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + HEAD, 1)
    m = re.search(r'<style>[\s\S]*?</style>', s)
    css = tokenize(m.group(0)) if full else m.group(0)
    extra = ""
    if full and page in PAGE_LIGHT:
        v, rules = PAGE_LIGHT[page]
        extra += ("/* theme:start 이 페이지 라이트 색표 */\n@media (prefers-color-scheme:light){%s{%s}%s}\n%s{%s}%s\n/* theme:end */\n"
                  % (SYS, v, "".join(pre(SYS, r) for r in rules), PICK, v, "".join(pre(PICK, r) for r in rules)))
    if full and page in SCOPES:
        a = ",".join(SYS + " " + x for x in SCOPES[page]); b = ",".join(PICK + " " + x for x in SCOPES[page])
        extra += ("/* theme:start 라이트에서도 어두운 부분 */\n@media (prefers-color-scheme:light){%s{%s}}\n%s{%s}\n/* theme:end */\n"
                 % (a, DARK_VARS, b, DARK_VARS))
    css = css.replace("</style>", (CSS + extra if full else "") + THM_CSS + "</style>")
    s = s[:m.start()] + css + s[m.end():]
    s = re.sub(r'(<nav aria-label="전체 메뉴">[\s\S]*?</nav>)', lambda m: m.group(1) + TOGGLE, s, count=1)
    s = s.replace("</body>", JS + "</body>", 1) if "</body>" in s else s.rstrip("\n") + "\n" + JS
    return s

if __name__ == "__main__":
    for p in PAGES + ["index"]:
        f = os.path.join(repo, p + ".html"); s = io.open(f, encoding="utf-8").read()
        s = apply(s, full=True, page=p)
        io.open(f, "w", encoding="utf-8", newline="").write(s)
        print(p, "theme", s.count("theme:start"), "toggle", s.count('class="thm"'))
