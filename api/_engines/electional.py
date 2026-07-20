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
import swisseph as swe
from datetime import datetime, timedelta, timezone, date as date_cls
from zoneinfo import ZoneInfo

import engines

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
       apply_w=3, avoid_w=-3):
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
    # Money, work, enterprise
    _r("business", "Starting a business", "Work",
       ["Jupiter", "Mercury", "Sun"], ["Saturn", "Mars"], ["Jupiter", "Mercury", "Sun"], "waxing",
       angular=("Jupiter",), retro=["Mercury"]),
    _r("contract", "Signing a contract", "Work",
       ["Mercury", "Jupiter"], ["Mars", "Saturn"], ["Mercury", "Jupiter"], "waxing",
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4),
    _r("launch", "Product launch / going live", "Work",
       ["Jupiter", "Sun"], ["Saturn", "Mars"], ["Sun", "Jupiter"], "waxing",
       angular=("Sun", "Jupiter")),
    _r("job", "Job interview / new job", "Work",
       ["Sun", "Jupiter", "Mercury"], ["Saturn", "Mars"], ["Sun", "Jupiter", "Mercury"], "waxing",
       angular=("Jupiter",), retro=["Mercury"]),
    _r("raise", "Raise / salary negotiation", "Work",
       ["Jupiter", "Venus"], ["Saturn", "Mars"], ["Jupiter", "Venus"], "waxing",
       angular=("Jupiter",), avoid_w=-4),
    _r("shop", "Opening a shop / restaurant", "Work",
       ["Venus", "Jupiter"], ["Saturn", "Mars"], ["Venus", "Jupiter"], "waxing",
       retro=["Mercury"]),
    _r("investment", "Investment / opening an account", "Work",
       ["Jupiter", "Venus"], ["Saturn", "Mars"], ["Jupiter", "Venus"], "waxing",
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4),
    _r("publishing", "Publishing / book launch", "Work",
       ["Jupiter", "Mercury", "Sun"], ["Saturn", "Mars"], ["Mercury", "Jupiter", "Sun"], "waxing",
       angular=("Jupiter", "Sun"), retro=["Mercury"]),
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
       angular=("Jupiter",), retro=["Mercury"], avoid_w=-4),
]
RECIPES_BY_KEY = {r["key"]: r for r in RECIPES}

jd_ut = engines.cs.jd_ut
body_lonspeed = engines.cs.body_lonspeed
signed_delta = engines.cs.signed_delta


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

def scan(criteria, get_chart=None):
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

    needs_angles = any(r["rule"] == "benefic_on_angle" for r in c["hard"] + c["soft"])
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
        })

    out.sort(key=lambda w: (-w["peak_score"], -w["duration_min"]))
    return {"windows": out[:c["top_n"]],
            "scanned_days": days,
            "total_windows": len(out),
            "voc_intervals": [
                {"from": v0.astimezone(tz).strftime("%a %b %-d %-I:%M %p"),
                 "to": v1.astimezone(tz).strftime("%a %b %-d %-I:%M %p")}
                for v0, v1 in vocs if v1 > start_utc]}
