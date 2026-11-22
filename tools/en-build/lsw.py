# 언어 전환 버튼(한/EN 플립 스위치) — lang.py(한국어 페이지)와 build.py(영문판)가 함께 씀
# 디자인: Uiverse.io flip switch(pharmacist-sabot)를 머리글 크기로 줄여 적용

def lsw(page, cur):
    """page: index|about|…, cur: 'ko' 또는 'en' — 지금 보고 있는 언어"""
    path = "" if page == "index" else page
    ko, en = "/" + path, "/en/" + path
    a_ko = '<a href="%s" lang="ko" hreflang="ko"%s>한</a>' % (ko, ' aria-current="true"' if cur == "ko" else "")
    a_en = '<a href="%s" lang="en" hreflang="en"%s>EN</a>' % (en, ' aria-current="true"' if cur == "en" else "")
    label = "언어 선택 · Language"
    return '<div class="lsw" data-lang="%s" role="group" aria-label="%s"><span class="lsw-card" aria-hidden="true"></span>%s%s</div>' % (cur, label, a_ko, a_en)

CSS = (
    "/* 언어 전환 플립 스위치 (Uiverse.io flip switch by pharmacist-sabot 축소판) */\n"
    ".lsw{--lsw-w:38px;--lsw-h:30px;--lsw-hi:#64ffda;position:relative;display:flex;width:calc(var(--lsw-w)*2);height:var(--lsw-h);margin-left:auto;margin-right:16px;"
    "background:rgba(var(--fg-rgb,255,255,255),.1);border:1px solid rgba(var(--fg-rgb,255,255,255),.2);border-radius:10px;perspective:600px;flex:none;"
    "box-shadow:0 4px 16px rgba(31,38,135,.25),inset 0 2px 4px rgba(var(--fg-rgb,255,255,255),.1);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}\n"
    ".lsw a{position:relative;z-index:2;flex:1;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;letter-spacing:.04em;"
    "color:rgba(var(--fg-rgb,255,255,255),.6);text-decoration:none;transition:color .3s;-webkit-tap-highlight-color:transparent}\n"
    ".lsw a:hover,.lsw a[aria-current]{color:var(--fg,#fff)}\n"
    ".lsw a[aria-current]{text-shadow:0 0 8px rgba(100,255,218,.5)}\n"
    ".lsw a[aria-current]::after{content:\"\";position:absolute;bottom:3px;width:14px;height:2px;border-radius:2px;background:var(--lsw-hi);animation:lswGlow 1.5s infinite alternate}\n"
    ".lsw a:focus-visible{outline:2px solid #00A1DB;outline-offset:2px;border-radius:8px}\n"
    ".lsw-card{position:absolute;top:0;left:0;width:var(--lsw-w);height:100%;z-index:1;border-radius:9px;"
    "background:linear-gradient(135deg,rgba(var(--fg-rgb,255,255,255),.2),rgba(var(--fg-rgb,255,255,255),.1));border:1px solid rgba(var(--fg-rgb,255,255,255),.15);"
    "box-shadow:0 2px 10px rgba(0,0,0,.2),inset 0 1px 3px rgba(var(--fg-rgb,255,255,255),.1);transform-style:preserve-3d}\n"
    ".lsw[data-lang=en] .lsw-card{transform:translateX(100%) rotateY(180deg)}\n"
    ".lsw[data-go=en] .lsw-card{animation:lswR .45s cubic-bezier(.76,0,.24,1) forwards}\n"
    ".lsw[data-go=ko] .lsw-card{animation:lswL .45s cubic-bezier(.76,0,.24,1) forwards}\n"
    ".lsw[data-go] a[aria-current]::after{opacity:0}\n"
    "@keyframes lswR{0%{transform:translateX(0) rotateY(0)}50%{transform:translateX(50%) rotateY(90deg) scale(1.05)}100%{transform:translateX(100%) rotateY(180deg)}}\n"
    "@keyframes lswL{0%{transform:translateX(100%) rotateY(180deg)}50%{transform:translateX(50%) rotateY(90deg) scale(1.05)}100%{transform:translateX(0) rotateY(0)}}\n"
    "@keyframes lswGlow{from{box-shadow:0 0 4px var(--lsw-hi)}to{box-shadow:0 0 10px var(--lsw-hi),0 0 16px var(--lsw-hi)}}\n"
    "@media (prefers-reduced-motion:reduce){.lsw-card,.lsw a[aria-current]::after{animation:none!important}}\n"
)

JS = ('<script>/* 언어 전환: 카드가 뒤집힌 뒤 이동 */\n'
      'document.addEventListener("click",function(e){var a=e.target.closest(".lsw a:not([aria-current])");if(!a||e.metaKey||e.ctrlKey||e.shiftKey)return;'
      'e.preventDefault();var w=a.parentNode;w.setAttribute("data-go",w.getAttribute("data-lang")==="ko"?"en":"ko");'
      'var d=matchMedia("(prefers-reduced-motion: reduce)").matches?0:380;setTimeout(function(){location.href=a.href},d)});\n'
      '</script>\n')
