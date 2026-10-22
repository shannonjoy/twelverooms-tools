"""GET /big-3/<sun>-<moon>-<rising> (rewritten to /api/big3?combo=...) — the
shareable Big 3 page.

The URL is built from three sign names only, never a birth date, time
or place. /big-3/<sun>-<moon> is the untimed form (no rising sign).

Scaled-content guard (2026-10-21): there are 12 x 12 x 13 = 1,872 possible
combinations and every one shares the calculator's copy, so every one is
served `noindex, follow` (meta tag and X-Robots-Tag header), carries no
canonical of its own, and is left out of the sitemap. The pages exist to be
shared and to send people to /big-3-calculator, not to rank.
"""
import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent))
import crawl       # noqa: E402
import big3_copy   # noqa: E402

SITE = "https://thetwelverooms.com"
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
BY_SLUG = {s.lower(): s for s in SIGNS}
ELEMENT = {s: ["fire", "earth", "air", "water"][i % 4] for i, s in enumerate(SIGNS)}
SLUG = "|".join(BY_SLUG)
COMBO_RE = re.compile(rf"^({SLUG})-({SLUG})(?:-({SLUG}))?$")
GLYPH = {s: chr(0x2648 + i) for i, s in enumerate(SIGNS)}

e = html.escape


def parse(combo):
    """(sun, moon, rising or None), or None if the path is not a Big 3."""
    m = COMBO_RE.match((combo or "").strip().lower())
    if not m:
        return None
    sun, moon, rising = (BY_SLUG[g] if g else None for g in m.groups())
    return sun, moon, rising


def element_line(sun, moon, rising):
    els = [ELEMENT[sun], ELEMENT[moon]] + ([ELEMENT[rising]] if rising else [])
    if len(set(els)) == 1:
        return (f"All {els[0]}: one element runs through how you arrive, what you want and what "
                f"you need, so the tone stays consistent all the way down.")
    if len(set(els)) == len(els):
        return ("Every one in a different element: real range on purpose. You carry more than one "
                "register, and each one is true.")
    common = max(set(els), key=els.count)
    return (f"Two of the three in {common}: that element sets the keynote, and the other gives it "
            f"somewhere to go.")


def glyph(sign):
    return (f'<svg viewBox="0 0 24 24" width="1.05em" height="1.05em" style="vertical-align:-0.16em;'
            f'overflow:visible" aria-hidden="true"><text x="12" y="13" text-anchor="middle" '
            f'dominant-baseline="central" font-family="-apple-system,Helvetica,Arial,sans-serif" '
            f'font-size="22" fill="currentColor">{GLYPH[sign]}︎</text></svg>')


def render(sun, moon, rising):
    title = f"{sun} Sun, {moon} Moon" + (f", {rising} Rising" if rising else "") + ": a Big 3"
    desc = (f"A Big 3 of {sun} Sun, {moon} Moon" + (f" and {rising} rising" if rising else "")
            + ", read together. Find your own Sun, Moon and rising sign free at The Twelve Rooms.")
    path = "/big-3/" + "-".join(s.lower() for s in (sun, moon, rising) if s)
    url = SITE + path

    def box(label, sign):
        if not sign:
            return f'<div><span class="tg">&middot;</span><b>&mdash;</b><span>{label}</span></div>'
        return f'<div><span class="tg">{glyph(sign)}</span><b>{sign}</b><span>{label}</span></div>'

    def row(sign, head, text):
        return (f'<div class="place"><div class="place-glyph">{glyph(sign)}</div><div>'
                f'<div class="place-head">{e(head)}</div><div class="place-mean">{e(text)}</div></div></div>')

    rows = []
    if rising:
        rows.append(row(rising, f"{rising} rising · how you arrive", big3_copy.RISING[rising]))
    rows.append(row(sun, f"{sun} Sun · what you are becoming", big3_copy.SUN[sun]))
    rows.append(row(moon, f"{moon} Moon · what settles you", big3_copy.MOON[moon]))
    untimed = "" if rising else (
        '<p class="hint" style="margin-top:10px">Shared without a rising sign: that one needs a birth '
        'time.</p>')
    og = f"{SITE}/og/big-3.png"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · The Twelve Rooms</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Twelve Rooms">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="My Big 3: Sun, Moon and rising sign, from The Twelve Rooms.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div id="masthead"></div>
<main class="wrap" id="main-content" tabindex="-1">
  <h1>{e(sun)} Sun, {e(moon)} Moon{(", " + e(rising) + " rising") if rising else ""}</h1>
  <p class="lede">Someone shared their Big 3 with you: the Sun, Moon and rising sign, the short version of a whole chart. {e(element_line(sun, moon, rising))}</p>
  <div class="glance">
    <h2>A Big 3</h2>
    <div class="triad">{box("Rising", rising)}{box("Sun", sun)}{box("Moon", moon)}</div>
  </div>
  <div class="card" data-big3 data-sun="{sun}" data-moon="{moon}" data-rising="{rising or ''}">
    <div class="places">
      {"".join(rows)}
    </div>
    {untimed}
  </div>
  <div class="cta">
    <h2>What is your Big 3?</h2>
    <p>Your Sun, Moon and rising sign, computed with the Swiss Ephemeris from your birth date, time and place. Free, no account.</p>
    <a href="/big-3-calculator">Find my Big 3</a>
  </div>
  <section class="prose">
    <h2>Reading a Big 3</h2>
    <p>Read the three as one voice in three registers. The rising sign is how a person arrives, the Sun is what they are becoming, and the Moon is what they need underneath it all. The rest of the chart, every planet, house and aspect, is the long version; a <a href="/natal-chart">free natal chart</a> shows it whole.</p>
  </section>
  <div id="site-footer">{crawl.FOOTER_HTML}</div>
</main>
<script src="/tools.js"></script>
<script src="/big3-share.js"></script>
</body>
</html>
"""


NOT_FOUND = (b"<!doctype html><meta charset=utf-8><meta name=robots content='noindex'>"
             b"<title>Not found</title><p style='font-family:sans-serif;padding:40px'>That is not a "
             b"Big 3 link. Find yours with the <a href='/big-3-calculator'>Big 3 calculator</a>.</p>")
