"""GET /saturn-return/YYYY  (rewritten to /api/saturn_year?year=...) —
server-rendered page: for anyone born in a given year, the sign(s) Saturn
occupied that year and the calendar window of their first (and second)
Saturn return, baked into the HTML so it indexes. Exact months depend on
the birth date, which is the handoff into the /saturn-return-calculator.
Saturn's motion is deterministic, so these pages are correct forever."""
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402
import swisseph as swe  # noqa: E402

cs = engines.cs
SATURN = swe.SATURN

# What Saturn's stay in each sign asks a person to build. Honest, no doom.
SIGN_THEME = {
    "Aries": "acting with patience, and forging raw courage into something that holds",
    "Taurus": "security and worth, the slow work of building something solid and truly your own",
    "Gemini": "the discipline of thought and word, and finishing what you start saying",
    "Cancer": "home, roots, and emotional structure, learning to feel safe on your own terms",
    "Leo": "authentic authority, earning real confidence without needing the applause",
    "Virgo": "craft and usefulness, the patience to do the unglamorous work well",
    "Libra": "commitment and fairness, learning what you owe others and what you are owed",
    "Scorpio": "trust, power, and depth, the work of facing what you would rather not",
    "Sagittarius": "meaning and belief, turning a restless search into ground you can stand on",
    "Capricorn": "ambition and responsibility, the long climb toward something real (Saturn's own sign)",
    "Aquarius": "your place in the group and the structures that outlast you (Saturn's own sign)",
    "Pisces": "boundaries and faith, giving form to compassion without losing yourself in it",
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _jd(y, m, d):
    return cs.jd_ut(datetime(y, m, d, 12, tzinfo=timezone.utc))


def _sign_at(jd):
    return cs.sign_of(cs.body_lonspeed(jd, SATURN)[0])[0]


def _find_ingress_day(jd_lo, jd_hi):
    """jd_lo and jd_hi hold different signs; binary-search the boundary to
    day precision. Returns the first jd on the jd_hi side of the crossing."""
    target = _sign_at(jd_lo)
    lo, hi = jd_lo, jd_hi
    while hi - lo > 1:
        mid = (lo + hi) / 2
        if _sign_at(mid) == target:
            lo = mid
        else:
            hi = mid
    return hi


def year_signs(year):
    """Sign(s) Saturn occupied during `year`, in order. Returns a list of
    (sign, ingress_jd); the first entry's ingress is None (the sign it was
    already in on Jan 1). Compares the year's endpoints, so a brief
    retrograde wobble at a cusp is smoothed to the dominant transition."""
    jd0, jd1 = _jd(year, 1, 1), _jd(year, 12, 31)
    s0, s1 = _sign_at(jd0), _sign_at(jd1)
    if s0 == s1:
        return [(s0, None)]
    return [(s0, None), (s1, _find_ingress_day(jd0, jd1))]


def return_years(sign, year_lo, year_hi):
    """Calendar-year span in which transiting Saturn re-occupies `sign`
    within [year_lo, year_hi]. Year precision is deliberate: the exact
    months need a birth date. Returns (first_year, last_year) or None."""
    x, end = _jd(year_lo, 1, 1), _jd(year_hi, 12, 31)
    first = last = None
    while x <= end:
        if _sign_at(x) == sign:
            if first is None:
                first = x
            last = x
        x += 5.0
    if first is None:
        return None
    return swe.revjul(first, swe.GREG_CAL)[0], swe.revjul(last, swe.GREG_CAL)[0]


def _fmt_day(jd):
    y, m, d, _ = swe.revjul(jd, swe.GREG_CAL)
    return datetime(y, m, int(d)).strftime("%B %-d, %Y")


def _win_phrase(years):
    return str(years[0]) if years[0] == years[1] else f"{years[0]} to {years[1]}"


def _sign_block(sign, born_year):
    """The computed facts for one natal Saturn sign: first and second
    return windows, ages, and the sign's theme."""
    first = return_years(sign, born_year + 26, born_year + 33)
    second = return_years(sign, born_year + 55, born_year + 62)
    return {"sign": sign, "theme": SIGN_THEME.get(sign, "structure and time"),
            "first": first, "second": second}


def render(year):
    signs = year_signs(year)
    blocks = [(_sign_block(s, year), ing) for s, ing in signs]
    two = len(blocks) == 2

    # Lede + the headline window (first block's first return).
    lead = blocks[0][0]
    lead_first = lead["first"]
    first_phrase = _win_phrase(lead_first) if lead_first else "your late twenties"
    if two:
        ing_day = _fmt_day(blocks[1][1])
        sign_summary = (f"Saturn changed signs in {year}: it was in <strong>{esc(blocks[0][0]['sign'])}</strong> "
                        f"until {esc(ing_day)}, then moved into <strong>{esc(blocks[1][0]['sign'])}</strong>. "
                        f"Which one is your natal Saturn depends on whether you were born before or after that date.")
        meta_signs = f"{blocks[0][0]['sign']} or {blocks[1][0]['sign']}"
    else:
        sign_summary = (f"If you were born in {year}, your natal Saturn is in "
                        f"<strong>{esc(lead['sign'])}</strong>.")
        meta_signs = lead["sign"]

    # Per-sign detail cards.
    cards = []
    for blk, ing in blocks:
        s = blk["sign"]
        who = ""
        if two:
            if ing is None:
                who = f'<p class="hint">For {esc(year)} births before {esc(_fmt_day(blocks[1][1]))}.</p>'
            else:
                who = f'<p class="hint">For {esc(year)} births on or after {esc(_fmt_day(ing))}.</p>'
        first_txt = (f"Saturn is back in {esc(s)} across <strong>{esc(_win_phrase(blk['first']))}</strong>; "
                     f"your exact return, near age 29 to 30, lands inside that window"
                     if blk["first"] else "in your late twenties")
        second_txt = ""
        if blk["second"]:
            second_txt = (f"<li><strong>Second Saturn return:</strong> around "
                          f"{esc(_win_phrase(blk['second']))}, near age 58 to 59.</li>")
        cards.append(f"""<div class="card">
      {who}
      <div class="big">&#9796; Saturn in {esc(s)}</div>
      <p class="moon-mood">A Saturn return in {esc(s)} is about {esc(blk['theme'])}.</p>
      <ul class="facts">
        <li><strong>First Saturn return:</strong> {first_txt}.</li>
        {second_txt}
      </ul>
    </div>""")

    prev_y, next_y = year - 1, year + 1
    faq = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        '{"@type":"Question","name":"When is the Saturn return for someone born in ' + esc(year) + '?",'
        '"acceptedAnswer":{"@type":"Answer","text":"'
        + esc(f"If you were born in {year}, your first Saturn return lands in the window {first_phrase}, "
              f"with the exact return near age 29 to 30, when transiting Saturn comes back to the sign it "
              f"held at your birth. The exact dates depend on your birth date and are computed by the free "
              f"Saturn return calculator.")
        + '"}},'
        '{"@type":"Question","name":"What sign is Saturn in for ' + esc(year) + ' births?",'
        '"acceptedAnswer":{"@type":"Answer","text":"'
        + esc(f"For {year} births, natal Saturn is in {meta_signs}, computed with the Swiss Ephemeris.")
        + '"}}]}'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Saturn Return for {esc(year)} Births: When Is It? &middot; The Twelve Rooms</title>
<meta name="description" content="Born in {esc(year)}? Your natal Saturn is in {esc(meta_signs)}, and your first Saturn return lands in {esc(first_phrase)}, near age 29 to 30. Computed with the Swiss Ephemeris. Get your exact dates with the free calculator.">
<link rel="canonical" href="https://thetwelverooms.com/saturn-return/{year}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{faq}</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>Saturn return for {esc(year)} births</h1>
  <p class="lede">{sign_summary} Your first Saturn return, when Saturn comes home to that sign, lands in the window <strong>{esc(first_phrase)}</strong>, with the exact return near age 29 to 30. Times to the day depend on your exact birth date: get them free in the <a href="/saturn-return-calculator">Saturn return calculator</a>.</p>

  {''.join(cards)}

  <section class="prose">
    <h2>What the Saturn return is</h2>
    <p>Saturn takes about twenty-nine and a half years to circle the zodiac, so a little before you turn thirty it arrives back at the place it sat when you were born. That homecoming is your <strong>Saturn return</strong>, and the tradition treats it as the true threshold into adulthood: the season the life you built in your twenties gets its first honest audit. What is real is confirmed; what was scaffolding tends to come loose. It is demanding, not cursed, and in hindsight it is almost always the making of the next version of you.</p>
    <p>Because Saturn spends part of most years retrograde, a return can arrive as one clean pass or as three passes spread across roughly a year. The honest way to hold it is as a window, the whole stretch Saturn spends on your natal degree, rather than a single day. For {esc(year)} births that window is the range above; your exact passes come from your birth date.</p>
    <h2>Get your exact dates</h2>
    <p>This page is keyed to your birth year, which pins the sign and the rough window. Your precise passes, and the house the return lands in, come from your full birth details. The <a href="/saturn-return-calculator">free calculator</a> computes them to the day, and nothing is stored.</p>
  </section>

  <nav class="daynav">
    <a href="/saturn-return/{prev_y}">&larr; {esc(prev_y)} births</a>
    <a href="/saturn-return-calculator">Your exact dates</a>
    <a href="/saturn-return/{next_y}">{esc(next_y)} births &rarr;</a>
  </nav>

  <div class="cta">
    <h2>The dates are free. The meaning is the reading.</h2>
    <p>The Twelve Rooms Saturn Return reading reads your natal Saturn in full, the room the return lands in, and what this season is here to confirm, honestly and without doom.</p>
    <a href="/reports">Explore the Saturn return reading</a>
  </div>
  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        raw = q.get("year", [""])[0]
        try:
            year = int(raw)
            if not (1900 <= year <= 2100):
                raise ValueError("out of range")
            html = render(year).encode()
            code, ctype = 200, "text/html; charset=utf-8"
        except Exception:
            html = (b"<!doctype html><meta charset=utf-8><title>Not found</title>"
                    b"<p style='font-family:sans-serif;padding:40px'>That year isn't valid. "
                    b"Try the <a href='/saturn-return-calculator'>Saturn return calculator</a>.</p>")
            code, ctype = 404, "text/html; charset=utf-8"
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(html)
