#!/usr/bin/env python3
"""Generate Sabian symbol pages: the reusable template + generation approach
for The Twelve Rooms' Sabian symbol series.

RESUMABLE, PER-SIGN BUILD: each sign's 30 degree entries live in their own
file under bin/sabian_data/<slug>.py (see bin/sabian_data/SCHEMA.md for the
exact schema, canonical sign order, and how to add a sign). This script
never needs editing to add a sign: it discovers whatever sign files exist
in bin/sabian_data/, generates pages for every sign with 30 valid entries,
and renders every other sign as "coming soon" on the hub. That means many
signs can be written in parallel, in separate files, by separate people or
agents, and the build can be re-run at any point to pick up newly finished
signs without redoing already-generated ones.

Structure produced (URL, via Vercel cleanUrls):
  /sabian-symbols                    hub: all 12 signs, live ones link out, rest "coming soon"
  /sabian-symbols/<slug>              sign index: all 30 degrees
  /sabian-symbols/<slug>-1 .. <slug>-30   one page per degree

CORRECTNESS: the degree->symbol mapping (the `image` field in each sign's
ENTRIES) must be the canonical Jones/Wheeler 1925 Sabian symbol, one per
whole zodiac degree, numbered 1-30 within the sign, cross-verified against
multiple independent published sources (not generated or guessed). See
bin/sabian_data/SCHEMA.md and the per-sign data files for the full
discipline. Do NOT add a sign's data file without the same verification
discipline: fewer verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a woman rises
from the sea"), not a verbatim quote of Marc Edmund Jones' 1953 book or
Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation,
written fresh for this project; none of it is copied from Jones or
Rudhyar.

SHAREABLE-TOOL-OUTPUT GROWTH LOOP (proof staged Jul 24 2026, Aries only):
every degree page carries a ".tr-share" button (tools.js's initShare())
that shares the page's own URL, and og_tags() below points that page's
og:image/twitter:image at a pre-rendered 1200x630 branded card at
/og/sabian/<slug>-<n>.png, so the shared link unfurls as a Twelve Rooms
card in iMessage/Slack/Twitter/etc instead of a bare URL. og_tags() only
emits the image tags when that PNG actually exists on disk at generation
time, so wiring another sign's OG is zero-code: render its cards with
bin/gen_sabian_cards.py (same headless-Chrome-screenshot method as
brand-assets/gen_pins.py), then re-run this generator. See
gen_sabian_cards.py's own docstring for the scale path from these 360
FIXED cards to DYNAMIC og:image for personalized tool results (Big 3,
synastry, natal chart), which pre-rendering can't cover.

Run: python3 bin/gen_sabian_pages.py   (writes hub + sign index + all degree pages)
"""
import html
import importlib.util
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "sabian_data"

REQUIRED_ENTRY_FIELDS = {"degree", "image", "meaning", "colors", "reflection"}


def esc(s):
    return html.escape(str(s), quote=True)


# Canonical 12-sign zodiac order, names, and glyphs. This table is fixed
# astrology metadata (there are only ever 12 signs) and is NOT where a
# sign's Sabian symbol data lives -- that lives in bin/sabian_data/<slug>.py.
# Adding a new sign's data means adding bin/sabian_data/<slug>.py; this
# table does not need to change, and this file does not need to be edited
# to bring a sign live.
#
# GLYPH RENDERING: each glyph carries a trailing U+FE0E (VS15, text
# presentation selector). Without it, Apple platforms render these specific
# codepoints (U+2648-U+2653) via Apple Color Emoji as fixed multicolor
# (purple-ish) badges that ignore CSS color entirely, clashing with brand
# gold. VS15 forces the text-glyph presentation, which is a plain glyph the
# `.toolgrid .glyph` rule can color with `--gold` like every other icon in
# this toolgrid (see index.html's ✶ ✧ ☽ ☉ etc., none of which have this
# emoji-presentation problem). Do not remove the VS15 suffix.
CANONICAL_SIGNS = [
    {"name": "Aries", "slug": "aries", "glyph": "♈︎", "order": 1},
    {"name": "Taurus", "slug": "taurus", "glyph": "♉︎", "order": 2},
    {"name": "Gemini", "slug": "gemini", "glyph": "♊︎", "order": 3},
    {"name": "Cancer", "slug": "cancer", "glyph": "♋︎", "order": 4},
    {"name": "Leo", "slug": "leo", "glyph": "♌︎", "order": 5},
    {"name": "Virgo", "slug": "virgo", "glyph": "♍︎", "order": 6},
    {"name": "Libra", "slug": "libra", "glyph": "♎︎", "order": 7},
    {"name": "Scorpio", "slug": "scorpio", "glyph": "♏︎", "order": 8},
    {"name": "Sagittarius", "slug": "sagittarius", "glyph": "♐︎", "order": 9},
    {"name": "Capricorn", "slug": "capricorn", "glyph": "♑︎", "order": 10},
    {"name": "Aquarius", "slug": "aquarius", "glyph": "♒︎", "order": 11},
    {"name": "Pisces", "slug": "pisces", "glyph": "♓︎", "order": 12},
]


def _valid_entries(entries):
    """True if `entries` is a list of exactly 30 dicts, degrees 1-30 in
    order, each with all required fields. See bin/sabian_data/SCHEMA.md."""
    if not isinstance(entries, list) or len(entries) != 30:
        return False
    if [e.get("degree") for e in entries] != list(range(1, 31)):
        return False
    return all(REQUIRED_ENTRY_FIELDS.issubset(e.keys()) for e in entries)


def load_sign_data(slug):
    """Load bin/sabian_data/<slug>.py if present and valid.

    Returns the sign's ENTRIES list (30 valid dicts) if the file exists,
    imports cleanly, and passes validation; otherwise returns None and the
    sign renders as "coming soon" in the hub. A file that exists but fails
    validation prints a warning instead of failing the whole build, so an
    in-progress or broken sign file never blocks the other signs.
    """
    module_path = DATA_DIR / f"{slug}.py"
    if not module_path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"sabian_data.{slug}", module_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"warning: {module_path} failed to import ({e}); rendering '{slug}' as coming soon", file=sys.stderr)
        return None
    entries = getattr(module, "ENTRIES", None)
    if not _valid_entries(entries):
        print(f"warning: {module_path} does not have 30 valid ENTRIES; rendering '{slug}' as coming soon", file=sys.stderr)
        return None
    return entries


def build_signs():
    """Assemble the hub/nav sign list: canonical metadata plus each sign's
    entries (if its data file exists and is valid) and a `live` flag."""
    signs = []
    for meta in CANONICAL_SIGNS:
        entries = load_sign_data(meta["slug"])
        signs.append({**meta, "live": entries is not None, "entries": entries})
    return signs


def og_tags(sign_name, sign_slug, n, entry):
    """og:*/twitter:* meta tags for one degree page -- emitted ONLY when
    that degree's share-card PNG has actually been rendered (see
    bin/gen_sabian_cards.py). No card yet means no tags at all, so a sign
    with no cards renders byte-identical to before this feature (the proof
    is scoped to Aries; every other sign's OG is untouched on purpose).
    This is also the whole scaling mechanism: render another sign's cards
    with gen_sabian_cards.py, re-run this generator, and that sign's pages
    pick up full OG automatically -- no hand-editing here or per-page."""
    card_path = OUT / "og" / "sabian" / f"{sign_slug}-{n}.png"
    if not card_path.exists():
        return ""
    title = f"{sign_name} {n}° Sabian Symbol · The Twelve Rooms"
    desc = f"“{entry['image']}”"
    page_url = f"https://thetwelverooms.com/sabian-symbols/{sign_slug}-{n}"
    tags = [
        '<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{page_url}">',
        '<meta property="og:site_name" content="The Twelve Rooms">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
    ]
    img_url = f"https://thetwelverooms.com/og/sabian/{sign_slug}-{n}.png"
    img_alt = f"{sign_name} {n}°: {entry['image']}"
    tags += [
        f'<meta property="og:image" content="{img_url}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(img_alt)}">',
        f'<meta name="twitter:image" content="{img_url}">',
    ]
    return "\n".join(tags)


def degree_page(sign_name, sign_slug, entry, total):
    n = entry["degree"]
    slug = f"{sign_slug}-{n}"
    prev_link = (f'<a href="/sabian-symbols/{sign_slug}-{n-1}">← {sign_name} {n-1}°</a>'
                 if n > 1 else f'<a href="/sabian-symbols/{sign_slug}">← All of {sign_name}</a>')
    next_link = (f'<a href="/sabian-symbols/{sign_slug}-{n+1}">{sign_name} {n+1}° →</a>'
                 if n < total else f'<a href="/sabian-symbols">Explore other signs →</a>')
    note = entry.get("note")
    note_html = f'\n    <p class="sabian-note">{esc(note)}</p>' if note else ""
    og_html = og_tags(sign_name, sign_slug, n, entry)
    og_line = f"{og_html}\n" if og_html else ""
    title = f"{sign_name} {n}° Sabian Symbol: {esc(entry['image']).rstrip('.')} · The Twelve Rooms"
    desc = (f"The Sabian symbol for {sign_name} {n}°: {entry['image']} What it means, how it "
            f"colors a planet or point at this exact degree, and a reflection to sit with.")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols/{slug}">
{og_line}<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{sign_name} {n}° Sabian Symbol","author":{{"@type":"Organization","name":"The Twelve Rooms"}},"about":"Sabian symbol for {sign_name} degree {n}"}}
</script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div id="masthead"></div>
<main class="wrap" id="main-content" tabindex="-1">
  <p class="hint"><a href="/sabian-symbols">Sabian Symbols</a> &middot; <a href="/sabian-symbols/{sign_slug}">{sign_name}</a> &middot; Degree {n} of {total}</p>
  <h1>{sign_name} {n}&deg;</h1>
  <p class="lede">The traditional symbol for this degree, one of the 360 Sabian symbols first recorded in 1925: <strong>&ldquo;{esc(entry['image'])}&rdquo;</strong></p>

  <div class="card">
    <p class="kicker">THE SYMBOL</p>
    <p class="big" style="font-size:19px;line-height:1.45">&ldquo;{esc(entry['image'])}&rdquo;</p>
    <p class="hint">{sign_name} {n}&deg; &middot; Sabian symbols, devised 1925 (Marc Edmund Jones, clairvoyant Elsie Wheeler)</p>
    <p class="hint">Remember to round up: a planet or point at 9&deg;30&prime; takes the 10&deg; symbol, not the 9&deg; one.</p>
  </div>{note_html}

  <div class="tr-share">
    <button type="button" class="tr-share-btn" data-share-title="{esc(f'{sign_name} {n}° Sabian Symbol')}" data-share-text="{esc(entry['image'])}">Share this symbol</button>
    <p class="tr-share-note" aria-live="polite"></p>
  </div>

  <section class="prose">
    <h2>What this degree describes</h2>
    <p>{entry['meaning']}</p>
    <h2>When a planet or point falls here</h2>
    <p>{entry['colors']}</p>
  </section>

  <div class="card" style="text-align:center">
    <p class="hint" style="font-style:italic;font-size:14px">{entry['reflection']}</p>
  </div>

  <div class="cta">
    <h2>Find your own Sabian symbols</h2>
    <p>Your Sun, Moon, Ascendant, and every planet each sit at their own exact degree. Cast a free natal chart to find yours, or let a full reading trace what they mean together.</p>
    <a href="/natal-chart">Cast your free chart</a>
  </div>

  <p class="hint" style="display:flex;justify-content:space-between;gap:12px;margin-top:18px">
    <span>{prev_link}</span><span>{next_link}</span>
  </p>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols" / f"{slug}.html").write_text(page)
    return slug


def sign_index_page(sign_name, sign_slug, entries):
    cards = "\n".join(
        f'    <a class="almanac-card" href="/sabian-symbols/{sign_slug}-{e["degree"]}">'
        f'<h3>{sign_name} {e["degree"]}&deg;</h3><p>{esc(e["image"])}</p></a>'
        for e in entries)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{sign_name} Sabian Symbols: All 30 Degrees &middot; The Twelve Rooms</title>
<meta name="description" content="Every Sabian symbol in {sign_name}, degree by degree: the traditional 1925 image for each of the sign's 30 degrees, with an original Twelve Rooms meaning for each.">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols/{sign_slug}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div id="masthead"></div>
<main class="wrap" id="main-content" tabindex="-1">
  <p class="hint"><a href="/sabian-symbols">Sabian Symbols</a> &middot; {sign_name}</p>
  <h1>{sign_name}: all 30 Sabian symbols</h1>
  <p class="lede">Every whole degree of {sign_name} has its own Sabian symbol, a small traditional picture first recorded in 1925. Find the exact degree of your Sun, Moon, Ascendant, or any planet in {sign_name}, and read what that degree adds to it.</p>

  <div class="almanac-grid">
{cards}
  </div>

  <section class="prose">
    <h2>Don't know your exact degree?</h2>
    <p>A Sabian symbol is specific to the whole degree a planet or point occupies, so you need the exact placement, not just the sign, to find yours. Cast a free <a href="/natal-chart">natal chart</a> to see every planet's precise degree, then look up its Sabian symbol here.</p>
  </section>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols" / f"{sign_slug}.html").write_text(page)


def hub_page(signs):
    cards = []
    live_signs = [s for s in signs if s["live"]]
    for s in signs:
        if s["live"]:
            cards.append(
                f'    <a href="/sabian-symbols/{s["slug"]}"><span class="glyph" aria-hidden="true">{s["glyph"]}</span>'
                f'<h2>{s["name"]}</h2><p>All 30 degrees, symbol and meaning.</p></a>')
        else:
            cards.append(
                f'    <div class="soon"><span class="glyph" aria-hidden="true">{s["glyph"]}</span>'
                f'<h2>{s["name"]}</h2><p>30 degrees, in progress.</p><span class="tag gold">Coming soon</span></div>')
    grid = "\n".join(cards)

    # Copy that names the live signs and counts the rest -- kept dynamic so
    # this page never needs a manual edit as more signs come live.
    live_names = [s["name"] for s in live_signs]
    remaining = len(signs) - len(live_signs)
    example_sign = live_names[0] if live_names else "Aries"

    def _join_names(names):
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return f"{names[0]} and {names[1]}"
        return ", ".join(names[:-1]) + f", and {names[-1]}"

    if live_names:
        names_joined = _join_names(live_names)
        is_are = "is" if len(live_names) == 1 else "are"
        meta_desc = (f"The Sabian symbols: a traditional picture for each of the 360 degrees of the "
                     f"zodiac, devised in 1925. {names_joined} {is_are} live, all 30 degrees each; "
                     f"the remaining {remaining} signs are coming soon.")
        lede_status = f"{names_joined} {'is' if len(live_names) == 1 else 'are'} complete, all 30 degrees each; the rest of the wheel is being written to the same standard."
        faq_answer = (f"Not yet. {names_joined} {is_are} live and complete, all 30 degrees each. "
                      f"The remaining {remaining} signs are being written to the same standard and will publish as they're finished.")
    else:
        meta_desc = "The Sabian symbols: a traditional picture for each of the 360 degrees of the zodiac, devised in 1925. All 12 signs are coming soon."
        lede_status = "All 12 signs are being written to the same standard and will publish as they're finished."
        faq_answer = "Not yet. All 12 signs are being written to the same standard and will publish as they're finished."

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sabian Symbols: The Meaning of Every Zodiac Degree &middot; The Twelve Rooms</title>
<meta name="description" content="{esc(meta_desc)}">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"What is a Sabian symbol?","acceptedAnswer":{{"@type":"Answer","text":"A Sabian symbol is a short traditional picture assigned to each of the 360 whole degrees of the zodiac, one degree at a time. They were received by clairvoyant Elsie Wheeler and recorded by astrologer Marc Edmund Jones in 1925. Astrologers use them to add texture to a planet or point's exact degree, beyond its sign alone."}}}},
{{"@type":"Question","name":"How do I find my Sabian symbol?","acceptedAnswer":{{"@type":"Answer","text":"You need the exact degree of a planet or point, not just its sign, since each of the 30 degrees in a sign has its own symbol. Cast a free natal chart to see every planet's precise degree, then look it up in the sign's list here."}}}},
{{"@type":"Question","name":"Are all 360 Sabian symbols here?","acceptedAnswer":{{"@type":"Answer","text":{json.dumps(faq_answer)}}}}}
]}}
</script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div id="masthead"></div>
<main class="wrap" id="main-content" tabindex="-1">
  <h1>The Sabian symbols</h1>
  <p class="lede">A short traditional picture for each of the 360 whole degrees of the zodiac, one per degree, first recorded in 1925. Every planet and point in a chart sits at one exact degree; its Sabian symbol adds a layer of meaning beyond the sign alone. {lede_status}</p>

  <div class="toolgrid">
{grid}
  </div>

  <div class="card">
    <p class="kicker">HOW TO FIND YOUR DEGREE</p>
    <p class="hint" style="font-size:14px;line-height:1.6;color:#33384a">Sabian symbols belong to whole degrees, and the convention is to round up: a planet or point at 9&deg;30&prime; {example_sign} takes the <strong>{example_sign} 10&deg;</strong> symbol, not the 9&deg; one. So find your planet's exact degree, round up to the next whole degree, and look that number up in the sign's list below.</p>
  </div>

  <section class="prose">
    <h2>Where the Sabian symbols come from</h2>
    <p>In 1925, astrologer Marc Edmund Jones worked with clairvoyant Elsie Wheeler in Balboa Park, San Diego, showing her blank flash-cards and recording the image each one brought to mind, one degree at a time, until all 360 were captured. The result, later published by Jones in 1953 and given a literary expansion by Dane Rudhyar in 1973, became one of the most widely used systems for reading the exact degree of a planet or point, not just its sign.</p>
    <h2>How to use one</h2>
    <p>Sabian symbols are precise: they describe a single whole degree, so the symbol for 14&deg; is not the symbol for 15&deg;. You need an exact birth time and a cast chart to know which degree your Sun, Moon, Ascendant, or any planet actually occupies. Once you have that degree, the symbol adds color and image to what the sign and house already tell you, a closer read of one specific point in the chart.</p>
  </section>

  <div class="cta">
    <h2>Find your own exact degrees</h2>
    <p>Cast a free natal chart to see every planet's precise degree, then explore what each one's Sabian symbol adds. For the whole chart read as one story, The Twelve Rooms writes it by hand.</p>
    <a href="/natal-chart">Cast your free chart</a>
  </div>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols.html").write_text(page)


def main():
    (OUT / "sabian-symbols").mkdir(exist_ok=True)
    signs = build_signs()
    total_degree_pages = 0
    live_signs = 0
    for s in signs:
        if not s["live"]:
            continue
        for entry in s["entries"]:
            degree_page(s["name"], s["slug"], entry, len(s["entries"]))
        sign_index_page(s["name"], s["slug"], s["entries"])
        total_degree_pages += len(s["entries"])
        live_signs += 1
    hub_page(signs)
    print(f"wrote {total_degree_pages} degree pages across {live_signs} live sign(s), "
          f"{live_signs} sign index page(s), 1 hub page")


if __name__ == "__main__":
    main()
