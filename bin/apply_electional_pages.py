#!/usr/bin/env python3
"""Bring the 24 best-dates pages to one standard (search plan 2026-10-21,
moves 2 and 3). Pure text work: no ephemeris here, so it runs anywhere.

For the eighteen pages with computed rows in bin/electional_data/ (written
by bin/compute_electional_rows.py):
  - the table shows the Twelve Rooms Timing Scale (stars, plain word, room
    name on hover), never a bare number;
  - a one-line answer above the table names the year's strongest dates,
    and the first FAQ answer opens with the same sentence;
  - every row note is computed: a weak month points at the year's best,
    an eclipse within five days is named, a Mercury retrograde is named
    where the election does not already exclude it, and a date moved off
    a sibling page's day says so and links it.

For all 24 pages:
  - month anchors (#january ... #december) and a month row above the table;
  - the CTA and the "does my chart matter" answers stop promising "a full
    electional reading", which is not sold anywhere, and name a reading
    that is: the Year-Ahead Reading, or for the two-person pages the
    Synastry Report, each a tagged Etsy listing link
    (utm_source=thetwelverooms&utm_medium=referral&utm_campaign=<slug>).

Idempotent: the table block sits between markers and every substitution
checks for its own output first.

Usage: python3 bin/apply_electional_pages.py
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "bin" / "electional_data"

# Same table as api/_seo/shop.py; ids from ~/orchestrator/ids.json.
LISTINGS = {"year_ahead": "4539692523", "synastry": "4542152602"}
PRODUCT_NAME = {"year_ahead": "The Year-Ahead Reading", "synastry": "The Synastry Report"}

PAGES = [
    "best-wedding-dates-2027", "best-wedding-dates-2028", "best-days-to-propose-2027",
    "best-days-to-sign-a-contract-2027", "best-days-to-start-a-business-2027",
    "best-days-to-launch-a-product-2027", "best-days-to-invest-2027",
    "best-days-to-buy-a-house-2027", "best-days-to-buy-a-car-2027",
    "best-days-to-move-to-a-new-city-2027", "best-days-to-open-a-restaurant-2027",
    "best-days-for-a-job-interview-2027", "best-days-to-ask-for-a-raise-2027",
    "best-days-to-send-an-important-email-2027", "best-days-to-publish-a-book-2027",
    "best-days-to-file-a-lawsuit-2027", "best-days-for-surgery-2027",
    "best-days-to-conceive-2027", "best-days-for-a-first-date-2027",
    "best-days-to-reconcile-2027", "best-days-to-throw-a-party-2027",
    "best-days-to-travel-2027", "best-days-to-start-a-diet-2027",
    "best-days-to-cut-your-hair-2027",
]
TWO_PERSON = {"best-wedding-dates-2027", "best-wedding-dates-2028", "best-days-to-propose-2027",
              "best-days-for-a-first-date-2027", "best-days-to-reconcile-2027"}
SIBLING_NAME = {
    "best-days-to-start-a-business-2027": "start-a-business guide",
    "best-days-to-invest-2027": "investing guide",
    "best-days-to-launch-a-product-2027": "product-launch guide",
    "best-days-to-propose-2027": "proposal guide",
}
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

START = "<!-- electional-table: start (bin/apply_electional_pages.py) -->"
END = "<!-- electional-table: end -->"


def etsy(product, slug):
    return (f"https://www.etsy.com/listing/{LISTINGS[product]}?utm_source=thetwelverooms"
            f"&amp;utm_medium=referral&amp;utm_campaign={slug}")


def long_day(iso):
    return date.fromisoformat(iso).strftime("%B %-d")


def short_day(iso):
    return date.fromisoformat(iso).strftime("%b %-d")


def and_list(items):
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def stars(n):
    return "★" * n + "☆" * (5 - n)


def verb_phrase(page_html, slug):
    if slug.startswith("best-wedding-dates"):
        return "to marry"
    h1 = re.search(r"<h1>(.*?)</h1>", page_html).group(1)
    m = re.match(r"Best Days (to|for) (.+?) in \d{4}", h1)
    return f"{m.group(1)} {m.group(2).lower()}"


# ---------- the computed table ----------

def _the(p):
    return f"the {p}" if p in ("Sun", "Moon") else p


def _nth(n):
    n = int(n)
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def polish(why):
    """Turn electional.explain()'s receipt shorthand into a sentence.

    explain() writes "Asc ruler Venus angular (house 7), day chart"; the
    pages already on the scale read "with Venus angular in the 7th". Same
    facts, reworded by rule, nothing added."""
    parts = why.rstrip(".").split(", ")
    lead = parts[0]
    lead = re.sub(r"a conjunction to (\w+)", r"a conjunction with \1", lead)
    lead = re.sub(r"\bto (Sun|Moon)$", r"to the \1", lead)
    ruler, ruler_bits, tail = None, [], []
    for t in parts[1:]:
        m = re.match(r"Asc ruler (\w+) angular \(house (\d+)\)$", t)
        if m:
            ruler = m.group(1)
            ruler_bits.append(f"angular in the {_nth(m.group(2))} house")
            continue
        m = re.match(r"Asc ruler (\w+) (domicile|exaltation) in (\w+)$", t)
        if m:
            ruler = m.group(1)
            ruler_bits.insert(0, ("at home in " if m.group(2) == "domicile" else "exalted in ") + m.group(3))
            continue
        m = re.match(r"(\w+) (domicile|exaltation) in (\w+)$", t)
        if m:
            tail.append(f"with {_the(m.group(1))} " + ("at home in " if m.group(2) == "domicile" else "exalted in ") + m.group(3))
            continue
        m = re.match(r"with (\w+) on the (Ascendant|Midheaven)$", t)
        if m:
            tail.append(f"with {_the(m.group(1))} on the {m.group(2)}")
            continue
        if t in ("day chart", "night chart"):
            tail.append("a " + t)
            continue
        tail.append(t)
    if ruler:
        ins = f"with {_the(ruler)}, the Ascendant's ruler, {' and '.join(ruler_bits)}"
        pos = next((i for i, t in enumerate(tail) if t.startswith("a ") or t.startswith("in a ")), len(tail))
        tail.insert(pos, ins)
    return ", ".join([lead] + tail) + "."


def row_notes(r, data, sky, best):
    notes = []
    d = date.fromisoformat(r["date"])
    mf = r.get("moved_from")
    if mf:
        notes.append(f'The strongest sky this month, {html.escape(mf["day"])}, leads the '
                     f'<a href="/{mf["page"]}">{SIBLING_NAME.get(mf["page"], "sibling guide")}</a>; '
                     f'this is the next-best day for this election.')
    for e in sky["eclipses"]:
        gap = abs((date.fromisoformat(e["date"]) - d).days)
        if gap == 0:
            notes.append(f'On the day of the {short_day(e["date"])} {e["kind"]} eclipse; pad it if you can.')
        elif gap <= 5:
            word = ["One", "Two", "Three", "Four", "Five"][gap - 1]
            notes.append(f'{word} day{"s" if gap > 1 else ""} from the {short_day(e["date"])} '
                         f'{e["kind"]} eclipse; pad it if you can.')
    if not data["mercury_direct_rule"]:
        for span in sky["mercury_retrograde"]:
            if span["from"] <= r["date"] <= span["to"]:
                notes.append(f'Mercury is retrograde ({short_day(span["from"])} to '
                             f'{short_day(span["to"])}), so keep paperwork out of it.')
    if r["stars"] <= 2 and best["date"] != r["date"]:
        notes.append(f'A thin month for {MATTER.get(data["recipe"], "this election")}; '
                     f'{long_day(best["date"])} is the year\'s strongest day if your date is flexible.')
    return notes


def _clock(iso_or_pretty):
    """'2027-01-13T15:13-06:00' or '4:00 PM' -> '3:13 p.m.' / '4 p.m.'."""
    s = iso_or_pretty
    if "T" in s:
        h, m = int(s[11:13]), int(s[14:16])
    else:
        hm, ap = s.split()
        h, m = (int(x) for x in hm.split(":"))
        h = h % 12 + (12 if ap.upper() == "PM" else 0)
    suffix = "a.m." if h < 12 else "p.m."
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {suffix}" if m else f"{h12} {suffix}"


# How each election is named inside a sentence.
MATTER = {"wedding": "a wedding", "engagement": "a proposal", "first_date": "a first date",
          "reconciliation": "reconciling", "conception": "conceiving",
          "business": "starting a business", "contract": "signing a contract",
          "launch": "a product launch", "job": "a job interview", "raise": "asking for a raise",
          "shop": "opening a restaurant", "investment": "investing",
          "publishing": "publishing a book", "home": "buying a house", "relocation": "a move",
          "car": "buying a car", "diet": "starting a diet", "haircut": "a haircut"}

_APPLY_RE = re.compile(r"applies to an? \w+ (?:to|with) (?:the )?(\w+)")
_HOUR_RE = re.compile(r"in an? (\w+) hour")
_ANGLE_RE = re.compile(r"with (?:the )?(\w+) on the (Ascendant|Midheaven)")


def significator_note(r, data):
    """Which of THIS election's own rules the window meets (2026-10-21,
    index plan). Elections that pick the same day share its sky; what
    differs is what each one is looking for in it, which the recipe says
    (bin/compute_electional_rows.significators)."""
    sig = data.get("significators")
    if not sig:
        return []
    why = r["why"]
    matter = MATTER.get(data["recipe"], data["label"].lower())
    hits = []
    m = _APPLY_RE.search(why)
    applies = sig["applies"]
    if m and m.group(1) in applies:
        pl = m.group(1)
        role = ("the planet it wants first" if pl == applies[0]
                else f"one of the {['', 'one', 'two', 'three'][len(applies)]} it looks for")
        hits.append(f"the Moon reaches {_the(pl)}, {role}")
    m = _HOUR_RE.search(why)
    if m and m.group(1) in sig["hours"]:
        hits.append(f"the hour is {_the(m.group(1))}'s, "
                    + ("its chosen hour" if len(sig["hours"]) == 1 else "one of its chosen hours"))
    for pl, ang in _ANGLE_RE.findall(why):
        if pl in sig["angular"]:
            hits.append(f"{_the(pl)} holds the {ang}")
    if hits:
        return [f"For {matter}: " + "; ".join(hits) + "."]
    return [f"For {matter}, none of its own planets ({and_list(applies)}) is touched here; "
            f"the rating rests on the rest of the chart."]


def window_note(r):
    """The computed window for this election on this day (2026-10-21,
    index plan). Two elections that share a day share its sky, but not its
    hours: each recipe scores its own planetary-hour rulers and angles."""
    if not r.get("start"):
        return []
    return [f'Open {_clock(r["start"])} to {_clock(r["end"])}, strongest near {_clock(r["peak_at"])} '
            f'Central time.']


def summary(data, verb):
    """The one-line answer, as (html, plain)."""
    rows = [r for r in data["rows"] if not r.get("none")]
    year = data["year"]
    top = [r for r in rows if r["stars"] == 5]
    if top:
        days = and_list([long_day(r["date"]) for r in top])
        one = len(top) == 1
        lead = (f"{days} {'is' if one else 'are'} {year}'s standout day{'' if one else 's'} {verb}, "
                f"rated Excellent on the Twelve Rooms Timing Scale, the top tenth of five years of "
                f"this election's own sky data.")
        aeo = f"{year}'s strongest day{'' if one else 's'} {verb}, on the Twelve Rooms Timing Scale: {days} (Excellent)."
    else:
        good = [r for r in rows if r["stars"] == 4]
        if good:
            days = and_list([long_day(r["date"]) for r in good])
            n = len(good)
            lead = (f"no month in {year} reaches the top Excellent tier for this election, but "
                    f"{'one is' if n == 1 else f'{n} are'} rated Good on the Twelve Rooms Timing "
                    f"Scale: {days}.")
            aeo = f"{year}'s strongest day{'' if n == 1 else 's'} {verb}, on the Twelve Rooms Timing Scale: {days} (Good)."
        else:
            best = max(rows, key=lambda r: r["score"])
            lead = (f"no month in {year} rises above Average for this election; the strongest day "
                    f"is {long_day(best['date'])}.")
            aeo = (f"{year}'s strongest day {verb}, on the Twelve Rooms Timing Scale: "
                   f"{long_day(best['date'])} ({best['label']}).")
    return f"<strong>If your date is flexible:</strong> {lead}", aeo


def table_block(data, sky, verb):
    rows = [r for r in data["rows"] if not r.get("none")]
    best = max(rows, key=lambda r: r["score"])
    out = []
    for r in data["rows"]:
        mid = r["month"].lower()
        if r.get("none"):
            out.append(f'        <tr id="{mid}"><td><strong>{r["month"]}</strong></td><td>None</td>'
                       f'<td>&mdash;</td><td>No window this month clears the requirements for this '
                       f'election; look to the neighboring months.</td></tr>')
            continue
        why = " ".join([html.escape(polish(r["why"]))] + significator_note(r, data) + window_note(r)
                       + row_notes(r, data, sky, best))
        title = html.escape(f'{r["blurb"]} ({r["room_name"]})')
        out.append(f'        <tr id="{mid}"><td><strong>{r["month"]}</strong></td>'
                   f'<td>{html.escape(r["day"])}</td>'
                   f'<td><span class="tag gold" title="{title}">{stars(r["stars"])} {r["label"]}</span></td>'
                   f'<td>{why}</td></tr>')
    highlight, _ = summary(data, verb)
    mercury = (f" Every {data['year']} date here keeps Mercury direct."
               if data["mercury_direct_rule"] else "")
    return (f'{START}\n'
            f'  <div class="highlight">{highlight}</div>\n\n'
            f'  <div class="card">\n'
            f'    {month_nav()}\n'
            f'    <table class="year-table">\n'
            f'      <thead><tr><th>Month</th><th>Best day</th><th>Strength</th><th>Why this one</th></tr></thead>\n'
            f'      <tbody>\n' + "\n".join(out) + '\n'
            f'      </tbody>\n'
            f'    </table>\n'
            f'    <p class="hint" style="margin-top:8px">Strength for {html.escape(MATTER.get(data["recipe"], data["label"].lower()))} '
            f'is read on the Twelve Rooms Timing Scale, against five years of this election\'s own '
            f'windows; times are computed for the geographic center of the contiguous US and move with '
            f'your city in the <a href="/electional">timing finder</a>.{mercury}</p>\n'
            f'  </div>\n'
            f'  {END}')


def month_nav():
    links = "".join(f'<a href="#{m.lower()}">{m[:3]}</a>' for m in MONTHS)
    return f'<nav class="monthnav" aria-label="Jump to a month">{links}</nav>'


OLD_CARD = re.compile(
    r'(?:<div class="highlight">.*?</div>\s*)?<div class="card">\s*<table class="year-table">.*?</table>'
    r'\s*<p class="hint"[^>]*>.*?</p>\s*</div>', re.S)
MARKED = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def set_table(s, data, sky, verb):
    block = table_block(data, sky, verb)
    if MARKED.search(s):
        return MARKED.sub(lambda _: block, s, count=1)
    s, n = OLD_CARD.subn(lambda _: block, s, count=1)
    if not n:
        raise SystemExit("no year table found")
    return s


# ---------- FAQ: first answer opens with the computed answer ----------

AEO_RE = re.compile(r"^\d{4}'s strongest days? [^:]*, on the Twelve Rooms Timing Scale: [^.]*\.\s*")


def set_first_answer(s, aeo):
    m = re.search(r'(<div class="qa"><h3>[^<]*</h3><p>)(.*?)(</p></div>)', s, re.S)
    if "<" in m.group(2):
        raise SystemExit("first FAQ answer carries markup; edit it by hand")
    body = AEO_RE.sub("", html.unescape(m.group(2)))
    new_plain = f"{aeo} {body}"
    s = s[:m.start(2)] + html.escape(new_plain, quote=False) + s[m.end(2):]
    # the FAQPage JSON-LD mirrors the visible answers on these pages
    sm = next(x for x in re.finditer(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)', s, re.S)
              if '"FAQPage"' in x.group(2))
    d = json.loads(sm.group(2))
    d["mainEntity"][0]["acceptedAnswer"]["text"] = new_plain
    js = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    return s[:sm.start(2)] + js + s[sm.end(2):]


# ---------- prose that named the old rows ----------
# Sentences written around the earlier, hand-entered rows. Each one either
# named a date the table no longer shows or said "every date" of something
# the computed rows do not all share. Replaced with what the rows support.
PROSE_FIXES = {
    "best-wedding-dates-2028": [
        (", which lifts March 27 and January 6 above the rest.", "."),
        ("The strongest fall on a Taurus Moon, the Moon's exaltation: March 27 and January 6. "
         "Each has the waxing Moon applying to Jupiter and clear of Mercury retrograde. "
         "The table above gives the best day in every month.",
         "The table above gives the best day in every month, each clear of the void and of "
         "Mercury retrograde."),
    ],
    "best-days-to-buy-a-house-2027": [
        (", which lifts February 12 and December 10.", "."),
    ],
    "best-days-to-start-a-business-2027": [
        ("which is why February and mid-summer are the year's weakest windows for a launch.",
         "which is part of why February, June, and October rate Weak for a launch this year."),
    ],
    "best-days-to-start-a-diet-2027": [
        ("Every date above sits on a waning Moon reaching toward restraint.",
         "Most dates above sit on a waning Moon reaching toward restraint."),
    ],
    "best-days-to-launch-a-product-2027": [
        ("Every date above keeps the Moon clear of Mars and Saturn.",
         "The dates above favor a Moon clear of Mars and Saturn."),
        ("Every date here is chosen to keep the Moon making a clean applying aspect at the peak window, not drifting void.",
         "Every date here keeps the Moon out of the void at the peak window."),
    ],
    "best-days-to-move-to-a-new-city-2027": [
        ("Every date keeps the Moon clear and moving toward fortune.",
         "Every date keeps the Moon out of the void."),
    ],
}


# ---------- anchors on pages already on the scale ----------

def add_anchors(s):
    if 'class="monthnav"' not in s:
        s = s.replace('<table class="year-table">', month_nav() + '\n    <table class="year-table">', 1)
    for m in MONTHS:
        s = re.sub(rf'<tr(?: id="[a-z]+")?><td><strong>{m}</strong>',
                   f'<tr id="{m.lower()}"><td><strong>{m}</strong>', s, count=1)
    return s


# ---------- the promise ----------

def promise(s, slug):
    product = "synastry" if slug in TWO_PERSON else "year_ahead"
    name = PRODUCT_NAME[product]
    if product == "synastry":
        reads = f"{name} reads how your two birth charts meet, written as one reading."
    else:
        reads = f"{name} reads your next twelve months from your own birth chart, with the dates worth circling."
    swaps = [
        (", which is the personalized electional reading, done by hand.",
         f". No table can judge that, this one included. What a reading can add is your own year: the Year-Ahead Reading reads your next twelve months from your birth chart."),
        (", and that is the personalized electional reading, done by hand.",
         f". This page cannot see your charts; {reads[0].lower() + reads[1:]}"),
        (", which is the personalized electional reading.", f", which this page cannot see. {reads}"),
        (", which is the personalized reading.", f", which this page cannot see. {reads}"),
        (" is the personalized electional reading.",
         f" is the one to look for. This page cannot see your chart; {reads[0].lower() + reads[1:]}"),
        ("<h2>Why this one wants the full reading</h2>", "<h2>Why a table only goes so far here</h2>"),
        (", which only a full electional reading, done by hand against both sides, can actually judge.",
         ", which no table, this one included, can judge."),
        ("<h2>Why this stays a reading, not a self-serve table</h2>",
         "<h2>Why this is a starting point, not a self-serve answer</h2>"),
        ("one that always wants the full traditional reading by hand:",
         "one that always wants the full traditional work done by hand:"),
        ("A table of monthly best days is a starting point for a conversation with your own reading, not a replacement for one,",
         "A table of monthly best days is a starting point for that work, not a replacement for it,"),
        ("one that always wants a full reading by hand, never a self-serve tool alone.",
         "one that always wants the full traditional work done by hand, never a self-serve tool alone."),
    ]
    for a, b in swaps:
        s = s.replace(a, b)

    m = re.search(r'<div class="cta">\s*<h2>(.*?)</h2>.*?</div>', s, re.S)
    if not m:
        raise SystemExit(f"{slug}: no CTA")
    if product == "synastry":
        p = ("Run your city and dates in the free timing finder for the exact windows. These dates "
             "rank the sky, which is the same for everyone; the Synastry Report reads how your two "
             "birth charts meet, written as one reading.")
    else:
        p = ("Run your city and dates in the free timing finder for the exact windows. These dates "
             "rank the sky, which is the same for everyone; the Year-Ahead Reading reads your next "
             "twelve months from your own birth chart, with the dates worth circling.")
    cta = (f'<div class="cta">\n    <h2>{m.group(1)}</h2>\n    <p>{p}</p>\n'
           f'    <a href="/electional" rel="noopener">Open the timing finder</a>\n'
           f'    <a class="secondary" href="{etsy(product, slug)}" rel="noopener">{name} on Etsy</a>\n'
           f'  </div>')
    return s[:m.start()] + cta + s[m.end():]


def specific_boilerplate(s, data):
    """Three stock sentences sat word for word on a dozen or more pages
    (2026-10-21, index plan). Say what they say about this election, with
    the method the rows were actually computed by. Idempotent: no new
    sentence contains the old one."""
    matter = MATTER.get(data["recipe"], data["label"].lower())
    year = data["year"]
    swaps = [
        ("By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses.",
         f"By Western electional astrology: every day of {year} scanned in 15-minute steps from 7 a.m. "
         f"to 9 p.m. Central with the Swiss Ephemeris in whole-sign houses, and each month's best "
         f"window for {matter} rated against five years of the same election."),
        ("These dates rank the sky, which is the same for everyone. The single",
         f"These dates rank the sky for {matter}, which is the same for everyone. The single"),
        ("Run your city and dates in the free timing finder for the exact windows.",
         f"Run your city and dates for {matter} in the free timing finder for the exact windows."),
    ]
    for a, b in swaps:
        s = s.replace(a, b)
    return s


def main():
    sky_all = json.loads((DATA / "sky.json").read_text())
    for slug in PAGES:
        f = ROOT / f"{slug}.html"
        s = f.read_text(encoding="utf-8")
        data_file = DATA / f"{slug}.json"
        if data_file.exists():
            data = json.loads(data_file.read_text())
            sky = sky_all[str(data["year"])]
            verb = verb_phrase(s, slug)
            s = set_table(s, data, sky, verb)
            for a, b in PROSE_FIXES.get(slug, []):
                s = s.replace(a, b)
            s = set_first_answer(s, summary(data, verb)[1])
            s = specific_boilerplate(s, data)
        else:
            s = add_anchors(s)
        s = promise(s, slug)
        left = [p for p in ("electional reading", "full reading") if p in s]
        if left:
            raise SystemExit(f"{slug}: still promises {left}")
        f.write_text(s, encoding="utf-8")
        print(f"{slug}: {'computed table' if data_file.exists() else 'anchors'}, promise, CTA")


if __name__ == "__main__":
    main()
