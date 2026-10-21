"""Shared crawl and indexation policy for The Twelve Rooms.

Two problems this module exists to solve, both measured on 2026-08-10:

1. The site had no server-rendered internal links at all. Every page shipped
   an empty `<div id="masthead"></div>` and an empty `<div id="site-footer">`,
   and the whole navigation was built client side by tools.js. On the raw HTML
   pass, which is what Google uses to schedule crawling, every page on the
   domain carried zero sitewide links. FOOTER_HTML below is the server-rendered
   link block that fixes that. tools.js only injects its own copy when the slot
   is still empty, so a page that ships this markup keeps it.

2. The `/moon/:date` and `/void-of-course-moon/:date` routes answered 200 for
   every date from 1900-01-01 to 2100-12-31, and each page linked to the day
   before and the day after. That is 73,414 dates across two routes, 146,828
   crawlable URLs, all reachable by walking the prev and next chain from any
   single entry point, against 362 of them in the sitemap. INDEX_FROM and
   INDEX_TO bound that space: dates inside the window stay fully indexable,
   dates outside it are served with `noindex, follow` and the chain link that
   would leave the window is dropped, so the walk terminates.

3. Added 2026-10-21 (search plan, move 1): a dated page is only worth
   indexing while it is current. Inside INDEX_FROM..INDEX_TO a page is now
   indexable only within a rolling window of ROLL_BACK days before today to
   ROLL_FORWARD days after it, judged at request time. Older and further-out
   dates still serve 200 for visitors and keep their day-to-day links, but
   carry `noindex, follow`, and a chain link into that zone is marked
   `rel="nofollow"` so a crawler is not walked through it. Nothing expires
   by being forgotten in a static file any more.

Keep INDEX_FROM, INDEX_TO, ROLL_BACK and ROLL_FORWARD in step with
seo-window.json at the repo root. bin/check-seo.py fails if they disagree.
"""
from datetime import date, datetime, timedelta, timezone

# Indexable window for the per-date programmatic series. Wider than the
# sitemap window on purpose: a reader asking about a wedding date eighteen
# months out should still land on an indexable page, while the unbounded
# two-century tail stops being crawlable at all.
INDEX_FROM = date(2026, 1, 1)
INDEX_TO = date(2027, 12, 31)

# Rolling indexable window, counted from today (UTC) at request time.
ROLL_BACK = 7
ROLL_FORWARD = 30


def today_utc():
    return datetime.now(timezone.utc).date()


def in_index_window(d):
    """True when a per-date page may be chain-linked at all."""
    return INDEX_FROM <= d <= INDEX_TO


def in_rolling_window(d, today=None):
    """True when a per-date page is current enough to be indexed."""
    today = today or today_utc()
    return (in_index_window(d)
            and today - timedelta(days=ROLL_BACK) <= d <= today + timedelta(days=ROLL_FORWARD))


def robots_meta(d, today=None):
    """Robots meta tag for a per-date page: empty only while it is current."""
    if in_rolling_window(d, today):
        return ""
    return '<meta name="robots" content="noindex, follow">'


def chain_rel(d, today=None):
    """rel attribute for a prev or next link: nofollow into a stale date."""
    return "" if in_rolling_window(d, today) else ' rel="nofollow"'


def chain_href(d, path_prefix):
    """Anchor href for a prev or next day, or empty past the window edge.

    Returning empty is what closes the infinite walk. The page still serves
    200 if someone asks for it directly; it just stops being advertised.
    """
    if in_index_window(d):
        return f"{path_prefix}/{d.isoformat()}"
    return ""


# Server-rendered sitewide footer. Mirrors the NAV structure in tools.js so
# the crawlable link set and the rendered link set name the same pages.
# Visible, permanent content: no hidden links, nothing a reader cannot see.
FOOTER_HTML = """<footer class="site">
    <nav class="footer-nav" aria-label="Site">
      <div class="footer-col">
        <h2>Calculate</h2>
        <a href="/natal-chart">Natal chart</a>
        <a href="/big-3-calculator">Big 3 calculator</a>
        <a href="/saturn-return-calculator">Saturn return</a>
        <a href="/synastry">Synastry</a>
        <a href="/transit-timeline">Transit timeline</a>
        <a href="/daily-horoscope">Daily horoscope</a>
      </div>
      <div class="footer-col">
        <h2>The sky now</h2>
        <a href="/moon">Moon right now</a>
        <a href="/void-of-course-moon">Void-of-course Moon</a>
        <a href="/planetary-hours">Planetary hours</a>
        <a href="/mercury-retrograde">Mercury retrograde</a>
        <a href="/venus-retrograde">Venus retrograde</a>
      </div>
      <div class="footer-col">
        <h2>Best dates</h2>
        <a href="/almanac">Dates by intention</a>
        <a href="/electional">Pick your moment</a>
        <a href="/electional-astrology">How timing works</a>
        <a href="/best-wedding-dates-2027">Best wedding dates 2027</a>
        <a href="/best-days-to-start-a-business-2027">Best days to start a business</a>
        <a href="/best-days-to-sign-a-contract-2027">Best days to sign a contract</a>
      </div>
      <div class="footer-col">
        <h2>Read</h2>
        <a href="/the-twelve-houses">The twelve houses</a>
        <a href="/sabian-symbols">Sabian symbols</a>
        <a href="/forecast">Monthly Sky Forecast</a>
        <a href="/reports">Readings</a>
        <a href="/about">About</a>
      </div>
    </nav>
    <div><a href="/forecast">Monthly Sky Forecast</a> &middot; the free email</div>
    <div class="privacy">&copy; 2026 The Twelve Rooms &middot; City data &copy; GeoNames (CC BY 4.0)</div>
    <div class="privacy">Positions computed with the Swiss Ephemeris. Free software under the <a href="https://github.com/shannonjoy/twelverooms-tools" rel="noopener">AGPL-3.0</a>, source available. Brand and readings &copy; The Twelve Rooms.</div>
  </footer>"""
