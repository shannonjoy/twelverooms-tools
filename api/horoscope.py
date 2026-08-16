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

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
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
# A sky event outranks any personal contact for the headline: a Full Moon is the
# day, a station is the day, an ingress is close. Set above the contact ceiling
# (Pluto on an angle, hard, tops out around 9).
EVENT_WEIGHT = {"lunation": 14, "station": 12, "ingress": 10}
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


def _detail(time_local, orb, applying):
    """The small transparency line under a contact: an exact minute for fast
    contacts, an orb and direction for the slow ones sitting over the day."""
    if time_local:
        return f"exact {time_local}"
    if orb is not None:
        return f"{abs(orb):.1f}° {'applying' if applying else 'separating'}"
    return None


def _base(headline, symbol, line, tone, time_local, weight, *, retro=False,
          stationary=False, background=False, house=None, orb=None,
          applying=None, is_event=False):
    return {
        "headline": headline,
        "symbol": symbol,
        "line": line,
        "tone": tone,
        "time_local": time_local,
        "time_minutes": _minutes(time_local),
        "retro": retro,
        "stationary": stationary,
        "background": background,
        "house": house,
        "house_tag": hc.house_tag(house),
        "orb": orb,
        "applying": applying,
        "detail": _detail(time_local, orb, applying),
        "is_event": is_event,
        "weight": weight,
    }


def _entry(body, aspect, point, time_local, retro=False, stationary=False,
           background=False, house=None, orb=None, applying=None):
    e = _base(hc.headline(body, aspect, point), hc.symbol(body, aspect, point),
              hc.line(body, aspect, point, retro=retro, stationary=stationary),
              hc.tone(aspect), time_local, _weight(body, aspect, point),
              retro=retro, stationary=stationary, background=background,
              house=house, orb=orb, applying=applying)
    e.update({"body": body, "aspect": aspect, "point": point,
              "point_pretty": hc.pretty(point)})
    return e


def _event_entry(ev, house=None):
    e = _base(hc.event_headline(ev), hc.event_symbol(ev), hc.event_line(ev, house),
              hc.event_tone(ev), ev.get("time_local"),
              EVENT_WEIGHT.get(ev["type"], 8), house=house, is_event=True)
    e.update({"body": ev.get("body"), "aspect": ev["type"], "point": None,
              "event_type": ev["type"], "event_kind": ev.get("kind") or ev.get("direction"),
              # The same line without its house clause. The sky headline card
              # uses this one, because the bridge sentence directly beneath it
              # already places the event in a house and saying it twice in
              # three inches reads as a stutter.
              "line_sky": hc.event_line(ev, None)})
    return e


def build_ledger(slow_hits, moon_hits, events, house_of_point, house_of_sign):
    """The day's timed spine: sky events, inner-planet perfections, and Moon
    contacts, all on the clock in the order they arrive, plus at most one
    background line for a slow contact sitting over the day."""
    timed = []

    for ev in events:
        house = house_of_sign(ev.get("sign"))
        timed.append(_event_entry(ev, house))

    for h in slow_hits:
        timing = h.get("timing") or ""
        if not timing.startswith("exact today"):
            continue
        t = timing.replace("exact today", "").strip() or None
        if not t:
            continue
        timed.append(_entry(h["transit"], h["aspect"], h["point"], t,
                            retro=h.get("retro", False),
                            stationary=h.get("stationary", False),
                            house=house_of_point(h["point"]),
                            orb=h.get("orb"), applying=h.get("applying")))

    for h in moon_hits:
        timed.append(_entry("Moon", h["aspect"], h["point"], h.get("time_local"),
                            house=house_of_point(h["point"])))

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
                            background=True, house=house_of_point(best["point"]),
                            orb=best.get("orb"), applying=best.get("applying"))

    return timed, background


# How close a sky event has to come to a natal point before the bridge names it.
BRIDGE_ORB = 3.0
BRIDGE_ASPECTS = {0: "conjunction", 60: "sextile", 90: "square",
                  120: "trine", 180: "opposition"}


def pick_featured(timed, background):
    """Two headlines, not one: what the sky is doing, and what it is doing to you.

    They used to compete for a single slot, with EVENT_WEIGHT deliberately set
    above the personal ceiling so a Full Moon would win. That meant on roughly a
    dozen days a month the reader's own reading was silently demoted by a public
    event, which is the thing every sun-sign column already tells them. Separate
    pools, so the sky can be loud without taking the reader's place.

    Returns (sky, personal). `sky` is None on a day with no public event;
    `personal` falls back to the background contact when nothing perfects.
    """
    key = lambda e: (e["weight"], -(e["time_minutes"] or 0))
    # A Moon ingress is not news. It happens twelve times a month, the Moon's
    # sign is already on the page twice, and letting it hold the sky headline
    # would fill that slot with ambient weather on most days. It stays in the
    # ledger, where it is a real timed event; it just never leads.
    events = [e for e in timed if e.get("is_event")
              and not (e.get("event_type") == "ingress" and e.get("body") == "Moon")]
    contacts = [e for e in timed if not e.get("is_event")]
    sky = max(events, key=key) if events else None
    personal = max(contacts, key=key) if contacts else background
    return sky, personal


def event_lon(ev, positions):
    """Where a sky event sits, in ecliptic longitude.

    Derived rather than measured, so this needs no change to compute_sky.py
    (a generated copy synced from the Luna engine). An ingress is 0 degrees of
    the new sign by definition. For a lunation or a station the body's noon
    position is within a few arcminutes of the exact moment, and a stationing
    planet is by definition barely moving. Well inside BRIDGE_ORB either way.
    """
    if ev["type"] == "ingress":
        try:
            return cs.SIGNS.index(ev["to_sign"]) * 30.0
        except (ValueError, KeyError):
            return None
    info = positions.get(ev.get("body") or "")
    return info.get("lon") if info else None


def natal_hit(lon, natal_pts):
    """The tightest major aspect this longitude makes to a natal point, as
    (point, aspect), or None. Angles win ties at equal orb: a Full Moon on the
    Midheaven is a more useful sentence than one on Neptune."""
    if lon is None:
        return None
    best = None
    for name, nlon in natal_pts.items():
        sep = abs((lon - nlon + 180.0) % 360.0 - 180.0)
        for angle, aspect in BRIDGE_ASPECTS.items():
            orb = abs(sep - angle)
            if orb > BRIDGE_ORB:
                continue
            rank = (orb, 0 if name in ANGLES else 1)
            if best is None or rank < best[0]:
                best = (rank, (name, aspect))
    return best[1] if best else None


# Bodies drawn on the wheel. Chiron and the nodes are left off deliberately:
# at this size the ring gets crowded and the day's story is never about them.
WHEEL_BODIES = ("Sun", "Moon", "Mercury", "Venus", "Mars",
                "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto")


def wheel_data(natal_pts, positions, timed):
    """Longitudes for drawing the day on the reader's own wheel.

    Deliberately raw numbers rather than an SVG: gen_wheel.py draws a natal
    chart, it is a generated copy synced from the factsheet engine, and it has
    no concept of a transit ring. Sending longitudes lets the page draw the
    biwheel without touching a shared engine or adding an endpoint.

    `asc` is null on an untimed chart, in which case the page orients the wheel
    from 0 Aries and draws no house numbers, because there are none.
    """
    natal = {k: round(v, 3) for k, v in natal_pts.items()}
    transit = {b: round(i["lon"], 3) for b, i in positions.items()
               if b in WHEEL_BODIES and i.get("lon") is not None}
    lines = []
    for e in timed:
        if e.get("is_event") or not e.get("point"):
            continue
        a, b = transit.get(e.get("body")), natal.get(e.get("point"))
        if a is None or b is None:
            continue
        lines.append({"from": a, "to": b, "tone": e.get("tone"),
                      "label": e.get("headline")})
    return {"asc": natal.get("ASC"), "natal": natal,
            "transit": transit, "lines": lines}


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

    # Whole-sign house helpers, so every line can say which room of your life it
    # touches. Points map through their own natal sign; a sky event maps through
    # the sign it happens in. Both are None on an untimed chart (no Ascendant).
    asc_sign = int(natal_pts["ASC"] // 30) if "ASC" in natal_pts else None

    def house_of_point(pt):
        if asc_sign is None or pt not in natal_pts:
            return None
        return (int(natal_pts[pt] // 30) - asc_sign) % 12 + 1

    def house_of_sign(sign_name):
        if asc_sign is None or not sign_name:
            return None
        try:
            return (cs.SIGNS.index(sign_name) - asc_sign) % 12 + 1
        except ValueError:
            return None

    phase = cs.moon_phase(jd_noon)
    events = cs.sky_events_today(day_start_utc, tz, positions)
    moon = cs.moon_ingress_and_voc(day_start_utc, tz)
    moon_hits = cs.moon_aspects_to_natal(day_start_utc, tz, natal_pts)
    slow_hits = cs.slow_contacts_to_natal(day_start_utc, tz, natal_pts, positions)
    web = cs.transit_web(day_start_utc, positions)
    ctx = cs.standing_context(jd_noon, tz, positions)

    timed, background = build_ledger(slow_hits, moon_hits, events,
                                     house_of_point, house_of_sign)
    sky_featured, featured = pick_featured(timed, background)

    # The bridge: the day's loudest public event, placed inside this chart.
    # Written by rule here. The narrative version is a signed-in feature, held
    # per membership-spec.md; this stays the free reading and the fallback.
    bridge = None
    if sky_featured is not None:
        ev = next((e for e in events
                   if e["type"] == sky_featured.get("event_type")
                   and e.get("time_local") == sky_featured.get("time_local")), None)
        if ev is not None:
            bridge = hc.bridge_line(ev, house_of_sign(ev.get("sign")),
                                    natal_hit(event_lon(ev, positions), natal_pts))
    windows = hc.windows(timed)
    has_lunation = any(e["type"] == "lunation" for e in events)
    energy = hc.energy_line(featured, timed, phase, has_lunation)
    close = hc.closing_line(windows, featured)

    # Only glossary terms the day actually uses, for teach-on-tap.
    terms = set()
    for e in timed + ([background] if background else []):
        if e.get("is_event"):
            k = e.get("event_kind")
            if k in ("Full Moon", "New Moon"):
                terms.add(k)
            if k == "retrograde":
                terms.add("retrograde")
        else:
            terms.add(e.get("aspect"))
            if e.get("point") == "ASC":
                terms.add("Ascendant")
            if e.get("point") == "MC":
                terms.add("Midheaven")
        d = e.get("detail") or ""
        if "applying" in d:
            terms.update(("orb", "applying"))
        if "separating" in d:
            terms.update(("orb", "separating"))
        if e.get("retro"):
            terms.add("retrograde")
        if e.get("stationary"):
            terms.add("stationary")
    terms.add("whole-sign houses")
    if phase["name"] in ("Full Moon", "New Moon"):
        terms.add(phase["name"])
    definitions = hc.definitions_for(terms)

    engine = f"the Swiss Ephemeris (pyswisseph {cs.swe.version}, Moshier)"
    day_label = day_start_local.strftime("%A, %B %-d, %Y")

    return {
        "day": day.isoformat(),
        "day_label": day_label,
        "timezone": view_name,
        "timed": bool(natal.get("timed")),
        "engine": engine,
        "energy": energy,
        "sky": hc.sky_summary(moon, positions, web),
        "arc": hc.arc_line(ctx),
        "phase": phase,
        "featured": featured,
        "sky_featured": sky_featured,
        "bridge": bridge,
        "ledger": timed,
        "background": background,
        "windows": windows,
        "close": close,
        "definitions": definitions,
        "moon": {"sign": moon.get("start_sign"),
                 "ingress_sign": moon.get("ingress_sign"),
                 "ingress_local": moon.get("ingress_local"),
                 "phase": phase["name"],
                 "house": positions["Moon"].get("whole_sign_house")},
        "wheel": wheel_data(natal_pts, positions, timed),
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
