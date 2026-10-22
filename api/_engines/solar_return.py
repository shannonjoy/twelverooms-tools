# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/ventures/astrology-storefront/factsheet/solar_return.py
# Re-sync with bin/sync-engines.sh
#!/usr/bin/env python3
"""
solar_return.py — cast a solar return chart from a natal fact sheet.

The solar return: the exact instant the transiting Sun comes back to its
natal longitude in a given year, charted for where the person is at that
moment. Output uses the same JSON shape as compute_factsheet.py's natal
block, so gen_wheel.py renders it directly, plus SR-specific derivations
(SR chart aspects, SR planets in SR houses, SR-to-natal overlays).

Usage:
  python3 solar_return.py --natal shannon.json --year 2026 \
      --lat 38.5767 --lon -92.1735 --tz America/Chicago [--md] > sr.json

Location = where the person is on their birthday that year (defaults are
NOT assumed; pass them). No network, deterministic, minute-exact.
"""
import swisseph as swe
import json, argparse, sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from compute_factsheet import (FLAGS, SIGNS, PLANETS, ASPECTS, MAJORS, BASE_ORB,
                               HOUSE_MEANING, RULER, sign_of, fmt_deg, angdiff,
                               jd_ut, calc, positions_at, whole_sign_house,
                               natal_aspects, dignity)

def find_return_jd(natal_sun_lon, year, birth_month, birth_day):
    """Newton-iterate to the instant the Sun hits natal_sun_lon near the
    birthday in `year`. Minute precision or better."""
    guess = datetime(year, birth_month, birth_day, 12, tzinfo=timezone.utc)
    jd = jd_ut(guess)
    for _ in range(30):
        lon, speed = calc(jd, swe.SUN)
        delta = angdiff(lon, natal_sun_lon)
        if abs(delta) < 1e-6:
            break
        jd -= delta / speed
    return jd

def jd_to_dt(jd):
    y, m, d, ut = swe.revjul(jd, swe.GREG_CAL)
    hh = int(ut); mm = (ut - hh) * 60; ss = (mm % 1) * 60
    return datetime(y, m, d, hh, int(mm), int(ss), tzinfo=timezone.utc)

# the seven that can own a sign, and therefore can end a chain
TRAD7 = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

def dispositor_chains(planets):
    """Trace every planet to what it ANSWERS TO, and find where the chart resolves.

    A planet is disposited by the traditional ruler of the sign it occupies.
    Follow that chain and it always ends one of three ways: a planet in its own
    sign (a terminal, which answers to nobody), a two-planet cycle (mutual
    reception), or a longer cycle (a loop with no exit). The set of terminals is
    the chart's real power structure: a chart with one dignified terminal is
    governed by a single authority, a chart with several is divided, and a chart
    with none resolves only into a loop.

    This is the most-skipped move in a return reading and usually the strongest.
    """
    sign_of_p = {p: planets[p]["sign"] for p in planets if planets.get(p)}
    traceable = [p for p in list(TRAD7) + ["Uranus", "Neptune", "Pluto"] if p in sign_of_p]

    def ruler_of(p):
        return RULER[sign_of_p[p]]

    chains, terminals, cycles = {}, {}, []
    for p in traceable:
        chain, seen, cur = [p], {p}, p
        entry = {"sign": sign_of_p[p]}
        while True:
            nxt = ruler_of(cur)
            if nxt == cur:                       # rules the sign it sits in
                entry.update(resolves_to=cur, resolution="own sign")
                terminals.setdefault(cur, []).append(p)
                break
            if nxt in seen:                      # closed cycle, no terminal
                cyc = chain[chain.index(nxt):]
                kind = "mutual reception" if len(cyc) == 2 else "loop"
                entry.update(resolves_to=None, resolution=kind, cycle=cyc)
                if sorted(cyc) not in [sorted(c["planets"]) for c in cycles]:
                    cycles.append({"kind": kind, "planets": cyc})
                break
            chain.append(nxt); seen.add(nxt); cur = nxt
        entry["chain"] = chain
        entry["steps"] = len(chain) - 1
        chains[p] = entry

    finals = []
    for t, fed_by in sorted(terminals.items(), key=lambda kv: -len(kv[1])):
        finals.append({"planet": t, "sign": sign_of_p[t],
                       "dignities": dignity(t, sign_of_p[t]),
                       "disposits": sorted(p for p in fed_by if p != t),
                       "count": len(fed_by)})
    return {"chains": chains, "final_dispositors": finals, "cycles": cycles,
            "terminal_count": len(finals),
            "note": ("Traditional rulerships. A chart resolving into few dignified "
                     "terminals is self-sufficient; one resolving into a loop is not.")}

def dignity_summary(planets):
    """Who is strong and who is struggling, at a glance, for the year's tone."""
    strong, weak, neutral = [], [], []
    for p in TRAD7:
        e = planets.get(p)
        if not e:
            continue
        d = e.get("dignities") or []
        row = {"planet": p, "sign": e["sign"], "house": e["house"], "dignities": d}
        if any(x in d for x in ("domicile", "exaltation")):
            strong.append(row)
        elif any(x in d for x in ("detriment", "fall")):
            weak.append(row)
        else:
            neutral.append(row)
    return {"dignified": strong, "debilitated": weak, "peregrine": neutral,
            "verdict": ("%d of the seven in dignity, %d debilitated"
                        % (len(strong), len(weak)))}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--natal", required=True, help="fact-sheet JSON from compute_factsheet.py")
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--tz", required=True)
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()

    fs = json.load(open(a.natal))
    natal = fs["natal"]
    order = fs["order"]
    natal_sun = natal["planets"]["Sun"]["lon"]
    by, bm, bd = (int(x) for x in order["date"].split("-"))

    jd = find_return_jd(natal_sun, a.year, bm, bd)
    moment_utc = jd_to_dt(jd)
    moment_local = moment_utc.astimezone(ZoneInfo(a.tz))

    pos = positions_at(jd)
    cusps, ascmc = swe.houses_ex(jd, a.lat, a.lon, b'W', swe.FLG_MOSEPH)
    asc, mc = ascmc[0] % 360, ascmc[1] % 360
    rising_idx = int(asc // 30)
    below = 0 <= (pos["Sun"]["lon"] - asc) % 360 < 180
    sect = "night" if below else "day"

    sr = {"timed": True,
          "moment_utc": moment_utc.isoformat(),
          "moment_local": moment_local.isoformat(),
          "location": {"lat": a.lat, "lon": a.lon, "tz": a.tz},
          "asc": {"lon": asc, "pretty": fmt_deg(asc), "sign": SIGNS[rising_idx]},
          "mc": {"lon": mc, "pretty": fmt_deg(mc), "sign": sign_of(mc)[0],
                 "house": whole_sign_house(mc, rising_idx)},
          "sect": {"sect": sect,
                   "light": "Sun" if sect == "day" else "Moon",
                   "benefic_of_sect": "Jupiter" if sect == "day" else "Venus",
                   "malefic_contrary_to_sect": "Mars" if sect == "day" else "Saturn"}}

    planets = {}
    for p in list(PLANETS) + ["North Node", "South Node", "Chiron"]:
        if pos.get(p) is None:
            planets[p] = None
            continue
        lon = pos[p]["lon"]
        e = {"lon": round(lon, 4), "pretty": fmt_deg(lon),
             "sign": sign_of(lon)[0], "degree": round(sign_of(lon)[1], 2),
             "retrograde": pos[p]["retrograde"],
             "house": whole_sign_house(lon, rising_idx),
             "house_meaning": HOUSE_MEANING[whole_sign_house(lon, rising_idx)]}
        if p in PLANETS:
            e["dignities"] = dignity(p, e["sign"])
        planets[p] = e
    sr["planets"] = planets
    sr["aspects"] = natal_aspects(pos)

    # SR angle ruler chain
    rs = SIGNS[rising_idx]
    sr["chart_ruler"] = {"planet": RULER[rs], "sign": planets[RULER[rs]]["sign"],
                         "house": planets[RULER[rs]]["house"]}

    # overlays: where SR points land in the NATAL whole-sign houses, and
    # tight SR-to-natal contacts (the year's activations)
    natal_rising_idx = SIGNS.index(natal["asc"]["sign"]) if natal.get("asc") else None
    overlays = {}
    if natal_rising_idx is not None:
        overlays["sr_asc_in_natal_house"] = whole_sign_house(asc, natal_rising_idx)
        overlays["sr_mc_in_natal_house"] = whole_sign_house(mc, natal_rising_idx)
        overlays["sr_planets_in_natal_houses"] = {
            p: whole_sign_house(planets[p]["lon"], natal_rising_idx)
            for p in PLANETS}
    cross = []
    natal_targets = {p: natal["planets"][p]["lon"] for p in PLANETS if natal["planets"].get(p)}
    if natal.get("asc"):
        natal_targets["natal ASC"] = natal["asc"]["lon"]
        natal_targets["natal MC"] = natal["mc"]["lon"]
    for sp in PLANETS:
        for tgt, tlon in natal_targets.items():
            for name, angle in ASPECTS.items():
                if name not in MAJORS:
                    continue
                orb = abs(abs(angdiff(planets[sp]["lon"], tlon)) - angle)
                if orb <= 2.5:
                    cross.append({"sr_planet": sp, "aspect": name,
                                  "natal_point": tgt.replace("natal ", "") if tgt.startswith("natal ") else tgt,
                                  "orb": round(orb, 2)})
    sr["overlays"] = overlays
    sr["cross_aspects_to_natal"] = sorted(cross, key=lambda x: x["orb"])

    # who answers to whom, and who is strong: the year's power structure
    sr["dispositors"] = dispositor_chains(planets)
    sr["dignity_summary"] = dignity_summary(planets)

    out = {"order": order, "solar_return_year": a.year, "natal": sr,
           "method": ("Solar return computed to the second (Sun's exact return to its natal "
                      "longitude), whole-sign houses at the stated location. Same engine and "
                      "orbs as the natal fact sheet; cross-aspects capped at 2.5 degrees. "
                      "Dispositor chains use traditional rulerships.")}
    print(json.dumps(out, indent=1))

    if a.md:
        L = [f"# Solar Return {a.year}: {order['name']}",
             f"Return moment: {moment_local.strftime('%B %d, %Y at %I:%M:%S %p %Z')} ({a.tz})",
             f"SR rising {sr['asc']['pretty']} · SR MC {sr['mc']['pretty']} · {sect.upper()} chart",
             f"SR chart ruler: {sr['chart_ruler']['planet']} in {sr['chart_ruler']['sign']} (SR house {sr['chart_ruler']['house']})",
             "", "## SR planets"]
        for p in PLANETS:
            e = planets[p]
            L.append(f"- {p}: {e['pretty']} · SR house {e['house']} ({e['house_meaning']})"
                     + (" Rx" if e["retrograde"] else ""))
        if natal_rising_idx is not None:
            L.append("")
            L.append(f"## Overlays: SR ASC falls in natal house {overlays['sr_asc_in_natal_house']}, "
                     f"SR MC in natal house {overlays['sr_mc_in_natal_house']}")
        L.append("")
        L.append("## Tightest SR-to-natal contacts")
        for c in sr["cross_aspects_to_natal"][:10]:
            L.append(f"- SR {c['sr_planet']} {c['aspect']} natal {c['natal_point']} (orb {c['orb']}°)")
        dsp = sr["dispositors"]
        L.append("")
        L.append(f"## The year resolves into {dsp['terminal_count']} final dispositor(s)")
        for f in dsp["final_dispositors"]:
            dg = ", ".join(f["dignities"]) if f["dignities"] else "peregrine"
            L.append(f"- **{f['planet']} in {f['sign']}** ({dg}) receives "
                     f"{f['count']} planet(s): {', '.join(f['disposits']) or 'itself only'}")
        for c in dsp["cycles"]:
            L.append(f"- {c['kind']}: {' <-> '.join(c['planets'])} (no terminal)")
        L.append(f"- Dignity: {sr['dignity_summary']['verdict']}")
        for r in sr["dignity_summary"]["debilitated"]:
            L.append(f"  - CAUTION {r['planet']} in {r['sign']} ({', '.join(r['dignities'])}), SR house {r['house']}")
        sys.stderr.write("\n".join(L) + "\n")

if __name__ == "__main__":
    main()
