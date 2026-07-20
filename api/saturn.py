"""POST /api/saturn — free Saturn return dates from birth data.
Body: {date, time?, tz, lat, lon}. Computes the natal Saturn longitude,
then every Saturn return (exact passes, stations, sign window, return
number). Birth data is processed in memory and never stored or logged.
Shares the exact-return math with the Saturn Return Report engine
(factsheet/saturn_return.py) via build_returns, so the free tool and the
paid product can never disagree."""
import json
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines            # noqa: E402
import saturn_return as sr  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            order = {"name": "Your chart",
                     "date": o["date"], "time": o.get("time") or None,
                     "tz": o["tz"], "lat": float(o["lat"]), "lon": float(o["lon"]),
                     "place": str(o.get("place", ""))[:80]}
            natal = engines.cf.build_natal(order)[0]
            sat = natal["planets"]["Saturn"]
            born = date.fromisoformat(order["date"])
            sect = natal.get("sect") or None

            returns = sr.build_returns(sat["lon"], born, sect)
            out = {
                "natal_saturn": {"pretty": sat["pretty"], "sign": sat.get("sign"),
                                 "house": sat.get("house"),
                                 "sect_role": sr.sect_role_line(sect or {})},
                "timed": bool(order["time"]),
                "returns": returns,
                "method": sr.METHOD,
            }
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
