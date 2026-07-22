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

## Principles (updated Jul 21 2026 — see roadmap.md for the accounts item)
- The tools themselves stay open, ungated, and server-rendered/crawlable —
  that's an SEO requirement, not a branding stance. No paywalls on the tools.
- Optional accounts are roadmapped (save/sync only, never required to use a tool).
- Analytics (GA4) is live as of Jul 20 2026 — the old "no analytics" line is stale.
- Birth data is computed in memory, never stored or logged unless a signed-in
  user opts in to save it. Say so on every page.
- "Swiss Ephemeris" stated on-page for credibility.
- Marketing (email capture, CTAs, incentives) should use real, tasteful growth
  tactics — not a "no dark patterns" purity stance, not cheesy or meme-y either.
  See marketing-reports/email-list-strategy-0721.md.

## Deploy
1. `bin/sync-engines.sh` (after any engine change)
2. From this directory: `vercel --scope shanjoy` (preview) / `vercel --prod --scope shanjoy`
3. After first prod deploy: add the custom domain, submit the sitemap in
   Google Search Console.

## License
AGPL-3.0. Reuse the code freely under that license; the Twelve Rooms
brand (name, wordmark, XII medallion, palette, copy) is not covered and
remains © The Twelve Rooms. See NOTICE.md for full attribution.
