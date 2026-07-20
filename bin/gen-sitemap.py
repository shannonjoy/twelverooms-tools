#!/usr/bin/env python3
"""Regenerate sitemap.xml: the static pages plus a rolling window of
server-rendered per-date Moon pages (/moon/YYYY-MM-DD). Re-run periodically
to roll the window forward. The date pages are deterministic and valid
forever, so past entries dropping off only trims the sitemap, not the pages.
Usage: python3 bin/gen-sitemap.py [days_forward]"""
import sys
from datetime import date, timedelta
from pathlib import Path

BASE = "https://thetwelverooms.com"
STATIC = [
    ("/", "weekly", "1.0"),
    ("/moon", "daily", "0.9"),
    ("/natal-chart", "monthly", "0.9"),
    ("/synastry", "monthly", "0.8"),
    ("/electional", "monthly", "0.8"),
    ("/almanac", "weekly", "0.7"),
    ("/mercury-retrograde", "monthly", "0.7"),
    ("/best-wedding-dates-2027", "monthly", "0.8"),
    ("/best-wedding-dates-2028", "monthly", "0.7"),
    ("/best-days-to-start-a-business-2027", "monthly", "0.7"),
    ("/best-days-to-invest-2027", "monthly", "0.6"),
]

days = int(sys.argv[1]) if len(sys.argv) > 1 else 90
start = date.today()

rows = [f'  <url><loc>{BASE}{p}</loc><changefreq>{cf}</changefreq><priority>{pr}</priority></url>'
        for p, cf, pr in STATIC]
for i in range(days + 1):
    d = (start + timedelta(days=i)).isoformat()
    rows.append(f'  <url><loc>{BASE}/moon/{d}</loc><changefreq>never</changefreq><priority>0.4</priority></url>')

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")
out = Path(__file__).resolve().parent.parent / "sitemap.xml"
out.write_text(xml)
print(f"wrote {out} with {len(STATIC)} static + {days + 1} moon-date URLs")
