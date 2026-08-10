#!/usr/bin/env python3
"""Write the two internal-linking surfaces that only existed in JavaScript.

Measured on main, 2026-08-10, over the server-rendered link graph:

  - All 362 per-date pages in the sitemap were unreachable from the home
    page. The only thing that ever linked them was a template literal in
    moon.html and void-of-course-moon.html that a browser evaluates at
    runtime, and it covered a 10-day rolling window at that. Nothing in the
    HTML a crawler reads pointed at any of them.
  - Each of the 24 electional pages had exactly one real inbound link, all
    from the same page, /electional-astrology. Lose that one hub and the
    whole cluster that the Aug 23 gate is measured on goes dark.

This script writes both surfaces into the HTML itself, between markers, so
re-running it replaces rather than duplicates. Run it before
bin/gen-sitemap.py: the date index and the sitemap advertise the same
window, read from seo-window.json.

Usage: python3 bin/gen-internal-links.py [days_forward]
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW = json.loads((ROOT / "seo-window.json").read_text())
INDEX_FROM = date.fromisoformat(WINDOW["index_from"])
INDEX_TO = date.fromisoformat(WINDOW["index_to"])
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else WINDOW["sitemap_days_forward"]

DATE_HUBS = [
    ("moon.html", "/moon", "Browse the Moon by date",
     "Every date below is a page of its own: the Moon's sign, phase and "
     "void-of-course windows for that day, computed once and correct for good."),
    ("void-of-course-moon.html", "/void-of-course-moon", "Browse void-of-course by date",
     "Every date below is a page of its own: the exact void-of-course windows "
     "for that day, computed once and correct for good."),
]

ELECTIONAL = [
    ("/best-wedding-dates-2027", "Best wedding dates 2027"),
    ("/best-wedding-dates-2028", "Best wedding dates 2028"),
    ("/best-days-to-propose-2027", "Best days to propose in 2027"),
    ("/best-days-to-sign-a-contract-2027", "Best days to sign a contract in 2027"),
    ("/best-days-to-start-a-business-2027", "Best days to start a business in 2027"),
    ("/best-days-to-launch-a-product-2027", "Best days to launch a product in 2027"),
    ("/best-days-to-invest-2027", "Best days to start investing in 2027"),
    ("/best-days-to-buy-a-house-2027", "Best days to buy a house in 2027"),
    ("/best-days-to-buy-a-car-2027", "Best days to buy a car in 2027"),
    ("/best-days-to-move-to-a-new-city-2027", "Best days to move to a new city in 2027"),
    ("/best-days-to-open-a-restaurant-2027", "Best days to open a restaurant in 2027"),
    ("/best-days-for-a-job-interview-2027", "Best days for a job interview in 2027"),
    ("/best-days-to-ask-for-a-raise-2027", "Best days to ask for a raise in 2027"),
    ("/best-days-to-send-an-important-email-2027", "Best days to send an important email in 2027"),
    ("/best-days-to-publish-a-book-2027", "Best days to publish a book in 2027"),
    ("/best-days-to-file-a-lawsuit-2027", "Best days to file a lawsuit in 2027"),
    ("/best-days-for-surgery-2027", "Best days for surgery in 2027"),
    ("/best-days-to-conceive-2027", "Best days to conceive in 2027"),
    ("/best-days-for-a-first-date-2027", "Best days for a first date in 2027"),
    ("/best-days-to-reconcile-2027", "Best days to reconcile in 2027"),
    ("/best-days-to-throw-a-party-2027", "Best days to throw a party in 2027"),
    ("/best-days-to-travel-2027", "Best days to travel in 2027"),
    ("/best-days-to-start-a-diet-2027", "Best days to start a diet in 2027"),
    ("/best-days-to-cut-your-hair-2027", "Best days to cut your hair in 2027"),
]
SIBLINGS = 6  # how many peers each electional page links to

START = "<!-- gen-internal-links: start -->"
END = "<!-- gen-internal-links: end -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def splice(path, block):
    """Replace the marked block, or insert it before the footer slot."""
    f = ROOT / path
    s = f.read_text(encoding="utf-8")
    marked = f"{START}\n{block}\n  {END}"
    if BLOCK_RE.search(s):
        s = BLOCK_RE.sub(lambda _: marked, s, count=1)
    else:
        anchor = '  <div id="site-footer">'
        if anchor not in s:
            raise SystemExit(f"{path}: no footer slot to anchor the block to")
        s = s.replace(anchor, f"  {marked}\n\n{anchor}", 1)
    f.write_text(s, encoding="utf-8")


DATEBROWSE_RE = re.compile(
    r'<div class="datebrowse" id="datebrowse">.*?</div>\s*(?=\n)', re.S)


def date_index():
    """Fill the existing #datebrowse slot rather than adding a second block.

    tools.js builds a 10-day rolling chip row into this same slot and now
    skips a slot that already has children, so filling it here replaces that
    row instead of sitting next to it.
    """
    start = date.today()
    days = [start + timedelta(days=i) for i in range(DAYS + 1)]
    days = [d for d in days if INDEX_FROM <= d <= INDEX_TO]
    for filename, prefix, heading, lede in DATE_HUBS:
        chips = "".join(
            f'<a href="{prefix}/{d.isoformat()}">{d.strftime("%b %-d")}</a>'
            for d in days)
        block = (f'<div class="datebrowse" id="datebrowse">{START}\n'
                 f'    <h3>{heading}</h3>\n'
                 f'    <p class="hint">{lede}</p>\n'
                 f'    <div class="chips">{chips}</div>\n'
                 f'  {END}</div>\n')
        f = ROOT / filename
        s = f.read_text(encoding="utf-8")
        s, n = DATEBROWSE_RE.subn(lambda _: block, s, count=1)
        if not n:
            raise SystemExit(f"{filename}: no #datebrowse slot found")
        f.write_text(s, encoding="utf-8")
    return len(days)


def electional_cluster():
    n = len(ELECTIONAL)
    for i, (path, _) in enumerate(ELECTIONAL):
        peers = [ELECTIONAL[(i + k) % n] for k in range(1, SIBLINGS + 1)]
        items = "".join(f'      <li><a href="{h}">{t}</a></li>\n' for h, t in peers)
        block = ('  <section class="prose" aria-label="More timing guides">\n'
                 '    <h2>More best-date guides</h2>\n'
                 '    <p>Every guide below is scored the same way, against the same '
                 'ephemeris. If your question is not here, the '
                 '<a href="/electional">timing finder</a> will score any date for any '
                 'intention, and <a href="/electional-astrology">how timing works</a> '
                 'explains the doctrine behind the scores.</p>\n'
                 f'    <ul class="linklist">\n{items}    </ul>\n'
                 '  </section>')
        splice(path.lstrip("/") + ".html", block)
    return n


def main():
    days = date_index()
    count = electional_cluster()
    print(f"date index: {days} dates written into {len(DATE_HUBS)} hub pages "
          f"({DAYS} days forward, clipped to {INDEX_FROM}..{INDEX_TO})")
    print(f"electional cluster: {SIBLINGS} sibling links written into {count} pages")
    print("now run: python3 bin/gen-sitemap.py")


if __name__ == "__main__":
    main()
