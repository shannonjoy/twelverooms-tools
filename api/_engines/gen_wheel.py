# GENERATED COPY. Do not edit. Source: /Users/shannonowens/orchestrator/ventures/astrology-storefront/factsheet/gen_wheel.py
# Re-sync with bin/sync-engines.sh
#!/usr/bin/env python3
"""
gen_wheel.py — whole-sign chart wheel SVG from a fact-sheet JSON. v3 design.
Usage: python3 gen_wheel.py factsheet.json > wheel.svg
Design: fine-line, print-first, warm. Alternating sign band, degree ticks,
element-tinted glyphs, gold luminaries, house numerals, aspect lines with
anchor dots. Conjunction clusters are spread by relaxation at a single
planet ring, each glyph tied to its true degree by a hairline pointer
(the way professional chart software resolves crowding).
ASC on the left, zodiac counterclockwise. Untimed charts: 0° Aries left,
no axes or house numerals.
"""
import json, math, sys

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
         "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
GLYPH = {"Aries":"♈","Taurus":"♉","Gemini":"♊","Cancer":"♋",
         "Leo":"♌","Virgo":"♍","Libra":"♎","Scorpio":"♏",
         "Sagittarius":"♐","Capricorn":"♑","Aquarius":"♒","Pisces":"♓"}
PGLYPH = {"Sun":"☉","Moon":"☽","Mercury":"☿","Venus":"♀",
          "Mars":"♂","Jupiter":"♃","Saturn":"♄","Uranus":"♅",
          "Neptune":"♆","Pluto":"♇","North Node":"☊","South Node":"☋"}

INK, SOFT, FAINT = "#1d1d1f", "#6e6e73", "#d2d2d7"
ACCENT, RUST, GOLD = "#4a4a8f", "#a35548", "#a8863d"
WASH = "#f6f6f8"
ELEMENT_TINT = {"Fire": "#a3684a", "Earth": "#6f7d5c", "Air": "#7d86a8", "Water": "#4a6a8f"}
ELEMENT = dict(zip(SIGNS, ["Fire","Earth","Air","Water"]*3))

CX = CY = 280
R_RIM   = 268
R_OUT   = 262
R_SIGN  = 224
R_TICKS = 224
R_PLANET = 172   # single planet ring
R_LABEL  = 147   # radial degree labels
R_HOUSE = 104
R_HUB   = 92
R_ASPECT = 90
MIN_SEP = 8.5    # minimum angular separation between displayed glyphs

ASPECT_STYLE = {
    "trine":      (ACCENT, None,   1.05, 0.45),
    "sextile":    (ACCENT, "4 3",  0.95, 0.42),
    "square":     (RUST,   None,   1.05, 0.45),
    "opposition": (RUST,   "7 4",  1.05, 0.45),
    "quincunx":   (SOFT,   "2 4",  0.85, 0.5),
}

def spread(lons, min_sep=MIN_SEP, rounds=120):
    """Relax display angles apart until every adjacent pair is min_sep apart.
    lons: sorted ascending. Returns displaced copy (same order)."""
    d = list(lons)
    for _ in range(rounds):
        moved = False
        for i in range(1, len(d)):
            gap = d[i] - d[i-1]
            if gap < min_sep:
                push = (min_sep - gap) / 2
                d[i-1] -= push; d[i] += push
                moved = True
        if not moved:
            break
    return d

def build(fs):
    n = fs["natal"]
    timed = bool(n.get("asc"))
    asc = n["asc"]["lon"] if timed else 0.0

    def xy(lon, r):
        phi = math.radians(180.0 + (lon - asc))
        return CX + r*math.cos(phi), CY - r*math.sin(phi)

    def arc_band(l1, l2, r_in, r_out, fill):
        x1, y1 = xy(l1, r_out); x2, y2 = xy(l2, r_out)
        x3, y3 = xy(l2, r_in);  x4, y4 = xy(l1, r_in)
        return (f'<path d="M {x1:.1f} {y1:.1f} A {r_out} {r_out} 0 0 0 {x2:.1f} {y2:.1f} '
                f'L {x3:.1f} {y3:.1f} A {r_in} {r_in} 0 0 1 {x4:.1f} {y4:.1f} Z" '
                f'fill="{fill}" stroke="none"/>')

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 560" '
         f'font-family="-apple-system,Helvetica,Arial,sans-serif">']

    for k in range(12):
        if k % 2 == 0:
            s.append(arc_band(30*k, 30*(k+1), R_SIGN, R_OUT, WASH))

    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RIM}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_SIGN}" fill="none" stroke="{SOFT}" stroke-width="0.8"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_HUB}" fill="none" stroke="{FAINT}" stroke-width="0.9"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="2" fill="{INK}"/>')

    for d10 in range(0, 360, 5):
        strong = d10 % 10 == 0
        ln = 9 if strong else 5
        col = "#b8b8bd" if strong else FAINT
        x1, y1 = xy(d10, R_TICKS); x2, y2 = xy(d10, R_TICKS - ln)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.8"/>')

    for k in range(12):
        x1, y1 = xy(30*k, R_SIGN); x2, y2 = xy(30*k, R_RIM)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{SOFT}" stroke-width="0.9"/>')
        gx, gy = xy(30*k + 15, (R_SIGN + R_OUT) / 2)
        tint = ELEMENT_TINT[ELEMENT[SIGNS[k]]]
        s.append(f'<text x="{gx:.1f}" y="{gy:.1f}" font-size="19" fill="{tint}" '
                 f'text-anchor="middle" dominant-baseline="central">{GLYPH[SIGNS[k]]}︎</text>')

    # aspect lines + anchors
    lons = {p: e["lon"] for p, e in n["planets"].items()
            if e and p in PGLYPH and p not in ("North Node", "South Node")}
    anchors = set()
    for asp in n.get("aspects", []):
        a, b, kind = asp["a"], asp["b"], asp["aspect"]
        if kind not in ASPECT_STYLE or a not in lons or b not in lons:
            continue
        color, dash, width, op = ASPECT_STYLE[kind]
        x1, y1 = xy(lons[a], R_ASPECT); x2, y2 = xy(lons[b], R_ASPECT)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{color}" stroke-width="{width}" opacity="{op}"{d}/>')
        anchors.add(a); anchors.add(b)
    for p in sorted(anchors):
        ax, ay = xy(lons[p], R_ASPECT)
        s.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="1.9" fill="{INK}" opacity="0.7"/>')

    if timed:
        # horizon: light, elegant, full span; small arrowhead at ASC
        for lon_h, w, op in ((asc, 1.0, 0.9), (asc + 180, 0.9, 0.5)):
            x1, y1 = xy(lon_h, R_HUB); x2, y2 = xy(lon_h, R_RIM)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{SOFT}" stroke-width="{w}" opacity="{op}"/>')
        tipx, tipy = xy(asc, R_RIM - 1)
        bx, by = xy(asc, R_RIM - 11)
        s.append(f'<path d="M {tipx:.1f} {tipy:.1f} L {bx:.1f} {by-3.4:.1f} L {bx:.1f} {by+3.4:.1f} Z" fill="{SOFT}"/>')
        ax_, ay_ = xy(asc, R_HUB + 14)
        s.append(f'<text x="{ax_:.1f}" y="{ay_:.1f}" font-size="9.5" fill="{SOFT}" text-anchor="middle" '
                 f'dominant-baseline="central" letter-spacing="1.5" font-weight="600">ASC</text>')
        mc = n["mc"]["lon"]
        for lon_m, lab in ((mc, "MC"), (mc + 180, None)):
            x1, y1 = xy(lon_m, R_HUB); x2, y2 = xy(lon_m, R_RIM)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{ACCENT}" stroke-width="1" stroke-dasharray="5 4" opacity="{0.75 if lab else 0.3}"/>')
            if lab:
                mx, my = xy(lon_m, R_HUB + 14)
                s.append(f'<text x="{mx:.1f}" y="{my:.1f}" font-size="9.5" fill="{ACCENT}" text-anchor="middle" '
                         f'dominant-baseline="central" letter-spacing="1.5" font-weight="600">MC</text>')
        rising_idx = int(asc // 30)
        for h in range(12):
            sign_lon = ((rising_idx + h) % 12) * 30 + 15
            hx, hy = xy(sign_lon, R_HOUSE)
            s.append(f'<text x="{hx:.1f}" y="{hy:.1f}" font-size="10" fill="#b6b6bb" '
                     f'font-family="Georgia,serif" font-style="italic" text-anchor="middle" '
                     f'dominant-baseline="central">{h+1}</text>')

    # planets: single ring, relaxation-spread display angles, pointer to true degree
    bodies = [(p, e) for p, e in n["planets"].items() if e and p in PGLYPH and p != "South Node"]
    bodies.sort(key=lambda t: t[1]["lon"])
    true_lons = [e["lon"] for _, e in bodies]
    disp_lons = spread(true_lons)
    for (p, e), lon, disp in zip(bodies, true_lons, disp_lons):
        tx, ty = xy(lon, R_TICKS); tx2, ty2 = xy(lon, R_TICKS - 12)
        s.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="{INK}" stroke-width="1.3"/>')
        if abs(disp - lon) > 1.2:  # hairline pointer from true degree to shown glyph
            px1, py1 = xy(lon, R_TICKS - 14); px2, py2 = xy(disp, R_PLANET + 15)
            s.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" '
                     f'stroke="{FAINT}" stroke-width="0.7"/>')
        gx, gy = xy(disp, R_PLANET)
        col = GOLD if p in ("Sun", "Moon") else INK
        s.append(f'<text x="{gx:.1f}" y="{gy:.1f}" font-size="18" fill="{col}" text-anchor="middle" '
                 f'dominant-baseline="central">{PGLYPH[p]}︎</text>')
        deg = e["degree"]; mins = int(round((deg % 1) * 60))
        d_whole = int(deg)
        if mins == 60: d_whole += 1; mins = 0
        rx_flag = " Rx" if e.get("retrograde") and p not in ("North Node",) else ""
        lx, ly = xy(disp, R_LABEL)
        phi = (180.0 + (disp - asc)) % 360.0
        rot = -phi
        if 90 < phi < 270:
            rot += 180
        s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="8.6" fill="{SOFT}" '
                 f'font-family="Georgia,serif" text-anchor="middle" dominant-baseline="central" '
                 f'transform="rotate({rot:.1f} {lx:.1f} {ly:.1f})">{d_whole}°{mins:02d}′{rx_flag}</text>')

    s.append('</svg>')
    return "\n".join(s)

def main():
    print(build(json.load(open(sys.argv[1]))))

if __name__ == "__main__":
    main()
