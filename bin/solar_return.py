#!/usr/bin/env python3
"""solar_return.py — solar return chart + birthday-to-birthday year engine.

Given one birth (date, time, zone, place) and a return year, computes every
fact a solar-return reading needs, so the written reading can cross-reference
numbers instead of inventing them:

  - the exact solar-return moment (Sun back to its natal longitude, to the second)
  - the return chart: positions, retro flags, whole-sign houses from the return
    Ascendant, angles, sect, dignities, chart ruler, Lots of Fortune and Spirit,
    in-chart aspects, planetary day and hour, Sabian symbol of every point
  - overlays: return planets in the natal houses, natal planets in the return
    houses, return-to-natal aspects (tight orbs), planetary returns
  - the year, birthday to birthday: ingresses, stations, Mercury shadows,
    lunations with eclipse flags, transit perfections to every natal point with
    retrograde pass numbering, slow-transit "in orb" windows, sensitive-degree
    windows, the annual profection
  - a daily ledger for every day of the year: Moon sign, phase, void-of-course
    share of the working day, Moon perfections, planetary day, and the local
    windows when a chosen rising sign is on the Ascendant (electional rule)
  - every day of the year scored and RANKED for a library of occasions
    (money, career, love, family, body, spirit, home), each with a best local
    window and a plain-language "why"

No network. Deterministic. Swiss Ephemeris (Moshier model, no data files).
Chiron needs the asteroid files; pass --chiron "Taurus 13°49'" to supply a
verified natal Chiron instead, otherwise it is simply omitted. Never faked.

Usage:
  python3 bin/solar_return.py --date 1979-09-02 --time 01:43 --tz America/Chicago \
      --lat 38.5833 --lon -92.1667 --place "Jefferson City, MO" --year 2026 \
      [--sr-lat .. --sr-lon .. --sr-tz ..]  (relocated return) > sr.json
"""
import sys, json, argparse, math, importlib
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_engines"))
sys.path.insert(0, str(ROOT / "bin"))

import swisseph as swe
import engines                      # noqa: F401  (wires cs / cf / gen_wheel)
import compute_factsheet as cf
import compute_sky as cs
import electional as el
import mundane

FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED
SIGNS = cf.SIGNS
RULER = cf.RULER
ELEMENT = cf.ELEMENT
MODE = cf.MODE
HOUSE_MEANING = cf.HOUSE_MEANING
BODIES = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
          "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
          "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
          "North Node": swe.MEAN_NODE}
TRANSITING = ["Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
FAST = {"Sun", "Mercury", "Venus", "Mars"}
SLOW = ["Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
ASPECTS = {"conjunction": 0, "sextile": 60, "square": 90, "trine": 120,
           "opposition": 180, "quincunx": 150}
# Shannon-standard transit/synastry orbs: conj/opp <=5, trine/sextile <=4, square <=4, quincunx <=2
TIGHT_ORB = {"conjunction": 5, "opposition": 5, "trine": 4, "sextile": 4, "square": 4, "quincunx": 2}
SOFT = {"trine", "sextile"}
HARD = {"square", "opposition"}
CHALDEAN = el.CHALDEAN
DAY_RULER = el.DAY_RULER
ECL_TYPES = [(swe.ECL_TOTAL, "total"), (swe.ECL_ANNULAR_TOTAL, "hybrid"),
             (swe.ECL_ANNULAR, "annular"), (swe.ECL_PARTIAL, "partial"),
             (swe.ECL_PENUMBRAL, "penumbral")]

# ---------------------------------------------------------------- helpers

def norm(a): return a % 360.0
def sdelta(a, b): return (a - b + 180.0) % 360.0 - 180.0   # signed arc from b to a
def sep(a, b): return abs(sdelta(a, b))
def sign_of(lon): return cf.sign_of(lon)
def fmt(lon): return cf.fmt_deg(lon)
def jd_of(dt_utc): return cf.jd_ut(dt_utc)

def dt_of(jd):
    y, m, d, ut = swe.revjul(jd, swe.GREG_CAL)
    h = int(ut); mi = int((ut - h) * 60); s = int(round(((ut - h) * 60 - mi) * 60))
    if s == 60: s = 59
    return datetime(y, m, d, h, mi, s, tzinfo=timezone.utc)

def lonspeed(jd, body):
    xx, _ = swe.calc_ut(jd, body, FLAGS)
    return norm(xx[0]), xx[3]

def lon_at(dt_utc, body): return lonspeed(jd_of(dt_utc), body)[0]

def bisect_time(t0, t1, fn, iters=24):
    """fn changes sign between t0 and t1 (datetimes); return the crossing."""
    f0 = fn(t0)
    for _ in range(iters):
        mid = t0 + (t1 - t0) / 2
        fm = fn(mid)
        if (fm < 0) == (f0 < 0):
            t0, f0 = mid, fm
        else:
            t1 = mid
    return t1

def whole_sign_house(lon, rising_idx): return cf.whole_sign_house(lon, rising_idx)

def local(dt_utc, tz): return dt_utc.astimezone(tz)
def iso_local(dt_utc, tz): return local(dt_utc, tz).strftime("%Y-%m-%dT%H:%M")
def pretty_local(dt_utc, tz): return local(dt_utc, tz).strftime("%a %b %-d, %Y %-I:%M %p")

# ---------------------------------------------------------------- Sabian symbols

_SABIAN = {}
def sabian(lon):
    """Sabian symbol for a longitude. Convention: round UP to the next whole
    degree (9°12' Virgo -> Virgo 10). Uses the site's verified sign files."""
    s, d = sign_of(lon)
    n = int(d) + 1
    if n > 30: n = 30
    slug = s.lower()
    if slug not in _SABIAN:
        try:
            _SABIAN[slug] = importlib.import_module(f"sabian_data.{slug}").ENTRIES
        except Exception:
            _SABIAN[slug] = None
    entries = _SABIAN[slug]
    e = entries[n - 1] if entries and len(entries) >= n else None
    return {"label": f"{s} {n}", "sign": s, "degree": n,
            "image": e["image"] if e else None,
            "reflection": e.get("reflection") if e else None}

# ---------------------------------------------------------------- charts

def positions(jd, chiron_lon=None):
    pos = cf.positions_at(jd)
    if pos.get("Chiron") is None and chiron_lon is not None:
        pos["Chiron"] = {"lon": chiron_lon, "speed": 0.0, "retrograde": False, "supplied": True}
    return pos

def lots(asc, sun, moon, sect):
    if sect == "day":
        fortune = norm(asc + moon - sun); spirit = norm(asc + sun - moon)
    else:
        fortune = norm(asc + sun - moon); spirit = norm(asc + moon - sun)
    return fortune, spirit

def point_entry(name, lon, rising_idx, speed=0.0, retro=False):
    s, d = sign_of(lon)
    e = {"name": name, "lon": round(lon, 4), "sign": s, "degree": round(d, 3),
         "pretty": fmt(lon), "retrograde": bool(retro), "speed": round(speed, 4),
         "house": whole_sign_house(lon, rising_idx), "sabian": sabian(lon),
         "element": ELEMENT[s], "mode": MODE[s]}
    if name in cf.DOMICILE:
        e["dignities"] = cf.dignity(name, s)
    e["house_meaning"] = HOUSE_MEANING[e["house"]]
    return e

def cast(jd, lat, lon, tz, chiron_lon=None):
    """A full timed chart at jd for a place, whole-sign houses."""
    pos = positions(jd, chiron_lon)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_MOSEPH)
    asc, mc = norm(ascmc[0]), norm(ascmc[1])
    rising_idx = int(asc // 30)
    below = 0 <= (pos["Sun"]["lon"] - asc) % 360 < 180
    sect = "night" if below else "day"
    planets = {}
    for p in list(cf.PLANETS) + ["North Node", "South Node", "Chiron"]:
        if pos.get(p) is None:
            continue
        planets[p] = point_entry(p, pos[p]["lon"], rising_idx, pos[p]["speed"], pos[p]["retrograde"])
    angles = {"ASC": point_entry("ASC", asc, rising_idx), "MC": point_entry("MC", mc, rising_idx),
              "DSC": point_entry("DSC", norm(asc + 180), rising_idx), "IC": point_entry("IC", norm(mc + 180), rising_idx)}
    fortune, spirit = lots(asc, pos["Sun"]["lon"], pos["Moon"]["lon"], sect)
    lots_ = {"Fortune": point_entry("Fortune", fortune, rising_idx), "Spirit": point_entry("Spirit", spirit, rising_idx)}
    aspects = cf.natal_aspects(pos)
    for pt, lon_a in (("ASC", asc), ("MC", mc)):
        for p in cf.PLANETS:
            for name, angle in ASPECTS.items():
                orb = abs(sep(pos[p]["lon"], lon_a) - angle)
                cap = 3 if name != "quincunx" else 2
                if orb <= cap:
                    aspects.append({"a": p, "b": pt, "aspect": name, "orb": round(orb, 2),
                                    "tight": orb <= 1.5, "major": name != "quincunx"})
    aspects.sort(key=lambda x: x["orb"])
    rs = SIGNS[rising_idx]
    ruler = RULER[rs]
    chart_ruler = {"planet": ruler, **cf.condition(ruler, pos, rising_idx, sect)}
    if rs in cf.MODERN_CORULER:
        co = cf.MODERN_CORULER[rs]
        chart_ruler["modern_coruler"] = {"planet": co, **cf.condition(co, pos, rising_idx, sect)}
    houses = {}
    for h in range(1, 13):
        s = SIGNS[(rising_idx + h - 1) % 12]
        r = RULER[s]
        houses[h] = {"sign": s, "meaning": HOUSE_MEANING[h],
                     "occupants": [p for p in cf.PLANETS if planets[p]["house"] == h],
                     "ruler": r, "ruler_in": {"sign": planets[r]["sign"], "house": planets[r]["house"],
                                              "retrograde": planets[r]["retrograde"],
                                              "dignities": planets[r].get("dignities")}}
    counts = {"element": {}, "mode": {}}
    for p in list(cf.PLANETS) + ["ASC"]:
        s = rs if p == "ASC" else planets[p]["sign"]
        counts["element"][ELEMENT[s]] = counts["element"].get(ELEMENT[s], 0) + 1
        counts["mode"][MODE[s]] = counts["mode"].get(MODE[s], 0) + 1
    angular = [p for p in cf.PLANETS if planets[p]["house"] in (1, 4, 7, 10)]
    on_angle = []
    for p in cf.PLANETS:
        for pt, lon_a in (("ASC", asc), ("MC", mc), ("DSC", asc + 180), ("IC", mc + 180)):
            o = sep(pos[p]["lon"], lon_a)
            if o <= 6:
                on_angle.append({"planet": p, "angle": pt, "orb": round(o, 2)})
    # planetary day + hour of the moment
    lt = dt_of(jd).astimezone(tz)
    day_local = datetime(lt.year, lt.month, lt.day, tzinfo=tz)
    tables = el.planetary_hours_range(day_local - timedelta(days=1), 2, tz, lat, lon)
    hr, h0, h1 = el.hour_ruler_at(tables, dt_of(jd), tz)
    prev_day = (lt.date() - timedelta(days=1)).isoformat()
    tab_today = tables.get(lt.date().isoformat())
    sunrise_today = tab_today["hours"][0][0] if tab_today else None
    day_ruler = tab_today["day_ruler"] if (sunrise_today and dt_of(jd) >= sunrise_today) else tables[prev_day]["day_ruler"]
    return {
        "jd": jd, "utc": dt_of(jd).isoformat(), "local": lt.isoformat(), "local_pretty": lt.strftime("%A, %B %-d, %Y at %-I:%M:%S %p %Z"),
        "asc": angles["ASC"], "mc": angles["MC"], "dsc": angles["DSC"], "ic": angles["IC"],
        "rising_sign": rs, "rising_idx": rising_idx, "sect": sect,
        "sect_roles": {"light": "Sun" if sect == "day" else "Moon",
                       "benefic_of_sect": "Jupiter" if sect == "day" else "Venus",
                       "benefic_contrary": "Venus" if sect == "day" else "Jupiter",
                       "malefic_of_sect": "Saturn" if sect == "day" else "Mars",
                       "malefic_contrary": "Mars" if sect == "day" else "Saturn"},
        "planets": planets, "lots": lots_, "aspects": aspects, "chart_ruler": chart_ruler,
        "houses": houses, "balance": counts, "angular_planets": angular, "on_angle": on_angle,
        "planetary_day": day_ruler, "planetary_hour": {"ruler": hr,
            "start": iso_local(h0, tz) if h0 else None, "end": iso_local(h1, tz) if h1 else None},
        "pos_raw": {p: pos[p]["lon"] for p in pos if pos[p]},
    }

def find_return(natal_sun_lon, approx_utc):
    """Exact moment the transiting Sun returns to its natal longitude."""
    t = approx_utc - timedelta(days=3)
    f = lambda x: sdelta(lon_at(x, swe.SUN), natal_sun_lon)
    prev = f(t)
    while True:
        t2 = t + timedelta(hours=6)
        cur = f(t2)
        if prev < 0 <= cur:
            return bisect_time(t, t2, f, iters=28)
        t, prev = t2, cur
        if t > approx_utc + timedelta(days=6):
            raise RuntimeError("no solar return found near " + approx_utc.isoformat())

# ---------------------------------------------------------------- overlays

def natal_targets(natal):
    t = {p: natal["planets"][p]["lon"] for p in natal["planets"] if natal["planets"][p]
         and p not in ("South Node",)}
    t["ASC"] = natal["asc"]["lon"]; t["MC"] = natal["mc"]["lon"]
    return t

def overlay(sr, natal):
    n_idx = SIGNS.index(natal["asc"]["sign"])
    sr_in_natal = {}
    for p, e in sr["planets"].items():
        sr_in_natal[p] = whole_sign_house(e["lon"], n_idx)
    for a in ("ASC", "MC", "DSC", "IC"):
        sr_in_natal[a] = whole_sign_house(sr[a.lower()]["lon"], n_idx)
    for lname, e in sr["lots"].items():
        sr_in_natal["Lot of " + lname] = whole_sign_house(e["lon"], n_idx)
    natal_in_sr = {p: whole_sign_house(e["lon"], sr["rising_idx"]) for p, e in natal["planets"].items() if e}
    natal_in_sr["ASC"] = whole_sign_house(natal["asc"]["lon"], sr["rising_idx"])
    natal_in_sr["MC"] = whole_sign_house(natal["mc"]["lon"], sr["rising_idx"])
    targets = natal_targets(natal)
    sr_points = {p: e["lon"] for p, e in sr["planets"].items() if p != "South Node"}
    sr_points["ASC"] = sr["asc"]["lon"]; sr_points["MC"] = sr["mc"]["lon"]
    hits = []
    for sp, slon in sr_points.items():
        for np_, nlon in targets.items():
            for name, angle in ASPECTS.items():
                orb = abs(sep(slon, nlon) - angle)
                if orb <= TIGHT_ORB[name]:
                    hits.append({"sr": sp, "natal": np_, "aspect": name, "orb": round(orb, 2),
                                 "is_return": sp == np_ and name == "conjunction",
                                 "tight": orb <= 1.5})
    hits.sort(key=lambda x: x["orb"])
    return {"sr_planets_in_natal_houses": sr_in_natal, "natal_planets_in_sr_houses": natal_in_sr,
            "aspects_sr_to_natal": hits,
            "sr_asc_in_natal_house": sr_in_natal["ASC"], "sr_sun_house": sr["planets"]["Sun"]["house"],
            "sr_moon_house": sr["planets"]["Moon"]["house"],
            "sr_moon_in_natal_house": sr_in_natal["Moon"]}

# ---------------------------------------------------------------- the year

def daily_grid(start_utc, n_days, bodies):
    grid = {b: [] for b in bodies}
    for i in range(n_days + 1):
        jd = jd_of(start_utc + timedelta(days=i))
        for b in bodies:
            grid[b].append(lonspeed(jd, BODIES[b]))
    return grid

def find_ingresses(start_utc, n_days, grid, tz, natal_idx, sr_idx):
    out = []
    for b, rows in grid.items():
        if b in ("Moon", "North Node"):
            continue
        for i in range(1, len(rows)):
            s0, s1 = int(rows[i-1][0] // 30), int(rows[i][0] // 30)
            if s0 != s1:
                t0 = start_utc + timedelta(days=i-1); t1 = start_utc + timedelta(days=i)
                hit = bisect_time(t0, t1, lambda x, s=s0: -1 if int(lon_at(x, BODIES[b]) // 30) == s else 1)
                retro = rows[i][1] < 0
                out.append({"body": b, "sign": SIGNS[s1], "from_sign": SIGNS[s0], "retrograde": retro,
                            "utc": hit.isoformat(), "local": iso_local(hit, tz), "pretty": pretty_local(hit, tz),
                            "natal_house": whole_sign_house(s1 * 30 + 1, natal_idx),
                            "sr_house": whole_sign_house(s1 * 30 + 1, sr_idx)})
    out.sort(key=lambda x: x["utc"])
    return out

def find_stations(start_utc, n_days, grid, tz, natal_idx):
    out = []
    for b, rows in grid.items():
        if b in ("Sun", "Moon", "North Node"):
            continue
        for i in range(1, len(rows)):
            v0, v1 = rows[i-1][1], rows[i][1]
            if (v0 < 0) != (v1 < 0):
                t0 = start_utc + timedelta(days=i-1); t1 = start_utc + timedelta(days=i)
                hit = bisect_time(t0, t1, lambda x: lonspeed(jd_of(x), BODIES[b])[1])
                lon = lon_at(hit, BODIES[b])
                out.append({"body": b, "type": "retrograde" if v1 < 0 else "direct", "lon": round(lon, 3),
                            "pretty_lon": fmt(lon), "sabian": sabian(lon), "utc": hit.isoformat(),
                            "local": iso_local(hit, tz), "pretty": pretty_local(hit, tz),
                            "natal_house": whole_sign_house(lon, natal_idx)})
    out.sort(key=lambda x: x["utc"])
    return out

def mercury_shadows(stations, start_utc, end_utc, tz):
    """Pre-shadow: Mercury first reaches the degree of its later direct station.
    Post-shadow: Mercury direct again reaches the degree of its retrograde station."""
    ms = [s for s in stations if s["body"] == "Mercury"]
    out = []
    for i, s in enumerate(ms):
        if s["type"] != "retrograde":
            continue
        d = next((x for x in ms[i+1:] if x["type"] == "direct"), None)
        rx_t = datetime.fromisoformat(s["utc"])
        entry = {"retro_station": s["local"], "retro_lon": s["pretty_lon"]}
        if d:
            d_t = datetime.fromisoformat(d["utc"])
            # pre-shadow: scan backward from rx station for lon == direct-station lon
            t = rx_t; f = lambda x, L=d["lon"]: sdelta(lon_at(x, swe.MERCURY), L)
            prev = f(t)
            while t > rx_t - timedelta(days=45):
                t2 = t - timedelta(hours=6); cur = f(t2)
                if (prev < 0) != (cur < 0) and abs(prev) < 5 and abs(cur) < 5:
                    pre = bisect_time(t2, t, f); break
                t, prev = t2, cur
            else:
                pre = None
            t = d_t; f2 = lambda x, L=s["lon"]: sdelta(lon_at(x, swe.MERCURY), L)
            prev = f2(t)
            while t < d_t + timedelta(days=45):
                t2 = t + timedelta(hours=6); cur = f2(t2)
                if (prev < 0) != (cur < 0) and abs(prev) < 5 and abs(cur) < 5:
                    post = bisect_time(t, t2, f2); break
                t, prev = t2, cur
            else:
                post = None
            entry.update({"direct_station": d["local"], "direct_lon": d["pretty_lon"],
                          "pre_shadow_start": iso_local(pre, tz) if pre else None,
                          "post_shadow_end": iso_local(post, tz) if post else None,
                          "utc_retro": s["utc"], "utc_direct": d["utc"],
                          "utc_pre": pre.isoformat() if pre else None, "utc_post": post.isoformat() if post else None})
        out.append(entry)
    return out

def find_lunations(start_utc, end_utc, tz, natal_idx, sr_idx):
    """New, full, and quarter Moons with degree, Sabian, houses, eclipse flags."""
    out = []
    targets = [(0, "new"), (90, "first quarter"), (180, "full"), (270, "last quarter")]
    t = start_utc
    step = timedelta(hours=6)
    def elong(x): return norm(lon_at(x, swe.MOON) - lon_at(x, swe.SUN))
    prev = elong(t)
    while t < end_utc:
        t2 = min(t + step, end_utc); cur = elong(t2)
        for ang, kind in targets:
            d0, d1 = sdelta(prev, ang), sdelta(cur, ang)
            if d0 < 0 <= d1 and abs(d0) < 10 and abs(d1) < 10:
                hit = bisect_time(t, t2, lambda x, a=ang: sdelta(elong(x), a))
                jd = jd_of(hit)
                mlon = lon_at(hit, swe.MOON); slon = lon_at(hit, swe.SUN)
                ev = {"kind": kind, "utc": hit.isoformat(), "local": iso_local(hit, tz),
                      "pretty": pretty_local(hit, tz), "moon_lon": round(mlon, 3), "sun_lon": round(slon, 3),
                      "moon_pretty": fmt(mlon), "sun_pretty": fmt(slon), "sabian": sabian(mlon),
                      "natal_house": whole_sign_house(mlon, natal_idx), "sr_house": whole_sign_house(mlon, sr_idx),
                      "eclipse": None}
                if kind == "new":
                    rf, tret = swe.sol_eclipse_when_glob(jd - 2, swe.FLG_MOSEPH, 0, False)
                    if abs(tret[0] - jd) < 1.5:
                        ev["eclipse"] = {"type": next((n for c, n in ECL_TYPES if rf & c), "solar"), "kind": "solar",
                                         "max_utc": dt_of(tret[0]).isoformat()}
                if kind == "full":
                    rf, tret = swe.lun_eclipse_when(jd - 2, swe.FLG_MOSEPH, 0, False)
                    if abs(tret[0] - jd) < 1.5:
                        ev["eclipse"] = {"type": next((n for c, n in ECL_TYPES if rf & c), "lunar"), "kind": "lunar",
                                         "max_utc": dt_of(tret[0]).isoformat()}
                out.append(ev)
        t, prev = t2, cur
    out.sort(key=lambda x: x["utc"])
    return out

def find_perfections(start_utc, n_days, grid, targets, tz, natal_idx):
    """Exact transit-to-natal aspects for Sun..Pluto, with retro-pass numbering."""
    raw = []
    for b in TRANSITING:
        rows = grid[b]
        for tgt, tlon in targets.items():
            for name, angle in ASPECTS.items():
                offsets = (angle,) if angle in (0, 180) else (angle, -angle)
                for off in offsets:
                    goal = norm(tlon + off)
                    prev = sdelta(rows[0][0], goal)
                    for i in range(1, len(rows)):
                        cur = sdelta(rows[i][0], goal)
                        if (prev < 0) != (cur < 0) and abs(prev) < 12 and abs(cur) < 12:
                            t0 = start_utc + timedelta(days=i-1); t1 = start_utc + timedelta(days=i)
                            hit = bisect_time(t0, t1, lambda x, g=goal, bb=b: sdelta(lon_at(x, BODIES[bb]), g))
                            lon, spd = lonspeed(jd_of(hit), BODIES[b])
                            raw.append({"transiting": b, "natal_point": tgt, "aspect": name, "utc": hit.isoformat(),
                                        "local": iso_local(hit, tz), "date": local(hit, tz).date().isoformat(),
                                        "pretty": pretty_local(hit, tz), "transit_lon": round(lon, 3),
                                        "transit_pretty": fmt(lon), "retrograde": spd < 0,
                                        "transit_natal_house": whole_sign_house(lon, natal_idx),
                                        "is_return": (b == tgt and name == "conjunction"),
                                        "sabian": sabian(lon)})
                        prev = cur
    raw.sort(key=lambda x: x["utc"])
    groups = {}
    for h in raw:
        groups.setdefault((h["transiting"], h["natal_point"], h["aspect"]), []).append(h)
    for key, lst in groups.items():
        n = len(lst)
        for k, h in enumerate(lst, 1):
            h["pass"] = k; h["passes"] = n
            h["pass_label"] = ({1: "direct pass", 2: "retrograde pass", 3: "final pass"}.get(k, f"pass {k}")
                               if n >= 2 else "single pass")
    return raw

def slow_windows(start_utc, n_days, grid, targets, tz, orb=1.0):
    """Date ranges when Jupiter..Pluto sit within `orb` of an exact aspect to a natal point."""
    out = []
    for b in SLOW:
        rows = grid[b]
        for tgt, tlon in targets.items():
            for name, angle in ASPECTS.items():
                cap = orb if name != "quincunx" else 0.75
                active = None
                for i, (lon, spd) in enumerate(rows):
                    o = abs(sep(lon, tlon) - angle)
                    if o <= cap and active is None:
                        active = i
                    if (o > cap or i == len(rows) - 1) and active is not None:
                        d0 = (start_utc + timedelta(days=active)).astimezone(tz).date()
                        d1 = (start_utc + timedelta(days=i)).astimezone(tz).date()
                        out.append({"transiting": b, "natal_point": tgt, "aspect": name,
                                    "start": d0.isoformat(), "end": d1.isoformat(), "days": (d1 - d0).days + 1})
                        active = None
    out.sort(key=lambda x: x["start"])
    return out

def sensitive_windows(start_utc, n_days, grid, tz, zones):
    """zones: [{"label", "lo", "hi", "signs": [..] or None}] measured in degree-within-sign.
    Returns date windows when Mars..Pluto occupy the zone."""
    out = []
    for z in zones:
        for b in ["Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
            rows = grid[b]; active = None
            for i, (lon, spd) in enumerate(rows):
                s, d = sign_of(lon)
                inside = z["lo"] <= d <= z["hi"] and (not z.get("signs") or s in z["signs"])
                if inside and active is None:
                    active = i
                if (not inside or i == len(rows) - 1) and active is not None:
                    d0 = (start_utc + timedelta(days=active)).astimezone(tz).date()
                    d1 = (start_utc + timedelta(days=i)).astimezone(tz).date()
                    out.append({"zone": z["label"], "body": b, "sign": sign_of(rows[active][0])[0],
                                "start": d0.isoformat(), "end": d1.isoformat(), "days": (d1 - d0).days + 1})
                    active = None
    out.sort(key=lambda x: x["start"])
    return out

def asc_windows_for_day(day_local, tz, lat, lon, want_signs, step_min=4):
    """Local intervals during one calendar day when the Ascendant is in each wanted sign."""
    res = {s: [] for s in want_signs}
    t = day_local; end = day_local + timedelta(days=1)
    def asc_sign(x):
        cusps, ascmc = swe.houses_ex(jd_of(x.astimezone(timezone.utc)), lat, lon, b'W', swe.FLG_MOSEPH)
        return int(norm(ascmc[0]) // 30)
    cur = asc_sign(t); open_at = {s: (t if SIGNS[cur] == s else None) for s in want_signs}
    while t < end:
        t2 = min(t + timedelta(minutes=step_min), end)
        nxt = asc_sign(t2)
        if nxt != cur:
            # refine the change
            lo, hi = t, t2
            for _ in range(10):
                mid = lo + (hi - lo) / 2
                if asc_sign(mid) == cur: lo = mid
                else: hi = mid
            for s in want_signs:
                if SIGNS[cur] == s and open_at[s] is not None:
                    res[s].append((open_at[s], hi)); open_at[s] = None
                if SIGNS[nxt] == s:
                    open_at[s] = hi
            cur = nxt
        t = t2
    for s in want_signs:
        if open_at[s] is not None:
            res[s].append((open_at[s], end))
    return res

# ---------------------------------------------------------------- occasions

def occasion_library():
    """User-agnostic recipes. `points` name natal roles the engine resolves per chart:
    H<n> = planets in natal house n plus that house's ruler; named planets/angles literal."""
    L = []
    def add(key, label, group, kind, points, benefics, malefics, phase, days, hours,
            retro, moon_bonus=(), moon_avoid=(), notes="", weight_comm=False):
        L.append({"key": key, "label": label, "group": group, "kind": kind, "points": points,
                  "benefics": benefics, "malefics": malefics, "phase": phase, "day_rulers": days,
                  "hour_rulers": hours, "retro": retro, "moon_bonus": list(moon_bonus),
                  "moon_avoid": list(moon_avoid), "notes": notes, "comm": weight_comm})
    # MONEY
    add("ask_money", "Ask for money · negotiate salary or an offer", "Money", "external",
        ["H2", "Jupiter", "Venus", "Fortune"], ["Jupiter", "Venus"], ["Saturn", "Mars"], "waxing",
        ["Jupiter", "Venus", "Sun"], ["Jupiter", "Venus"], {"Mercury": -3, "Venus": -3},
        moon_bonus=["Taurus", "Leo", "Sagittarius"], moon_avoid=["Capricorn", "Scorpio"], weight_comm=True,
        notes="Waxing Moon applying to Jupiter or Venus, Mercury direct so the ask is heard, Jupiter's day or hour.")
    add("sign_contract", "Sign a contract · accept an offer", "Money", "external",
        ["H2", "Mercury", "Jupiter", "H7"], ["Jupiter", "Venus", "Mercury"], ["Saturn", "Mars"], "waxing",
        ["Jupiter", "Mercury", "Venus"], ["Jupiter", "Mercury"], {"Mercury": -4, "Venus": -1.5},
        moon_bonus=["Taurus", "Virgo", "Capricorn", "Libra"], moon_avoid=["Scorpio"], weight_comm=True,
        notes="Mercury direct and unafflicted, Moon applying to a benefic, no eclipse within reach; fixed or earth Moon holds.")
    add("invest", "Invest · open an account · move money", "Money", "external",
        ["H2", "H8", "Jupiter", "Venus", "Fortune"], ["Jupiter", "Venus"], ["Mars", "Uranus", "Neptune"], "waxing",
        ["Jupiter", "Venus", "Saturn"], ["Jupiter", "Venus"], {"Venus": -3, "Mercury": -2},
        moon_bonus=["Taurus", "Capricorn", "Virgo"], moon_avoid=["Aries", "Gemini"],
        notes="Earth Moon waxing toward a benefic, Saturn well placed for patience, Neptune and Uranus quiet.")
    add("launch_sell", "Launch · list · open the shop · sell", "Money", "external",
        ["H2", "H10", "MC", "Jupiter", "Venus", "Mercury"], ["Jupiter", "Venus", "Sun"], ["Saturn"], "waxing",
        ["Sun", "Jupiter", "Venus", "Mercury"], ["Jupiter", "Venus", "Sun"], {"Mercury": -3, "Venus": -2, "Mars": -1},
        moon_bonus=["Leo", "Aries", "Sagittarius", "Libra"], moon_avoid=["Scorpio", "Pisces"], weight_comm=True,
        notes="Fire or Libra Moon waxing, the Sun and Jupiter warm, Mercury direct so the listing is seen.")
    add("debt_budget", "Pay down debt · cancel · budget reset", "Money", "internal",
        ["H2", "H8", "Saturn", "Mercury"], ["Saturn", "Mercury", "Venus"], ["Jupiter", "Mars"], "waning",
        ["Saturn", "Mercury"], ["Saturn", "Mercury"], {},
        moon_bonus=["Virgo", "Capricorn", "Scorpio"], moon_avoid=["Leo", "Sagittarius"],
        notes="Waning Moon in an earth or Scorpio sign, Saturn's day: the sky for cutting, closing, and clearing.")
    # CAREER
    add("apply", "Apply · send the résumé · pitch yourself", "Career", "external",
        ["H10", "MC", "Sun", "Mercury", "H1"], ["Jupiter", "Sun", "Mercury", "Venus"], ["Saturn", "Neptune"], "waxing",
        ["Sun", "Jupiter", "Mercury"], ["Sun", "Jupiter", "Mercury"], {"Mercury": -3.5},
        moon_bonus=["Leo", "Aries", "Capricorn", "Gemini"], moon_avoid=["Pisces", "Scorpio"], weight_comm=True,
        notes="Mercury direct, Moon waxing in a visible sign, the Sun or Jupiter touching the Midheaven or Sun.")
    add("interview", "Interview · present · be seen", "Career", "external",
        ["H10", "MC", "Sun", "ASC", "Mercury"], ["Sun", "Jupiter", "Venus", "Mercury"], ["Saturn", "Mars", "Neptune"], "waxing",
        ["Sun", "Jupiter", "Venus"], ["Sun", "Jupiter", "Venus", "Mercury"], {"Mercury": -3},
        moon_bonus=["Leo", "Libra", "Gemini", "Aries"], moon_avoid=["Pisces", "Capricorn"], weight_comm=True,
        notes="A Moon that speaks (air or Leo) applying to a benefic, the Sun strong, Saturn away from your angles.")
    add("send_email", "Send the important email · the big message", "Career", "external",
        ["Mercury", "H3", "H10", "Jupiter"], ["Mercury", "Jupiter", "Venus"], ["Saturn", "Mars", "Neptune"], None,
        ["Mercury", "Jupiter", "Venus"], ["Mercury", "Jupiter"], {"Mercury": -4},
        moon_bonus=["Gemini", "Virgo", "Libra", "Aquarius"], moon_avoid=["Pisces"], weight_comm=True,
        notes="Mercury direct and clean, Moon in air or Virgo applying to a benefic, Mercury's hour; never void.")
    add("publish", "Publish · post · go public with the work", "Career", "external",
        ["H9", "H10", "MC", "Mercury", "Jupiter", "Sun"], ["Jupiter", "Sun", "Mercury", "Venus"], ["Saturn", "Neptune"], "full",
        ["Jupiter", "Sun", "Mercury"], ["Jupiter", "Sun", "Mercury"], {"Mercury": -3},
        moon_bonus=["Leo", "Sagittarius", "Gemini", "Aquarius"], moon_avoid=["Scorpio", "Capricorn"], weight_comm=True,
        notes="Toward the Full Moon or just after it, Jupiter and the Sun touching the Midheaven, Mercury direct.")
    add("network", "Network · ask for an introduction · meet allies", "Career", "external",
        ["H11", "Venus", "Jupiter", "Mercury"], ["Venus", "Jupiter", "Mercury"], ["Saturn", "Mars"], "waxing",
        ["Venus", "Jupiter", "Mercury"], ["Venus", "Jupiter"], {"Mercury": -2, "Venus": -2},
        moon_bonus=["Libra", "Aquarius", "Gemini", "Leo"], moon_avoid=["Capricorn", "Scorpio"], weight_comm=True,
        notes="Air Moon applying to Venus or Jupiter, Venus's day, the eleventh house warm.")
    add("start_build", "Start the build · begin a project quietly", "Career", "internal",
        ["H12", "H6", "Mercury", "Saturn", "Mars"], ["Mercury", "Saturn", "Jupiter"], ["Neptune", "Mars"], "new",
        ["Saturn", "Mercury", "Mars"], ["Saturn", "Mercury"], {"Mercury": -2, "Mars": -2},
        moon_bonus=["Virgo", "Capricorn", "Taurus", "Scorpio"], moon_avoid=["Gemini", "Pisces"],
        notes="Just after a New Moon, earth Moon applying to Saturn or Mercury, Mars direct: foundations that last.")
    # LOVE & FAMILY
    add("date_night", "Date night · romance · the anniversary", "Love", "external",
        ["H7", "DSC", "Venus", "Moon", "H5"], ["Venus", "Jupiter", "Moon"], ["Saturn", "Mars"], "waxing",
        ["Venus", "Moon", "Jupiter"], ["Venus", "Moon"], {"Venus": -3},
        moon_bonus=["Taurus", "Libra", "Pisces", "Leo", "Cancer"], moon_avoid=["Capricorn", "Virgo"],
        notes="Venus direct, the Moon in her own or Venus's signs applying to Venus, Venus's day and hour.")
    add("hard_talk", "The hard conversation · reconcile · repair", "Love", "internal",
        ["H7", "Mercury", "Venus", "Moon"], ["Venus", "Mercury", "Jupiter"], ["Mars", "Saturn", "Pluto"], "waxing",
        ["Venus", "Mercury", "Jupiter"], ["Venus", "Mercury"], {"Mercury": -3, "Venus": -2},
        moon_bonus=["Libra", "Cancer", "Pisces", "Taurus"], moon_avoid=["Aries", "Scorpio"], weight_comm=True,
        notes="Moon in Libra or a water sign applying to Venus or Mercury, Mars and Saturn away from the Moon.")
    add("family_gather", "Host · gather the family · the big dinner", "Family", "external",
        ["H4", "IC", "Moon", "Venus", "Jupiter"], ["Venus", "Jupiter", "Moon"], ["Saturn", "Mars"], "waxing",
        ["Venus", "Jupiter", "Moon", "Sun"], ["Venus", "Jupiter"], {"Venus": -1.5},
        moon_bonus=["Cancer", "Taurus", "Leo", "Libra", "Sagittarius"], moon_avoid=["Capricorn", "Aquarius"],
        notes="Moon in Cancer, Taurus, or Leo applying to a benefic, the fourth house warm, Saturn quiet.")
    add("kids", "Decisions for the kids · school · their milestones", "Family", "external",
        ["H5", "H4", "Moon", "Mercury", "Jupiter"], ["Jupiter", "Venus", "Mercury"], ["Saturn", "Mars"], "waxing",
        ["Jupiter", "Mercury", "Moon"], ["Jupiter", "Mercury"], {"Mercury": -2.5},
        moon_bonus=["Leo", "Cancer", "Sagittarius", "Gemini"], moon_avoid=["Scorpio", "Capricorn"], weight_comm=True,
        notes="Fifth-house matters: Moon waxing in Leo, Cancer, or Sagittarius applying to Jupiter or Mercury.")
    # BODY & SPIRIT
    add("fitness_start", "Start the fitness block · new regimen", "Body", "internal",
        ["H6", "H1", "ASC", "Mars", "Sun"], ["Mars", "Sun", "Saturn"], ["Neptune", "Jupiter"], "new",
        ["Mars", "Sun", "Saturn"], ["Mars", "Sun"], {"Mars": -2.5},
        moon_bonus=["Aries", "Capricorn", "Virgo", "Scorpio"], moon_avoid=["Pisces", "Libra"],
        notes="Just after a New Moon, Mars direct and dignified, Moon in Aries, Capricorn, or Virgo applying to Mars or Saturn.")
    add("diet_start", "Start the eating protocol · break a habit", "Body", "internal",
        ["H6", "Moon", "Saturn", "Mercury"], ["Saturn", "Mercury", "Sun"], ["Jupiter", "Venus", "Neptune"], "waning",
        ["Saturn", "Mercury", "Sun"], ["Saturn", "Mercury"], {},
        moon_bonus=["Virgo", "Capricorn", "Scorpio", "Aquarius"], moon_avoid=["Taurus", "Leo", "Pisces"],
        notes="Waning Moon (subtraction) in Virgo, Capricorn, or Scorpio applying to Saturn; appetite planets quiet.")
    add("beauty", "Haircut · beauty · the glow-up", "Body", "external",
        ["H1", "ASC", "Venus", "Moon"], ["Venus", "Jupiter", "Moon"], ["Saturn", "Mars"], "waxing",
        ["Venus", "Moon", "Sun"], ["Venus", "Moon"], {"Venus": -2},
        moon_bonus=["Taurus", "Leo", "Libra", "Cancer"], moon_avoid=["Aries", "Capricorn"],
        notes="Waxing Moon for growth, Venus applying, Moon in Taurus, Leo, or Libra; Venus's day.")
    add("rest_retreat", "Rest · retreat · say no to everything", "Spirit", "internal",
        ["H12", "H4", "Moon", "Neptune", "Venus"], ["Venus", "Neptune", "Moon", "Jupiter"], ["Mars", "Uranus"], "waning",
        ["Moon", "Venus", "Saturn"], ["Moon", "Venus"], {},
        moon_bonus=["Pisces", "Cancer", "Taurus", "Scorpio"], moon_avoid=["Aries", "Gemini"],
        notes="Waning water Moon, Neptune softly aspected, nothing angular and loud: the sky for closing the door.")
    add("ritual", "Ritual · planetary magic · the working", "Spirit", "internal",
        ["H9", "H12", "ASC", "Moon", "Neptune", "Jupiter"], ["Jupiter", "Venus", "Moon", "Neptune"], ["Saturn", "Mars"], None,
        ["Jupiter", "Venus", "Moon", "Sun"], ["Jupiter", "Venus", "Moon"], {},
        moon_bonus=["Cancer", "Pisces", "Scorpio", "Taurus", "Sagittarius"], moon_avoid=[],
        notes="Your own rising sign on the horizon, the Moon in water or Taurus applying to a benefic, the planetary hour that matches the intent.")
    add("vision", "Vision · strategy · the long look", "Spirit", "internal",
        ["H9", "MC", "Jupiter", "Neptune", "Mercury"], ["Jupiter", "Neptune", "Mercury", "Sun"], ["Mars", "Saturn"], "full",
        ["Jupiter", "Sun", "Mercury"], ["Jupiter", "Mercury"], {"Mercury": -1},
        moon_bonus=["Sagittarius", "Pisces", "Aquarius", "Gemini"], moon_avoid=["Taurus", "Scorpio"],
        notes="Around the Full Moon, Jupiter or Neptune touching Mercury or the ninth: for seeing the whole board.")
    # HOME
    add("declutter", "Declutter · clear the house · let go", "Home", "internal",
        ["H4", "IC", "Saturn", "Moon", "Pluto"], ["Saturn", "Mercury", "Pluto"], ["Jupiter", "Venus"], "waning",
        ["Saturn", "Mercury", "Moon"], ["Saturn", "Mercury"], {},
        moon_bonus=["Virgo", "Scorpio", "Capricorn", "Aquarius"], moon_avoid=["Taurus", "Cancer", "Leo"],
        notes="Waning Moon in Virgo, Scorpio, or Capricorn applying to Saturn: release without regret.")
    add("big_purchase", "Buy the big thing · the car · the appliance", "Home", "external",
        ["H2", "H4", "Venus", "Mercury", "Jupiter"], ["Venus", "Jupiter", "Mercury"], ["Mars", "Uranus", "Neptune"], "waxing",
        ["Venus", "Jupiter", "Mercury"], ["Venus", "Jupiter"], {"Mercury": -3, "Venus": -3, "Mars": -1},
        moon_bonus=["Taurus", "Virgo", "Capricorn"], moon_avoid=["Aries", "Aquarius", "Gemini"],
        notes="Earth Moon waxing, Venus and Mercury direct, Uranus quiet: nothing that breaks the week after.")
    add("travel", "Travel · the trip · leave town", "Home", "external",
        ["H9", "H3", "Mercury", "Jupiter", "Moon"], ["Jupiter", "Mercury", "Venus"], ["Saturn", "Mars", "Uranus"], "waxing",
        ["Jupiter", "Mercury", "Moon"], ["Jupiter", "Mercury"], {"Mercury": -3},
        moon_bonus=["Sagittarius", "Gemini", "Aquarius", "Aries"], moon_avoid=["Scorpio", "Capricorn"],
        notes="Mercury direct, Moon in Sagittarius or an air sign applying to Jupiter or Mercury, Uranus away from the Moon.")
    return L

def resolve_points(spec, natal, lots_natal):
    """Turn point roles into (name, longitude) pairs from the natal chart."""
    rising_idx = SIGNS.index(natal["asc"]["sign"])
    pts = {}
    for item in spec:
        if item.startswith("H"):
            h = int(item[1:])
            info = natal["houses"][h] if isinstance(natal["houses"], dict) and h in natal["houses"] else natal["houses"][str(h)]
            for p in info["occupants"]:
                pts[p] = natal["planets"][p]["lon"]
            r = info["ruler"]; pts[r] = natal["planets"][r]["lon"]
        elif item == "ASC": pts["ASC"] = natal["asc"]["lon"]
        elif item == "MC": pts["MC"] = natal["mc"]["lon"]
        elif item == "DSC": pts["DSC"] = norm(natal["asc"]["lon"] + 180)
        elif item == "IC": pts["IC"] = norm(natal["mc"]["lon"] + 180)
        elif item in ("Fortune", "Spirit"): pts["Lot of " + item] = lots_natal[item]
        elif natal["planets"].get(item): pts[item] = natal["planets"][item]["lon"]
    return pts

MIN_WINDOW = timedelta(minutes=12)
NATURE = {"Sun": 0.9, "Moon": 0.6, "Mercury": 0.6, "Venus": 1.3, "Jupiter": 1.6,
          "Mars": -1.2, "Saturn": -1.5, "Uranus": -0.8, "Neptune": -0.6, "Pluto": -1.0}

def transit_contacts_at(jd, all_targets):
    """All transit-to-natal aspects in orb at one moment: fast planets 3° conj / 2.5° others,
    slow planets 1.5° conj / 1.0° others; quincunx 1°."""
    out = []
    for b in TRANSITING:
        lon, spd = lonspeed(jd, BODIES[b])
        for tgt, tlon in all_targets.items():
            for name, angle in ASPECTS.items():
                o = abs(sep(lon, tlon) - angle)
                if b in FAST:
                    cap = 3.0 if name == "conjunction" else 2.5
                else:
                    cap = 1.5 if name == "conjunction" else 1.0
                if name == "quincunx": cap = min(cap, 1.0)
                if o <= cap:
                    out.append({"t": b, "p": tgt, "a": name, "orb": round(o, 2), "cap": cap, "retro": spd < 0})
    return out

def score_day(occ, day, pts, contacts, retro_state, shadow_state, lun_ctx, natal, sr_ctx):
    """Return (raw_score, reasons[]) for one occasion on one day."""
    s = 0.0; why = []
    ext = occ["kind"] == "external"
    # 1 phase
    ph = occ["phase"]; waxing = day["moon"]["waxing"]
    if ph == "waxing":
        if waxing: s += 2; why.append(("+", "waxing Moon"))
        else: s -= 1.5; why.append(("-", "waning Moon"))
    elif ph == "waning":
        if not waxing: s += 2; why.append(("+", "waning Moon"))
        else: s -= 1.5; why.append(("-", "waxing Moon"))
    elif ph == "new":
        d = lun_ctx["days_since_new"]
        if 0.5 <= d <= 3.5: s += 3; why.append(("+", "fresh after the New Moon"))
        elif d > 26 or d < 0.5: s -= 2; why.append(("-", "dark of the Moon"))
    elif ph == "full":
        d = abs(lun_ctx["days_to_full"])
        if d <= 1.5: s += 3; why.append(("+", "at the Full Moon"))
        elif lun_ctx["days_to_full"] < 0 and d <= 4: s += 1.5; why.append(("+", "just past Full"))
    if lun_ctx["eclipse_within"] is not None:
        pen = 5 if ext else 2.5
        s -= pen; why.append(("-", f"{lun_ctx['eclipse_within']} eclipse within reach"))
    if lun_ctx["days_since_new"] < 0.5 or lun_ctx["days_since_new"] > 28.8:
        if ph != "new" and ext: s -= 1; why.append(("-", "Moon dark and unseen"))
    # 2 Moon sign + house
    ms = day["moon"]["sign"]
    if ms in occ["moon_bonus"]: s += 1.5; why.append(("+", f"Moon in {ms}"))
    if ms in occ["moon_avoid"]: s -= 2; why.append(("-", f"Moon in {ms}"))
    rel_houses = {int(x[1:]) for x in occ["points"] if x.startswith("H")}
    if day["moon"]["natal_house"] in rel_houses: s += 1; why.append(("+", f"Moon in your {ordinal(day['moon']['natal_house'])} house"))
    if ext and day["moon"]["natal_house"] == 12 and 12 not in rel_houses: s -= 1; why.append(("-", "Moon in your 12th"))
    # 3 void
    v = day["moon"]["voc_share"]
    if v >= 0.15:
        s -= 4 * v; why.append(("-", f"Moon void {int(round(v*100))}% of the working day"))
    # 4 Moon perfections in the day
    good = bad = 0
    for p in day["moon"]["perfections"]:
        if p["planet"] in occ["benefics"] and p["aspect"] in ("trine", "sextile", "conjunction") and p["planet"] != "Sun":
            good += 1; why.append(("+", f"Moon {p['aspect']} {p['planet']} {p['time']}"))
        if p["planet"] in occ["malefics"] and p["aspect"] in ("square", "opposition", "conjunction"):
            bad += 1; why.append(("-", f"Moon {p['aspect']} {p['planet']} {p['time']}"))
    s += min(good, 2) * 2 - min(bad, 2) * 2
    # 5 transits to the occasion's natal points
    tsum = 0.0
    for c in contacts:
        if c["p"] not in pts: continue
        w = 1 - c["orb"] / c["cap"]
        nat = NATURE[c["t"]]
        if c["t"] == "Mercury" and occ["comm"]: nat = 1.0
        if c["t"] == "Neptune" and occ["group"] == "Spirit": nat = 0.8
        if c["t"] == "Saturn" and occ["phase"] == "waning": nat = 0.8
        if c["a"] in SOFT: val = abs(nat) * (1.0 if nat > 0 else 0.45) * w * 2
        elif c["a"] == "conjunction": val = nat * w * 2 * (1.0 if nat > 0 else 0.9)
        elif c["a"] == "quincunx": val = -abs(nat) * 0.5 * w
        else: val = (nat if nat < 0 else nat * 0.3) * w * 2
        tsum += val
        if abs(val) >= 0.8:
            why.append(("+" if val > 0 else "-", f"{c['t']} {c['a']} natal {c['p']} ({c['orb']:.1f}°)"))
    s += max(-6, min(6, tsum))
    # 6 personal cautions to Sun/Moon/ASC/MC
    caut = 0
    for c in contacts:
        if c["t"] in ("Mars", "Saturn") and c["p"] in ("Sun", "Moon", "ASC", "MC") and c["a"] in HARD | {"conjunction"} and c["p"] not in pts:
            caut += 1.5 * (1 - c["orb"] / c["cap"])
            why.append(("-", f"{c['t']} {c['a']} your {c['p']}"))
    s -= min(3, caut)
    # 7 mundane
    m = day["mundane"]
    s += max(-2, min(2, m * 0.25))
    # 8 retrogrades and shadows
    for pl, pen in occ["retro"].items():
        if retro_state.get(pl): s += pen; why.append(("-", f"{pl} retrograde"))
        elif pl == "Mercury" and shadow_state: s += pen / 2; why.append(("-", "Mercury in shadow"))
    # 9 planetary day / hour window
    if day["day_ruler"] in occ["day_rulers"]:
        s += 1.5; why.append(("+", f"{day['day_ruler']}'s day"))
    rising = day["windows_sign"]["external" if ext else "internal"]
    win = day["windows"][rising] if day["windows"] else []
    wake0, wake1 = day["wake"]
    best = None
    for (w0, w1) in win:
        for (h0, h1, r) in day["hours"]:
            lo, hi = max(w0, h0, wake0), min(w1, h1, wake1)
            if hi - lo >= MIN_WINDOW and r in occ["hour_rulers"]:
                cand = (lo, hi, r, "rising+hour")
                if best is None or (hi - lo) > (best[1] - best[0]): best = cand
    if best is None:
        for (w0, w1) in win:
            lo, hi = max(w0, wake0), min(w1, wake1)
            if hi - lo >= MIN_WINDOW and (best is None or (hi - lo) > (best[1] - best[0])):
                best = (lo, hi, rising, "rising")
    if best is None:
        for (h0, h1, r) in day["hours"]:
            lo, hi = max(h0, wake0 + timedelta(hours=1)), min(h1, wake1 - timedelta(hours=1))
            if hi - lo >= MIN_WINDOW and r in occ["hour_rulers"] and (best is None or (hi - lo) > (best[1] - best[0])):
                best = (lo, hi, r, "hour")
    if best and best[3] == "rising+hour":
        s += 1.0; why.append(("+", f"{best[2]}'s hour inside the {rising}-rising window"))
    elif best and best[3] == "hour":
        s += 0.4
    # weekends are poor for worldly asks that need an office on the other end
    if ext and occ["group"] in ("Career", "Money") and occ["key"] != "launch_sell" and day["weekday"] in ("Sat", "Sun"):
        s -= 1.0; why.append(("-", "weekend"))
    # 10 the big personal days
    for k in sr_ctx.get("bonus_days", []):
        if k["date"] == day["date"] and (k["groups"] is None or occ["group"] in k["groups"]):
            s += k["weight"]; why.append(("+", k["label"]))
    return s, why, best, win

def ordinal(n): return f"{n}{'th' if 10 <= n % 100 <= 20 else {1:'st',2:'nd',3:'rd'}.get(n % 10, 'th')}"

# ---------------------------------------------------------------- main build

def build(args):
    tz = ZoneInfo(args.tz)
    order = {"name": args.name, "date": args.date, "time": args.time, "tz": args.tz,
             "lat": args.lat, "lon": args.lon, "place": args.place}
    natal, npos, n_idx, n_sect, n_jd = cf.build_natal(order)
    natal["houses"] = {int(k): v for k, v in natal["houses"].items()}
    chiron_lon = cs.parse_natal_lon(args.chiron) if args.chiron else None
    if chiron_lon is not None and natal["planets"].get("Chiron") is None:
        natal["planets"]["Chiron"] = {**point_entry("Chiron", chiron_lon, n_idx), "supplied": True}
    natal["lots"] = {}
    f, sp = lots(natal["asc"]["lon"], natal["planets"]["Sun"]["lon"], natal["planets"]["Moon"]["lon"], n_sect)
    natal["lots"] = {"Fortune": point_entry("Fortune", f, n_idx), "Spirit": point_entry("Spirit", sp, n_idx)}
    for p, e in natal["planets"].items():
        if e: e["sabian"] = sabian(e["lon"])
    natal["asc"]["sabian"] = sabian(natal["asc"]["lon"]); natal["mc"]["sabian"] = sabian(natal["mc"]["lon"])

    sr_lat = args.sr_lat if args.sr_lat is not None else args.lat
    sr_lon = args.sr_lon if args.sr_lon is not None else args.lon
    sr_tz = ZoneInfo(args.sr_tz) if args.sr_tz else tz
    born = date.fromisoformat(args.date)
    approx = datetime(args.year, born.month, born.day, 12, tzinfo=timezone.utc)
    sr_t = find_return(natal["planets"]["Sun"]["lon"], approx)
    next_t = find_return(natal["planets"]["Sun"]["lon"], approx.replace(year=args.year + 1))
    sr = cast(jd_of(sr_t), sr_lat, sr_lon, sr_tz, chiron_lon=None)
    sr["place"] = args.sr_place or args.place
    sr["relocated"] = args.sr_lat is not None
    ov = overlay(sr, natal)
    prof = cf.profection(order, natal, born.replace(year=args.year))
    prof["year_lord_sr"] = sr["planets"][prof["year_lord"]]

    # ---- the year
    start_utc = sr_t; end_utc = next_t
    n_days = (end_utc - start_utc).days + 1
    grid_bodies = list(BODIES)
    grid = daily_grid(start_utc, n_days, grid_bodies)
    targets = natal_targets(natal)
    if natal["planets"].get("Chiron"): targets["Chiron"] = natal["planets"]["Chiron"]["lon"]
    ingresses = find_ingresses(start_utc, n_days, grid, tz, n_idx, sr["rising_idx"])
    stations = find_stations(start_utc, n_days, grid, tz, n_idx)
    shadows = mercury_shadows(stations, start_utc, end_utc, tz)
    lunations = find_lunations(start_utc, end_utc, tz, n_idx, sr["rising_idx"])
    perfections = find_perfections(start_utc, n_days, grid, targets, tz, n_idx)
    windows = slow_windows(start_utc, n_days, grid, targets, tz)
    zones = json.loads(args.zones) if args.zones else []
    sens = sensitive_windows(start_utc, n_days, grid, tz, zones) if zones else []

    # ---- Moon machinery for the daily ledger
    ingr = el.moon_ingresses(start_utc - timedelta(days=1), end_utc + timedelta(days=1))
    perf = el.moon_perfections(start_utc - timedelta(days=1), end_utc + timedelta(days=1))
    voc = el.voc_intervals(start_utc - timedelta(days=1), end_utc + timedelta(days=1), ingr, perf)
    first_local = local(start_utc, tz)
    day0 = datetime(first_local.year, first_local.month, first_local.day, tzinfo=tz)
    n_local_days = (local(end_utc, tz).date() - day0.date()).days + 1
    hour_tables = el.planetary_hours_range(day0 - timedelta(days=1), n_local_days + 2, tz, args.lat, args.lon)
    ext_sign = args.external_rising; int_sign = args.internal_rising
    lun_sorted = [(datetime.fromisoformat(l["utc"]), l) for l in lunations]
    retro_by_day = {}
    all_targets = dict(targets)
    all_targets["DSC"] = norm(natal["asc"]["lon"] + 180); all_targets["IC"] = norm(natal["mc"]["lon"] + 180)
    all_targets["Lot of Fortune"] = natal["lots"]["Fortune"]["lon"]; all_targets["Lot of Spirit"] = natal["lots"]["Spirit"]["lon"]

    days = []
    for i in range(n_local_days):
        dl = day0 + timedelta(days=i)
        d_iso = dl.date().isoformat()
        noon = (dl + timedelta(hours=12)).astimezone(timezone.utc)
        jd_noon = jd_of(noon)
        mlon, mspd = lonspeed(jd_noon, swe.MOON); slon, _ = lonspeed(jd_noon, swe.SUN)
        elong = norm(mlon - slon)
        illum = (1 - math.cos(math.radians(elong))) / 2
        # working-day void share 8am-8pm local
        w0 = (dl + timedelta(hours=8)).astimezone(timezone.utc); w1 = (dl + timedelta(hours=20)).astimezone(timezone.utc)
        void_secs = 0.0
        for (v0, v1) in voc:
            lo, hi = max(v0, w0), min(v1, w1)
            if lo < hi: void_secs += (hi - lo).total_seconds()
        voc_share = void_secs / (12 * 3600)
        day_start = dl.astimezone(timezone.utc); day_end = (dl + timedelta(days=1)).astimezone(timezone.utc)
        perfs = [{"time": local(t, tz).strftime("%-I:%M %p"), "planet": p, "aspect": a}
                 for (t, p, a) in perf if day_start <= t < day_end]
        voc_today = [(iso_local(max(v0, day_start), tz)[11:], iso_local(min(v1, day_end), tz)[11:])
                     for (v0, v1) in voc if v0 < day_end and v1 > day_start]
        ingress_today = [(iso_local(t, tz)[11:], SIGNS[s]) for (t, s) in ingr if day_start <= t < day_end]
        # lunation context
        prev_new = max((t for t, l in lun_sorted if l["kind"] == "new" and t <= noon), default=None)
        next_full = min((t for t, l in lun_sorted if l["kind"] == "full" and t >= noon - timedelta(days=4)), default=None)
        ecl = None
        for t, l in lun_sorted:
            if l["eclipse"] and abs((t - noon).total_seconds()) <= 3 * 86400:
                ecl = l["eclipse"]["kind"]
        days_since_new = (noon - prev_new).total_seconds() / 86400 if prev_new else 15.0
        days_to_full = (next_full - noon).total_seconds() / 86400 if next_full else 10.0
        # planetary day: the day-ruler table keyed by sunrise day
        tab = hour_tables.get(d_iso)
        # windows for the Ascendant rule
        win = asc_windows_for_day(dl, tz, args.lat, args.lon, [ext_sign, int_sign])
        win_iso = {k: [(a.astimezone(tz).strftime("%-I:%M %p"), b.astimezone(tz).strftime("%-I:%M %p")) for a, b in v] for k, v in win.items()}
        hours = [(h0, h1, r) for (h0, h1, r) in tab["hours"]] if tab else []
        prev_tab = hour_tables.get((dl.date() - timedelta(days=1)).isoformat())
        if prev_tab: hours = prev_tab["hours"][12:] + hours
        contacts = transit_contacts_at(jd_noon, all_targets)
        retro_state = {b: lonspeed(jd_noon, BODIES[b])[1] < 0 for b in ("Mercury", "Venus", "Mars", "Jupiter", "Saturn")}
        shadow = any(sh.get("utc_pre") and sh.get("utc_post") and
                     datetime.fromisoformat(sh["utc_pre"]) <= noon <= datetime.fromisoformat(sh["utc_post"])
                     for sh in shadows) and not retro_state["Mercury"]
        mscore, _ = mundane.live_score(noon, lambda t, code: lon_at(t, code))
        day = {"date": d_iso, "weekday": dl.strftime("%a"), "pretty": dl.strftime("%a %b %-d"),
               "moon": {"sign": sign_of(mlon)[0], "degree": round(sign_of(mlon)[1], 1), "pretty": fmt(mlon),
                        "waxing": elong < 180, "illumination": round(illum * 100),
                        "phase_name": phase_name(elong), "natal_house": whole_sign_house(mlon, n_idx),
                        "sr_house": whole_sign_house(mlon, sr["rising_idx"]), "voc_share": round(voc_share, 2),
                        "voc": voc_today, "ingress": ingress_today, "perfections": perfs},
               "day_ruler": tab["day_ruler"] if tab else DAY_RULER[dl.weekday()],
               "windows": win, "windows_pretty": win_iso, "hours": hours,
               "windows_sign": {"external": ext_sign, "internal": int_sign},
               "wake": ((dl + timedelta(hours=7)).astimezone(timezone.utc), (dl + timedelta(hours=22)).astimezone(timezone.utc)),
               "hours_pretty": [(h0.astimezone(tz).strftime("%-I:%M %p"), r) for (h0, h1, r) in (tab["hours"] if tab else [])],
               "retro": [b for b, v in retro_state.items() if v], "mercury_shadow": shadow,
               "mundane": round(mscore, 2), "contacts": contacts,
               "eclipse_near": ecl, "days_since_new": round(days_since_new, 1), "days_to_full": round(days_to_full, 1),
               "sun_pretty": fmt(slon)}
        day["_ctx"] = {"days_since_new": days_since_new, "days_to_full": days_to_full, "eclipse_within": ecl}
        day["_retro"] = retro_state; day["_shadow"] = shadow
        days.append(day)

    # bonus days: exact benefic perfections to the chart's money/career/love anchors
    bonus = []
    for h in perfections:
        if h["is_return"] and h["transiting"] == "Jupiter":
            for k in range(-2, 3):
                dd = (date.fromisoformat(h["date"]) + timedelta(days=k)).isoformat()
                bonus.append({"date": dd, "weight": 2.5 - abs(k) * 0.5, "groups": None, "label": f"Jupiter Return ({h['pass_label']})"})
        elif h["is_return"] and h["transiting"] == "Venus":
            for k in range(-1, 2):
                dd = (date.fromisoformat(h["date"]) + timedelta(days=k)).isoformat()
                bonus.append({"date": dd, "weight": 1.5, "groups": ["Love", "Money", "Body"], "label": "Venus Return"})
        elif h["transiting"] in ("Jupiter", "Venus", "Sun") and h["aspect"] in ("conjunction", "trine", "sextile") and h["natal_point"] in ("Jupiter", "Sun", "MC", "ASC", "Venus", "Mercury") and h["transiting"] != h["natal_point"]:
            bonus.append({"date": h["date"], "weight": 1.0, "groups": None, "label": f"{h['transiting']} {h['aspect']} natal {h['natal_point']} exact"})
    sr_ctx = {"bonus_days": bonus}

    occasions = occasion_library()
    lots_natal = {"Fortune": natal["lots"]["Fortune"]["lon"], "Spirit": natal["lots"]["Spirit"]["lon"]}
    ranked = {}
    for occ in occasions:
        pts = resolve_points(occ["points"], natal, lots_natal)
        rows = []
        for day in days:
            s, why, best, win = score_day(occ, day, pts, day["contacts"], day["_retro"], day["_shadow"], day["_ctx"], natal, sr_ctx)
            plus = [w for k, w in why if k == "+"]; minus = [w for k, w in why if k == "-"]
            rows.append({"date": day["date"], "raw": round(s, 2), "plus": plus[:5], "minus": minus[:4],
                         "best_window": ({"start": best[0].astimezone(tz).strftime("%-I:%M %p"),
                                          "end": best[1].astimezone(tz).strftime("%-I:%M %p"), "hour": best[2],
                                          "kind": best[3]} if best else None),
                         "asc_windows": [(a.astimezone(tz).strftime("%-I:%M %p"), b.astimezone(tz).strftime("%-I:%M %p")) for a, b in win]})
        lo = min(r["raw"] for r in rows); hi = max(r["raw"] for r in rows)
        for r in rows:
            r["score"] = int(round(100 * (r["raw"] - lo) / (hi - lo))) if hi > lo else 50
        order_ = sorted(rows, key=lambda r: (-r["raw"], r["date"]))
        for k, r in enumerate(order_, 1): r["rank"] = k
        for r in rows:
            r["stars"] = 5 if r["rank"] <= 12 else 4 if r["rank"] <= 45 else 3 if r["rank"] <= 130 else 2 if r["rank"] <= 260 else 1
        ranked[occ["key"]] = {"meta": {k: v for k, v in occ.items() if k != "points"} | {"points": sorted(pts)},
                              "days": rows}

    # overall "golden" and "hold" days (external occasions averaged)
    ext_keys = [o["key"] for o in occasions if o["kind"] == "external"]
    overall = []
    for i, day in enumerate(days):
        avg = sum(ranked[k]["days"][i]["score"] for k in ext_keys) / len(ext_keys)
        overall.append({"date": day["date"], "score": round(avg, 1)})
    overall_sorted = sorted(overall, key=lambda r: (-r["score"], r["date"]))
    for k, r in enumerate(overall_sorted, 1): r["rank"] = k

    for day in days:
        for k in ("_ctx", "_retro", "_shadow", "windows", "hours", "wake", "windows_sign"): day.pop(k, None)
        day["contacts"] = [c for c in day["contacts"] if c["orb"] <= (1.0 if c["t"] not in FAST else 1.5)]

    return {
        "generated": datetime.now(timezone.utc).isoformat(), "engine": "Swiss Ephemeris (pyswisseph, Moshier model)",
        "order": order, "year": args.year, "house_system": "whole sign",
        "orbs": TIGHT_ORB, "electional_rule": {"external_rising": ext_sign, "internal_rising": int_sign},
        "natal": natal, "solar_return": sr, "next_return_utc": next_t.isoformat(),
        "next_return_local": pretty_local(next_t, tz), "overlay": ov, "profection": prof,
        "year_events": {"ingresses": ingresses, "stations": stations, "mercury_shadows": shadows,
                        "lunations": lunations, "perfections": perfections, "slow_windows": windows,
                        "sensitive_windows": sens},
        "days": days, "occasions": ranked, "overall": overall,
    }

def phase_name(elong):
    if elong < 12 or elong >= 348: return "New Moon"
    if elong < 90: return "Waxing Crescent"
    if elong < 102: return "First Quarter"
    if elong < 180: return "Waxing Gibbous"
    if elong < 192: return "Full Moon"
    if elong < 270: return "Waning Gibbous"
    if elong < 282: return "Last Quarter"
    return "Waning Crescent"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="")
    ap.add_argument("--date", required=True); ap.add_argument("--time", required=True)
    ap.add_argument("--tz", required=True); ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True); ap.add_argument("--place", default="")
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--sr-lat", type=float); ap.add_argument("--sr-lon", type=float)
    ap.add_argument("--sr-tz"); ap.add_argument("--sr-place")
    ap.add_argument("--chiron", help="verified natal Chiron, e.g. \"Taurus 13°49'\"")
    ap.add_argument("--external-rising", default="Libra", help="rising sign for worldly elections")
    ap.add_argument("--internal-rising", default=None, help="rising sign for inner/ritual elections (default: natal rising)")
    ap.add_argument("--zones", help='JSON list of sensitive zones [{"label","lo","hi","signs"}]')
    ap.add_argument("--out", default="-")
    args = ap.parse_args()
    if args.internal_rising is None:
        tz = ZoneInfo(args.tz)
        local_dt = datetime.fromisoformat(f"{args.date}T{args.time}:00").replace(tzinfo=tz)
        cusps, ascmc = swe.houses_ex(jd_of(local_dt.astimezone(timezone.utc)), args.lat, args.lon, b'W', swe.FLG_MOSEPH)
        args.internal_rising = SIGNS[int(norm(ascmc[0]) // 30)]
    data = build(args)
    txt = json.dumps(data, indent=None, default=str)
    if args.out == "-": sys.stdout.write(txt)
    else: Path(args.out).write_text(txt)
    sys.stderr.write(f"solar return {data['solar_return']['local_pretty']} · {len(data['days'])} days · "
                     f"{len(data['year_events']['perfections'])} perfections · {len(data['occasions'])} occasions\n")

if __name__ == "__main__":
    main()
