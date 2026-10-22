"""Saturn endpoints, two methods on one function (Hobby-plan function budget):

POST /api/saturn — free Saturn return dates from birth data.
Body: {date, time?, tz, lat, lon}. Computes the natal Saturn longitude,
then every Saturn return (exact passes, stations, sign window, return
number). Birth data is processed in memory and never stored or logged.
Shares the exact-return math with the Saturn Return Report engine
(factsheet/saturn_return.py) via build_returns, so the free tool and the
paid product can never disagree.

GET /saturn-return/YYYY  (rewritten to /api/saturn?year=...) —
server-rendered page: for anyone born in a given year, the sign(s) Saturn
occupied that year and the calendar window of their first (and second)
Saturn return, baked into the HTML so it indexes. Exact months depend on
the birth date, which is the handoff into the /saturn-return-calculator.
Saturn's motion is deterministic, so these pages are correct forever."""
import json
import sys
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
sys.path.insert(0, str(Path(__file__).parent / "_seo"))
import engines            # noqa: E402
import crawl              # noqa: E402
import shop               # noqa: E402
import saturn_return as sr  # noqa: E402
import swisseph as swe    # noqa: E402

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


def sign_passes(sign, year_lo, year_hi):
    """Every day transiting Saturn entered or left `sign` between Jan 1 of
    year_lo and Dec 31 of year_hi, as [(jd, "enters"|"leaves")]. Retrograde
    returns show up as a leave and a re-entry, which is the honest shape of
    a three-pass return."""
    x, end = _jd(year_lo, 1, 1), _jd(year_hi, 12, 31)
    inside = _sign_at(x) == sign
    out = []
    while x < end:
        nxt = min(x + 2.0, end)
        now_in = _sign_at(nxt) == sign
        if now_in != inside:
            out.append((_find_ingress_day(x, nxt), "enters" if now_in else "leaves"))
            inside = now_in
        x = nxt
    return out


def _tense(sign, years, today=None):
    """past, now or future for a return, judged to the day: the return is
    over once Saturn has left the sign for the last time inside the window,
    and has not begun until it first enters."""
    today_jd = _jd(*(today or date.today()).timetuple()[:3])
    moves = sign_passes(sign, years[0] - 1, years[1])
    entries = [j for j, k in moves if k == "enters"]
    leaves = [j for j, k in moves if k == "leaves"]
    first_in = entries[0] if entries else _jd(years[0], 1, 1)
    last_out = leaves[-1] if leaves else _jd(years[1], 12, 31)
    if last_out < today_jd:
        return "past"
    if first_in <= today_jd:
        return "now"
    return "future"


def _win_phrase(years):
    return str(years[0]) if years[0] == years[1] else f"{years[0]} to {years[1]}"


def _sign_block(sign, born_year):
    """The computed facts for one natal Saturn sign: first and second
    return windows, ages, and the sign's theme."""
    first = return_years(sign, born_year + 26, born_year + 33)
    second = return_years(sign, born_year + 55, born_year + 62)
    return {"sign": sign, "theme": SIGN_THEME.get(sign, "structure and time"),
            "first": first, "second": second}


# ---------- Per-birth-month data (2026-10-21, index plan) ----------
# Google read the 46 cohort pages as one template with the year swapped
# (78% of sentences shared between neighbouring years). What is genuinely
# different about each birth year is the arithmetic, so the page now shows
# it: for a birth on the 15th of every month, the natal Saturn degree and
# every exact pass of the first return, found with the same calc, angdiff
# and bisection the calculator and the Saturn Return Report use.
ROW_DAY = 15
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def _noon(y, m, d):
    return sr._noon_jd(date(y, m, d))


def first_return(natal_lon, born):
    """Exact passes of the FIRST Saturn return for natal_lon, as a list of
    (jd, "direct"|"retrograde"). Daily scan from age 26 to 33 (the first
    return cannot fall outside that span), each crossing refined by
    bisection, clustered the way saturn_return.find_returns clusters."""
    crossings = []
    prev_jd = prev_delta = None
    start = date(born.year + 26, born.month, min(born.day, 28))
    for i in range(0, int(7 * 365.25)):
        jd = sr._noon_jd(start) + i
        delta = sr.angdiff(sr.calc(jd, SATURN)[0], natal_lon)
        if (prev_delta is not None and (prev_delta < 0) != (delta < 0)
                and abs(delta) < 1 and abs(prev_delta) < 1):
            exact = sr._bisect(prev_jd, jd,
                               lambda j: sr.angdiff(sr.calc(j, SATURN)[0], natal_lon))
            crossings.append(exact)
        prev_jd, prev_delta = jd, delta
    event = []
    for jd in crossings:
        if event and jd - event[-1] >= 500:
            break
        event.append(jd)
    return [(j, "retrograde" if sr.calc(j, SATURN)[1] < 0 else "direct") for j in event]


def _deg(lon):
    s, d = sr.sign_of(lon)
    m = int((d % 1) * 60)
    return f"{int(d)}&deg;{m:02d}&prime; {s}"


def _short(jd):
    y, m, d, _ = swe.revjul(jd, swe.GREG_CAL)
    return datetime(y, m, int(d)).strftime("%b %-d, %Y")


def _age(jd, born):
    y, m, d, _ = swe.revjul(jd, swe.GREG_CAL)
    return y - born.year - ((m, int(d)) < (born.month, born.day))


def month_rows(year):
    rows = []
    for mi in range(1, 13):
        born = date(year, mi, ROW_DAY)
        lon, speed = sr.calc(_noon(year, mi, ROW_DAY), SATURN)
        last = (date(year + (mi == 12), mi % 12 + 1, 1) - timedelta(days=1)).day
        lo = sr.calc(_noon(year, mi, 1), SATURN)[0]
        hi = sr.calc(_noon(year, mi, last), SATURN)[0]
        rows.append({"month": MONTHS[mi - 1], "born": born, "lon": lon,
                     "sign": sr.sign_of(lon)[0], "retro": speed < 0,
                     "span": (lo, hi), "passes": first_return(lon, born)})
    return rows


def year_stations(year):
    """Saturn's stations during the birth year, with the degree."""
    out = []
    for s in sr.stations_between(_jd(year, 1, 1), _jd(year, 12, 31) + 1):
        dt = datetime.fromisoformat(s["utc"])
        jd = sr.jd_ut(dt)
        out.append((jd, s["type"].replace("stations ", ""), sr.calc(jd, SATURN)[0]))
    return out


def year_ingresses(year):
    """Every sign change Saturn made during `year`, as [(jd, from, to)].
    year_signs compares only the endpoints, which hides a retrograde dip
    back across a cusp (1988 had three ingresses, not one)."""
    x, end = _jd(year, 1, 1), _jd(year, 12, 31)
    cur = _sign_at(x)
    out = []
    while x < end:
        nxt = min(x + 2.0, end)
        s = _sign_at(nxt)
        if s != cur:
            lo, hi = x, nxt
            while hi - lo > 1 / 1440:  # refine the crossing to the minute
                mid = (lo + hi) / 2
                if _sign_at(mid) == cur:
                    lo = mid
                else:
                    hi = mid
            out.append((hi, cur, s))
            cur = s
        x = nxt
    return out


_WORD = {2: "two", 3: "three", 4: "four"}


def _and(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def render(year):
    ingresses = year_ingresses(year)
    order = [_sign_at(_jd(year, 1, 1))]
    for _, _, to in ingresses:
        if to not in order:
            order.append(to)
    blocks = [(_sign_block(s, year), None) for s in order]
    rows = month_rows(year)
    stations = year_stations(year)

    all_passes = [p for r in rows for p in r["passes"]]
    earliest = min(all_passes, key=lambda p: p[0])[0] if all_passes else None
    latest = max(all_passes, key=lambda p: p[0])[0] if all_passes else None
    ages = sorted({_age(r["passes"][0][0], r["born"]) for r in rows if r["passes"]})
    age_txt = (f"age {ages[0]}" if len(ages) == 1 else f"ages {ages[0]} to {ages[-1]}") if ages else "age 29 to 30"
    counts = {}
    for r in rows:
        counts[len(r["passes"])] = counts.get(len(r["passes"]), 0) + 1
    today_jd = _jd(*date.today().timetuple()[:3])
    if latest is not None and latest < today_jd:
        tense = "past"
    elif earliest is not None and earliest <= today_jd:
        tense = "now"
    else:
        tense = "future"
    year_lo = _deg(sr.calc(_noon(year, 1, 1), SATURN)[0])
    year_hi = _deg(sr.calc(_noon(year, 12, 31), SATURN)[0])
    span_plain = f"{_short(earliest)} and {_short(latest)}" if earliest else "your late twenties"
    lead_verb = {"past": "fell between", "now": "runs between", "future": "falls between"}[tense]

    meta_signs = " or ".join(b["sign"] for b, _ in blocks)
    if len(ingresses) > 1:
        moves = [f"into {esc(to)} on {esc(_fmt_day(j))}" for j, _, to in ingresses]
        sign_line = (f"Saturn changed sign {_WORD[len(ingresses)]} times in {esc(year)}, crossing the cusp and "
                     f"back again around a retrograde station: {_and(moves)}. Natal Saturn's sign for a "
                     f"{esc(year)} birthday depends on which side of those dates it falls.")
        sign_rule = (f"Saturn crossed the cusp {_WORD[len(ingresses)]} times that year ("
                     + ", ".join(f"into {to} on {_fmt_day(j)}" for j, _, to in ingresses)
                     + "), so the birth date decides which. ")
    elif ingresses:
        j, fr, to = ingresses[0]
        sign_line = (f"Saturn moved from {esc(fr)} into {esc(to)} on {esc(_fmt_day(j))}, so a "
                     f"{esc(year)} birthday before that date has natal Saturn in {esc(fr)} and one "
                     f"after it in {esc(to)}.")
        sign_rule = f"Saturn changed sign on {_fmt_day(j)}, so the birth date decides which. "
    else:
        sign_line = f"Every {esc(year)} birthday has natal Saturn in {esc(blocks[0][0]['sign'])}."
        sign_rule = ""
    answer = (f"Born in {esc(year)}? Natal Saturn ran from {year_lo} on January 1 to {year_hi} on "
              f"December 31. Computed day by day, the first Saturn return for a {esc(year)} birthday "
              f"{lead_verb} <strong>{esc(span_plain)}</strong>, at {esc(age_txt)}.")
    answer_plain = (f"For a {year} birthday, the first exact Saturn return {lead_verb} {span_plain}, "
                    f"at {age_txt}, computed with the Swiss Ephemeris for a birth on the 15th of each month.")

    # Table: one row per birth month.
    trs = []
    for r in rows:
        if r["passes"]:
            cells = "<br>".join(f"{esc(_short(j))} <span class=\"hint\">({k})</span>" for j, k in r["passes"])
            age = _age(r["passes"][0][0], r["born"])
        else:
            cells, age = "not found in ages 26 to 33", ""
        rx = " <span class=\"hint\">(Rx)</span>" if r["retro"] else ""
        trs.append(f'        <tr id="{r["month"].lower()}"><td><strong>{esc(r["month"])}</strong></td>'
                   f'<td>{_deg(r["lon"])}{rx}</td><td>{cells}</td><td>{esc(age)}</td></tr>')

    # Year-specific sky sentences.
    sky = [sign_line]
    if stations:
        st = [f"{k} on {esc(_fmt_day(j))} at {_deg(l)}" for j, k, l in stations]
        sky.append(f"That year Saturn stationed {_and(st)}.")
        retro_rows = [r["month"] for r in rows if r["retro"]]
        if retro_rows:
            sky.append(f"Mid-month births in {esc(_and(retro_rows))} have natal Saturn retrograde, "
                       f"marked Rx in the table.")
    single = counts.get(1, 0)
    triple = counts.get(3, 0)
    parts = []
    if single:
        parts.append(f"{single} of {year}'s 12 birth months get a single-pass return")
    if triple:
        parts.append(f"{triple} of them get three passes, because Saturn turns retrograde across the natal degree")
    if counts.get(2):
        parts.append(f"{counts[2]} get two, with a station sitting almost on the natal degree")
    if parts:
        s_ = _and(parts)
        sky.append(s_[0].upper() + s_[1:] + ".")
    longest = max((r for r in rows if r["passes"]), key=lambda r: r["passes"][-1][0] - r["passes"][0][0], default=None)
    if longest and len(longest["passes"]) > 1:
        days_ = int(round(longest["passes"][-1][0] - longest["passes"][0][0]))
        sky.append(f"The longest stretch belongs to {esc(longest['month'])} birthdays: {days_} days from the "
                   f"first exact pass on {esc(_fmt_day(longest['passes'][0][0]))} to the last on "
                   f"{esc(_fmt_day(longest['passes'][-1][0]))}.")
    seconds = [b for b, _ in blocks if b["second"]]
    if seconds:
        sec = "; ".join(f"for {esc(year)} births with natal Saturn in {esc(b['sign'])}, Saturn is back in that sign across "
                        f"{esc(_win_phrase(b['second']))}" for b in seconds)
        sky.append(f"The second return comes near age 58 to 59: {sec}.")
    themes = " ".join(f"A return in {esc(b['sign'])} works on {esc(b['theme'])}." for b, _ in blocks)

    faqs = [
        (f"When is the Saturn return for someone born in {year}?",
         f"{answer_plain} The table lists every exact pass for {year} births month by month, and the free "
         f"calculator gives yours to the day."),
        (f"What sign is Saturn in for {year} births?",
         (f"Natal Saturn for {year} births is in {meta_signs}. "
          + sign_rule
          + f"It ran from {year_lo.replace('&deg;', '°').replace('&prime;', '′')} on January 1 to "
            f"{year_hi.replace('&deg;', '°').replace('&prime;', '′')} on December 31, computed with the Swiss Ephemeris.")),
        (f"Why do some {year} birthdays get three Saturn return passes?",
         f"Of the 12 mid-month {year} birthdays, {single} get one pass and {triple} get three. Saturn is "
         f"retrograde for about four and a half months of every year, and the three-pass birthdays are the ones "
         f"whose natal degree sits inside a retrograde loop around {_win_phrase(blocks[0][0]['first']) if blocks[0][0]['first'] else 'age 29'}, "
         f"so Saturn crosses it forward, backward, then forward again."),
    ]
    faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs]}, ensure_ascii=False).replace("</", "<\\/")
    faq_html = "\n".join(f'    <div class="qa"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in faqs)

    prev_y, next_y = year - 1, year + 1
    nav_prev = f'<a href="/saturn-return/{prev_y}">&larr; {esc(prev_y)} births</a>' if prev_y >= 1960 else "<span></span>"
    nav_next = f'<a href="/saturn-return/{next_y}">{esc(next_y)} births &rarr;</a>' if next_y <= 2005 else "<span></span>"
    desc = (f"Born in {year}? Natal Saturn in {meta_signs}. Exact first Saturn return passes for every "
            f"{year} birth month, {span_plain}, computed with the Swiss Ephemeris.")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Saturn Return Dates for {esc(year)} Births, by Month &middot; The Twelve Rooms</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://thetwelverooms.com/saturn-return/{year}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{faq_json}</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>Saturn return dates for {esc(year)} births</h1>
  <p class="lede">{answer}</p>

  <div class="card">
    <table class="year-table">
      <thead><tr><th>Born</th><th>Natal Saturn</th><th>First return, exact passes</th><th>Age</th></tr></thead>
      <tbody>
{chr(10).join(trs)}
      </tbody>
    </table>
    <p class="hint" style="margin-top:8px">Each row is computed for a birth on the 15th of that month of {esc(year)}, at noon UT; a {esc(year)} birthday earlier or later in the month moves natal Saturn by up to a degree, which can shift the passes by weeks and, near the edge of a retrograde loop, turn one pass into three. The <a href="/saturn-return-calculator">Saturn return calculator</a> gives yours to the day.</p>
  </div>

  <section class="prose">
    <h2>Saturn in {esc(year)}</h2>
    <p>{' '.join(sky)}</p>
    <h2>What a {esc(year)} return asks</h2>
    <p>{themes} Saturn takes about 29.5 years to circle the zodiac, so the first return is its first homecoming to the degree it held when you were born: the season the life you built in your twenties gets its first honest audit, and the seed of the next chapter is planted.</p>
  </section>

  <section class="faq">
    <h2>Questions about {esc(year)} Saturn returns</h2>
{faq_html}
  </section>

  <nav class="daynav">
    {nav_prev}
    <a href="/saturn-return-calculator">Your exact dates</a>
    {nav_next}
  </nav>

  <div class="cta">
    <h2>The dates are free. The meaning is the reading.</h2>
    <p>The Twelve Rooms Saturn Return Report reads your natal Saturn in full, the room the return lands in, and what this season is here to confirm, honestly and without doom.</p>
    <a href="{shop.etsy_url('saturn', f'saturn-return-{year}')}" rel="noopener">The Saturn Return Report on Etsy</a>
  </div>
  <div id="site-footer">{crawl.FOOTER_HTML}</div>
</main>
<script src="/tools.js"></script>
</body>
</html>"""



class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            order = {"name": "Your chart",
                     "date": o["date"], "time": o.get("time") or None,
                     "tz": o["tz"], "lat": float(o["lat"]), "lon": float(o["lon"]),
                     "place": str(o.get("place", ""))[:80]}
            natal = engines.cf.build_natal(order)[0]
            sat = natal["planets"]["Saturn"]
            born = date.fromisoformat(order["date"])
            sect = natal.get("sect") or None

            returns = sr.build_returns(sat["lon"], born, sect)
            out = {
                "natal_saturn": {"pretty": sat["pretty"], "sign": sat.get("sign"),
                                 "house": sat.get("house"),
                                 "sect_role": sr.sect_role_line(sect or {})},
                "timed": bool(order["time"]),
                "returns": returns,
                "method": sr.METHOD,
            }
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

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
