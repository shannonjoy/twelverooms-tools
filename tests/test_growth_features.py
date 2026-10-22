"""Tests for the sky calendar pages, the calendar feed, the Moon widget and
the Big 3 share page (branch site-creator/growth-features-1021).

Run from the repo root with a Python that has pyswisseph:
    python3 -m unittest discover -s tests -v
"""
import json
import re
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))
sys.path.insert(0, str(ROOT / "api"))
sys.path.insert(0, str(ROOT / "api" / "_seo"))

import sky_calendar as skc  # noqa: E402
import swisseph as swe  # noqa: E402

DATA = json.loads((ROOT / "bin" / "sky_data" / "sky.json").read_text(encoding="utf-8"))
NEW_PAGES = ["is-mercury-retrograde", "retrogrades-2027", "eclipses-2027", "full-moon-calendar",
             "new-moon-calendar", "astrology-calendar", "embed"]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class ComputedDatesMatchTheEngine(unittest.TestCase):
    """The committed data is what the engine computes, and the pages show it."""

    def test_mercury_2027_recomputes_identically(self):
        fresh = skc.retrogrades("Mercury", 2027, 2027)
        stored = [r for r in DATA["retrogrades"]["Mercury"]
                  if 2027 in (int(r["station_retrograde"]["utc"][:4]), int(r["station_direct"]["utc"][:4]))]
        self.assertEqual(len(fresh), 3)
        for a, b in zip(fresh, stored):
            for k in ("station_retrograde", "station_direct", "shadow_begins", "shadow_ends"):
                self.assertEqual(a[k]["utc"], b[k]["utc"], k)
            self.assertEqual(a["station_retrograde"]["label"], b["station_retrograde"]["label"])

    def test_mercury_speed_changes_sign_at_each_station(self):
        for r in DATA["retrogrades"]["Mercury"]:
            for k, before_sign in (("station_retrograde", 1), ("station_direct", -1)):
                t = datetime.strptime(r[k]["utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
                jd = skc.jd_of(t)
                self.assertEqual(skc.speed(jd - 0.02, "Mercury") > 0, before_sign > 0, (k, r[k]["utc"]))
                self.assertEqual(skc.speed(jd + 0.02, "Mercury") > 0, before_sign < 0, (k, r[k]["utc"]))

    def test_lunations_are_true_conjunctions_and_oppositions(self):
        for x in DATA["lunations"]:
            target = 0.0 if x["kind"] == "new" else 180.0
            self.assertLess(abs(skc.signed(skc.elong(x["jd"]), target)), 0.01, x["utc"])
            self.assertEqual(skc.pos(skc.lon(x["jd"], "Moon"))["sign"], x["sign"])

    def test_eclipses_recompute(self):
        for x in DATA["eclipses"]:
            fn = swe.sol_eclipse_when_glob if x["kind"] == "solar" else swe.lun_eclipse_when
            _, tret = fn(x["jd"] - 5, swe.FLG_MOSEPH, 0)
            self.assertAlmostEqual(tret[0], x["jd"], places=5)
        y2027 = [(x["kind"], x["type"], x["central_date"]) for x in DATA["eclipses"] if x["central_date"][:4] == "2027"]
        self.assertIn(("solar", "total", "2027-08-02"), y2027)
        self.assertEqual(len(y2027), 5)

    def test_pages_show_the_computed_values(self):
        merc = read("is-mercury-retrograde.html")
        periods = json.loads(re.search(r'<script type="application/json" id="merc-periods">(.*?)</script>',
                                       merc).group(1))
        self.assertEqual(len(periods), len(DATA["retrogrades"]["Mercury"]))
        for p, r in zip(periods, DATA["retrogrades"]["Mercury"]):
            self.assertEqual(p["retrograde"][:16], r["station_retrograde"]["utc"][:16])
            self.assertEqual(p["shadow_ends"][:16], r["shadow_ends"]["utc"][:16])
        full = read("full-moon-calendar.html")
        new = read("new-moon-calendar.html")
        for x in DATA["lunations"]:
            if x["central_date"][:4] != "2027":
                continue
            label = f"{x['deg']}&deg;{x['min']:02d}&prime; {x['sign']}"
            self.assertIn(label, full if x["kind"] == "full" else new, x["utc"])
        ecl = read("eclipses-2027.html")
        for x in DATA["eclipses"]:
            if x["central_date"][:4] == "2027":
                self.assertIn(f"{x['deg']}&deg;{x['min']:02d}&prime; {x['sign']}", ecl)
        rx = read("retrogrades-2027.html")
        mars = DATA["retrogrades"]["Mars"][0]["station_retrograde"]
        self.assertIn(f"{mars['deg']}&deg;{mars['min']:02d}&prime; {mars['sign']}", rx)


class CalendarFeed(unittest.TestCase):
    def check_ics(self, rel):
        raw = (ROOT / rel).read_bytes()
        text = raw.decode("utf-8")
        self.assertTrue(text.startswith("BEGIN:VCALENDAR\r\n"), rel)
        self.assertTrue(text.endswith("END:VCALENDAR\r\n"), rel)
        self.assertNotIn("\n", text.replace("\r\n", ""), "bare LF line ending")
        for line in raw.split(b"\r\n"):
            self.assertLessEqual(len(line), 75, line[:40])
        unfolded = text.replace("\r\n ", "")
        self.assertIn("VERSION:2.0", unfolded)
        self.assertIn("PRODID:", unfolded)
        events = re.findall(r"BEGIN:VEVENT\r\n(.*?)END:VEVENT", unfolded, re.S)
        self.assertEqual(len(events), unfolded.count("BEGIN:VEVENT"))
        self.assertGreater(len(events), 20)
        uids = set()
        for ev in events:
            self.assertRegex(ev, r"(?m)^UID:\S+@thetwelverooms\.com\r$")
            self.assertRegex(ev, r"(?m)^DTSTAMP:\d{8}T\d{6}Z\r$")
            self.assertRegex(ev, r"(?m)^DTSTART(:\d{8}T\d{6}Z|;VALUE=DATE:\d{8})\r$")
            self.assertRegex(ev, r"(?m)^SUMMARY:.+\r$")
            uid = re.search(r"(?m)^UID:(\S+)\r$", ev).group(1)
            self.assertNotIn(uid, uids)
            uids.add(uid)
        return events

    def test_rolling_feed_validates(self):
        self.check_ics("calendar/twelve-rooms.ics")

    def test_year_feed_validates_and_holds_2027(self):
        events = self.check_ics("calendar/twelve-rooms-2027.ics")
        lunes = [x for x in DATA["lunations"] if x["central_date"][:4] == "2027"]
        moons = [e for e in events if "Moon in " in e and "eclipse in" not in e.split("SUMMARY:")[1].split("\r")[0][:9]]
        self.assertEqual(sum(1 for e in events if re.search(r"SUMMARY:(Full|New) Moon in", e)), len(lunes))
        self.assertTrue(any("SUMMARY:Total solar eclipse in Leo" in e for e in events))
        self.assertEqual(sum(1 for e in events if "SUMMARY:Mercury retrograde" in e), 3)
        self.assertTrue(moons)


class Big3Share(unittest.TestCase):
    def setUp(self):
        import big3
        self.big3 = big3

    def test_only_sign_names_parse(self):
        p = self.big3.parse
        self.assertEqual(p("leo-pisces-scorpio"), ("Leo", "Pisces", "Scorpio"))
        self.assertEqual(p("leo-pisces"), ("Leo", "Pisces", None))
        for bad in ("1990-08-10", "leo-pisces-1430", "leo-pisces-scorpio-chicago", "leo", "",
                    "leo-pisces-41.87", "leo-pisces-scorpio?date=1990-08-10", "../etc"):
            self.assertIsNone(p(bad), bad)

    def test_share_page_carries_no_birth_data(self):
        page = self.big3.render("Leo", "Pisces", "Scorpio")
        self.assertNotRegex(page, r"\b(19|20)\d\d-\d\d-\d\d\b")
        self.assertNotRegex(page, r"\blat(itude)?\b|\blon(gitude)?\b")
        url = re.search(r'og:url" content="([^"]+)"', page).group(1)
        self.assertEqual(url, "https://thetwelverooms.com/big-3/leo-pisces-scorpio")

    def test_client_link_builder_uses_sign_names_only(self):
        js = read("big3-share.js")
        script = js + """
const P = TRBig3.path;
const out = [P({sun:"Leo", moon:"Pisces", rising:"Scorpio"}), P({sun:"Leo", moon:"Pisces", rising:null}),
  P({sun:"Leo", moon:"Pisces", rising:"1990-08-10"}), P({sun:"1990-08-10", moon:"Pisces"}),
  P({sun:"Leo", moon:"Pisces", rising:"Scorpio", date:"1990-08-10", lat:41.8})];
console.log(JSON.stringify(out));"""
        stub = "globalThis.document={readyState:'complete',querySelectorAll:()=>[]};globalThis.window=globalThis;"
        try:
            r = subprocess.run(["node", "-e", stub + script], capture_output=True, text=True, timeout=20)
        except FileNotFoundError:
            self.skipTest("node not installed")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), ["/big-3/leo-pisces-scorpio", "/big-3/leo-pisces",
                                                "/big-3/leo-pisces", None, "/big-3/leo-pisces-scorpio"])

    def test_calculator_passes_only_the_three_signs(self):
        page = read("big-3-calculator.html")
        calls = re.findall(r"TRBig3\.offer\(([^;]*)\);", page)
        self.assertEqual(calls, ['out.querySelector(".card"), { sun, moon, rising }'])

    def test_share_page_is_noindex(self):
        page = self.big3.render("Aries", "Cancer", None)
        self.assertIn('<meta name="robots" content="noindex, follow">', page)
        self.assertNotIn('rel="canonical"', page)

        class Fake(self.big3.handler):
            def __init__(self, path):
                self.path, self.wfile, self.headers_out = path, BytesIO(), []
                self.request_version, self.requestline, self.command = "HTTP/1.1", "GET", "GET"

            def send_response(self, code, message=None):
                self.code = code

            def send_header(self, k, v):
                self.headers_out.append((k, v))

            def end_headers(self):
                pass

        for path, code in (("/api/big3?combo=aries-cancer-leo", 200), ("/api/big3?combo=1990-01-01", 404)):
            h = Fake(path)
            h.do_GET()
            self.assertEqual(h.code, code)
            self.assertIn(("X-Robots-Tag", "noindex, follow"), h.headers_out)

    def test_copy_matches_the_calculator(self):
        import big3_copy
        page = read("big-3-calculator.html")
        for name in ("SUN", "MOON", "RISING"):
            block = re.search(r"const %s = \{(.*?)\n\};" % name, page, re.S).group(1)
            js = dict(re.findall(r'(\w+): "((?:[^"\\]|\\.)*)"', block))
            self.assertEqual(js, getattr(big3_copy, name), name)


class IndexingAndPages(unittest.TestCase):
    def test_noindex_pages_stay_out_of_the_sitemap(self):
        sm = read("sitemap.xml")
        self.assertNotIn("/big-3/", sm)
        self.assertNotIn("/embed/moon-today", sm)
        self.assertIn('content="noindex, follow"', read("embed/moon-today.html"))
        for slug in NEW_PAGES:
            self.assertIn(f"<loc>https://thetwelverooms.com/{slug}</loc>", sm, slug)

    def test_vercel_routes(self):
        cfg = json.loads(read("vercel.json"))
        self.assertIn({"source": "/big-3/:combo", "destination": "/api/big3?combo=:combo"}, cfg["rewrites"])
        embed = next(h for h in cfg["headers"] if h["source"].startswith("/embed/"))
        self.assertIn({"key": "X-Robots-Tag", "value": "noindex, follow"}, embed["headers"])

    def test_new_pages_have_unique_titles_descriptions_and_schema(self):
        titles = {}
        for f in sorted(ROOT.glob("*.html")):
            t = re.search(r"<title>(.*?)</title>", f.read_text(encoding="utf-8"), re.S).group(1)
            titles.setdefault(t, []).append(f.name)
        for slug in NEW_PAGES:
            page = read(f"{slug}.html")
            title = re.search(r"<title>(.*?)</title>", page).group(1)
            self.assertLessEqual(len(title.replace("&#x27;", "'")), 60, title)
            self.assertEqual(titles[title], [f"{slug}.html"], title)
            desc = re.search(r'<meta name="description" content="([^"]+)"', page).group(1)
            self.assertGreater(len(desc), 70)
            self.assertIn(f'<link rel="canonical" href="https://thetwelverooms.com/{slug}">', page)
            self.assertNotIn("noindex", page)
            blocks = re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', page, re.S)
            types = {json.loads(b)["@type"] for b in blocks}
            self.assertIn("FAQPage", types, slug)
            self.assertIn('id="site-footer"><footer class="site">', page)

    def test_brand_banned_phrases(self):
        banned = ["for entertainment purposes", "reviewed by a human", "the universe has plans",
                  "no analytics", "no tracking", "no cookies", "what we keep", "nothing else"]
        files = [f"{s}.html" for s in NEW_PAGES] + ["embed/moon-today.html", "big3-share.js", "api/big3.py"]
        for f in files:
            text = read(f).lower()
            for b in banned:
                self.assertNotIn(b, text, (f, b))


if __name__ == "__main__":
    unittest.main()
