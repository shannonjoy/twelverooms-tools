#!/usr/bin/env python3
"""Render the sky calendar pages and feeds from bin/sky_data/sky.json.

Every date, time, sign and degree on these pages comes from that file,
which bin/sky_calendar.py computes with the site's own Swiss Ephemeris
engine. Nothing here is typed in by hand except the plain-language copy.

Writes:
  is-mercury-retrograde.html     live yes/no plus every 2026-2028 retrograde
  retrogrades-2027.html          every planet's 2027 retrogrades
  eclipses-2027.html             the five 2027 eclipses
  full-moon-calendar.html        every 2027 Full Moon, with almanac names
  new-moon-calendar.html         every 2027 New Moon
  astrology-calendar.html        the subscribable feed, explained
  calendar/twelve-rooms.ics      rolling feed (from the current month to the end of the data)
  calendar/twelve-rooms-2027.ics the 2027 year on its own
  embed.html                     the Moon widget, with copy-paste code
  embed/moon-today.html          the widget itself (noindex)

Usage: python3 bin/sky_calendar.py && python3 bin/gen_sky_pages.py [--asof YYYY-MM-DD]
It finishes by running bin/apply_og_tags.py, which gives the new pages the
shared share-card block (it changes no other page unless that page drifted).
"""
import html
import json
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_seo"))
sys.path.insert(0, str(ROOT / "bin"))
import crawl  # noqa: E402
import sky_calendar as skc  # noqa: E402

SITE = "https://thetwelverooms.com"
DATA = json.loads((ROOT / "bin" / "sky_data" / "sky.json").read_text(encoding="utf-8"))
ASOF = date.today()
if "--asof" in sys.argv:
    ASOF = date.fromisoformat(sys.argv[sys.argv.index("--asof") + 1])
YEAR = 2027
ETSY_YEAR_AHEAD = "https://www.etsy.com/listing/4539692523"

WORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
COUNTRY = {"IS": "Iceland", "BR": "Brazil", "EG": "Egypt", "AU": "Australia",
           "ES": "Spain", "MA": "Morocco", "SA": "Saudi Arabia", "LY": "Libya"}

e = html.escape


# ---------- small formatting helpers ----------

def d_of(iso_utc):
    return datetime.strptime(iso_utc, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)


def iso_z(iso_utc):
    return d_of(iso_utc).strftime("%Y-%m-%dT%H:%M:00Z")


def central(ev):
    """'Sat Feb 6, 2027' and '9:56 AM CST' from a stamped event."""
    lab = ev["central_label"]
    day, _, rest = lab.partition(", 20")
    year = "20" + rest[:2]
    clock = rest[4:]
    return f"{day}, {year}", clock


def short_day(ev):
    c = datetime.fromisoformat(ev["central"][:16])
    return c.strftime("%b %-d")


def long_day(ev):
    c = datetime.fromisoformat(ev["central"][:16])
    return c.strftime("%B %-d, %Y")


def utc_clock(ev):
    """UTC time, with the UTC date when it differs from the Central date."""
    u = d_of(ev["utc"])
    if u.date().isoformat() != ev["central_date"]:
        return u.strftime("%b %-d, %H:%M UTC")
    return u.strftime("%H:%M UTC")


def deg_label(p):
    return f"{p['deg']}&deg;{p['min']:02d}&prime; {p['sign']}"


def deg_text(p):
    return f"{p['deg']}\u00b0{p['min']:02d}\u2032 {p['sign']}"


def year_of(ev):
    return int(ev["central_date"][:4])


def etsy(campaign):
    return (f"{ETSY_YEAR_AHEAD}?utm_source=thetwelverooms&amp;utm_medium=referral"
            f"&amp;utm_campaign={campaign}")


def jsonld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "\n</script>")


def faq_schema(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in qas]}


def faq_html(qas):
    rows = "\n".join(f'    <div class="qa"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in qas)
    return f'  <section class="faq">\n    <h2>Common questions</h2>\n{rows}\n  </section>'


def item_list(name, url, items):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name, "url": url,
            "numberOfItems": len(items),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "description": d}
                                for i, (n, d) in enumerate(items)]}


def page(slug, title, desc, body, schema=(), robots="", extra_head="", scripts=""):
    assert len(title) <= 62, (slug, len(title), title)
    assert 70 <= len(desc) <= 175, (slug, len(desc), desc)
    canon = f"{SITE}/{slug}"
    head = [
        "<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(desc)}">',
    ]
    if robots:
        head.append(f'<meta name="robots" content="{robots}">')
    head += [f'<link rel="canonical" href="{canon}">',
             '<link rel="stylesheet" href="/tools.css">',
             '<link rel="stylesheet" href="/sky.css">',
             '<link rel="icon" href="/favicon.svg">']
    head += [jsonld(s) for s in schema]
    if extra_head:
        head.append(extra_head)
    head.append("</head>")
    doc = "\n".join(head) + f"""
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div id="masthead"></div>
<main class="wrap" id="main-content" tabindex="-1">
{body}

  <div id="site-footer">{crawl.FOOTER_HTML}</div>
</main>
<script src="/tools.js"></script>
<script src="/sky.js"></script>
{scripts}</body>
</html>
"""
    (ROOT / f"{slug}.html").write_text(doc, encoding="utf-8")
    return slug


def related(links):
    items = " &middot; ".join(f'<a href="{h}">{e(t)}</a>' for h, t in links)
    return f'  <p class="hint" style="margin:14px 0 4px">Also on the sky calendar: {items}</p>'


SKY_LINKS = [("/is-mercury-retrograde", "Is Mercury retrograde right now?"),
             ("/retrogrades-2027", "Retrogrades 2027"),
             ("/eclipses-2027", "Eclipses 2027"),
             ("/full-moon-calendar", "Full Moon calendar"),
             ("/new-moon-calendar", "New Moon calendar"),
             ("/astrology-calendar", "Add it all to your calendar")]


def others(slug):
    return related([(h, t) for h, t in SKY_LINKS if h != "/" + slug])


# ---------- data views ----------

MERC = DATA["retrogrades"]["Mercury"]
LUNES = DATA["lunations"]
ECL = DATA["eclipses"]


def or_phrase(signs):
    return " or ".join(signs) if len(signs) <= 2 else ", ".join(signs[:-1]) + " or " + signs[-1]


def signs_phrase(signs):
    return " and ".join(signs) if len(signs) <= 2 else ", ".join(signs[:-1]) + " and " + signs[-1]


def merc_current(asof):
    """The retrograde whose post-shadow has not ended on `asof` (UTC noon)."""
    t = datetime(asof.year, asof.month, asof.day, 12, tzinfo=timezone.utc)
    for r in MERC:
        if d_of(r["shadow_ends"]["utc"]) > t:
            return r, t
    return None, t


def merc_state(asof):
    r, t = merc_current(asof)
    if r is None:
        return "No", None, "direct"
    if t < d_of(r["shadow_begins"]["utc"]):
        return "No", r, "direct"
    if t < d_of(r["station_retrograde"]["utc"]):
        return "Not yet", r, "pre"
    if t < d_of(r["station_direct"]["utc"]):
        return "Yes", r, "rx"
    return "No", r, "post"


# ---------- 1. Is Mercury retrograde right now? ----------

def gen_is_mercury():
    slug = "is-mercury-retrograde"
    verdict, cur, phase = merc_state(ASOF)
    rx, dr = cur["station_retrograde"], cur["station_direct"]
    sb, se = cur["shadow_begins"], cur["shadow_ends"]
    asof_label = ASOF.strftime("%B %-d, %Y")
    if phase == "pre":
        say = (f"Mercury is in its pre-shadow. It stations retrograde <strong>{long_day(rx)}</strong> "
               f"at {deg_label(rx)} and turns direct {long_day(dr)}.")
    elif phase == "rx":
        say = (f"Mercury is retrograde in {signs_phrase(cur['signs'])}. It turns direct "
               f"<strong>{long_day(dr)}</strong> at {deg_label(dr)}.")
    elif phase == "post":
        say = (f"Mercury turned direct {long_day(dr)} and is in its post-shadow until "
               f"<strong>{long_day(se)}</strong>.")
    else:
        say = (f"Mercury is moving direct. The next retrograde runs <strong>{long_day(rx)} to "
               f"{long_day(dr)}</strong>.")
    periods = [{"retrograde": iso_z(r["station_retrograde"]["utc"]),
                "direct": iso_z(r["station_direct"]["utc"]),
                "shadow_begins": iso_z(r["shadow_begins"]["utc"]),
                "shadow_ends": iso_z(r["shadow_ends"]["utc"]),
                "signs": signs_phrase(r["signs"])} for r in MERC]

    def cell(label, ev, extra, ph):
        day, clock = central(ev)
        now_cls = ' class="now"' if ph == phase else ""
        return (f'<div data-phase="{ph}"{now_cls}><b>{label}</b>'
                f'<span>{day}</span><small>{clock} &middot; {utc_clock(ev)}</small>'
                f'<small>{extra}</small></div>')

    phase_row = "".join([
        cell("Shadow begins", sb, f"Mercury reaches {deg_label(dr)}", "pre"),
        cell("Retrograde", rx, f"stations at {deg_label(rx)}", "rx"),
        cell("Direct", dr, f"stations at {deg_label(dr)}", "post"),
        cell("Shadow ends", se, f"clears {deg_label(rx)}", "direct"),
    ])

    rows = []
    for r in MERC:
        a, b = r["station_retrograde"], r["station_direct"]
        rows.append(
            f'      <tr data-utc="{iso_z(a["utc"])}" data-end="{iso_z(r["shadow_ends"]["utc"])}">'
            f'<td><strong>{short_day(a)} to {short_day(b)}, {year_of(b)}</strong>'
            f'<small>{r["days"]} days</small></td>'
            f'<td>{deg_label(a)}<small>back to {deg_label(b)}</small></td>'
            f'<td>{short_day(r["shadow_begins"])} to {short_day(r["shadow_ends"])}</td></tr>')
    per_year = {}
    for r in MERC:
        per_year.setdefault(year_of(r["station_retrograde"]), []).append(r)
    lens = [r["days"] for r in MERC]

    nxt = next(r for r in MERC if d_of(r["station_retrograde"]["utc"]).date() > ASOF) \
        if phase in ("rx", "post") else cur
    qas = [
        ("When is the next Mercury retrograde?",
         f"Mercury next stations retrograde on {long_day(nxt['station_retrograde'])} at "
         f"{deg_text(nxt['station_retrograde'])} and turns direct on {long_day(nxt['station_direct'])} "
         f"at {deg_text(nxt['station_direct'])} (US Central time). The shadow runs "
         f"{long_day(nxt['shadow_begins'])} to {long_day(nxt['shadow_ends'])}."),
        ("How many times is Mercury retrograde in 2027?",
         f"Three times: " + "; ".join(
             f"{long_day(r['station_retrograde'])} to {long_day(r['station_direct'])} in "
             f"{signs_phrase(r['signs'])}" for r in per_year[2027]) + "."),
        ("How long does Mercury retrograde last?",
         f"Between {min(lens)} and {max(lens)} days for every retrograde from 2026 to 2028, "
         f"station to station. With the shadow on either side, the whole cycle runs about two months."),
        ("What is the Mercury retrograde shadow?",
         "The pre-shadow begins when Mercury first reaches the degree where it will later turn "
         "direct, and the post-shadow ends when it clears the degree where it turned retrograde. "
         "Inside the shadow Mercury covers the same stretch of sky three times."),
        ("Is it Mercury retrograde in my timezone too?",
         "Yes. A station happens at one moment for the whole Earth. Only the clock reading changes, "
         "so near midnight the date can differ by one day between, say, Chicago and London. This page "
         "shows US Central time and UTC, and the live answer above uses your own clock."),
    ]
    items = [(f"Mercury retrograde {long_day(r['station_retrograde'])} to {long_day(r['station_direct'])}",
              f"Stations retrograde at {deg_text(r['station_retrograde'])}, direct at "
              f"{deg_text(r['station_direct'])}; shadow {long_day(r['shadow_begins'])} to "
              f"{long_day(r['shadow_ends'])}.") for r in MERC]

    body = f"""  <h1>Is Mercury retrograde right now?</h1>
  <div class="answer" data-mercury="merc-periods" aria-live="polite">
    <div class="kicker">Mercury today</div>
    <div class="verdict">{verdict}</div>
    <p class="say">{say}</p>
    <p class="asof">As of {asof_label}. This answer updates with your own clock when the page loads.</p>
  </div>
  <p class="lede">The short answer, then the dates. Every station, shadow and degree below is computed with the Swiss Ephemeris, shown in US Central time with UTC beside it. For what the season means and what to do with it, read <a href="/mercury-retrograde">Mercury retrograde, explained</a>.</p>

  <div class="card">
    <h2 style="margin-top:0">{"This" if phase in ("pre", "rx", "post") else "The next"} retrograde, start to finish</h2>
    <div class="phase-row">{phase_row}</div>
    <p class="hint" style="margin-top:10px">A retrograde has four marks: the shadow opens, Mercury stations retrograde, it stations direct, and the shadow closes. The highlighted box is where Mercury is today.</p>
  </div>

  <section class="prose">
    <h2>Every Mercury retrograde, 2026 to 2028</h2>
    <p>Mercury turns retrograde three times a year, for about three weeks each time. The past ones stay on the list for reference; the next one is highlighted.</p>
  </section>
  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Retrograde</th><th>Stations</th><th>Shadow</th></tr>
{chr(10).join(rows)}
    </table>
    <p class="hint" style="margin-top:8px">Dates in US Central time. Want them in your calendar? <a href="/astrology-calendar">Subscribe to the free sky calendar</a>.</p>
  </div>

  <section class="prose">
    <h2>What each mark means</h2>
    <p><strong>Pre-shadow.</strong> Mercury is still moving forward, but it is walking ground it will soon retrace. Themes that will matter during the retrograde often show their first edge here, so this is the time to back up, finish, and get signatures settled.</p>
    <p><strong>Retrograde.</strong> From Earth, Mercury appears to stop and move backward. It is the season for anything with the prefix re: revise, review, reconnect, repair. Beginnings you want to run cleanly go better after it.</p>
    <p><strong>Post-shadow.</strong> Mercury is direct again and recrossing the same stretch of sky for the third time. Plans firm up, delays clear, and what you revised gets its second chance.</p>
  </section>

  <div class="cta">
    <h2>Your year, read from your own chart</h2>
    <p>Mercury's dates are the same for everyone. The Year-Ahead Reading reads how the coming twelve months move through your own chart, with the dates worth circling.</p>
    <a href="{etsy(slug)}" rel="noopener">The Year-Ahead Reading on Etsy</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    data_tag = ('<script type="application/json" id="merc-periods">'
                + json.dumps(periods, separators=(",", ":")) + "</script>\n")
    return page(slug, "Is Mercury Retrograde Right Now? Today's Answer",
                "Is Mercury retrograde today? A live yes or no, the current or next retrograde with "
                "its shadow dates, and every Mercury retrograde from 2026 to 2028.",
                body, [faq_schema(qas), item_list("Mercury retrograde dates 2026 to 2028",
                                                  f"{SITE}/{slug}", items)],
                scripts=data_tag)


# ---------- 2. Retrogrades 2027 ----------

PLANET_NOTE = {
    "Mercury": "Words, plans, contracts and travel turn to review. Revise and reconnect; start the clean beginnings after.",
    "Venus": "Love, money and what you value come back for a second look.",
    "Mars": "Drive turns inward. Effort pays when it goes into finishing and repairing rather than pushing new fronts open.",
    "Jupiter": "Growth turns inward: belief, study and generosity deepen before they expand again.",
    "Saturn": "Commitments and structures get their inspection. What is load-bearing stays; what is not gets rebuilt.",
    "Uranus": "Change works from the inside first. Freedom you have been circling gets clearer in private before it shows.",
    "Neptune": "The fog thins, and ideals and illusions get easier to tell apart.",
    "Pluto": "A slow, deep inventory of power: what you hold, what holds you, and what you are ready to let go.",
}


def rx_overlap(r, year):
    a = d_of(r["station_retrograde"]["utc"]).date()
    b = d_of(r["station_direct"]["utc"]).date()
    return a.year <= year <= b.year


def daily_rx_counts(year):
    """Planets retrograde at 12:00 UTC on each day of `year`, from the engine."""
    out = {}
    d = date(year, 1, 1)
    while d.year == year:
        jd = skc.jd_of(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))
        out[d] = [p for p in skc.PLANETS if skc.speed(jd, p) < 0]
        d += timedelta(days=1)
    return out


def runs(counts, pred):
    """Longest unbroken run of days where pred(list) holds: (start, end, n)."""
    best, start = None, None
    days_ = sorted(counts)
    for i, d in enumerate(days_):
        if pred(counts[d]):
            start = start or d
            end = d
            if best is None or (end - start).days > (best[1] - best[0]).days:
                best = (start, end)
        else:
            start = None
    return best


def gen_retrogrades():
    slug = f"retrogrades-{YEAR}"
    counts = daily_rx_counts(YEAR)
    peak = max(len(v) for v in counts.values())
    peak_days = sorted(d for d, v in counts.items() if len(v) == peak)
    peak_run = runs(counts, lambda v: len(v) == peak)
    peak_planets = counts[peak_run[0]]
    low = min(len(v) for v in counts.values())
    low_days = sum(1 for v in counts.values() if len(v) == low)
    all_direct = sum(1 for v in counts.values() if not v)

    rows, items, sections = [], [], []
    for p in skc.PLANETS:
        rs = [r for r in DATA["retrogrades"][p] if rx_overlap(r, YEAR)]
        if not rs:
            nxt = next((r for r in DATA["retrogrades"][p]
                        if d_of(r["station_retrograde"]["utc"]).year > YEAR), None)
            line = (f"No retrograde in {YEAR}. The next runs {long_day(nxt['station_retrograde'])} to "
                    f"{long_day(nxt['station_direct'])} in {signs_phrase(nxt['signs'])}.") if nxt else \
                f"No retrograde in {YEAR}."
            rows.append(f'      <tr><td><strong>{p}</strong></td><td colspan="3">{e(line)}</td></tr>')
            sections.append(f"    <p><strong>{p}:</strong> {e(line)} {PLANET_NOTE[p]}</p>")
            continue
        texts = []
        for r in rs:
            a, b = r["station_retrograde"], r["station_direct"]
            shadow = ""
            if r.get("shadow_begins"):
                shadow = (f'<small>shadow {short_day(r["shadow_begins"])}, {year_of(r["shadow_begins"])} '
                          f'to {short_day(r["shadow_ends"])}, {year_of(r["shadow_ends"])}</small>')
            rows.append(
                f'      <tr data-utc="{iso_z(a["utc"])}" data-end="{iso_z(b["utc"])}"><td><strong>{p}</strong></td>'
                f'<td>{short_day(a)}, {year_of(a)}<small>{deg_label(a)}</small></td>'
                f'<td>{short_day(b)}, {year_of(b)}<small>{deg_label(b)}</small></td>'
                f'<td>{r["days"]} days{shadow}</td></tr>')
            items.append((f"{p} retrograde {long_day(a)} to {long_day(b)}",
                          f"Stations retrograde at {deg_text(a)} and direct at {deg_text(b)}, "
                          f"in {signs_phrase(r['signs'])}."))
            texts.append(f"{long_day(a)} to {long_day(b)} ({deg_text(a)} back to {deg_text(b)})")
        sections.append(f"    <p><strong>{p}:</strong> {e('; '.join(texts))}. {PLANET_NOTE[p]}</p>")

    mars = [r for r in DATA["retrogrades"]["Mars"] if rx_overlap(r, YEAR)]
    n_merc = sum(1 for r in DATA["retrogrades"]["Mercury"] if d_of(r["station_retrograde"]["utc"]).year == YEAR)
    mars_line = ""
    if mars:
        mars_line = (f" Mars's run from {d_of(mars[0]['station_retrograde']['utc']).strftime('%B')} to "
                     f"{d_of(mars[0]['station_direct']['utc']).strftime('%B')} is the rarest of the year: "
                     f"Mars turns back only about once every two years.")
    with_rx = [p for p in skc.PLANETS if any(rx_overlap(r, YEAR) for r in DATA["retrogrades"][p])]
    without = [p for p in skc.PLANETS if p not in with_rx]
    count_word = {8: "All eight", 7: "Seven", 6: "Six", 5: "Five"}.get(len(with_rx), str(len(with_rx)))
    lede_rx = (f"{count_word} of the eight planets from Mercury to Pluto turn retrograde in {YEAR}"
               + (f"; {signs_phrase(without)} {'stays' if len(without) == 1 else 'stay'} direct all year." if without else "."))
    qas = [
        (f"Which planets are retrograde in {YEAR}?",
         "; ".join(f"{p} {', '.join(long_day(r['station_retrograde']) + ' to ' + long_day(r['station_direct']) for r in DATA['retrogrades'][p] if rx_overlap(r, YEAR))}"
                   for p in skc.PLANETS if any(rx_overlap(r, YEAR) for r in DATA["retrogrades"][p]))
         + f". Venus does not turn retrograde in {YEAR}."),
        (f"When is the most planets retrograde at once in {YEAR}?",
         f"{WORD.get(peak, str(peak))} planets are retrograde together from {peak_run[0].strftime('%B %-d')} to "
         f"{peak_run[1].strftime('%B %-d')}, {YEAR}: {signs_phrase(peak_planets)}."),
        (f"Is Mars retrograde in {YEAR}?",
         (f"Yes, once: Mars stations retrograde on {long_day(mars[0]['station_retrograde'])} at "
          f"{deg_text(mars[0]['station_retrograde'])} and turns direct on "
          f"{long_day(mars[0]['station_direct'])} at {deg_text(mars[0]['station_direct'])}.")
         if mars else f"No, Mars does not turn retrograde in {YEAR}."),
        ("Is a retrograde bad?",
         "No. A retrograde is a review season for whatever the planet governs. It favors returning, "
         "revising and finishing, and asks you to time clean new starts around it where you can."),
    ]
    body = f"""  <h1>Retrogrades {YEAR}: every planet, every date</h1>
  <p class="lede">{lede_rx} Here is each station, the degree it happens at, and how long it lasts, computed with the Swiss Ephemeris in US Central time.</p>

  <div class="highlight"><strong>The busiest stretch:</strong> {WORD.get(peak, str(peak))} planets are retrograde at once from {peak_run[0].strftime('%B %-d')} to {peak_run[1].strftime('%B %-d')} ({e(signs_phrase(peak_planets))}). {f"On {all_direct} days of {YEAR} every planet is direct." if all_direct else f"At least one planet is retrograde on every day of {YEAR}."}</div>

  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Planet</th><th>Turns retrograde</th><th>Turns direct</th><th>Length</th></tr>
{chr(10).join(rows)}
    </table>
    <p class="hint" style="margin-top:8px">Retrogrades that began in late 2026 or run into 2028 are included where they touch {YEAR}. Dates in US Central time. For Mercury's live status, see <a href="/is-mercury-retrograde">is Mercury retrograde right now</a>; for Venus, <a href="/venus-retrograde">Venus retrograde</a>.</p>
  </div>

  <section class="prose">
    <h2>What to know about each one</h2>
{chr(10).join(sections)}
    <h2>How to use a retrograde year</h2>
    <p>A retrograde is the sky's way of handing you a second draft. The planet is not broken and nothing is cursed; the work simply turns from opening new ground to tending what is already yours. Mercury's {WORD.get(n_merc, str(n_merc)).lower()} seasons are the ones most people feel in daily life.{mars_line} The slow outer planets spend months retrograde every year, so their stations matter most when they touch a planet in your own chart.</p>
  </section>

  <div class="cta">
    <h2>Which of these touch your chart?</h2>
    <p>The dates are the same for everyone; what they stir is personal. The Year-Ahead Reading reads {YEAR} through your own chart, with the dates worth circling.</p>
    <a href="{etsy(slug)}" rel="noopener">The Year-Ahead Reading on Etsy</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    return page(slug, f"Retrogrades {YEAR}: Every Planet's Dates and Signs",
                f"Every planetary retrograde in {YEAR}, computed with the Swiss Ephemeris: Mercury, "
                f"Mars, Jupiter, Saturn, Uranus, Neptune and Pluto, with dates, degrees and shadows.",
                body, [faq_schema(qas), item_list(f"Planetary retrogrades {YEAR}", f"{SITE}/{slug}", items)])


# ---------- 3. Eclipses 2027 ----------

TYPE_NOTE = {
    ("solar", "total"): "The Moon covers the Sun completely along a narrow path; the sky darkens to deep twilight.",
    ("solar", "annular"): "The Moon is too far from Earth to cover the Sun, leaving a ring of sunlight around it.",
    ("solar", "hybrid"): "Annular along part of its path and total along the rest.",
    ("solar", "partial"): "The Moon covers only part of the Sun from anywhere on Earth.",
    ("lunar", "total"): "The whole Moon passes through Earth's dark inner shadow and often turns copper-red.",
    ("lunar", "partial"): "Part of the Moon passes through Earth's dark inner shadow.",
    ("lunar", "penumbral"): "The Moon passes only through Earth's faint outer shadow; the dimming is subtle to the eye.",
}


def degree_window(p, orb=5):
    lon = p["lon"]
    lo, hi = skc.pos((lon - orb) % 360), skc.pos((lon + orb) % 360)
    return f"{lo['deg']}&deg; {lo['sign']} to {hi['deg']}&deg; {hi['sign']}" if lo["sign"] != hi["sign"] \
        else f"{lo['deg']}&deg; to {hi['deg']}&deg; {lo['sign']}"


def square_signs(sign):
    i = SIGNS.index(sign)
    return [SIGNS[(i + 3) % 12], SIGNS[(i + 6) % 12], SIGNS[(i + 9) % 12]]


def gen_eclipses():
    slug = f"eclipses-{YEAR}"
    ys = [x for x in ECL if year_of(x) == YEAR]
    cards, items, rows = [], [], []
    for x in ys:
        day, clock = central(x)
        kind = f"{x['type'].capitalize()} {x['kind']} eclipse"
        geo = ""
        if x["kind"] == "solar":
            g = x["greatest_at"]
            lat = f"{abs(g['lat'])}&deg;{'N' if g['lat'] >= 0 else 'S'}"
            lon = f"{abs(g['lon'])}&deg;{'E' if g['lon'] >= 0 else 'W'}"
            near = ""
            if g.get("near"):
                n = g["near"]
                near = f", about {n['km']} km from {e(n['name'])}, {COUNTRY.get(n['country'], n['country'])}"
            dur = ""
            if x.get("central_seconds"):
                m, s = divmod(x["central_seconds"], 60)
                word = "totality" if x["type"] == "total" else "the ring of fire"
                dur = f" At that spot {word} lasts {m} min {s} s."
            geo = (f"<p>Greatest eclipse falls at {lat}, {lon}{near}.{dur} "
                   f"Magnitude {x['magnitude']}.</p>")
        else:
            if x["type"] == "penumbral":
                mag = f"Penumbral magnitude {x['penumbral_magnitude']}."
                if x["penumbral_magnitude"] < 0.1:
                    mag += " The Moon barely grazes the outer shadow, so no dimming will be visible."
            else:
                mag = f"Umbral magnitude {x['magnitude']}."
            if "barely" not in mag:
                mag += " A lunar eclipse can be seen from wherever the Moon is above the horizon at the time."
            geo = f"<p>{mag}</p>"
        others3 = square_signs(x["sign"])
        cards.append(f"""  <div class="card">
    <h2 style="margin-top:0">{day}: {kind} in {x['sign']}</h2>
    <p><strong>{clock}</strong> ({utc_clock(x)}) at {deg_label(x)}. {TYPE_NOTE[(x['kind'], x['type'])]}</p>
    {geo}
    <p class="hint">Most felt if you have a planet or angle from {degree_window(x)}, or at the same degrees of {', '.join(others3[:2])} or {others3[2]}.</p>
  </div>""")
        items.append((f"{kind} {long_day(x)}", f"At {deg_text(x)}; peak {x['utc_label']}."))
        rows.append(f'      <tr data-utc="{iso_z(x["utc"])}"><td>{short_day(x)}</td><td>{kind}</td>'
                    f'<td>{deg_label(x)}</td></tr>')

    seasons = []
    for grp in ([x for x in ys if x["central_date"] < f"{YEAR}-06-01"],
                [x for x in ys if x["central_date"] >= f"{YEAR}-06-01"]):
        if grp:
            seasons.append(f"{long_day(grp[0]).rsplit(',', 1)[0]} to {long_day(grp[-1])}")
    node = ys[0]["node"]["sign"]
    south = SIGNS[(SIGNS.index(node) + 6) % 12]
    later = [x for x in ECL if year_of(x) > YEAR]
    later_rows = "\n".join(
        f'      <tr><td>{short_day(x)}, {year_of(x)}</td><td>{x["type"].capitalize()} {x["kind"]}</td>'
        f'<td>{deg_label(x)}</td></tr>' for x in later)
    total = next((x for x in ys if x["kind"] == "solar" and x["type"] == "total"), None)
    headline = ""
    if total and total.get("central_seconds"):
        m_, s_ = divmod(total["central_seconds"], 60)
        headline = (f"The headline is the total solar eclipse of {long_day(total)}, with totality "
                    f"lasting up to {m_} minutes {s_} seconds.")
    neighbors = ""
    axis = {ys[0]["node"]["sign"], SIGNS[(SIGNS.index(ys[0]["node"]["sign"]) + 6) % 12]}
    off_axis = [x["sign"] for x in ys if x["sign"] not in axis]
    if off_axis and all(any(abs((SIGNS.index(sg) - SIGNS.index(a)) % 12) in (1, 11) for a in axis)
                        for sg in off_axis):
        neighbors = f", with the rest in the signs beside them ({or_phrase(sorted(set(off_axis), key=SIGNS.index)).replace(' or ', ' and ')})"
    touched = []
    for x in ys:
        if x["sign"] not in touched:
            touched.append(x["sign"])
    qas = [
        (f"How many eclipses are there in {YEAR}?",
         f"{len(ys)}: " + "; ".join(f"{long_day(x)}, {x['type']} {x['kind']} in {x['sign']}" for x in ys) + "."),
        (f"When are eclipse seasons in {YEAR}?",
         f"Two: {seasons[0]}, and {seasons[1]}. The lunar nodes sit on the {south}-{node} axis all year, "
         f"so the eclipses fall mostly in those signs and their neighbors."),
    ]
    if total:
        m, s = divmod(total.get("central_seconds", 0), 60)
        qas.append((f"When is the total solar eclipse in {YEAR}?",
                    f"{long_day(total)}, at {deg_text(total)}. Greatest eclipse is at "
                    f"{total['utc_label']}, with totality lasting up to {m} minutes {s} seconds."))
    qas.append(("Are eclipses bad luck?",
                "No. In astrology an eclipse marks a turning point: a door that opens or closes faster than "
                "usual. They ask for attention, not fear, and they matter most where they touch your own chart."))
    body = f"""  <h1>Eclipses {YEAR}: dates, times and signs</h1>
  <p class="lede">There are {len(ys)} eclipses in {YEAR}, in two seasons: {seasons[0]}, and {seasons[1]}. {headline} Every time, degree and magnitude here is computed with the Swiss Ephemeris; times are US Central with UTC beside them.</p>

  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Date</th><th>Eclipse</th><th>Degree</th></tr>
{chr(10).join(rows)}
    </table>
  </div>

{chr(10).join(cards)}

  <section class="prose">
    <h2>What the {YEAR} eclipses touch</h2>
    <p>Eclipses follow the Moon's nodes, and in {YEAR} the North Node travels through {node} with the South Node in {south}. That is why this year's eclipses gather around {node} and {south}{neighbors}. If your Sun, Moon, rising sign or another personal planet sits in {or_phrase(touched)}, near the degrees listed above, the year asks something of you: eclipses tend to move things along faster than ordinary New and Full Moons, closing what has run its course and opening what is ready.</p>
    <p>The traditional advice is simple. Notice what arrives or ends within a few weeks of an eclipse, and give big decisions a little room on either side. Eclipses are turning points, not verdicts; the story stays yours.</p>
    <h2>Looking ahead</h2>
  </section>
  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Date</th><th>Eclipse</th><th>Degree</th></tr>
{later_rows}
    </table>
    <p class="hint" style="margin-top:8px">Every eclipse is also in the <a href="/full-moon-calendar">Full Moon</a> and <a href="/new-moon-calendar">New Moon</a> calendars, and in the <a href="/astrology-calendar">subscribable sky calendar</a>.</p>
  </div>

  <div class="cta">
    <h2>Where does {YEAR}'s eclipse axis fall in your chart?</h2>
    <p>The Year-Ahead Reading finds the houses these eclipses move through in your own chart, and the dates that matter most for you.</p>
    <a href="{etsy(slug)}" rel="noopener">The Year-Ahead Reading on Etsy</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    return page(slug, f"Eclipses {YEAR}: Dates, Times, Signs and Types",
                f"All {len(ys)} eclipses of {YEAR}, computed with the Swiss Ephemeris: exact times, "
                f"signs and degrees, including the {long_day(total) if total else ''} total solar eclipse.",
                body, [faq_schema(qas), item_list(f"Eclipses {YEAR}", f"{SITE}/{slug}", items)])


# ---------- 4. Full and New Moon calendars ----------

NEW_MOON_NOTE = {
    "Aries": "begin boldly; the first step is the point",
    "Taurus": "plant something you mean to keep",
    "Gemini": "start the conversation, the class, the draft",
    "Cancer": "tend home and the people who make it",
    "Leo": "begin the thing you would be proud to be seen making",
    "Virgo": "set up the routine that makes the rest possible",
    "Libra": "open a partnership or mend one",
    "Scorpio": "commit to the depth, or let go of the surface",
    "Sagittarius": "set the far goal and buy the ticket",
    "Capricorn": "lay the first stone of a long build",
    "Aquarius": "join the circle, or start one",
    "Pisces": "rest, dream, and let the next chapter find you",
}


def lunation_rows(kind, year):
    rows = []
    for x in LUNES:
        if x["kind"] != kind or year_of(x) != year:
            continue
        day, clock = central(x)
        mark = f' <span class="eclipse-mark">{e(x["eclipse"])}</span>' if x.get("eclipse") else ""
        blue = ' <span class="eclipse-mark">Blue Moon</span>' if x.get("blue_moon") else ""
        name = f'<td>{e(x.get("name", ""))}{blue}</td>' if kind == "full" else \
            f'<td>{NEW_MOON_NOTE[x["sign"]].capitalize()}</td>'
        weekday = datetime.fromisoformat(x["central"][:16]).strftime("%A")
        rows.append(f'      <tr data-utc="{iso_z(x["utc"])}"><td><strong>{short_day(x)}</strong>'
                    f'<small>{weekday}</small></td><td>{clock}<small>{utc_clock(x)}</small></td>'
                    f'<td>{deg_label(x)}{mark}</td>{name}</tr>')
    return rows


def compact(kind, year):
    xs = [x for x in LUNES if x["kind"] == kind and year_of(x) == year]
    return " &middot; ".join(f"{short_day(x)} ({x['sign']})" for x in xs)


def upcoming(kind, asof, n=2):
    return [x for x in LUNES if x["kind"] == kind and date.fromisoformat(x["central_date"]) >= asof][:n]


def gen_full_moons():
    slug = "full-moon-calendar"
    xs = [x for x in LUNES if x["kind"] == "full" and year_of(x) == YEAR]
    ecl = [x for x in xs if x.get("eclipse")]
    rest_2026 = [x for x in LUNES if x["kind"] == "full" and year_of(x) == YEAR - 1
                 and date.fromisoformat(x["central_date"]) >= ASOF]
    harvest = next(x for x in xs if x.get("name") == "Harvest Moon")
    blue = [x for x in LUNES if x.get("blue_moon")]
    qas = [
        (f"How many full moons are in {YEAR}?",
         f"{len(xs)}, from the {xs[0]['name']} on {long_day(xs[0])} to the {xs[-1]['name']} on {long_day(xs[-1])}."),
        (f"What are the full moon names for {YEAR}?",
         "; ".join(f"{datetime.fromisoformat(x['central'][:16]).strftime('%B')}: {x['name']} in {x['sign']}" for x in xs) + "."),
        (f"When is the Harvest Moon in {YEAR}?",
         f"{long_day(harvest)}, in {harvest['sign']}. The Harvest Moon is the Full Moon closest to the "
         f"September equinox, and the Hunter's Moon is the one after it."),
        (f"Are there lunar eclipses at the full moons of {YEAR}?",
         f"{len(ecl)} of them: " + "; ".join(f"{long_day(x)} ({x['eclipse']} in {x['sign']})" for x in ecl) + "."),
        ("Is there a Blue Moon soon?",
         ("The next calendar Blue Moon, a second Full Moon in one month, falls on "
          + "; ".join(f"{long_day(x)} in {x['sign']}" for x in blue if date.fromisoformat(x['central_date']) >= ASOF)
          + " (US Central time).") if any(date.fromisoformat(x['central_date']) >= ASOF for x in blue)
         else f"Not between now and the end of {DATA['to_year']}."),
    ]
    rest = ""
    if rest_2026:
        rest = (f'  <div class="highlight"><strong>Still to come in {YEAR - 1}:</strong> '
                + " &middot; ".join(f"{long_day(x)}, {x['name']} in {x['sign']} at {central(x)[1]}" for x in rest_2026)
                + ".</div>")
    items = [(f"{x['name']} {long_day(x)}", f"Full Moon at {deg_text(x)}, {x['central_label']}"
              + (f"; {x['eclipse']}" if x.get("eclipse") else "")) for x in xs]
    body = f"""  <h1>Full Moon calendar {YEAR}</h1>
  <p class="lede">There are {len(xs)} Full Moons in {YEAR}. Each one below has its exact time in US Central and UTC, the sign and degree the Moon is in, and its traditional almanac name, computed with the Swiss Ephemeris. {len(ecl)} of them are lunar eclipses.</p>
{rest}
  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Date</th><th>Exact time</th><th>Moon in</th><th>Name</th></tr>
{chr(10).join(lunation_rows("full", YEAR))}
    </table>
    <p class="hint" style="margin-top:8px">The next Full Moon is highlighted. Names follow the North American almanac tradition by calendar month in US Central time. Put them all in your calendar with the <a href="/astrology-calendar">free sky calendar feed</a>.</p>
  </div>

  <section class="prose">
    <h2>What a Full Moon is for</h2>
    <p>At the Full Moon the Sun and Moon stand opposite each other, and what began at the New Moon two weeks earlier comes to light. It is the culmination of the month: things are seen clearly, feelings run near the surface, and it is a natural moment to finish, celebrate, or let something go. The sign the Moon is in names the part of life that gets lit up; the Sun's sign across from it names what you balance against it.</p>
    <h2>The names, and where they come from</h2>
    <p>The almanac names (Wolf, Snow, Worm, Pink, Flower, Strawberry, Buck, Sturgeon, Corn or Harvest, Hunter's, Beaver, Cold) are the North American names popularized by farmers' almanacs, drawn from seasonal life in the northern hemisphere. Two have a rule rather than a month: the Harvest Moon is the Full Moon nearest the September equinox, which in {YEAR} is {long_day(harvest)}, and the Hunter's Moon follows it. A Blue Moon, by the calendar rule used here, is a second Full Moon in the same month.</p>
    <h2>{YEAR + 1} at a glance</h2>
    <p>{compact("full", YEAR + 1)}</p>
  </section>

  <div class="cta">
    <h2>Read the Moon in your own chart</h2>
    <p>Every Full Moon lands in one of the twelve houses of your chart. Cast your free natal chart to see which room each one lights, or see where the Moon is <a href="/moon" style="color:var(--gold-hi)">right now</a>.</p>
    <a href="/natal-chart">Cast your free natal chart</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    return page(slug, f"Full Moon Calendar {YEAR}: Dates, Times and Names",
                f"Every Full Moon of {YEAR} with exact Central and UTC times, zodiac sign and degree, "
                f"almanac names from Wolf Moon to Cold Moon, and the lunar eclipses marked.",
                body, [faq_schema(qas), item_list(f"Full Moons {YEAR}", f"{SITE}/{slug}", items)])


def gen_new_moons():
    slug = "new-moon-calendar"
    xs = [x for x in LUNES if x["kind"] == "new" and year_of(x) == YEAR]
    ecl = [x for x in xs if x.get("eclipse")]
    rest_2026 = [x for x in LUNES if x["kind"] == "new" and year_of(x) == YEAR - 1
                 and date.fromisoformat(x["central_date"]) >= ASOF]
    qas = [
        (f"How many new moons are in {YEAR}?",
         f"{len(xs)}, from {long_day(xs[0])} in {xs[0]['sign']} to {long_day(xs[-1])} in {xs[-1]['sign']}."),
        (f"When are the new moons in {YEAR}?",
         "; ".join(f"{long_day(x)} in {x['sign']}" for x in xs) + " (US Central time)."),
        (f"Which new moons are solar eclipses in {YEAR}?",
         "; ".join(f"{long_day(x)}, {x['eclipse']} in {x['sign']}" for x in ecl) + "."),
        ("What should you do on a new moon?",
         "Begin. The New Moon is the dark start of the lunar month, the traditional moment to set an "
         "intention, plant a seed, or take the first small step on something you want to grow over the "
         "weeks ahead. The sign it falls in suggests the kind of beginning it favors."),
    ]
    rest = ""
    if rest_2026:
        rest = (f'  <div class="highlight"><strong>Still to come in {YEAR - 1}:</strong> '
                + " &middot; ".join(f"{long_day(x)} in {x['sign']} at {central(x)[1]}" for x in rest_2026)
                + ".</div>")
    items = [(f"New Moon in {x['sign']} {long_day(x)}", f"At {deg_text(x)}, {x['central_label']}"
              + (f"; {x['eclipse']}" if x.get("eclipse") else "")) for x in xs]
    body = f"""  <h1>New Moon calendar {YEAR}</h1>
  <p class="lede">There are {len(xs)} New Moons in {YEAR}, each the start of a lunar month and a natural day to begin something. Below are the exact times in US Central and UTC, the sign and degree, and what each sign's New Moon favors, computed with the Swiss Ephemeris. {len(ecl)} of them are solar eclipses.</p>
{rest}
  <div class="card table-scroll">
    <table class="sky-table">
      <tr><th>Date</th><th>Exact time</th><th>Moon in</th><th>A good month to</th></tr>
{chr(10).join(lunation_rows("new", YEAR))}
    </table>
    <p class="hint" style="margin-top:8px">The next New Moon is highlighted. Add every New and Full Moon to your phone with the <a href="/astrology-calendar">free sky calendar</a>.</p>
  </div>

  <section class="prose">
    <h2>Why begin at the New Moon</h2>
    <p>At the New Moon the Sun and Moon meet in the same sign, and the Moon is dark. Over the next two weeks she grows toward full, and the tradition reads that growth as momentum: what you start now has the whole waxing half of the month behind it. This is why electional astrology, the art of choosing a good moment, so often prefers a waxing Moon for anything you want to grow.</p>
    <p>A New Moon is a seed, not a guarantee. Name one thing you want to become true in the month ahead, take the first concrete step toward it within a day or two, and check in at the Full Moon two weeks later to see what has come to light. For the strongest single days to begin a specific thing, the <a href="/almanac">best-dates guides</a> go further.</p>
    <h2>{YEAR + 1} at a glance</h2>
    <p>{compact("new", YEAR + 1)}</p>
  </section>

  <div class="cta">
    <h2>Pick the moment, not just the month</h2>
    <p>The free timing finder scans the coming weeks for the strongest windows to launch, sign, travel or marry, with every reason shown.</p>
    <a href="/electional">Find your best dates</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    return page(slug, f"New Moon Calendar {YEAR}: Dates, Times and Signs",
                f"Every New Moon of {YEAR} with exact Central and UTC times, sign and degree, what each "
                f"one favors, and the solar eclipses marked. Computed with the Swiss Ephemeris.",
                body, [faq_schema(qas), item_list(f"New Moons {YEAR}", f"{SITE}/{slug}", items)])


# ---------- 5. The calendar feed and its page ----------

def feed_events(start, end):
    """(sort_key, VEVENT lines) for every event between two dates."""
    evs = []
    for x in LUNES:
        cd = date.fromisoformat(x["central_date"])
        if not start <= cd <= end:
            continue
        kind = "Full Moon" if x["kind"] == "full" else "New Moon"
        name = f" ({x['name']})" if x.get("name") else ""
        ecl = f": {x['eclipse']}" if x.get("eclipse") else ""
        summary = f"{kind} in {x['sign']}{name}{ecl}"
        page_ = "full-moon-calendar" if x["kind"] == "full" else "new-moon-calendar"
        desc = (f"Exact at {x['central_label']} ({x['utc_label']}), {deg_text(x)}. "
                f"Computed with the Swiss Ephemeris. {SITE}/{page_}")
        uid = f"{x['kind']}moon-{x['utc'][:10]}@thetwelverooms.com"
        dt = d_of(x["utc"]).strftime("%Y%m%dT%H%M00Z")
        evs.append((x["utc"], ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTART:{dt}", f"SUMMARY:{summary}",
                               f"DESCRIPTION:{desc}", f"URL:{SITE}/{page_}", "TRANSP:TRANSPARENT",
                               "END:VEVENT"]))
    for p in ("Mercury", "Venus", "Mars"):
        for r in DATA["retrogrades"][p]:
            a, b = r["station_retrograde"], r["station_direct"]
            ad, bd = date.fromisoformat(a["central_date"]), date.fromisoformat(b["central_date"])
            if bd < start or ad > end:
                continue
            shadow = ""
            if r.get("shadow_begins"):
                shadow = (f" Shadow {long_day(r['shadow_begins'])} to {long_day(r['shadow_ends'])}.")
            page_ = {"Mercury": "is-mercury-retrograde", "Venus": "venus-retrograde"}.get(p, f"retrogrades-{YEAR}")
            desc = (f"{p} stations retrograde {a['central_label']} at {deg_text(a)} and direct "
                    f"{b['central_label']} at {deg_text(b)}.{shadow} {SITE}/{page_}")
            evs.append((a["utc"], ["BEGIN:VEVENT", f"UID:{p.lower()}-rx-{a['utc'][:10]}@thetwelverooms.com",
                                   f"DTSTART;VALUE=DATE:{ad.strftime('%Y%m%d')}",
                                   f"DTEND;VALUE=DATE:{(bd + timedelta(days=1)).strftime('%Y%m%d')}",
                                   f"SUMMARY:{p} retrograde in {signs_phrase(r['signs'])}",
                                   f"DESCRIPTION:{desc}", f"URL:{SITE}/{page_}", "TRANSP:TRANSPARENT",
                                   "END:VEVENT"]))
    for x in ECL:
        cd = date.fromisoformat(x["central_date"])
        if not start <= cd <= end:
            continue
        # A lunation event already carries the eclipse in its title; this one
        # marks the eclipse maximum itself, which can sit minutes to an hour away.
        summary = f"{x['type'].capitalize()} {x['kind']} eclipse in {x['sign']} (maximum)"
        epage = f"eclipses-{YEAR}" if cd.year == YEAR else (
            "new-moon-calendar" if x["kind"] == "solar" else "full-moon-calendar")
        desc = (f"Greatest eclipse {x['central_label']} ({x['utc_label']}), {deg_text(x)}. "
                f"{SITE}/{epage}")
        dt = d_of(x["utc"]).strftime("%Y%m%dT%H%M00Z")
        evs.append((x["utc"], ["BEGIN:VEVENT", f"UID:{x['kind']}-eclipse-{x['utc'][:10]}@thetwelverooms.com",
                               f"DTSTART:{dt}", f"SUMMARY:{summary}", f"DESCRIPTION:{desc}",
                               f"URL:{SITE}/{epage}", "TRANSP:TRANSPARENT", "END:VEVENT"]))
    return sorted(evs, key=lambda t: t[0])


def ics_escape(line):
    key, _, val = line.partition(":")
    if key in ("SUMMARY", "DESCRIPTION"):
        val = val.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    return f"{key}:{val}"


def fold(line):
    """RFC 5545: lines over 75 octets continue on the next line after a space."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not parts else 74):
            parts.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    parts.append(cur.decode("utf-8"))
    return "\r\n ".join(parts)


def write_ics(path, name, start, end):
    stamp = datetime(ASOF.year, ASOF.month, ASOF.day, tzinfo=timezone.utc).strftime("%Y%m%dT000000Z")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//The Twelve Rooms//Sky Calendar//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{name}",
             "X-WR-CALDESC:New and Full Moons\\, eclipses\\, and Mercury\\, Venus and Mars retrogrades. "
             "Computed with the Swiss Ephemeris by The Twelve Rooms.",
             "X-WR-TIMEZONE:UTC", "REFRESH-INTERVAL;VALUE=DURATION:P1W", "X-PUBLISHED-TTL:P1W"]
    n = 0
    for _, ev in feed_events(start, end):
        ev = [ics_escape(l) for l in ev]
        ev.insert(2, f"DTSTAMP:{stamp}")
        lines += ev
        n += 1
    lines.append("END:VCALENDAR")
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(("\r\n".join(fold(l) for l in lines) + "\r\n").encode("utf-8"))
    return n


FEED = "calendar/twelve-rooms.ics"
FEED_YEAR = f"calendar/twelve-rooms-{YEAR}.ics"


def gen_calendar():
    slug = "astrology-calendar"
    end = date(DATA["to_year"], 12, 31)
    n_roll = write_ics(ROOT / FEED, "The Twelve Rooms: Sky Calendar", ASOF.replace(day=1), end)
    n_year = write_ics(ROOT / FEED_YEAR, f"The Twelve Rooms: Sky Calendar {YEAR}",
                       date(YEAR, 1, 1), date(YEAR, 12, 31))
    host = SITE.split("//")[1]
    webcal = f"webcal://{host}/{FEED}"
    gcal = f"https://calendar.google.com/calendar/render?cid={webcal}"
    events = feed_events(date(YEAR, 1, 1), date(YEAR, 12, 31))
    months = {}
    for key, ev in events:
        summary = next(l for l in ev if l.startswith("SUMMARY:"))[8:]
        start_line = next(l for l in ev if l.startswith("DTSTART"))
        if "VALUE=DATE" in start_line:
            d = datetime.strptime(start_line.split(":")[1], "%Y%m%d")
            label = f"{d.strftime('%b %-d')}: {summary} begins"
        else:
            u = datetime.strptime(start_line.split(":")[1], "%Y%m%dT%H%M00Z").replace(tzinfo=timezone.utc)
            c = u.astimezone(skc.CENTRAL)
            d = c
            label = f"{c.strftime('%b %-d, %-I:%M %p')} {c.tzname()}: {summary}"
        if d.year != YEAR:
            continue
        months.setdefault(d.strftime("%B"), []).append(label)
    month_html = "\n".join(
        f'    <div class="month-block"><h3>{m} {YEAR}</h3><ul>'
        + "".join(f"<li>{e(x)}</li>" for x in v) + "</ul></div>" for m, v in months.items())
    full = sum(1 for x in LUNES if year_of(x) == YEAR and x["kind"] == "full")
    new = sum(1 for x in LUNES if year_of(x) == YEAR and x["kind"] == "new")
    ecl = sum(1 for x in ECL if year_of(x) == YEAR)
    qas = [
        ("How do I add the astrology calendar to Google Calendar?",
         f"On a computer, open Google Calendar, choose the plus sign next to Other calendars, pick From URL, "
         f"and paste https://{host}/{FEED}. Or use the Add to Google Calendar button on this page. It then "
         f"appears on your phone too."),
        ("How do I add it to Apple Calendar on iPhone?",
         "Tap Subscribe on Apple Calendar on this page and confirm. Or go to Settings, Calendar, Accounts, "
         f"Add Account, Other, Add Subscribed Calendar, and enter https://{host}/{FEED}."),
        ("What is in the calendar?",
         f"For {YEAR}: {full} Full Moons with their almanac names, {new} New Moons, {ecl} eclipses, and the "
         f"Mercury and Mars retrogrades as all-day spans, each with its exact time, sign and degree."),
        ("Does it update itself?",
         "Yes, if you subscribe rather than download. Subscribed calendars refresh on their own, so new "
         "dates appear as the feed is extended. A downloaded file is a one-time copy."),
        ("Is it free?", "Yes. No account, no sign-up."),
    ]
    body = f"""  <h1>The astrology calendar, free for your phone</h1>
  <p class="lede">Every New and Full Moon, every eclipse, and every Mercury retrograde, in the calendar you already use. Subscribe once and the dates arrive on their own, each with its exact time, sign and degree, computed with the Swiss Ephemeris.</p>

  <div class="card">
    <h2 style="margin-top:0">Subscribe in one tap</h2>
    <div class="subscribe">
      <a class="primary" href="{gcal}" rel="noopener">Add to Google Calendar</a>
      <a href="{webcal}">Subscribe on Apple Calendar</a>
      <a href="/{FEED}" download>Download the .ics</a>
    </div>
    <p class="hint">Outlook: Add calendar, Subscribe from web, and paste the address below. Any app that reads iCalendar (.ics) feeds works.</p>
    <textarea class="codebox" id="feed-url" readonly rows="1" style="min-height:0">https://{host}/{FEED}</textarea>
    <button class="copybtn" type="button" data-copy="feed-url" data-label="Copy the feed address">Copy the feed address</button>
    <p class="hint" style="margin-top:10px">Just {YEAR}? <a href="/{FEED_YEAR}" download>Download the {YEAR} file</a> ({n_year} events). The subscribed feed carries {n_roll} events from this month through {DATA['to_year']}.</p>
  </div>

  <section class="prose">
    <h2>What arrives in your calendar</h2>
    <p><strong>Full Moons</strong> with their traditional names, from the Wolf Moon to the Cold Moon, and <strong>New Moons</strong>, each at the exact minute. <strong>Eclipses</strong>, solar and lunar, marked at their maximum. <strong>Mercury retrograde</strong> as an all-day span from station to station, with the shadow dates in the note, plus the rarer Venus and Mars retrogrades. Every event links back to the page that explains it.</p>
    <p>Events are set as free time, so they never block a meeting. Times are stored in UTC and your calendar shows them in your own timezone.</p>
    <h2>The {YEAR} sky, month by month</h2>
{month_html}
  </section>

  <div class="cta">
    <h2>Your own dates, not just the sky's</h2>
    <p>This calendar is the shared sky. The Year-Ahead Reading reads {YEAR} through your own chart, with the dates that matter to you.</p>
    <a href="{etsy(slug)}" rel="noopener">The Year-Ahead Reading on Etsy</a>
  </div>

{faq_html(qas)}
{others(slug)}"""
    page(slug, f"Astrology Calendar {YEAR}: Free Feed for Your Phone",
         f"A free astrology calendar for Google, Apple and Outlook: every {YEAR} New and Full Moon, eclipse "
         f"and Mercury retrograde, with exact times and signs. Subscribe once.",
         body, [faq_schema(qas)])
    return n_roll, n_year


# ---------- 6. The Moon widget ----------

WIDGET = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Moon today · The Twelve Rooms</title>
<meta name="description" content="Today's Moon sign and phase, computed live with the Swiss Ephemeris. An embeddable widget from The Twelve Rooms.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://thetwelverooms.com/moon">
<meta property="og:title" content="The Moon today · The Twelve Rooms">
<meta property="og:description" content="Today's Moon sign and phase, computed live with the Swiss Ephemeris.">
<meta property="og:image" content="https://thetwelverooms.com/og/webtools.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<style>
:root { --navy:#26355e; --gold:#a8863d; --gold-deep:#7a5f24; --gold-hi:#e6cf96; --cream:#fbfaf7; --line:#e4ddcf; --soft:#656b85; }
* { box-sizing: border-box; margin: 0; }
html, body { background: transparent; }
body { font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }
.w { width: 100%; max-width: 320px; min-height: 150px; border: 1px solid var(--line); border-radius: 14px;
  background: var(--cream); color: var(--navy); padding: 14px 16px; display: flex; gap: 14px; align-items: center; }
.dark .w { background: radial-gradient(130% 150% at 50% 0%, #1f2b4e, #101830); border-color: #2c3a63; color: #e8ebf4; }
svg.m { flex: 0 0 64px; }
.k { font-size: 10px; letter-spacing: .22em; text-transform: uppercase; color: var(--soft); }
.dark .k { color: #9aa5c2; }
.s { font-family: Didot, "Bodoni 72", Georgia, serif; font-size: 21px; line-height: 1.2; margin: 3px 0 2px; }
.p { font-size: 13.5px; }
.n { font-size: 12px; color: var(--soft); margin-top: 6px; line-height: 1.4; }
.dark .n { color: #b6bed6; }
.c { display: block; font-size: 11px; margin-top: 8px; color: var(--gold-deep); text-decoration: none; }
.dark .c { color: var(--gold-hi); }
.c:hover { text-decoration: underline; }
</style>
</head>
<body>
<div class="w" id="w">
  <svg class="m" id="moon" viewBox="-32 -32 64 64" width="64" height="64" aria-hidden="true"></svg>
  <div>
    <div class="k">The Moon today</div>
    <div class="s" id="sign">Reading the sky&hellip;</div>
    <div class="p" id="phase"></div>
    <div class="n" id="next"></div>
    <a class="c" href="https://thetwelverooms.com/moon?utm_source=embed&amp;utm_medium=widget&amp;utm_campaign=moon-today" target="_blank" rel="noopener">Moon data by The Twelve Rooms</a>
  </div>
</div>
<script>
"use strict";
(function () {
  var q = new URLSearchParams(location.search);
  if (q.get("theme") === "dark") document.documentElement.className = "dark";
  var tz = "America/Chicago";
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || tz; } catch (e) {}
  if (q.get("tz")) tz = q.get("tz");
  function draw(elong) {
    /* Lit fraction and limb from the Sun-Moon elongation the API returns. */
    var r = 26, k = Math.cos(elong * Math.PI / 180), waxing = elong < 180;
    var rx = Math.abs(k) * r, lit = waxing ? 1 : 0;
    var outer = "M0,-" + r + " A" + r + "," + r + " 0 0," + lit + " 0," + r;
    var inner = " A" + rx.toFixed(2) + "," + r + " 0 0," + ((k > 0) === waxing ? 0 : 1) + " 0,-" + r;
    var dark = document.documentElement.className === "dark";
    document.getElementById("moon").innerHTML =
      '<circle r="' + r + '" fill="' + (dark ? "#26335a" : "#e9e3d3") + '"/>' +
      '<path d="' + outer + inner + '" fill="' + (dark ? "#e6cf96" : "#c9a55c") + '"/>' +
      '<circle r="' + r + '" fill="none" stroke="#b18b45" stroke-width="0.8"/>';
  }
  fetch("/api/moon?tz=" + encodeURIComponent(tz)).then(function (r) { return r.json(); }).then(function (d) {
    if (d.error) throw new Error(d.error);
    document.getElementById("sign").textContent = "Moon in " + d.sign;
    document.getElementById("phase").textContent = d.phase + (d.void_of_course ? " \\u00b7 void of course" : "");
    var n = d.void_of_course && d.voc_until ? "Void until " + d.voc_until : "";
    if (d.next_ingress) n = (n ? n + ". " : "") + "Enters " + d.next_ingress.sign + " " + d.next_ingress.at;
    document.getElementById("next").textContent = n;
    draw(d.illumination_deg);
  }).catch(function () {
    document.getElementById("sign").textContent = "The Moon today";
    document.getElementById("phase").textContent = "See it live at thetwelverooms.com/moon";
  });
})();
</script>
<script src="/tools.js"></script>
</body>
</html>
"""


def gen_embed():
    (ROOT / "embed").mkdir(exist_ok=True)
    (ROOT / "embed" / "moon-today.html").write_text(WIDGET, encoding="utf-8")
    slug = "embed"
    snippet_light = ('<iframe src="https://thetwelverooms.com/embed/moon-today" title="The Moon today" '
                     'width="320" height="160" style="border:0;max-width:100%" loading="lazy"></iframe>\n'
                     '<p style="font-size:12px;margin:4px 0 0"><a href="https://thetwelverooms.com/moon">'
                     'Moon sign and phase today</a> by The Twelve Rooms</p>')
    snippet_dark = snippet_light.replace("/embed/moon-today\"", "/embed/moon-today?theme=dark\"")
    qas = [
        ("Is the Moon widget free?",
         "Yes, for any site, personal or commercial. Keep the credit line under the widget so readers can "
         "find where the data comes from."),
        ("How accurate is it?",
         "The sign, phase and next sign change are computed live with the Swiss Ephemeris every time the "
         "widget loads, the same engine behind the site's Moon page. Times show in each reader's own timezone."),
        ("Can I change the size or colors?",
         "The widget fits any width up to 320 pixels and comes in a light cream and a navy theme. Add "
         "?theme=dark to the address for the navy one."),
        ("Does it slow my page down?",
         "It loads lazily in its own frame, so it waits until a reader scrolls near it and never blocks "
         "your page."),
    ]
    body = f"""  <h1>Free Moon phase widget for your website</h1>
  <p class="lede">Show your readers today's Moon sign and phase, updated live with the Swiss Ephemeris. Copy two lines of code, paste them into any page, and the widget does the rest. Free, with a small credit line back to The Twelve Rooms.</p>

  <div class="card">
    <h2 style="margin-top:0">Preview</h2>
    <div class="embed-preview">
      <iframe src="/embed/moon-today" title="The Moon today, light theme" width="320" height="160" loading="lazy"></iframe>
      <iframe src="/embed/moon-today?theme=dark" title="The Moon today, navy theme" width="320" height="160" loading="lazy"></iframe>
    </div>
  </div>

  <div class="card">
    <h2 style="margin-top:0">Copy the code: light</h2>
    <textarea class="codebox" id="code-light" readonly>{e(snippet_light)}</textarea>
    <button class="copybtn" type="button" data-copy="code-light" data-label="Copy code">Copy code</button>
    <h2>Copy the code: navy</h2>
    <textarea class="codebox" id="code-dark" readonly>{e(snippet_dark)}</textarea>
    <button class="copybtn" type="button" data-copy="code-dark" data-label="Copy code">Copy code</button>
    <p class="hint" style="margin-top:10px"><a href="/embed/moon-today">Open the widget on its own</a> to check it before you paste. Works in WordPress (Custom HTML block), Squarespace (Code block), Wix (Embed HTML), Ghost, Webflow and plain HTML.</p>
  </div>

  <section class="prose">
    <h2>What it shows</h2>
    <p>The sign the Moon is in right now, her phase from New to Full and back, whether she is void of course, and when she enters the next sign, all in your reader's own timezone. The drawing of the Moon matches the real lit fraction and the side it is lit from. Nothing is cached from yesterday: every load asks the ephemeris.</p>
    <p>It suits astrology blogs, yoga and wellness studios, gardening sites that plant by the Moon, and anyone who writes a weekly horoscope. For the full picture, readers can follow the credit to <a href="/moon">the Moon right now</a>, with the day's aspects and the void-of-course windows.</p>
  </section>

{faq_html(qas)}
{related([("/moon", "The Moon right now"), ("/full-moon-calendar", "Full Moon calendar"), ("/astrology-calendar", "The sky calendar feed")])}"""
    return page(slug, "Free Moon Phase Widget for Your Website",
                "A free, embeddable Moon widget: today's Moon sign and phase, computed live with the "
                "Swiss Ephemeris. Copy two lines of code into any site. Light and navy themes.",
                body, [faq_schema(qas), {"@context": "https://schema.org", "@type": "WebApplication",
                                         "name": "The Moon today widget", "applicationCategory": "LifestyleApplication",
                                         "operatingSystem": "Web", "url": f"{SITE}/embed",
                                         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}])


def main():
    written = [gen_is_mercury(), gen_retrogrades(), gen_eclipses(), gen_full_moons(), gen_new_moons()]
    n_roll, n_year = gen_calendar()
    written += ["astrology-calendar", gen_embed(), "embed/moon-today"]
    print("as of", ASOF.isoformat(), "wrote:", ", ".join(f"/{w}" for w in written))
    print(f"feeds: /{FEED} ({n_roll} events), /{FEED_YEAR} ({n_year} events)")
    subprocess.run([sys.executable, str(ROOT / "bin" / "apply_og_tags.py")], check=True)


if __name__ == "__main__":
    main()
