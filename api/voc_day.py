"""GET /void-of-course-moon/YYYY-MM-DD (rewritten to /api/voc_day?date=...)
— server-rendered page led by void-of-course status for one calendar
date, baked into the HTML so it indexes for "void of course moon
[date]" queries distinctly from /moon/YYYY-MM-DD, which leads with the
Moon's sign instead. Same underlying data (electional.voc_intervals),
different primary framing, canonical to itself, cross-linked with the
sign-led page rather than duplicating it. Times in UTC; the live tool
localizes. Deterministic per date, so these pages are correct forever."""
import sys
from datetime import datetime, date as date_cls, timedelta, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402
import electional  # noqa: E402
import swisseph as swe  # noqa: E402


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def compute(d):
    day0 = datetime(d.year, d.month, d.day, 0, 0, tzinfo=timezone.utc)
    day1 = day0 + timedelta(days=1)
    noon = day0 + timedelta(hours=12)
    jd = engines.cs.jd_ut(noon)
    mlon = engines.cs.body_lonspeed(jd, swe.MOON)[0]
    sign, deg = engines.cs.sign_of(mlon)

    ings = electional.moon_ingresses(day0 - timedelta(hours=6), day1 + timedelta(hours=6))
    perfs = electional.moon_perfections(day0 - timedelta(days=1), day1 + timedelta(hours=6))
    vocs = electional.voc_intervals(day0 - timedelta(days=1), day1 + timedelta(hours=6), ings, perfs)
    day_voc = [(max(v0, day0), min(v1, day1)) for v0, v1 in vocs if v0 < day1 and v1 > day0]
    next_ing = next(((dt, s) for dt, s in ings if dt >= day0), None)

    def t(dt):
        return dt.strftime("%-I:%M %p UTC")

    return {"sign": sign, "deg": deg,
            "voc": [{"from": t(a), "to": t(b)} for a, b in day_voc],
            "next_ingress": {"sign": engines.cs.SIGNS[next_ing[1]], "at": t(next_ing[0])} if next_ing else None}


def render(d):
    m = compute(d)
    pretty = d.strftime("%B %-d, %Y")
    iso = d.isoformat()
    prev = (d - timedelta(days=1)).isoformat()
    nxt = (d + timedelta(days=1)).isoformat()
    is_void = bool(m["voc"])
    status = "Void of course" if is_void else "Not void of course"

    if is_void:
        spans = "; ".join(f"{v['from']} to {v['to']}" for v in m["voc"])
        answer = f"Yes, on {pretty} the Moon is void of course from {spans} (Universal Time), computed with the Swiss Ephemeris."
        body = (f"<p class=\"big\" style=\"color:#9c4460\">Void of course</p>"
                f"<p>The Moon is in <strong>{esc(m['sign'])}</strong>, making no new aspects "
                f"<strong>{esc(spans)}</strong> (UTC).</p>"
                f"<p class=\"hint\">A poor stretch to begin anything you want to go somewhere: launch, sign, decide, propose. "
                f"Good for finishing, tidying, or resting instead.</p>")
    else:
        answer = f"No, on {pretty} the Moon is not void of course; she keeps making aspects through the day, computed with the Swiss Ephemeris."
        body = (f"<p class=\"big\">Not void of course</p>"
                f"<p>The Moon is in <strong>{esc(m['sign'])}</strong>, actively forming aspects all day.</p>"
                f"<p class=\"hint\">A clear day to begin something, as far as the Moon is concerned.</p>")

    ing_line = (f"<li>Enters {esc(m['next_ingress']['sign'])} at {esc(m['next_ingress']['at'])}</li>"
                if m["next_ingress"] else "")

    faq = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"Is the Moon void of course on ' + esc(pretty) + '?",'
        '"acceptedAnswer":{"@type":"Answer","text":"' + esc(answer) + '"}},'
        '{"@type":"Question","name":"What sign is the Moon in on ' + esc(pretty) + '?",'
        '"acceptedAnswer":{"@type":"Answer","text":"On ' + esc(pretty) + ' the Moon is in ' + esc(m["sign"])
        + ', computed with the Swiss Ephemeris. Times are shown in UTC."}}]}'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Void of Course Moon on {esc(pretty)}? · The Twelve Rooms</title>
<meta name="description" content="{esc(answer)}">
<link rel="canonical" href="https://thetwelverooms.com/void-of-course-moon/{iso}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{faq}</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>Void of Course Moon on {esc(pretty)}</h1>
  <p class="lede">{"Yes" if is_void else "No"}: {esc(status.lower())} on {esc(pretty)}, computed with the Swiss Ephemeris. See the exact window below, and what to do with it.</p>
  <div class="card">
    {body}
    <ul class="facts">{ing_line}</ul>
  </div>

  <section class="prose">
    <h2>What this means for {esc(d.strftime('%B %-d'))}</h2>
    <p>Void of course is the Moon's coasting gap: after her last exact aspect in a sign, and before she crosses into the next one, she is forming no new connections. Traditionally it is a poor stretch to begin something you want to go somewhere: sign, launch, propose, decide. It is a fine stretch to finish, tidy, reflect, or rest. See the full <a href="/void-of-course-moon">guide to void of course Moon</a> for the doctrine behind it, or the <a href="/moon/{iso}">full sign and phase read for {esc(pretty)}</a>.</p>
  </section>

  <nav class="daynav">
    <a href="/void-of-course-moon/{prev}">&larr; {esc((d - timedelta(days=1)).strftime('%b %-d'))}</a>
    <a href="/void-of-course-moon">Void of course now</a>
    <a href="/void-of-course-moon/{nxt}">{esc((d + timedelta(days=1)).strftime('%b %-d'))} &rarr;</a>
  </nav>

  <div class="cta">
    <h2>Timing something on {esc(d.strftime('%B %-d'))}?</h2>
    <p>The free timing finder excludes void-of-course Moon from every window it scores, for your own city and intention.</p>
    <a href="/electional" rel="noopener">Open the timing finder</a>
  </div>
  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        raw = q.get("date", [""])[0]
        try:
            d = date_cls.fromisoformat(raw)
            if not (1900 <= d.year <= 2100):
                raise ValueError("out of range")
            html = render(d).encode()
            code, ctype = 200, "text/html; charset=utf-8"
        except Exception:
            html = (b"<!doctype html><meta charset=utf-8><title>Not found</title>"
                    b"<p style='font-family:sans-serif;padding:40px'>That date isn't valid. "
                    b"Try <a href='/void-of-course-moon'>the live void-of-course tool</a>.</p>")
            code, ctype = 404, "text/html; charset=utf-8"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(html)
