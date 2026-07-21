# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/ventures/astrology-storefront/factsheet/compute_factsheet.py
# Re-sync with bin/sync-engines.sh
#!/usr/bin/env python3
"""
compute_factsheet.py — per-order natal fact sheet generator for the storefront.

Given one client order (birth data), computes EVERYTHING the report generation
needs, so prose sections can cross-reference facts instead of inventing them:

  - natal positions (Sun..Pluto, Chiron if ephemeris allows, mean nodes),
    with retrograde flags and speeds
  - angles (ASC/MC) and whole-sign houses
  - natal aspects with orbs (luminary-widened), majors only
  - aspect patterns: stelliums, t-squares, grand trines, grand crosses
  - sect (day/night) + sect roles (light, benefic of sect, malefic contrary)
  - dignities-lite for the traditional seven (domicile/exaltation/detriment/fall)
  - element / mode / hemisphere balance
  - chart ruler and its condition
  - rulership chains for all twelve houses (occupants, ruler, where it went)
  - annual profection year (as of --asof) + year lord and its natal condition
  - current slow transits in orb (as of --asof), with transited natal house
  - exact slow-planet hits to natal points over the next 12 months (day precision)

No network. Deterministic. Uses the Moshier model (no data files needed).
Chiron requires Swiss Ephemeris asteroid files; when unavailable it is set to
null with a note — the report simply omits its section. NEVER fake Chiron.

No-time orders (--time omitted): positions computed at local noon, Moon given
as a day-range, no angles / houses / sect / profections. The JSON says exactly
what is missing so generation can stay honest.

Usage:
  python3 compute_factsheet.py --name "Avery Quinn" --date 1991-03-14 \
      --time 07:42 --tz America/Los_Angeles --lat 45.52 --lon -122.68 \
      --place "Portland, Oregon" [--asof 2026-07-17] [--md] > factsheet.json

  Or from an order file:  python3 compute_factsheet.py --order order.json --md
"""

import swisseph as swe
import json, argparse, sys
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo

FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
         "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
ELEMENT = dict(zip(SIGNS, ["Fire","Earth","Air","Water"]*3))
MODE = dict(zip(SIGNS, ["Cardinal","Fixed","Mutable"]*4))

PLANETS = {  # the ten, in traditional order
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
    "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}
SLOW = ["Jupiter","Saturn","Uranus","Neptune","Pluto"]

RULER = {"Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
         "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
         "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn",
         "Pisces":"Jupiter"}
MODERN_CORULER = {"Scorpio":"Pluto","Aquarius":"Uranus","Pisces":"Neptune"}
DOMICILE = {"Sun":["Leo"],"Moon":["Cancer"],"Mercury":["Gemini","Virgo"],
            "Venus":["Taurus","Libra"],"Mars":["Aries","Scorpio"],
            "Jupiter":["Sagittarius","Pisces"],"Saturn":["Capricorn","Aquarius"]}
EXALT = {"Sun":"Aries","Moon":"Taurus","Mercury":"Virgo","Venus":"Pisces",
         "Mars":"Capricorn","Jupiter":"Cancer","Saturn":"Libra"}
ASPECTS = {"conjunction":0,"sextile":60,"square":90,"trine":120,"opposition":180,
           "quincunx":150,"semisextile":30}
MAJORS = ("conjunction","sextile","square","trine","opposition")
# per-aspect base orb; quincunx/semisextile kept tight so only real ones surface
BASE_ORB = {"conjunction":7,"opposition":7,"square":7,"trine":7,"sextile":5,
            "quincunx":2.5,"semisextile":2.0}

HOUSE_MEANING = {
    1:"body, arrival, name", 2:"money, worth, appetite", 3:"mind, siblings, the near world",
    4:"home, roots, family", 5:"pleasure, creation, children", 6:"work, health, routine",
    7:"partnership, the other", 8:"shared resources, depth, loss", 9:"belief, distance, learning",
    10:"career, reputation, the public", 11:"friends, allies, the future", 12:"retreat, the unseen, undoing",
}

def sign_of(lon):
    lon %= 360.0
    return SIGNS[int(lon // 30)], lon % 30.0

def fmt_deg(lon):
    s, d = sign_of(lon)
    m = (d % 1) * 60
    return f"{int(d)}°{int(m):02d}' {s}"

def angdiff(a, b):
    """Smallest signed angular difference a-b in degrees, range (-180, 180]."""
    d = (a - b) % 360.0
    return d - 360.0 if d > 180.0 else d

def jd_ut(dt_utc):
    h = dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, h, swe.GREG_CAL)

def calc(jd, body, flags=FLAGS):
    (lon, lat, dist, splon, splat, spdist), _ = swe.calc_ut(jd, body, flags)
    return lon % 360.0, splon

def positions_at(jd):
    out = {}
    for name, body in PLANETS.items():
        lon, sp = calc(jd, body)
        out[name] = {"lon": lon, "speed": sp, "retrograde": sp < 0}
    lon, sp = calc(jd, swe.MEAN_NODE)
    out["North Node"] = {"lon": lon, "speed": sp, "retrograde": True}
    out["South Node"] = {"lon": (lon + 180) % 360, "speed": sp, "retrograde": True}
    try:  # Chiron needs seas_*.se1; absent under pure Moshier
        lon, sp = calc(jd, swe.CHIRON, swe.FLG_SWIEPH | swe.FLG_SPEED)
        out["Chiron"] = {"lon": lon, "speed": sp, "retrograde": sp < 0}
    except swe.Error:
        out["Chiron"] = None
    return out

def whole_sign_house(lon, rising_sign_idx):
    return (int((lon % 360) // 30) - rising_sign_idx) % 12 + 1

def natal_aspects(pos):
    """Majors between the ten planets + nodes-as-axis + angles handled elsewhere.
    Orbs: 7 deg (conj/sq/tr/opp), 5 deg sextile, +1 when Sun or Moon involved."""
    bodies = [b for b in list(PLANETS) + ["North Node","Chiron"] if pos.get(b)]
    found = []
    for i, a in enumerate(bodies):
        for b in bodies[i+1:]:
            if {a, b} == {"North Node", "South Node"}:
                continue
            for name, angle in ASPECTS.items():
                orb_max = BASE_ORB[name] + (1 if name in MAJORS and ("Sun" in (a,b) or "Moon" in (a,b)) else 0)
                if a in ("North Node","Chiron") or b in ("North Node","Chiron"):
                    orb_max = min(orb_max, 3)
                sep = abs(angdiff(pos[a]["lon"], pos[b]["lon"]))  # separation 0..180
                orb = abs(sep - angle)
                if orb <= orb_max:
                    found.append({"a": a, "b": b, "aspect": name,
                                  "orb": round(orb, 2), "tight": orb <= 2.0,
                                  "major": name in MAJORS})
    return sorted(found, key=lambda x: x["orb"])

def find_patterns(pos, aspects):
    pat = []
    # stelliums: 3+ of the ten in one sign
    by_sign = {}
    for p in PLANETS:
        s, _ = sign_of(pos[p]["lon"])
        by_sign.setdefault(s, []).append(p)
    for s, ps in by_sign.items():
        if len(ps) >= 3:
            pat.append({"type": "stellium", "sign": s, "planets": ps})
    def has(a, b, kind):
        return any(x for x in aspects if {x["a"], x["b"]} == {a, b} and x["aspect"] == kind)
    ten = list(PLANETS)
    # t-squares and grand crosses
    for i, a in enumerate(ten):
        for j, b in enumerate(ten[i+1:], i+1):
            if not has(a, b, "opposition"):
                continue
            for c in ten:
                if c in (a, b):
                    continue
                if has(a, c, "square") and has(b, c, "square"):
                    cross = [d for d in ten if d not in (a,b,c)
                             and has(c, d, "opposition") and has(a, d, "square") and has(b, d, "square")]
                    if cross:
                        pat.append({"type": "grand cross", "planets": sorted([a,b,c,cross[0]])})
                    else:
                        pat.append({"type": "t-square", "opposition": [a, b], "apex": c})
    # grand trines
    for i, a in enumerate(ten):
        for j, b in enumerate(ten[i+1:], i+1):
            for c in ten[j+1:]:
                if has(a,b,"trine") and has(b,c,"trine") and has(a,c,"trine"):
                    pat.append({"type": "grand trine", "planets": [a,b,c],
                                "element": ELEMENT[sign_of(pos[a]["lon"])[0]]})
    # dedupe grand crosses (t-squares subsumed) and identical entries
    seen, out = set(), []
    crosses = [frozenset(p["planets"]) for p in pat if p["type"] == "grand cross"]
    for p in pat:
        if p["type"] == "t-square" and any(set(p["opposition"] + [p["apex"]]) <= c for c in crosses):
            continue
        key = json.dumps(p, sort_keys=True)
        if key not in seen:
            seen.add(key); out.append(p)
    return out

def dignity(planet, sign):
    if planet not in DOMICILE:
        return None
    d = []
    if sign in DOMICILE[planet]: d.append("domicile")
    if EXALT.get(planet) == sign: d.append("exaltation")
    if any(SIGNS[(SIGNS.index(s)+6) % 12] == sign for s in DOMICILE[planet]): d.append("detriment")
    if EXALT.get(planet) and SIGNS[(SIGNS.index(EXALT[planet])+6) % 12] == sign: d.append("fall")
    return d or None

def condition(planet, pos, rising_idx, sect):
    lon = pos[planet]["lon"]
    sign, deg = sign_of(lon)
    c = {"sign": sign, "degree": round(deg, 2), "house": whole_sign_house(lon, rising_idx),
         "retrograde": pos[planet]["retrograde"], "dignities": dignity(planet, sign)}
    if sect and planet in ("Jupiter","Venus","Mars","Saturn"):
        benefic_of_sect = "Jupiter" if sect == "day" else "Venus"
        malefic_contrary = "Mars" if sect == "day" else "Saturn"
        if planet == benefic_of_sect: c["sect_role"] = "benefic of sect"
        elif planet == malefic_contrary: c["sect_role"] = "malefic contrary to sect"
    return c

# --- Timezone resolution -----------------------------------------------------
# IANA regional zones (America/Chicago, etc.) misapply DST to historical US
# births: before the Uniform Time Act (effective 1967) DST was local option and
# many places, Missouri included, did not observe it. IANA still stamps CDT on a
# 1965 date; the Shanks/ACS atlas (what astro.com uses) says CST. A one-hour
# error moves the Ascendant ~15 degrees and invalidates every house. So: never
# silently trust IANA for a pre-1967 US birth. Accept an explicit fixed offset
# that overrides IANA, and warn loudly when IANA is being trusted for a
# DST-ambiguous historical birth. See lessons.md ("Historical DST").
DST_ATLAS_YEAR = 1967


def _fmt_offset(td):
    if td is None:
        return "?"
    total = int(td.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    return f"UTC{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"


def resolve_tz(order):
    """Resolve the birth timezone, preferring an explicit fixed offset over IANA.

    order may carry:
      "utc_offset": -6         explicit fixed offset in hours; overrides IANA, no DST
      "tz": "Etc/GMT+6"        a fixed IANA zone (no DST; trusted as given)
      "tz": "America/Chicago"  a regional IANA zone (may misapply historical DST)
    Returns (tzinfo, label, is_fixed).
    """
    off = order.get("utc_offset")
    if off is not None:
        off = float(off)
        return timezone(timedelta(hours=off)), f"UTC{off:+g} (fixed offset)", True
    tz = order.get("tz")
    if not tz:
        raise SystemExit("order needs either 'utc_offset' (fixed hours) or 'tz'")
    zi = ZoneInfo(tz)
    fixed = tz in ("UTC", "GMT") or tz.startswith(("Etc/", "GMT+", "GMT-"))
    return zi, tz, fixed


def dst_ambiguity_warning(order, local, label, is_fixed):
    """Loud stderr warning when IANA is trusted for a DST-ambiguous historical
    birth. Returns a warning dict (also embedded in the fact sheet) or None.

    Fires for any pre-1967 birth on a regional zone (the atlas beats IANA there),
    and for any pre-1970 birth where IANA is actually applying DST (the classic
    error). Explicit fixed offsets are trusted and never warned."""
    if is_fixed:
        return None
    year = local.year
    dst_active = bool(local.dst())
    if not (year < DST_ATLAS_YEAR or (dst_active and year < 1970)):
        return None
    us_zone = label.startswith(("America/", "US/", "Canada/"))
    warn = {
        "kind": "historical_dst_ambiguity",
        "zone": label,
        "birth": f"{order['date']} {order.get('time', '')}".strip(),
        "iana_offset_at_birth": _fmt_offset(local.utcoffset()),
        "iana_applying_dst": dst_active,
        "action": ("verify Ascendant vs astro.com before writing; if off by ~1h "
                   "of time (~15deg of Asc), set utc_offset (e.g. -6) or tz "
                   "Etc/GMT+6 and regenerate everything."),
    }
    bar = "=" * 74
    msg = [
        "", bar,
        "  WARNING  historical DST / timezone ambiguity, do NOT trust IANA blindly",
        bar,
        f"  Birth : {warn['birth']}   zone '{label}'",
        f"  IANA  : offset {warn['iana_offset_at_birth']}"
        + ("   (DST is being applied)" if dst_active else "   (standard time)"),
    ]
    if us_zone:
        msg += [
            f"  Note  : US/North-America zone before {DST_ATLAS_YEAR}. The Uniform "
            "Time Act (effective",
            "          1967) is when US DST became uniform; earlier dates followed "
            "local practice,",
            "          which IANA does not model (Missouri did not observe DST in "
            "1965: CST).",
        ]
    else:
        msg += [
            "  Note  : pre-1970 birth on a regional zone. The Shanks/ACS atlas "
            "(what astro.com",
            "          uses) is the authority for historical local time and often "
            "disagrees.",
        ]
    msg += [
        "  A one-hour error moves the Ascendant ~15 degrees and invalidates every "
        "house.",
        "  ACTION: verify the Ascendant against astro.com BEFORE writing a word. "
        "If it",
        "          disagrees, set an explicit fixed offset in order.json:",
        '             "utc_offset": -6        (e.g. CST, no DST)',
        '          or  "tz": "Etc/GMT+6"      (same thing, an IANA fixed-offset '
        "zone)",
        "          then regenerate everything.",
        bar, "",
    ]
    sys.stderr.write("\n".join(msg) + "\n")
    return warn


def build_natal(order):
    tz, tz_label, tz_fixed = resolve_tz(order)
    timed = bool(order.get("time"))
    t = order.get("time") or "12:00"
    local = datetime.fromisoformat(f"{order['date']}T{t}:00").replace(tzinfo=tz)
    jd = jd_ut(local.astimezone(timezone.utc))
    pos = positions_at(jd)

    warn = dst_ambiguity_warning(order, local, tz_label, tz_fixed)
    natal = {"timed": timed, "birth_utc": local.astimezone(timezone.utc).isoformat(),
             "timezone": {"label": tz_label, "fixed_offset": tz_fixed,
                          "offset_at_birth": _fmt_offset(local.utcoffset()),
                          "dst_applied": bool(local.dst())},
             "warnings": [warn] if warn else []}
    rising_idx = None; sect = None
    if timed:
        cusps, ascmc = swe.houses_ex(jd, order["lat"], order["lon"], b'W', swe.FLG_MOSEPH)
        asc, mc = ascmc[0] % 360, ascmc[1] % 360
        rising_idx = int(asc // 30)
        below = 0 <= (pos["Sun"]["lon"] - asc) % 360 < 180
        sect = "night" if below else "day"
        natal.update({
            "asc": {"lon": asc, "pretty": fmt_deg(asc), "sign": SIGNS[rising_idx]},
            "mc": {"lon": mc, "pretty": fmt_deg(mc), "sign": sign_of(mc)[0],
                   "house": whole_sign_house(mc, rising_idx)},
            "sect": {"sect": sect,
                     "light": "Sun" if sect == "day" else "Moon",
                     "benefic_of_sect": "Jupiter" if sect == "day" else "Venus",
                     "malefic_contrary_to_sect": "Mars" if sect == "day" else "Saturn"},
            "chart_ruler": None,  # filled below
        })
    else:
        # Moon moves ~12-14 deg/day: report the day's range honestly
        jd0 = jd_ut(datetime.fromisoformat(f"{order['date']}T00:00:00").replace(tzinfo=tz).astimezone(timezone.utc))
        jd1 = jd_ut(datetime.fromisoformat(f"{order['date']}T23:59:00").replace(tzinfo=tz).astimezone(timezone.utc))
        natal["moon_day_range"] = {"start": fmt_deg(calc(jd0, swe.MOON)[0]),
                                   "end": fmt_deg(calc(jd1, swe.MOON)[0])}
        natal["missing_because_untimed"] = ["asc","mc","houses","sect","profections","chart_ruler"]

    planets = {}
    for p in list(PLANETS) + ["North Node","South Node","Chiron"]:
        if pos.get(p) is None:
            planets[p] = None
            continue
        lon = pos[p]["lon"]
        entry = {"lon": round(lon, 4), "pretty": fmt_deg(lon),
                 "sign": sign_of(lon)[0], "degree": round(sign_of(lon)[1], 2),
                 "retrograde": pos[p]["retrograde"]}
        if p in PLANETS:
            entry["dignities"] = dignity(p, entry["sign"])
        if timed:
            entry["house"] = whole_sign_house(lon, rising_idx)
            entry["house_meaning"] = HOUSE_MEANING[entry["house"]]
        planets[p] = entry
    natal["planets"] = planets
    if pos.get("Chiron") is None:
        natal["chiron_note"] = "Chiron unavailable (needs Swiss Ephemeris asteroid files). Omit the Chiron section; never improvise it."

    aspects = natal_aspects(pos)
    if timed:  # aspects to angles, tight orb
        for point, lon_a in (("ASC", natal["asc"]["lon"]), ("MC", natal["mc"]["lon"])):
            for p in PLANETS:
                for name, angle in ASPECTS.items():
                    orb = abs(abs(angdiff(pos[p]["lon"], lon_a)) - angle)
                    cap = 3 if name in MAJORS else 2
                    if orb <= cap:
                        aspects.append({"a": p, "b": point, "aspect": name,
                                        "orb": round(orb, 2), "tight": orb <= 1.5,
                                        "major": name in MAJORS})
        rs = SIGNS[rising_idx]
        ruler = RULER[rs]
        natal["chart_ruler"] = {"planet": ruler, **condition(ruler, pos, rising_idx, sect)}
        if rs in MODERN_CORULER:
            co = MODERN_CORULER[rs]
            natal["chart_ruler"]["modern_coruler"] = {"planet": co, **condition(co, pos, rising_idx, sect)}
    natal["aspects"] = sorted(aspects, key=lambda x: x["orb"])
    natal["patterns"] = find_patterns(pos, natal["aspects"])

    # focal planets: bodies wired into the most other points (aspect web).
    # A tightly, widely-aspected planet is a switchboard for the whole chart.
    deg = {}
    for asp in natal["aspects"]:
        for who in (asp["a"], asp["b"]):
            if who in PLANETS:
                deg.setdefault(who, []).append(
                    {"aspect": asp["aspect"], "other": asp["b"] if who == asp["a"] else asp["a"],
                     "orb": asp["orb"], "major": asp.get("major", True)})
    focal = sorted(deg.items(), key=lambda kv: (-len(kv[1]), min(a["orb"] for a in kv[1])))
    natal["aspect_web"] = [{"planet": p, "contacts": sorted(v, key=lambda x: x["orb"])}
                           for p, v in focal if len(v) >= 4]

    counts = {"element": {}, "mode": {}}
    weigh = list(PLANETS) + (["ASC"] if timed else [])
    for p in weigh:
        s = natal["asc"]["sign"] if p == "ASC" else planets[p]["sign"]
        counts["element"][ELEMENT[s]] = counts["element"].get(ELEMENT[s], 0) + 1
        counts["mode"][MODE[s]] = counts["mode"].get(MODE[s], 0) + 1
    if timed:
        asc = natal["asc"]["lon"]
        hemis = {"above_horizon": 0, "below_horizon": 0, "east": 0, "west": 0}
        for p in PLANETS:
            rel = (pos[p]["lon"] - asc) % 360
            hemis["below_horizon" if rel < 180 else "above_horizon"] += 1
            hemis["east" if (rel < 90 or rel >= 270) else "west"] += 1
        counts["hemispheres"] = hemis
    natal["balance"] = counts

    if timed:
        houses = {}
        for h in range(1, 13):
            s = SIGNS[(rising_idx + h - 1) % 12]
            ruler = RULER[s]
            houses[h] = {"sign": s, "meaning": HOUSE_MEANING[h],
                         "occupants": [p for p in PLANETS if planets[p]["house"] == h],
                         "ruler": ruler,
                         "ruler_in": {"sign": planets[ruler]["sign"],
                                      "house": planets[ruler]["house"],
                                      "house_meaning": planets[ruler]["house_meaning"]}}
            if s in MODERN_CORULER:
                co = MODERN_CORULER[s]
                houses[h]["modern_coruler_in"] = {"planet": co, "sign": planets[co]["sign"],
                                                  "house": planets[co]["house"]}
        natal["houses"] = houses
    return natal, pos, rising_idx, sect, jd

def profection(order, natal, asof):
    born = date.fromisoformat(order["date"])
    age = asof.year - born.year - ((asof.month, asof.day) < (born.month, born.day))
    house = age % 12 + 1
    rising_idx = SIGNS.index(natal["asc"]["sign"])
    sign = SIGNS[(rising_idx + house - 1) % 12]
    lord = RULER[sign]
    nxt = born.replace(year=asof.year if (asof.month, asof.day) < (born.month, born.day) else asof.year + 1)
    return {"age": age, "activated_house": house, "house_meaning": HOUSE_MEANING[house],
            "activated_sign": sign, "year_lord": lord,
            "year_lord_natal": natal["planets"][lord],
            "runs_until_birthday": nxt.isoformat()}

def current_transits(natal, rising_idx, asof):
    jd = jd_ut(datetime(asof.year, asof.month, asof.day, 12, tzinfo=timezone.utc))
    targets = {p: natal["planets"][p]["lon"] for p in PLANETS if natal["planets"].get(p)}
    if natal.get("asc"):
        targets["ASC"] = natal["asc"]["lon"]; targets["MC"] = natal["mc"]["lon"]
    hits, retro = [], []
    for tp in SLOW:
        lon, sp = calc(jd, PLANETS[tp])
        if sp < 0:
            retro.append(tp)
        entry_house = whole_sign_house(lon, rising_idx) if rising_idx is not None else None
        for tgt, tlon in targets.items():
            for name, angle in ASPECTS.items():
                if name not in MAJORS:
                    continue
                orb = abs(abs(angdiff(lon, tlon)) - angle)
                if orb <= (2 if name == "sextile" else 3):
                    hits.append({"transiting": tp, "pretty": fmt_deg(lon),
                                 "aspect": name, "natal_point": tgt,
                                 "orb": round(orb, 2), "transiting_house": entry_house,
                                 "retrograde": sp < 0})
    return sorted(hits, key=lambda x: x["orb"]), retro

def upcoming_hits(natal, asof, months=12, outer_sextiles=True):
    """Day-precision exact aspect dates, slow planets to natal points, next N months.
    outer_sextiles=True includes Uranus/Neptune/Pluto sextiles (they are real,
    multi-year contacts); set False to trim them from a shorter reading."""
    targets = {p: natal["planets"][p]["lon"] for p in PLANETS if natal["planets"].get(p)}
    if natal.get("asc"):
        targets["ASC"] = natal["asc"]["lon"]; targets["MC"] = natal["mc"]["lon"]
    days = int(months * 30.44)
    daily = {tp: [] for tp in SLOW}
    for i in range(days + 1):
        d = asof + timedelta(days=i)
        jd = jd_ut(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))
        for tp in SLOW:
            daily[tp].append(calc(jd, PLANETS[tp])[0])
    out = []
    for tp in SLOW:
        lons = daily[tp]
        for tgt, tlon in targets.items():
            for name, angle in ASPECTS.items():
                if name not in MAJORS:
                    continue
                if name == "sextile" and tp in ("Uranus","Neptune","Pluto") and not outer_sextiles:
                    continue
                # an aspect is exact at separation +angle OR -angle around the
                # circle; scan both branches (0 and 180 have only one)
                for ta in ({angle} if angle in (0, 180) else {angle, 360 - angle}):
                    prev = angdiff(lons[0] - tlon, ta)
                    for i in range(1, len(lons)):
                        cur = angdiff(lons[i] - tlon, ta)
                        if prev == 0 or (prev < 0) != (cur < 0):
                            if abs(cur) < 1.5 and abs(prev) < 1.5:  # true crossing, not wraparound
                                out.append({"date": (asof + timedelta(days=i)).isoformat(),
                                            "transiting": tp, "aspect": name, "natal_point": tgt})
                        prev = cur
    return sorted(out, key=lambda x: x["date"])

def build_calendar(natal, rising_idx, asof, slow_hits, months=12):
    """Month-by-month event calendar: lunations (with natal house), retrograde
    and direct stations, Venus/Mars conjunctions to natal points, plus the
    slow-planet exact hits. Each event carries a priority; the writer takes
    the top 3 per month."""
    days = int(months * 30.44) + 2
    bodies = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
              "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
              "Saturn": swe.SATURN}
    daily = {b: [] for b in bodies}
    for i in range(days + 1):
        d = asof + timedelta(days=i)
        jd = jd_ut(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))
        for b, code in bodies.items():
            daily[b].append(calc(jd, code))
    targets = {p: natal["planets"][p]["lon"] for p in PLANETS if natal["planets"].get(p)}
    if natal.get("asc"):
        targets["ASC"] = natal["asc"]["lon"]; targets["MC"] = natal["mc"]["lon"]
    ANGULAR = (1, 4, 7, 10)
    events = []

    def house_of(lon):
        return whole_sign_house(lon, rising_idx) if rising_idx is not None else None

    # lunations: new moon when elongation wraps 360->0, full when it crosses 180
    elong = [(daily["Moon"][i][0] - daily["Sun"][i][0]) % 360 for i in range(days + 1)]
    for i in range(1, days + 1):
        d = (asof + timedelta(days=i)).isoformat()
        kind = None
        if elong[i] < elong[i - 1]:
            kind = "new moon"
        elif elong[i - 1] < 180 <= elong[i]:
            kind = "full moon"
        if not kind:
            continue
        mlon = daily["Moon"][i][0]
        h = house_of(mlon)
        on_natal = min(((p, abs(angdiff(mlon, t))) for p, t in targets.items()),
                       key=lambda x: x[1])
        prio = 45 + (20 if h in ANGULAR else 0)
        ev = {"date": d, "kind": kind, "sign": sign_of(mlon)[0],
              "degree": int(sign_of(mlon)[1]), "natal_house": h, "priority": prio}
        if on_natal[1] <= 3:
            ev["on_natal"] = on_natal[0]; ev["priority"] = 78
        events.append(ev)

    # stations: speed sign change (Mercury..Saturn)
    for b in ("Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
        for i in range(1, days + 1):
            s0, s1 = daily[b][i - 1][1], daily[b][i][1]
            if s0 == 0 or (s0 < 0) == (s1 < 0):
                continue
            kind = "stations retrograde" if s1 < 0 else "stations direct"
            lon = daily[b][i][0]
            events.append({"date": (asof + timedelta(days=i)).isoformat(),
                           "kind": f"{b} {kind}", "sign": sign_of(lon)[0],
                           "degree": int(sign_of(lon)[1]), "natal_house": house_of(lon),
                           "priority": 85 if b in ("Jupiter", "Saturn") else 70})

    # Venus / Mars conjunctions to natal points
    for b, prio in (("Venus", 50), ("Mars", 60)):
        lons = [daily[b][i][0] for i in range(days + 1)]
        for tgt, tlon in targets.items():
            prev = angdiff(lons[0], tlon)
            for i in range(1, len(lons)):
                cur = angdiff(lons[i], tlon)
                if (prev < 0) != (cur < 0) and abs(cur) < 2 and abs(prev) < 2:
                    events.append({"date": (asof + timedelta(days=i)).isoformat(),
                                   "kind": f"{b} conjoins natal {tgt}",
                                   "natal_house": house_of(lons[i]),
                                   "priority": prio + (10 if tgt in ("ASC", "MC", "Sun", "Moon") else 0)})
                prev = cur

    # slow-planet exact hits (highest priority, the year's spine)
    for h in slow_hits:
        prio = 100
        if h["transiting"] == "Jupiter" and h["natal_point"] == "Jupiter" and h["aspect"] == "conjunction":
            prio = 120  # a return
        events.append({"date": h["date"],
                       "kind": f"{h['transiting']} {h['aspect']} natal {h['natal_point']} (exact)",
                       "priority": prio})

    months_out = []
    by_month = {}
    for ev in events:
        by_month.setdefault(ev["date"][:7], []).append(ev)
    for m in sorted(by_month):
        top = sorted(by_month[m], key=lambda e: (-e["priority"], e["date"]))[:3]
        months_out.append({"month": m, "events": sorted(top, key=lambda e: e["date"])})
    return months_out

def render_md(fs):
    n = fs["natal"]; L = []
    L.append(f"# Fact sheet: {fs['order']['name']}")
    L.append(f"{fs['order']['date']} {fs['order'].get('time') or '(no birth time)'} · {fs['order'].get('place','')} · whole-sign houses")
    tzinfo = n.get("timezone")
    if tzinfo:
        src = "fixed offset" if tzinfo["fixed_offset"] else "IANA zone"
        L.append(f"Timezone: {tzinfo['label']} ({src}), birth offset {tzinfo['offset_at_birth']}"
                 + (", DST applied" if tzinfo["dst_applied"] else ""))
    for w in n.get("warnings", []):
        L.append(f"\n**WARNING ({w['kind']}):** IANA offset {w['iana_offset_at_birth']} for "
                 f"{w['birth']} in '{w['zone']}'. {w['action']}")
    if n["timed"]:
        L.append(f"\n**{n['sect']['sect'].upper()} chart** · light: {n['sect']['light']} · benefic of sect: {n['sect']['benefic_of_sect']} · malefic contrary: {n['sect']['malefic_contrary_to_sect']}")
        L.append(f"**Rising** {n['asc']['pretty']} · **MC** {n['mc']['pretty']} (house {n['mc']['house']})")
        cr = n["chart_ruler"]
        L.append(f"**Chart ruler** {cr['planet']}: {cr['sign']} {cr['degree']}°, house {cr['house']}" + (f", {', '.join(cr['dignities'])}" if cr.get("dignities") else ""))
    L.append("\n## Planets")
    for p, e in n["planets"].items():
        if e is None:
            L.append(f"- {p}: unavailable"); continue
        row = f"- **{p}** {e['pretty']}"
        if e.get("house"): row += f" · house {e['house']} ({e['house_meaning']})"
        if e.get("retrograde") and p not in ("North Node","South Node"): row += " · Rx"
        if e.get("dignities"): row += f" · {', '.join(e['dignities'])}"
        L.append(row)
    L.append("\n## Tightest aspects")
    for a in [x for x in n["aspects"] if x["tight"]][:14]:
        L.append(f"- {a['a']} {a['aspect']} {a['b']} (orb {a['orb']}°)")
    if n["patterns"]:
        L.append("\n## Patterns")
        for p in n["patterns"]:
            L.append(f"- {json.dumps(p)}")
    L.append(f"\n## Balance\n- {json.dumps(n['balance'])}")
    if n.get("houses"):
        L.append("\n## The twelve rooms")
        for h, e in n["houses"].items():
            occ = ", ".join(e["occupants"]) or "empty"
            L.append(f"- **{h}** ({e['sign']}, {e['meaning']}): {occ} · ruler {e['ruler']} sits in house {e['ruler_in']['house']} ({e['ruler_in']['house_meaning']})")
    if fs.get("profection"):
        pr = fs["profection"]
        L.append(f"\n## Current chapter (as of {fs['asof']})")
        L.append(f"- Age {pr['age']}: a **house-{pr['activated_house']} profection year** ({pr['house_meaning']}), {pr['activated_sign']}, year lord **{pr['year_lord']}**, until {pr['runs_until_birthday']}")
    if fs.get("transits_in_orb"):
        L.append("\n## Slow transits in orb now")
        for t in fs["transits_in_orb"]:
            L.append(f"- {t['transiting']} {t['aspect']} natal {t['natal_point']} (orb {t['orb']}°{', Rx' if t['retrograde'] else ''})")
    if fs.get("upcoming_exact_hits"):
        L.append("\n## Exact hits, next 12 months")
        for t in fs["upcoming_exact_hits"]:
            L.append(f"- {t['date']}: {t['transiting']} {t['aspect']} natal {t['natal_point']}")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", help="JSON file: name,date,time,tz,lat,lon,place")
    ap.add_argument("--name"); ap.add_argument("--date"); ap.add_argument("--time")
    ap.add_argument("--tz"); ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float)
    ap.add_argument("--place", default="")
    ap.add_argument("--asof", default=date.today().isoformat())
    ap.add_argument("--md", action="store_true", help="also write factsheet.md next to stdout JSON")
    a = ap.parse_args()

    if a.order:
        order = json.load(open(a.order))
    else:
        need = [k for k in ("name","date","tz","lat","lon") if getattr(a, k) is None]
        if need:
            ap.error("missing: " + ", ".join(need))
        order = {"name": a.name, "date": a.date, "time": a.time, "tz": a.tz,
                 "lat": a.lat, "lon": a.lon, "place": a.place}
    asof = date.fromisoformat(a.asof)

    natal, pos, rising_idx, sect, jd = build_natal(order)
    fs = {"order": order, "asof": asof.isoformat(), "natal": natal}
    if natal.get("warnings"):
        fs["warnings"] = natal["warnings"]
    if natal["timed"]:
        fs["profection"] = profection(order, natal, asof)
    fs["transits_in_orb"], fs["current_retrogrades"] = current_transits(natal, rising_idx, asof)
    fs["upcoming_exact_hits"] = upcoming_hits(natal, asof)
    fs["calendar_12mo"] = build_calendar(natal, rising_idx, asof, fs["upcoming_exact_hits"])
    fs["method"] = ("Whole-sign houses. Sect-aware. Positions: Swiss Ephemeris (Moshier model), "
                    "computed, never remembered. Orbs: 7° majors / 5° sextile, +1° luminaries, "
                    "3° nodes-Chiron-angles. Transit orbs 3° (sextile 2°).")
    print(json.dumps(fs, indent=1))
    if a.md:
        sys.stderr.write(render_md(fs) + "\n")

if __name__ == "__main__":
    main()
