#!/usr/bin/env python3
"""The shared sky calendar: every retrograde station, shadow, New and Full
Moon and eclipse the growth pages quote, computed with the site's own
Swiss Ephemeris engine (api/_engines/compute_sky.py, Moshier model, the
same positions /api/moon and the daily horoscope use). Nothing on those
pages is typed in by hand: bin/gen_sky_pages.py renders them from the JSON
this writes, and tests/test_growth_features.py recomputes a sample of it.

Method, in one place:
  - Stations: scan the planet's longitudinal speed every 6 hours, then
    bisect the sign change to well under a minute.
  - Shadow: the pre-shadow begins when the planet, still direct, first
    reaches the degree where it will later station direct; the post-shadow
    ends when it clears the degree where it stationed retrograde.
  - New and Full Moons: scan the Sun-Moon elongation for 0 and 180 degrees,
    bisect to the second. Sign and degree are the Moon's at that moment.
  - Eclipses: swe.sol_eclipse_when_glob and swe.lun_eclipse_when, with the
    type read from the Swiss Ephemeris return flags.
  - Almanac names for Full Moons follow the North American almanac
    convention by calendar month in US Central time, with the Harvest Moon
    as the Full Moon nearest the September equinox (the Hunter's Moon is
    the one after it) and a Blue Moon as a second Full Moon in a month.

Usage: python3 bin/sky_calendar.py            (writes bin/sky_data/sky.json)
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_engines"))
import engines  # noqa: E402
import swisseph as swe  # noqa: E402

cs = engines.cs
CENTRAL = ZoneInfo("America/Chicago")
OUT = ROOT / "bin" / "sky_data" / "sky.json"

# The span the pages and the calendar feed cover.
FROM_YEAR, TO_YEAR = 2026, 2028

PLANETS = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
SHADOW_PLANETS = {"Mercury", "Venus", "Mars"}
SHADOW_SEARCH_DAYS = {"Mercury": 60, "Venus": 90, "Mars": 150}

MONTH_MOON = {1: "Wolf Moon", 2: "Snow Moon", 3: "Worm Moon", 4: "Pink Moon",
              5: "Flower Moon", 6: "Strawberry Moon", 7: "Buck Moon",
              8: "Sturgeon Moon", 9: "Corn Moon", 10: "Hunter's Moon",
              11: "Beaver Moon", 12: "Cold Moon"}


# ---------- time helpers ----------

def jd_of(dt_utc):
    return cs.jd_ut(dt_utc)


def dt_of(jd):
    y, m, d, ut = swe.revjul(jd, swe.GREG_CAL)
    base = datetime(y, m, d, tzinfo=timezone.utc)
    return base + timedelta(hours=ut)


def stamp(jd):
    """One moment, rounded to the minute, in UTC and US Central."""
    t = dt_of(jd)
    t = (t + timedelta(seconds=30)).replace(second=0, microsecond=0)
    c = t.astimezone(CENTRAL)
    return {"utc": t.strftime("%Y-%m-%dT%H:%MZ"),
            "central": c.strftime("%Y-%m-%dT%H:%M%z"),
            "central_date": c.date().isoformat(),
            "central_label": c.strftime("%a %b %-d, %Y, %-I:%M %p ") + c.tzname(),
            "utc_label": t.strftime("%b %-d, %Y, %H:%M UTC")}


def lon(jd, name):
    return cs.body_lonspeed(jd, cs.BODIES[name])[0]


def speed(jd, name):
    return cs.body_lonspeed(jd, cs.BODIES[name])[1]


def pos(lon_deg):
    sign, deg = cs.sign_of(lon_deg)
    d = int(deg)
    m = int(round((deg - d) * 60))
    if m == 60:
        d, m = d + 1, 0
    return {"sign": sign, "deg": d, "min": m, "lon": round(lon_deg, 4),
            "label": f"{d}°{m:02d}′ {sign}"}


def bisect(a, b, pred, iters=40):
    """pred(a) is False, pred(b) is True; return the boundary."""
    for _ in range(iters):
        mid = (a + b) / 2
        if pred(mid):
            b = mid
        else:
            a = mid
    return b


def signed(a, target):
    return (a - target + 180.0) % 360.0 - 180.0


# ---------- retrogrades ----------

def stations(name, jd0, jd1, step=0.25):
    """Every station between jd0 and jd1: (jd, 'R' or 'D')."""
    out = []
    j, s = jd0, speed(jd0, name)
    while j < jd1:
        jn = j + step
        sn = speed(jn, name)
        if (s >= 0) != (sn >= 0):
            kind = "R" if s >= 0 else "D"
            t = bisect(j, jn, lambda x, s0=s: (speed(x, name) >= 0) != (s0 >= 0))
            out.append((t, kind))
        j, s = jn, sn
    return out


def crossing(name, target, start, direction, limit_days, step=0.25):
    """First moment, walking from `start` in `direction` (+1 or -1), when the
    planet moving DIRECT sits exactly on `target` longitude."""
    j = start
    prev = signed(lon(j, name), target)
    for _ in range(int(limit_days / step)):
        jn = j + direction * step
        cur = signed(lon(jn, name), target)
        if abs(prev) < 90 and abs(cur) < 90 and (prev < 0) != (cur < 0):
            lo, hi = (j, jn) if direction > 0 else (jn, j)
            neg_first = signed(lon(lo, name), target) < 0
            t = bisect(lo, hi, lambda x: (signed(lon(x, name), target) < 0) != neg_first)
            if speed(t, name) > 0:
                return t
        j, prev = jn, cur
    return None


def signs_between(name, jd_a, jd_b, step=0.5):
    seen = []
    j = jd_a
    while j <= jd_b:
        s = cs.sign_of(lon(j, name))[0]
        if s not in seen:
            seen.append(s)
        j += step
    s = cs.sign_of(lon(jd_b, name))[0]
    if s not in seen:
        seen.append(s)
    return seen


def retrogrades(name, from_year, to_year):
    """Every retrograde of `name` that touches from_year..to_year."""
    jd0 = swe.julday(from_year - 1, 6, 1, 0)
    jd1 = swe.julday(to_year + 1, 9, 1, 0)
    st = stations(name, jd0, jd1)
    out = []
    for i, (j, kind) in enumerate(st):
        if kind != "R" or i + 1 >= len(st) or st[i + 1][1] != "D":
            continue
        jr, jdir = j, st[i + 1][0]
        r_year, d_year = dt_of(jr).year, dt_of(jdir).year
        if d_year < from_year or r_year > to_year:
            continue
        lr, ld = lon(jr, name), lon(jdir, name)
        row = {"planet": name,
               "station_retrograde": {**stamp(jr), **pos(lr)},
               "station_direct": {**stamp(jdir), **pos(ld)},
               "days": round(jdir - jr),
               "signs": signs_between(name, jr, jdir)}
        if name in SHADOW_PLANETS:
            lim = SHADOW_SEARCH_DAYS[name]
            pre = crossing(name, ld, jr - 0.5, -1, lim)
            post = crossing(name, lr, jdir + 0.5, +1, lim)
            row["shadow_begins"] = stamp(pre) if pre else None
            row["shadow_ends"] = stamp(post) if post else None
        out.append(row)
    return out


# ---------- lunations and eclipses ----------

def elong(j):
    return (lon(j, "Moon") - lon(j, "Sun")) % 360.0


def lunations(from_year, to_year, step=0.25):
    jd0 = swe.julday(from_year, 1, 1, 0) - 2
    jd1 = swe.julday(to_year + 1, 1, 1, 0) + 2
    out = []
    j, prev = jd0, elong(jd0)
    while j < jd1:
        jn = j + step
        cur = elong(jn)
        for target, kind in ((0.0, "new"), (180.0, "full")):
            d0, d1 = signed(prev, target), signed(cur, target)
            if abs(d0) < 90 and abs(d1) < 90 and d0 < 0 <= d1:
                t = bisect(j, jn, lambda x, tg=target: signed(elong(x), tg) >= 0)
                out.append({"kind": kind, "jd": t, **stamp(t), **pos(lon(t, "Moon"))})
        j, prev = jn, cur
    return [e for e in out if from_year <= int(e["central_date"][:4]) <= to_year]


SOLAR_TYPES = [(swe.ECL_ANNULAR_TOTAL, "hybrid"), (swe.ECL_TOTAL, "total"),
               (swe.ECL_ANNULAR, "annular"), (swe.ECL_PARTIAL, "partial")]
LUNAR_TYPES = [(swe.ECL_TOTAL, "total"), (swe.ECL_PARTIAL, "partial"),
               (swe.ECL_PENUMBRAL, "penumbral")]


def _type(flags, table):
    for bit, label in table:
        if flags & bit:
            return label
    return "unknown"


def eclipses(from_year, to_year):
    jd0 = swe.julday(from_year, 1, 1, 0) - 2
    jd1 = swe.julday(to_year + 1, 1, 1, 0) + 2
    out = []
    t = jd0
    while True:
        flags, tret = swe.sol_eclipse_when_glob(t, swe.FLG_MOSEPH, 0)
        peak = tret[0]
        if peak >= jd1:
            break
        _, geo, attr = swe.sol_eclipse_where(peak, swe.FLG_MOSEPH)
        row = {"kind": "solar", "type": _type(flags, SOLAR_TYPES), "jd": peak,
               "node": pos(lon(peak, "North Node")),
               "magnitude": round(attr[0], 3),
               "greatest_at": {"lat": round(geo[1], 1), "lon": round(geo[0], 1),
                               "near": nearest_city(geo[1], geo[0])},
               **stamp(peak), **pos(lon(peak, "Moon"))}
        if row["type"] in ("total", "annular", "hybrid"):
            _, tl, _ = swe.sol_eclipse_when_loc(peak - 0.3, (geo[0], geo[1], 0.0), swe.FLG_MOSEPH)
            if tl[2] and tl[3]:
                row["central_seconds"] = round((tl[3] - tl[2]) * 86400)
        out.append(row)
        t = peak + 20
    t = jd0
    while True:
        flags, tret = swe.lun_eclipse_when(t, swe.FLG_MOSEPH, 0)
        peak = tret[0]
        if peak >= jd1:
            break
        how = swe.lun_eclipse_how(peak, (0.0, 0.0, 0.0), swe.FLG_MOSEPH)
        out.append({"kind": "lunar", "type": _type(flags, LUNAR_TYPES), "jd": peak,
                    "node": pos(lon(peak, "North Node")),
                    "magnitude": round(how[1][0], 3),
                    "penumbral_magnitude": round(how[1][1], 3),
                    **stamp(peak), **pos(lon(peak, "Moon"))})
        t = peak + 20
    out = [e for e in out if from_year <= int(e["central_date"][:4]) <= to_year]
    return sorted(out, key=lambda e: e["jd"])


def nearest_city(lat, lon_deg, limit_km=400):
    """Nearest place in the site's own GeoNames city list (api/_data), or
    None when the greatest eclipse falls over open water."""
    import csv
    import math
    best = None
    with open(ROOT / "api" / "_data" / "cities.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            la, lo = math.radians(float(r["lat"])), math.radians(float(r["lon"]))
            a, b = math.radians(lat), math.radians(lon_deg)
            d = 6371 * math.acos(max(-1.0, min(1.0, math.sin(a) * math.sin(la)
                                 + math.cos(a) * math.cos(la) * math.cos(b - lo))))
            if best is None or d < best[0]:
                best = (d, r)
    if best is None or best[0] > limit_km:
        return None
    d, r = best
    return {"name": r["name"], "country": r["country"], "km": round(d)}


def september_equinox(year):
    a = swe.julday(year, 9, 15, 0)
    b = swe.julday(year, 9, 30, 0)
    return bisect(a, b, lambda x: signed(lon(x, "Sun"), 180.0) >= 0)


def name_full_moons(lunes):
    """Almanac names, by calendar month in US Central time."""
    fulls = [e for e in lunes if e["kind"] == "full"]
    for e in fulls:
        e["name"] = MONTH_MOON[int(e["central_date"][5:7])]
    for year in sorted({int(e["central_date"][:4]) for e in fulls}):
        eq = september_equinox(year)
        yr = [e for e in fulls if int(e["central_date"][:4]) == year]
        harvest = min(yr, key=lambda e: abs(e["jd"] - eq))
        i = fulls.index(harvest)
        harvest["name"] = "Harvest Moon"
        if i + 1 < len(fulls):
            fulls[i + 1]["name"] = "Hunter's Moon"
        if harvest["central_date"][5:7] == "10":
            for e in yr:
                if e["central_date"][5:7] == "09" and e is not harvest:
                    e["name"] = "Corn Moon"
    seen = {}
    for e in fulls:
        key = e["central_date"][:7]
        if key in seen:
            e["blue_moon"] = True
        seen[key] = True
    return lunes


def mark_eclipses(lunes, ecl):
    for e in lunes:
        for x in ecl:
            if abs(e["jd"] - x["jd"]) < 1.0 and (
                    (e["kind"] == "new") == (x["kind"] == "solar")):
                e["eclipse"] = f"{x['type']} {x['kind']} eclipse"
    return lunes


def compute(from_year=FROM_YEAR, to_year=TO_YEAR):
    ecl = eclipses(from_year, to_year)
    lunes = mark_eclipses(name_full_moons(lunations(from_year, to_year)), ecl)
    retro = {p: retrogrades(p, from_year, to_year) for p in PLANETS}
    return {"method": "Swiss Ephemeris (Moshier model) via the site engine, "
                      "api/_engines/compute_sky.py; see bin/sky_calendar.py",
            "from_year": from_year, "to_year": to_year,
            "retrogrades": retro, "lunations": lunes, "eclipses": ecl}


def main():
    data = compute()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    m = data["retrogrades"]["Mercury"]
    print(f"wrote {OUT.relative_to(ROOT)}: {len(data['lunations'])} lunations, "
          f"{len(data['eclipses'])} eclipses, "
          + ", ".join(f"{p} {len(v)}" for p, v in data["retrogrades"].items()) + " retrogrades")
    for r in m:
        print("  Mercury Rx", r["station_retrograde"]["utc"], "->", r["station_direct"]["utc"],
              "shadow", (r["shadow_begins"] or {}).get("utc"), "..", (r["shadow_ends"] or {}).get("utc"))
    for e in data["eclipses"]:
        print("  ", e["kind"], e["type"], e["utc"], e["label"])


if __name__ == "__main__":
    main()
