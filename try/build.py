#!/usr/bin/env python3
"""P304. One page, two paths, built from one template so they cannot drift.

/try/    is the permanent door. The URL never changes and the page grows as
         applications land.
/try/w/  is the same page on a second path, so the codes handed out on
         9/9/2026 count separately from every later scan.

A card appears here only when the application behind it is LIVE and has been
tested end to end. Nothing aspirational goes on a page the Director hands to
his friends.
"""
import pathlib

MARK = "Detter"
LINE = "Try Detter. Every answer shows its maths."
COUNT_LINE = "We count visits, nothing else."

# P304 item 4. THE COUNTER, and an honest gap.
#
# Free, no cookies, no personal data. GoatCounter's hosted free tier is
# NON-COMMERCIAL ONLY and $15/mo for business, so it is refused here for the
# same reason P299 refused Remotion and P291 flagged Open WebUI: this is a
# company. Cloudflare Web Analytics is free with no cookies and no
# fingerprinting, and its 1.1 KB beacon works on GitHub Pages, so it is the
# right answer. It needs one token from the Cloudflare dashboard, which is
# the Director's hands, and there is no free counter without an account.
#
# Until that token exists NOTHING is counted, so the page does NOT carry the
# sentence saying it counts. A disclosure line on a page that counts nothing
# is not a privacy notice, it is a false statement.
BEACON_TOKEN = ""   # paste the Cloudflare Web Analytics token here
FOOTER = "A MAG Product"

# Every card here was proven working before it was written in. See
# DECISIONS.md for the door test and why detter.pages.dev is not linked.
CARDS = [
    {
        "name": "Detter Drive",
        "what": "Put in a delivery offer and it tells you to take it or skip it, "
                "and shows you the maths it used.",
        "url": "https://detter.co.nz",
        "button": "Open Detter Drive",
        "try": "Try this: put in a $12 offer that is 6 km away and watch what it says.",
        "ios": "iPhone: tap the share button, then Add to Home Screen.",
        "android": "Android: tap the three dots, then Add to Home screen.",
    },
    {
        "name": "MirrorMirror",
        "what": "Copy something on your Mac and it is on your phone. There is no "
                "account and no cloud. This opens in demo mode, so it works with "
                "no Mac in front of you.",
        "url": "./mirrormirror/",
        "button": "Open the MirrorMirror demo",
        "try": "Try this: tap Run a sample Crunch.",
        "ios": "iPhone: tap the share button, then Add to Home Screen.",
        "android": "Android: tap the three dots, then Add to Home screen.",
    },
]

CSS = """:root{--bg:#e9e7e0;--card:#fff;--tp:#1c1c1a;--ts:#5f5e5a;--tt:#8c8b85;--go:#1d9e75}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tp);
  font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  -webkit-text-size-adjust:100%}
main{max-width:560px;margin:0 auto;padding:40px 20px 56px}
.mark{font-size:30px;font-weight:700;letter-spacing:-.5px;margin:0 0 6px}
.lede{color:var(--ts);margin:0 0 28px;font-size:18px}
.card{background:var(--card);border-radius:16px;padding:22px 20px;margin:0 0 16px}
.card h2{font-size:20px;margin:0 0 8px}
.card p{margin:0 0 16px;color:var(--ts)}
.btn{display:block;width:100%;background:var(--go);color:#fff;text-decoration:none;
  text-align:center;font-size:18px;font-weight:600;padding:16px 18px;border-radius:12px;
  min-height:52px;line-height:20px}
.btn:active{opacity:.85}
.hint{font-size:14px;color:var(--tt);margin:12px 0 0}
.hint span{display:block}
.note{color:var(--tt);font-size:13px;text-align:center;margin:26px 0 0}
footer{color:var(--tt);font-size:13px;text-align:center;margin-top:10px}
@media (prefers-color-scheme:dark){
  :root{--bg:#1a1a18;--card:#252522;--tp:#f0efe9;--ts:#b3b1a8;--tt:#87857e}}"""


def page(path_label):
    cards = []
    for c in CARDS:
        extra = f'<p class="hint">{c["try"]}</p>' if len(CARDS) == 1 else ""
        cards.append(f"""  <section class="card">
    <h2>{c['name']}</h2>
    <p>{c['what']}</p>
    <a class="btn" href="{c['url']}">{c['button']}</a>
    {extra}
    <p class="hint"><span>{c['ios']}</span><span>{c['android']}</span></p>
  </section>""")
    beacon = (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              f'data-cf-beacon=\'{{"token": "{BEACON_TOKEN}"}}\'></script>') if BEACON_TOKEN else ""
    count = f'  <p class="note">{COUNT_LINE}</p>\n' if BEACON_TOKEN else ""
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Try Detter</title>
<meta name="description" content="{LINE}">
<meta name="robots" content="noindex">
<style>{CSS}</style>
</head>
<body>
<main>
  <h1 class="mark">{MARK}</h1>
  <p class="lede">{LINE}</p>
{chr(10).join(cards)}
{count}  <footer>{FOOTER}</footer>
</main>
{beacon}
<!-- path:{path_label} -->
</body>
</html>
"""


root = pathlib.Path(__file__).parent
(root / "index.html").write_text(page("try"), encoding="utf-8")
(root / "w" / "index.html").write_text(page("try-w"), encoding="utf-8")
print("wrote /try/index.html and /try/w/index.html")
for f in ("index.html", "w/index.html"):
    b = (root / f).stat().st_size
    print(f"  {f}: {b} bytes")
