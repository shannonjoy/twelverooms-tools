"""POST /api/transits — a personal transit timeline from birth data.
Body: {date, time?, tz, lat, lon}. Computes the natal chart, then the slow
planets' (Jupiter through Pluto) exact major aspects to the natal points
over the next 3 years, clusters retrograde multi-passes into single
windows, and tags each with a plain-language theme and a weight. Birth
data is processed in memory and never stored or logged. Shares the transit
math with the reading engine (compute_factsheet.upcoming_hits), so the free
tool and the paid year-ahead reading can never disagree."""
import json
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_engines"))
import engines  # noqa: E402

# What each transiting planet brings (honest, planning-framed, no doom).
BODY_THEME = {
    "Jupiter": "growth and opportunity",
    "Saturn": "structure, testing, and maturity",
    "Uranus": "awakening and change",
    "Neptune": "dreaming and dissolving",
    "Pluto": "deep transformation",
}
# The life area each natal point governs.
POINT_AREA = {
    "Sun": "your identity and vitality",
    "Moon": "your emotions, home, and inner life",
    "Mercury": "your mind, plans, and how you communicate",
    "Venus": "your relationships, values, and money",
    "Mars": "your drive and how you take action",
    "Jupiter": "your sense of meaning and where you expand",
    "Saturn": "your responsibilities and long-term foundations",
    "Uranus": "your individuality and need for freedom",
    "Neptune": "your imagination and spiritual life",
    "Pluto": "your deepest drives and what you transform",
    "North Node": "your growth direction and path forward",
    "South Node": "what you are ready to release",
    "ASC": "how you meet the world and show up",
    "MC": "your career, calling, and public role",
}
# How each aspect tends to feel.
ASPECT_VERB = {
    "conjunction": ("activates", "A new cycle begins; this theme comes to the foreground."),
    "sextile": ("opens a door for", "An opportunity that rewards you for taking the first step."),
    "trine": ("brings ease to", "Support and flow; the easiest weather for this area."),
    "square": ("challenges", "Productive friction; growth that comes through effort and choices."),
    "opposition": ("brings to a head in", "A culmination that asks for balance and perspective."),
}
HARD = {"conjunction", "square", "opposition"}
BIG_POINTS = {"Sun", "Moon", "ASC", "MC"}
POINT_PRETTY = {"ASC": "Ascendant", "MC": "Midheaven"}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _weight(tp, aspect, point, is_return):
    w = {"Pluto": 3, "Neptune": 3, "Uranus": 3, "Saturn": 2, "Jupiter": 1}.get(tp, 1)
    if aspect in HARD:
        w += 1
    if point in BIG_POINTS:
        w += 1
    if is_return:
        w += 2
    return w


def _tier(w):
    return "major" if w >= 4 else ("notable" if w >= 2 else "light")


def _headline(tp, aspect, point, is_return):
    pt = POINT_PRETTY.get(point, point)
    if is_return:
        return f"Your {tp} return"
    return f"{tp} {aspect} your {pt}"


def _meaning(tp, aspect, point, is_return):
    if is_return and tp == "Jupiter":
        return "A fresh twelve-year chapter of growth opens. A good season to plant something you want to see expand."
    if is_return and tp == "Saturn":
        return "The threshold into a more grounded, self-authored chapter. What is real is confirmed; what was scaffolding falls away."
    verb, tone = ASPECT_VERB[aspect]
    return f"{tp} {verb} {POINT_AREA.get(point, 'this part of your chart')}, bringing {BODY_THEME.get(tp, 'change')}. {tone}"


def cluster(hits):
    """Group a slow planet's retrograde multi-passes (same transiting body,
    aspect, and natal point within ~5 months) into one event with all its
    exact dates. upcoming_hits returns passes already sorted by date."""
    by_key = {}
    order = []
    for h in hits:
        key = (h["transiting"], h["aspect"], h["natal_point"])
        placed = False
        for ev in by_key.get(key, []):
            if (date.fromisoformat(h["date"]) - date.fromisoformat(ev["dates"][-1])).days <= 160:
                ev["dates"].append(h["date"])
                placed = True
                break
        if not placed:
            ev = {"transiting": h["transiting"], "aspect": h["aspect"],
                  "natal_point": h["natal_point"], "dates": [h["date"]]}
            by_key.setdefault(key, []).append(ev)
            order.append(ev)
    events = []
    for ev in order:
        tp, aspect, point = ev["transiting"], ev["aspect"], ev["natal_point"]
        is_return = (tp == point and aspect == "conjunction")
        w = _weight(tp, aspect, point, is_return)
        events.append({
            "transiting": tp, "aspect": aspect, "natal_point": point,
            "point_pretty": POINT_PRETTY.get(point, point),
            "dates": ev["dates"], "pass_count": len(ev["dates"]),
            "is_return": is_return, "tier": _tier(w), "weight": w,
            "headline": _headline(tp, aspect, point, is_return),
            "meaning": _meaning(tp, aspect, point, is_return),
        })
    events.sort(key=lambda e: e["dates"][0])
    return events


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            o = json.loads(self.rfile.read(length))
            years = min(max(int(o.get("years", 3)), 1), 5)
            order = {"name": "Your chart",
                     "date": o["date"], "time": o.get("time") or None,
                     "tz": o["tz"], "lat": float(o["lat"]), "lon": float(o["lon"]),
                     "place": str(o.get("place", ""))[:80]}
            natal = engines.cf.build_natal(order)[0]
            hits = engines.cf.upcoming_hits(natal, date.today(), months=years * 12)
            events = cluster(hits)
            planets = natal["planets"]
            big3 = {"sun": planets["Sun"]["pretty"], "moon": planets["Moon"]["pretty"],
                    "rising": natal.get("asc", {}).get("pretty")}
            out = {
                "timed": bool(order["time"]),
                "years": years,
                "big3": big3,
                "count": len(events),
                "events": events,
            }
            body, code = json.dumps(out).encode(), 200
        except Exception as e:
            body, code = json.dumps({"error": str(e)[:200]}).encode(), 400
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
