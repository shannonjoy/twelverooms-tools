#!/usr/bin/env python3
"""Answer-first copy, one FAQ per page, WebApplication schema and related
links on the twelve core tool pages (index plan, 2026-10-21).

Shannon: "make twelve rooms get traffic", "get it some AEO too". Bing,
which ChatGPT Search and Copilot draw on, already indexes the site, so
the pages should hand an answer engine a short, quotable answer to the
question people actually type, near the top, and an FAQ whose visible
text and FAQPage schema say exactly the same thing.

For each page in PAGES this script:
  1. writes a short direct answer under the lede (div.highlight, between
     aeo-answer markers);
  2. makes the FAQ one list: the visible questions and the FAQPage JSON-LD
     are rebuilt from the same (question, answer) pairs, every answer 40
     to 70 words. An answer whose visible HTML already says the same text
     (links and all) keeps its HTML;
  3. adds WebApplication JSON-LD to calculators that lack it;
  4. writes a "Where to go next" block of 3 to 5 related tools and date
     pages with descriptive anchors, before the site footer.
It also gives the home page in-body links to the core guides it lacked.

Every fact here is computed elsewhere on the site or by its engines
(Mercury stations checked against the Swiss Ephemeris on 2026-10-21).
Nothing promises limits on data collection (CLAUDE.md, measurement).

Idempotent: every block sits between markers and is replaced on re-run.
Usage: python3 bin/apply_aeo.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ANSWER_START, ANSWER_END = "<!-- aeo-answer: start (bin/apply_aeo.py) -->", "<!-- aeo-answer: end -->"
REL_START, REL_END = "<!-- aeo-related: start (bin/apply_aeo.py) -->", "<!-- aeo-related: end -->"
APP_START, APP_END = "<!-- aeo-webapp: start -->", "<!-- aeo-webapp: end -->"
HOME_START, HOME_END = "<!-- aeo-guides: start (bin/apply_aeo.py) -->", "<!-- aeo-guides: end -->"

MIN_WORDS, MAX_WORDS = 40, 70

# Shared answers, reused where a question is asked on several pages.
CALC_NATAL = ("Every position comes from the Swiss Ephemeris, the astronomical engine professional "
              "astrology software is built on, using the coordinates and timezone of your birthplace. "
              "Houses are whole-sign, the oldest system, so your rising sign is your entire first house. "
              "Aspects are measured to the exact degree, and the chart's patterns are found from them.")

PAGES = {
    "natal-chart": {
        "answer": ("<strong>What is a natal chart?</strong> A map of the sky at the minute and place you "
                   "were born: where the Sun, Moon and planets stood, in which signs and houses, and the "
                   "angles they made to each other. This calculator draws yours free from your birth "
                   "date, time and place, computed with the Swiss Ephemeris in whole-sign houses."),
        "faq_override": {"How is this calculated?": CALC_NATAL},
        "webapp": ("Free Natal Chart Calculator",
                   "A birth chart wheel with exact degrees, whole-sign houses, aspects and patterns, "
                   "computed with the Swiss Ephemeris."),
        "related": [
            ("/big-3-calculator", "Find your Sun, Moon and rising sign"),
            ("/the-twelve-houses", "What each of the twelve houses holds"),
            ("/transit-timeline", "Your transits for the next three years"),
            ("/synastry", "Compare two birth charts in the synastry grid"),
            ("/daily-horoscope", "Today's transits to your own chart"),
        ],
    },
    "big-3-calculator": {
        "answer": ("<strong>What is my Big 3?</strong> Your Sun sign, Moon sign and rising sign. The Sun "
                   "comes from your birth date and the Moon almost always does too; the rising sign needs "
                   "your birth time, because it changes about every two hours. Enter your details and the "
                   "calculator gives all three, computed with the Swiss Ephemeris."),
        "faq_add": [
            ("Why is my rising sign different from other sites?",
             "Usually the birth time. The rising sign changes about every two hours, so near a sign "
             "change a time that is a few minutes off, or a timezone or daylight saving rule applied "
             "wrongly, moves it into the next sign. This calculator uses the Swiss Ephemeris with your "
             "exact time, place and timezone, so check the time you entered on each site."),
        ],
        "faq_override": {
            "How is this calculated?":
                ("With the Swiss Ephemeris, the astronomical engine professional astrology software is "
                 "built on, from your birth date, time and place. The Big 3 comes from the same "
                 "calculation as the free natal chart on this site, so the Sun, Moon and rising sign "
                 "here always match the full chart you get there, in whole-sign houses."),
        },
        "faq_order_last": "How is this calculated?",
        "related": [
            ("/natal-chart", "See your full natal chart"),
            ("/the-twelve-houses", "The twelve houses your rising sign sets up"),
            ("/daily-horoscope", "A daily horoscope from your own chart, not your Sun sign"),
            ("/synastry", "How your chart meets someone else's"),
        ],
    },
    "saturn-return-calculator": {
        "answer": ("<strong>When is my Saturn return?</strong> Your first Saturn return comes between "
                   "about ages 27 and 30, when Saturn arrives back at the exact degree it held at your "
                   "birth; the second comes near 58 or 59. Many returns make three exact passes across "
                   "about a year. Enter your birth date for yours to the day, or browse the computed "
                   "dates by birth year below."),
        "faq_add": [
            ("How is this calculated?",
             "Natal Saturn comes from the Swiss Ephemeris for your birth date, time and place. The "
             "calculator then follows Saturn's path day by day, finds every moment it crosses that exact "
             "degree, refines each crossing to the minute, and groups the crossings into returns with "
             "the stations between them. It is the same engine that writes the Saturn Return Report."),
        ],
        "related": [
            ("/saturn-return/1996", "Saturn return dates for 1996 births, by month"),
            ("/transit-timeline", "Every major transit in your next three years"),
            ("/solar-return-calculator", "Your solar return chart for this birthday"),
            ("/natal-chart", "Where Saturn sits in your natal chart"),
            ("/the-twelve-houses", "The house your Saturn return lands in"),
        ],
    },
    "synastry": {
        "answer": ("<strong>What is synastry?</strong> Synastry compares two birth charts by measuring "
                   "every planet in one against every planet in the other. The grid lists the aspects "
                   "between you: trines and sextiles where you flow, squares and oppositions where the "
                   "relationship does its work, computed to the degree with the Swiss Ephemeris."),
        "faq_override": {
            "How is this calculated?":
                ("Both charts are computed with the Swiss Ephemeris from each person's birth date, time "
                 "and place, in whole-sign houses. Every planet of one chart is then measured against "
                 "every planet of the other, and each pair that falls within orb of a major aspect is "
                 "listed, so you see the actual contacts between you rather than a single score."),
        },
        "webapp": ("Synastry Chart Calculator",
                   "Cross-aspects between two birth charts, computed with the Swiss Ephemeris."),
        "related": [
            ("/natal-chart", "Each person's natal chart"),
            ("/big-3-calculator", "Compare your Sun, Moon and rising signs"),
            ("/best-days-to-propose-2027", "The best days to propose in 2027"),
            ("/best-wedding-dates-2027", "The best wedding dates of 2027"),
        ],
    },
    "moon": {
        "answer": ("<strong>What sign is the Moon in today?</strong> The Moon changes sign every two to "
                   "three days, so the answer moves: the live panel on this page shows today's sign, "
                   "phase and any void-of-course window, computed with the Swiss Ephemeris, and every "
                   "date has its own page with that day's sign change timed to the minute."),
        "faq_override": {
            "How is this calculated?":
                ("Positions are computed live with the Swiss Ephemeris. A sign change is the moment the "
                 "Moon's longitude crosses into the next 30-degree sign; the void-of-course stretch runs "
                 "from her last major aspect in a sign until she enters the next one; and the phase "
                 "comes from the angle between the Sun and the Moon."),
        },
        "webapp": ("Moon Sign Today",
                   "The Moon's sign, phase and void-of-course status, live, computed with the Swiss Ephemeris."),
        "related": [
            ("/void-of-course-moon", "Void-of-course Moon times"),
            ("/planetary-hours", "Today's planetary hours"),
            ("/electional", "Find the best window to begin something"),
            ("/daily-horoscope", "Today's transits to your own chart"),
        ],
    },
    "daily-horoscope": {
        "answer": ("<strong>What is my horoscope today?</strong> Not a sun-sign paragraph: this computes "
                   "today's real transits to your own birth chart, each with the minute it is exact and "
                   "what it asks of you. Enter your birth details once, then read any day within five "
                   "years either way."),
        "faq_override": {
            "Can I read a past or future date?":
                ("Yes, any date within five years either way. The sky is computed fresh for whatever "
                 "date you pick, so a day last March and a day next autumn are both real readings "
                 "rather than recycled text. Looking back is a good way to see how a transit actually "
                 "played out before you meet the next one."),
        },
        "faq_replace": {
            "Is my birth data stored?": (
                "Where do the transits come from?",
                "From the Swiss Ephemeris. For the day you pick, the tool computes where the Moon and "
                "planets are, finds every transit within orb of your natal planets and angles, and times "
                "the exact ones to the minute. Your natal chart comes from the same engine as the free "
                "natal chart on this site, in whole-sign houses."),
        },
        "webapp": ("Personal Daily Horoscope",
                   "Today's transits to your own birth chart, timed to the minute, computed with the Swiss Ephemeris."),
        "related": [
            ("/natal-chart", "Your free natal chart"),
            ("/transit-timeline", "The slow transits of your next three years"),
            ("/moon", "The Moon's sign and phase right now"),
            ("/planetary-hours", "Which planet rules this hour"),
        ],
    },
    "transit-timeline": {
        "answer": ("<strong>What transits am I in?</strong> Enter your birth details and this lists every "
                   "exact aspect the slow planets, Jupiter through Pluto, make to your natal chart over "
                   "the next three years, dated to the day with retrograde passes included: your Saturn "
                   "return, Jupiter's growth cycles and the outer-planet turning points."),
        "faq_override": {
            "How is this calculated?":
                ("With the Swiss Ephemeris in whole-sign houses. The timeline scans the slow planets, "
                 "Jupiter through Pluto, day by day for their exact major aspects to your natal points, "
                 "including the extra passes a retrograde can bring, and dates each one. Your natal "
                 "chart comes from the same engine as the free natal chart."),
        },
        "text_fix": [("No account, nothing stored.", "No account needed.")],
        "related": [
            ("/saturn-return-calculator", "The exact dates of your Saturn return"),
            ("/daily-horoscope", "Today's transits, timed to the minute"),
            ("/solar-return-calculator", "Your solar return chart for the year ahead"),
            ("/natal-chart", "Your free natal chart"),
            ("/mercury-retrograde", "Mercury retrograde dates for 2026 and 2027"),
        ],
    },
    "planetary-hours": {
        "answer": ("<strong>What planetary hour is it now?</strong> Daylight is split into 12 planetary "
                   "hours and the night into 12 more, ruled in the Chaldean order: Saturn, Jupiter, Mars, "
                   "Sun, Venus, Mercury, Moon. The day's first hour belongs to the planet the day is named "
                   "for. Pick your city and the table shows the current hour, computed live."),
        "webapp": ("Planetary Hours Calculator",
                   "Today's planetary hours for your city, from local sunrise and sunset, computed with the Swiss Ephemeris."),
        "related": [
            ("/electional", "Score a date range for the best window"),
            ("/moon", "The Moon's sign and void-of-course status"),
            ("/void-of-course-moon", "Void-of-course Moon times"),
            ("/daily-horoscope", "Your own transits for today"),
        ],
    },
    "electional": {
        "answer": ("<strong>When is the best day to start something?</strong> Electional astrology picks "
                   "it: a waxing Moon that is not void of course, applying to Venus or Jupiter and clear "
                   "of Mars and Saturn, with the planets that rule your matter strong. Choose an intention "
                   "and a date range, and the finder scores the windows and shows the best with its "
                   "reasons."),
        "webapp": ("Electional Astrology Timing Finder",
                   "Scores a date range for the best windows to marry, launch, sign or move, computed with the Swiss Ephemeris."),
        "related": [
            ("/almanac", "Every best-dates guide, by intention"),
            ("/best-wedding-dates-2027", "The best wedding dates of 2027"),
            ("/best-days-to-start-a-business-2027", "The best days to start a business in 2027"),
            ("/mercury-retrograde", "Mercury retrograde dates to plan around"),
            ("/planetary-hours", "Today's planetary hours"),
        ],
    },
    "mercury-retrograde": {
        "answer": ("<strong>When is Mercury retrograde?</strong> The autumn 2026 retrograde runs October 24 "
                   "to November 13, in Scorpio. In 2027 Mercury is retrograde three times: February 9 to "
                   "March 3, June 10 to July 4, and October 7 to 28. Dates are in Universal Time, computed "
                   "with the Swiss Ephemeris."),
        "faq_override": {
            "What should you not do during Mercury retrograde?":
                ("Hold off, where you can, on signing contracts, launching something new, buying "
                 "electronics or a car, and starting a first-time commitment you want to run clean. These "
                 "are beginnings, and beginnings want a clear Mercury. If you cannot wait, read every line "
                 "twice and plan to revisit; revising, repairing and finishing all go well."),
        },
        "related": [
            ("/venus-retrograde", "Venus retrograde dates for 2026 and 2028"),
            ("/best-days-to-sign-a-contract-2027", "The best days to sign a contract in 2027"),
            ("/electional", "Find a window with Mercury direct"),
            ("/best-days-to-launch-a-product-2027", "The best days to launch a product in 2027"),
        ],
    },
    "best-wedding-dates-2027": {
        "related": [
            ("/best-wedding-dates-2028", "The best wedding dates of 2028"),
            ("/best-days-to-propose-2027", "The best days to propose in 2027"),
            ("/venus-retrograde", "Why 2027 has no Venus retrograde"),
            ("/synastry", "How your two charts meet"),
            ("/electional", "Score your own wedding date"),
        ],
    },
    "the-twelve-houses": {
        "answer": ("<strong>What are the 12 houses?</strong> Twelve areas of life laid out from your rising "
                   "sign: self, money, mind, home, pleasure, work, partnership, depth, belief, career, "
                   "community and the inner life. In whole-sign houses, the system this site uses, each "
                   "sign is one whole house, so your rising sign is your first."),
        "faq_add": [
            ("Which house is most important?",
             "The first, because it anchors the floor plan, and the tenth, because it is the most "
             "visible. But the honest answer is whichever room your chart's planets and current transits "
             "are lighting up: importance moves. That is what a timed reading is for."),
        ],
        "related": [
            ("/natal-chart", "See which planets sit in your houses"),
            ("/big-3-calculator", "Find your rising sign"),
            ("/transit-timeline", "Which rooms the slow planets visit next"),
            ("/sabian-symbols", "The Sabian symbol for every degree"),
        ],
    },
}

HOME_GUIDES = [
    ("/mercury-retrograde", "Mercury retrograde 2026 and 2027 dates"),
    ("/best-wedding-dates-2027", "The best wedding dates of 2027"),
    ("/the-twelve-houses", "The twelve houses, read as rooms"),
    ("/venus-retrograde", "Venus retrograde, and why 2027 has none"),
    ("/saturn-return/1996", "Saturn return dates by birth year"),
]

LD_RE = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
QA_RE = re.compile(r'<div class="qa"><h3>(.*?)</h3><p>(.*?)</p></div>', re.S)


def words(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def faq_ld(s):
    for m in LD_RE.finditer(s):
        d = json.loads(m.group(1))
        if d.get("@type") == "FAQPage":
            return m, d
    raise SystemExit("no FAQPage")


def build_faq(s, cfg):
    m, d = faq_ld(s)
    pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in d["mainEntity"]]
    rep = cfg.get("faq_replace", {})
    pairs = [rep.get(q, (q, a)) for q, a in pairs]
    over = cfg.get("faq_override", {})
    pairs = [(q, over.get(q, a)) for q, a in pairs]
    have = {q for q, _ in pairs}
    pairs += [(q, a) for q, a in cfg.get("faq_add", []) if q not in have]
    last = cfg.get("faq_order_last")
    if last:
        pairs = [p for p in pairs if p[0] != last] + [p for p in pairs if p[0] == last]
    for q, a in pairs:
        n = words(a)
        if not MIN_WORDS <= n <= MAX_WORDS:
            raise SystemExit(f"FAQ answer out of range ({n} words): {q}")
    return m, d, pairs


def set_faq(s, cfg):
    m, d, pairs = build_faq(s, cfg)
    d["mainEntity"] = [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
    new_ld = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    s = s[:m.start(1)] + new_ld + s[m.end(1):]
    # Visible FAQ: keep an item's HTML when it already says the same text.
    old = list(QA_RE.finditer(s))
    if not old:
        raise SystemExit("no visible FAQ")
    by_text = {plain(a): f'<div class="qa"><h3>{q}</h3><p>{a}</p></div>' for q, a in
               ((x.group(1), x.group(2)) for x in old)}
    items = []
    for q, a in pairs:
        keep = by_text.get(plain(a))
        if keep and plain(re.search(r"<h3>(.*?)</h3>", keep).group(1)) == plain(q):
            items.append(keep)
        else:
            items.append(f'<div class="qa"><h3>{html.escape(q, quote=False)}</h3>'
                         f'<p>{html.escape(a, quote=False)}</p></div>')
    start, end = old[0].start(), old[-1].end()
    return s[:start] + "\n    ".join(items) + s[end:]


def set_block(s, start, end, block, anchor_re, after=True):
    if start in s:
        return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, s, count=1, flags=re.S)
    m = re.search(anchor_re, s, re.S)
    if not m:
        raise SystemExit(f"anchor not found: {anchor_re}")
    pos = m.end() if after else m.start()
    return s[:pos] + block + s[pos:]


def set_answer(s, answer):
    block = f'{ANSWER_START}\n  <div class="highlight">{answer}</div>\n  {ANSWER_END}'
    return set_block(s, ANSWER_START, ANSWER_END, "\n  " + block if ANSWER_START not in s else block,
                     r'<p class="lede">.*?</p>')


def set_webapp(s, name, desc, slug):
    if '"WebApplication"' in s and APP_START not in s:
        return s
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": name,
                     "url": f"https://thetwelverooms.com/{slug}", "description": desc,
                     "applicationCategory": "LifestyleApplication", "operatingSystem": "Web",
                     "isAccessibleForFree": True,
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
                    ensure_ascii=False)
    block = f'{APP_START}\n<script type="application/ld+json">\n{ld}\n</script>\n{APP_END}'
    if APP_START in s:
        return set_block(s, APP_START, APP_END, block, "")
    return s.replace("</head>", block + "\n</head>", 1)


def set_related(s, links):
    lis = "\n".join(f'      <li><a href="{h}">{html.escape(t, quote=False)}</a></li>' for h, t in links)
    block = (f'{REL_START}\n  <section class="prose" aria-label="Related tools">\n'
             f'    <h2>Where to go next</h2>\n    <ul class="linklist">\n{lis}\n    </ul>\n'
             f'  </section>\n  {REL_END}')
    if REL_START in s:
        return set_block(s, REL_START, REL_END, block, "")
    return set_block(s, REL_START, REL_END, block + "\n  ", r'<div id="site-footer"', after=False)


def set_home(s):
    lis = "".join(f'<li><a href="{h}">{html.escape(t, quote=False)}</a></li>' for h, t in HOME_GUIDES)
    block = (f'{HOME_START}\n  <section class="prose" aria-label="Guides">\n    <h2>Guides to the sky</h2>\n'
             f'    <ul class="linklist">{lis}</ul>\n  </section>\n  {HOME_END}')
    if HOME_START in s:
        return set_block(s, HOME_START, HOME_END, block, "")
    m = re.search(r'<div class="toolgrid">.*?</div>', s, re.S)
    return s[:m.end()] + "\n  " + block + s[m.end():]


def main():
    for slug, cfg in PAGES.items():
        f = ROOT / f"{slug}.html"
        s = f.read_text(encoding="utf-8")
        for a, b in cfg.get("text_fix", []):
            s = s.replace(a, b)
        if "answer" in cfg:
            s = set_answer(s, cfg["answer"])
        s = set_faq(s, cfg)
        if "webapp" in cfg:
            s = set_webapp(s, *cfg["webapp"], slug)
        s = set_related(s, cfg["related"])
        for m in LD_RE.finditer(s):
            json.loads(m.group(1))
        f.write_text(s, encoding="utf-8")
        print(f"{slug}: answer={'answer' in cfg} faq={len(faq_ld(s)[1]['mainEntity'])} "
              f"webapp={'WebApplication' in s} related={len(cfg['related'])}")
    f = ROOT / "index.html"
    f.write_text(set_home(f.read_text(encoding="utf-8")), encoding="utf-8")
    print("index: guide links")


if __name__ == "__main__":
    main()
