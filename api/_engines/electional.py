# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/apps/twelve-rooms-studio/electional.py
# Re-sync with bin/sync-engines.sh
"""Electional window scanner.

Precompute range facts (Moon ingresses, Moon-planet perfections, VoC
intervals, planetary hours, retro flags), then step-scan the allowed
local hours: hard rules gate a moment, soft rules score it. Contiguous
passing steps merge into windows; edges snap to the precomputed exact
boundary (VoC start, ingress, hour change) when one binds.

User-agnostic: charts arrive as order dicts, location as lat/lon/tz.
"""
import calendar
import swisseph as swe
from datetime import datetime, timedelta, timezone, date as date_cls
from zoneinfo import ZoneInfo

import engines
import mundane

SIGNS = engines.cs.SIGNS
PTOLEMAIC = {"conjunction": 0.0, "sextile": 60.0, "square": 90.0,
             "trine": 120.0, "opposition": 180.0}
VOC_BODIES = {"Sun": swe.SUN, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
              "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN}
PLANET_CODE = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
               "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
               "Saturn": swe.SATURN, "Uranus": swe.URANUS,
               "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO}
CHALDEAN = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
DAY_RULER = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter", 4: "Venus",
             5: "Saturn", 6: "Sun"}
MAX_DAYS = 92
APPLYING_HOURS = 13  # Moon orb ~6 deg at ~0.5 deg/h

# ---- Election recipe library (single source of truth; see
# ventures/astrology-storefront/electional-methodology.md for the doctrine).
# Traditional scoring: Moon applies to the benefic of the matter, avoids
# the malefic that spoils it, in a friendly hour with a benefic angular,
# under the right light. moon_not_voc is prepended to every recipe.
SOFT_ASP = ["trine", "sextile", "conjunction"]
HARD_ASP = ["square", "opposition", "conjunction"]
ANG = ["ASC", "MC"]


def _r(key, label, category, applies, avoid, hours, phase,
       angular=("Venus", "Jupiter"), retro=None, moon_in=None,
       moon_avoid_signs=None, moon_bonus=None, avoid_asp=None,
       apply_w=3, avoid_w=-3,
       # Traditional-dignity pilot (venture cluster only; see
       # electional-methodology.md, "What the tool gates vs what the
       # reading adds"). None = recipe is untouched, byte-identical to
       # before this pilot.
       dignity_planets=None, dignity_w=2.5, malefic_angle_w=-3,
       sect_pref=None, sect_w=2, asc_ruler_w=2):
    hard = [{"rule": "moon_not_voc"}]
    if retro:
        hard.append({"rule": "planet_not_retrograde", "planets": retro})
    if moon_in:
        hard.append({"rule": "moon_sign_in", "signs": moon_in})
    if moon_avoid_signs:
        hard.append({"rule": "moon_sign_avoid", "signs": moon_avoid_signs})
    soft = [
        {"rule": "moon_applying_aspect", "to": applies, "aspects": SOFT_ASP, "weight": apply_w},
        {"rule": "moon_avoid_aspect", "to": avoid, "aspects": avoid_asp or HARD_ASP, "weight": avoid_w},
        {"rule": "planetary_hour_ruler", "rulers": hours, "weight": 2},
    ]
    if angular:
        soft.append({"rule": "benefic_on_angle", "planets": list(angular), "angles": ANG, "orb": 5, "weight": 2})
    if phase == "waxing":
        soft.append({"rule": "moon_waxing", "weight": 2})
    elif phase == "waning":
        soft.append({"rule": "moon_waning", "weight": 2})
    if moon_bonus:
        soft.append({"rule": "moon_sign_bonus", "signs": moon_bonus, "weight": 1})
    if dignity_planets:
        soft.append({"rule": "planet_dignity", "planets": list(dignity_planets), "weight": dignity_w})
        soft.append({"rule": "malefic_on_angle", "planets": list(avoid), "angles": ANG, "orb": 5, "weight": malefic_angle_w})
        soft.append({"rule": "asc_ruler_dignity", "weight": asc_ruler_w})
        if sect_pref:
            soft.append({"rule": "sect_bonus", "sect": sect_pref, "weight": sect_w})
    return {"key": key, "label": label, "category": category, "hard": hard, "soft": soft}


RECIPES = [
    # Love, union, family
    _r("wedding", "Wedding / marriage", "Love",
       ["Venus", "Jupiter"], ["Mars", "Saturn"], ["Venus", "Jupiter"], "waxing",
       retro=["Venus", "Mercury"], moon_bonus=["Taurus"], avoid_w=-4),
    _r("engagement", "Engagement / proposal", "Love",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus"], "waxing",
       angular=("Venus",), retro=["Venus"]),
    _r("first_date", "First date / new relationship", "Love",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus"], "waxing",
       angular=("Venus",), retro=["Venus"]),
    _r("reconciliation", "Reconciliation / mending", "Love",
       ["Venus", "Jupiter", "Mercury"], ["Mars", "Saturn"], ["Venus", "Mercury"], "waxing",
       angular=("Venus",), avoid_w=-4),
    _r("conception", "Trying to conceive", "Love",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus", "Jupiter"], "waxing",
       moon_in=["Cancer", "Scorpio", "Pisces"]),
    # Venus is the primary significator (sociability, pleasure, aesthetics),
    # not Jupiter -- and unlike every other recipe here, night suits this
    # matter better than day: Venus is the nocturnal sect benefic, and most
    # parties are evening events anyway. First recipe where sect_pref
    # points away from the day/Jupiter pattern for a real traditional
    # reason, not an oversight.
    _r("party", "Party / celebration", "Love",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus", "Jupiter"], "waxing",
       angular=("Venus", "Jupiter"),
       dignity_planets=["Venus"], sect_pref="night"),
    # Money, work, enterprise
    _r("business", "Starting a business", "Work",
       ["Jupiter", "Mercury", "Sun"], ["Saturn", "Mars"], ["Jupiter", "Mercury", "Sun"], "waxing",
       angular=("Jupiter",), retro=["Mercury"],
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("contract", "Signing a contract", "Work",
       ["Mercury", "Jupiter"], ["Mars", "Saturn"], ["Mercury", "Jupiter"], "waxing",
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("launch", "Product launch / going live", "Work",
       ["Jupiter", "Sun"], ["Saturn", "Mars"], ["Sun", "Jupiter"], "waxing",
       angular=("Sun", "Jupiter"),
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("job", "Job interview / new job", "Work",
       ["Sun", "Jupiter", "Mercury"], ["Saturn", "Mars"], ["Sun", "Jupiter", "Mercury"], "waxing",
       angular=("Jupiter",), retro=["Mercury"],
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("raise", "Raise / salary negotiation", "Work",
       ["Jupiter", "Venus"], ["Saturn", "Mars"], ["Jupiter", "Venus"], "waxing",
       angular=("Jupiter",), avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("shop", "Opening a shop / restaurant", "Work",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus", "Jupiter"], "waxing",
       retro=["Mercury"],
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("investment", "Investment / opening an account", "Work",
       ["Jupiter", "Venus"], ["Saturn", "Mars"], ["Jupiter", "Venus"], "waxing",
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
    # Private (studio-only, never in PUBLIC_KEYS): traditional financial-venture
    # timing. Reflective astrology, NOT a market forecast or trading advice.
    _r("financial_venture", "Financial venture / speculation", "Work",
       ["Jupiter", "Venus", "Mercury"], ["Mars", "Saturn"], ["Mercury", "Jupiter"], "waxing",
       angular=("Jupiter", "Venus"), retro=["Mercury"], avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
    # Private (studio-only, never in PUBLIC_KEYS): same significators as
    # financial_venture but waning, not waxing -- selling/closing a
    # position is a release, not a beginning, the same principle behind
    # surgery/diet's waning phase. Reflective astrology, NOT a market
    # forecast or trading advice.
    _r("sell_stock", "Sell stock / close a position", "Work",
       ["Jupiter", "Venus", "Mercury"], ["Mars", "Saturn"], ["Mercury", "Jupiter"], "waning",
       angular=("Jupiter", "Venus"), retro=["Mercury"], avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
    _r("publishing", "Publishing / book launch", "Work",
       ["Jupiter", "Mercury", "Sun"], ["Saturn", "Mars"], ["Mercury", "Jupiter", "Sun"], "waxing",
       angular=("Jupiter", "Sun"), retro=["Mercury"],
       dignity_planets=["Jupiter"], sect_pref="day"),
    # Home, movement, property
    _r("home", "Buying / moving into a home", "Home",
       ["Venus", "Jupiter"], ["Mars", "Saturn"], ["Venus", "Moon"], "waxing",
       moon_bonus=["Taurus", "Leo", "Scorpio", "Aquarius"]),
    _r("relocation", "Relocation / new city", "Home",
       ["Jupiter", "Venus"], ["Saturn", "Mars"], ["Jupiter", "Moon"], "waxing",
       moon_bonus=["Aries", "Cancer", "Libra", "Capricorn", "Gemini", "Virgo", "Sagittarius", "Pisces"]),
    _r("car", "Buying a car / major purchase", "Home",
       ["Venus", "Jupiter"], ["Mars", "Saturn"], ["Mercury", "Venus"], "waxing",
       retro=["Mercury"], apply_w=2),
    # Body, health, self
    _r("surgery", "Surgery / operation", "Health",
       ["Jupiter", "Venus"], ["Mars", "Saturn"], ["Sun", "Jupiter"], "waning",
       angular=("Jupiter", "Venus"), avoid_w=-4, apply_w=2),
    _r("diet", "Diet / breaking a habit", "Health",
       ["Saturn", "Sun"], ["Jupiter", "Venus"], ["Saturn", "Sun"], "waning",
       angular=None, apply_w=2, avoid_w=-1),
    _r("haircut", "Haircut (grow)", "Health",
       ["Venus", "Jupiter"], ["Mars", "Saturn"], ["Venus", "Moon"], "waxing",
       angular=("Venus",), apply_w=2, avoid_w=-2),
    # Conflict
    _r("lawsuit", "Lawsuit / legal action", "Conflict",
       ["Jupiter", "Sun"], ["Saturn", "Mars"], ["Jupiter", "Sun"], "waxing",
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4,
       dignity_planets=["Jupiter"], sect_pref="day"),
]
# Mundane weather (Saturn/Uranus/Neptune/Pluto standing configurations,
# triggered by Sun/Mercury/Venus/Mars/Jupiter — see mundane.py) applies to
# every matter equally, not just a subset of recipes, so it's appended
# here rather than threaded through _r() as another opt-in kwarg.
for _r_entry in RECIPES:
    _r_entry["soft"] = _r_entry["soft"] + [{"rule": "mundane_aspect"}]
del _r_entry
RECIPES_BY_KEY = {r["key"]: r for r in RECIPES}


# ---------- The Twelve Rooms Timing Scale (star rating) ----------
# A raw peak_score means nothing on its own (a wedding scan and a
# haircut scan don't share a ceiling), so every window is read against
# how strong its OWN recipe's windows actually run over time. Star
# thresholds are empirically calibrated, not guessed: bin/
# calibrate_timing_scale.py scanned 5 years (2024-2028) of sky-only
# windows per recipe, at the geographic center of the contiguous US, and
# set the boundaries at the 15th/35th/70th/90th percentile of that
# recipe's own real score distribution (n=471-1851 windows per recipe;
# full distribution in calibration_data.json). 3 stars = average on
# purpose: it is the widest band (35th-70th percentile) because most
# windows for most matters ARE ordinary. 5 stars sits in the top decile
# deliberately, so it stays a real distinction and not grade inflation.
# Re-run the calibration whenever a recipe's rule weights change in
# RECIPES above.
#
# Known artifact: a few recipes (diet, publishing, car, surgery,
# haircut) have so few distinct achievable raw scores that two
# percentile boundaries land on the same value. When that happens, that
# star rating simply never occurs for that recipe (e.g. haircut has no
# 4-star windows in 5 years of data; diet and publishing have no
# 2-star). This reflects those recipes having fewer stacking rules, not
# a calibration bug.
STAR_THRESHOLDS = {
    "wedding": {"p15": 0.85, "p35": 3.5, "p70": 8.0, "p90": 11.5},
    "engagement": {"p15": -0.5, "p35": 2.5, "p70": 7.0, "p90": 10.5},
    "first_date": {"p15": -0.5, "p35": 2.5, "p70": 7.0, "p90": 10.5},
    "reconciliation": {"p15": 0.0, "p35": 3.0, "p70": 7.5, "p90": 11.0},
    "conception": {"p15": 1.0, "p35": 3.5, "p70": 8.0, "p90": 12.0},
    "party": {"p15": 2.5, "p35": 5.9, "p70": 10.5, "p90": 14.5},
    "business": {"p15": 2.99, "p35": 6.5, "p70": 11.0, "p90": 15.0},
    "contract": {"p15": 2.0, "p35": 6.0, "p70": 10.0, "p90": 14.0},
    "launch": {"p15": 2.8, "p35": 6.5, "p70": 11.0, "p90": 15.0},
    "job": {"p15": 2.99, "p35": 6.5, "p70": 11.0, "p90": 15.0},
    "raise": {"p15": 2.0, "p35": 6.0, "p70": 10.5, "p90": 14.5},
    "shop": {"p15": 2.8, "p35": 6.5, "p70": 10.5, "p90": 15.0},
    "investment": {"p15": 2.0, "p35": 6.0, "p70": 10.0, "p90": 14.0},
    "financial_venture": {"p15": 3.0, "p35": 6.5, "p70": 11.0, "p90": 15.0},
    "sell_stock": {"p15": 2.5, "p35": 6.5, "p70": 11.0, "p90": 15.0},
    "publishing": {"p15": 3.5, "p35": 7.2, "p70": 11.5, "p90": 15.5},
    "home": {"p15": 1.0, "p35": 4.0, "p70": 8.0, "p90": 12.0},
    "relocation": {"p15": 1.0, "p35": 4.0, "p70": 8.5, "p90": 12.5},
    "car": {"p15": 0.0, "p35": 3.0, "p70": 7.0, "p90": 10.8},
    "surgery": {"p15": 0.0, "p35": 3.0, "p70": 7.5, "p90": 11.5},
    "diet": {"p15": -1.0, "p35": 2.0, "p70": 6.5, "p90": 10.5},
    "haircut": {"p15": 0.0, "p35": 3.0, "p70": 7.0, "p90": 10.5},
    "lawsuit": {"p15": 2.0, "p35": 6.0, "p70": 10.0, "p90": 14.0},
}

# Plain-word labels (the comprehensible layer) plus the room name (the
# named, ownable layer) for each star count, worst to best.
STAR_LABELS = {
    1: {"label": "Weak", "room_name": "Threshold",
        "blurb": "Little traditional support, in the bottom 15% of five"
                 " years of this election's windows; some 1-star windows"
                 " have the Moon actively applying toward what spoils"
                 " this matter. Usable only if nothing better is on the"
                 " calendar."},
    2: {"label": "Below Average", "room_name": "Open Door",
        "blurb": "Fewer of the traditional supports than usual for this"
                 " matter, though the Moon is clear of the spoilers."},
    3: {"label": "Average", "room_name": "Lit Room",
        "blurb": "A typical window for this matter, the most common"
                 " outcome, neither rare nor weak."},
    4: {"label": "Good", "room_name": "Full House",
        "blurb": "Solidly stronger than the ordinary window for this"
                 " matter, in the top 30%."},
    5: {"label": "Excellent", "room_name": "Every Window Open",
        "blurb": "As strong as this election gets: the top 10% of five"
                 " years of this election's windows."},
}


# Separate calibration for "best dates this year": that feature shows
# only the single strongest window per month (scan_year, below), and a
# max-of-~20 is structurally almost always near the top of the ALL-
# windows distribution above. Comparing it to STAR_THRESHOLDS made every
# month of a 12-month scan come back 5-star in testing, useless as a
# scale. This is calibrated instead against the distribution of monthly
# maxima themselves (n=60, one per month across the same 5 years).
# Consequence, also real: a handful of recipes (diet in particular) hit
# their monthly-best ceiling in nearly every month, so the annual view
# will often show 5 stars across the board for those specific matters.
# That is the honest finding, not a bug to smooth away, but the plain
# scan of that same recipe (STAR_THRESHOLDS) still spreads normally.
STAR_THRESHOLDS_MONTHLY = {
    "wedding": {"p15": 8.0, "p35": 11.15, "p70": 14.29, "p90": 17.55},
    "engagement": {"p15": 7.42, "p35": 10.5, "p70": 13.65, "p90": 17.6},
    "first_date": {"p15": 7.42, "p35": 10.5, "p70": 13.65, "p90": 17.6},
    "reconciliation": {"p15": 9.0, "p35": 11.82, "p70": 14.65, "p90": 17.6},
    "conception": {"p15": 7.0, "p35": 9.5, "p70": 12.86, "p90": 16.0},
    "party": {"p15": 11.97, "p35": 14.5, "p70": 17.65, "p90": 20.55},
    "business": {"p15": 10.5, "p35": 14.15, "p70": 17.5, "p90": 19.7},
    "contract": {"p15": 10.0, "p35": 13.5, "p70": 17.0, "p90": 19.6},
    "launch": {"p15": 12.93, "p35": 14.82, "p70": 18.15, "p90": 22.5},
    "job": {"p15": 10.5, "p35": 14.15, "p70": 17.5, "p90": 19.7},
    "raise": {"p15": 12.43, "p35": 14.32, "p70": 17.0, "p90": 20.6},
    "shop": {"p15": 10.5, "p35": 13.5, "p70": 17.65, "p90": 20.05},
    "investment": {"p15": 10.0, "p35": 13.5, "p70": 16.65, "p90": 20.05},
    "financial_venture": {"p15": 11.7, "p35": 14.32, "p70": 18.0, "p90": 20.05},
    "sell_stock": {"p15": 12.0, "p35": 14.5, "p70": 18.5, "p90": 21.05},
    "publishing": {"p15": 10.93, "p35": 14.5, "p70": 18.15, "p90": 21.15},
    "home": {"p15": 9.76, "p35": 12.82, "p70": 15.5, "p90": 18.1},
    "relocation": {"p15": 10.43, "p35": 13.0, "p70": 15.65, "p90": 19.0},
    "car": {"p15": 6.85, "p35": 9.39, "p70": 13.5, "p90": 16.55},
    "surgery": {"p15": 9.0, "p35": 10.7, "p70": 15.0, "p90": 18.55},
    "diet": {"p15": 7.42, "p35": 9.82, "p70": 13.06, "p90": 16.5},
    "haircut": {"p15": 7.92, "p35": 10.5, "p70": 13.65, "p90": 17.1},
    "lawsuit": {"p15": 10.43, "p35": 13.13, "p70": 16.5, "p90": 19.7},
}


def stars_for_score(score, recipe_key, population="window"):
    """1-5 star rating for a window's peak_score, calibrated per recipe.
    population="window" (default) compares against all qualifying
    windows, the population a plain scan or the public tool shows.
    population="monthly_best" compares against the distribution of
    monthly maxima, for scan_year's one-per-month display. Returns None
    if recipe_key wasn't calibrated (e.g. a fully custom scan not built
    from one of the RECIPES presets)."""
    table = STAR_THRESHOLDS_MONTHLY if population == "monthly_best" else STAR_THRESHOLDS
    t = table.get(recipe_key)
    if not t:
        return None
    if score < t["p15"]:
        stars = 1
    elif score < t["p35"]:
        stars = 2
    elif score < t["p70"]:
        stars = 3
    elif score < t["p90"]:
        stars = 4
    else:
        stars = 5
    info = STAR_LABELS[stars]
    return {"stars": stars, "label": info["label"],
            "room_name": info["room_name"], "blurb": info["blurb"]}


jd_ut = engines.cs.jd_ut
body_lonspeed = engines.cs.body_lonspeed
signed_delta = engines.cs.signed_delta

# Traditional-dignity pilot: reuse compute_factsheet's tables/functions rather
# than reinventing them. NOTE engines.cf.whole_sign_house(lon, rising_idx) has
# a different signature from engines.cs.whole_sign_house — always use this one.
cf_dignity = engines.cf.dignity
cf_whole_sign_house = engines.cf.whole_sign_house
RULER = engines.cf.RULER


def _lon(dt_utc, code):
    return body_lonspeed(jd_ut(dt_utc), code)[0]


def _bisect(t0, t1, fn, iters=20):
    """fn flips sign between t0 and t1; return the crossing time."""
    f0 = fn(t0)
    for _ in range(iters):
        mid = t0 + (t1 - t0) / 2
        if (fn(mid) < 0) == (f0 < 0):
            t0 = mid
            f0 = fn(mid)
        else:
            t1 = mid
    return t1


# ---------- range precomputation ----------

def moon_ingresses(start_utc, end_utc):
    """[(dt_utc, new_sign_idx)] across the range, 10-min scan + bisect."""
    out = []
    step = timedelta(minutes=10)
    t = start_utc
    prev = int(_lon(t, swe.MOON) // 30)
    while t < end_utc:
        t2 = min(t + step, end_utc)
        cur = int(_lon(t2, swe.MOON) // 30)
        if cur != prev:
            hit = _bisect(t, t2, lambda x, p=prev: -1 if int(_lon(x, swe.MOON) // 30) == p else 1)
            out.append((hit, cur))
            prev = cur
        else:
            prev = cur
        t = t2
    return out


def moon_perfections(start_utc, end_utc, step_min=15):
    """Exact Moon-to-planet Ptolemaic aspects, both bodies live.
    [(dt_utc, planet, aspect)] sorted."""
    hits = []
    step = timedelta(minutes=step_min)
    targets = [(p, a, ang) for p in VOC_BODIES for a, ang in PTOLEMAIC.items()]

    def deltas(t):
        mlon = _lon(t, swe.MOON)
        plons = {p: _lon(t, code) for p, code in VOC_BODIES.items()}
        out = []
        for p, a, ang in targets:
            d = signed_delta(mlon, plons[p] + ang)
            d2 = signed_delta(mlon, plons[p] - ang) if ang not in (0.0, 180.0) else None
            out.append((d, d2))
        return out

    t = start_utc
    prev = deltas(t)
    while t < end_utc:
        t2 = min(t + step, end_utc)
        cur = deltas(t2)
        for i, (p, a, ang) in enumerate(targets):
            for branch, off in ((0, ang), (1, -ang)):
                d0 = prev[i][branch]
                d1 = cur[i][branch]
                if d0 is None or d1 is None:
                    continue
                if (d0 < 0) != (d1 < 0) and abs(d0) < 8 and abs(d1) < 8:
                    hit = _bisect(t, t2, lambda x, p_=p, o=off:
                                  signed_delta(_lon(x, swe.MOON),
                                               _lon(x, VOC_BODIES[p_]) + o))
                    hits.append((hit, p, a))
        prev = cur
        t = t2
    hits.sort(key=lambda h: h[0])
    return hits


def voc_intervals(start_utc, end_utc, ingresses, perfections):
    """[(voc_start, voc_end)] — from the Moon's last Ptolemaic perfection
    before each ingress until the ingress itself."""
    out = []
    for ing_dt, _sign in ingresses:
        before = [h[0] for h in perfections if h[0] < ing_dt]
        voc_start = max(before) if before else start_utc
        if voc_start < ing_dt:
            out.append((voc_start, ing_dt))
    return out


def planetary_hours_range(start_local, days, tz, lat, lon):
    """{date_iso: {'day_ruler', 'hours': [(start_utc, end_utc, ruler)]}}.
    Same algorithm as compute_sky.planetary_hours but returns datetimes."""
    def sun_event(jd_from, rsmi):
        res, tret = swe.rise_trans(jd_from, swe.SUN, rsmi | swe.BIT_DISC_CENTER,
                                   (lon, lat, 0.0), 0.0, 0.0, swe.FLG_MOSEPH)
        if res != 0:
            raise RuntimeError("no rise/set")
        y, m, d, ut = swe.revjul(tret[0], swe.GREG_CAL)
        hh = int(ut)
        mm = (ut - hh) * 60
        return datetime(y, m, d, hh, int(mm), int((mm % 1) * 60), tzinfo=timezone.utc)

    out = {}
    for i in range(days):
        the_date = (start_local + timedelta(days=i)).date()
        day0 = datetime(the_date.year, the_date.month, the_date.day, tzinfo=tz)
        jd0 = jd_ut(day0.astimezone(timezone.utc))
        sunrise = sun_event(jd0, swe.CALC_RISE)
        sunset = sun_event(jd_ut(sunrise), swe.CALC_SET)
        next_rise = sun_event(jd_ut(sunset), swe.CALC_RISE)
        ruler = DAY_RULER[the_date.weekday()]
        start_idx = CHALDEAN.index(ruler)
        day_len = (sunset - sunrise) / 12
        night_len = (next_rise - sunset) / 12
        hours = []
        for k in range(24):
            t0 = sunrise + day_len * k if k < 12 else sunset + night_len * (k - 12)
            t1 = t0 + (day_len if k < 12 else night_len)
            hours.append((t0, t1, CHALDEAN[(start_idx + k) % 7]))
        out[the_date.isoformat()] = {"day_ruler": ruler, "hours": hours}
    return out


def hour_ruler_at(hour_tables, dt_utc, tz):
    """Planetary-hour ruler at a moment. A local calendar day's early hours
    belong to the previous planetary day, so check today then yesterday."""
    local_day = dt_utc.astimezone(tz).date()
    for day in (local_day, local_day - timedelta(days=1)):
        tab = hour_tables.get(day.isoformat())
        if not tab:
            continue
        for t0, t1, ruler in tab["hours"]:
            if t0 <= dt_utc < t1:
                return ruler, t0, t1
    return None, None, None


# ---------- criteria ----------

def validate(criteria):
    rng = criteria["range"]
    start = date_cls.fromisoformat(rng["start"])
    end = date_cls.fromisoformat(rng["end"])
    if end < start:
        raise ValueError("range end before start")
    if (end - start).days + 1 > MAX_DAYS:
        raise ValueError(f"range capped at {MAX_DAYS} days")
    loc = criteria["location"]
    tz = ZoneInfo(loc["tz"])
    return {
        "start": start, "end": end, "tz": tz,
        "lat": float(loc["lat"]), "lon": float(loc["lon"]),
        "earliest": criteria.get("hours", {}).get("earliest", "07:00"),
        "latest": criteria.get("hours", {}).get("latest", "22:00"),
        "step": int(criteria.get("step_minutes", 10)),
        "top_n": int(criteria.get("top_n", 10)),
        "min_window": int(criteria.get("min_window_minutes", 30)),
        "hard": criteria.get("hard", []),
        "soft": criteria.get("soft", []),
    }


def _natal_targets(chart_order):
    natal, pos, rising_idx, sect, jd = engines.cf.build_natal(chart_order)
    targets = {p: natal["planets"][p]["lon"] for p in PLANET_CODE
               if natal["planets"].get(p)}
    if natal.get("asc"):
        targets["ASC"] = natal["asc"]["lon"]
        targets["MC"] = natal["mc"]["lon"]
    return targets


# ---------- the scan ----------

def scan(criteria, get_chart=None, recipe_key=None, population="window"):
    c = validate(criteria)
    tz = c["tz"]
    days = (c["end"] - c["start"]).days + 1
    start_local = datetime(c["start"].year, c["start"].month, c["start"].day, tzinfo=tz)
    end_local = start_local + timedelta(days=days)
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)

    # precompute
    ingresses = moon_ingresses(start_utc - timedelta(hours=30), end_utc + timedelta(hours=30))
    perfections = moon_perfections(start_utc - timedelta(hours=30), end_utc + timedelta(hours=30))
    vocs = voc_intervals(start_utc - timedelta(hours=60), end_utc, ingresses, perfections)
    needs_hours = any(r["rule"] == "planetary_hour_ruler" for r in c["soft"])
    hour_tables = planetary_hours_range(start_local - timedelta(days=1), days + 2,
                                        tz, c["lat"], c["lon"]) if needs_hours else {}
    retro_by_day = {}
    for i in range(days + 1):
        d = c["start"] + timedelta(days=i)
        jd = jd_ut(datetime(d.year, d.month, d.day, 12, tzinfo=tz).astimezone(timezone.utc))
        retro_by_day[d.isoformat()] = {
            p: body_lonspeed(jd, code)[1] < 0 for p, code in PLANET_CODE.items()
            if p not in ("Sun", "Moon")}

    natal_cache = {}
    for rule in c["hard"] + c["soft"]:
        if rule["rule"] == "transit_to_natal":
            cid = rule["natal_chart"]
            if cid not in natal_cache:
                if get_chart is None:
                    raise ValueError("transit_to_natal needs a chart library")
                chart = get_chart(cid)
                if not chart:
                    raise ValueError(f"unknown chart {cid}")
                natal_cache[cid] = _natal_targets(chart["order"])

    ANGLE_RULES = ("benefic_on_angle", "malefic_on_angle", "asc_ruler_dignity", "sect_bonus")
    needs_angles = any(r["rule"] in ANGLE_RULES for r in c["hard"] + c["soft"])
    eh, em = map(int, c["earliest"].split(":"))
    lh, lm = map(int, c["latest"].split(":"))

    def next_perfection(t, planets, aspects):
        for hdt, p, a in perfections:
            if hdt <= t:
                continue
            if hdt - t > timedelta(hours=APPLYING_HOURS):
                break
            if p in planets and a in aspects:
                ing = next((idt for idt, _ in ingresses if idt > t), None)
                if ing is None or hdt < ing:
                    return hdt, p, a
        return None

    def in_voc(t):
        return any(v0 <= t < v1 for v0, v1 in vocs)

    def evaluate(t_utc):
        """Returns (passes_hard, score, notes) for one moment."""
        local = t_utc.astimezone(tz)
        day_iso = local.date().isoformat()
        mlon, mspeed = body_lonspeed(jd_ut(t_utc), swe.MOON)
        slon = _lon(t_utc, swe.SUN)
        moon_sign = SIGNS[int(mlon // 30)]
        waxing = 0 < (mlon - slon) % 360 < 180
        notes = []
        score = 0.0

        for rule in c["hard"]:
            r = rule["rule"]
            if r == "moon_not_voc":
                if in_voc(t_utc):
                    return False, 0, []
            elif r == "moon_sign_in":
                if moon_sign not in rule["signs"]:
                    return False, 0, []
            elif r == "moon_sign_avoid":
                if moon_sign in rule["signs"]:
                    return False, 0, []
            elif r == "planet_not_retrograde":
                flags = retro_by_day.get(day_iso, {})
                if any(flags.get(p) for p in rule["planets"]):
                    return False, 0, []
            else:
                raise ValueError(f"unknown hard rule {r}")

        angles = None
        if needs_angles:
            cusps, ascmc = swe.houses_ex(jd_ut(t_utc), c["lat"], c["lon"], b'W',
                                         swe.FLG_MOSEPH)
            angles = {"ASC": ascmc[0] % 360, "MC": ascmc[1] % 360}

        for rule in c["soft"]:
            r = rule["rule"]
            w = float(rule.get("weight", 1))
            if r == "planetary_hour_ruler":
                ruler, h0, h1 = hour_ruler_at(hour_tables, t_utc, tz)
                if ruler in rule["rulers"]:
                    score += w
                    notes.append(f"{ruler} hour")
            elif r in ("moon_applying_aspect", "moon_avoid_aspect"):
                hit = next_perfection(t_utc, set(rule["to"]), set(rule["aspects"]))
                if hit:
                    hdt, p, a = hit
                    score += w
                    verb = "applying" if r == "moon_applying_aspect" else "applying (avoid)"
                    notes.append(f"Moon {verb} {a} {p}, exact "
                                 f"{hdt.astimezone(tz).strftime('%a %-I:%M %p')}")
            elif r == "benefic_on_angle":
                orb = float(rule.get("orb", 5))
                for p in rule["planets"]:
                    plon = _lon(t_utc, PLANET_CODE[p])
                    for ang_name in rule.get("angles", ["ASC", "MC"]):
                        d = abs(signed_delta(plon, angles[ang_name]))
                        if d <= orb:
                            score += w
                            notes.append(f"{p} on {ang_name} ({d:.1f} deg)")
            elif r == "malefic_on_angle":
                # Mirrors benefic_on_angle but penalizes: "keep Saturn away
                # from exactly conjoining the Ascendant degree" (Brennan &
                # Schaim, repeated through the 2025 report).
                orb = float(rule.get("orb", 5))
                for p in rule["planets"]:
                    plon = _lon(t_utc, PLANET_CODE[p])
                    for ang_name in rule.get("angles", ["ASC", "MC"]):
                        d = abs(signed_delta(plon, angles[ang_name]))
                        if d <= orb:
                            score += w  # w is negative for this rule
                            notes.append(f"{p} on {ang_name} ({d:.1f} deg) [avoid]")
            elif r == "planet_dignity":
                # Essential dignity of a named significator: domicile/
                # exaltation score up, detriment/fall score down. This is
                # the direct fix for a planet like Jupiter exalted in
                # Cancer scoring even when it isn't sitting on an angle.
                for p in rule["planets"]:
                    plon = _lon(t_utc, PLANET_CODE[p])
                    sign = SIGNS[int(plon // 30)]
                    dig = cf_dignity(p, sign)
                    if not dig:
                        continue
                    if "domicile" in dig or "exaltation" in dig:
                        score += w
                        notes.append(f"{p} {dig[0]} in {sign}")
                    if "detriment" in dig or "fall" in dig:
                        score -= w
                        notes.append(f"{p} {dig[-1]} in {sign} [avoid]")
            elif r == "sect_bonus":
                # Day/night chart of the electional moment itself. Jupiter
                # is the diurnal benefic, so Jupiter-led elections favor a
                # day chart — the soft version of the report's recurring
                # "essential to make sure the Sun is above the Ascendant."
                below = 0 <= (slon - angles["ASC"]) % 360 < 180
                sect = "night" if below else "day"
                if sect == rule["sect"]:
                    score += w
                    notes.append(f"{sect} chart")
            elif r == "asc_ruler_dignity":
                # Moment-level analogue of build_natal()'s chart_ruler
                # condition: how strong is THIS chart's own Ascendant ruler.
                rising_idx = int(angles["ASC"] // 30)
                ruler = RULER[SIGNS[rising_idx]]
                rlon = _lon(t_utc, PLANET_CODE[ruler])
                rsign = SIGNS[int(rlon // 30)]
                dig = cf_dignity(ruler, rsign)
                if dig and ("domicile" in dig or "exaltation" in dig):
                    score += w
                    notes.append(f"Asc ruler {ruler} {dig[0]} in {rsign}")
                rhouse = cf_whole_sign_house(rlon, rising_idx)
                if rhouse in (1, 4, 7, 10):
                    score += w
                    notes.append(f"Asc ruler {ruler} angular (house {rhouse})")
            elif r == "mundane_aspect":
                m_score, m_notes = mundane.live_score(t_utc, _lon)
                score += m_score
                notes += m_notes
            elif r == "transit_to_natal":
                targets = natal_cache[rule["natal_chart"]]
                tp = rule["transit"]
                plon = _lon(t_utc, PLANET_CODE[tp])
                orb = float(rule.get("orb", 3))
                for pt in ([rule["natal_point"]] if isinstance(rule.get("natal_point"), str)
                           else rule.get("natal_points", list(targets))):
                    if pt not in targets:
                        continue
                    for a in rule["aspects"]:
                        ang = PTOLEMAIC[a]
                        d = abs(abs(signed_delta(plon, targets[pt])) - ang) \
                            if ang in (0.0, 180.0) else \
                            min(abs(signed_delta(plon, targets[pt] + ang)),
                                abs(signed_delta(plon, targets[pt] - ang)))
                        if d <= orb:
                            score += w
                            notes.append(f"{tp} {a} natal {pt} ({d:.1f} deg)")
            elif r == "moon_waxing":
                if waxing:
                    score += w
                    notes.append("Moon waxing")
            elif r == "moon_waning":
                if not waxing:
                    score += w
                    notes.append("Moon waning")
            elif r == "moon_sign_bonus":
                if moon_sign in rule["signs"]:
                    score += w
                    notes.append(f"Moon in {moon_sign}")
            else:
                raise ValueError(f"unknown soft rule {r}")

        return True, score, notes

    # step scan within allowed local hours
    step = timedelta(minutes=c["step"])
    moments = []
    for i in range(days):
        day = start_local + timedelta(days=i)
        t = day.replace(hour=eh, minute=em)
        day_end = day.replace(hour=lh, minute=lm)
        while t <= day_end:
            t_utc = t.astimezone(timezone.utc)
            ok, score, notes = evaluate(t_utc)
            moments.append((t_utc, ok, score, notes))
            t += step

    # merge contiguous passing steps into windows
    windows = []
    cur = None
    for t_utc, ok, score, notes in moments:
        if ok:
            if cur and t_utc - cur["last"] <= step:
                cur["last"] = t_utc
                if score > cur["peak"]:
                    cur["peak"] = score
                    cur["peak_at"] = t_utc
                    cur["peak_notes"] = notes
                cur["scores"].append(score)
            else:
                if cur:
                    windows.append(cur)
                cur = {"first": t_utc, "last": t_utc, "peak": score,
                       "peak_at": t_utc, "peak_notes": notes, "scores": [score]}
        else:
            if cur:
                windows.append(cur)
                cur = None
    if cur:
        windows.append(cur)

    # snap edges to exact boundaries when one binds
    def snap(w):
        start, end = w["first"], w["last"] + step
        day_close = w["last"].astimezone(tz).replace(hour=lh, minute=lm)\
            .astimezone(timezone.utc)
        end = min(end, day_close)
        for v0, v1 in vocs:
            if start - step < v1 <= start:
                start = v1                      # window opened when VoC ended
            if end <= v0 < end + step:
                end = v0                        # window closed when VoC began
        for idt, _s in ingresses:
            if end <= idt < end + step:
                end = idt
        return start, end

    out = []
    for w in windows:
        start, end = snap(w)
        dur = (end - start).total_seconds() / 60
        if dur < c["min_window"]:
            continue
        mid = w["peak_at"]
        mlon = _lon(mid, swe.MOON)
        slon = _lon(mid, swe.SUN)
        exact_inside = [
            {"time": h[0].astimezone(tz).strftime("%a %b %-d %-I:%M %p"),
             "what": f"Moon {h[2]} {h[1]} exact"}
            for h in perfections if start <= h[0] < end]
        receipts = {
            "moon_sign": SIGNS[int(mlon // 30)],
            "moon_phase": "waxing" if 0 < (mlon - slon) % 360 < 180 else "waning",
            "voc_free": not any(v0 < end and start < v1 for v0, v1 in vocs),
            "peak_notes": w["peak_notes"],
            "exact_aspects_inside": exact_inside,
        }
        if needs_hours:
            spans = []
            t = start
            while t < end:
                ruler, h0, h1 = hour_ruler_at(hour_tables, t, tz)
                if ruler is None:
                    break
                seg_end = min(h1, end)
                spans.append({"ruler": ruler,
                              "from": t.astimezone(tz).strftime("%-I:%M %p"),
                              "to": seg_end.astimezone(tz).strftime("%-I:%M %p")})
                t = seg_end
            receipts["planetary_hours"] = spans
        out.append({
            "start": start.astimezone(tz).isoformat(timespec="minutes"),
            "end": end.astimezone(tz).isoformat(timespec="minutes"),
            "start_pretty": start.astimezone(tz).strftime("%a %b %-d, %-I:%M %p"),
            "end_pretty": end.astimezone(tz).strftime("%-I:%M %p"),
            "duration_min": int(dur),
            "peak_score": round(w["peak"], 1),
            "peak_at": mid.astimezone(tz).strftime("%-I:%M %p"),
            "receipts": receipts,
            "scale": stars_for_score(w["peak"], recipe_key, population),
        })

    out.sort(key=lambda w: (-w["peak_score"], -w["duration_min"]))
    return {"windows": out[:c["top_n"]],
            "scanned_days": days,
            "total_windows": len(out),
            "voc_intervals": [
                {"from": v0.astimezone(tz).strftime("%a %b %-d %-I:%M %p"),
                 "to": v1.astimezone(tz).strftime("%a %b %-d %-I:%M %p")}
                for v0, v1 in vocs if v1 > start_utc]}


# ---------- annual "best dates of the year" ----------

SIGN_THE = {"ASC": "Ascendant", "MC": "Midheaven"}


def explain(window):
    """One-sentence rationale for a chosen window, built from its receipts.
    Note strings come from scan() in known formats, so parsing is safe."""
    r = window["receipts"]
    asp = None
    angles = []
    hour = None
    natal = []
    dignities = []
    sect = None
    for n in r.get("peak_notes", []):
        if n.startswith("Moon applying (avoid)") or n.endswith("[avoid]"):
            continue
        if n.startswith("Moon applying "):
            body = n[len("Moon applying "):].split(", exact")[0].split()
            if len(body) >= 2:
                asp = f"a {body[0]} to {body[1]}"
        elif n.endswith("hour"):
            hour = n[:-5].strip()  # "Jupiter"
        elif n.endswith("chart") and ("day" in n or "night" in n):
            sect = n  # "day chart" / "night chart"
        elif " on ASC" in n or " on MC" in n:
            planet, _, rest = n.partition(" on ")
            ang = rest.split(" (")[0]
            angles.append(f"{planet} on the {SIGN_THE.get(ang, ang)}")
        elif n.startswith("Asc ruler"):
            dignities.append(n)
        elif "natal" in n:
            natal.append(n.split(" (")[0])
        elif " in " in n and (" domicile " in f" {n} " or " exaltation " in f" {n} "):
            dignities.append(n)
    lead = f"The {r['moon_phase']} Moon in {r['moon_sign']}"
    if asp:
        sentence = f"{lead} applies to {asp}"
    else:
        sentence = f"{lead} holds clear of the hard aspects and is not void"
    tail = []
    tail += [f"with {a}" for a in angles]
    tail += dignities
    if sect:
        tail.append(sect)
    if hour:
        tail.append(f"in a {hour} hour")
    tail += natal
    if tail:
        sentence += ", " + ", ".join(tail)
    return sentence + "."


def scan_year(recipe, location, hours=None, asof=None, months=12,
              extra_soft=None, get_chart=None):
    """Best window in each of the next `months` calendar months.
    Returns [{month, ...window fields, why}] with None-window months flagged."""
    asof = asof or date_cls.today()
    out = []
    y, m = asof.year, asof.month
    for _ in range(months):
        last = calendar.monthrange(y, m)[1]
        start = f"{y:04d}-{m:02d}-01"
        end = f"{y:04d}-{m:02d}-{last:02d}"
        crit = {
            "range": {"start": start, "end": end},
            "location": location,
            "hours": hours or {"earliest": "07:00", "latest": "21:00"},
            "step_minutes": 15, "top_n": 1,
            "hard": [dict(x) for x in recipe["hard"]],
            "soft": [dict(x) for x in recipe["soft"]] + (extra_soft or []),
        }
        res = scan(crit, get_chart=get_chart, recipe_key=recipe["key"], population="monthly_best")
        label = datetime(y, m, 1).strftime("%B %Y")
        if res["windows"]:
            w = res["windows"][0]
            w["month"] = label
            w["why"] = explain(w)
            out.append(w)
        else:
            out.append({"month": label, "none": True,
                        "why": "No window this month clears the requirements; "
                               "widen the hours or consider the neighboring months."})
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out
