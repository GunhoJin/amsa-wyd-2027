# 영문판 생성: 한국어 페이지(<page>.html) → en/<page>.html
# 사용 (저장소 루트에서):
#   python tools/en-build/build.py --check [page ...]   번역표에 없는 한국어 문구만 보여 줌 (파일 안 바꿈)
#   python tools/en-build/build.py [page ...]           영문판 생성 (빠진 문구가 있으면 그 페이지는 건너뜀)
#   node tools/en-build/prerender.js en                 영문 program·join 미리 채운 본문 갱신
# 번역표: tr/common.json(공통) + tr/<page>.json {"한국어 문구": "English"}
#   tr/<page>.raw.json  번역 전에 그대로 바꿀 코드 조각(작은따옴표 문자열·CSS 등)
#   tr/<page>.post.json 번역 뒤에 바꿀 조각(한국어를 일부러 남길 곳)
# 영문 문구에는 ASCII 따옴표(" ')를 쓰지 말고 ‘ ’ “ ” 를 쓴다 (HTML 속성·JS 문자열이 깨지지 않게).
import re, io, json, os, sys
W = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, W)
from lang import apply_switch
repo = os.path.normpath(os.path.join(W, "..", ".."))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
CHECK = "--check" in sys.argv
PAGES = "index about plan pilgrim program join market homestay rosary donate contact request inquiry".split()
want = args or PAGES
K = re.compile(r'[가-힣]')
LIT = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'|`((?:[^`\\]|\\.)*)`')
LINKS = "|".join(PAGES[1:])
ASSETS = r'(?:bg-desktop|bg-ipad|bg|hands|og|prog-letter|prog-photo|prog-rosary-2)\.(?:png|jpg)|wyd-logo\.svg|[a-z-]+-mask-(?:top|bottom)\.svg|fonts/[\w.-]+'

def load(name):
    f = os.path.join(W, "tr", name)
    return json.load(io.open(f, encoding="utf-8")) if os.path.exists(f) else {}

def strip_switch(s):
    s = re.sub(r'<div class="lsw"[^>]*>[\s\S]*?</div>', '', s)
    return re.sub(r'<script>/\* 언어 전환: 카드가 뒤집힌 뒤 이동 \*/[\s\S]*?</script>', '', s)

def segments(s):
    """페이지에서 번역이 필요한 한국어 문구 (본문, 속성, 스크립트 문자열)"""
    s = strip_switch(s)
    out = []
    for code in re.findall(r'<script[^>]*>([\s\S]*?)</script>', s):
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        code = re.sub(r'(?m)^\s*//.*$', '', code)
        for lit in LIT.findall(code):
            for x in lit:
                if not K.search(x): continue
                for piece in re.split(r'\$\{[^}]*\}|<[^>]+>', x):
                    piece = piece.strip()
                    if K.search(piece): out.append(piece)
    s2 = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', s)
    s2 = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', s2)
    s2 = re.sub(r'<!--pre-->[\s\S]*?<!--/pre-->', '', s2)
    s2 = re.sub(r'<!--[\s\S]*?-->', '', s2)
    for a, v in re.findall(r'\s(content|alt|aria-label|placeholder|title|data-[a-z-]+)="([^"]*)"', s2):
        if K.search(v): out.append(v)
    for t in re.split(r'<[^>]+>', s2):
        t = t.strip()
        if K.search(t): out.append(t)
    return list(dict.fromkeys(out))

def leftovers(s):
    """영문판에 남은 한국어(주석·글꼴 이름·의도적으로 남긴 코드 제외)"""
    c = strip_switch(s)
    c = re.sub(r'/\*[\s\S]*?\*/|<!--[\s\S]*?-->', '', c)
    c = re.sub(r'(?m)//[^\n"\'`]*$', '', c)
    c = c.replace('"맑은 고딕"', '').replace('>한국어</a>', '')
    c = re.sub(r'const KO = \{.*?\};', '', c); c = re.sub(r'const mapUrl.*', '', c); c = re.sub(r'var P=/.*?SKIP=', '', c)
    return sorted(set(x for x in re.findall(r'[가-힣][^"\'<>`\n]{0,30}', c) if x not in ("서울)",)))

common = load("common.json")
bad = 0
os.makedirs(os.path.join(repo, "en"), exist_ok=True)
for p in want:
    tr = dict(common); tr.update(load(p + ".json"))
    s = io.open(os.path.join(repo, p + ".html"), encoding="utf-8").read()
    raw = load(p + ".raw.json")
    pre = s
    for a in raw: pre = pre.replace(a, "")
    miss = [x for x in segments(pre) if x not in tr]
    if miss:
        bad += 1
        print("%s: 번역표(tr/%s.json)에 없는 문구 %d개" % (p, p, len(miss)))
        for m in miss: print("   " + json.dumps(m, ensure_ascii=False))
        continue
    if CHECK:
        print(p, "OK"); continue
    s = re.sub(r'<!--pre-->[\s\S]*?<!--/pre-->', '<!--pre--><!--/pre-->', s)
    for a, b in raw.items():
        if a not in s: print(p, "raw 조각 못 찾음:", a[:80])
        s = s.replace(a, b)
    s = s.replace('content:"고정"', 'content:"Fixed"')
    # 폼 선택지: 보내는 값은 한국어 그대로 (접수 시트·정기 작업이 한국어 값으로 구분)
    s = re.sub(r'<option>([^<]+)</option>', lambda m: '<option value="%s">%s</option>' % ("".join("&#%d;" % ord(c) if K.match(c) else c for c in m.group(1)), m.group(1)), s)
    m = re.search(r'<style[^>]*>[\s\S]*?</style>', s)
    head, css, rest = (s[:m.start()], m.group(0), s[m.end():]) if m else (s, "", "")
    def apply(t):
        for k in sorted(tr, key=len, reverse=True):
            if k in t: t = t.replace(k, tr[k])
        return t
    s = apply(strip_switch(head)) + css + apply(strip_switch(rest))
    for a, b in load(p + ".post.json").items():
        if a not in s: print(p, "post 조각 못 찾음:", a[:80])
        s = s.replace(a, b)
    s = s.replace('<html lang="ko">', '<html lang="en">')
    s = s.replace('content="ko_KR"', 'content="en_US"')
    s = s.replace('"inLanguage": "ko-KR"', '"inLanguage": "en"')
    s = s.replace('toLocaleString("ko-KR")', 'toLocaleString("en-US")')
    s = re.sub(r'(https://amsawyd\.com)/(%s)(?=["#?])' % LINKS, r'\1/en/\2', s)
    s = re.sub(r'(<link rel="canonical" href="https://amsawyd\.com)/(?=")', r'\1/en/', s)
    s = re.sub(r'(<meta property="og:url" content="https://amsawyd\.com)/(?=")', r'\1/en/', s)
    s = re.sub(r'(["\'])/(%s)(?=[#"\'])' % LINKS, r'\1/en/\2', s)
    s = re.sub(r'href=(["\'])/(?=[#"\'])', r'href=\1/en/', s)
    s = re.sub(r'(src=|href=|url\()(["\']?)(%s)' % ASSETS, r'\1\2/\3', s)
    s = s.replace("lang=kr&amp;", "lang=en&amp;")
    kp = "/" if p == "index" else "/" + p
    s = re.sub(r'<a href="/en/[a-z]*" class="mn-sub" hreflang="en" lang="en">English</a>', '<a href="%s" class="mn-sub" hreflang="ko" lang="ko">한국어</a>' % kp, s)
    s = re.sub(r'(hreflang="(?:ko|x-default)" href="https://amsawyd\.com)/en/', r'\1/', s)
    s = s.replace('<meta property="og:locale" content="en_US">\n', '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="ko_KR">\n')
    # 언어 스위치: 한국어 페이지와 같은 위치에 영어 상태로 다시 넣기
    s = apply_switch(s, p, "en") if 'data-menu-open' in s else s
    io.open(os.path.join(repo, "en", p + ".html"), "w", encoding="utf-8", newline="").write(s)
    left = leftovers(s)
    print(p, "OK" + ("  남은 한국어: " + " | ".join(left) if left else ""))
    if left: bad += 1
sys.exit(1 if bad else 0)
