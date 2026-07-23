"""POST /api/windows — electional window finder (lite).
Body: {start, end, tz, lat, lon, intention}. Range capped at 21 days,
top 3 windows. Nothing stored. Recipes come from the shared engine
(electional.RECIPES); the public tool exposes a curated subset."""
import json
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import electional  # noqa: E402

# Curated public set (highest search intent + broad appeal). The full
# twenty live in the studio.
PUBLIC_KEYS = ["wedding", "engagement", "first_date", "conception",
               "business", "contract", "launch", "job", "investment",
               "home", "relocation"]

GET_META = {"public": [{"key": k, "label": electional.RECIPES_BY_KEY[k]["label"]}
                       for k in PUBLIC_KEYS if k in electional.RECIPES_BY_KEY]}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(GET_META).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            key = o.get("intention", "wedding")
            if key not in PUBLIC_KEYS:
                raise ValueError("unknown intention")
            recipe = electional.RECIPES_BY_KEY[key]
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
                "hard": [dict(r) for r in recipe["hard"]],
                "soft": [dict(r) for r in recipe["soft"]],
            }
            out = electional.scan(criteria, recipe_key=key)
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
