#!/usr/bin/env python3
"""Shared webtools share-card generator: renders ONE branded 1200x630 PNG
that every top-level webtools page uses as its og:image.

Method is the house standard (same as gen_sabian_cards.py and
brand-assets/gen_pins.py): write a plain HTML/CSS card to a scratch file,
screenshot it with headless Chrome at the exact pixel size, keep the PNG.

Output: webtools/og/webtools.png, served straight from the repo root like
every other static asset here. bin/apply_og_tags.py is what points the
pages at it.

WHY ONE SHARED CARD AND NOT ONE PER TOOL. The Sabian cards are per-degree
because there are 360 fixed pages whose whole value is the specific quote
on each one, and a shared card would say nothing. The tools are the
opposite: 44 pages that are all "The Twelve Rooms, free astrology tools,"
and their real per-page distinctness (a visitor's own Big 3, their
synastry score, their Saturn return) is PERSONALIZED and cannot be
pre-rendered at all -- it needs a dynamic @vercel/og route, which is a
separate piece of work. Until that exists, one strong shared card beats 44
near-identical ones, and beats today's situation, which is no card at all.

The procedural constellation layer from gen_sabian_cards.py is
deliberately NOT reused. That layer exists to stop 360 identically-laid-out
cards from looking like the same image; a single card has no such problem,
and a fixed-seed constellation would just be decoration competing with the
words. This card gets a quiet hand-placed star field instead, kept well
clear of the type, per brand.md's rule: if you notice the sparkle before
the words, there is too much sparkle.

Re-run after any change to the card design:
    python3 bin/gen_webtools_card.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE.parent
CARD_PATH = OUT_ROOT / "og" / "webtools.png"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CARD_W, CARD_H = 1200, 630

# The XII medallion, imported rather than copied so the mark can never
# drift between this card and the 360 Sabian cards.
sys.path.insert(0, str(HERE))
from gen_sabian_cards import MEDALLION  # noqa: E402

# Star field: (x, y, radius, opacity), hand-placed in the corners and
# margins so nothing lands within the centred text column. Fixed values,
# not random, so the card is byte-reproducible across runs.
STARS = [
    (118, 92, 1.6, 0.55), (168, 148, 1.1, 0.40), (92, 196, 2.0, 0.70),
    (212, 96, 1.3, 0.45), (146, 268, 1.2, 0.38), (86, 348, 1.5, 0.50),
    (176, 432, 1.1, 0.42), (108, 498, 1.9, 0.62), (232, 528, 1.3, 0.44),
    (1082, 94, 1.7, 0.58), (1024, 152, 1.2, 0.42), (1108, 208, 2.0, 0.68),
    (976, 104, 1.1, 0.38), (1052, 276, 1.3, 0.46), (1112, 356, 1.5, 0.52),
    (1010, 438, 1.2, 0.40), (1090, 502, 1.8, 0.60), (958, 534, 1.2, 0.43),
    (398, 78, 1.2, 0.40), (612, 66, 1.5, 0.48), (824, 82, 1.2, 0.38),
    (446, 566, 1.3, 0.44), (742, 572, 1.5, 0.50),
]

# Four-point gold sparkles, the brand's signature motif. Same reasoning:
# fixed positions, well outside the text column. (x, y, arm-length).
SPARKLES = [(138, 146, 9), (1064, 118, 8), (1096, 452, 10), (152, 470, 8)]


def star_svg():
    parts = []
    for x, y, r, o in STARS:
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e6cf96" opacity="{o}"/>'
        )
    for x, y, a in SPARKLES:
        # A four-point sparkle: two tapered strokes crossing at the centre.
        parts.append(
            f'<path d="M{x} {y - a} Q{x} {y} {x + a} {y} Q{x} {y} {x} {y + a} '
            f'Q{x} {y} {x - a} {y} Q{x} {y} {x} {y - a} Z" '
            f'fill="#d4b06a" opacity="0.75"/>'
        )
    return "\n".join(parts)


CARD_HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:{CARD_W}px; height:{CARD_H}px; overflow:hidden; position:relative;
  font-family:-apple-system,Helvetica,Arial,sans-serif;
  background: radial-gradient(120% 150% at 50% 18%, #1f2b4e 0%, #101830 100%); }}
* {{ box-sizing:border-box }}
.frame {{ position:absolute; inset:22px; border:2px solid #b18b45; pointer-events:none }}
.frame2 {{ position:absolute; inset:30px; border:1px solid #b18b45; opacity:.55; pointer-events:none }}
#art {{ position:absolute; inset:0; pointer-events:none }}
.wrap {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding: 76px 120px 110px; }}
.textcol {{ display:flex; flex-direction:column; align-items:center; }}
.medallion {{ margin-bottom: 10px; }}
.brand {{ font-family:Optima,Helvetica; letter-spacing:.32em; color:#e6cf96; font-size:16px;
  text-transform:uppercase; margin-bottom:22px; }}
.kicker {{ font-family:Optima,Helvetica; letter-spacing:.2em; color:#9aa5c2; font-size:13px;
  text-transform:uppercase; margin-bottom:16px; }}
.head {{ font-family:Didot,'Bodoni 72',Georgia,serif; color:#f3ecdd; font-size:56px;
  line-height:1.15; margin-bottom:22px; font-weight:600; }}
.rule {{ width:76px; height:1px; background:#b18b45; opacity:.8; margin:0 0 22px; }}
.snippet {{ font-family:Georgia,serif; font-style:italic; color:#c4cbe0; font-size:19px;
  line-height:1.55; max-width:720px; }}
.foot {{ position:absolute; left:0; right:0; bottom:44px; text-align:center; }}
.tag {{ font-family:Didot,'Bodoni 72',Georgia,serif; font-style:italic; color:#d4b06a; font-size:16px; }}
.dom {{ font-family:Optima,Helvetica; letter-spacing:.18em; color:#8b95b3; font-size:11.5px;
  text-transform:uppercase; margin-top:7px; }}
</style></head><body>
<svg id="art" width="{CARD_W}" height="{CARD_H}" xmlns="http://www.w3.org/2000/svg">
{star_svg()}
</svg>
<div class="frame"></div><div class="frame2"></div>
<div class="wrap">
  <div class="textcol">
    <div class="medallion">{MEDALLION}</div>
    <div class="brand">The Twelve Rooms</div>
    <div class="kicker">Free Astrology Tools</div>
    <div class="head">Read the sky yourself.</div>
    <div class="rule"></div>
    <div class="snippet">Natal charts, your Big 3, synastry, Saturn returns,
      planetary hours, moon phases, and elections for the days that matter.</div>
  </div>
</div>
<div class="foot">
  <div class="tag">The whole sky, written for you.</div>
  <div class="dom">thetwelverooms.com</div>
</div>
</body></html>"""


def main():
    CARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tr-webtools-card-") as scratch:
        html_path = Path(scratch) / "card.html"
        html_path.write_text(CARD_HTML)
        result = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu",
             f"--window-size={CARD_W},{CARD_H}",
             f"--screenshot={CARD_PATH}", f"file://{html_path}"],
            capture_output=True,
        )
    if result.returncode != 0 or not CARD_PATH.exists():
        print("failed to render the card:",
              result.stderr.decode(errors="replace")[:400], file=sys.stderr)
        return 1

    data = CARD_PATH.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("output is not a PNG", file=sys.stderr)
        return 1
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    if (w, h) != (CARD_W, CARD_H):
        print(f"card is {w}x{h}, expected {CARD_W}x{CARD_H}", file=sys.stderr)
        return 1

    rel = CARD_PATH.relative_to(OUT_ROOT)
    print(f"{rel}  {w}x{h}  {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
