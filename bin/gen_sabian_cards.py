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
already generic over sign name / degree / quote / reflection / art.

CELESTIAL ART LAYER (added to fix "every card looks the same"): each card
gets its own procedurally-generated antique-star-map constellation instead
of a static sparkle frame. It is pure generative SVG built by inline JS
that runs synchronously while headless Chrome renders the page (no
network, no images, no AI generation) -- see `ART_JS` below for the full
algorithm. Key properties:

  - DETERMINISTIC: seeded by `seed = sign_order*30 + degree` (e.g. Aries
    14 deg = 1*30+14 = 44) through a small mulberry32 PRNG, so a given
    degree always renders the same constellation and the whole 360-card
    set stays reproducible. No Math.random anywhere in ART_JS.
  - MEASURES THE ACTUAL TEXT, not a guessed box: it reads the real
    getBoundingClientRect() of the .wrap text column at render time and
    keeps every star and line at least 30px outside it (plus a segment
    vs. rect check on every connecting line), so varying quote/reflection
    lengths across 360 different degrees can never clutter the words --
    the composition adapts to the content instead of assuming a fixed
    text height.
  - FOUR COMPOSITION FAMILIES (halo / crown / twin / cascade), chosen by
    the seed, so cards don't all resolve to "dots around the border" --
    each is a genuinely different silhouette (full ring, top arc, two
    corner clusters, one falling column).
  - PER-SIGN MOTIF: a large, very faint (opacity ~0.06) Didot rendering of
    the sign's own glyph sits behind the constellation as a watermark, and
    each of the 4 classical elements (fire/earth/air/water, derived from
    the sign's 1-12 order) gets one quiet accent color reused from the
    already-locked brand.md per-product accent palette (marigold / sage /
    slate / lapis) -- never a new hue, just tinting the focal-star glow
    and one thin decorative corner arc.

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
  same navy/gold card design system (constellation algorithm included) --
  and every personalized tool (Big 3, synastry, saturn-return calculator,
  natal chart) then points its own og:image at it with its own query
  params. Not built yet; this proof covers only the fixed-content (Sabian)
  half of the loop end to end so the mechanism is proven before that
  second piece gets built.

TO SCALE TO ALL 360: add the remaining 11 signs to SIGNS_TO_RENDER below
(same {"slug": ...} entries gen_sabian_pages.py's CANONICAL_SIGNS already
lists) and re-run `python3 bin/gen_sabian_cards.py`. Nothing else changes
-- the art algorithm is already generic over sign order/glyph/degree, and
the seed space (order*30+degree) already covers all 360 degrees uniquely.

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

# The full wheel, in zodiac order. This was Aries-only through Aug 6 2026
# while the mechanism was being proved (design, render pipeline, OG wiring,
# share button); all 360 degree PAGES already existed, but the other 11
# signs had no card, so 330 of the 360 pages unfurled as a bare URL. The
# proof held, so the list is now the whole wheel. Each slug must match a
# bin/sabian_data/<slug>.py file, whose SIGN dict supplies name/order/glyph
# -- same list and order as CANONICAL_SIGNS in gen_sabian_pages.py.
SIGNS_TO_RENDER = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

# Classical element by 1-12 zodiac order, cycling fire/earth/air/water.
ELEMENT_BY_ORDER_MOD = {1: "fire", 2: "earth", 3: "air", 0: "water"}

# Reuses brand.md's already-locked per-product accent hexes (Accent system,
# Jul 20 2026) instead of inventing new colors -- keeps the element tint
# inside the approved palette so the set stays one cohesive shop.
ACCENT_BY_ELEMENT = {
    "fire": "#c98a2e",   # marigold
    "earth": "#5c7a5e",  # sage
    "air": "#8ea0bd",    # slate
    "water": "#3f5488",  # lapis
}


def esc(s):
    return html.escape(str(s), quote=True)


def load_module(slug):
    module_path = DATA_DIR / f"{slug}.py"
    spec = importlib.util.spec_from_file_location(f"sabian_data.{slug}", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

# Procedural celestial-art layer. Pure inline JS, no external assets, no
# Math.random -- everything flows from the mulberry32 PRNG seeded by
# __SEED__ so a given degree always reproduces the same constellation.
# Placeholders (__SEED__, __GLYPH__, __ACCENT__) are substituted via plain
# string.replace in card_html() -- avoids f-string brace-escaping hell for
# a script this size.
ART_JS = """
(function () {
  var W = 1200, H = 630;
  var SEED = __SEED__;
  var GLYPH = "__GLYPH__";
  var ACCENT = "__ACCENT__";
  var svgNS = "http://www.w3.org/2000/svg";

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rand = mulberry32(SEED);

  var art = document.getElementById("art");
  // IMPORTANT: measure the shrink-wrapped .textcol (the actual visible
  // content), never .wrap itself -- .wrap is `position:absolute; inset:0`
  // so ITS bounding rect is the full 1200x630 canvas, which would make
  // every point "in the text" and silently render zero stars.
  var pad = 26;
  var rects = [];
  ["textcol", "foot"].forEach(function (cls) {
    var el = document.querySelector("." + cls);
    if (!el) return;
    var r = el.getBoundingClientRect();
    rects.push({ x1: r.left - pad, y1: r.top - pad, x2: r.right + pad, y2: r.bottom + pad });
  });
  // avoid.* mirrors the tightest content rect (used by the sampling
  // regions below); inAvoid/segCrossesAvoid check against ALL rects.
  var avoid = rects[0] || { x1: W / 2 - 10, y1: H / 2 - 10, x2: W / 2 + 10, y2: H / 2 + 10 };
  var margin = 38;

  function inAvoid(x, y) {
    for (var i = 0; i < rects.length; i++) {
      var r = rects[i];
      if (x > r.x1 && x < r.x2 && y > r.y1 && y < r.y2) return true;
    }
    return false;
  }
  function segCrossesAvoid(x1, y1, x2, y2) {
    for (var t = 0; t <= 1; t += 0.06) {
      var x = x1 + (x2 - x1) * t, y = y1 + (y2 - y1) * t;
      if (inAvoid(x, y)) return true;
    }
    return false;
  }

  // Four composition families -- each returns a candidate [x, y] within
  // its own silhouette. Rejection sampling below still enforces the text
  // keep-out and the margin, so a family that fits a card poorly just
  // yields fewer, sparser stars rather than ever crossing the words.
  var families = ["halo", "crown", "twin", "cascade"];
  var comp = families[Math.floor(rand() * families.length)];

  function sample() {
    var x, y;
    if (comp === "crown") {
      // Gentle downward-opening arc (high at center, lower near the
      // edges) so the top band reads as one deliberate crown shape
      // instead of a near-straight scatter of points.
      var topBand = Math.max(avoid.y1 - margin, margin + 60);
      var bandH = topBand - margin;
      var t = rand();
      x = margin + t * (W - margin * 2);
      var envelope = Math.sin(t * Math.PI); // 1 at center, 0 at edges
      y = margin + bandH * (1 - envelope) * 0.7 + rand() * bandH * 0.3;
    } else if (comp === "twin") {
      var leftBox = avoid.x1 - margin, rightBox = W - margin - avoid.x2;
      var goLeft = rand() < 0.5;
      if (goLeft && leftBox > 40) {
        x = margin + rand() * leftBox;
      } else if (rightBox > 40) {
        x = avoid.x2 + rand() * rightBox;
      } else {
        x = margin + rand() * (W - margin * 2);
      }
      var topBox = avoid.y1 - margin, botBox = H - margin - avoid.y2;
      var goTop = rand() < 0.5;
      if (goTop && topBox > 40) {
        y = margin + rand() * topBox;
      } else if (botBox > 40) {
        y = avoid.y2 + rand() * botBox;
      } else {
        y = margin + rand() * (H - margin * 2);
      }
    } else if (comp === "cascade") {
      var leftW = avoid.x1 - margin, rightW = W - margin - avoid.x2;
      var side = rightW > leftW ? "r" : "l";
      if (side === "l" && leftW > 30) {
        x = margin + rand() * leftW;
      } else if (rightW > 30) {
        x = avoid.x2 + rand() * rightW;
      } else {
        x = margin + rand() * (W - margin * 2);
      }
      y = margin + rand() * (H - margin * 2);
    } else {
      // halo: anywhere in the card; the avoid-rect rejection naturally
      // leaves only the border ring available.
      x = margin + rand() * (W - margin * 2);
      y = margin + rand() * (H - margin * 2);
    }
    return [x, y];
  }

  var n = 7 + Math.floor(rand() * 6); // 7-12 stars
  var pts = [];
  var tries = 0;
  while (pts.length < n && tries < 500) {
    tries++;
    var p = sample();
    var x = p[0], y = p[1];
    if (inAvoid(x, y)) continue;
    if (x < margin || x > W - margin || y < margin || y > H - margin) continue;
    var tooClose = false;
    for (var i = 0; i < pts.length; i++) {
      var dx = pts[i].x - x, dy = pts[i].y - y;
      if (Math.sqrt(dx * dx + dy * dy) < 46) { tooClose = true; break; }
    }
    if (tooClose) continue;
    pts.push({ x: x, y: y });
  }

  if (pts.length >= 3) {
    var cx = 0, cy = 0;
    for (i = 0; i < pts.length; i++) { cx += pts[i].x; cy += pts[i].y; }
    cx /= pts.length; cy /= pts.length;
    pts.sort(function (a, b) {
      return Math.atan2(a.y - cy, a.x - cx) - Math.atan2(b.y - cy, b.x - cx);
    });
  }

  var g = document.createElementNS(svgNS, "g");
  var closeLoop = comp === "halo" || comp === "twin";
  var segCount = closeLoop ? pts.length : Math.max(pts.length - 1, 0);
  for (i = 0; i < segCount; i++) {
    var a = pts[i], b = pts[(i + 1) % pts.length];
    if (segCrossesAvoid(a.x, a.y, b.x, b.y)) continue;
    var line = document.createElementNS(svgNS, "line");
    line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
    line.setAttribute("stroke", "#c9a86a");
    line.setAttribute("stroke-width", (0.55 + rand() * 0.35).toFixed(2));
    line.setAttribute("opacity", (0.2 + rand() * 0.16).toFixed(2));
    g.appendChild(line);
  }

  var nFocal = pts.length > 4 ? 1 + Math.floor(rand() * 2) : 1;
  var focalIdx = {};
  var guard = 0;
  while (Object.keys(focalIdx).length < Math.min(nFocal, pts.length) && guard < 50) {
    focalIdx[Math.floor(rand() * pts.length)] = true;
    guard++;
  }

  pts.forEach(function (p, idx) {
    var focal = !!focalIdx[idx];
    var r = focal ? 3.0 + rand() * 1.4 : 1.3 + rand() * 1.3;
    if (focal) {
      var glow = document.createElementNS(svgNS, "circle");
      glow.setAttribute("cx", p.x); glow.setAttribute("cy", p.y);
      glow.setAttribute("r", (r * 3.6).toFixed(1));
      glow.setAttribute("fill", ACCENT);
      glow.setAttribute("opacity", "0.11");
      g.appendChild(glow);
    }
    var c = document.createElementNS(svgNS, "circle");
    c.setAttribute("cx", p.x); c.setAttribute("cy", p.y);
    c.setAttribute("r", r.toFixed(2));
    c.setAttribute("fill", focal ? "#f3ecdd" : "#d4b06a");
    c.setAttribute("opacity", (focal ? 0.92 : 0.5 + rand() * 0.35).toFixed(2));
    g.appendChild(c);
  });
  art.appendChild(g);

  // Per-sign glyph watermark: large, very faint, behind everything.
  var corners = [
    { x: 150, y: 130, r: -6 }, { x: W - 150, y: 130, r: 6 },
    { x: 150, y: H - 120, r: 5 }, { x: W - 150, y: H - 120, r: -5 }
  ];
  var corner = corners[Math.floor(rand() * corners.length)];
  var size = 260 + rand() * 130;
  var rot = corner.r + (rand() * 4 - 2);
  var wm = document.createElementNS(svgNS, "text");
  wm.setAttribute("x", corner.x); wm.setAttribute("y", corner.y);
  wm.setAttribute("text-anchor", "middle");
  wm.setAttribute("font-family", "Didot,'Bodoni 72',Georgia,serif");
  wm.setAttribute("font-size", size.toFixed(0));
  wm.setAttribute("fill", "#e6cf96");
  wm.setAttribute("opacity", "0.06");
  wm.setAttribute("transform", "rotate(" + rot.toFixed(1) + " " + corner.x + " " + corner.y + ")");
  wm.textContent = GLYPH;
  art.insertBefore(wm, art.firstChild);

  // One quiet accent-colored corner arc -- the "signature accent" per
  // brand.md's Accent system, applied here per element instead of per
  // product: a small surface only, never a repaint of the core palette.
  var arcCorners = [
    { cx: 46, cy: 46, sx: 1, sy: 1 }, { cx: W - 46, cy: 46, sx: -1, sy: 1 },
    { cx: 46, cy: H - 46, sx: 1, sy: -1 }, { cx: W - 46, cy: H - 46, sx: -1, sy: -1 }
  ];
  var ac = arcCorners[Math.floor(rand() * arcCorners.length)];
  var ar = 70 + rand() * 55;
  var ax1 = ac.cx + ac.sx * ar, ay1 = ac.cy;
  var ax2 = ac.cx, ay2 = ac.cy + ac.sy * ar;
  var sweep = (ac.sx * ac.sy) > 0 ? 1 : 0;
  var arcPath = document.createElementNS(svgNS, "path");
  arcPath.setAttribute("d", "M " + ax1.toFixed(1) + "," + ay1.toFixed(1) +
    " A " + ar.toFixed(1) + "," + ar.toFixed(1) + " 0 0 " + sweep + " " +
    ax2.toFixed(1) + "," + ay2.toFixed(1));
  arcPath.setAttribute("fill", "none");
  arcPath.setAttribute("stroke", ACCENT);
  arcPath.setAttribute("stroke-width", "1.1");
  arcPath.setAttribute("opacity", "0.3");
  art.appendChild(arcPath);
})();
"""


def card_html(sign_meta, n, entry):
    quote = entry["image"].rstrip(".")
    reflection = entry["reflection"]
    order = sign_meta["order"]
    seed = order * 30 + n
    # Keep the VS15 (text-presentation selector) intact -- stripping it
    # made Chrome fall back to Apple Color Emoji's fixed multicolor glyph
    # (the purple blob artifact), same rationale as gen_sabian_pages.py.
    glyph = sign_meta["glyph"]
    element = ELEMENT_BY_ORDER_MOD[order % 4]
    accent = ACCENT_BY_ELEMENT[element]
    art_js = (
        ART_JS.replace("__SEED__", str(seed))
        .replace("__GLYPH__", glyph)
        .replace("__ACCENT__", accent)
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; width:{CARD_W}px; height:{CARD_H}px; overflow:hidden; position:relative;
  font-family:-apple-system,Helvetica,Arial,sans-serif;
  background: radial-gradient(120% 150% at 50% 18%, #1f2b4e 0%, #101830 100%); }}
* {{ box-sizing:border-box }}
.frame {{ position:absolute; inset:22px; border:2px solid #b18b45; pointer-events:none }}
.frame2 {{ position:absolute; inset:30px; border:1px solid #b18b45; opacity:.55; pointer-events:none }}
#art {{ position:absolute; inset:0; pointer-events:none }}
.wrap {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; text-align:center; padding: 76px 120px 96px; }}
.textcol {{ display:flex; flex-direction:column; align-items:center; }}
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
<svg id="art" width="{CARD_W}" height="{CARD_H}" xmlns="http://www.w3.org/2000/svg"></svg>
<div class="frame"></div><div class="frame2"></div>
<div class="wrap">
  <div class="textcol">
    <div class="medallion">{MEDALLION}</div>
    <div class="brand">The Twelve Rooms</div>
    <div class="kicker">Sabian Symbol</div>
    <div class="degree">{esc(sign_meta["name"])} {n}&deg;</div>
    <div class="quote">&ldquo;{esc(quote)}&rdquo;</div>
    <div class="snippet">{esc(reflection)}</div>
  </div>
</div>
<div class="foot">
  <div class="tag">The whole sky, written for you.</div>
  <div class="dom">thetwelverooms.com</div>
</div>
<script>{art_js}</script>
</body></html>"""


def render_sign(sign_meta, entries, scratch_dir):
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    slug = sign_meta["slug"]
    for entry in entries:
        n = entry["degree"]
        html_path = scratch_dir / f"{slug}-{n}.html"
        png_path = CARD_DIR / f"{slug}-{n}.png"
        html_path.write_text(card_html(sign_meta, n, entry))
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
        for slug in SIGNS_TO_RENDER:
            module = load_module(slug)
            sign_meta = module.SIGN
            entries = module.ENTRIES
            written = render_sign(sign_meta, entries, scratch_dir)
            total += len(written)
            print(f"{sign_meta['name']}: {len(written)}/{len(entries)} cards -> {CARD_DIR}/")
    print(f"wrote {total} share-card PNG(s) total")


if __name__ == "__main__":
    main()
