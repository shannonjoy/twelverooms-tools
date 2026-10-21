#!/usr/bin/env python3
"""Regenerate sitemap.xml: the hand-built pages, the Sabian hub and 12 sign
pages, and the 46 Saturn return cohort pages. Nothing else.

Since 2026-10-21 (search plan move 1, Shannon's call) the sitemap carries
no per-date Moon or void-of-course URLs and no Sabian degree pages. Those
pages still serve for readers and links; the date pages are indexable only
inside the rolling window in api/_seo/crawl.py, and the degree pages are
noindex. lastmod is the date of the last commit that touched the file
serving each URL, or today for a file with uncommitted changes, so run this
after committing content changes and commit the sitemap on its own.
Usage: python3 bin/gen-sitemap.py"""
import subprocess
from datetime import date
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
# Programmatic per-birth-year Saturn return pages (/saturn-return/YYYY).
# Computed per request and written in the tense the calendar calls for.
SATURN_YEARS = range(1960, 2006)

# Left out on purpose (Shannon, 2026-10-21, search plan move 1):
#  - the 360 Sabian degree pages, now served noindex, follow;
#  - every per-date /moon/ and /void-of-course-moon/ URL. A committed sitemap
#    cannot roll forward, so each date it listed went stale within weeks
#    (all 122 had by Oct 20). The hubs link the current dates instead, and
#    api/_seo/crawl.py keeps only the rolling window indexable.
ROOT = Path(__file__).resolve().parent.parent

today = date.today().isoformat()


def url(path, changefreq, priority, lastmod):
    """One sitemap entry. lastmod is the only one of these three fields
    Google is documented to use, and every URL in this file was missing it
    until 2026-08-10, so the sitemap carried no freshness signal at all."""
    return (f'  <url><loc>{BASE}{path}</loc><lastmod>{lastmod}</lastmod>'
            f'<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')


def git_date(*files):
    """Date of the last commit that touched any of these files; today when
    one has uncommitted changes. A checkout stamps every file with the
    checkout time, so file mtimes said 'today' for the whole site."""
    rel = [str(f.relative_to(ROOT)) for f in files if f.exists()]
    if not rel:
        return today
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *rel],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return today
    out = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--", *rel],
                         capture_output=True, text=True).stdout.strip()
    return out or today


def serving_file(path):
    return ROOT / ("index.html" if path == "/" else path.lstrip("/") + ".html")


rows = [url(p, cf, pr, git_date(serving_file(p))) for p, cf, pr in STATIC]
saturn_lastmod = git_date(ROOT / "api" / "saturn.py", ROOT / "api" / "_seo" / "crawl.py")
for y in SATURN_YEARS:
    rows.append(url(f"/saturn-return/{y}", "yearly", "0.5", saturn_lastmod))

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")
out = Path(__file__).resolve().parent.parent / "sitemap.xml"
out.write_text(xml)
print(f"wrote {out}: {len(rows)} URLs = {len(STATIC)} static + {len(SATURN_YEARS)} saturn-year "
      f"(no per-date or Sabian degree URLs, by design)")
