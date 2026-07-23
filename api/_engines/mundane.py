# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/apps/twelve-rooms-studio/mundane.py
# Re-sync with bin/sync-engines.sh
"""Mundane weather: traditional-doctrine scoring for planet-to-planet
aspects, independent of any electional matter or natal chart.

Two tiers, not one flat pair list — verified against a real 30-year
crossing count before any weight was assigned (see
~/.claude/plans/wiggly-pondering-valiant.md for the full reasoning and the
two corrections that got this here). Mars and Jupiter make regular contact
with the slow outer planets (30-47+ exact crossings per 30 years) and are
NOT rare; only Saturn/Uranus/Neptune/Pluto aspecting each other are
genuinely rare (0-27 crossings per 30 years, several in single digits).

  Tier 1 — standing configurations (rare, sets the multi-year theme):
    Saturn, Uranus, Neptune, Pluto aspecting EACH OTHER. 6 pairs.
  Tier 2 — trigger contacts (frequent, marks the specific day/week):
    Sun, Mercury, Venus, Mars, Jupiter, each aspecting a Tier-1 body.
    20 pairs. Fast-to-fast aspects among Tier 2 bodies themselves are
    out of scope here — that's personal/daily-scale weather, not mundane.

The Moon is excluded entirely (monthly-scale noise at a yearly view).
Sect is excluded deliberately: it's a property of a chart cast for a
specific place, and this report is intentionally global/location-agnostic.
Quincunx/semisextile are excluded: the five Ptolemaic aspects are the
classical set; quincunx is a later, non-Hellenistic addition.

Tier 1 does NOT get a percentile-calibrated band — the rarest pairs here
(Neptune-Pluto, ~492yr cycle) have too few real occurrences in any
reasonable window for a percentile band to mean anything. Tier 1 events
report their real synodic cycle length instead. Tier 2 DOES get a
percentile-calibrated band (bin/calibrate_mundane_scale.py) since its
pairs have real sample sizes (30-47+ crossings per 30 years).
"""
import swisseph as swe
from datetime import datetime, timezone

import engines

TIER1 = {"Saturn", "Uranus", "Neptune", "Pluto"}
TIER2 = {"Sun", "Mercury", "Venus", "Mars", "Jupiter"}

TIER1_PAIRS = {frozenset({a, b}) for i, a in enumerate(TIER1)
               for b in list(TIER1)[i + 1:]}
TIER2_PAIRS = {frozenset({t2, t1}) for t2 in TIER2 for t1 in TIER1}

# Known synodic cycle lengths for the six Tier-1 pairs (years) — real
# orbital-mechanics facts, not calibration output.
SYNODIC_YEARS = {
    frozenset({"Saturn", "Uranus"}): 45,
    frozenset({"Saturn", "Neptune"}): 36,
    frozenset({"Saturn", "Pluto"}): 33,
    frozenset({"Uranus", "Neptune"}): 171,
    frozenset({"Uranus", "Pluto"}): 127,
    frozenset({"Neptune", "Pluto"}): 492,
}

# Traditional dignity/malefic-benefic weight. The three modern outers get
# a nature by standard mundane-astrology consensus (they postdate the
# classical system and have no Hellenistic dignity status).
PLANET_WEIGHT = {
    "Jupiter": 3, "Venus": 2, "Sun": 1, "Mercury": 0, "Mars": -2,
    "Uranus": -1, "Neptune": -1, "Pluto": -2, "Saturn": -3,
}

PLANET_THEME = {
    "Sun": "leadership, vitality, and collective identity",
    "Mercury": "communication, agreements, and information flow",
    "Venus": "relationship, finance, and shared values",
    "Mars": "conflict, assertion, and decisive action",
    "Jupiter": "expansion, opportunity, and confidence",
    "Saturn": "structure, restriction, and consequence",
    "Uranus": "disruption, innovation, and sudden change",
    "Neptune": "confusion, idealism, and the dissolving of boundaries",
    "Pluto": "power, upheaval, and crisis-driven transformation",
}

# Classical dynamic per aspect, on its own terms (not modern-psychological
# "internalized vs. externalized" framing). Conjunction has no fixed
# polarity in the tradition — handled separately in score_and_reason.
ASPECT_MULT = {"trine": 2.0, "sextile": 1.0, "square": -2.0, "opposition": -1.5}
ASPECT_DYNAMIC = {
    "trine": "flows easily",
    "sextile": "opens a supportive opportunity",
    "square": "forces friction and obstruction",
    "opposition": "polarizes toward confrontation and culmination",
}
ASPECT_ANGLES = {"conjunction": 0.0, "sextile": 60.0, "square": 90.0,
                  "trine": 120.0, "opposition": 180.0}


def score_and_reason(a, b, aspect):
    """(score, sentence) for one aspect between two named bodies.
    Order of a/b doesn't matter — combustion is detected by membership,
    not position."""
    if aspect == "conjunction":
        if "Sun" in (a, b):
            other = b if a == "Sun" else a
            score = -abs(PLANET_WEIGHT[other]) - 1
            sentence = (f"Sun conjunct {other}: {other} combust, its "
                        f"significations obscured rather than amplified.")
            return score, sentence
        score = PLANET_WEIGHT[a] + PLANET_WEIGHT[b]
        mixed = (PLANET_WEIGHT[a] > 0) != (PLANET_WEIGHT[b] > 0)
        tag = " — a complex, mixed blend of benefic and malefic" if mixed else ""
        sentence = (f"{a} conjunct {b}: fuses {PLANET_THEME[a]} and "
                    f"{PLANET_THEME[b]}{tag}.")
        return score, sentence

    mult = ASPECT_MULT[aspect]
    avg_severity = (abs(PLANET_WEIGHT[a]) + abs(PLANET_WEIGHT[b])) / 2
    score = mult * avg_severity
    sentence = (f"{a} {aspect} {b}: {ASPECT_DYNAMIC[aspect]} between "
                f"{PLANET_THEME[a]} and {PLANET_THEME[b]}.")
    return score, sentence


def _sep(lon_a, lon_b):
    d = abs(lon_a - lon_b) % 360.0
    return d if d <= 180.0 else 360.0 - d


def live_score(t_utc, lon_fn, orb=3.0):
    """Per-moment mundane check for electional.py: live longitudes for
    the nine bodies, every Tier-2-to-Tier-1 pair within orb, summed.
    Fast-to-fast pairs among Tier 2 excluded, matching mundane_year's
    scope. Returns (score, notes)."""
    bodies = TIER1 | TIER2
    lons = {p: lon_fn(t_utc, engines.cs.BODIES[p]) for p in bodies}
    score = 0.0
    notes = []
    for t2 in TIER2:
        for t1 in TIER1:
            sep = _sep(lons[t2], lons[t1])
            for aspect, ang in ASPECT_ANGLES.items():
                d = abs(sep - ang)
                if d <= orb:
                    s, sentence = score_and_reason(t2, t1, aspect)
                    score += s
                    notes.append(f"mundane: {sentence} ({d:.1f} deg orb)")
    return score, notes


# Tier-2 band thresholds, calibrated by bin/calibrate_mundane_scale.py
# against a real 2000-2030 distribution (n=3795 exact crossings across the
# 20 Tier-2 pairs) — same convention as electional.py's STAR_THRESHOLDS.
# Re-run that script if PLANET_WEIGHT/ASPECT_MULT ever change.
TIER2_BANDS = {"p15": -3.0, "p35": -2.0, "p70": 1.5, "p90": 3.0}


def band_for_score(score, bands=None):
    t = bands or TIER2_BANDS
    if score < t["p15"]:
        return "Harsh"
    if score < t["p35"]:
        return "Difficult"
    if score < t["p70"]:
        return "Mixed"
    if score < t["p90"]:
        return "Supportive"
    return "Excellent"


def mundane_year(start_date, end_date, tz):
    """Full traditional rundown for a date range: Tier-1 standing
    configurations (with real synodic cycle length, no fake band) and
    Tier-2 trigger contacts (calibrated band), plus informational
    stations and eclipse-flagged lunations. Returns a dict with
    'tier1', 'tier2', 'stations', 'lunations'."""
    bodies = list(TIER1 | TIER2)
    start_utc = datetime(start_date.year, start_date.month, start_date.day,
                          tzinfo=tz).astimezone(timezone.utc)
    end_utc = datetime(end_date.year, end_date.month, end_date.day,
                        tzinfo=tz).astimezone(timezone.utc)
    n_days = (end_utc - start_utc).days

    grid = engines.cr.daily_grid(start_utc, n_days, bodies)
    web = engines.cr.find_transit_web_exacts(start_utc, n_days, grid, tz)
    stations = engines.cr.find_stations(start_utc, n_days, grid, tz, bodies=bodies)
    lunations = engines.cr.find_lunations(start_utc, n_days, tz, None, [])

    tier1, tier2 = [], []
    for hit in web:
        a, b, aspect = hit["a"], hit["b"], hit["aspect"]
        pair = frozenset({a, b})
        if aspect not in ASPECT_ANGLES:
            continue  # quincunx/semisextile -- find_transit_web_exacts checks
                       # more than the five Ptolemaic aspects; out of scope here.
        if pair in TIER1_PAIRS:
            tier = 1
        elif pair in TIER2_PAIRS:
            tier = 2
        else:
            continue
        score, sentence = score_and_reason(a, b, aspect)
        ev = {"a": a, "b": b, "aspect": aspect, "score": round(score, 2),
              "sentence": sentence, "time_local": hit["time_local"],
              "retro_involved": hit["retro_involved"]}
        if tier == 1:
            ev["synodic_years"] = SYNODIC_YEARS.get(pair)
            tier1.append(ev)
        else:
            ev["band"] = band_for_score(score)
            tier2.append(ev)

    tier1.sort(key=lambda e: e["time_local"])
    tier2.sort(key=lambda e: e["time_local"])
    return {
        "start": start_date.isoformat(), "end": end_date.isoformat(),
        "tier1": tier1, "tier2": tier2,
        "stations": [s for s in stations if s["body"] in bodies],
        "lunations": lunations,
    }
