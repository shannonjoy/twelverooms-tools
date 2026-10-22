"""Tests for 2026-10-22 (site-creator/wedding-solar-1022): the 2027 wedding
dates come from the engine, the solar return calculator, the date-neutral
Mercury answer, the function count and the sitemap.

Needs pyswisseph (the system python3 on Shannon's Mac has it):
    /usr/bin/python3 -m unittest discover -s tests -v
"""
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "api" / "_engines"), str(ROOT / "bin")]
import compute_factsheet as cf  # noqa: E402
import solar_return_calc as src  # noqa: E402
import swisseph as swe  # noqa: E402

ROW_RE = re.compile(r'<tr id="([a-z]+)"><td><strong>\w+</strong></td><td>([^<]+)</td>'
                    r'<td><span class="tag gold"[^>]*>[★☆]+ ([A-Za-z ]+)</span>')
# A made-up test chart (not a customer): Chicago, July 15, 1990, 2:30 PM.
CHART = {"date": "1990-07-15", "time": "14:30", "tz": "America/Chicago",
         "lat": 41.8781, "lon": -87.6298}


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class WeddingDates2027(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import compute_electional_rows as cer
        cls.rows = cer.compute("best-wedding-dates-2027", "wedding", 2027)["rows"]
        cls.page = read("best-wedding-dates-2027.html")

    def test_page_rows_equal_engine_output(self):
        published = [(m, d, lab) for m, d, lab in ROW_RE.findall(self.page)]
        engine = [(r["month"].lower(), r["day"], r["label"]) for r in self.rows]
        self.assertEqual(published, engine)

    def test_april_is_the_13th(self):
        april = next(r for r in self.rows if r["month"] == "April")
        self.assertEqual(april["date"], "2027-04-13")
        self.assertIn("Tue, Apr 13", self.page)

    def test_no_copy_repeats_the_old_rows(self):
        for rel in ("best-wedding-dates-2027.html", "llms.txt"):
            text = read(rel)
            for old in ("April 8", "Apr 8", "August 31", "Aug 31"):
                self.assertNotIn(old, text, f"{rel}: {old}")

    def test_strongest_days_are_repeated_correctly(self):
        top = max(r["stars"] for r in self.rows)
        best = [date.fromisoformat(r["date"]).strftime("%B %-d") for r in self.rows if r["stars"] == top]
        joined = ", ".join(best[:-1]) + ", and " + best[-1]
        self.assertIn(joined, self.page)  # the answer block and FAQ
        llms = next(l for l in read("llms.txt").splitlines() if "wedding dates of 2027" in l)
        for d in best:
            self.assertIn(d, llms)

    def test_faq_schema_matches_visible(self):
        ld = next(json.loads(m) for m in re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>', self.page, re.S)
            if '"FAQPage"' in m)
        visible = re.findall(r'<div class="qa"><h3>(.*?)</h3><p>(.*?)</p></div>', self.page, re.S)
        self.assertEqual([q["name"] for q in ld["mainEntity"]], [q for q, _ in visible])
        self.assertEqual(ld["mainEntity"][0]["acceptedAnswer"]["text"], visible[0][1])


class SolarReturn(unittest.TestCase):
    def compute(self, **kw):
        with redirect_stderr(io.StringIO()):
            return src.compute({**CHART, "year": 2027, **kw})

    def test_return_lands_on_the_birthday_and_the_natal_degree(self):
        d = self.compute()
        moment = datetime.fromisoformat(d["moment_utc"])
        self.assertLessEqual(abs((moment.date() - date(2027, 7, 15)).days), 1)
        self.assertLess(d["sun_check_arcsec"], 1.0)
        jd = swe.julday(moment.year, moment.month, moment.day,
                        moment.hour + moment.minute / 60 + moment.second / 3600)
        with redirect_stderr(io.StringIO()):
            natal_sun = cf.build_natal({**CHART, "name": "t"})[0]["planets"]["Sun"]["lon"]
        self.assertLess(abs(cf.angdiff(cf.calc(jd, swe.SUN)[0], natal_sun)) * 3600, 60)

    def test_every_year_in_range_finds_its_return(self):
        for y in (1991, 2000, 2026, 2030, 2050):
            d = self.compute(year=y)
            self.assertLessEqual(abs((datetime.fromisoformat(d["moment_utc"]).date()
                                      - date(y, 7, 15)).days), 1, y)

    def test_leap_day_birth(self):
        with redirect_stderr(io.StringIO()):
            d = src.compute({**CHART, "date": "1992-02-29", "year": 2027})
        m = datetime.fromisoformat(d["moment_utc"]).date()
        self.assertIn(m, (date(2027, 2, 28), date(2027, 3, 1)))

    def test_matches_the_reading_engine(self):
        """The canonical engine's CLI (api/_engines/solar_return.py, the Solar
        Return Reading's own) casts the same chart to the second."""
        with redirect_stderr(io.StringIO()):
            natal = cf.build_natal({**CHART, "name": "t"})[0]
        fs = {"order": {**CHART, "name": "t"}, "natal": natal}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(fs, fh)
        res = subprocess.run([sys.executable, str(ROOT / "api" / "_engines" / "solar_return.py"),
                              "--natal", fh.name, "--year", "2027", "--lat", str(CHART["lat"]),
                              "--lon", str(CHART["lon"]), "--tz", CHART["tz"]],
                             capture_output=True, text=True, cwd=ROOT / "api" / "_engines")
        self.assertEqual(res.returncode, 0, res.stderr[-500:])
        ref = json.loads(res.stdout)["natal"]
        d = self.compute()
        self.assertEqual(d["moment_utc"], ref["moment_utc"])
        self.assertEqual(d["asc"]["position"], ref["asc"]["pretty"])
        self.assertEqual(d["mc"]["position"], ref["mc"]["pretty"])
        self.assertEqual(d["chart_ruler"]["planet"], ref["chart_ruler"]["planet"])
        for row in d["planets"]:
            self.assertEqual(row["position"], ref["planets"][row["body"]]["pretty"], row["body"])
            self.assertEqual(row["house"], ref["planets"][row["body"]]["house"], row["body"])
        self.assertEqual(d["sr_asc_in_natal_house"], ref["overlays"]["sr_asc_in_natal_house"])

    def test_untimed_gives_a_window_and_no_houses(self):
        with redirect_stderr(io.StringIO()):
            d = src.compute({**CHART, "time": None, "year": 2027})
        self.assertFalse(d["timed"])
        self.assertNotIn("asc", d)
        self.assertTrue(all("house" not in p for p in d["planets"]))
        lo = datetime.fromisoformat(d["window_local"]["from"])
        hi = datetime.fromisoformat(d["window_local"]["to"])
        self.assertTrue(20 <= (hi - lo).total_seconds() / 3600 <= 26)

    def test_relocated_return_keeps_the_moment(self):
        here = self.compute()
        away = self.compute(where={"lat": 39.7392, "lon": -104.9903, "tz": "America/Denver",
                                   "place": "Denver, Colorado"})
        self.assertEqual(here["moment_utc"], away["moment_utc"])
        self.assertFalse(away["location"]["birthplace"])

    def test_api_mode_on_the_natal_function(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("natal_api", ROOT / "api" / "natal.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        class Fake(mod.handler):
            def __init__(self, body):
                self.headers = {"Content-Length": str(len(body))}
                self.rfile = io.BytesIO(body)
                self.wfile = io.BytesIO()
                self.sent = []

            def send_response(self, code):
                self.sent.append(code)

            def send_header(self, *a):
                pass

            def end_headers(self):
                pass

        h = Fake(json.dumps({**CHART, "mode": "solar_return", "year": 2027}).encode())
        with redirect_stderr(io.StringIO()):
            h.do_POST()
        self.assertEqual(h.sent, [200])
        out = json.loads(h.wfile.getvalue())
        self.assertIn("moment_utc", out)
        self.assertTrue(out["wheel_svg"].lstrip().startswith("<svg"))


class NoBirthDataInUrls(unittest.TestCase):
    def test_page_posts_birth_data_and_tracks_the_tool_name_only(self):
        page = read("solar-return-calculator.html")
        script = page.split('<script src="/tools.js"></script>', 1)[1]
        fetches = re.findall(r'fetch\(([^,)]+)', script)
        self.assertEqual(fetches, ['"/api/natal"'])
        self.assertIn('method: "POST"', script)
        for bad in ("location.search", "location.hash", "pushState", "replaceState",
                    "URLSearchParams", "?date=", "&date=", "encodeURIComponent"):
            self.assertNotIn(bad, script, bad)
        self.assertEqual(re.findall(r'TR\.trackToolUse\(([^)]*)\)', script), ['"solar-return"'])
        self.assertNotIn("gtag(", script)
        self.assertNotIn("clarity(", script)

    def test_no_new_rewrite_carries_birth_data(self):
        cfg = json.loads(read("vercel.json"))
        for r in cfg["rewrites"]:  # /moon/:date is a sky date, not a birth date
            self.assertNotIn("/api/natal", r["destination"], r)
            self.assertNotRegex(r["destination"], r"time=|lat=|lon=|tz=", r)


class Deploy(unittest.TestCase):
    def test_python_function_count_within_hobby_limit(self):
        funcs = sorted(p.name for p in (ROOT / "api").glob("*.py") if not p.name.startswith("_"))
        self.assertLessEqual(len(funcs), 12, funcs)

    def test_sitemap_lists_the_solar_return_calculator(self):
        sm = read("sitemap.xml")
        self.assertIn("<loc>https://thetwelverooms.com/solar-return-calculator</loc>", sm)

    def test_llms_and_nav_name_the_calculator(self):
        self.assertIn("https://thetwelverooms.com/solar-return-calculator", read("llms.txt"))
        self.assertIn('["/solar-return-calculator", "Solar return"]', read("tools.js"))

    def test_page_schema_and_etsy_link(self):
        page = read("solar-return-calculator.html")
        types = [json.loads(m)["@type"] for m in re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S)]
        self.assertEqual(sorted(types), ["FAQPage", "WebApplication"])
        ids = json.loads(Path.home().joinpath("orchestrator", "ids.json").read_text())
        listing = ids["ventures"]["listing-solar-return"]
        self.assertIn(f"https://www.etsy.com/listing/{listing}?utm_source=thetwelverooms"
                      f"&amp;utm_medium=referral&amp;utm_campaign=solar-return-calculator", page)
        self.assertIn('<link rel="canonical" href="https://thetwelverooms.com/solar-return-calculator">', page)


class MercuryStaticAnswer(unittest.TestCase):
    def test_static_answer_is_a_schedule_not_a_dated_verdict(self):
        page = read("is-mercury-retrograde.html")
        box = re.search(r'<div class="answer".*?</div>\s*</div>|<div class="answer".*?<p class="asof">.*?</p>',
                        page, re.S).group(0)
        verdict = re.search(r'<div class="verdict">(.*?)</div>', box).group(1)
        self.assertNotIn(verdict, ("Yes", "No", "Not yet"))
        self.assertIn("Oct 24 to Nov 13", verdict)
        for stale in ("pre-shadow. It stations", "As of ", "next stations retrograde"):
            self.assertNotIn(stale, page, stale)
        self.assertIn("2:13 AM CDT", box)
        self.assertIn("20&deg;59&prime; Scorpio", box)
        self.assertNotIn('class="now"', page)


if __name__ == "__main__":
    unittest.main()
