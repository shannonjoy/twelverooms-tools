#!/usr/bin/env python3
"""The share card for /big-3/<sun>-<moon>-<rising>: one branded 1200x630 PNG
at og/big-3.png, same design and method as bin/gen_webtools_card.py (plain
HTML card, headless Chrome screenshot).

One card, not one per combination: 1,872 PNGs would add tens of megabytes
of near-identical images to the repo for pages that are noindex by design.
Each share page names its own three signs in og:title, which is the line
an unfurl shows under the image, and the visitor can save a per-combination
image drawn on their own device (big3-share.js).

    python3 bin/gen_big3_card.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_webtools_card as base  # noqa: E402

CARD_PATH = HERE.parent / "og" / "big-3.png"
HTML = (base.CARD_HTML
        .replace('<div class="kicker">Free Astrology Tools</div>', '<div class="kicker">My Big 3</div>')
        .replace('<div class="head">Read the sky yourself.</div>', '<div class="head">Sun, Moon, Rising.</div>')
        .replace("""<div class="snippet">Natal charts, your Big 3, synastry, Saturn returns,
      planetary hours, moon phases, and elections for the days that matter.</div>""",
                 """<div class="snippet">The short version of a whole chart.
      Find yours free, in a minute.</div>"""))
assert HTML != base.CARD_HTML and "My Big 3" in HTML and "Sun, Moon, Rising." in HTML and "short version" in HTML


def main():
    with tempfile.TemporaryDirectory(prefix="tr-big3-card-") as scratch:
        page = Path(scratch) / "card.html"
        page.write_text(HTML)
        r = subprocess.run([base.CHROME, "--headless=new", "--disable-gpu",
                            f"--window-size={base.CARD_W},{base.CARD_H}",
                            f"--screenshot={CARD_PATH}", f"file://{page}"], capture_output=True)
    data = CARD_PATH.read_bytes() if CARD_PATH.exists() else b""
    if r.returncode != 0 or data[:8] != b"\x89PNG\r\n\x1a\n":
        print("failed to render the card", r.stderr.decode(errors="replace")[:300], file=sys.stderr)
        return 1
    w, h = int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    print(f"og/big-3.png {w}x{h} {len(data)} bytes")
    return 0 if (w, h) == (base.CARD_W, base.CARD_H) else 1


if __name__ == "__main__":
    sys.exit(main())
