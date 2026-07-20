#!/usr/bin/env python3
"""Generate a 'best dates' SEO page from a config. Reusable for any
intention/year. Run: python3 bin/gen_dates_page.py  (emits all PAGES below).
Rows come from the studio electional engine (scan_year, sky-only universal
ranking). Keep the honest eclipse/retrograde caveats in `avoid`."""
import html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent


def esc(s):
    return html.escape(str(s), quote=True)


def build(cfg):
    rows = "\n".join(
        f'        <tr><td><strong>{esc(m)}</strong></td><td>{esc(d)}</td>'
        f'<td><span class="tag gold">{s}</span></td><td>{w}</td></tr>'
        for m, d, s, w in cfg["rows"])
    faq_schema = ",".join(
        '{"@type":"Question","name":' + _json(q) +
        ',"acceptedAnswer":{"@type":"Answer","text":' + _json(a) + '}}'
        for q, a in cfg["faq"])
    faq_html = "\n".join(
        f'    <div class="qa"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>'
        for q, a in cfg["faq"])
    disclaimer = (f'\n  <div class="disclaimer">{cfg["disclaimer"]}</div>\n'
                  if cfg.get("disclaimer") else "")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(cfg['title'])}</title>
<meta name="description" content="{esc(cfg['description'])}">
<link rel="canonical" href="https://thetwelverooms.com/{cfg['slug']}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_schema}]}}
</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>{esc(cfg['h1'])}</h1>{disclaimer}
  <p class="lede">{cfg['lede']}</p>

  <div class="card">
    <table class="year-table">
      <thead><tr><th>Month</th><th>Best day</th><th>Score</th><th>Why this one</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
    <p class="hint" style="margin-top:8px">Best day shown by date; the exact best hour depends on your location. Run your city in the <a href="/electional">timing finder</a>.</p>
  </div>

  <section class="prose">
    <h2>How these dates are chosen</h2>
    {cfg['how_chosen']}
    <h2>What to avoid</h2>
    {cfg['avoid']}
  </section>

  <div class="cta">
    <h2>{esc(cfg['cta_h2'])}</h2>
    <p>{cfg['cta_p']}</p>
    <a href="{cfg['cta_href']}" rel="noopener">{esc(cfg['cta_label'])}</a>
  </div>

  <section class="faq">
    <h2>Common questions</h2>
{faq_html}
  </section>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / f"{cfg['slug']}.html").write_text(page)
    return cfg["slug"]


def _json(s):
    import json
    return json.dumps(str(s))


PAGES = [
    {
        "slug": "best-days-to-start-a-business-2027",
        "title": "Best Days to Start a Business in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to launch a business, by Western electional astrology: the waxing Moon applying to Jupiter, Mercury, or the Sun, with Mercury direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Start a Business in 2027",
        "lede": "The best day in each month of 2027 to open a business, sign the papers, or go live, by Western electional astrology: the waxing Moon applying to Jupiter (fortune), Mercury (commerce), or the Sun, with Mercury direct so the paperwork holds. Computed with the Swiss Ephemeris.",
        "rows": [
            ("January", "Fri, Jan 15", 5, "Waxing Moon in Taurus, applying to a trine to the Sun."),
            ("February", "Sun, Feb 7", 5, "Waxing Moon in Pisces, conjunct Mercury, but wedged between the Feb 6 eclipse and the Feb 10 Mercury retrograde. A weak month."),
            ("March", "Sat, Mar 13", 5, "Waxing Moon in Gemini, applying to a sextile to Jupiter, just clear of the retrograde."),
            ("April", "Wed, Apr 14", 5, "Waxing Moon in Leo, applying to a trine to Mercury, planet of commerce."),
            ("May", "Tue, May 11", 5, "Waxing Moon in Leo, applying to a sextile to Mercury."),
            ("June", "Sat, Jun 5", 5, "Waxing Moon in Cancer, conjunct Mercury, before the June retrograde."),
            ("July", "Sun, Jul 11", 5, "Waxing Moon in Scorpio, applying to a trine to the Sun, just clear of the retrograde."),
            ("August", "Thu, Aug 12", 5, "Waxing Moon in Capricorn, trine Jupiter, but in eclipse season (Aug 2 and 17). Handle with care."),
            ("September", "Sat, Sep 11", 5, "Waxing Moon in Aquarius, applying to a trine to Mercury."),
            ("October", "Sun, Oct 3", 5, "Waxing Moon in Sagittarius, sextile the Sun, before the October retrograde."),
            ("November", "Thu, Nov 4", 5, "Waxing Moon in Aquarius, applying to a trine to Mercury."),
            ("December", "Mon, Dec 27", 5, "Waxing Moon in Capricorn, conjunct Mercury, a steady close to the year."),
        ],
        "how_chosen": (
            "<p>In electional astrology a launch is a beginning, and the Moon leads. "
            "For a business she should be <strong>waxing</strong>, so the venture grows, "
            "<strong>not void of course</strong>, and <strong>applying to a benefic</strong>: "
            "Jupiter for fortune and expansion, Mercury for commerce and the paperwork, the Sun "
            "for visibility. She should steer clear of Mars (loss, haste) and Saturn (stagnation). "
            "And the cardinal rule for anything you sign: <strong>Mercury must be direct</strong>, "
            "which is why every date above dodges the three retrogrades.</p>"),
        "avoid": (
            "<p><strong>The three Mercury retrogrades:</strong> Feb 10 to Mar 4, Jun 11 to Jul 5, "
            "and Oct 8 to 29. Signing and launching under a backward Mercury invites errors and "
            "do-overs. See the full <a href='/mercury-retrograde'>Mercury retrograde 2027 guide</a>. "
            "<strong>Eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and "
            "Aug 17 are also unstable ground, which is why February and mid-summer are the year's "
            "weakest windows for a launch.</p>"),
        "cta_h2": "Timing a launch that matters?",
        "cta_p": "Find the exact best window for your city and business in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to start a business in 2027?",
             "There is no single best day; the strongest windows fall on a waxing Moon applying to Jupiter or Mercury with Mercury direct. The table above gives the best day in each month, so you can pick one that fits your own timeline."),
            ("Why does Mercury retrograde matter for a business launch?",
             "Mercury rules commerce, contracts, and communication. Traditionally you avoid signing or launching while it is retrograde (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29 in 2027) because agreements made then tend to be revisited. Every date here keeps Mercury direct."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own birth chart matter?",
             "For the strongest launch, yes. These dates rank the sky itself, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized electional reading."),
        ],
    },
    {
        "slug": "best-wedding-dates-2028",
        "title": "Best Wedding Dates 2028, by Astrology · The Twelve Rooms",
        "description": "The best wedding date each month in 2028 by Western electional astrology: the waxing Moon applying to Venus or Jupiter, clear of void-of-course and Mercury retrograde. Computed with the Swiss Ephemeris.",
        "h1": "Best Wedding Dates 2028",
        "lede": "The best day in each month of 2028 to marry, by Western electional astrology: the waxing Moon applying to Venus or Jupiter, clear of the void and of Mercury retrograde. Computed with the Swiss Ephemeris. Planning sooner? See <a href='/best-wedding-dates-2027'>2027's dates</a>.",
        "rows": [
            ("January", "Thu, Jan 6", 5, "Waxing Moon in Taurus, exalted, applying to a trine to Jupiter. Just mind the Jan 12 eclipse a few days later."),
            ("February", "Sun, Feb 27", 5, "Waxing Moon in Aries, applying to a conjunction with Venus."),
            ("March", "Mon, Mar 27", 5, "Waxing Moon in Taurus, exalted, applying to a trine to Jupiter. One of the year's loveliest."),
            ("April", "Sat, Apr 1", 5, "Waxing Moon in Cancer, her home sign, applying to a sextile to Jupiter."),
            ("May", "Fri, May 5", 5, "Waxing Moon in Libra, ruled by Venus, applying to a trine to Venus."),
            ("June", "Mon, Jun 26", 5, "Waxing Moon in Virgo, applying to a conjunction with Jupiter."),
            ("July", "Fri, Jul 28", 5, "Waxing Moon in Scorpio, applying to a sextile to Jupiter, clear of the July eclipses."),
            ("August", "Tue, Aug 1", 5, "Waxing Moon in Capricorn, applying to a trine to Jupiter."),
            ("September", "Mon, Sep 18", 5, "Waxing Moon in Libra, Venus-ruled, applying to a conjunction with Jupiter."),
            ("October", "Fri, Oct 20", 5, "Waxing Moon in Sagittarius, applying to a sextile to Jupiter."),
            ("November", "Thu, Nov 16", 5, "Waxing Moon in Sagittarius, applying to a sextile to Jupiter."),
            ("December", "Mon, Dec 18", 5, "Waxing Moon in Aquarius, applying to a sextile to Venus."),
        ],
        "how_chosen": (
            "<p>The Moon leads every wedding election. She should be <strong>waxing</strong>, so the "
            "marriage grows in light, <strong>not void of course</strong>, and <strong>applying to "
            "a benefic</strong>, Venus (love) or Jupiter (blessing), and away from Mars (strife) and "
            "Saturn (coldness). <strong>Venus and Mercury should be direct</strong>. The loveliest "
            "days add a Moon in <strong>Taurus</strong>, her sign of exaltation, which lifts March 27 "
            "and January 6 above the rest.</p>"),
        "avoid": (
            "<p><strong>The three Mercury retrogrades of 2028:</strong> Jan 25 to Feb 15, May 22 to "
            "Jun 15, and Sep 20 to Oct 12. <strong>Eclipse seasons</strong> cluster around Jan 12 and "
            "26, around Jul 6 and 22, and on Dec 31. Astrologers keep weddings several days clear of "
            "eclipses, so early January and both eclipse windows are the year's most delicate ground, "
            "even where the Moon's best available day looks fine.</p>"),
        "cta_h2": "Find your hour, and your date",
        "cta_p": "Run your city and dates in the free timing finder for the exact windows, or commission a full electional reading that weighs the sky against your two charts.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What are the best wedding dates in 2028?",
             "The strongest fall on a Taurus Moon, the Moon's exaltation: March 27 and January 6. Each has the waxing Moon applying to Jupiter and clear of Mercury retrograde. The table above gives the best day in every month."),
            ("How are these dates chosen?",
             "By Western electional astrology: a waxing Moon, not void of course, applying to Venus or Jupiter with Venus and Mercury direct, computed with the Swiss Ephemeris. The exact best time depends on your location."),
            ("What months should I avoid for a 2028 wedding?",
             "Sidestep the Mercury retrogrades (Jan 25 to Feb 15, May 22 to Jun 15, Sep 20 to Oct 12) and the eclipse seasons around Jan 12 and 26, Jul 6 and 22, and Dec 31."),
            ("Do these dates work for my location and my chart?",
             "The dates rank the sky itself, which is the same everywhere. The exact best time shifts by location, and the single strongest date is the one that also speaks well to you and your partner's own charts, which is the personalized electional reading."),
        ],
    },
]

if __name__ == "__main__":
    for cfg in PAGES:
        print("wrote", build(cfg) + ".html")
