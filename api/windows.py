"""POST /api/windows — electional window finder (lite).
Body: {start, end, tz, lat, lon, intention}. Range capped at 21 days,
top 3 windows. Nothing stored."""
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import electional  # noqa: E402

PRESETS = {
    "launch": {
        "hard": [{"rule": "moon_not_voc"},
                 {"rule": "planet_not_retrograde", "planets": ["Mercury"]}],
        "soft": [
            {"rule": "moon_applying_aspect", "to": ["Jupiter", "Sun", "Venus"],
             "aspects": ["trine", "sextile", "conjunction"], "weight": 3},
            {"rule": "moon_avoid_aspect", "to": ["Mars", "Saturn"],
             "aspects": ["square", "opposition"], "weight": -3},
            {"rule": "moon_waxing", "weight": 1}]},
    "contract": {
        "hard": [{"rule": "moon_not_voc"},
                 {"rule": "planet_not_retrograde", "planets": ["Mercury"]}],
        "soft": [
            {"rule": "moon_applying_aspect", "to": ["Mercury", "Venus", "Jupiter"],
             "aspects": ["trine", "sextile", "conjunction"], "weight": 3},
            {"rule": "moon_avoid_aspect", "to": ["Mars", "Saturn"],
             "aspects": ["square", "opposition"], "weight": -3},
            {"rule": "moon_waxing", "weight": 1}]},
    "conversation": {
        "hard": [{"rule": "moon_not_voc"}],
        "soft": [
            {"rule": "moon_applying_aspect", "to": ["Venus", "Mercury", "Jupiter"],
             "aspects": ["trine", "sextile"], "weight": 3},
            {"rule": "moon_avoid_aspect", "to": ["Mars", "Saturn"],
             "aspects": ["square", "opposition", "conjunction"], "weight": -4}]},
}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            preset = PRESETS.get(o.get("intention", "launch"), PRESETS["launch"])
            from datetime import date
            start = date.fromisoformat(o["start"])
            end = date.fromisoformat(o["end"])
            if (end - start).days + 1 > 21:
                raise ValueError("range capped at 21 days for the free tool")
            criteria = {
                "range": {"start": o["start"], "end": o["end"]},
                "hours": {"earliest": "08:00", "latest": "21:00"},
                "location": {"lat": float(o["lat"]), "lon": float(o["lon"]),
                             "tz": o["tz"]},
                "top_n": 3, "step_minutes": 15,
                "hard": preset["hard"], "soft": preset["soft"],
            }
            out = electional.scan(criteria)
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
