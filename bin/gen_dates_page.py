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
    {
        "slug": "best-days-to-conceive-2027",
        "title": "Best Days to Conceive in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to try to conceive, by Western electional astrology: the Moon in a fertile water sign (Cancer, Scorpio, Pisces) applying to Venus or Jupiter. Computed with the Swiss Ephemeris. Planning and intention, not medical advice.",
        "h1": "Best Days to Conceive in 2027",
        "disclaimer": "This is traditional, symbolic timing for planning and intention, not medical or fertility advice. For anything medical, your doctor comes first.",
        "lede": "The best day in each month of 2027 to try to conceive, by Western electional astrology: the Moon in a fertile water sign (Cancer, Scorpio, or Pisces), applying to Venus or Jupiter, and not void of course. Computed with the Swiss Ephemeris. One quiet gift this year: 2027 has no Venus retrograde.",
        "rows": [
            ("January", "Sat, Jan 2", 7, "Moon in Scorpio applying to a conjunction with Venus, Jupiter rising. Just past the full Moon, but a strong Venus day."),
            ("February", "Sun, Feb 7", 6, "Waxing Moon in Pisces applying to a sextile to Venus, Jupiter rising."),
            ("March", "Wed, Mar 17", 6, "Waxing Moon in Cancer, her home sign, clear and not void, Venus on the Midheaven."),
            ("April", "Tue, Apr 13", 9, "Waxing Moon in Cancer applying to a trine to Venus, Jupiter rising. One of the year's best."),
            ("May", "Tue, May 18", 6, "Waxing Moon in Scorpio, clear and not void, Venus on the Midheaven and Jupiter rising."),
            ("June", "Mon, Jun 7", 9, "Waxing Moon in Cancer applying to a sextile to Venus, in a Venus hour."),
            ("July", "Mon, Jul 12", 6, "Waxing Moon in Scorpio, clear and not void, Jupiter rising."),
            ("August", "Fri, Aug 27", 9, "Moon in Cancer applying to a sextile to Jupiter, Venus and Jupiter rising, in a Venus hour."),
            ("September", "Sun, Sep 5", 9, "Waxing Moon in Scorpio applying to a sextile to Venus, Jupiter on the Midheaven."),
            ("October", "Sat, Oct 2", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Venus rising."),
            ("November", "Mon, Nov 8", 8, "Waxing Moon in Pisces, clear and not void, Venus rising, Jupiter on the Midheaven."),
            ("December", "Sun, Dec 5", 9, "Waxing Moon in Pisces applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
        ],
        "how_chosen": (
            "<p>The Moon governs the body and its cycles, so a conception election puts her first. "
            "The tradition favors the Moon in a <strong>fertile water sign</strong>, Cancer, Scorpio, "
            "or Pisces, <strong>waxing</strong> where possible so life grows toward the light, "
            "<strong>not void of course</strong>, and <strong>applying to a benefic</strong>, Venus "
            "for the body and love, Jupiter for increase. Every date above sits in a water-sign Moon, "
            "held away from Mars and Saturn.</p>"),
        "avoid": (
            "<p>2027 carries <strong>no Venus retrograde</strong>, which is uncommon and steady ground "
            "for anything to do with the body and love. The Mercury retrogrades (Feb 10 to Mar 4, "
            "Jun 11 to Jul 5, Oct 8 to 29) matter less here than for contracts, but the "
            "<strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 "
            "are unsettled ground worth stepping around when you can.</p>"),
        "cta_h2": "Timing something this tender?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or ask The Twelve Rooms for a full reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What are the best days to get pregnant in 2027 by astrology?",
             "Traditionally the strongest days put the Moon in a fertile water sign (Cancer, Scorpio, Pisces), waxing and not void of course, applying to Venus or Jupiter. The table above gives the best such day in each month of 2027. This is symbolic timing for intention, not medical advice."),
            ("Does the Moon sign really affect conception?",
             "In the tradition the Moon rules the body and its cycles, and the water signs are considered fertile. This is a reflective, symbolic practice, a way to choose a meaningful moment. Use it alongside medical guidance, never instead of it."),
            ("Why is 2027 good for this?",
             "2027 has no Venus retrograde, which astrologers read as steady ground for love and the body, and the water-sign Moons fall on genuinely clean days. Everything is computed with the Swiss Ephemeris for the sky itself."),
            ("Does my own chart matter?",
             "For the most personal timing, yes. These dates rank the sky, which is the same for everyone. The strongest day is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-sign-a-contract-2027",
        "title": "Best Days to Sign a Contract in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to sign a contract or close a deal, by Western electional astrology: a waxing Moon applying to Mercury or Jupiter, with Mercury direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Sign a Contract in 2027",
        "lede": "The best day in each month of 2027 to sign a contract, close a deal, or put your name to something binding, by Western electional astrology: the waxing Moon applying to Mercury (agreements) or Jupiter (good faith), with Mercury direct so the terms hold. Computed with the Swiss Ephemeris.",
        "rows": [
            ("January", "Thu, Jan 7", 9, "Waxing Moon in Capricorn applying to a conjunction with Mercury, Jupiter rising, in a Jupiter hour."),
            ("February", "Sat, Feb 6", 6, "Waxing Moon in Aquarius, clear and not void, Jupiter rising, in a Mercury hour. Sign before the Feb 10 retrograde."),
            ("March", "Sun, Mar 14", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter rising, just clear of the retrograde."),
            ("April", "Wed, Apr 14", 9, "Waxing Moon in Leo applying to a trine to Mercury, Jupiter rising."),
            ("May", "Sun, May 16", 9, "Waxing Moon in Libra applying to a trine to Mercury, Jupiter rising."),
            ("June", "Fri, Jun 4", 7, "Waxing Moon in Gemini applying to a sextile to Jupiter, in a Mercury hour. Sign before the June retrograde."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Mercury hour."),
            ("August", "Wed, Aug 11", 9, "Waxing Moon in Sagittarius applying to a trine to Mercury, Jupiter rising."),
            ("September", "Sat, Sep 4", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter on the Midheaven, in a Mercury hour."),
            ("October", "Sat, Oct 2", 7, "Waxing Moon in Scorpio applying to a sextile to Jupiter. Sign before the Oct 8 retrograde."),
            ("November", "Mon, Nov 1", 9, "Waxing Moon in Sagittarius applying to a sextile to Mercury, Jupiter on the Midheaven."),
            ("December", "Thu, Dec 2", 9, "Waxing Moon in Aquarius applying to a sextile to Mercury, Jupiter on the Midheaven."),
        ],
        "how_chosen": (
            "<p>Contracts belong to Mercury, planet of agreements, terms, and the written word. The "
            "Moon should be <strong>waxing</strong>, <strong>not void of course</strong>, and "
            "<strong>applying to a benefic</strong>, Mercury for the deal itself or Jupiter for good "
            "faith and fair terms, and away from Mars (dispute) and Saturn (delay). The cardinal rule: "
            "<strong>Mercury must be direct</strong>, so every date above sidesteps the three "
            "retrogrades.</p>"),
        "avoid": (
            "<p><strong>The three Mercury retrogrades:</strong> Feb 10 to Mar 4, Jun 11 to Jul 5, and "
            "Oct 8 to 29. Signing under a backward Mercury is the one thing the tradition is most firm "
            "about, because agreements made then tend to be reopened. See the "
            "<a href='/mercury-retrograde'>Mercury retrograde 2027 guide</a>. The "
            "<strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 "
            "are also volatile ground for anything you want to stay settled.</p>"),
        "cta_h2": "Signing something that matters?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to sign a contract in 2027?",
             "The strongest days fall on a waxing Moon applying to Mercury or Jupiter with Mercury direct. The table above gives the best such day in each month, so you can pick one that fits your timeline."),
            ("Why does Mercury retrograde matter for signing?",
             "Mercury rules contracts, terms, and communication. The tradition avoids signing while it is retrograde (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29 in 2027) because those agreements tend to be revisited. Every date here keeps Mercury direct."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest signing, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-buy-a-house-2027",
        "title": "Best Days to Buy a House or Move in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to buy a home or move in, by Western electional astrology: a waxing Moon applying to Venus or Jupiter, in a fixed or fortunate sign. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Buy a House or Move in 2027",
        "lede": "The best day in each month of 2027 to buy a home, close on a house, or move in, by Western electional astrology: the waxing Moon applying to Venus (comfort, value) or Jupiter (fortune, room to grow), and not void of course. Computed with the Swiss Ephemeris. 2027 has no Venus retrograde, which is steady ground for property.",
        "rows": [
            ("January", "Tue, Jan 19", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Fri, Feb 12", 8, "Waxing Moon in Taurus, Venus-ruled, applying to a trine to Venus, in a Venus hour."),
            ("March", "Tue, Mar 9", 9, "Waxing Moon in Aries applying to a sextile to Venus, Jupiter rising, in a Venus hour."),
            ("April", "Sat, Apr 10", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter rising."),
            ("May", "Sat, May 8", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("June", "Tue, Jun 8", 10, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter on the Midheaven, in a Venus hour."),
            ("July", "Tue, Jul 6", 10, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Venus hour."),
            ("August", "Wed, Aug 11", 9, "Waxing Moon in Sagittarius applying to a trine to Venus, Jupiter rising."),
            ("September", "Sat, Sep 4", 10, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter rising."),
            ("October", "Sat, Oct 2", 10, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter on the Midheaven, in a Venus hour."),
            ("November", "Fri, Nov 5", 12, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising, Jupiter on the Midheaven. The year's strongest."),
            ("December", "Fri, Dec 10", 10, "Waxing Moon in Taurus, Venus-ruled, applying to a trine to Venus, Venus on the Midheaven."),
        ],
        "how_chosen": (
            "<p>A home is Venus and the Moon's business, comfort, belonging, and value. The Moon should "
            "be <strong>waxing</strong>, so the home grows on you, <strong>not void of course</strong>, "
            "and <strong>applying to a benefic</strong>, Venus for warmth and worth or Jupiter for room "
            "and fortune, and away from Mars (repairs, conflict) and Saturn (cold, heavy). The loveliest "
            "days add a Moon in Taurus, Venus's own sign, which lifts February 12 and December 10.</p>"),
        "avoid": (
            "<p>2027 carries <strong>no Venus retrograde</strong>, uncommon and welcome for anything to "
            "do with value and home. If you are also signing paperwork, keep <strong>Mercury direct</strong> "
            "(avoid Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29). And the <strong>eclipse seasons</strong> "
            "around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 are shaky ground for a move you want "
            "to feel settled.</p>"),
        "cta_h2": "Timing a move that matters?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to buy a house in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus or Jupiter and not void of course, with a Taurus or fortunate-sign Moon a bonus. The table above gives the best such day in each month of 2027."),
            ("Is there a good day to move in astrologically?",
             "Yes. The same factors apply to moving in as to buying: a waxing, benefic-applying Moon settles the home. The dates above work for closing, signing, or the move itself, whichever you are timing."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-for-a-job-interview-2027",
        "title": "Best Days for a Job Interview or New Job in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 for a job interview or starting a new job, by Western electional astrology: a waxing Moon applying to the Sun, Jupiter, or Mercury, with Mercury direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days for a Job Interview or New Job in 2027",
        "lede": "The best day in each month of 2027 to interview, accept an offer, or start a new job, by Western electional astrology: the waxing Moon applying to the Sun (recognition), Jupiter (opportunity), or Mercury (the conversation), with Mercury direct. Computed with the Swiss Ephemeris.",
        "rows": [
            ("January", "Thu, Jan 7", 9, "Waxing Moon in Capricorn applying to a conjunction with Mercury, Jupiter rising."),
            ("February", "Sun, Feb 7", 7, "Waxing Moon in Pisces applying to a conjunction with Mercury, in a Sun hour."),
            ("March", "Sun, Mar 14", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter rising, in a Mercury hour."),
            ("April", "Wed, Apr 14", 9, "Waxing Moon in Leo applying to a trine to Mercury, Jupiter rising."),
            ("May", "Wed, May 12", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Sun hour."),
            ("June", "Tue, Jun 8", 9, "Waxing Moon in Leo applying to a sextile to the Sun, Jupiter rising, in a Mercury hour."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Mercury hour."),
            ("August", "Wed, Aug 11", 9, "Waxing Moon in Sagittarius applying to a trine to the Sun, Jupiter rising, in a Mercury hour."),
            ("September", "Sat, Sep 4", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter on the Midheaven, in a Mercury hour."),
            ("October", "Mon, Oct 4", 9, "Waxing Moon in Sagittarius applying to a sextile to the Sun, Jupiter on the Midheaven, in a Sun hour."),
            ("November", "Mon, Nov 1", 9, "Waxing Moon in Sagittarius applying to a sextile to Mercury, Jupiter on the Midheaven."),
            ("December", "Thu, Dec 2", 9, "Waxing Moon in Aquarius applying to a sextile to Mercury, Jupiter on the Midheaven."),
        ],
        "how_chosen": (
            "<p>A new job is the Sun (recognition, the role), Jupiter (opportunity, growth), and Mercury "
            "(the interview, the offer letter). The Moon should be <strong>waxing</strong>, "
            "<strong>not void of course</strong>, and <strong>applying to a benefic</strong>, away from "
            "Mars (friction) and Saturn (obstacles). For the interview and the paperwork, "
            "<strong>Mercury direct</strong> keeps the conversation clean, so every date above avoids the "
            "retrogrades.</p>"),
        "avoid": (
            "<p>Keep <strong>Mercury direct</strong> for interviews and offers: avoid Feb 10 to Mar 4, "
            "Jun 11 to Jul 5, and Oct 8 to 29. The <strong>eclipse seasons</strong> around Feb 6 and 20 "
            "and around Jul 18, Aug 2, and Aug 17 are unstable for beginnings you want to last. See the "
            "<a href='/mercury-retrograde'>Mercury retrograde 2027 guide</a> for the full windows.</p>"),
        "cta_h2": "Timing a move that matters?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day for a job interview in 2027?",
             "The strongest days fall on a waxing Moon applying to the Sun, Jupiter, or Mercury with Mercury direct. The table above gives the best such day in each month, so you can match it to your interview or start date."),
            ("Does astrology help with getting a job?",
             "Electional astrology is about timing, not guarantees. It picks a moment when the sky favors recognition and clear communication. It supports your preparation; it does not replace it."),
            ("Why keep Mercury direct?",
             "Mercury rules interviews, offers, and paperwork. Under retrograde (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29 in 2027) those tend to get muddled or revisited, so the dates here keep Mercury direct."),
            ("Does my own chart matter?",
             "For the strongest timing, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-launch-a-product-2027",
        "title": "Best Days to Launch a Product in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to launch a product or go live, by Western electional astrology: a waxing Moon applying to the Sun or Jupiter, with the Sun angular. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Launch a Product in 2027",
        "lede": "The best day in each month of 2027 to launch, publish, or go live, by Western electional astrology: the waxing Moon applying to the Sun (visibility) or Jupiter (reach), with the Sun on an angle. Computed with the Swiss Ephemeris. Starting a whole business? See <a href='/best-days-to-start-a-business-2027'>2027's business dates</a>.",
        "rows": [
            ("January", "Tue, Jan 12", 9, "Waxing Moon in Pisces applying to a sextile to the Sun, Sun on the Midheaven, in a Jupiter hour."),
            ("February", "Mon, Feb 15", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter rising. Note: Mercury is retrograde, workable for visibility, not for signing."),
            ("March", "Wed, Mar 10", 9, "Waxing Moon in Aries applying to a trine to Jupiter, Sun on the Midheaven, in a Sun hour."),
            ("April", "Sun, Apr 25", 9, "Moon in Capricorn applying to a trine to the Sun, Sun on the Midheaven, Jupiter rising."),
            ("May", "Wed, May 12", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Sun hour."),
            ("June", "Tue, Jun 8", 9, "Waxing Moon in Leo applying to a sextile to the Sun, Sun on the Midheaven, in a Jupiter hour."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Sun on the Midheaven, in a Jupiter hour."),
            ("August", "Fri, Aug 6", 9, "Waxing Moon in Libra applying to a sextile to the Sun, Sun on the Midheaven, in a Sun hour."),
            ("September", "Sat, Sep 4", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Sun and Jupiter rising."),
            ("October", "Mon, Oct 4", 9, "Waxing Moon in Sagittarius applying to a sextile to the Sun, Jupiter on the Midheaven, in a Sun hour."),
            ("November", "Mon, Nov 8", 9, "Waxing Moon in Pisces applying to a trine to the Sun, Jupiter on the Midheaven, in a Jupiter hour."),
            ("December", "Thu, Dec 2", 8, "Waxing Moon in Aquarius, clear and not void, Sun rising, Jupiter on the Midheaven."),
        ],
        "how_chosen": (
            "<p>A launch is about being seen, so it leans on the Sun (light, visibility) and Jupiter "
            "(reach, goodwill). The Moon should be <strong>waxing</strong>, so the thing grows after it "
            "ships, <strong>not void of course</strong> (or it 'goes nowhere'), and "
            "<strong>applying to a benefic</strong>, with the Sun ideally on an angle so it stands in "
            "the light. Every date above keeps the Moon clear of Mars and Saturn.</p>"),
        "avoid": (
            "<p>A void-of-course Moon is the classic mistake for a launch: the old rule is that nothing "
            "done under it comes to much. If your launch also involves signing or heavy messaging, keep "
            "<strong>Mercury direct</strong> (avoid Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29). The "
            "<strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 "
            "are dramatic, unpredictable ground for a debut.</p>"),
        "cta_h2": "Timing a launch that matters?",
        "cta_p": "Find the exact best window for your city and launch in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to launch a product in 2027?",
             "The strongest days fall on a waxing Moon applying to the Sun or Jupiter, not void of course, with the Sun on an angle. The table above gives the best such day in each month of 2027."),
            ("Why does the void-of-course Moon matter for a launch?",
             "The tradition holds that ventures begun under a void Moon tend to fizzle. Every date here is chosen to keep the Moon making a clean applying aspect at the peak window, not drifting void."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest launch, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-propose-2027",
        "title": "Best Days to Propose or Get Engaged in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to propose or get engaged, by Western electional astrology: a waxing Moon applying to Venus, with Venus angular and direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Propose or Get Engaged in 2027",
        "lede": "The best day in each month of 2027 to propose or get engaged, by Western electional astrology: the waxing Moon applying to Venus (love), with Venus strong on an angle and direct all year. Computed with the Swiss Ephemeris. Ready to set the date too? See <a href='/best-wedding-dates-2027'>2027's wedding dates</a>.",
        "rows": [
            ("January", "Tue, Jan 19", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Fri, Feb 12", 7, "Waxing Moon in Taurus, Venus-ruled, applying to a trine to Venus, in a Venus hour."),
            ("March", "Thu, Mar 4", 7, "Moon in Aquarius applying to a conjunction with Venus, Venus on the Midheaven, in a Venus hour."),
            ("April", "Sat, Apr 3", 7, "Moon in Pisces applying to a conjunction with Venus, Venus on the Midheaven, in a Venus hour."),
            ("May", "Sat, May 8", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("June", "Mon, Jun 7", 9, "Waxing Moon in Cancer applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
            ("July", "Tue, Jul 6", 7, "Waxing Moon in Leo applying to a conjunction with Jupiter, in a Venus hour."),
            ("August", "Wed, Aug 11", 9, "Waxing Moon in Sagittarius applying to a trine to Venus, Venus on the Midheaven, in a Venus hour."),
            ("September", "Sat, Sep 4", 7, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Venus rising."),
            ("October", "Sat, Oct 2", 7, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Venus rising."),
            ("November", "Wed, Nov 3", 7, "Waxing Moon in Capricorn applying to a trine to Jupiter, in a Venus hour."),
            ("December", "Sun, Dec 5", 9, "Waxing Moon in Pisces applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
        ],
        "how_chosen": (
            "<p>A proposal is Venus's moment. The election wants the Moon <strong>waxing</strong>, "
            "<strong>not void of course</strong>, and <strong>applying to Venus</strong> or Jupiter, "
            "with <strong>Venus strong</strong>, ideally on an angle, and away from Mars and Saturn. A "
            "quiet advantage this year: Venus is <strong>direct the whole of 2027</strong>, so love's "
            "planet is never walking backward when you ask.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, which is genuinely rare and good news for "
            "matters of the heart. The Mercury retrogrades (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to "
            "29) matter less for a proposal than for a contract, but the <strong>eclipse seasons</strong> "
            "around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 carry a charge you may prefer to "
            "step around for a tender moment.</p>"),
        "cta_h2": "Asking a question this big?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or ask The Twelve Rooms for a full reading that weighs the sky against your two charts.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to propose in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus, with Venus strong and direct. The table above gives the best such day in each month of 2027, so you can pick one that fits your plan."),
            ("Is 2027 a good year to get engaged?",
             "Astrologically, yes: 2027 has no Venus retrograde, which the tradition reads as steady, honest ground for love, so the planet of romance is direct every day of the year."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the most meaningful moment, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to you and your partner's charts, which is the personalized reading."),
        ],
    },
]

if __name__ == "__main__":
    for cfg in PAGES:
        print("wrote", build(cfg) + ".html")
