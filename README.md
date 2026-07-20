# The Twelve Rooms — Free Web Tools

Free astrology tools that funnel organic search traffic to
thetwelverooms.etsy.com. Static pages at the project root, Python
serverless functions in `api/`, engines synced from the orchestrator
into `api/_engines/` (generated copies, never edited here).

Licensed **AGPL-3.0** (see LICENSE and NOTICE.md). This is the
compliance path for the Swiss Ephemeris, which is AGPL-or-commercial
dual licensed: because the tools are served over a network, the AGPL
requires the complete source be public, which it is.

## Tools
- `/moon` + `/api/moon` — Moon sign, phase, void-of-course, next ingress
- `/natal-chart` + `/api/natal` — free natal wheel, positions, aspects
- `/synastry` + `/api/synastry` — cross-aspect grid, overlays
- `/electional` + `/api/windows` — electional window finder (lite, 21-day cap)
- `/api/geo` — offline city lookup (GeoNames, CC-BY) for the birthplace fields

## Principles (the positioning IS the marketing)
- No accounts, no paywalls, no cookies, no analytics, no dark patterns.
- Birth data is computed in memory, never stored or logged. Say so on every page.
- "Swiss Ephemeris" stated on-page for credibility.
- Every page ends in one tasteful CTA to the Etsy shop.

## Deploy
1. `bin/sync-engines.sh` (after any engine change)
2. From this directory: `vercel --scope shanjoy` (preview) / `vercel --prod --scope shanjoy`
3. After first prod deploy: add the custom domain, submit the sitemap in
   Google Search Console.

## License
AGPL-3.0. Reuse the code freely under that license; the Twelve Rooms
brand (name, wordmark, XII medallion, palette, copy) is not covered and
remains © The Twelve Rooms. See NOTICE.md for full attribution.
