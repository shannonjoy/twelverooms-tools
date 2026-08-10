#!/usr/bin/env python3
"""Regenerate sitemap.xml: the static pages plus a rolling window of
server-rendered per-date Moon pages (/moon/YYYY-MM-DD) and per-date
void-of-course pages (/void-of-course-moon/YYYY-MM-DD, added Jul 22 2026
as a second programmatic series: same underlying data, led by
void-of-course status instead of sign, targeting "void of course moon
[date]" distinctly). Re-run periodically to roll the window forward. The
date pages are deterministic and valid forever, so past entries dropping
off only trims the sitemap, not the pages.
Usage: python3 bin/gen-sitemap.py [days_forward]"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

BASE = "https://thetwelverooms.com"
STATIC = [
    ("/", "weekly", "1.0"),
    ("/moon", "daily", "0.9"),
    ("/natal-chart", "monthly", "0.9"),
    ("/daily-horoscope", "daily", "0.9"),
    ("/synastry", "monthly", "0.8"),
    ("/electional", "monthly", "0.8"),
    ("/saturn-return-calculator", "monthly", "0.8"),
    ("/transit-timeline", "monthly", "0.8"),
    ("/big-3-calculator", "monthly", "0.7"),
    ("/the-twelve-houses", "monthly", "0.6"),
    ("/reports", "monthly", "0.7"),
    ("/forecast", "monthly", "0.6"),
    ("/about", "yearly", "0.5"),
    ("/almanac", "weekly", "0.7"),
    ("/mercury-retrograde", "monthly", "0.7"),
    ("/best-wedding-dates-2027", "monthly", "0.8"),
    ("/best-wedding-dates-2028", "monthly", "0.7"),
    ("/best-days-to-start-a-business-2027", "monthly", "0.7"),
    ("/best-days-to-invest-2027", "monthly", "0.6"),
    ("/electional-astrology", "monthly", "0.8"),
    ("/best-days-to-conceive-2027", "monthly", "0.7"),
    ("/best-days-to-sign-a-contract-2027", "monthly", "0.7"),
    ("/best-days-to-buy-a-house-2027", "monthly", "0.7"),
    ("/best-days-for-a-job-interview-2027", "monthly", "0.7"),
    ("/best-days-to-launch-a-product-2027", "monthly", "0.7"),
    ("/best-days-to-propose-2027", "monthly", "0.7"),
    ("/best-days-to-buy-a-car-2027", "monthly", "0.7"),
    ("/best-days-to-ask-for-a-raise-2027", "monthly", "0.7"),
    ("/best-days-to-open-a-restaurant-2027", "monthly", "0.7"),
    ("/best-days-to-publish-a-book-2027", "monthly", "0.6"),
    ("/best-days-to-move-to-a-new-city-2027", "monthly", "0.7"),
    ("/best-days-to-reconcile-2027", "monthly", "0.6"),
    ("/best-days-for-a-first-date-2027", "monthly", "0.6"),
    ("/best-days-to-start-a-diet-2027", "monthly", "0.6"),
    ("/best-days-to-cut-your-hair-2027", "monthly", "0.6"),
    ("/venus-retrograde", "monthly", "0.7"),
    ("/planetary-hours", "weekly", "0.7"),
    ("/void-of-course-moon", "weekly", "0.7"),
    ("/best-days-to-file-a-lawsuit-2027", "monthly", "0.6"),
    ("/best-days-for-surgery-2027", "monthly", "0.6"),
    ("/best-days-to-send-an-important-email-2027", "monthly", "0.6"),
    ("/best-days-to-travel-2027", "monthly", "0.6"),
    ("/best-days-to-throw-a-party-2027", "monthly", "0.6"),
    ("/sabian-symbols", "monthly", "0.6"),
    ("/sabian-symbols/aries", "monthly", "0.6"),
    ("/sabian-symbols/taurus", "monthly", "0.6"),
    ("/sabian-symbols/gemini", "monthly", "0.6"),
    ("/sabian-symbols/cancer", "monthly", "0.6"),
    ("/sabian-symbols/leo", "monthly", "0.6"),
    ("/sabian-symbols/virgo", "monthly", "0.6"),
    ("/sabian-symbols/libra", "monthly", "0.6"),
    ("/sabian-symbols/scorpio", "monthly", "0.6"),
    ("/sabian-symbols/sagittarius", "monthly", "0.6"),
    ("/sabian-symbols/capricorn", "monthly", "0.6"),
    ("/sabian-symbols/aquarius", "monthly", "0.6"),
    ("/sabian-symbols/pisces", "monthly", "0.6"),
]
# Individual Sabian symbol degree pages. Aries was the Jul 24 2026 proof
# batch; Taurus/Gemini/Cancer (Wave 1) added the same day. Extend
# SABIAN_SIGNS as each additional sign is verified and written.
SABIAN_SIGNS = {"aries": 30, "taurus": 30, "gemini": 30, "cancer": 30, "leo": 30, "virgo": 30, "libra": 30, "scorpio": 30, "sagittarius": 30, "capricorn": 30, "aquarius": 30, "pisces": 30}
# Programmatic per-birth-year Saturn return pages (/saturn-return/YYYY).
# Deterministic and valid forever, like the moon-date pages.
SATURN_YEARS = range(1960, 2006)

ROOT = Path(__file__).resolve().parent.parent
WINDOW = json.loads((ROOT / "seo-window.json").read_text())
INDEX_FROM = date.fromisoformat(WINDOW["index_from"])
INDEX_TO = date.fromisoformat(WINDOW["index_to"])

# How much of the indexable window to advertise, counted forward from today.
# Was 180 days, which put 362 per-date URLs in a sitemap that held 24
# electional pages: the money pages were outnumbered 15 to 1 in the one file
# Google reads to decide what to crawl. The pages outside this window still
# serve 200 and stay indexable; they are simply not pushed.
days = int(sys.argv[1]) if len(sys.argv) > 1 else WINDOW["sitemap_days_forward"]
start = date.today()
today = start.isoformat()


def url(path, changefreq, priority, lastmod):
    """One sitemap entry. lastmod is the only one of these three fields
    Google is documented to use, and every URL in this file was missing it
    until 2026-08-10, so the sitemap carried no freshness signal at all."""
    return (f'  <url><loc>{BASE}{path}</loc><lastmod>{lastmod}</lastmod>'
            f'<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')


def file_mtime(path):
    """Last modified date of the file that serves this path, when there is
    one. Real mtimes beat stamping every URL with today: a sitewide lastmod
    of today on every regeneration is the pattern that teaches Google to
    stop trusting the field."""
    candidate = ROOT / (path.lstrip("/") + ".html")
    if path == "/":
        candidate = ROOT / "index.html"
    if candidate.exists():
        return date.fromtimestamp(candidate.stat().st_mtime).isoformat()
    return today


rows = [url(p, cf, pr, file_mtime(p)) for p, cf, pr in STATIC]
dated_count = 0
for i in range(days + 1):
    d = start + timedelta(days=i)
    if not (INDEX_FROM <= d <= INDEX_TO):
        continue  # outside the indexable window: api/_seo/crawl.py noindexes it
    iso = d.isoformat()
    rows.append(url(f"/moon/{iso}", "never", "0.4", today))
    rows.append(url(f"/void-of-course-moon/{iso}", "never", "0.4", today))
    dated_count += 2
saturn_mtime = file_mtime("/saturn-return-calculator")
for y in SATURN_YEARS:
    rows.append(url(f"/saturn-return/{y}", "yearly", "0.5", saturn_mtime))
sabian_count = 0
for sign, n in SABIAN_SIGNS.items():
    for d in range(1, n + 1):
        path = f"/sabian-symbols/{sign}-{d}"
        rows.append(url(path, "yearly", "0.5", file_mtime(path)))
        sabian_count += 1

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")
out = Path(__file__).resolve().parent.parent / "sitemap.xml"
out.write_text(xml)
print(f"wrote {out}: {len(rows)} URLs = {len(STATIC)} static + {dated_count} moon/void-date "
      f"+ {len(SATURN_YEARS)} saturn-year + {sabian_count} sabian-degree")
print(f"per-date window advertised: {days} days forward, clipped to {INDEX_FROM}..{INDEX_TO}")
