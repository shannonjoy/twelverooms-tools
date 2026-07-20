"""POST /api/synastry — cross-aspect grid for two birth data sets.
Body: {a: {date,time?,tz,lat,lon,name?}, b: {...}}. Processed in memory,
never stored or logged."""
import importlib.util
import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Load the engine by explicit path so this file's own name (synastry) can
# never shadow the _engines/synastry.py module in Vercel's runtime.
_ENG = Path(__file__).parent / "_engines"
sys.path.insert(0, str(_ENG))
_spec = importlib.util.spec_from_file_location("syn_engine", _ENG / "synastry.py")
syn_engine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(syn_engine)


def _order(o, fallback):
    return {"name": str(o.get("name") or fallback)[:60], "date": o["date"],
            "time": o.get("time") or None, "tz": o["tz"],
            "lat": float(o["lat"]), "lon": float(o["lon"])}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body_in = json.loads(self.rfile.read(length))
            a = _order(body_in["a"], "Person A")
            b = _order(body_in["b"], "Person B")
            out = syn_engine.compare(a, b, a["name"], b["name"])
            out["aspects"] = [x for x in out["aspects"] if x["tight"]][:16]
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
