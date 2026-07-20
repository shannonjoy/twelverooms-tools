"""POST /api/natal — free natal chart wheel + positions.
Body: {date, time?, tz, lat, lon, name?}. Birth data is processed in memory
and never stored or logged."""
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            order = {"name": str(o.get("name") or "Your chart")[:60],
                     "date": o["date"], "time": o.get("time") or None,
                     "tz": o["tz"], "lat": float(o["lat"]), "lon": float(o["lon"]),
                     "place": str(o.get("place", ""))[:80]}
            natal = engines.cf.build_natal(order)[0]
            fs = {"order": order, "natal": natal}
            positions = []
            for p, e in natal["planets"].items():
                if e is None:
                    continue
                positions.append({"body": p, "position": e["pretty"],
                                  "house": e.get("house"),
                                  "retrograde": e.get("retrograde", False)})
            out = {
                "wheel_svg": engines.gen_wheel.build(fs),
                "timed": natal["timed"],
                "rising": natal["asc"]["pretty"] if natal.get("asc") else None,
                "mc": natal["mc"]["pretty"] if natal.get("mc") else None,
                "sect": natal["sect"]["sect"] if natal.get("sect") else None,
                "positions": positions,
                "tight_aspects": [
                    {"a": a["a"], "b": a["b"], "aspect": a["aspect"], "orb": a["orb"]}
                    for a in natal["aspects"] if a["tight"]][:12],
                "patterns": natal["patterns"],
                "method": "Swiss Ephemeris (Moshier), whole-sign houses",
            }
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
