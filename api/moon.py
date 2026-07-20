"""GET /api/moon?tz=America/Chicago — the Moon right now.
Sign, degree, phase, void-of-course status, next ingress, last/next aspect."""
import json
import sys
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402
import electional  # noqa: E402
import swisseph as swe  # noqa: E402


def build(tz_name):
    tz = ZoneInfo(tz_name)
    now = datetime.now(timezone.utc)
    jd = engines.cs.jd_ut(now)
    mlon, mspeed = engines.cs.body_lonspeed(jd, swe.MOON)
    slon = engines.cs.body_lonspeed(jd, swe.SUN)[0]
    sign, deg = engines.cs.sign_of(mlon)
    elong = (mlon - slon) % 360
    phase_names = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
                   "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    phase = phase_names[int(((elong + 22.5) % 360) // 45)]

    t0, t1 = now - timedelta(hours=30), now + timedelta(hours=60)
    ingresses = electional.moon_ingresses(t0, t1)
    perfections = electional.moon_perfections(t0, t1)
    vocs = electional.voc_intervals(t0, t1, ingresses, perfections)
    in_voc = any(v0 <= now < v1 for v0, v1 in vocs)
    nxt_ing = next(((dt, s) for dt, s in ingresses if dt > now), None)
    last_asp = next(((dt, p, a) for dt, p, a in reversed(perfections) if dt <= now), None)
    next_asp = next(((dt, p, a) for dt, p, a in perfections if dt > now), None)

    def loc(dt):
        return dt.astimezone(tz).strftime("%a %b %-d, %-I:%M %p")

    return {
        "moon": f"{sign} {int(deg)}°{int((deg % 1) * 60):02d}′",
        "sign": sign, "phase": phase,
        "illumination_deg": round(elong, 1),
        "void_of_course": in_voc,
        "voc_until": loc(next(v1 for v0, v1 in vocs if v0 <= now < v1)) if in_voc else None,
        "next_ingress": {"sign": engines.cs.SIGNS[nxt_ing[1]], "at": loc(nxt_ing[0])} if nxt_ing else None,
        "last_aspect": {"what": f"Moon {last_asp[2]} {last_asp[1]}", "at": loc(last_asp[0])} if last_asp else None,
        "next_aspect": {"what": f"Moon {next_asp[2]} {next_asp[1]}", "at": loc(next_asp[0])} if next_asp else None,
        "tz": tz_name,
        "method": "Swiss Ephemeris (Moshier), computed live",
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        tz_name = q.get("tz", ["America/Chicago"])[0]
        try:
            body = json.dumps(build(tz_name)).encode()
            code = 200
        except Exception as e:
            body = json.dumps({"error": str(e)[:200]}).encode()
            code = 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, max-age=60")
        self.end_headers()
        self.wfile.write(body)
