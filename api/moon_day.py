"""GET /moon/YYYY-MM-DD  (rewritten to /api/moon_day?date=...) —
server-rendered page: the Moon's sign, phase, ingress, and void-of-course
windows for one calendar date, baked into the HTML so it indexes. Times
in UTC; the live tool localizes. Data is deterministic per date, so these
pages are correct forever."""
import sys
from datetime import datetime, date as date_cls, timedelta, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402
import electional  # noqa: E402
import swisseph as swe  # noqa: E402

SIGN_STYLE = {
    "Aries": "bold and headlong", "Taurus": "steady and sensory",
    "Gemini": "quick and curious", "Cancer": "tender and protective",
    "Leo": "warm and wholehearted", "Virgo": "precise and useful",
    "Libra": "gracious and relational", "Scorpio": "intense and deep",
    "Sagittarius": "restless and searching", "Capricorn": "serious and steady",
    "Aquarius": "cool and original", "Pisces": "dreamy and soft",
}
PHASE_MEAN = {
    "New Moon": "a beginning, a seed in the dark, good for setting intentions",
    "Waxing Crescent": "building, taking the first real steps",
    "First Quarter": "a push and a decision point, act on what you started",
    "Waxing Gibbous": "refining and polishing, almost there",
    "Full Moon": "culmination and full light, things come to a head",
    "Waning Gibbous": "sharing and giving back what you gathered",
    "Last Quarter": "release and turning, let go of what is done",
    "Waning Crescent": "rest and surrender before the next cycle",
}
PHASES = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
          "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def compute(d):
    day0 = datetime(d.year, d.month, d.day, 0, 0, tzinfo=timezone.utc)
    day1 = day0 + timedelta(days=1)
    noon = day0 + timedelta(hours=12)
    jd = engines.cs.jd_ut(noon)
    mlon = engines.cs.body_lonspeed(jd, swe.MOON)[0]
    slon = engines.cs.body_lonspeed(jd, swe.SUN)[0]
    sign, deg = engines.cs.sign_of(mlon)
    elong = (mlon - slon) % 360
    phase = PHASES[int(((elong + 22.5) % 360) // 45)]

    ings = electional.moon_ingresses(day0 - timedelta(hours=6), day1 + timedelta(hours=6))
    perfs = electional.moon_perfections(day0 - timedelta(days=1), day1 + timedelta(hours=6))
    vocs = electional.voc_intervals(day0 - timedelta(days=1), day1 + timedelta(hours=6), ings, perfs)

    day_ing = [(dt, s) for dt, s in ings if day0 <= dt < day1]
    day_voc = [(max(v0, day0), min(v1, day1)) for v0, v1 in vocs if v0 < day1 and v1 > day0]

    def t(dt):
        return dt.strftime("%-I:%M %p UTC")

    return {"sign": sign, "deg": deg, "phase": phase,
            "ingress": [{"sign": engines.cs.SIGNS[s], "at": t(dt)} for dt, s in day_ing],
            "voc": [{"from": t(a), "to": t(b)} for a, b in day_voc]}


def render(d):
    m = compute(d)
    pretty = d.strftime("%B %-d, %Y")
    iso = d.isoformat()
    prev = (d - timedelta(days=1)).isoformat()
    nxt = (d + timedelta(days=1)).isoformat()
    sign = m["sign"]
    style = SIGN_STYLE.get(sign, "distinct")
    phase_mean = PHASE_MEAN.get(m["phase"], "")
    ing_txt = ""
    if m["ingress"]:
        i = m["ingress"][0]
        ing_txt = f" It crosses into {i['sign']} at {i['at']}, so the day carries both moods."
    voc_line = ""
    if m["voc"]:
        spans = "; ".join(f"{v['from']} to {v['to']}" for v in m["voc"])
        voc_line = (f"<li><strong>Void of course:</strong> {esc(spans)}. "
                    f"Poor timing to begin anything you want to go somewhere.</li>")
    else:
        voc_line = "<li>The Moon makes clean aspects through the day (no long void window).</li>"

    faq = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"What sign is the Moon in on ' + esc(pretty) + '?",'
        '"acceptedAnswer":{"@type":"Answer","text":"On ' + esc(pretty) + ' the Moon is in ' + esc(sign)
        + ' (' + esc(m["phase"]) + '), computed with the Swiss Ephemeris. Times are shown in UTC."}},'
        '{"@type":"Question","name":"Is the Moon void of course on ' + esc(pretty) + '?",'
        '"acceptedAnswer":{"@type":"Answer","text":"'
        + (esc("Yes, during " + "; ".join(v["from"] + " to " + v["to"] for v in m["voc"]) + " UTC.") if m["voc"]
           else "No long void-of-course window that day; the Moon keeps making aspects.")
        + '"}}]}'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moon Sign on {esc(pretty)}: What Sign Is the Moon In? · The Twelve Rooms</title>
<meta name="description" content="On {esc(pretty)} the Moon is in {esc(sign)} ({esc(m['phase'])}). See the sign, phase, void-of-course windows, and any sign change that day, computed with the Swiss Ephemeris.">
<link rel="canonical" href="https://thetwelverooms.com/moon/{iso}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{faq}</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>The Moon on {esc(pretty)}</h1>
  <p class="lede">Where the Moon sits on {esc(pretty)}: her sign, phase, and void-of-course windows, computed with the Swiss Ephemeris. Times in UTC; for your own timezone see the <a href="/moon">live Moon tool</a>.</p>
  <div class="card">
    <div class="big">&#9789; {esc(sign)}</div>
    <p><strong>{esc(m['phase'])}</strong>{' &middot; <strong style="color:#9c4460">void of course part of the day</strong>' if m['voc'] else ' &middot; making aspects all day'}</p>
    <p class="moon-mood">With the Moon in {esc(sign)}, the emotional weather runs {esc(style)}.{esc(ing_txt)} The {esc(m['phase'].lower())} is {esc(phase_mean)}.</p>
    <ul class="facts">
      {''.join(f'<li>Enters {esc(i["sign"])} at {esc(i["at"])}</li>' for i in m['ingress'])}
      {voc_line}
    </ul>
  </div>

  <section class="prose">
    <h2>What a {esc(sign)} Moon feels like</h2>
    <p>When the Moon moves through {esc(sign)}, the mood of the day tilts {esc(style)}. The Moon is the fastest body in the sky and she sets the emotional weather, so this is the undertone beneath {esc(pretty)}, changing again in a day or two as she moves on.{esc(ing_txt)}</p>
    <p>Her phase is the other half. This is a <strong>{esc(m['phase'].lower())}</strong>: {esc(phase_mean)}. If you are timing something that matters, the rule of thumb is to build on a waxing Moon, release on a waning one, and steer clear of the void-of-course windows above.</p>
    <p>For the void-of-course windows on {esc(pretty)} led up front, with what to do about them, see the <a href="/void-of-course-moon/{iso}">void of course read for this date</a>.</p>
  </section>

  <nav class="daynav">
    <a href="/moon/{prev}">&larr; {esc((d - timedelta(days=1)).strftime('%b %-d'))}</a>
    <a href="/moon">Today's Moon</a>
    <a href="/moon/{nxt}">{esc((d + timedelta(days=1)).strftime('%b %-d'))} &rarr;</a>
  </nav>

  <div class="cta">
    <h2>Timing something on {esc(d.strftime('%B %-d'))}?</h2>
    <p>Find the exact best window for your city and intention in the free timing finder, or ask The Twelve Rooms for a full reading.</p>
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
                    b"Try <a href='/moon'>the live Moon tool</a>.</p>")
            code, ctype = 404, "text/html; charset=utf-8"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(html)
