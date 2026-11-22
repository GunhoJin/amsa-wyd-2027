# 한국어 페이지에 언어 전환 스위치·hreflang 넣기/갱신 (여러 번 실행해도 같은 결과)
# 사용: python tools/en-build/lang.py   (저장소 루트에서)
import re, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lsw import lsw, CSS, JS
repo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PAGES = "index about plan pilgrim program join market homestay rosary donate contact request inquiry".split()
CSS_BLOCK = "/* lsw:start */\n" + CSS + "/* lsw:end */\n"

def apply_switch(s, page, cur):
    # CSS
    s = re.sub(r'/\* lsw:start \*/[\s\S]*?/\* lsw:end \*/\n', '', s)
    s = re.sub(r'\.lang\{[^}]*\}\.lang:hover\{opacity:1\}\n', '', s)
    i = s.index("</style>"); s = s[:i] + CSS_BLOCK + s[i:]
    # 버튼 (예전 EN 링크 또는 이전 스위치를 교체)
    s = re.sub(r'<a class="lang" href="[^"]*" hreflang="[a-z]+" lang="[a-z]+">(?:EN|KO)</a>', lsw(page, cur), s)
    s = re.sub(r'<div class="lsw"[^>]*>[\s\S]*?</div>', lambda m: lsw(page, cur), s)
    if 'class="lsw"' not in s:
        s = re.sub(r'(\s*)(<button class="(?:mn-btn|menu)" type="button" data-menu-open)', lambda m: m.group(1) + lsw(page, cur) + m.group(1) + m.group(2), s)
    # 스크립트
    s = re.sub(r'<script>/\* 언어 전환: 카드가 뒤집힌 뒤 이동 \*/[\s\S]*?</script>\n', '', s)
    s = s.replace("</body>", JS + "</body>", 1) if "</body>" in s else s.rstrip("\n") + "\n" + JS
    return s

if __name__ == "__main__":
    for p in PAGES:
        f = os.path.join(repo, p + ".html"); s = io.open(f, encoding="utf-8").read()
        path = "" if p == "index" else p
        if 'hreflang="x-default"' not in s:
            alt = ('<link rel="alternate" hreflang="ko" href="https://amsawyd.com/%s">\n'
                   '<link rel="alternate" hreflang="en" href="https://amsawyd.com/en/%s">\n'
                   '<link rel="alternate" hreflang="x-default" href="https://amsawyd.com/%s">\n') % (path, path, path)
            s = re.sub(r'(<link rel="canonical"[^>]*>\n)', lambda m: m.group(1) + alt, s, count=1)
        if 'class="mn-sub" hreflang="en"' not in s:
            s = re.sub(r'(class="mn-sub"[^>]*>[^<]*</a>)', r'\1<a href="/en/%s" class="mn-sub" hreflang="en" lang="en">English</a>' % path, s, count=1)
        s = apply_switch(s, p, "ko")
        io.open(f, "w", encoding="utf-8", newline="").write(s)
        print(p, "switch:", s.count('class="lsw"'))
