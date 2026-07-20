# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/ventures/astrology-storefront/factsheet/saturn_return.py
# Re-sync with bin/sync-engines.sh
#!/usr/bin/env python3
"""
saturn_return.py — the 29.5-year cycle from a natal fact sheet.

Finds every Saturn return (transiting Saturn exactly conjunct natal
Saturn) from birth through the NEXT return, with all exact passes
(direct and retrograde) refined to the minute, the retrograde/direct
stations inside each return, the window(s) when Saturn occupies the
natal Saturn sign, and which return each event is (first, second,
third). Plus the natal Saturn's full condition. Feeds the Saturn Return
Report product and the free /saturn-return-calculator webtool (import
find_returns / sign_windows / stations_between from here; keep this
module the single source of the math).

Usage: python3 saturn_return.py shannon.json [--md] > satr.json
"""
import swisseph as swe
import json, argparse, sys
from datetime import datetime, date, timedelta, timezone

from compute_factsheet import (angdiff, jd_ut, calc, fmt_deg, sign_of, SIGNS)

ORDINAL = {1: "first", 2: "second", 3: "third", 4: "fourth"}


def _noon_jd(d):
    return jd_ut(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))


def _jd_to_utc(jd):
    y, m, dd, ut = swe.revjul(jd, swe.GREG_CAL)
    hh = int(ut); mm = (ut - hh) * 60; ss = round((mm % 1) * 60)
    mm = int(mm)
    if ss == 60:
        ss, mm = 0, mm + 1
    if mm == 60:
        mm, hh = 0, hh + 1
    return datetime(y, m, dd, hh, mm, ss, tzinfo=timezone.utc)


def _bisect(jd_lo, jd_hi, f, iters=42):
    """Root of f (sign change guaranteed between endpoints). Bisection,
    not Newton: passes near stations have speeds close to zero, where
    Newton misbehaves and bisection does not."""
    f_lo = f(jd_lo)
    for _ in range(iters):
        mid = (jd_lo + jd_hi) / 2
        f_mid = f(mid)
        if (f_lo < 0) == (f_mid < 0):
            jd_lo, f_lo = mid, f_mid
        else:
            jd_hi = mid
    return (jd_lo + jd_hi) / 2


def find_returns(natal_lon, born, horizon_years=34, body=swe.SATURN):
    """Every return event from birth to today + horizon_years. Daily scan
    for conjunction crossings, each refined to the minute, clustered into
    events (1 or 3 passes each; 2 can occur when a station sits almost
    exactly on the natal degree)."""
    # Start the scan 5 years after birth: in the first months of life the
    # transiting planet can retrograde back across its own natal degree,
    # and that infancy wobble is not a return. The first real Saturn
    # return cannot land before ~age 27.
    end = date.today() + timedelta(days=int(horizon_years * 365.25))
    skip = int(5 * 365.25)
    days = (end - born).days
    crossings = []
    prev_jd, prev_delta = None, None
    for i in range(skip, days + 1):
        d = born + timedelta(days=i)
        jd = _noon_jd(d)
        lon, _ = calc(jd, body)
        delta = angdiff(lon, natal_lon)
        if (prev_delta is not None and (prev_delta < 0) != (delta < 0)
                and abs(delta) < 1 and abs(prev_delta) < 1):
            exact = _bisect(prev_jd, jd, lambda j: angdiff(calc(j, body)[0], natal_lon))
            crossings.append(exact)
        prev_jd, prev_delta = jd, delta

    events = []
    for jd in crossings:
        if events and (jd - events[-1][-1]) < 500:
            events[-1].append(jd)
        else:
            events.append([jd])
    return events


def stations_between(jd_lo, jd_hi, body=swe.SATURN):
    """Retrograde and direct stations (speed zero-crossings), refined to
    the minute, between two julian days."""
    out = []
    step = 1.0
    prev_jd, prev_speed = None, None
    jd = jd_lo
    while jd <= jd_hi:
        speed = calc(jd, body)[1]
        if prev_speed is not None and (prev_speed < 0) != (speed < 0):
            exact = _bisect(prev_jd, jd, lambda j: calc(j, body)[1])
            out.append({"utc": _jd_to_utc(exact).isoformat(),
                        "type": "stations retrograde" if prev_speed > 0 else "stations direct"})
        prev_jd, prev_speed = jd, speed
        jd += step
    return out


def sign_windows(natal_lon, passes_jd, body=swe.SATURN):
    """Continuous interval(s) when the transiting body occupies the natal
    sign, covering all passes of one return event (retrograde can dip it
    out of the sign and back; each stay is reported)."""
    target = sign_of(natal_lon)[0]
    lo, hi = passes_jd[0] - 3 * 365.25, passes_jd[-1] + 3 * 365.25
    intervals, start = [], None
    jd = lo
    while jd <= hi:
        in_sign = sign_of(calc(jd, body)[0])[0] == target
        if in_sign and start is None:
            start = jd
        if not in_sign and start is not None:
            intervals.append((start, jd - 1))
            start = None
        jd += 1
    if start is not None:
        intervals.append((start, hi))
    keep = [iv for iv in intervals if any(iv[0] - 2 <= p <= iv[1] + 2 for p in passes_jd)]
    return [{"from": _jd_to_utc(a).date().isoformat(),
             "to": _jd_to_utc(b).date().isoformat()} for a, b in keep]


def sect_role_line(sect):
    """Human sentence for Saturn's sect standing. `sect` is the natal sect
    dict (may be empty when birth time is unknown)."""
    if not sect:
        return ("sect unknown without a birth time (day births carry Saturn "
                "more easily than night births; add a time for this reading)")
    if sect.get("malefic_contrary_to_sect") == "Saturn":
        return ("malefic contrary to sect (night birth: Saturn is the "
                "chart's harder taskmaster; the return asks more and pays more)")
    return ("malefic of sect (day birth: Saturn's hand is steadier "
            "here; the return runs closer to plain honest work)")


def build_returns(natal_lon, born, sect=None):
    """The reusable core: every Saturn return event for a natal Saturn
    longitude and birth date, fully formatted. Shared by the CLI and the
    web /api/saturn endpoint so the math lives in exactly one place.
    `sect` is the natal sect dict when known, else None."""
    events = find_returns(natal_lon, born)
    today = date.today()
    returns = []
    for n, ev in enumerate(events, start=1):
        first, last = _jd_to_utc(ev[0]), _jd_to_utc(ev[-1])
        age = first.year - born.year - ((first.month, first.day) < (born.month, born.day))
        if last.date() < today:
            status = "past"
        elif first.date() <= today:
            status = "underway"
        else:
            status = "next"
        returns.append({
            "return_number": n,
            "return_name": f"{ORDINAL.get(n, str(n) + 'th')} Saturn return",
            "age_at_first_pass": age,
            "status": status,
            "passes": [_jd_to_utc(j).isoformat() for j in ev],
            "pass_count": len(ev),
            "stations_within": stations_between(ev[0] - 30, ev[-1] + 30) if len(ev) > 1 else [],
            "sign_window": sign_windows(natal_lon, ev),
        })
    return returns


METHOD = ("Return passes found by daily scan for exact conjunction to the "
          "natal Saturn longitude, each pass refined to the minute by "
          "bisection, Swiss Ephemeris. Stations are speed zero-crossings, "
          "minute precision. Sign windows are the transiting Saturn's "
          "stay(s) in the natal Saturn sign covering the passes.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("natal"); ap.add_argument("--md", action="store_true")
    a = ap.parse_args()
    fs = json.load(open(a.natal))
    natal = fs["natal"]
    order = fs["order"]
    sat = natal["planets"]["Saturn"]
    slon = sat["lon"]
    born = date.fromisoformat(order["date"])

    sect = natal.get("sect", {})
    returns = build_returns(slon, born, sect)
    sect_role = sect_role_line(sect)
    s_aspects = [x for x in natal["aspects"] if "Saturn" in (x["a"], x["b"])]

    out = {"order": {"name": order["name"], "date": order["date"]},
           "natal_saturn": {**sat, "sect_role": sect_role,
                            "aspects": sorted(s_aspects, key=lambda x: x["orb"])[:6]},
           "returns": returns,
           "method": METHOD}
    print(json.dumps(out, indent=1))

    if a.md:
        L = [f"# Saturn Returns: {order['name']} (natal Saturn {sat['pretty']}, house {sat.get('house')})",
             f"Sect: {sect_role}"]
        for r in returns:
            L.append(f"- {r['return_name']}, age {r['age_at_first_pass']} [{r['status']}]: "
                     + ", ".join(p[:16].replace("T", " ") + " UTC" for p in r["passes"]))
            for st in r["stations_within"]:
                L.append(f"    {st['type']}: {st['utc'][:16].replace('T', ' ')} UTC")
            for w in r["sign_window"]:
                L.append(f"    in natal sign: {w['from']} to {w['to']}")
        sys.stderr.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
