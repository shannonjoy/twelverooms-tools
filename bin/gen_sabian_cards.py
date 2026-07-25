#!/usr/bin/env python3
"""Sabian share-card generator: renders a branded 1200x630 PNG per Sabian
degree, for the "shareable tool output" growth loop (see
gen_sabian_pages.py's docstring for how these wire into each degree page's
og:image). Same method as brand-assets/gen_pins.py: write a plain HTML/CSS
card to a scratch file, screenshot it with headless Chrome at the exact
pixel size, keep the PNG.

Output: webtools/og/sabian/<slug>-<n>.png  (e.g. og/sabian/aries-1.png),
served directly from the repo root like every other static asset here --
no build step, no function, nothing else has to know these exist beyond
gen_sabian_pages.py checking whether the file is on disk.

PROOF SCOPE: this run renders only Aries's 30 degrees, to prove the
mechanism (design, render pipeline, OG wiring, share button) before
spending render time on the other 330 degrees. To extend: add more signs
to SIGNS_TO_RENDER below (any slug with a valid bin/sabian_data/<slug>.py,
same list gen_sabian_pages.py already discovers), re-run this script, then
re-run gen_sabian_pages.py. No template change needed -- the card is
already generic over sign name / degree / quote / reflection.

SCALE PATH -- FIXED CONTENT (this method) VS PERSONALIZED CONTENT (needs
something else):
  The 360 Sabian degrees are FIXED: the same card renders for every
  visitor who lands on a given degree, so pre-rendering once (this
  headless-Chrome method, run ahead of time, committed as static files) is
  correct and cheap -- render once, or whenever the design changes, done.

  PERSONALIZED tool results -- a visitor's own Big 3, their synastry
  score, their Saturn return date, their natal chart -- can NOT be
  pre-rendered this way: there is one correct card per visitor, computed
  from their birth data at request time, and there's no way to run
  headless Chrome for every possible input in advance. Those need a
  DYNAMIC og:image: a URL the social crawler requests at share time that
  computes and rasterizes the card on the fly, e.g.
    <meta property="og:image" content="/api/og/big-3?sun=Leo&moon=Pisces&asc=Gemini">
  The standard way to build that on Vercel is @vercel/og: a JS/Satori edge
  function that takes an HTML/CSS-like React tree and rasterizes straight
  to PNG at request time, no headless browser needed at the edge (fast
  enough for a crawler's fetch timeout, unlike spinning up Chrome per
  request). That function gets built ONCE -- one edge route, reusing this
  same navy/gold card design system -- and every personalized tool (Big 3,
  synastry, saturn-return calculator, natal chart) then points its own
  og:image at it with its own query params. Not built yet; this proof
  covers only the fixed-content (Sabian) half of the loop end to end so
  the mechanism is proven before that second piece gets built.

Run: python3 bin/gen_sabian_cards.py   (writes webtools/og/sabian/*.png)
"""
import html
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # webtools/bin
OUT_ROOT = HERE.parent                            # webtools/
DATA_DIR = HERE / "sabian_data"
CARD_DIR = OUT_ROOT / "og" / "sabian"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CARD_W, CARD_H = 1200, 630

# PROOF: Aries only. Add more {"name": ..., "slug": ...} entries (matching
# bin/sabian_data/<slug>.py files) to render the rest of the wheel -- see
# CANONICAL_SIGNS in gen_sabian_pages.py for the full 12-sign list/order.
SIGNS_TO_RENDER = [
    {"name": "Aries", "slug": "aries"},
]


def esc(s):
    return html.escape(str(s), quote=True)


def load_entries(slug):
    module_path = DATA_DIR / f"{slug}.py"
    spec = importlib.util.spec_from_file_location(f"sabian_data.{slug}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ENTRIES


# Small gold 4-point sparkle + star-dot scatter, brand law: opacity 0.45-0.9,
# always clear of type. Positions chosen for the 1200x630 canvas's corners,
# clear of the centered text column.
SPARK = """<svg style="position:absolute;inset:0" width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
<g fill="#d4b06a">
<path transform="translate(90,80) scale(1.2)" d="M0 -6 L1.2 -1.2 L6 0 L1.2 1.2 L0 6 L-1.2 1.2 L-6 0 L-1.2 -1.2 Z" opacity="0.85"/>
<path transform="translate(1110,72) scale(1.0)" d="M0 -6 L1.2 -1.2 L6 0 L1.2 1.2 L0 6 L-1.2 1.2 L-6 0 L-1.2 -1.2 Z" opacity="0.7"/>
<path transform="translate(1128,558) scale(0.85)" d="M0 -6 L1.2 -1.2 L6 0 L1.2 1.2 L0 6 L-1.2 1.2 L-6 0 L-1.2 -1.2 Z" opacity="0.6"/>
<path transform="translate(72,568) scale(0.7)" d="M0 -6 L1.2 -1.2 L6 0 L1.2 1.2 L0 6 L-1.2 1.2 L-6 0 L-1.2 -1.2 Z" opacity="0.55"/>
<circle cx="150" cy="150" r="2" opacity="0.55"/><circle cx="1050" cy="140" r="1.6" opacity="0.5"/>
<circle cx="60" cy="320" r="1.6" opacity="0.45"/><circle cx="1145" cy="330" r="1.8" opacity="0.5"/>
<circle cx="180" cy="500" r="1.5" opacity="0.5"/><circle cx="1010" cy="510" r="1.4" opacity="0.45"/>
</g></svg>"""

# The XII medallion, same mark as tools.js's masthead, scaled down for a
# small top-of-card lockup -- reads at thumbnail size where the full
# letterspaced wordmark alone would not.
MEDALLION = """<svg width="46" height="46" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs><linearGradient id="tr-gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#d4b06a"/><stop offset="0.5" stop-color="#b18b45"/><stop offset="1" stop-color="#96742f"/>
  </linearGradient></defs>
  <circle cx="75" cy="75" r="62" fill="none" stroke="url(#tr-gold)" stroke-width="1.6"/>
  <circle cx="75" cy="75" r="58" fill="none" stroke="url(#tr-gold)" stroke-width="0.5"/>
  <text x="75" y="85" text-anchor="middle" font-family="Didot,'Bodoni 72',Georgia,serif" font-size="27" fill="#e6cf96" letter-spacing="1">XII</text>
</svg>"""


def card_html(sign_name, n, entry):
    quote = entry["image"].rstrip(".")
    reflection = entry["reflection"]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:{CARD_W}px; height:{CARD_H}px; overflow:hidden; position:relative;
  font-family:-apple-system,Helvetica,Arial,sans-serif;
  background: radial-gradient(120% 150% at 50% 18%, #1f2b4e 0%, #101830 100%); }}
* {{ box-sizing:border-box }}
.frame {{ position:absolute; inset:22px; border:2px solid #b18b45; pointer-events:none }}
.frame2 {{ position:absolute; inset:30px; border:1px solid #b18b45; opacity:.55; pointer-events:none }}
.wrap {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding: 76px 120px 96px; }}
.medallion {{ margin-bottom: 10px; }}
.brand {{ font-family:Optima,Helvetica; letter-spacing:.32em; color:#e6cf96; font-size:16px;
  text-transform:uppercase; margin-bottom:20px; }}
.kicker {{ font-family:Optima,Helvetica; letter-spacing:.2em; color:#9aa5c2; font-size:13px;
  text-transform:uppercase; margin-bottom:12px; }}
.degree {{ font-family:Didot,'Bodoni 72',Georgia,serif; color:#f3ecdd; font-size:42px;
  margin-bottom:18px; font-weight:600; }}
.quote {{ font-family:Didot,'Bodoni 72',Georgia,serif; font-style:italic; color:#d4b06a;
  font-size:32px; line-height:1.4; margin-bottom:20px; max-width: 900px; }}
.snippet {{ font-family:Georgia,serif; font-style:italic; color:#c4cbe0; font-size:16px;
  line-height:1.5; max-width:640px; }}
.foot {{ position:absolute; left:0; right:0; bottom:40px; text-align:center; }}
.tag {{ font-family:Didot,'Bodoni 72',Georgia,serif; font-style:italic; color:#d4b06a; font-size:15px; }}
.dom {{ font-family:Optima,Helvetica; letter-spacing:.18em; color:#8b95b3; font-size:11.5px;
  text-transform:uppercase; margin-top:6px; }}
</style></head><body>
<div class="frame"></div><div class="frame2"></div>
{SPARK}
<div class="wrap">
  <div class="medallion">{MEDALLION}</div>
  <div class="brand">The Twelve Rooms</div>
  <div class="kicker">Sabian Symbol</div>
  <div class="degree">{esc(sign_name)} {n}&deg;</div>
  <div class="quote">&ldquo;{esc(quote)}&rdquo;</div>
  <div class="snippet">{esc(reflection)}</div>
</div>
<div class="foot">
  <div class="tag">The whole sky, written for you.</div>
  <div class="dom">thetwelverooms.com</div>
</div>
</body></html>"""


def render_sign(sign_name, slug, entries, scratch_dir):
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for entry in entries:
        n = entry["degree"]
        html_path = scratch_dir / f"{slug}-{n}.html"
        png_path = CARD_DIR / f"{slug}-{n}.png"
        html_path.write_text(card_html(sign_name, n, entry))
        result = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", f"--window-size={CARD_W},{CARD_H}",
             f"--screenshot={png_path}", f"file://{html_path}"],
            capture_output=True,
        )
        if result.returncode != 0 or not png_path.exists():
            print(f"warning: failed to render {slug}-{n}: {result.stderr.decode(errors='replace')[:300]}",
                  file=sys.stderr)
            continue
        written.append(png_path)
    return written


def main():
    total = 0
    with tempfile.TemporaryDirectory(prefix="tr-sabian-cards-") as scratch:
        scratch_dir = Path(scratch)
        for meta in SIGNS_TO_RENDER:
            entries = load_entries(meta["slug"])
            written = render_sign(meta["name"], meta["slug"], entries, scratch_dir)
            total += len(written)
            print(f"{meta['name']}: {len(written)}/{len(entries)} cards -> {CARD_DIR}/")
    print(f"wrote {total} share-card PNG(s) total")


if __name__ == "__main__":
    main()
