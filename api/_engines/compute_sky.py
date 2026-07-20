# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/luna-astrologer-plugin/luna-astrologer/scripts/compute_sky.py
# Re-sync with bin/sync-engines.sh
#!/usr/bin/env python3
"""
compute_sky.py — Luna's local ephemeris engine (Swiss Ephemeris / pyswisseph).

Computes, for a given date + the user's natal chart:
  - today's planetary positions (sign, degree, RETROGRADE flag, SPEED)
  - the user's Whole-Sign house that each transiting body currently occupies
  - transiting-Moon aspects to the user's natal points today, WITH EXACT TIMES
  - faster-planet (Sun..Mars) + slow-planet contacts to natal planets/angles,
    each flagged exact-time (fast) or "in orb, no exact time" (slow/stationary)
  - the Moon's sign-ingress time today and whether it is void-of-course
  - standing context: current retrogrades + last/next lunation

No network. Deterministic. NASA JPL-based. This is what drives Luna's read — the
skill INTERPRETS this JSON; it never invents positions or times.

Usage:
    python3 compute_sky.py --config ../config.json --date 2026-07-16 > sky.json
    python3 compute_sky.py --config ../config.json           # defaults to today

Requires: pip install pyswisseph  (uses built-in Moshier model; no data files needed)
"""

import swisseph as swe
import json, argparse, sys
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
         "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

# transiting bodies we track
BODIES = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    "North Node": swe.MEAN_NODE,
}
# transiting Chiron needs the seas_*.se1 asteroid file (not in the Moshier model);
# natal Chiron is still a contact target. Never fake a Chiron transit.
PLANETS = [b for b in BODIES if b != "North Node"]

def sabian_degree(lon):
    """Sabian convention: round UP to the next whole degree (9°12' Virgo -> 10 Virgo)."""
    s, deg = sign_of(lon)
    return f"{int(deg) + 1} {s}"

CHALDEAN = ["Saturn","Jupiter","Mars","Sun","Venus","Mercury","Moon"]
DAY_RULER = {0:"Moon",1:"Mars",2:"Mercury",3:"Jupiter",4:"Venus",5:"Saturn",6:"Sun"}  # Mon=0

def planetary_hours(the_date, tz, lat, lon):
    """Planetary day + 24 unequal hours (sunrise->sunset->next sunrise), Chaldean order."""
    def sun_event(jd_from, rsmi):
        res, tret = swe.rise_trans(jd_from, swe.SUN, rsmi | swe.BIT_DISC_CENTER,
                                   (lon, lat, 0.0), 0.0, 0.0, swe.FLG_MOSEPH)
        if res != 0: raise RuntimeError("no rise/set")
        y, m, d, ut = swe.revjul(tret[0], swe.GREG_CAL)
        hh = int(ut); mm = (ut - hh) * 60
        return datetime(y, m, d, hh, int(mm), int((mm % 1) * 60), tzinfo=timezone.utc)
    try:
        day0 = datetime(the_date.year, the_date.month, the_date.day, 0, 0, tzinfo=tz)
        jd0 = jd_ut(day0.astimezone(timezone.utc))
        sunrise = sun_event(jd0, swe.CALC_RISE)
        sunset = sun_event(jd_ut(sunrise), swe.CALC_SET)
        next_rise = sun_event(jd_ut(sunset), swe.CALC_RISE)
        ruler = DAY_RULER[the_date.weekday()]
        start_idx = CHALDEAN.index(ruler)
        hours = []
        day_len = (sunset - sunrise) / 12; night_len = (next_rise - sunset) / 12
        for i in range(24):
            t0 = sunrise + day_len * i if i < 12 else sunset + night_len * (i - 12)
            t1 = t0 + (day_len if i < 12 else night_len)
            hours.append({"hour": i + 1, "ruler": CHALDEAN[(start_idx + i) % 7],
                          "start": t0.astimezone(tz).strftime("%-I:%M %p"),
                          "end": t1.astimezone(tz).strftime("%-I:%M %p"),
                          "phase": "day" if i < 12 else "night"})
        return {"day_ruler": ruler,
                "sunrise": sunrise.astimezone(tz).strftime("%-I:%M %p"),
                "sunset": sunset.astimezone(tz).strftime("%-I:%M %p"),
                "hours": hours}
    except Exception as e:
        return {"error": f"planetary hours unavailable: {e}"}
FAST = {"Moon","Sun","Mercury","Venus","Mars"}   # get exact times when aspecting
ASPECTS = {"conjunction":0.0,"sextile":60.0,"square":90.0,"trine":120.0,"opposition":180.0,
           "quincunx":150.0}
# orbs (degrees) for detecting an aspect as "in orb today" (quincunx tight per Shannon's standards)
ORB = {"conjunction":6.0,"sextile":4.0,"square":5.0,"trine":5.0,"opposition":6.0,"quincunx":2.0}
# the classical five (VoC and lunation work exclude the quincunx)
PTOLEMAIC = {"conjunction","sextile","square","trine","opposition"}
# tighter orb used when hunting the Moon's exact-minute perfection
MOON_EXACT_ORB = 0.20

# ---------- helpers ----------

def norm(a):  # normalize angle to [0,360)
    return a % 360.0

def sep(a, b):  # angular separation 0..180
    d = abs(norm(a) - norm(b)) % 360.0
    return 360.0 - d if d > 180.0 else d

def sign_of(lon):
    lon = norm(lon)
    return SIGNS[int(lon // 30)], lon % 30.0

def fmt_pos(lon, retro):
    s, deg = sign_of(lon)
    d = int(deg); m = int(round((deg - d) * 60))
    if m == 60: d += 1; m = 0
    return f"{s} {d}\u00b0{m:02d}'" + (" \u211e" if retro else "")

def jd_ut(dt_utc):
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                      dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600, swe.GREG_CAL)

def body_lonspeed(jd, body):
    # Moshier model, with speed; returns (lon, speed_deg_per_day)
    xx, _ = swe.calc_ut(jd, body, swe.FLG_MOSEPH | swe.FLG_SPEED)
    return norm(xx[0]), xx[3]

def parse_natal_lon(s):
    """Parse 'Virgo 9\u00b013'' or 'Pisces 18\u00b0' or 'Cancer 8\u00b036''' -> absolute longitude."""
    if not s or not s.strip():
        return None
    txt = s.strip()
    sign_idx = None
    for i, nm in enumerate(SIGNS):
        if txt.lower().startswith(nm.lower()):
            sign_idx = i; rest = txt[len(nm):]; break
    if sign_idx is None:
        return None
    digits = (rest.replace("\u00b0"," ").replace("'"," ").replace("\u2032"," ")
                  .replace('"'," ").replace("\u2033"," "))
    parts = [p for p in digits.replace("(", " ").replace(")"," ").split() if p.replace(".","",1).isdigit()]
    deg = float(parts[0]) if parts else 0.0
    minute = float(parts[1]) if len(parts) > 1 else 0.0
    second = float(parts[2]) if len(parts) > 2 else 0.0
    return sign_idx*30 + deg + minute/60.0 + second/3600.0

# ---------- core computations ----------

def whole_sign_house(natal_asc_lon, transit_lon):
    asc_sign = int(norm(natal_asc_lon)//30)
    t_sign = int(norm(transit_lon)//30)
    return ((t_sign - asc_sign) % 12) + 1

def positions_at(jd):
    out = {}
    for name, code in BODIES.items():
        lon, spd = body_lonspeed(jd, code)
        out[name] = {"lon":lon, "speed":spd, "retro":spd < 0,
                     "stationary":abs(spd) < 0.05 and name != "North Node",
                     "display":fmt_pos(lon, spd < 0), "sabian_degree":sabian_degree(lon)}
    return out

def moon_ingress_and_voc(day_start_utc, tz):
    """Find the Moon's sign at day start; if it changes today, find the ingress time;
    detect void-of-course = after Moon's last major aspect to a planet until ingress."""
    jd0 = jd_ut(day_start_utc)
    start_lon,_ = body_lonspeed(jd0, swe.MOON)
    start_sign = int(start_lon//30)
    # scan the day minute-ish (2-min steps) for a sign change
    ingress_dt = None; ingress_sign = None
    steps = int(24*60/2)
    prev_sign = start_sign
    for k in range(1, steps+1):
        dt = day_start_utc + timedelta(minutes=2*k)
        lon,_ = body_lonspeed(jd_ut(dt), swe.MOON)
        sgn = int(lon//30)
        if sgn != prev_sign:
            # refine to the minute
            lo, hi = dt - timedelta(minutes=2), dt
            for _ in range(6):
                mid = lo + (hi-lo)/2
                if int(body_lonspeed(jd_ut(mid), swe.MOON)[0]//30) != prev_sign:
                    hi = mid
                else:
                    lo = mid
            ingress_dt = hi; ingress_sign = sgn; break
        prev_sign = sgn
    return {
        "start_sign": SIGNS[start_sign],
        "ingress_local": ingress_dt.astimezone(tz).strftime("%-I:%M %p") if ingress_dt else None,
        "ingress_sign": SIGNS[ingress_sign] if ingress_sign is not None else None,
    }

def signed_delta(lon, target):
    """Signed shortest arc from target to lon, in (-180, 180]."""
    return (lon - target + 180.0) % 360.0 - 180.0

def aspect_targets(natal_pts):
    """Every longitude at which a transiting body perfects a major aspect to a natal
    point: natal_lon +/- angle (conjunction and opposition each yield one target)."""
    targets = []
    for pt, plon in natal_pts.items():
        for asp, ang in ASPECTS.items():
            offsets = {norm(ang), norm(-ang)}   # {0}, {180}, or {ang, 360-ang}
            for off in offsets:
                targets.append((pt, asp, norm(plon + off)))
    return targets

def perfection_times(day_start_utc, tz, body, natal_pts, step_min):
    """Moments today when a transiting body's longitude crosses an exact aspect degree
    to a natal point. Detects a sign flip of the signed arc to each target longitude,
    which catches conjunctions/oppositions (sep()-based tests can't) and handles
    retrograde motion."""
    hits = []
    targets = aspect_targets(natal_pts)
    steps = int(24*60/step_min)
    prev = None; prev_dt = None
    for k in range(0, steps+1):
        dt = day_start_utc + timedelta(minutes=step_min*k)
        lon,_ = body_lonspeed(jd_ut(dt), body)
        deltas = [signed_delta(lon, t[2]) for t in targets]
        if prev is not None:
            for i, (pt, asp, tlon) in enumerate(targets):
                d0, d1 = prev[i], deltas[i]
                if (d0 < 0) == (d1 < 0) or abs(d0) > 8 or abs(d1) > 8:
                    continue
                lo, hi = prev_dt, dt
                for _ in range(8):
                    mid = lo + (hi-lo)/2
                    dm = signed_delta(body_lonspeed(jd_ut(mid), body)[0], tlon)
                    if (dm < 0) == (d0 < 0): lo = mid
                    else: hi = mid
                hits.append({"point":pt,"aspect":asp,"dt":hi,
                             "time_local":hi.astimezone(tz).strftime("%-I:%M %p"),
                             "exact":True})
        prev = deltas; prev_dt = dt
    hits.sort(key=lambda h: h["dt"])
    for h in hits: del h["dt"]
    return hits

def moon_aspects_to_natal(day_start_utc, tz, natal):
    """For each natal point, find times today when transiting Moon perfects a major aspect."""
    natal_pts = {k:v for k,v in natal.items() if v is not None}
    return perfection_times(day_start_utc, tz, swe.MOON, natal_pts, step_min=4)

def slow_contacts_to_natal(day_start_utc, tz, natal, positions):
    """Non-Moon transiting planets in orb of a natal point today. Fast movers
    (Sun..Mars, not stationary) that actually perfect today get the real computed
    time; everything else => 'in orb, no exact time' — no false precision."""
    hits = []
    natal_pts = {k:v for k,v in natal.items() if v is not None}
    # real perfection times today for the fast non-Moon movers (10-min scan)
    exact = {}
    for tname in FAST - {"Moon"}:
        if positions[tname]["stationary"]: continue
        for h in perfection_times(day_start_utc, tz, BODIES[tname], natal_pts, step_min=10):
            exact[(tname, h["point"], h["aspect"])] = h["time_local"]
    for tname, tinfo in positions.items():
        if tname == "Moon": continue
        for pt, plon in natal_pts.items():
            for asp, ang in ASPECTS.items():
                s = sep(tinfo["lon"], plon)
                orb = s - ang
                if abs(orb) <= ORB[asp]:
                    # applying? check separation an hour later using current speed
                    lon_next = norm(tinfo["lon"] + tinfo["speed"]/24.0)
                    orb_next = sep(lon_next, plon) - ang
                    applying = abs(orb_next) < abs(orb)
                    t = exact.get((tname, pt, asp))
                    hits.append({
                        "transit": tname, "point": pt, "aspect": asp,
                        "orb": round(orb, 2),
                        "applying": applying,
                        "retro": tinfo["retro"], "stationary": tinfo["stationary"],
                        "timing": f"exact today {t}" if t else "in orb, no exact time",
                    })
    return hits

def transit_web(day_start_utc, positions):
    """The mundane aspect web: aspects among transiting planets (Moon excluded —
    its story is ingress + natal contacts). exact_today = the offset crosses zero
    between local midnight and midnight."""
    names = [n for n in positions if n not in ("Moon", "North Node")]
    jd0 = jd_ut(day_start_utc); jd1 = jd_ut(day_start_utc + timedelta(hours=24))
    lons0 = {n: body_lonspeed(jd0, BODIES[n])[0] for n in names}
    lons1 = {n: body_lonspeed(jd1, BODIES[n])[0] for n in names}
    hits = []
    for i, a in enumerate(names):
        for b in names[i+1:]:
            ia, ib = positions[a], positions[b]
            for asp, ang in ASPECTS.items():
                orb = sep(ia["lon"], ib["lon"]) - ang
                if abs(orb) <= ORB[asp]:
                    s_next = sep(norm(ia["lon"] + ia["speed"]/24.0),
                                 norm(ib["lon"] + ib["speed"]/24.0))
                    d0 = sep(lons0[a], lons0[b]) - ang
                    d1 = sep(lons1[a], lons1[b]) - ang
                    hits.append({
                        "a": a, "b": b, "aspect": asp, "orb": round(orb, 2),
                        "applying": abs(s_next - ang) < abs(orb),
                        "exact_today": d0 == 0.0 or (d0 < 0) != (d1 < 0),
                        "retro_involved": ia["retro"] or ib["retro"],
                        "stationary_involved": ia["stationary"] or ib["stationary"],
                    })
    hits.sort(key=lambda h: abs(h["orb"]))
    return hits

def standing_context(jd, tz, positions):
    """Retrogrades + the lunation arc: last and next New/Full Moon around today,
    found by scanning the Sun-Moon elongation for 0deg (new) / 180deg (full)
    crossings, then bisecting to the hour."""
    retros = [f"{n} \u211e" for n,i in positions.items() if i["retro"]]

    def elong(j):
        slon,_ = body_lonspeed(j, swe.SUN)
        mlon,_ = body_lonspeed(j, swe.MOON)
        return (mlon - slon) % 360.0

    events = []  # (jd, "New Moon"|"Full Moon", moon sign)
    step = 0.25  # 6-hour scan across +/-16 days
    j = jd - 16.0
    prev = elong(j)
    while j < jd + 16.0:
        jn = j + step
        cur = elong(jn)
        for target, label in ((0.0, "New Moon"), (180.0, "Full Moon")):
            d0 = (prev - target + 180.0) % 360.0 - 180.0
            d1 = (cur  - target + 180.0) % 360.0 - 180.0
            if d0 != 0.0 and (d0 < 0) != (d1 < 0) and abs(d0) < 90 and abs(d1) < 90:
                lo, hi = j, jn
                for _ in range(12):
                    mid = (lo+hi)/2
                    dm = (elong(mid) - target + 180.0) % 360.0 - 180.0
                    if (dm < 0) == (d0 < 0): lo = mid
                    else: hi = mid
                mlon,_ = body_lonspeed(hi, swe.MOON)
                events.append((hi, label, sign_of(mlon)[0]))
        prev = cur; j = jn

    def jd_to_local(j):
        y, m, d, ut = swe.revjul(j, swe.GREG_CAL)
        hh = int(ut); mm = int((ut-hh)*60)
        return datetime(y, m, d, hh, mm, tzinfo=timezone.utc).astimezone(tz)

    last = max((e for e in events if e[0] <= jd), default=None, key=lambda e: e[0])
    nxt  = min((e for e in events if e[0] >  jd), default=None, key=lambda e: e[0])
    def fmt(e):
        if not e: return None
        return {"event": f"{e[1]} in {e[2]}", "date_local": jd_to_local(e[0]).strftime("%B %-d, %-I:%M %p")}
    return {"retrogrades": retros, "last_lunation": fmt(last), "next_lunation": fmt(nxt)}

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: today in config tz)")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    tz = ZoneInfo(cfg.get("timezone","UTC"))
    natal_in = cfg.get("natal", {})
    natal = {k: parse_natal_lon(v) for k,v in natal_in.items()}
    # angles that matter for aspects
    natal_asc = natal.get("ascendant")
    natal_mc  = natal.get("midheaven")

    the_date = datetime.strptime(args.date,"%Y-%m-%d").date() if args.date else datetime.now(tz).date()
    day_start_local = datetime(the_date.year, the_date.month, the_date.day, 0,0, tzinfo=tz)
    day_start_utc = day_start_local.astimezone(timezone.utc)
    noon_local = day_start_local + timedelta(hours=12)
    jd_noon = jd_ut(noon_local.astimezone(timezone.utc))

    positions = positions_at(jd_noon)

    # whole-sign house each transiting body sits in (needs natal asc)
    if natal_asc is not None:
        for n,i in positions.items():
            i["whole_sign_house"] = whole_sign_house(natal_asc, i["lon"])

    result = {
        "date": the_date.isoformat(),
        "timezone": cfg.get("timezone"),
        "engine": f"Swiss Ephemeris (pyswisseph {swe.version}, Moshier)",
        "positions": positions,
        "moon": moon_ingress_and_voc(day_start_utc, tz),
        "moon_aspects_to_natal": moon_aspects_to_natal(day_start_utc, tz, natal),
        "slow_contacts_to_natal": slow_contacts_to_natal(day_start_utc, tz, natal, positions),
        "transit_web": transit_web(day_start_utc, positions),
        "standing_context": standing_context(jd_noon, tz, positions),
        "planetary_hours": (planetary_hours(the_date, tz, cfg["location"]["lat"], cfg["location"]["lon"])
                            if cfg.get("location") else None),
        "natal_used": {k: fmt_pos(v, False) for k,v in natal.items() if v is not None},
        "notes": [
            "Fast movers (Moon) carry exact times. Slow/stationary contacts are 'in orb, no exact time' by design.",
            "retro=true means review/revisit framing, never a launch signal.",
        ],
    }
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

if __name__ == "__main__":
    main()
