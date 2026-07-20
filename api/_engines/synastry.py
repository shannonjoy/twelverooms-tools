# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/apps/twelve-rooms-studio/synastry.py
# Re-sync with bin/sync-engines.sh
"""Synastry: cross-aspects, house overlays, and balance for two charts.

Reuses compute_factsheet's aspect table, orb conventions, and helpers.
Untimed charts degrade per the existing missing_because_untimed convention:
no angles for that side, house overlays only in the timed direction.
"""
import engines

cf = engines.cf

PLANET_ORDER = list(cf.PLANETS) + ["North Node", "Chiron"]
CROSS_ORBS = {"conjunction": 6, "opposition": 6, "square": 6, "trine": 6,
              "sextile": 4, "quincunx": 2.5}
HARMONIOUS = {"trine", "sextile"}
FRICTION = {"square", "opposition", "quincunx"}


def _points(natal):
    """Longitudes for planets + angles of one computed natal."""
    pts = {}
    for p in PLANET_ORDER:
        e = natal["planets"].get(p)
        if e:
            pts[p] = e["lon"]
    if natal.get("asc"):
        pts["ASC"] = natal["asc"]["lon"]
        pts["MC"] = natal["mc"]["lon"]
    return pts


def cross_aspects(pts_a, pts_b):
    found = []
    for pa, la in pts_a.items():
        for pb, lb in pts_b.items():
            if pa in ("ASC", "MC") and pb in ("ASC", "MC"):
                continue
            for name, angle in cf.ASPECTS.items():
                if name == "semisextile":
                    continue
                orb_max = CROSS_ORBS[name]
                if name in cf.MAJORS and ("Sun" in (pa, pb) or "Moon" in (pa, pb)):
                    orb_max += 1
                if pa in ("North Node", "Chiron") or pb in ("North Node", "Chiron"):
                    orb_max = min(orb_max, 3)
                sep = abs(cf.angdiff(la, lb))
                orb = abs(sep - angle)
                if orb <= orb_max:
                    found.append({"a": pa, "b": pb, "aspect": name,
                                  "orb": round(orb, 2), "tight": orb <= 2.0,
                                  "harmony": ("harmonious" if name in HARMONIOUS
                                              else "friction" if name in FRICTION
                                              else "conjunction")})
    return sorted(found, key=lambda x: x["orb"])


def house_overlays(pts_from, natal_to):
    """Which of natal_to's whole-sign houses receive pts_from's planets."""
    if not natal_to.get("asc"):
        return None
    rising_idx = cf.SIGNS.index(natal_to["asc"]["sign"])
    out = {}
    for p, lon in pts_from.items():
        if p in ("ASC", "MC"):
            continue
        h = cf.whole_sign_house(lon, rising_idx)
        out.setdefault(h, []).append(p)
    return [{"house": h, "meaning": cf.HOUSE_MEANING[h], "planets": ps}
            for h, ps in sorted(out.items())]


def compare(order_a, order_b, name_a=None, name_b=None):
    natal_a = cf.build_natal(dict(order_a))[0]
    natal_b = cf.build_natal(dict(order_b))[0]
    pts_a, pts_b = _points(natal_a), _points(natal_b)
    aspects = cross_aspects(pts_a, pts_b)
    counts = {"harmonious": 0, "friction": 0, "conjunction": 0}
    for x in aspects:
        counts[x["harmony"]] += 1
    result = {
        "a": {"name": name_a or order_a.get("name"), "timed": natal_a["timed"],
              "balance": natal_a["balance"],
              "sun": natal_a["planets"]["Sun"]["pretty"],
              "moon": natal_a["planets"]["Moon"]["pretty"],
              "rising": natal_a["asc"]["pretty"] if natal_a.get("asc") else None},
        "b": {"name": name_b or order_b.get("name"), "timed": natal_b["timed"],
              "balance": natal_b["balance"],
              "sun": natal_b["planets"]["Sun"]["pretty"],
              "moon": natal_b["planets"]["Moon"]["pretty"],
              "rising": natal_b["asc"]["pretty"] if natal_b.get("asc") else None},
        "aspects": aspects,
        "counts": counts,
        "overlays_a_in_b": house_overlays(pts_a, natal_b),
        "overlays_b_in_a": house_overlays(pts_b, natal_a),
        "grid_svg": grid_svg(pts_a, pts_b, aspects,
                             name_a or order_a.get("name") or "A",
                             name_b or order_b.get("name") or "B"),
    }
    notes = []
    if not natal_a["timed"]:
        notes.append(f"{result['a']['name']}: untimed chart, no angles or house overlays from their side")
    if not natal_b["timed"]:
        notes.append(f"{result['b']['name']}: untimed chart, no angles or house overlays from their side")
    if notes:
        result["notes"] = notes
    return result


# ---------- rectangular A x B grid SVG ----------

ASPECT_GLYPH = {"conjunction": "☌", "sextile": "⚹", "square": "□",
                "trine": "△", "opposition": "☍", "quincunx": "⚻"}
INK, SOFT, FAINT = "#1d1d1f", "#6e6e73", "#d2d2d7"
ACCENT, RUST, GOLD, WASH = "#4a4a8f", "#a35548", "#a8863d", "#f6f6f8"
PGLYPH = dict(engines.gen_wheel.PGLYPH)
PGLYPH.update({"Chiron": "⚷", "ASC": "Asc", "MC": "MC"})


def grid_svg(pts_a, pts_b, aspects, name_a, name_b):
    rows = [p for p in PLANET_ORDER + ["ASC", "MC"] if p in pts_a]
    cols = [p for p in PLANET_ORDER + ["ASC", "MC"] if p in pts_b]
    lookup = {}
    for x in aspects:
        lookup[(x["a"], x["b"])] = x
    cell = 34
    left, top = 74, 74
    wdt = left + cell * len(cols) + 12
    hgt = top + cell * len(rows) + 12
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {wdt} {hgt}" '
         f'font-family="-apple-system,Helvetica,Arial,sans-serif">']
    s.append(f'<text x="{left - 58}" y="24" font-size="12" fill="{SOFT}" '
             f'font-family="Georgia,serif" font-style="italic">{name_a} ↓ · {name_b} →</text>')
    for j, pb in enumerate(cols):
        x = left + cell * j + cell / 2
        glyph = PGLYPH.get(pb, pb)
        size = 10 if pb in ("ASC", "MC") else 15
        s.append(f'<text x="{x:.0f}" y="{top - 12}" font-size="{size}" fill="{INK}" '
                 f'text-anchor="middle">{glyph}</text>')
    for i, pa in enumerate(rows):
        y = top + cell * i + cell / 2
        glyph = PGLYPH.get(pa, pa)
        size = 10 if pa in ("ASC", "MC") else 15
        s.append(f'<text x="{left - 18}" y="{y + 5:.0f}" font-size="{size}" fill="{INK}" '
                 f'text-anchor="middle">{glyph}</text>')
        for j, pb in enumerate(cols):
            x = left + cell * j
            yy = top + cell * i
            asp = lookup.get((pa, pb))
            fill = WASH if (i + j) % 2 == 0 else "#ffffff"
            s.append(f'<rect x="{x}" y="{yy}" width="{cell}" height="{cell}" '
                     f'fill="{fill}" stroke="{FAINT}" stroke-width="0.6"/>')
            if asp:
                col = (ACCENT if asp["harmony"] == "harmonious"
                       else RUST if asp["harmony"] == "friction" else GOLD)
                weight = "bold" if asp["tight"] else "normal"
                s.append(f'<text x="{x + cell / 2}" y="{yy + cell / 2 + 1}" font-size="14" '
                         f'fill="{col}" font-weight="{weight}" text-anchor="middle" '
                         f'dominant-baseline="central">{ASPECT_GLYPH[asp["aspect"]]}</text>')
                s.append(f'<text x="{x + cell / 2}" y="{yy + cell - 5}" font-size="7" '
                         f'fill="{SOFT}" text-anchor="middle">{asp["orb"]:.0f}°</text>')
    s.append('</svg>')
    return "\n".join(s)
