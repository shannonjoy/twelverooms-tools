"""The free solar return calculator (POST /api/natal with mode "solar_return").

HAND-WRITTEN. Like engines.py and horoscope_copy.py, this file is not a
generated copy: bin/sync-engines.sh does not touch it. The math is the
paid Solar Return reading's own engine (solar_return.py, synced from the
factsheet folder): find_return_jd for the exact instant, and the same
positions, whole-sign houses, dignities and orbs as its main(). This module
only arranges that engine's output for the web page, so the free tool and
the reading can never disagree.

Honesty rules, the same as the natal chart tool:
  - With a birth time: the return to the second, the Ascendant, Midheaven
    and every planet's house, at the place you spend the birthday.
  - Without one: the natal Sun is known only to about half a degree, so
    the return moment is known only to about half a day. The page gets the
    date range, the planets' signs and the Moon's possible signs, and no
    Ascendant or houses, rather than a guess.
"""
import calendar
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

import compute_factsheet as cf
import solar_return as sre

ORDER = list(cf.PLANETS)
CROSS_ORB = 2.5  # the reading's own cap for SR-to-natal contacts
OUTER = {"Uranus", "Neptune", "Pluto"}


def _guess_day(birth, year):
    """Birthday in `year`; Feb 29 births use Feb 28 as the starting guess."""
    m, d = birth.month, birth.day
    if m == 2 and d == 29 and not calendar.isleap(year):
        d = 28
    return m, d


def _return_jd(natal_sun_lon, birth, year):
    m, d = _guess_day(birth, year)
    return sre.find_return_jd(natal_sun_lon, year, m, d)


def _iso(dt):
    return dt.replace(microsecond=0).isoformat()


def _planet_rows(pos, rising_idx):
    rows = []
    for p in ORDER:
        lon = pos[p]["lon"]
        sign, deg = cf.sign_of(lon)
        row = {"body": p, "position": cf.fmt_deg(lon), "sign": sign,
               "degree": round(deg, 2), "retrograde": pos[p]["retrograde"],
               "dignities": cf.dignity(p, sign)}
        if rising_idx is not None:
            h = cf.whole_sign_house(lon, rising_idx)
            row["house"] = h
            row["house_meaning"] = cf.HOUSE_MEANING[h]
        rows.append(row)
    return rows


def compute(o):
    """o: the POST body. {date, time?, tz, lat, lon, year, where?: {lat, lon, tz, place?}}"""
    birth = date.fromisoformat(o["date"])
    year = int(o["year"])
    if not (birth.year < year <= 2100):
        raise ValueError("Choose a year after your birth year, up to 2100.")
    order = {"name": "Solar return", "date": o["date"], "time": o.get("time") or None,
             "tz": o["tz"], "lat": float(o["lat"]), "lon": float(o["lon"])}
    natal, natal_pos, natal_rising, _sect, _jd = cf.build_natal(order)
    timed = natal["timed"]

    where = o.get("where") or {}
    if where.get("tz") and where.get("lat") not in (None, "") and where.get("lon") not in (None, ""):
        loc = {"lat": float(where["lat"]), "lon": float(where["lon"]), "tz": where["tz"],
               "place": str(where.get("place") or "")[:80], "birthplace": False}
    else:
        loc = {"lat": order["lat"], "lon": order["lon"], "tz": order["tz"],
               "place": str(o.get("place") or "")[:80], "birthplace": True}
    tz = ZoneInfo(loc["tz"])

    # The fact sheet's Sun (rounded to 0.0001 degree, a few seconds of time),
    # the value the reading's engine reads, so the two agree to the second.
    natal_sun = natal["planets"]["Sun"]["lon"]
    jd = _return_jd(natal_sun, birth, year)
    moment_utc = sre.jd_to_dt(jd)
    pos = cf.positions_at(jd)
    sun_off = abs(cf.angdiff(pos["Sun"]["lon"], natal_sun))

    out = {"year": year, "timed": timed,
           "natal_sun": cf.fmt_deg(natal_sun),
           "location": {"place": loc["place"], "tz": loc["tz"], "birthplace": loc["birthplace"]},
           "method": ("Swiss Ephemeris (Moshier), the Sun's exact return to its natal longitude, "
                      "whole-sign houses; the same engine as the Solar Return reading"),
           "sun_check_arcsec": round(sun_off * 3600, 3)}

    if timed:
        moment_local = moment_utc.astimezone(tz)
        cusps, ascmc = swe.houses_ex(jd, loc["lat"], loc["lon"], b'W', swe.FLG_MOSEPH)
        asc, mc = ascmc[0] % 360, ascmc[1] % 360
        rising_idx = int(asc // 30)
        below = 0 <= (pos["Sun"]["lon"] - asc) % 360 < 180
        rs = cf.SIGNS[rising_idx]
        ruler = cf.RULER[rs]
        planets = _planet_rows(pos, rising_idx)
        by = {r["body"]: r for r in planets}
        natal_rising_idx = natal_rising
        out.update({
            "moment_utc": _iso(moment_utc), "moment_local": _iso(moment_local),
            "moment_label": moment_local.strftime("%B %-d, %Y at %-I:%M:%S %p ") + moment_local.tzname(),
            "asc": {"position": cf.fmt_deg(asc), "sign": rs},
            "mc": {"position": cf.fmt_deg(mc), "sign": cf.sign_of(mc)[0],
                   "house": cf.whole_sign_house(mc, rising_idx)},
            "sect": "night" if below else "day",
            "chart_ruler": {"planet": ruler, "sign": by[ruler]["sign"], "house": by[ruler]["house"]},
            "sun_house": by["Sun"]["house"], "sun_house_meaning": by["Sun"]["house_meaning"],
            "moon": {"sign": by["Moon"]["sign"], "position": by["Moon"]["position"],
                     "house": by["Moon"]["house"], "house_meaning": by["Moon"]["house_meaning"]},
            "planets": planets,
            "sr_asc_in_natal_house": cf.whole_sign_house(asc, natal_rising_idx),
        })
        # The year's tightest contacts to the birth chart (majors, 2.5 degrees).
        targets = {p: natal_pos[p]["lon"] for p in ORDER}
        targets["Ascendant"] = natal["asc"]["lon"]
        targets["Midheaven"] = natal["mc"]["lon"]
        cross = []
        for sp in ORDER:
            for tgt, tlon in targets.items():
                if sp == "Sun" and tgt == "Sun":
                    continue  # the return itself
                if sp in OUTER and tgt in OUTER:
                    continue  # generational: true for everyone born that year
                for name in cf.MAJORS:
                    orb = abs(abs(cf.angdiff(pos[sp]["lon"], tlon)) - cf.ASPECTS[name])
                    if orb <= CROSS_ORB:
                        cross.append({"sr": sp, "aspect": name, "natal": tgt, "orb": round(orb, 2)})
        out["contacts"] = sorted(cross, key=lambda c: c["orb"])[:6]
        # The wheel, drawn by the same renderer as the natal chart tool.
        try:
            import gen_wheel
            sr_chart = {"timed": True,
                        "asc": {"lon": asc, "pretty": cf.fmt_deg(asc), "sign": rs},
                        "mc": {"lon": mc, "pretty": cf.fmt_deg(mc), "sign": cf.sign_of(mc)[0],
                               "house": cf.whole_sign_house(mc, rising_idx)},
                        "planets": {}, "aspects": cf.natal_aspects(pos), "patterns": []}
            for p in list(cf.PLANETS) + ["North Node", "South Node", "Chiron"]:
                if pos.get(p) is None:
                    sr_chart["planets"][p] = None
                    continue
                lon = pos[p]["lon"]
                sr_chart["planets"][p] = {"lon": round(lon, 4), "pretty": cf.fmt_deg(lon),
                                          "sign": cf.sign_of(lon)[0],
                                          "degree": round(cf.sign_of(lon)[1], 2),
                                          "retrograde": pos[p]["retrograde"],
                                          "house": cf.whole_sign_house(lon, rising_idx)}
            out["wheel_svg"] = gen_wheel.build({"order": {"name": f"Solar return {year}"},
                                                "natal": sr_chart})
        except Exception:  # the wheel is a picture; the numbers above stand without it
            out["wheel_svg"] = None
    else:
        # Untimed: the natal Sun could sit anywhere in that day's arc, so the
        # return could fall anywhere in a matching span about a day long.
        btz = ZoneInfo(order["tz"])
        lo_local = datetime.fromisoformat(f"{o['date']}T00:00:00").replace(tzinfo=btz)
        hi_local = datetime.fromisoformat(f"{o['date']}T23:59:00").replace(tzinfo=btz)
        sun_lo = cf.calc(cf.jd_ut(lo_local.astimezone(timezone.utc)), swe.SUN)[0]
        sun_hi = cf.calc(cf.jd_ut(hi_local.astimezone(timezone.utc)), swe.SUN)[0]
        jd_lo = _return_jd(sun_lo, birth, year)
        jd_hi = _return_jd(sun_hi, birth, year)
        t_lo = sre.jd_to_dt(jd_lo).astimezone(tz)
        t_hi = sre.jd_to_dt(jd_hi).astimezone(tz)
        moons = []
        for j in (jd_lo, jd, jd_hi):
            s = cf.sign_of(cf.calc(j, swe.MOON)[0])[0]
            if s not in moons:
                moons.append(s)
        out.update({
            "window_local": {"from": _iso(t_lo), "to": _iso(t_hi)},
            "window_label": (f"between {t_lo.strftime('%B %-d at %-I:%M %p')} and "
                             f"{t_hi.strftime('%B %-d, %Y at %-I:%M %p')} {t_hi.tzname()}"),
            "moon": {"signs": moons},
            "planets": [r for r in _planet_rows(pos, None) if r["body"] != "Moon"],
        })
        # A planet near a sign line can change sign inside the window; say so.
        edge = [cf.positions_at(jd_lo), cf.positions_at(jd_hi)]
        for r in out["planets"]:
            signs = []
            for p_ in (edge[0], pos, edge[1]):
                sg = cf.sign_of(p_[r["body"]]["lon"])[0]
                if sg not in signs:
                    signs.append(sg)
            if len(signs) > 1:
                r["signs"] = signs
    return out
