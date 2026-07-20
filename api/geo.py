"""GET /api/geo?q=jefferson — offline city lookup for the birth-place field.
Returns [{name, admin1, country, lat, lon, tz}]. No network, nothing stored."""
import csv
import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CITIES_CSV = Path(__file__).parent / "_data" / "cities.csv"
_cities = None


def _load():
    global _cities
    if _cities is None:
        _cities = []
        with open(CITIES_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["lat"] = float(row["lat"])
                row["lon"] = float(row["lon"])
                row["_q"] = f"{row['name']}, {row['admin1']}".lower()
                _cities.append(row)
    return _cities


def search(q, limit=12):
    q = q.strip().lower()
    if len(q) < 2:
        return []
    prefix, substr = [], []
    for c in _load():
        if c["_q"].startswith(q):
            prefix.append(c)
        elif q in c["_q"]:
            substr.append(c)
        if len(prefix) >= limit:
            break
    out = (prefix + substr)[:limit]
    return [{k: c[k] for k in ("name", "admin1", "country", "lat", "lon", "tz")}
            for c in out]


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
        try:
            body = json.dumps({"results": search(q)}).encode()
            code = 200
        except Exception as e:
            body = json.dumps({"error": str(e)[:200]}).encode()
            code = 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(body)
