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
sys.path.insert(0, str(Path(__file__).parent / "_seo"))
import engines  # noqa: E402
import electional  # noqa: E402
import swisseph as swe  # noqa: E402
import crawl  # noqa: E402

SIGN_STYLE = {
    "Aries": "bold and headlong", "Taurus": "steady and sensory",
    "Gemini": "quick and curious", "Cancer": "tender and protective",
    "Leo": "warm and wholehearted", "Virgo": "precise and useful",
    "Libra": "gracious and relational", "Scorpio": "intense and deep",
    "Sagittarius": "restless and searching", "Capricorn": "serious and steady",
    "Aquarius": "cool and original", "Pisces": "dreamy and soft",
}
# Ruler and practical do/avoid guidance, one clear instruction each way.
# These recur every two to three days as the Moon changes sign, which is
# the correct astronomical cadence, not padding: what makes each date page
# unique is this text combined with that date's phase, aspects, ingress,
# and void-of-course windows below.
SIGN_RULER = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "the Moon",
    "Leo": "the Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars and Pluto",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn and Uranus",
    "Pisces": "Jupiter and Neptune",
}
SIGN_PRACTICAL = {
    "Aries": "Good day to start rather than plan further, decisiveness reads as "
             "competence right now. Watch the temper: the quick reaction costs more "
             "than it solves.",
    "Taurus": "Good day to slow down and do the tactile thing you have been putting "
              "off, cooking, a walk, paying a bill. Resist digging in on principle "
              "alone, not every hill needs holding today.",
    "Gemini": "Good day for the conversation, the email, or the research you have "
              "been avoiding, words move easily. Watch scattering across five "
              "threads instead of finishing one.",
    "Cancer": "Good day to tend people and home, a call to family or a meal cooked "
              "from scratch lands well. Watch taking a neutral comment personally, "
              "the skin is thinner than usual.",
    "Leo": "Good day to ask for what you want out loud, warmth is well received "
           "right now. Watch needing an audience for every small win, some things "
           "can just be done.",
    "Virgo": "Good day to fix the one broken system, laundry, budget, inbox, the "
             "effort actually holds. Watch turning care into criticism, especially "
             "of yourself.",
    "Libra": "Good day for the negotiation or the apology, fairness lands and "
             "people meet you halfway. Watch avoiding a needed conflict just to "
             "keep the peace.",
    "Scorpio": "Good day for the hard, honest conversation, depth is available and "
               "worth using. Watch the urge to control an outcome that is not "
               "yours to control.",
    "Sagittarius": "Good day to book the trip, start the course, say the blunt "
                   "true thing. Watch overpromising on time or money before you "
                   "have checked the math.",
    "Capricorn": "Good day to do the unglamorous work that compounds, nobody "
                 "notices today, everyone notices in a year. Watch letting duty "
                 "crowd out actual rest.",
    "Aquarius": "Good day to step back and see the pattern, a little distance "
                "clarifies more than more input would. Watch detaching so far "
                "you miss what someone needed from you.",
    "Pisces": "Good day for rest, art, or anything that asks you to feel rather "
              "than solve. Watch absorbing a mood that was never yours to carry.",
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

# Moon-to-planet aspect language: verb for the aspect, then what it colors
# for each of the six classical planets that voc_intervals already tracks.
# 5 aspects times 6 planets, each hand-written so the day's actual aspect
# set (which varies date to date) reads as real guidance, not a fill-in.
ASPECT_VERB = {
    "conjunction": "meets", "sextile": "opens an easy angle to",
    "square": "squares off with", "trine": "flows easily with",
    "opposition": "stands opposite",
}
ASPECT_PLANET_TEXT = {
    ("conjunction", "Sun"): "blending feeling and will for the day, whatever you decide now lands with extra weight",
    ("conjunction", "Mercury"): "sharpening the line between what you feel and what you say, a good window to speak plainly",
    ("conjunction", "Venus"): "warming the day toward comfort, affection, and small pleasures",
    ("conjunction", "Mars"): "raising the temperature, energy runs hot and quick to act",
    ("conjunction", "Jupiter"): "swelling the mood, appetite and optimism both run large today",
    ("conjunction", "Saturn"): "sobering the day, feelings meet a real limit or an old responsibility",
    ("sextile", "Sun"): "opening an easy window to line up what you want with what you feel, worth the small effort to use it",
    ("sextile", "Mercury"): "making conversation and small decisions come easier than usual",
    ("sextile", "Venus"): "smoothing the social hours, a good stretch for connection or a kindness",
    ("sextile", "Mars"): "giving a low-friction lift to get something moving",
    ("sextile", "Jupiter"): "offering a gentle boost of luck or generosity, easy to miss if you are not looking for it",
    ("sextile", "Saturn"): "supporting steady, practical progress on something that needed discipline",
    ("square", "Sun"): "putting feeling and will at odds, expect a real choice rather than a comfortable one",
    ("square", "Mercury"): "making it easy to say the wrong thing fast, worth a pause before you speak",
    ("square", "Venus"): "straining comfort or budget, a want and a need pulling in different directions",
    ("square", "Mars"): "raising friction and impatience, a good day to move the body before the mood moves you",
    ("square", "Jupiter"): "tempting overreach, the urge to promise or spend more than is wise",
    ("square", "Saturn"): "pressing feeling against duty, something you have been avoiding gets harder to keep avoiding",
    ("trine", "Sun"): "letting feeling and will move together with little resistance, a good day to act on instinct",
    ("trine", "Mercury"): "making honest, easy conversation more available than usual",
    ("trine", "Venus"): "softening the day toward warmth, good for connection, beauty, or rest",
    ("trine", "Mars"): "giving energy a clean, usable outlet",
    ("trine", "Jupiter"): "widening the mood toward ease and generosity, a fortunate undertone",
    ("trine", "Saturn"): "grounding feeling in something durable, a good day to commit to a plan",
    ("opposition", "Sun"): "asking you to balance what you feel against what you are trying to become",
    ("opposition", "Mercury"): "highlighting a gap between what you feel and what is being said, worth naming out loud",
    ("opposition", "Venus"): "putting your own needs across the table from someone else's, a negotiation more than a fight",
    ("opposition", "Mars"): "raising the odds of a clash, better to name the tension than let it simmer",
    ("opposition", "Jupiter"): "tempting a swing between too much caution and too much confidence",
    ("opposition", "Saturn"): "setting feeling against obligation, a day that asks what you owe against what you need",
}


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
    day_asp = [(dt, p, a) for dt, p, a in perfs if day0 <= dt < day1]

    def t(dt):
        return dt.strftime("%-I:%M %p UTC")

    return {"sign": sign, "deg": deg, "phase": phase,
            "ingress": [{"sign": engines.cs.SIGNS[s], "at": t(dt)} for dt, s in day_ing],
            "voc": [{"from": t(a), "to": t(b)} for a, b in day_voc],
            "aspects": [{"planet": p, "aspect": a, "at": t(dt),
                         "new_moon": p == "Sun" and a == "conjunction",
                         "full_moon": p == "Sun" and a == "opposition"}
                        for dt, p, a in day_asp]}


def render(d):
    m = compute(d)
    pretty = d.strftime("%B %-d, %Y")
    iso = d.isoformat()
    # Day-to-day chain, clipped at the indexable window so the walk ends.
    # See api/_seo/crawl.py: unclipped this route reached 73,414 dates.
    prev_d, next_d = d - timedelta(days=1), d + timedelta(days=1)
    daynav = "".join(
        [f'<a href="{h}">&larr; {esc(prev_d.strftime("%b %-d"))}</a>'
         for h in [crawl.chain_href(prev_d, "/moon")] if h]
        + ['<a href="/moon">Today\'s Moon</a>']
        + [f'<a href="{h}">{esc(next_d.strftime("%b %-d"))} &rarr;</a>'
           for h in [crawl.chain_href(next_d, "/moon")] if h]
    )
    robots = crawl.robots_meta(d)
    sign = m["sign"]
    style = SIGN_STYLE.get(sign, "distinct")
    ruler = SIGN_RULER.get(sign, "")
    practical = SIGN_PRACTICAL.get(sign, "")
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

    is_new_moon = any(a["new_moon"] for a in m["aspects"])
    is_full_moon = any(a["full_moon"] for a in m["aspects"])
    lunation_line = ""
    if is_new_moon:
        lunation_line = (f'<p class="moon-mood"><strong>This is the New Moon</strong>, exact in {esc(sign)} '
                          f"today: the Sun and Moon meet in the same sign, the dark of the cycle and the "
                          f"clearest day of the month to set an intention in this sign's {esc(style)} "
                          f"register.</p>")
    elif is_full_moon:
        opp = engines.cs.SIGNS[(engines.cs.SIGNS.index(sign) + 6) % 12] if sign in engines.cs.SIGNS else ""
        lunation_line = (f'<p class="moon-mood"><strong>This is the Full Moon</strong>, exact in {esc(sign)} '
                          f"today, opposite the Sun in {esc(opp)}: whatever began around the New Moon two "
                          f"weeks back comes to a head or comes to light now.</p>")

    asp_items = "".join(
        f'<li>Moon {esc(ASPECT_VERB.get(a["aspect"], a["aspect"]))} {esc(a["planet"])} at {esc(a["at"])}</li>'
        for a in m["aspects"]
    )
    asp_prose = ""
    if m["aspects"]:
        lines = []
        for a in m["aspects"]:
            clause = ASPECT_PLANET_TEXT.get((a["aspect"], a["planet"]), "")
            verb = ASPECT_VERB.get(a["aspect"], a["aspect"])
            if clause:
                lines.append(f"At {esc(a['at'])}, the Moon {esc(verb)} {esc(a['planet'])}, "
                              f"{esc(clause)}.")
        if lines:
            asp_prose = (f"<h2>The Moon's aspects on {esc(pretty)}</h2>"
                         f"<p>{' '.join(lines)}</p>")
    else:
        asp_prose = (f"<h2>The Moon's aspects on {esc(pretty)}</h2>"
                     f"<p>The Moon perfects no major aspect to another planet within the day itself, "
                     f"so {esc(pretty)} runs on sign and phase alone, without a sharp trigger from "
                     f"another planet.</p>")

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
{robots}
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
    {lunation_line}
    <ul class="facts">
      {''.join(f'<li>Enters {esc(i["sign"])} at {esc(i["at"])}</li>' for i in m['ingress'])}
      {voc_line}
      {asp_items}
    </ul>
  </div>

  <section class="prose">
    <h2>What a {esc(sign)} Moon feels like</h2>
    <p>When the Moon moves through {esc(sign)}, the mood of the day tilts {esc(style)}. The Moon is the fastest body in the sky and she sets the emotional weather, so this is the undertone beneath {esc(pretty)}, changing again in a day or two as she moves on.{esc(ing_txt)} {esc(sign)} is ruled by {esc(ruler)}, and that rulership is where the sign's style comes from.</p>
    <p>Her phase is the other half. This is a <strong>{esc(m['phase'].lower())}</strong>: {esc(phase_mean)}. If you are timing something that matters, the rule of thumb is to build on a waxing Moon, release on a waning one, and steer clear of the void-of-course windows above.</p>
    <p>For the void-of-course windows on {esc(pretty)} led up front, with what to do about them, see the <a href="/void-of-course-moon/{iso}">void of course read for this date</a>.</p>
  </section>

  <section class="prose">
    {asp_prose}
  </section>

  <section class="prose">
    <h2>What to do with a {esc(sign)} Moon on {esc(pretty)}</h2>
    <p>{esc(practical)}</p>
  </section>

  <nav class="daynav">{daynav}</nav>

  <div class="cta">
    <h2>Timing something on {esc(d.strftime('%B %-d'))}?</h2>
    <p>Find the exact best window for your city and intention in the free timing finder, or ask The Twelve Rooms for a full reading.</p>
    <a href="/electional" rel="noopener">Open the timing finder</a>
  </div>
  <div id="site-footer">{crawl.FOOTER_HTML}</div>
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
