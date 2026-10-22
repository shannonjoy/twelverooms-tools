"""Tests for the 2026-10-21 index plan: unique Saturn year pages, the
best-dates overlap, FAQ and WebApplication schema, related links, the
sitemap, redirects and IndexNow.

Needs pyswisseph (the system python3 on Shannon's Mac has it):
    /usr/bin/python3 -m unittest discover -s tests -v
"""
import html
import json
import re
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "api"), str(ROOT / "tests")]
import overlap  # noqa: E402
import saturn  # noqa: E402

YEARS = range(1960, 2006)
CORE = ["natal-chart", "big-3-calculator", "saturn-return-calculator", "synastry", "moon",
        "daily-horoscope", "transit-timeline", "planetary-hours", "electional",
        "mercury-retrograde", "best-wedding-dates-2027", "the-twelve-houses"]
CALCULATORS = ["natal-chart", "big-3-calculator", "saturn-return-calculator", "synastry", "moon",
               "daily-horoscope", "transit-timeline", "planetary-hours", "electional"]
LD_RE = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
QA_RE = re.compile(r'<div class="qa"><h3>(.*?)</h3><p>(.*?)</p></div>', re.S)


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def ld_blocks(page):
    return [json.loads(m.group(1)) for m in LD_RE.finditer(page)]


def faq_of(page):
    faqs = [d for d in ld_blocks(page) if d.get("@type") == "FAQPage"]
    assert len(faqs) == 1, f"expected one FAQPage, found {len(faqs)}"
    return faqs[0]


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


class SaturnYearPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {y: saturn.render(y) for y in YEARS}

    def test_neighbouring_years_share_under_30_percent(self):
        vals = [overlap.overlap(self.pages[y], self.pages[y + 1]) for y in YEARS[:-1]]
        self.assertLess(max(vals), 0.30, f"worst neighbouring pair {max(vals):.0%}")
        self.assertLess(sum(vals) / len(vals), 0.25)

    def test_each_page_has_twelve_birth_months(self):
        for y, p in self.pages.items():
            rows = re.findall(r'<tr id="(january|february|march|april|may|june|july|august|'
                              r'september|october|november|december)">', p)
            self.assertEqual(len(rows), 12, y)

    def test_passes_match_the_report_engine(self):
        for y, m in [(1990, 1), (1975, 3), (1988, 12), (2003, 6)]:
            lon = saturn.sr.calc(saturn._noon(y, m, 15), saturn.SATURN)[0]
            mine = [saturn._short(j) for j, _ in saturn.first_return(lon, date(y, m, 15))]
            eng = saturn.sr.build_returns(lon, date(y, m, 15))[0]["passes"]
            want = [date.fromisoformat(e[:10]).strftime("%b %-d, %Y") for e in eng]
            self.assertEqual(mine, want, (y, m))

    def test_retrograde_dip_across_a_cusp_names_both_signs(self):
        # Saturn was in Taurus from June 9 to October 25, 1998.
        p = self.pages[1998]
        self.assertIn("into Taurus on June 9, 1998", p)
        self.assertIn("Aries or Taurus", p)
        self.assertNotIn("Every 1998 birthday has natal Saturn in Aries", p)
        self.assertIn("changed sign three times in 1988", self.pages[1988])

    def test_faq_schema_parses_and_matches_visible(self):
        for y, p in self.pages.items():
            faq = faq_of(p)
            self.assertGreaterEqual(len(faq["mainEntity"]), 3)
            schema = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq["mainEntity"]]
            visible = [(plain(q), plain(a)) for q, a in QA_RE.findall(p)]
            self.assertEqual(schema, visible, y)

    def test_canonical_and_no_noindex(self):
        for y, p in self.pages.items():
            self.assertIn(f'<link rel="canonical" href="https://thetwelverooms.com/saturn-return/{y}">', p)
            self.assertNotIn("noindex", p)


class BestDatesFamily(unittest.TestCase):
    def test_family_overlap_under_25_percent(self):
        pages = [read(f.name) for f in sorted(ROOT.glob("best-days-*-2027.html"))]
        mean, _ = overlap.family_overlap(pages)
        self.assertLess(mean, 0.25)

    def test_wedding_2028_differs_from_2027(self):
        self.assertLess(overlap.overlap(read("best-wedding-dates-2028.html"),
                                        read("best-wedding-dates-2027.html")), 0.35)

    def test_rows_name_their_own_election(self):
        s = read("best-days-to-sign-a-contract-2027.html")
        self.assertIn("For signing a contract: the Moon reaches", s)
        self.assertIn("Central time.", s)

    def test_every_best_dates_page_schema_parses(self):
        for f in sorted(ROOT.glob("best-*.html")):
            faq = faq_of(read(f.name))
            self.assertTrue(faq["mainEntity"], f.name)


class CorePages(unittest.TestCase):
    def test_faq_answers_40_to_70_words_and_match_visible(self):
        for slug in CORE:
            p = read(f"{slug}.html")
            faq = faq_of(p)
            self.assertGreaterEqual(len(faq["mainEntity"]), 3, slug)
            self.assertLessEqual(len(faq["mainEntity"]), 6, slug)
            for q in faq["mainEntity"]:
                n = len(q["acceptedAnswer"]["text"].split())
                self.assertTrue(40 <= n <= 70, f"{slug}: {q['name']} has {n} words")
            schema = [(plain(q["name"]), plain(q["acceptedAnswer"]["text"])) for q in faq["mainEntity"]]
            visible = [(plain(q), plain(a)) for q, a in QA_RE.findall(p)]
            self.assertEqual(schema, visible, slug)

    def test_answer_block_near_the_top(self):
        for slug in CORE:
            p = read(f"{slug}.html")
            h1 = p.index("<h1")
            box = p.find('<div class="highlight">')
            self.assertGreater(box, h1, slug)
            self.assertLess(box - h1, 2500, f"{slug}: answer is not near the top")

    def test_calculators_carry_webapplication(self):
        for slug in CALCULATORS:
            types = [d.get("@type") for d in ld_blocks(read(f"{slug}.html"))]
            self.assertIn("WebApplication", types, slug)

    def test_related_links(self):
        for slug in CORE:
            p = read(f"{slug}.html")
            block = re.search(r"aeo-related: start.*?aeo-related: end", p, re.S)
            self.assertIsNotNone(block, slug)
            links = re.findall(r'<a href="(/[^"]+)">([^<]+)</a>', block.group(0))
            self.assertTrue(3 <= len(links) <= 5, slug)
            for href, text in links:
                self.assertNotEqual(href, f"/{slug}")
                self.assertGreaterEqual(len(text.split()), 3, f"{slug}: anchor '{text}' is not descriptive")
                target = href.lstrip("/")
                if not target.startswith("saturn-return/"):
                    self.assertTrue((ROOT / f"{target}.html").exists(), href)

    def test_home_links_every_core_tool_in_the_body(self):
        body = re.split(r'<div id="site-footer"', re.sub(r"<script\b.*?</script>", "", read("index.html"), flags=re.S))[0]
        for slug in CORE:
            self.assertIn(f'href="/{slug}"', body, slug)

    def test_no_copy_promising_limits_on_collection(self):
        banned = ["nothing stored", "never stored", "nothing is stored", "no analytics",
                  "no tracking", "no cookies", "what we keep", "nothing else"]
        for slug in CORE + ["index"]:
            low = read(f"{slug}.html").lower()
            for b in banned:
                self.assertNotIn(b, low, f"{slug}: {b}")


class SitemapAndRouting(unittest.TestCase):
    def setUp(self):
        self.locs = re.findall(r"<loc>https://thetwelverooms.com([^<]*)</loc>", read("sitemap.xml"))

    def test_sitemap_contents(self):
        self.assertEqual(len(self.locs), 109)  # 102 + the 7 sky-calendar and embed pages (growth-features-1021)
        self.assertEqual(len(set(self.locs)), 109)
        years = [p for p in self.locs if p.startswith("/saturn-return/")]
        self.assertEqual(years, [f"/saturn-return/{y}" for y in YEARS])
        for slug in CORE:
            self.assertIn(f"/{slug}", self.locs)
        for p in self.locs:
            self.assertFalse(re.match(r"^/(moon|void-of-course-moon)/\d", p), p)
            self.assertFalse(re.match(r"^/sabian-symbols/[a-z]+-\d+$", p), p)
            if p == "/" or p.startswith("/saturn-return/"):
                continue
            self.assertTrue((ROOT / f"{p.lstrip('/')}.html").exists(), p)

    def test_redirects_unchanged_and_year_pages_served(self):
        cfg = json.loads(read("vercel.json"))
        self.assertEqual(len(cfg["redirects"]), 1)  # www -> apex only; no year page is redirected
        self.assertIn({"source": "/saturn-return/:year", "destination": "/api/saturn?year=:year"},
                      cfg["rewrites"])


class IndexNow(unittest.TestCase):
    def test_key_file_and_dry_run(self):
        keys = [f for f in ROOT.iterdir() if re.fullmatch(r"[0-9a-f]{32}\.txt", f.name)]
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0].read_text().strip() + ".txt", keys[0].name)
        out = subprocess.run(["node", str(ROOT / "bin" / "indexnow.mjs"), "--dry-run"],
                             capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("dry run: 109 URLs, nothing sent", out.stdout)


if __name__ == "__main__":
    unittest.main()
