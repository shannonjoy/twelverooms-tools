"""POST /api/horoscope — a personalized one-day reading from birth data.

Body: {date, time?, tz, lat, lon, day, view_tz?}
  date/time/tz/lat/lon  the birth data (same shape as /api/natal)
  day                   the date to read, YYYY-MM-DD
  view_tz               IANA zone the times should be shown in; defaults to
                        the birth zone, since that is all we are given

Computes the natal chart, then the sky for `day`, then assembles the ledger:
transiting-Moon contacts to natal points with exact times, inner-planet
contacts that actually perfect that day, and at most one background line for a
slow or stationary contact still in orb. Contacts that are merely in orb are
left out — a nearing aspect belongs to the day it perfects.

Birth data is processed in memory and never stored or logged.
"""
import json
import sys
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "_engines"))
sys.path.insert(0, str(HERE / "_copy"))
import engines  # noqa: E402
import horoscope_copy as hc  # noqa: E402

cs = engines.cs
cf = engines.cf

# Natal points we read contacts against.
POINTS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
          "Uranus", "Neptune", "Pluto", "Chiron", "North Node"]
ANGLES = {"ASC", "MC"}
# How much a contact weighs when choosing the day's headline.
BODY_WEIGHT = {"Pluto": 5, "Neptune": 5, "Uranus": 5, "Saturn": 4, "Jupiter": 3,
               "Mars": 3, "Venus": 2, "Mercury": 2, "Sun": 3, "Moon": 1}
MAX_YEARS = 5


def _minutes(t):
    """'2:14 PM' -> minutes past midnight. None for untimed entries."""
    if not t:
        return None
    try:
        d = datetime.strptime(t.strip(), "%I:%M %p")
    except ValueError:
        return None
    return d.hour * 60 + d.minute


def _natal_points(natal):
    """Absolute longitudes for every natal point we can read. Angles are
    included only when the chart is timed — they move too fast to guess."""
    pts = {}
    for p in POINTS:
        e = (natal.get("planets") or {}).get(p)
        if e:
            pts[p] = e["lon"]
    if natal.get("timed"):
        if natal.get("asc"):
            pts["ASC"] = natal["asc"]["lon"]
        if natal.get("mc"):
            pts["MC"] = natal["mc"]["lon"]
    return pts


def _weight(body, aspect, point):
    w = BODY_WEIGHT.get(body, 2)
    if point in ANGLES or point in ("Sun", "Moon"):
        w += 2
    if aspect in hc.HARD:
        w += 1
    if aspect == "conjunction":
        w += 1
    return w


def _entry(body, aspect, point, time_local, retro=False, stationary=False,
           background=False):
    return {
        "body": body,
        "aspect": aspect,
        "point": point,
        "point_pretty": hc.pretty(point),
        "headline": hc.headline(body, aspect, point),
        "symbol": hc.symbol(body, aspect, point),
        "line": hc.line(body, aspect, point, retro=retro, stationary=stationary),
        "tone": hc.tone(aspect),
        "time_local": time_local,
        "time_minutes": _minutes(time_local),
        "retro": retro,
        "stationary": stationary,
        "background": background,
        "weight": _weight(body, aspect, point),
    }


def build_ledger(slow_hits, moon_hits):
    """The day's timed spine, plus at most one background line.

    Only contacts that actually perfect today get a place on the clock.
    Everything merely in orb is dropped, except one background note so the
    reader knows what is sitting over the day without being handed a minute
    that does not exist."""
    timed = []

    for h in slow_hits:
        timing = h.get("timing") or ""
        if not timing.startswith("exact today"):
            continue
        t = timing.replace("exact today", "").strip() or None
        if not t:
            continue
        timed.append(_entry(h["transit"], h["aspect"], h["point"], t,
                            retro=h.get("retro", False),
                            stationary=h.get("stationary", False)))

    for h in moon_hits:
        timed.append(_entry("Moon", h["aspect"], h["point"], h.get("time_local")))

    timed.sort(key=lambda e: (e["time_minutes"] is None, e["time_minutes"] or 0))

    slow_bodies = ("Jupiter", "Saturn", "Uranus", "Neptune", "Pluto")
    candidates = [
        h for h in slow_hits
        if not (h.get("timing") or "").startswith("exact today")
        and h.get("applying")
        and (h.get("stationary") or h["transit"] in slow_bodies or h["point"] in ANGLES)
    ]
    background = None
    if candidates:
        best = max(candidates,
                   key=lambda h: (_weight(h["transit"], h["aspect"], h["point"]),
                                  -abs(h.get("orb", 9))))
        background = _entry(best["transit"], best["aspect"], best["point"], None,
                            retro=best.get("retro", False),
                            stationary=best.get("stationary", False),
                            background=True)
        background["orb"] = best.get("orb")

    return timed, background


def pick_featured(timed, background):
    """The day's headline: the heaviest contact that actually perfects today.
    Weight already favours the angles and the slower bodies, so a 3am Moon
    contact does not outrank Saturn on the Midheaven. Falls back to the
    background line when nothing perfects at all."""
    if timed:
        return max(timed, key=lambda e: (e["weight"], -(e["time_minutes"] or 0)))
    return background


def compute(o):
    tz_name = str(o["tz"]).strip()
    view_name = str(o.get("view_tz") or tz_name).strip()
    try:
        tz = ZoneInfo(view_name)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError(f"Unknown timezone: {view_name}")

    try:
        day = date.fromisoformat(str(o["day"]).strip())
    except ValueError:
        raise ValueError("Pick a date to read, as YYYY-MM-DD.")
    if abs((day - date.today()).days) > MAX_YEARS * 366:
        raise ValueError(f"Pick a date within {MAX_YEARS} years of today.")

    try:
        lat, lon = float(o["lat"]), float(o["lon"])
    except (TypeError, ValueError):
        raise ValueError("Pick your birthplace from the list, or enter coordinates.")

    order = {"name": "Daily reading", "date": o["date"], "time": o.get("time") or None,
             "tz": tz_name, "lat": lat, "lon": lon,
             "place": str(o.get("place", ""))[:80]}
    try:
        natal = cf.build_natal(order)[0]
    except ValueError:
        raise ValueError("Check your birth date and time, then try again.")
    natal_pts = _natal_points(natal)
    if not natal_pts:
        raise ValueError("Could not read that birth chart.")

    day_start_local = datetime(day.year, day.month, day.day, 0, 0, tzinfo=tz)
    day_start_utc = day_start_local.astimezone(timezone.utc)
    jd_noon = cs.jd_ut((day_start_local + timedelta(hours=12)).astimezone(timezone.utc))

    positions = cs.positions_at(jd_noon)
    if "ASC" in natal_pts:
        for info in positions.values():
            info["whole_sign_house"] = cs.whole_sign_house(natal_pts["ASC"], info["lon"])

    moon = cs.moon_ingress_and_voc(day_start_utc, tz)
    moon_hits = cs.moon_aspects_to_natal(day_start_utc, tz, natal_pts)
    slow_hits = cs.slow_contacts_to_natal(day_start_utc, tz, natal_pts, positions)
    web = cs.transit_web(day_start_utc, positions)
    ctx = cs.standing_context(jd_noon, tz, positions)

    timed, background = build_ledger(slow_hits, moon_hits)
    featured = pick_featured(timed, background)
    engine = f"the Swiss Ephemeris (pyswisseph {cs.swe.version}, Moshier)"
    day_label = day_start_local.strftime("%A, %B %-d, %Y")

    return {
        "day": day.isoformat(),
        "day_label": day_label,
        "timezone": view_name,
        "timed": bool(natal.get("timed")),
        "engine": engine,
        "sky": hc.sky_summary(moon, positions, web),
        "arc": hc.arc_line(ctx),
        "featured": featured,
        "ledger": timed,
        "background": background,
        "windows": hc.windows(timed),
        "moon": {"sign": moon.get("start_sign"),
                 "ingress_sign": moon.get("ingress_sign"),
                 "ingress_local": moon.get("ingress_local"),
                 "house": positions["Moon"].get("whole_sign_house")},
        "natal_used": {hc.pretty(k): cs.fmt_pos(v, False) for k, v in natal_pts.items()},
        "note": hc.note(day_label, engine),
        "method": "Swiss Ephemeris (Moshier), whole-sign houses",
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            for field in ("date", "tz", "lat", "lon", "day"):
                if not str(o.get(field) or "").strip():
                    raise ValueError(f"Missing {field}.")
            body, code = json.dumps(compute(o)).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
