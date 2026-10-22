#!/usr/bin/env python3
"""Compute the month-by-month rows for the best-dates pages that still
showed a bare, unlabeled score, and write them to bin/electional_data/.

Search plan 2026-10-21, move 2. Six best-dates pages (wedding 2027, surgery,
lawsuit, party, travel, send-an-email) already carried the Twelve Rooms
Timing Scale. The other eighteen showed a "Score" column with no scale:
"5" in every row on two pages, 8 to 12 out of nothing on another, no column
at all on invest. This script reruns those eighteen through the same engine
and the same terms the scaled pages use, so every date and every rating on
the site comes from one method:

  - electional.scan_year (the studio engine synced into api/_engines),
    best window per calendar month, 07:00 to 21:00, 15-minute steps;
  - at the geographic center of the contiguous US (39.8333, -98.5855,
    America/Chicago), the location the Timing Scale was calibrated at;
  - rated against that election's own monthly-best distribution
    (electional.stars_for_score, population="monthly_best").

It checks the method first: the lawsuit page, built on the scale, must come
back date for date and rating for rating, or nothing is written.

Two pages may not share a date in the same month when the brief says they
give the same answer (business and invest picked the same day in six of
seven months). For those, the second page takes its own election's best
window on a different day, still computed, and the row says so.

Eclipses and Mercury retrograde stations are computed here too, with the
Swiss Ephemeris, so the per-row notes are never typed by hand.

Needs pyswisseph (the system python3 on Shannon's Mac has it). Run:
    /usr/bin/python3 bin/compute_electional_rows.py [slug ...]
then python3 bin/apply_electional_pages.py to write the pages.
"""
import calendar
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_engines"))
import electional as el  # noqa: E402
import swisseph as swe  # noqa: E402

OUT = ROOT / "bin" / "electional_data"
LOC = {"lat": 39.8333, "lon": -98.5855, "tz": "America/Chicago"}
HOURS = {"earliest": "07:00", "latest": "21:00"}

BUSINESS = "best-days-to-start-a-business-2027"
INVEST = "best-days-to-invest-2027"
LAUNCH = "best-days-to-launch-a-product-2027"
PROPOSE = "best-days-to-propose-2027"
# slug: (recipe key, year, pages it must not share a month's date with).
# job and business, and first_date and engagement, are the same recipe in
# the engine, so without this they publish identical tables.
PAGES = {
    BUSINESS: ("business", 2027, ()),
    INVEST: ("investment", 2027, (BUSINESS,)),
    "best-wedding-dates-2028": ("wedding", 2028, ()),
    "best-days-to-conceive-2027": ("conception", 2027, ()),
    "best-days-to-sign-a-contract-2027": ("contract", 2027, ()),
    "best-days-to-buy-a-house-2027": ("home", 2027, ()),
    LAUNCH: ("launch", 2027, (BUSINESS, INVEST)),
    "best-days-for-a-job-interview-2027": ("job", 2027, (BUSINESS, INVEST, LAUNCH)),
    PROPOSE: ("engagement", 2027, ()),
    "best-days-to-buy-a-car-2027": ("car", 2027, ()),
    "best-days-to-ask-for-a-raise-2027": ("raise", 2027, ()),
    "best-days-to-open-a-restaurant-2027": ("shop", 2027, ()),
    "best-days-to-publish-a-book-2027": ("publishing", 2027, ()),
    "best-days-to-move-to-a-new-city-2027": ("relocation", 2027, ()),
    "best-days-to-reconcile-2027": ("reconciliation", 2027, ()),
    "best-days-for-a-first-date-2027": ("first_date", 2027, (PROPOSE,)),
    "best-days-to-start-a-diet-2027": ("diet", 2027, ()),
    "best-days-to-cut-your-hair-2027": ("haircut", 2027, ()),
}
# The method check: a page already on the scale, and what it publishes.
CONTROL = ("best-days-to-file-a-lawsuit-2027", "lawsuit", 2027)


def month_windows(recipe, y, m, top_n):
    last = calendar.monthrange(y, m)[1]
    crit = {"range": {"start": f"{y:04d}-{m:02d}-01", "end": f"{y:04d}-{m:02d}-{last:02d}"},
            "location": LOC, "hours": HOURS, "step_minutes": 15, "top_n": top_n,
            "hard": [dict(x) for x in recipe["hard"]],
            "soft": [dict(x) for x in recipe["soft"]]}
    return el.scan(crit, recipe_key=recipe["key"], population="monthly_best")["windows"]


def row(w, month):
    d = date.fromisoformat(w["start"][:10])
    return {"month": month, "date": d.isoformat(), "day": d.strftime("%a, %b %-d"),
            "score": w["peak_score"], "stars": w["scale"]["stars"],
            "label": w["scale"]["label"], "room_name": w["scale"]["room_name"],
            "blurb": w["scale"]["blurb"], "why": el.explain(w),
            # Window and peak, local time at LOC (2026-10-21, index plan):
            # the one fact that differs between elections that share a day.
            "start": w["start"], "end": w["end"], "peak_at": w["peak_at"]}


def compute(slug, key, year, avoid=None):
    """avoid: {slug: rows} of pages this one must not repeat a date from."""
    recipe = el.RECIPES_BY_KEY[key]
    taken = {}
    for other_slug, rows_ in (avoid or {}).items():
        for r in rows_:
            if not r.get("none"):
                taken.setdefault(r["month"], {})[r["date"]] = other_slug
    rows = []
    for m in range(1, 13):
        month = calendar.month_name[m]
        used = taken.get(month, {})
        wins = month_windows(recipe, year, m, 12 if used else 1)
        if not wins:
            rows.append({"month": month, "none": True})
            continue
        best = wins[0]
        free = [w for w in wins if w["start"][:10] not in used]
        pick = free[0] if free else best
        r = row(pick, month)
        r["moved_from"] = None
        if pick is not best:
            b = date.fromisoformat(best["start"][:10])
            r["moved_from"] = {"date": b.isoformat(), "day": b.strftime("%B %-d"),
                               "page": used[best["start"][:10]], "stars": best["scale"]["stars"]}
        rows.append(r)
    return {"slug": slug, "recipe": key, "label": recipe["label"], "year": year,
            "significators": significators(recipe),
            "location": LOC, "hours": HOURS, "mercury_direct_rule": mercury_rule(recipe),
            "rows": rows}


def significators(recipe):
    """What this election's recipe looks for, so a page can say which of
    its own rules a window meets (2026-10-21, index plan)."""
    soft = {r["rule"]: r for r in recipe["soft"]}
    return {"applies": soft["moon_applying_aspect"]["to"],
            "hours": soft["planetary_hour_ruler"]["rulers"],
            "angular": (soft.get("benefic_on_angle") or {}).get("planets", [])}


def mercury_rule(recipe):
    """True when the election already refuses a retrograde Mercury."""
    return any(h["rule"] == "planet_not_retrograde" and "Mercury" in h.get("planets", [])
               for h in recipe["hard"])


# ---------- sky events, computed ----------

def _date_of(jd):
    y, m, d, _ = swe.revjul(jd, swe.GREG_CAL)
    return date(y, m, int(d))


def eclipses(year):
    out = []
    jd = swe.julday(year, 1, 1, 0)
    end = swe.julday(year + 1, 1, 1, 0)
    t = jd
    while True:
        res = swe.sol_eclipse_when_glob(t, swe.FLG_SWIEPH, 0)
        peak = res[1][0]
        if peak >= end:
            break
        out.append({"date": _date_of(peak).isoformat(), "kind": "solar"})
        t = peak + 20
    t = jd
    while True:
        res = swe.lun_eclipse_when(t, swe.FLG_SWIEPH, 0)
        peak = res[1][0]
        if peak >= end:
            break
        out.append({"date": _date_of(peak).isoformat(), "kind": "lunar"})
        t = peak + 20
    return sorted(out, key=lambda e: e["date"])


def mercury_retrogrades(year):
    """Station retrograde to station direct, for spans touching `year`."""
    out, start = [], None
    jd = swe.julday(year - 1, 12, 1, 0)
    end = swe.julday(year + 1, 1, 31, 0)
    speed = lambda j: swe.calc_ut(j, swe.MERCURY, swe.FLG_SWIEPH | swe.FLG_SPEED)[0][3]
    prev = speed(jd)
    def station(a, b):
        """Bisect the moment the speed changes sign, to the minute."""
        sa = speed(a)
        for _ in range(20):
            mid = (a + b) / 2
            if (speed(mid) >= 0) == (sa >= 0):
                a = mid
            else:
                b = mid
        return _date_of(b)
    while jd < end:
        nxt = jd + 0.25
        s = speed(nxt)
        if prev >= 0 > s:
            start = station(jd, nxt)
        elif prev < 0 <= s and start:
            stop = station(jd, nxt)
            if start.year == year or stop.year == year:
                out.append({"from": start.isoformat(), "to": stop.isoformat()})
            start = None
        prev, jd = s, nxt
    return out


def main():
    only = set(sys.argv[1:])
    OUT.mkdir(exist_ok=True)

    # Method check against a page already on the scale.
    slug, key, year = CONTROL
    html = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
    published = re.findall(r'<td>(\w{3}, \w{3} \d+)</td><td><span class="tag gold"[^>]*>[★☆]+ ([A-Za-z ]+)</span>', html)
    got = [(r["day"], r["label"]) for r in compute(slug, key, year)["rows"] if not r.get("none")]
    if got != published:
        raise SystemExit(f"method check failed: {slug} computes {got}, page shows {published}")
    print(f"method check: {slug} reproduced, 12 of 12 dates and ratings")

    sky = {}
    for y in sorted({y for _, y, _ in PAGES.values()}):
        sky[str(y)] = {"eclipses": eclipses(y), "mercury_retrograde": mercury_retrogrades(y)}
    (OUT / "sky.json").write_text(json.dumps(sky, indent=1) + "\n")
    print("sky events:", json.dumps(sky))

    done = {}
    for slug, (key, year, distinct) in PAGES.items():
        needed = {d for _, _, ds in PAGES.values() for d in ds}
        if only and slug not in only and slug not in needed:
            continue
        for d in distinct:
            if d not in done:
                done[d] = json.loads((OUT / f"{d}.json").read_text())
        data = compute(slug, key, year, {d: done[d]["rows"] for d in distinct})
        data["distinct_from"] = list(distinct)
        data["computed"] = datetime.now(timezone.utc).date().isoformat()
        done[slug] = data
        if only and slug not in only:
            continue
        (OUT / f"{slug}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
        print(slug, " ".join(f"{r['day'][5:]}:{r.get('stars', '-')}" for r in data["rows"] if not r.get("none")))


if __name__ == "__main__":
    main()
