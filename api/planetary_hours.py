"""POST /api/planetary-hours — today's (or a given date's) 12 day hours
and 12 night hours, ruled by the Chaldean order, for one city. Nothing
stored. Body: {lat, lon, tz, date?}. date defaults to today in tz."""
import json
import sys
from datetime import date as date_cls, datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import electional  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            tz = ZoneInfo(o["tz"])
            lat, lon = float(o["lat"]), float(o["lon"])
            d = date_cls.fromisoformat(o["date"]) if o.get("date") else datetime.now(tz).date()
            start_local = datetime(d.year, d.month, d.day, tzinfo=tz)
            table = electional.planetary_hours_range(start_local, 1, tz, lat, lon)
            day = table[d.isoformat()]
            now = datetime.now(tz)
            hours = [{"ruler": r, "from": t0.astimezone(tz).strftime("%-I:%M %p"),
                      "to": t1.astimezone(tz).strftime("%-I:%M %p"),
                      "current": t0 <= now < t1 and d == now.date()}
                     for t0, t1, r in day["hours"]]
            out = {"date": d.isoformat(), "date_pretty": d.strftime("%A, %B %-d, %Y"),
                   "day_ruler": day["day_ruler"], "hours": hours}
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
