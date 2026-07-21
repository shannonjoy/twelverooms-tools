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
    {
        "slug": "best-days-to-buy-a-car-2027",
        "title": "Best Days to Buy a Car in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to buy a car, by Western electional astrology: a waxing Moon applying to Venus or Jupiter, with Mercury direct for the paperwork. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Buy a Car in 2027",
        "lede": "The best day in each month of 2027 to buy a car or make a major purchase, by Western electional astrology: the waxing Moon applying to Venus (value) or Jupiter (fortune), with Mercury direct for the paperwork. Computed with the Swiss Ephemeris. 2027 has no Venus retrograde, steady ground for anything you buy and keep.",
        "rows": [
            ("January", "Tue, Jan 19", 8, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Mon, Feb 1", 6, "Moon in Sagittarius applying to a trine to Jupiter, Jupiter rising. Buy before the Feb 10 retrograde."),
            ("March", "Tue, Mar 9", 8, "Waxing Moon in Aries applying to a sextile to Venus, Venus on the Midheaven."),
            ("April", "Thu, Apr 8", 8, "Waxing Moon in Taurus, Venus-ruled, applying to a sextile to Venus, Venus on the Midheaven."),
            ("May", "Sat, May 8", 8, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("June", "Tue, Jun 8", 8, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter on the Midheaven, in a Venus hour."),
            ("July", "Tue, Jul 6", 8, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Venus hour."),
            ("August", "Wed, Aug 11", 8, "Waxing Moon in Sagittarius applying to a trine to Venus, Venus rising."),
            ("September", "Fri, Sep 3", 8, "Waxing Moon in Libra, Venus-ruled, clear and not void, Venus and Jupiter rising, in a Venus hour."),
            ("October", "Sat, Oct 2", 8, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter on the Midheaven. Buy before the Oct 8 retrograde."),
            ("November", "Fri, Nov 5", 10, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising, Jupiter on the Midheaven. The year's strongest."),
            ("December", "Sun, Dec 5", 8, "Waxing Moon in Pisces applying to a sextile to Venus, Venus rising."),
        ],
        "how_chosen": (
            "<p>A car is a purchase and a possession, so it belongs to <strong>Venus</strong> (value, "
            "what you own), with <strong>Mercury</strong> watching the paperwork. The Moon should be "
            "<strong>waxing</strong>, <strong>not void of course</strong>, and <strong>applying to "
            "Venus or Jupiter</strong>, away from Mars (haste, accidents). Because buying is also "
            "signing, every date keeps <strong>Mercury direct</strong>.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, good news for anything you buy and keep. "
            "Keep <strong>Mercury direct</strong> for the contract (avoid Feb 10 to Mar 4, Jun 11 to "
            "Jul 5, Oct 8 to 29), and step around the <strong>eclipse seasons</strong> around Feb 6 and "
            "20 and around Jul 18, Aug 2, and Aug 17, jangly ground for a big purchase.</p>"),
        "cta_h2": "Buying something big?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to buy a car in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus or Jupiter, not void of course, with Mercury direct for the paperwork. The table above gives the best such day in each month of 2027."),
            ("Why does Mercury matter for buying a car?",
             "Because a purchase is also a signing. Mercury rules contracts and paperwork, so the dates keep it direct, avoiding the 2027 retrogrades (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29)."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-ask-for-a-raise-2027",
        "title": "Best Days to Ask for a Raise in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to ask for a raise or negotiate salary, by Western electional astrology: a waxing Moon applying to Jupiter or Venus, the planets of increase and worth. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Ask for a Raise in 2027",
        "lede": "The best day in each month of 2027 to ask for a raise or negotiate your salary, by Western electional astrology: the waxing Moon applying to Jupiter (increase) or Venus (worth, goodwill). Computed with the Swiss Ephemeris. A tailwind this year: 2027 has no Venus retrograde.",
        "rows": [
            ("January", "Sat, Jan 2", 7, "Moon in Scorpio applying to a conjunction with Venus, Jupiter rising."),
            ("February", "Fri, Feb 12", 9, "Waxing Moon in Taurus, Venus-ruled, applying to a trine to Venus, Jupiter rising."),
            ("March", "Tue, Mar 9", 9, "Waxing Moon in Aries applying to a sextile to Venus, Jupiter rising."),
            ("April", "Thu, Apr 8", 9, "Waxing Moon in Taurus applying to a sextile to Venus, Jupiter rising."),
            ("May", "Sat, May 8", 9, "Waxing Moon in Gemini applying to a sextile to Venus, Jupiter on the Midheaven."),
            ("June", "Tue, Jun 8", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter on the Midheaven."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising."),
            ("August", "Tue, Aug 31", 9, "Waxing Moon in Virgo applying to a conjunction with Venus, Jupiter on the Midheaven."),
            ("September", "Sun, Sep 5", 9, "Waxing Moon in Scorpio applying to a sextile to Venus, Jupiter on the Midheaven."),
            ("October", "Sat, Oct 2", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter on the Midheaven."),
            ("November", "Wed, Nov 3", 7, "Waxing Moon in Capricorn applying to a trine to Jupiter."),
            ("December", "Sun, Dec 5", 7, "Waxing Moon in Pisces applying to a sextile to Venus."),
        ],
        "how_chosen": (
            "<p>A raise is <strong>Jupiter</strong> (increase, generosity) and <strong>Venus</strong> "
            "(your worth, and the warmth in the room). The Moon should be <strong>waxing</strong>, "
            "<strong>not void of course</strong>, and <strong>applying to Jupiter or Venus</strong>, "
            "away from Saturn (not now) and Mars (friction). Ask when the sky is inclined to say yes.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, steady ground for questions of worth. It "
            "helps to ask when <strong>Mercury is direct</strong> too (avoid Feb 10 to Mar 4, Jun 11 to "
            "Jul 5, Oct 8 to 29), since the ask is a conversation, and to steer clear of the "
            "<strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17, "
            "when moods swing.</p>"),
        "cta_h2": "Asking for what you're worth?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to ask for a raise in 2027?",
             "The strongest days fall on a waxing Moon applying to Jupiter or Venus, the planets of increase and worth. The table above gives the best such day in each month, so you can time your ask."),
            ("Does astrology really help with a salary negotiation?",
             "It sets the timing, not the outcome. Electional astrology picks a moment when the sky leans toward increase and goodwill. It supports a well-prepared ask; it does not replace one."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-open-a-restaurant-2027",
        "title": "Best Days to Open a Restaurant or Shop in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to open a restaurant, cafe, or shop, by Western electional astrology: a waxing Moon applying to Venus or Jupiter, with Mercury direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Open a Restaurant or Shop in 2027",
        "lede": "The best day in each month of 2027 to open a restaurant, cafe, or shop, by Western electional astrology: the waxing Moon applying to Venus (welcome, pleasure) or Jupiter (abundance), with Mercury direct for the lease and signage. Computed with the Swiss Ephemeris. Starting a different kind of business? See <a href='/best-days-to-start-a-business-2027'>2027's business dates</a>.",
        "rows": [
            ("January", "Tue, Jan 19", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Mon, Feb 1", 7, "Moon in Sagittarius applying to a trine to Jupiter, Venus on the Midheaven. Open before the Feb 10 retrograde."),
            ("March", "Tue, Mar 9", 9, "Waxing Moon in Aries applying to a sextile to Venus, Jupiter rising, in a Venus hour."),
            ("April", "Thu, Apr 8", 9, "Waxing Moon in Taurus, Venus-ruled, applying to a sextile to Venus, Jupiter rising."),
            ("May", "Sat, May 8", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("June", "Tue, Jun 8", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter on the Midheaven."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising."),
            ("August", "Tue, Aug 31", 11, "Waxing Moon in Virgo applying to a conjunction with Venus, Venus and Jupiter on the Midheaven. The year's strongest."),
            ("September", "Thu, Sep 9", 9, "Waxing Moon in Capricorn applying to a trine to Jupiter, Venus rising."),
            ("October", "Sat, Oct 2", 9, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Venus rising."),
            ("November", "Fri, Nov 5", 9, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising, Jupiter on the Midheaven."),
            ("December", "Sun, Dec 5", 9, "Waxing Moon in Pisces applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
        ],
        "how_chosen": (
            "<p>Hospitality and retail are <strong>Venus</strong>'s trade, warmth, welcome, and things "
            "people enjoy, backed by <strong>Jupiter</strong> for a full house. The Moon should be "
            "<strong>waxing</strong>, <strong>not void of course</strong>, and <strong>applying to a "
            "benefic</strong>, away from Mars and Saturn. For the lease and the paperwork, keep "
            "<strong>Mercury direct</strong>.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, welcome for a Venus-ruled venture. Keep "
            "<strong>Mercury direct</strong> for signing (avoid Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 "
            "to 29) and mind the <strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, "
            "Aug 2, and Aug 17.</p>"),
        "cta_h2": "Opening your doors?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to open a restaurant in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus or Jupiter with Mercury direct. The table above gives the best such day in each month of 2027 for opening your doors."),
            ("Is opening a shop different from starting a business?",
             "The timing overlaps, but a shop or restaurant leans harder on Venus, the planet of welcome and pleasure, since customers come for the experience. These dates weight Venus accordingly. For a non-retail business, see the business-launch dates."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-publish-a-book-2027",
        "title": "Best Days to Publish a Book in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to publish a book or release your writing, by Western electional astrology: a waxing Moon applying to Mercury, Jupiter, or the Sun, with Mercury direct. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Publish a Book in 2027",
        "lede": "The best day in each month of 2027 to publish a book, release your writing, or send it into the world, by Western electional astrology: the waxing Moon applying to Mercury (the word), Jupiter (reach), or the Sun (visibility), with Mercury direct. Computed with the Swiss Ephemeris.",
        "rows": [
            ("January", "Thu, Jan 7", 9, "Waxing Moon in Capricorn applying to a conjunction with Mercury, Jupiter rising."),
            ("February", "Mon, Feb 1", 7, "Moon in Sagittarius applying to a trine to Jupiter, Sun on the Midheaven. Before the Feb 10 retrograde."),
            ("March", "Wed, Mar 10", 9, "Waxing Moon in Aries applying to a trine to Jupiter, Sun rising, in a Mercury hour."),
            ("April", "Wed, Apr 14", 9, "Waxing Moon in Leo applying to a trine to Mercury, Sun on the Midheaven, in a Sun hour."),
            ("May", "Wed, May 12", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Sun hour."),
            ("June", "Tue, Jun 8", 9, "Waxing Moon in Leo applying to a sextile to the Sun, Jupiter rising, in a Mercury hour."),
            ("July", "Tue, Jul 6", 9, "Waxing Moon in Leo applying to a conjunction with Jupiter, Jupiter rising, in a Mercury hour."),
            ("August", "Fri, Aug 6", 9, "Waxing Moon in Libra applying to a sextile to the Sun, Sun on the Midheaven, in a Sun hour."),
            ("September", "Sat, Sep 4", 11, "Waxing Moon in Scorpio applying to a sextile to Jupiter, Jupiter and Sun on the Midheaven. The year's strongest."),
            ("October", "Mon, Oct 4", 9, "Waxing Moon in Sagittarius applying to a sextile to the Sun, Sun rising, in a Mercury hour."),
            ("November", "Mon, Nov 1", 9, "Waxing Moon in Sagittarius applying to a sextile to Mercury, Sun rising, in a Mercury hour."),
            ("December", "Thu, Dec 2", 11, "Waxing Moon in Aquarius applying to a sextile to Mercury, Jupiter on the Midheaven, Sun rising."),
        ],
        "how_chosen": (
            "<p>Publishing is <strong>Mercury</strong> (the written word) lifted by <strong>Jupiter</strong> "
            "(a wide audience) and the <strong>Sun</strong> (recognition). The Moon should be "
            "<strong>waxing</strong>, <strong>not void of course</strong>, and <strong>applying to one "
            "of these</strong>, away from Mars and Saturn. Above all, <strong>Mercury direct</strong>, "
            "so the words land as written.</p>"),
        "avoid": (
            "<p><strong>Mercury retrograde</strong> is the one to dodge for anything built on words: "
            "Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29. The <strong>eclipse seasons</strong> around "
            "Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 are loud, unpredictable ground for a "
            "debut you want read on its merits.</p>"),
        "cta_h2": "Sending your words out?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to publish a book in 2027?",
             "The strongest days fall on a waxing Moon applying to Mercury, Jupiter, or the Sun, with Mercury direct. The table above gives the best such day in each month of 2027."),
            ("Why keep Mercury direct for publishing?",
             "Mercury rules writing, print, and the message itself. Releasing under a retrograde Mercury (Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29 in 2027) invites mix-ups and revisions, so the dates keep it direct."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-move-to-a-new-city-2027",
        "title": "Best Days to Move to a New City in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to relocate or move to a new city, by Western electional astrology: a waxing Moon applying to Jupiter or Venus. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Move to a New City in 2027",
        "lede": "The best day in each month of 2027 to relocate, move to a new city, or start over somewhere new, by Western electional astrology: the waxing Moon applying to Jupiter (opportunity, horizons) or Venus (ease, belonging). Computed with the Swiss Ephemeris. Buying a home in place? See <a href='/best-days-to-buy-a-house-2027'>2027's home dates</a>.",
        "rows": [
            ("January", "Wed, Jan 27", 8, "Moon in Libra applying to a sextile to Venus, Venus on the Midheaven."),
            ("February", "Mon, Feb 15", 10, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven."),
            ("March", "Wed, Mar 10", 10, "Waxing Moon in Aries applying to a trine to Jupiter, Venus on the Midheaven."),
            ("April", "Sat, Apr 10", 10, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter rising."),
            ("May", "Sun, May 16", 10, "Waxing Moon in Libra applying to a sextile to Jupiter, Jupiter on the Midheaven."),
            ("June", "Fri, Jun 4", 10, "Waxing Moon in Gemini applying to a sextile to Jupiter, Jupiter on the Midheaven."),
            ("July", "Wed, Jul 7", 10, "Waxing Moon in Virgo applying to a sextile to Venus, Jupiter rising."),
            ("August", "Tue, Aug 31", 12, "Waxing Moon in Virgo applying to a conjunction with Venus, Venus and Jupiter on the Midheaven. The year's strongest."),
            ("September", "Thu, Sep 9", 10, "Waxing Moon in Capricorn applying to a trine to Jupiter, Venus rising."),
            ("October", "Tue, Oct 5", 10, "Waxing Moon in Sagittarius applying to a sextile to Venus, Jupiter on the Midheaven."),
            ("November", "Fri, Nov 5", 11, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising, Jupiter on the Midheaven."),
            ("December", "Wed, Dec 1", 10, "Waxing Moon in Capricorn applying to a trine to Jupiter, Venus on the Midheaven."),
        ],
        "how_chosen": (
            "<p>A move to a new city is <strong>Jupiter</strong>'s territory, horizons, travel, and luck, "
            "with <strong>Venus</strong> for landing softly. The Moon should be <strong>waxing</strong>, "
            "<strong>not void of course</strong>, and <strong>applying to a benefic</strong>, away from "
            "Mars (upheaval) and Saturn (heaviness). Every date keeps the Moon clear and moving toward "
            "fortune.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, steady for belonging and home. If you are "
            "also signing a lease, keep <strong>Mercury direct</strong> (avoid Feb 10 to Mar 4, Jun 11 "
            "to Jul 5, Oct 8 to 29), and give the <strong>eclipse seasons</strong> around Feb 6 and 20 "
            "and around Jul 18, Aug 2, and Aug 17 a wide berth for a fresh start you want to hold.</p>"),
        "cta_h2": "Starting over somewhere new?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or commission a full electional reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to move to a new city in 2027?",
             "The strongest days fall on a waxing Moon applying to Jupiter or Venus, not void of course. The table above gives the best such day in each month of 2027 for the move."),
            ("Is relocating different from moving house?",
             "The sky-craft is similar, but a relocation leans on Jupiter, the planet of horizons and long journeys, more than a local move does. These dates weight Jupiter for the leap. For buying or settling a home in place, see the home dates."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-reconcile-2027",
        "title": "Best Days to Reconcile in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to reconcile or mend a rift, by Western electional astrology: a waxing Moon applying to Venus or Mercury. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Reconcile in 2027",
        "lede": "The best day in each month of 2027 to reconcile, mend a rift, or reach out and try again, by Western electional astrology: the waxing Moon applying to Venus (love) or Mercury (the conversation). Computed with the Swiss Ephemeris. A gentle year for it: 2027 has no Venus retrograde.",
        "rows": [
            ("January", "Tue, Jan 19", 9, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Fri, Feb 12", 7, "Waxing Moon in Taurus applying to a sextile to Mercury, in a Venus hour."),
            ("March", "Tue, Mar 9", 9, "Waxing Moon in Aries applying to a sextile to Venus, Venus on the Midheaven."),
            ("April", "Thu, Apr 8", 9, "Waxing Moon in Taurus, Venus-ruled, applying to a sextile to Venus, Venus on the Midheaven."),
            ("May", "Thu, May 6", 9, "Waxing Moon in Taurus applying to a conjunction with Mercury, Venus on the Midheaven."),
            ("June", "Mon, Jun 14", 9, "Waxing Moon in Scorpio applying to a trine to Mercury, Venus on the Midheaven, in a Venus hour."),
            ("July", "Tue, Jul 6", 7, "Waxing Moon in Leo applying to a conjunction with Jupiter, in a Venus hour."),
            ("August", "Wed, Aug 11", 9, "Waxing Moon in Sagittarius applying to a trine to Venus, Venus rising."),
            ("September", "Wed, Sep 1", 9, "Waxing Moon in Virgo applying to a conjunction with Mercury, Venus rising."),
            ("October", "Wed, Oct 6", 9, "Waxing Moon in Capricorn applying to a sextile to Mercury, Venus rising."),
            ("November", "Fri, Nov 5", 9, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising."),
            ("December", "Sun, Dec 5", 9, "Waxing Moon in Pisces applying to a sextile to Venus, Venus rising."),
        ],
        "how_chosen": (
            "<p>Mending is <strong>Venus</strong> (affection, forgiveness) and <strong>Mercury</strong> "
            "(the honest conversation). The Moon should be <strong>waxing</strong>, so warmth grows, "
            "<strong>not void of course</strong>, and <strong>applying to Venus or Mercury</strong>, "
            "away from Mars (old fights) and Saturn (cold shoulders). Reach out when the sky is soft.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, which the tradition reads as clear ground "
            "for love and repair. For the conversation itself, <strong>Mercury direct</strong> helps "
            "(avoid Feb 10 to Mar 4, Jun 11 to Jul 5, Oct 8 to 29), and the <strong>eclipse seasons</strong> "
            "around Feb 6 and 20 and around Jul 18, Aug 2, and Aug 17 tend to stir feelings up rather "
            "than settle them.</p>"),
        "cta_h2": "Reaching out again?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or ask The Twelve Rooms for a full reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to reconcile with someone in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus or Mercury, the planets of love and honest words. The table above gives the best such day in each month of 2027."),
            ("Can astrology help mend a relationship?",
             "It chooses the timing, not the heart. Electional astrology finds a moment when Venus and Mercury lean toward warmth and clear words. The reaching out, and the honesty, are yours."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the most meaningful moment, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-for-a-first-date-2027",
        "title": "Best Days for a First Date in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 for a first date, by Western electional astrology: a waxing Moon applying to Venus, love's own planet, direct all year. Computed with the Swiss Ephemeris.",
        "h1": "Best Days for a First Date in 2027",
        "lede": "The best day in each month of 2027 for a first date or the start of something new, by Western electional astrology: the waxing Moon applying to Venus, love's own planet, direct all year in 2027. Computed with the Swiss Ephemeris.",
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
            "<p>A first meeting is pure <strong>Venus</strong>: attraction, ease, delight. The Moon "
            "should be <strong>waxing</strong>, <strong>not void of course</strong> (so it goes "
            "somewhere), and <strong>applying to Venus</strong>, with Venus strong and away from Mars "
            "and Saturn. This year Venus is direct all twelve months, so love's planet is never walking "
            "backward.</p>"),
        "avoid": (
            "<p>2027 has <strong>no Venus retrograde</strong>, the single best thing you can ask for in "
            "matters of the heart. The Mercury retrogrades matter less for a date than for a contract, "
            "but the <strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, and "
            "Aug 17 carry a charge you may prefer to skip for a soft first meeting.</p>"),
        "cta_h2": "Starting something new?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or ask The Twelve Rooms for a full reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day for a first date in 2027?",
             "The strongest days fall on a waxing Moon applying to Venus, love's planet, which is direct all year in 2027. The table above gives the best such day in each month."),
            ("Why is Venus the key for a first date?",
             "Venus rules attraction, warmth, and pleasure, everything a first meeting is made of. The strongest days have the Moon applying to a well-placed Venus, and in 2027 Venus is direct all year."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-start-a-diet-2027",
        "title": "Best Days to Start a Diet in 2027, by Astrology · The Twelve Rooms",
        "description": "The best day each month in 2027 to start a diet or break a habit, by Western electional astrology. Here the rule flips: a waning Moon, to diminish rather than grow. Computed with the Swiss Ephemeris.",
        "h1": "Best Days to Start a Diet in 2027",
        "lede": "The best day in each month of 2027 to start a diet or break a habit, by Western electional astrology. Here the usual rule flips: you want a <strong>waning</strong> Moon, to diminish rather than grow, applying to Saturn (discipline) or the Sun (vitality). Computed with the Swiss Ephemeris.",
        "rows": [
            ("January", "Fri, Jan 1", 6, "Waning Moon in Scorpio applying to a sextile to the Sun, in a Saturn hour."),
            ("February", "Fri, Feb 5", 6, "Waning Moon in Aquarius applying to a sextile to Saturn, in a Sun hour."),
            ("March", "Thu, Mar 4", 6, "Waning Moon in Aquarius applying to a sextile to Saturn."),
            ("April", "Thu, Apr 1", 6, "Waning Moon in Aquarius applying to a sextile to the Sun."),
            ("May", "Tue, May 4", 6, "Waning Moon in Aries applying to a conjunction with Saturn."),
            ("June", "Fri, Jun 4", 6, "Waning Moon in Gemini applying to a conjunction with the Sun."),
            ("July", "Fri, Jul 2", 6, "Waning Moon in Gemini applying to a sextile to Saturn."),
            ("August", "Sat, Aug 21", 6, "Waning Moon in Aries applying to a conjunction with Saturn."),
            ("September", "Wed, Sep 22", 6, "Waning Moon in Gemini applying to a sextile to Saturn."),
            ("October", "Tue, Oct 19", 6, "Waning Moon in Gemini applying to a sextile to Saturn."),
            ("November", "Fri, Nov 19", 6, "Waning Moon in Leo applying to a trine to Saturn."),
            ("December", "Sun, Dec 26", 6, "Waning Moon in Sagittarius applying to a trine to Saturn."),
        ],
        "how_chosen": (
            "<p>Most elections want a waxing Moon, but breaking a habit is the exception. To "
            "<strong>reduce</strong> something, the tradition uses a <strong>waning</strong> Moon, "
            "shrinking as you want the craving to shrink, applying to <strong>Saturn</strong> "
            "(discipline, structure) or the <strong>Sun</strong> (will, vitality). Every date above "
            "sits on a waning Moon reaching toward restraint.</p>"),
        "avoid": (
            "<p>Avoid starting on a <strong>waxing</strong> Moon, which the tradition says feeds what "
            "you are trying to starve. Skip the days the Moon applies to Jupiter or Venus (indulgence), "
            "and give the <strong>eclipse seasons</strong> around Feb 6 and 20 and around Jul 18, Aug 2, "
            "and Aug 17 a miss, since resolve tends to wobble around them.</p>"),
        "cta_h2": "Breaking a habit for good?",
        "cta_p": "Find the exact best window for your city in the free timing finder, or ask The Twelve Rooms for a reading that weighs the sky against your own chart.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to start a diet in 2027?",
             "The strongest days fall on a waning Moon applying to Saturn or the Sun, since you want the habit to shrink. The table above gives the best such day in each month of 2027."),
            ("Why a waning Moon for a diet?",
             "Because you want the thing to shrink, not grow. Electional astrology mirrors the intention in the sky: a waxing Moon for what you want more of, a waning Moon for what you want less of. Diets and habit-breaking take the waning Moon."),
            ("How are these dates calculated?",
             "By Western electional astrology, computed with the Swiss Ephemeris in whole-sign houses. The exact best hour depends on your location, since the angles and planetary hours are local."),
            ("Does my own chart matter?",
             "For the strongest result, yes. These dates rank the sky, which is the same for everyone. The single best date is the one that also speaks well to your own chart, which is the personalized reading."),
        ],
    },
    {
        "slug": "best-days-to-cut-your-hair-2027",
        "title": "Best Days to Cut Your Hair in 2027 (for Growth), by the Moon · The Twelve Rooms",
        "description": "The best day each month in 2027 to cut your hair for growth, by the old lunar tradition: a waxing Moon in a fruitful sign. Computed with the Swiss Ephemeris. Gentle folk astrology, lightly held.",
        "h1": "Best Days to Cut Your Hair in 2027 (for Growth)",
        "lede": "The best day in each month of 2027 to cut your hair for faster, fuller growth, by the old lunar tradition: a <strong>waxing</strong> Moon in a fruitful sign, applying to Venus or Jupiter. Computed with the Swiss Ephemeris. Want a trim that holds its shape instead? A waning Moon slows regrowth.",
        "rows": [
            ("January", "Tue, Jan 19", 8, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("February", "Fri, Feb 12", 6, "Waxing Moon in Taurus, clear and not void, Venus on the Midheaven."),
            ("March", "Sun, Mar 14", 8, "Waxing Moon in Gemini applying to a trine to Venus, Venus on the Midheaven."),
            ("April", "Tue, Apr 13", 8, "Waxing Moon in Cancer, fruitful, applying to a trine to Venus, Venus on the Midheaven."),
            ("May", "Sat, May 8", 8, "Waxing Moon in Gemini applying to a sextile to Jupiter, Venus on the Midheaven, in a Venus hour."),
            ("June", "Mon, Jun 7", 8, "Waxing Moon in Cancer, fruitful, applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
            ("July", "Mon, Jul 5", 6, "Waxing Moon in Leo, clear and not void, Venus on the Midheaven, in a Venus hour."),
            ("August", "Wed, Aug 11", 8, "Waxing Moon in Sagittarius applying to a trine to Venus, Venus on the Midheaven, in a Venus hour."),
            ("September", "Sat, Sep 4", 8, "Waxing Moon in Scorpio, fruitful, applying to a sextile to Jupiter, Venus on the Midheaven."),
            ("October", "Sat, Oct 2", 6, "Waxing Moon in Scorpio, fruitful, applying to a sextile to Jupiter."),
            ("November", "Fri, Nov 5", 8, "Waxing Moon in Aquarius applying to a sextile to Venus, Venus rising."),
            ("December", "Sun, Dec 5", 8, "Waxing Moon in Pisces, fruitful, applying to a sextile to Venus, Venus on the Midheaven, in a Venus hour."),
        ],
        "how_chosen": (
            "<p>The lunar hair tradition is simple. To encourage <strong>growth</strong>, cut on a "
            "<strong>waxing</strong> Moon, ideally in a fruitful sign (the water signs, or lush Taurus), "
            "<strong>applying to Venus</strong> (beauty) or Jupiter (abundance). The waxing Moon that "
            "grows the hair is the opposite of the waning Moon you would use to keep a cut looking sharp "
            "for longer.</p>"),
        "avoid": (
            "<p>For growth, avoid the <strong>waning</strong> Moon (it slows regrowth, which is exactly "
            "what you want when you would like a shape to last) and the barren signs. This is folk "
            "tradition, gentle and fun, not a promise; take it in that spirit.</p>"),
        "cta_h2": "Curious what else the Moon times?",
        "cta_p": "See where the Moon is right now on the free Moon page, or find the best window for anything you are timing in the electional finder.",
        "cta_href": "/electional", "cta_label": "Open the timing finder",
        "faq": [
            ("What is the best day to cut your hair for growth in 2027?",
             "By the lunar tradition, the strongest days fall on a waxing Moon in a fruitful sign applying to Venus or Jupiter. The table above gives the best such day in each month of 2027."),
            ("Does cutting hair by the Moon actually work?",
             "It is a centuries-old folk tradition, not a proven one. Many people enjoy timing a trim to a waxing Moon in a fruitful sign for growth, or a waning Moon to keep a cut sharp. Take it as a bit of lunar lore, lightly held."),
            ("How are these dates calculated?",
             "By the Moon's phase and sign, computed with the Swiss Ephemeris. The exact timing shifts a little by location, since the Moon changes sign at a set moment worldwide but the local clock differs."),
            ("What if I want my cut to last instead?",
             "Flip the rule: cut on a waning Moon to slow regrowth and hold the shape longer. The dates above are chosen for growth, so for a lasting cut, aim for the opposite half of the lunar month."),
        ],
    },
]

if __name__ == "__main__":
    for cfg in PAGES:
        print("wrote", build(cfg) + ".html")
