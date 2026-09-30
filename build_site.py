#!/usr/bin/env python3
"""Generate index + one page per ad for GitHub Pages. Videos live in ./videos, posters in ./posters."""
import json, os, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
ADS = json.load(open(f"{ROOT}/ads.json"))

CSS = """
:root{--bg:#070B1F;--bg2:#0E1A45;--blue:#78B9FF;--gold:#FFD666;--txt:#F4F7FF;--mut:#AEBBDB}
*{box-sizing:border-box}html,body{margin:0;background:radial-gradient(1200px 800px at 50% -10%,#1b2f6e 0%,var(--bg) 60%);color:var(--txt);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
header img{height:56px}
.tag{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);font-weight:700}
h1{font-size:clamp(28px,4.4vw,52px);line-height:1.02;margin:22px 0 8px;font-weight:900;letter-spacing:-.02em}
h1 span{color:var(--blue)}
.sub{color:var(--mut);font-size:16px;max-width:760px;margin:0 0 30px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.10);border-radius:22px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45);transition:transform .25s ease,border-color .25s ease}
.card:hover{transform:translateY(-4px);border-color:rgba(120,185,255,.5)}
.card .thumb{position:relative;aspect-ratio:9/16;background:#000;display:block}
.card .thumb video,.card .thumb img{width:100%;height:100%;object-fit:cover;display:block}
.card .thumb .play{position:absolute;inset:0;display:grid;place-items:center}
.card .thumb .play i{width:72px;height:72px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.card .thumb .play i:after{content:"";border-left:24px solid #0a1440;border-top:14px solid transparent;border-bottom:14px solid transparent;margin-left:6px}
.card .body{padding:16px 18px 18px}
.card h3{margin:0 0 6px;font-size:18px;font-weight:800}
.card p{margin:0 0 12px;color:var(--mut);font-size:14px;line-height:1.45}
.row{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 18px;border-radius:999px;font-weight:800;text-decoration:none;font-size:15px;border:1px solid transparent}
.btn.p{background:#fff;color:#0a1440}.btn.s{background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.18)}
.btn.p:hover{background:var(--gold)}
.meta{display:flex;gap:14px;flex-wrap:wrap;color:var(--mut);font-size:13px;margin:8px 0 0}
.meta b{color:#fff}
.spec{margin-top:40px;padding:22px;border-radius:18px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);font-size:14px;color:var(--mut);line-height:1.6}
.spec h2{margin:0 0 8px;font-size:16px;color:#fff}
/* single page */
.player{display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:34px;align-items:start;margin-top:24px}
.phone{position:relative;aspect-ratio:9/16;border-radius:34px;overflow:hidden;background:#000;border:6px solid #12193a;box-shadow:0 40px 100px rgba(0,0,0,.6)}
.phone video{width:100%;height:100%;object-fit:cover;display:block}
.unmute{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);background:rgba(255,255,255,.95);color:#0a1440;border:0;padding:12px 20px;border-radius:999px;font-weight:900;font-size:15px;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.45);display:none}
.unmute.show{display:block}
.side h2{margin:0 0 10px;font-size:26px;font-weight:900;letter-spacing:-.01em}
.side p{color:var(--mut);line-height:1.55}
.kv{display:grid;grid-template-columns:140px 1fr;gap:8px 14px;font-size:14px;margin:18px 0 22px}
.kv div:nth-child(odd){color:var(--mut)}
.script{white-space:pre-wrap;font-size:14px;line-height:1.6;color:#dfe7ff;background:rgba(0,0,0,.25);padding:16px;border-radius:14px;border:1px solid rgba(255,255,255,.08)}
@media (max-width:760px){.player{grid-template-columns:1fr}.phone{max-width:420px;margin:0 auto}}
"""

def page_head(title):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="robots" content="noindex"><link rel="icon" href="lla-logo.png"><style>{CSS}</style></head><body><div class="wrap">"""

def header():
    return """<header><img src="lla-logo.png" alt="Longevity Life Academy"><a class="tag" href="index.html">Julie Masterclass · UGC Ads</a></header>"""

def index():
    cards = []
    for a in ADS:
        cards.append(f"""<div class="card"><a class="thumb" href="{a['slug']}.html" aria-label="Open {a['title']}">
<img src="posters/{a['slug']}.jpg" alt="{a['title']} poster"><span class="play"><i></i></span></a>
<div class="body"><h3>{a['title']}</h3><p>{a['desc']}</p>
<div class="row"><a class="btn p" href="{a['slug']}.html">Play with sound</a><a class="btn s" href="videos/{a['file']}" download>Download MP4</a></div>
<div class="meta"><span><b>{a['duration']}</b> s</span><span><b>1080×1920</b> 9:16</span><span>source <b>{a['source']}</b></span><span><b>{a['size']}</b></span></div></div></div>""")
    body = f"""{header()}
<h1>Longevity Masterclass of the Year<br><span>Julie Gibson Clark · UGC ad set</span></h1>
<p class="sub">Three 9:16 talking-head ads, one script, one hook. Film opener, PR pop-up cut-in, Zoom power shot, offer closer with live-page dates and prices. Each page autoplays with sound and has a direct MP4 download for Meta upload.</p>
<div class="grid">{''.join(cards)}</div>
<div class="spec"><h2>Upload spec</h2>MP4 · H.264 · 1080×1920 · 30 fps · AAC 48 kHz stereo · captions burned in · safe zones respected (captions end above the Reels UI area). Product facts on the closer come from the live page longevitylifeacademy.com/julie-masterclass (Tue Oct 27 · 7 PM ET / Sat Nov 14 · 1 PM ET; $49; VIP $79 incl. private Q&amp;A + $249 Blueprint credit; 14-day refund).</div>
</div></body></html>"""
    open(f"{ROOT}/index.html", "w").write(page_head("Julie Masterclass UGC Ads · LLA") + body)

def single(a):
    body = f"""{header()}
<div class="player">
<div class="phone"><video id="v" src="videos/{a['file']}" poster="posters/{a['slug']}.jpg" autoplay playsinline controls preload="auto"></video>
<button class="unmute" id="um">Tap for sound</button></div>
<div class="side"><h2>{a['title']}</h2><p>{a['desc']}</p>
<div class="kv"><div>Length</div><div>{a['duration']} s</div><div>Format</div><div>1080×1920 · 9:16 · MP4 H.264 · 30 fps</div><div>Audio</div><div>AAC 48 kHz stereo, speech + film stings</div><div>Source render</div><div>{a['source']}</div><div>File size</div><div>{a['size']}</div><div>QC</div><div>{a['qc']}</div></div>
<div class="row"><a class="btn p" href="videos/{a['file']}" download>Download MP4</a><a class="btn s" href="index.html">All ads</a></div>
<h3 style="margin:28px 0 8px">Spoken script (verified transcript)</h3><div class="script">{a['transcript']}</div></div></div>
<script>
const v=document.getElementById('v'),b=document.getElementById('um');
v.muted=false;v.volume=1;
function tryPlay(){{const p=v.play();if(p)p.catch(()=>{{v.muted=true;v.play().then(()=>b.classList.add('show')).catch(()=>b.classList.add('show'));}});}}
tryPlay();
b.addEventListener('click',()=>{{v.muted=false;v.volume=1;v.currentTime=0;v.play();b.classList.remove('show');}});
v.addEventListener('volumechange',()=>{{if(!v.muted)b.classList.remove('show');}});
</script>
</div></body></html>"""
    open(f"{ROOT}/{a['slug']}.html", "w").write(page_head(f"{a['title']} · Julie Masterclass UGC") + body)

index()
for a in ADS: single(a)
print("built", len(ADS), "pages")
