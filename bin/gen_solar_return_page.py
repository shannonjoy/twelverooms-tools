#!/usr/bin/env python3
"""gen_solar_return_page.py — render a solar-return year book as one
self-contained HTML page (light, print-ready) from the engine JSON plus a
hand-written reading JSON.

    python3 bin/solar_return.py ... --out sr.json
    python3 bin/gen_solar_return_page.py --data sr.json --reading reading.json --out year.html

The engine supplies every number; the reading supplies the prose. Nothing in
the prose is computed here, and nothing in the tables is written by hand.

Reading JSON (all keys optional; paragraphs are plain strings, light HTML ok):
  title, subtitle, dedication
  overture: [p], chart_argument: [p]
  houses: {"1": {"title": str, "body": [p]}, ...}
  money / career / love / family / body_spirit / home: {"lede": str, "body": [p],
      "dates": [{"date": "YYYY-MM-DD", "label": str, "why": str}]}
  chapters: [{"title": str, "range": "YYYY-MM-DD..YYYY-MM-DD", "body": [p]}]
  eclipses: [p], closing: [p], sources: [str]
"""
import json, argparse, math, html
from pathlib import Path
from datetime import date, datetime, timedelta

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
         "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
GLYPH = {"Aries":"♈︎","Taurus":"♉︎","Gemini":"♊︎","Cancer":"♋︎","Leo":"♌︎","Virgo":"♍︎",
         "Libra":"♎︎","Scorpio":"♏︎","Sagittarius":"♐︎","Capricorn":"♑︎","Aquarius":"♒︎","Pisces":"♓︎"}
PG = {"Sun":"☉","Moon":"☽","Mercury":"☿","Venus":"♀","Mars":"♂","Jupiter":"♃","Saturn":"♄",
      "Uranus":"♅","Neptune":"♆","Pluto":"♇","North Node":"☊","South Node":"☋","Chiron":"⚷",
      "ASC":"Asc","MC":"MC","DSC":"Dsc","IC":"IC","Fortune":"⊗","Spirit":"⊙"}
ELEMENT = dict(zip(SIGNS, ["Fire","Earth","Air","Water"]*3))
TINT = {"Fire": "#a3684a", "Earth": "#6f7d5c", "Air": "#7d86a8", "Water": "#4a6a8f"}
ASP_SYM = {"conjunction":"☌","sextile":"⚹","square":"□","trine":"△","opposition":"☍","quincunx":"⚻","semisextile":"⚺"}
ASP_COLOR = {"trine":"#4a4a8f","sextile":"#4a4a8f","square":"#a35548","opposition":"#a35548","conjunction":"#7a5f24","quincunx":"#8a8a90"}
ORD = lambda n: f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"

def esc(s): return html.escape(str(s), quote=True)
def fmtdate(iso, fmt="%a, %b %-d"):
    return datetime.fromisoformat(iso[:10]).strftime(fmt)
def deg_min(d):
    m = int(round((d % 1) * 60)); w = int(d)
    if m == 60: w += 1; m = 0
    return f"{w}°{m:02d}′"

# ------------------------------------------------------------------ art

def biwheel(sr, natal, overlay, size=680):
    """Outer ring: solar-return planets. Inner ring: natal planets. Houses from the
    return Ascendant (left). Aspect lines: return-to-natal contacts within 2°."""
    cx = cy = size / 2
    asc = sr["asc"]["lon"]
    R_RIM, R_SIGN_OUT, R_SIGN_IN = size*0.485, size*0.475, size*0.415
    R_SR, R_SRLAB = size*0.365, size*0.315
    R_DIV = size*0.285
    R_NAT, R_NATLAB = size*0.235, size*0.19
    R_HUB, R_ASP = size*0.155, size*0.15
    def xy(lon, r):
        phi = math.radians(180.0 + (lon - asc))
        return cx + r*math.cos(phi), cy - r*math.sin(phi)
    def arc(l1, l2, r_in, r_out, fill):
        x1,y1 = xy(l1,r_out); x2,y2 = xy(l2,r_out); x3,y3 = xy(l2,r_in); x4,y4 = xy(l1,r_in)
        return (f'<path d="M {x1:.1f} {y1:.1f} A {r_out:.1f} {r_out:.1f} 0 0 0 {x2:.1f} {y2:.1f} '
                f'L {x3:.1f} {y3:.1f} A {r_in:.1f} {r_in:.1f} 0 0 1 {x4:.1f} {y4:.1f} Z" fill="{fill}" stroke="none"/>')
    def spread(lons, min_sep=8.0):
        d = list(lons)
        for _ in range(160):
            moved = False
            for i in range(1, len(d)):
                gap = d[i]-d[i-1]
                if gap < min_sep:
                    push = (min_sep-gap)/2; d[i-1]-=push; d[i]+=push; moved=True
            if not moved: break
        return d
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" class="biwheel" role="img" aria-label="Solar return chart over the natal chart">']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R_RIM}" fill="#fff" stroke="#26355e" stroke-width="0.9"/>')
    for k in range(12):
        if k % 2 == 0: s.append(arc(30*k, 30*(k+1), R_SIGN_IN, R_SIGN_OUT, "#f4f0e6"))
    for r, col, w in ((R_SIGN_OUT,"#26355e",1.1),(R_SIGN_IN,"#a8863d",0.9),(R_DIV,"#e4ddcf",0.9),(R_HUB,"#e4ddcf",0.8)):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>')
    for d in range(0, 360, 5):
        ln = 8 if d % 10 == 0 else 4
        x1,y1 = xy(d, R_SIGN_IN); x2,y2 = xy(d, R_SIGN_IN-ln)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#c9c2b4" stroke-width="0.7"/>')
    for k in range(12):
        x1,y1 = xy(30*k, R_SIGN_IN); x2,y2 = xy(30*k, R_RIM)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#a8863d" stroke-width="0.8"/>')
        gx,gy = xy(30*k+15, (R_SIGN_IN+R_SIGN_OUT)/2)
        s.append(f'<text x="{gx:.1f}" y="{gy:.1f}" font-size="{size*0.03:.1f}" fill="{TINT[ELEMENT[SIGNS[k]]]}" text-anchor="middle" dominant-baseline="central">{GLYPH[SIGNS[k]]}</text>')
        # house cusp lines (whole sign) inside
        hx1,hy1 = xy(30*k, R_HUB); hx2,hy2 = xy(30*k, R_SIGN_IN)
        s.append(f'<line x1="{hx1:.1f}" y1="{hy1:.1f}" x2="{hx2:.1f}" y2="{hy2:.1f}" stroke="#ebe5d8" stroke-width="0.7"/>')
    # axes
    for lon_, lab, col in ((asc,"ASC","#26355e"),(asc+180,"DSC","#26355e"),(sr["mc"]["lon"],"MC","#7a5f24"),(sr["mc"]["lon"]+180,"IC","#7a5f24")):
        x1,y1 = xy(lon_, R_HUB); x2,y2 = xy(lon_, R_RIM)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{1.4 if lab in ("ASC","MC") else 0.8}" opacity="0.8" stroke-dasharray="{"" if lab in ("ASC","DSC") else "6 4"}"/>')
        tx,ty = xy(lon_, R_HUB-13)
        s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="9" fill="{col}" text-anchor="middle" dominant-baseline="central" letter-spacing="1.2" font-weight="600">{lab}</text>')
    ridx = sr["rising_idx"]
    for h in range(12):
        hx,hy = xy(((ridx+h)%12)*30+15, R_DIV+ (R_SR-R_DIV)*0.0 - 12)
        s.append(f'<text x="{hx:.1f}" y="{hy:.1f}" font-size="10" fill="#b6b0a4" font-family="Cormorant Garamond,Georgia,serif" font-style="italic" text-anchor="middle" dominant-baseline="central">{h+1}</text>')
    # aspect lines return -> natal within 2°
    nat_l = {p: e["lon"] for p, e in natal["planets"].items() if e and p not in ("South Node",)}
    nat_l["ASC"] = natal["asc"]["lon"]; nat_l["MC"] = natal["mc"]["lon"]
    sr_l = {p: e["lon"] for p, e in sr["planets"].items() if p != "South Node"}
    sr_l["ASC"] = sr["asc"]["lon"]; sr_l["MC"] = sr["mc"]["lon"]
    for a in overlay["aspects_sr_to_natal"]:
        if a["orb"] > 2.0 or a["aspect"] not in ASP_COLOR or a["is_return"]: continue
        if a["sr"] not in sr_l or a["natal"] not in nat_l: continue
        x1,y1 = xy(sr_l[a["sr"]], R_ASP); x2,y2 = xy(nat_l[a["natal"]], R_ASP)
        dash = ' stroke-dasharray="4 3"' if a["aspect"] in ("sextile","opposition","quincunx") else ""
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ASP_COLOR[a["aspect"]]}" stroke-width="1" opacity="0.55"{dash}/>')
    # rings of planets
    def ring(entries, r_g, r_lab, size_g, color_fn, ring_r_tick):
        entries = sorted(entries, key=lambda t: t[1]); true = [t[1] for t in entries]; disp = spread(true)
        for (p, lon, retro), dl in zip(entries, disp):
            tx,ty = xy(lon, ring_r_tick); tx2,ty2 = xy(lon, ring_r_tick-9)
            s.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="#1d1d1f" stroke-width="1.2"/>')
            if abs(dl-lon) > 1.0:
                px1,py1 = xy(lon, ring_r_tick-10); px2,py2 = xy(dl, r_g+size_g*0.7)
                s.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="#d2ccbf" stroke-width="0.6"/>')
            gx,gy = xy(dl, r_g)
            s.append(f'<text x="{gx:.1f}" y="{gy:.1f}" font-size="{size_g}" fill="{color_fn(p)}" text-anchor="middle" dominant-baseline="central">{PG[p]}</text>')
            lx,ly = xy(dl, r_lab); phi = (180+(dl-asc))%360; rot = -phi + (180 if 90<phi<270 else 0)
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="8" fill="#656b85" font-family="Cormorant Garamond,Georgia,serif" text-anchor="middle" dominant-baseline="central" transform="rotate({rot:.1f} {lx:.1f} {ly:.1f})">{deg_min(lon%30)}{" ℞" if retro else ""}</text>')
    sr_entries = [(p, e["lon"], e["retrograde"]) for p, e in sr["planets"].items() if p in PG and p != "South Node"]
    nat_entries = [(p, e["lon"], e["retrograde"]) for p, e in natal["planets"].items() if e and p in PG and p != "South Node"]
    ring(sr_entries, R_SR, R_SRLAB, size*0.03, lambda p: "#7a5f24" if p in ("Sun","Moon") else "#1d1d1f", R_SIGN_IN)
    ring(nat_entries, R_NAT, R_NATLAB, size*0.024, lambda p: "#8a6a28" if p in ("Sun","Moon") else "#656b85", R_DIV)
    s.append(f'<text x="{cx}" y="{cy-6}" font-size="9" fill="#a8863d" text-anchor="middle" letter-spacing="2" font-family="Cormorant Garamond,Georgia,serif">RETURN</text>')
    s.append(f'<text x="{cx}" y="{cy+8}" font-size="8" fill="#b6b0a4" text-anchor="middle" letter-spacing="1.5" font-family="Cormorant Garamond,Georgia,serif">over natal</text>')
    s.append('</svg>')
    return "\n".join(s)

def aspect_grid(chart):
    """Triangular aspect grid of the return chart."""
    order = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","ASC","MC"]
    look = {}
    for a in chart["aspects"]:
        look[(a["a"], a["b"])] = a; look[(a["b"], a["a"])] = a
    cell = 30; n = len(order); pad = 34
    W = pad + cell*n + 6; H = pad + cell*n + 6
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="aspgrid" role="img" aria-label="Aspect grid of the solar return chart">']
    for i, p in enumerate(order):
        s.append(f'<text x="{pad-8}" y="{pad+cell*i+cell/2}" font-size="13" fill="#26355e" text-anchor="end" dominant-baseline="central">{PG[p] if p not in ("ASC","MC") else p}</text>')
        for j in range(i):
            q = order[j]; x = pad+cell*j; y = pad+cell*i
            s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{"#fff" if (i+j)%2 else "#f9f6ef"}" stroke="#e4ddcf" stroke-width="0.6"/>')
            a = look.get((p, q))
            if a and a["aspect"] in ASP_SYM:
                col = ASP_COLOR.get(a["aspect"], "#8a8a90")
                s.append(f'<text x="{x+cell/2}" y="{y+cell/2-4}" font-size="13" fill="{col}" text-anchor="middle" dominant-baseline="central">{ASP_SYM[a["aspect"]]}</text>')
                s.append(f'<text x="{x+cell/2}" y="{y+cell/2+9}" font-size="7.5" fill="#8a8a90" text-anchor="middle" dominant-baseline="central">{a["orb"]:.1f}°</text>')
    for j, p in enumerate(order[:-1]):
        s.append(f'<text x="{pad+cell*j+cell/2}" y="{pad+cell*(j+1)-cell/2+cell}" font-size="12" fill="#26355e" text-anchor="middle" dominant-baseline="central">{PG[p] if p not in ("ASC","MC") else p}</text>')
    s.append('</svg>')
    return "\n".join(s)

def moon_glyph(kind, size=22):
    r = size/2 - 1; cx = cy = size/2
    if kind == "new":
        body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#26355e"/>'
    elif kind == "full":
        body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f3e3b3"/>'
    elif kind == "first quarter":
        body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#26355e"/><path d="M {cx} {cy-r} A {r} {r} 0 0 1 {cx} {cy+r} Z" fill="#f3e3b3"/>'
    else:
        body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#26355e"/><path d="M {cx} {cy-r} A {r} {r} 0 0 0 {cx} {cy+r} Z" fill="#f3e3b3"/>'
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="moonglyph" aria-hidden="true"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#a8863d" stroke-width="0.8"/>{body}</svg>'

def constellation_svg(sr, w=1200, h=200):
    """Decorative: the return chart's planets as a gold constellation across the hero."""
    pts = []
    ORDER = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","North Node"]
    for p, e in sr["planets"].items():
        if p not in ORDER: continue
        # x from longitude, y from the degree within the sign: deterministic, chart-specific
        x = 40 + (e["lon"]/360.0)*(w-80)
        y = 36 + ((e["degree"] * 3.7 + ORDER.index(p) * 41) % 100) / 100.0 * (h-84)
        pts.append((p, x, y))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="constellation" preserveAspectRatio="none" aria-hidden="true">']
    import random
    rnd = random.Random(7)
    for _ in range(90):
        s.append(f'<circle cx="{rnd.uniform(0,w):.0f}" cy="{rnd.uniform(0,h):.0f}" r="{rnd.uniform(0.4,1.3):.1f}" fill="#a8863d" opacity="{rnd.uniform(0.15,0.5):.2f}"/>')
    pts.sort(key=lambda t: t[1])
    for (p1,x1,y1),(p2,x2,y2) in zip(pts, pts[1:]):
        s.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#a8863d" stroke-width="0.6" opacity="0.35"/>')
    for p,x,y in pts:
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.4" fill="#a8863d"/><circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="none" stroke="#a8863d" stroke-width="0.5" opacity="0.5"/>')
        s.append(f'<text x="{x:.0f}" y="{y-11:.0f}" font-size="11" fill="#7a5f24" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif">{PG[p]}</text>')
    s.append('</svg>')
    return "\n".join(s)

# ------------------------------------------------------------------ helpers for prose blocks

def paras(lst, cls=""):
    return "\n".join(f'<p class="{cls}">{p}</p>' for p in (lst or []))

def stars(n): return '<span class="stars">' + "★"*n + '<span class="dim">' + "★"*(5-n) + "</span></span>"

# ------------------------------------------------------------------ page

def build(data, reading):
    sr = data["solar_return"]; natal = data["natal"]; ov = data["overlay"]; ye = data["year_events"]
    tzname = data["order"]["tz"]; name = data["order"].get("name") or "the native"
    days = data["days"]; occ = data["occasions"]; year = data["year"]
    first_name = name.split()[0]
    prof = data["profection"]
    n_idx = SIGNS.index(natal["asc"]["sign"])
    R = reading

    # ---------- slim JSON for the interactive parts
    day_index = {d["date"]: i for i, d in enumerate(days)}
    slim_days = [{"d": d["date"], "w": d["weekday"], "ms": d["moon"]["sign"], "mp": d["moon"]["phase_name"],
                  "il": d["moon"]["illumination"], "mh": d["moon"]["natal_house"], "voc": d["moon"]["voc"],
                  "vs": d["moon"]["voc_share"], "perf": d["moon"]["perfections"], "dr": d["day_ruler"],
                  "win": d["windows_pretty"], "rx": d["retro"], "sh": d["mercury_shadow"], "ecl": d["eclipse_near"],
                  "hours": d["hours_pretty"], "sun": d["sun_pretty"], "moon": d["moon"]["pretty"]} for d in days]
    slim_occ = {}
    for k, o in occ.items():
        slim_occ[k] = {"meta": o["meta"], "days": [[r["score"], r["rank"], r["stars"],
                        (f'{r["best_window"]["start"]}–{r["best_window"]["end"]} · {r["best_window"]["hour"]}' + (" hour" if r["best_window"]["kind"] != "rising" else " rising") if r["best_window"] else ""),
                        r["plus"][:3], r["minus"][:2]] for r in o["days"]]}
    events_slim = {
        "lunations": [{"d": l["local"][:10], "k": l["kind"], "deg": l["moon_pretty"], "ecl": (l["eclipse"] or {}).get("type"), "kind_e": (l["eclipse"] or {}).get("kind"), "h": l["natal_house"], "sab": l["sabian"]["label"]} for l in ye["lunations"]],
        "stations": [{"d": s["local"][:10], "b": s["body"], "t": s["type"], "deg": s["pretty_lon"]} for s in ye["stations"]],
        "returns": [{"d": h["date"], "b": h["transiting"], "p": h["pass_label"]} for h in ye["perfections"] if h["is_return"] and h["transiting"] in ("Jupiter","Venus","Mars","Mercury")],
        "ingresses": [{"d": i["local"][:10], "b": i["body"], "s": i["sign"], "rx": i["retrograde"]} for i in ye["ingresses"]],
    }
    overall = {r["date"]: [r["score"], r["rank"]] for r in data["overall"]}
    payload = {"days": slim_days, "occ": slim_occ, "events": events_slim, "overall": overall,
               "start": days[0]["date"], "rule": data["electional_rule"], "name": first_name}
    payload_json = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

    # ---------- hero facts
    sun = sr["planets"]["Sun"]; moon = sr["planets"]["Moon"]; ruler = sr["chart_ruler"]
    jr = [h for h in ye["perfections"] if h["is_return"] and h["transiting"] == "Jupiter"]
    ecl_count = sum(1 for l in ye["lunations"] if l["eclipse"])
    hero_stats = [
        ("Rising", f'{GLYPH[sr["rising_sign"]]} {deg_min(sr["asc"]["degree"])} {sr["rising_sign"]}'),
        ("Midheaven", f'{GLYPH[sr["mc"]["sign"]]} {deg_min(sr["mc"]["degree"])} {sr["mc"]["sign"]}'),
        ("Moon", f'{GLYPH[moon["sign"]]} {deg_min(moon["degree"])} {moon["sign"]} · {ORD(moon["house"])} house'),
        ("Chart ruler", f'{PG[ruler["planet"]]} {ruler["planet"]} in {ruler["sign"]} · {ORD(ruler["house"])} house' + (" · " + ", ".join(ruler["dignities"]) if ruler.get("dignities") else "")),
        ("Sect", f'{sr["sect"].title()} chart · benefic of sect {sr["sect_roles"]["benefic_of_sect"]}'),
        ("Year lord", f'{PG[prof["year_lord"]]} {prof["year_lord"]} · {ORD(prof["activated_house"])} house profection ({prof["activated_sign"]})'),
    ]
    if jr:
        hero_stats.append(("Jupiter Return", " · ".join(fmtdate(h["date"], "%b %-d, %Y") for h in jr)))
    hero_stats.append(("Eclipses this year", str(ecl_count)))

    # ---------- positions table
    def pos_rows(chart, in_natal=None):
        rows = []
        order = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","North Node","Chiron"]
        for p in order:
            e = chart["planets"].get(p)
            if not e: continue
            dign = ", ".join(e.get("dignities") or []) if e.get("dignities") else ""
            nat_h = f'<td>{ORD(in_natal[p])}</td>' if in_natal else ""
            rows.append(f'<tr><td class="g">{PG[p]}</td><td><strong>{p}</strong></td><td class="mono">{deg_min(e["degree"])} {GLYPH[e["sign"]]} {e["sign"]}{" ℞" if e["retrograde"] else ""}</td>'
                        f'<td>{ORD(e["house"])}</td>{nat_h}<td class="soft">{dign}</td><td class="sab">{esc(e["sabian"]["label"])}: {esc(e["sabian"]["image"] or "")}</td></tr>')
        for a in ("asc","mc"):
            e = chart[a]
            deg = e.get("degree", e["lon"] % 30)
            hse = e.get("house") or (1 if a == "asc" else ((SIGNS.index(e["sign"]) - SIGNS.index(chart["asc"]["sign"])) % 12) + 1)
            nat_h = f'<td>{ORD(in_natal[a.upper()])}</td>' if in_natal else ""
            rows.append(f'<tr><td class="g">{a.upper()}</td><td><strong>{"Ascendant" if a=="asc" else "Midheaven"}</strong></td><td class="mono">{deg_min(deg)} {GLYPH[e["sign"]]} {e["sign"]}</td><td>{ORD(hse)}</td>{nat_h}<td></td><td class="sab">{esc(e["sabian"]["label"])}: {esc(e["sabian"]["image"] or "")}</td></tr>')
        for ln, e in chart["lots"].items():
            nat_h = f'<td>{ORD(in_natal["Lot of "+ln])}</td>' if in_natal and ("Lot of "+ln) in in_natal else (f'<td></td>' if in_natal else "")
            rows.append(f'<tr><td class="g">{PG[ln]}</td><td><strong>Lot of {ln}</strong></td><td class="mono">{deg_min(e["degree"])} {GLYPH[e["sign"]]} {e["sign"]}</td><td>{ORD(e["house"])}</td>{nat_h}<td></td><td class="sab">{esc(e["sabian"]["label"])}: {esc(e["sabian"]["image"] or "")}</td></tr>')
        return "\n".join(rows)

    sr_table = f'''<table class="tbl positions"><thead><tr><th></th><th>Body</th><th>Return position</th><th>Return house</th><th>Falls in natal house</th><th>Dignity</th><th>Sabian symbol</th></tr></thead><tbody>{pos_rows(sr, ov["sr_planets_in_natal_houses"])}</tbody></table>'''
    natal_table = f'''<table class="tbl positions"><thead><tr><th></th><th>Body</th><th>Natal position</th><th>Natal house</th><th>Dignity</th><th>Sabian symbol</th></tr></thead><tbody>{pos_rows(natal)}</tbody></table>'''

    # SR-to-natal aspects
    sn_rows = "\n".join(
        f'<tr><td>{PG.get(a["sr"], a["sr"])} <strong>Return {a["sr"]}</strong></td><td class="asp" style="color:{ASP_COLOR.get(a["aspect"],"#555")}">{ASP_SYM.get(a["aspect"],"")} {a["aspect"]}</td><td>{PG.get(a["natal"], a["natal"])} natal {a["natal"]}</td><td class="mono">{a["orb"]:.2f}°</td><td>{"return" if a["is_return"] else ("tight" if a["tight"] else "")}</td></tr>'
        for a in ov["aspects_sr_to_natal"] if a["orb"] <= 3.0)
    sr_asp_rows = "\n".join(
        f'<tr><td>{PG.get(a["a"], a["a"])} {a["a"]}</td><td class="asp" style="color:{ASP_COLOR.get(a["aspect"],"#555")}">{ASP_SYM.get(a["aspect"],"")} {a["aspect"]}</td><td>{PG.get(a["b"], a["b"])} {a["b"]}</td><td class="mono">{a["orb"]:.2f}°</td></tr>'
        for a in sr["aspects"] if a["orb"] <= 3.0 and a["aspect"] in ASP_SYM)

    # ---------- twelve rooms
    rooms = []
    for h in range(1, 13):
        info = sr["houses"][str(h)] if str(h) in sr["houses"] else sr["houses"][h]
        occs = ", ".join(f'{PG[p]} {p}' for p in info["occupants"]) or "—"
        rr = info["ruler_in"]
        nat_here = [p for p, hh in ov["natal_planets_in_sr_houses"].items() if hh == h and p not in ("South Node",)]
        natal_sign_house = ((SIGNS.index(info["sign"]) - n_idx) % 12) + 1
        rd = R.get("houses", {}).get(str(h), {})
        rooms.append(f'''<article class="room"><div class="room-head"><span class="roman">{["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"][h-1]}</span>
<div><h3>{esc(rd.get("title") or info["meaning"].capitalize())}</h3><div class="room-meta">{GLYPH[info["sign"]]} {info["sign"]} · {info["meaning"]} · your natal {ORD(natal_sign_house)} house</div></div></div>
<dl class="room-facts"><dt>Return planets here</dt><dd>{occs}</dd><dt>Ruler {PG[info["ruler"]]} {info["ruler"]}</dt><dd>in {rr["sign"]}, {ORD(rr["house"])} house{" ℞" if rr["retrograde"] else ""}{(" · " + ", ".join(rr["dignities"])) if rr.get("dignities") else ""}</dd><dt>Your natal planets here</dt><dd>{", ".join((PG.get(p,"")+" "+p).strip() if p not in ("ASC","MC") else ("Ascendant" if p=="ASC" else "Midheaven") for p in nat_here) or "—"}</dd></dl>
{paras(rd.get("body"))}</article>''')

    # ---------- domain sections
    def top_dates_block(keys, n=10):
        """Union of the best days across the given occasion keys, ranked by best score."""
        best = {}
        for k in keys:
            for r in occ[k]["days"]:
                if r["rank"] <= 25:
                    cur = best.get(r["date"])
                    if cur is None or r["score"] > cur[0]:
                        best[r["date"]] = (r["score"], k, r)
        rows = sorted(best.values(), key=lambda t: (-t[0], t[2]["date"]))[:n]
        out = []
        for sc, k, r in rows:
            w = r["best_window"]
            out.append(f'<tr><td class="mono">{fmtdate(r["date"], "%a, %b %-d, %Y")}</td><td>{esc(occ[k]["meta"]["label"].split(" · ")[0])}</td><td>{stars(r["stars"])}</td><td class="mono">{(w["start"]+"–"+w["end"]+" · "+w["hour"]+(" hour" if w["kind"]!="rising" else " rising")) if w else ""}</td><td class="why">{esc("; ".join(r["plus"][:3]))}</td></tr>')
        return f'<table class="tbl dates"><thead><tr><th>Date</th><th>For</th><th></th><th>Best window</th><th>Why</th></tr></thead><tbody>{"".join(out)}</tbody></table>'

    def transits_block(points, bodies=("Jupiter","Saturn","Uranus","Neptune","Pluto","Mars","Venus","Sun"), limit=40):
        rows = [h for h in ye["perfections"] if h["natal_point"] in points and h["transiting"] in bodies and h["aspect"] != "quincunx" or (h["natal_point"] in points and h["is_return"])]
        rows = rows[:limit]
        return '<table class="tbl transits"><thead><tr><th>When</th><th>Transit</th><th></th><th>Natal point</th><th>Pass</th><th>Sabian of the transit degree</th></tr></thead><tbody>' + "".join(
            f'<tr><td class="mono">{fmtdate(h["date"], "%a, %b %-d, %Y")}</td><td>{PG[h["transiting"]]} {h["transiting"]}{" ℞" if h["retrograde"] else ""} at {esc(h["transit_pretty"])}</td><td class="asp" style="color:{ASP_COLOR.get(h["aspect"],"#555")}">{ASP_SYM.get(h["aspect"],"")} {h["aspect"]}</td><td>{PG.get(h["natal_point"],"")} {h["natal_point"]}{" — RETURN" if h["is_return"] else ""}</td><td class="soft">{h["pass_label"]}</td><td class="sab">{esc(h["sabian"]["label"])}: {esc(h["sabian"]["image"] or "")}</td></tr>'
            for h in rows) + "</tbody></table>"

    def domain(key, title, keys, points, color):
        rd = R.get(key, {})
        hand_dates = ""
        if rd.get("dates"):
            hand_dates = '<div class="handpicked"><h4>Hand-picked dates</h4><ul>' + "".join(
                f'<li><span class="mono">{fmtdate(d["date"], "%a, %b %-d, %Y")}</span> · <strong>{esc(d["label"])}</strong><br><span class="soft">{d["why"]}</span></li>' for d in rd["dates"]) + "</ul></div>"
        return f'''<section class="domain" id="{key}" style="--dom:{color}">
<div class="section-head"><span class="eyebrow">{esc(title)}</span><h2>{esc(rd.get("title") or title)}</h2>{f'<p class="lede">{rd["lede"]}</p>' if rd.get("lede") else ""}</div>
<div class="prose">{paras(rd.get("body"))}</div>
{hand_dates}
<h4>The engine's best days for {esc(title.lower())}</h4>{top_dates_block(keys)}
<details class="more"><summary>Every exact transit to your {esc(title.lower())} points this year</summary>{transits_block(points)}</details>
</section>'''

    money_pts = {"Jupiter","Mercury","Venus","Lot of Fortune"} | {p for p, e in natal["planets"].items() if e and e.get("house") == 2}
    career_pts = {"MC","Sun","Saturn"} | {p for p, e in natal["planets"].items() if e and e.get("house") == 10}
    love_pts = {"Venus","Moon","DSC"} | {p for p, e in natal["planets"].items() if e and e.get("house") == 7}
    family_pts = {"Moon","IC"} | {p for p, e in natal["planets"].items() if e and e.get("house") in (4, 5)}
    body_pts = {"ASC","Mars","Sun","Moon"} | {p for p, e in natal["planets"].items() if e and e.get("house") in (1, 6)}
    home_pts = {"IC","Moon"} | {p for p, e in natal["planets"].items() if e and e.get("house") == 4}

    domains_html = "\n".join([
        domain("money", "Money", ["ask_money","sign_contract","invest","launch_sell","debt_budget"], money_pts, "#7a5f24"),
        domain("career", "Career", ["apply","interview","send_email","publish","network","start_build"], career_pts, "#3d5c3a"),
        domain("love", "Love", ["date_night","hard_talk"], love_pts, "#7a2848"),
        domain("family", "Family", ["family_gather","kids"], family_pts, "#2a3d52"),
        domain("body_spirit", "Body & Spirit", ["fitness_start","diet_start","beauty","rest_retreat","ritual","vision"], body_pts, "#5b4a7a"),
        domain("home", "Home", ["declutter","big_purchase","travel"], home_pts, "#2f6b6b"),
    ])

    # ---------- calendar of the sky
    lun_rows = "".join(
        f'<tr class="{"ecl" if l["eclipse"] else ""}"><td>{moon_glyph(l["kind"])}</td><td class="mono">{esc(l["pretty"])}</td><td><strong>{l["kind"].title()} Moon</strong>{(" · <span class=eclipse>" + l["eclipse"]["type"] + " " + l["eclipse"]["kind"] + " eclipse</span>") if l["eclipse"] else ""}</td><td class="mono">{esc(l["moon_pretty"])}</td><td>{ORD(l["natal_house"])} natal · {ORD(l["sr_house"])} return</td><td class="sab">{esc(l["sabian"]["label"])}: {esc(l["sabian"]["image"] or "")}</td></tr>'
        for l in ye["lunations"] if l["kind"] in ("new", "full"))
    st_rows = "".join(
        f'<tr><td class="mono">{esc(s["pretty"])}</td><td>{PG[s["body"]]} <strong>{s["body"]}</strong> stations {s["type"]}</td><td class="mono">{esc(s["pretty_lon"])}</td><td>{ORD(s["natal_house"])} house</td><td class="sab">{esc(s["sabian"]["label"])}: {esc(s["sabian"]["image"] or "")}</td></tr>'
        for s in ye["stations"])
    sh_rows = "".join(
        f'<tr><td class="mono">{esc(fmtdate(sh["pre_shadow_start"], "%b %-d")) if sh.get("pre_shadow_start") else "—"}</td><td class="mono">{esc(fmtdate(sh["retro_station"], "%b %-d, %Y"))} · {esc(sh["retro_lon"])}</td><td class="mono">{esc(fmtdate(sh["direct_station"], "%b %-d, %Y")) if sh.get("direct_station") else "—"} · {esc(sh.get("direct_lon",""))}</td><td class="mono">{esc(fmtdate(sh["post_shadow_end"], "%b %-d")) if sh.get("post_shadow_end") else "—"}</td></tr>'
        for sh in ye["mercury_shadows"])
    ing_rows = "".join(
        f'<tr><td class="mono">{esc(i["pretty"])}</td><td>{PG[i["body"]]} {i["body"]}{" ℞" if i["retrograde"] else ""} enters {GLYPH[i["sign"]]} <strong>{i["sign"]}</strong></td><td>your {ORD(i["natal_house"])} house · return {ORD(i["sr_house"])}</td></tr>'
        for i in ye["ingresses"])
    sens_rows = "".join(
        f'<tr><td class="mono">{fmtdate(w["start"], "%b %-d, %Y")} → {fmtdate(w["end"], "%b %-d, %Y")}</td><td>{PG[w["body"]]} {w["body"]} in {w["sign"]}</td><td>{esc(w["zone"])}</td><td class="mono">{w["days"]} days</td></tr>'
        for w in ye["sensitive_windows"])
    slow_rows = "".join(
        f'<tr><td class="mono">{fmtdate(w["start"], "%b %-d, %Y")} → {fmtdate(w["end"], "%b %-d, %Y")}</td><td>{PG[w["transiting"]]} {w["transiting"]} <span class="asp" style="color:{ASP_COLOR.get(w["aspect"],"#555")}">{ASP_SYM.get(w["aspect"],"")} {w["aspect"]}</span> natal {PG.get(w["natal_point"],"")} {w["natal_point"]}</td><td class="mono">{w["days"]} days within 1°</td></tr>'
        for w in ye["slow_windows"] if w["aspect"] != "quincunx")

    # ---------- chapters (month by month)
    chapters_html = []
    for ch in R.get("chapters", []):
        a, b = ch["range"].split("..")
        evs = []
        for l in ye["lunations"]:
            if a <= l["local"][:10] <= b and l["kind"] in ("new","full"):
                evs.append((l["local"][:10], f'{moon_glyph(l["kind"], 14)} {l["kind"].title()} Moon {esc(l["moon_pretty"])}{" — <em>" + l["eclipse"]["type"] + " " + l["eclipse"]["kind"] + " eclipse</em>" if l["eclipse"] else ""} · your {ORD(l["natal_house"])}'))
        for s in ye["stations"]:
            if a <= s["local"][:10] <= b: evs.append((s["local"][:10], f'{PG[s["body"]]} {s["body"]} stations {s["type"]} at {esc(s["pretty_lon"])}'))
        for i in ye["ingresses"]:
            if a <= i["local"][:10] <= b and i["body"] in ("Jupiter","Saturn","Mars","Venus","Uranus","Neptune","Pluto"): evs.append((i["local"][:10], f'{PG[i["body"]]} {i["body"]} enters {i["sign"]} (your {ORD(i["natal_house"])})'))
        for h in ye["perfections"]:
            if a <= h["date"] <= b and (h["transiting"] in ("Jupiter","Saturn","Uranus","Neptune","Pluto") and h["aspect"] != "quincunx" or h["is_return"]):
                evs.append((h["date"], f'{PG[h["transiting"]]} {h["transiting"]} {ASP_SYM.get(h["aspect"],"")} natal {h["natal_point"]}{" — RETURN" if h["is_return"] else ""} <span class="soft">({h["pass_label"]})</span>'))
        evs.sort()
        ev_html = "".join(f'<li><span class="mono">{fmtdate(d, "%b %-d")}</span> {t}</li>' for d, t in evs)
        # best + hold days of the month by the overall score
        month_days = [r for r in data["overall"] if a <= r["date"] <= b]
        best = sorted(month_days, key=lambda r: -r["score"])[:4]; hold = sorted(month_days, key=lambda r: r["score"])[:2]
        bh = ('<div class="bh"><div><span class="lab gold">Golden days</span> ' + ", ".join(f'<span class="mono">{fmtdate(r["date"], "%b %-d")}</span>' for r in sorted(best, key=lambda r: r["date"])) +
              '</div><div><span class="lab hold">Hold days</span> ' + ", ".join(f'<span class="mono">{fmtdate(r["date"], "%b %-d")}</span>' for r in sorted(hold, key=lambda r: r["date"])) + '</div></div>')
        chapters_html.append(f'''<article class="chapter"><div class="chapter-head"><h3>{esc(ch["title"])}</h3><div class="range mono">{fmtdate(a, "%b %-d, %Y")} → {fmtdate(b, "%b %-d, %Y")}</div></div>
<div class="chapter-grid"><div class="prose">{paras(ch.get("body"))}</div><aside class="chapter-side"><h4>In the sky</h4><ul class="evlist">{ev_html}</ul>{bh}</aside></div></article>''')

    # ---------- golden / hold
    gold = sorted(data["overall"], key=lambda r: r["rank"])[:24]
    hold = sorted(data["overall"], key=lambda r: -r["rank"])[:12]
    def why_overall(dte):
        d = days[day_index[dte]]
        bits = [f'Moon in {d["moon"]["sign"]}, {d["moon"]["phase_name"].lower()}']
        if d["retro"]: bits.append(", ".join(d["retro"]) + " retrograde")
        if d["eclipse_near"]: bits.append(f'{d["eclipse_near"]} eclipse near')
        if d["moon"]["voc_share"] >= 0.3: bits.append(f'void {int(d["moon"]["voc_share"]*100)}% of the day')
        tight = [c for c in d["contacts"] if c["orb"] <= 1.0 and c["t"] in ("Sun","Venus","Jupiter","Mars","Saturn") and c["a"] != "quincunx"]
        for c in tight[:2]: bits.append(f'{c["t"]} {c["a"]} natal {c["p"]}')
        return "; ".join(bits)
    gold_rows = "".join(f'<tr><td class="mono">#{r["rank"]}</td><td class="mono">{fmtdate(r["date"], "%a, %b %-d, %Y")}</td><td><span class="bar" style="width:{r["score"]}%"></span> {r["score"]:.0f}</td><td class="why">{esc(why_overall(r["date"]))}</td></tr>' for r in gold)
    hold_rows = "".join(f'<tr><td class="mono">#{r["rank"]}</td><td class="mono">{fmtdate(r["date"], "%a, %b %-d, %Y")}</td><td><span class="bar hold" style="width:{max(r["score"],2)}%"></span> {r["score"]:.0f}</td><td class="why">{esc(why_overall(r["date"]))}</td></tr>' for r in hold)

    # ---------- occasion nav
    groups = {}
    for k, o in occ.items(): groups.setdefault(o["meta"]["group"], []).append((k, o["meta"]["label"]))
    occ_nav = "".join(f'<div class="occ-group"><div class="occ-glabel">{g}</div>' + "".join(f'<button class="occ-btn" data-key="{k}">{esc(l.split(" · ")[0])}</button>' for k, l in items) + '</div>' for g, items in groups.items())

    css = CSS
    page = TEMPLATE
    repl = {
        "%%TITLE%%": esc(R.get("title") or f"Solar Return {year} · {name}"),
        "%%SUBTITLE%%": R.get("subtitle") or f"The year from {fmtdate(days[0]['date'], '%B %-d, %Y')} to {fmtdate(days[-1]['date'], '%B %-d, %Y')}",
        "%%DEDICATION%%": R.get("dedication") or "",
        "%%NAME%%": esc(name), "%%FIRST%%": esc(first_name),
        "%%MOMENT%%": esc(sr["local_pretty"]), "%%PLACE%%": esc(sr.get("place") or data["order"].get("place") or ""),
        "%%CONSTELLATION%%": constellation_svg(sr),
        "%%HERO_STATS%%": "".join(f'<div class="stat"><div class="k">{esc(k)}</div><div class="v">{v}</div></div>' for k, v in hero_stats),
        "%%SABIANS%%": "".join(f'<div class="sab-card"><div class="k">{lab}</div><div class="deg">{esc(e["sabian"]["label"])}</div><div class="img">{esc(e["sabian"]["image"] or "")}</div>{("<div class=refl>" + esc(e["sabian"]["reflection"]) + "</div>") if e["sabian"].get("reflection") else ""}</div>'
                          for lab, e in (("Return Ascendant", sr["asc"]), ("Return Midheaven", sr["mc"]), ("Return Sun", sr["planets"]["Sun"]), ("Return Moon", sr["planets"]["Moon"]))),
        "%%PLANETARY_HOUR%%": f'{sr["planetary_day"]}\'s day · {sr["planetary_hour"]["ruler"]}\'s hour ({sr["planetary_hour"]["start"][11:]}–{sr["planetary_hour"]["end"][11:]})',
        "%%OVERTURE%%": paras(R.get("overture")),
        "%%CHART_ARGUMENT%%": paras(R.get("chart_argument")),
        "%%BIWHEEL%%": biwheel(sr, natal, ov),
        "%%ASPGRID%%": aspect_grid(sr),
        "%%SR_TABLE%%": sr_table, "%%NATAL_TABLE%%": natal_table,
        "%%SN_ROWS%%": sn_rows, "%%SR_ASP_ROWS%%": sr_asp_rows,
        "%%ANGULAR%%": ", ".join(f'{PG[p]} {p} ({ORD(sr["planets"][p]["house"])})' for p in sr["angular_planets"]) or "none",
        "%%ON_ANGLE%%": ", ".join(f'{PG[o["planet"]]} {o["planet"]} on the {o["angle"]} ({o["orb"]:.1f}°)' for o in sr["on_angle"]) or "none within 6°",
        "%%BALANCE%%": " · ".join(f'{k} {v}' for k, v in sorted(sr["balance"]["element"].items(), key=lambda kv: -kv[1])) + " &nbsp;|&nbsp; " + " · ".join(f'{k} {v}' for k, v in sorted(sr["balance"]["mode"].items(), key=lambda kv: -kv[1])),
        "%%ROOMS%%": "\n".join(rooms),
        "%%DOMAINS%%": domains_html,
        "%%LUN_ROWS%%": lun_rows, "%%ST_ROWS%%": st_rows, "%%SH_ROWS%%": sh_rows, "%%ING_ROWS%%": ing_rows,
        "%%SENS_ROWS%%": sens_rows, "%%SLOW_ROWS%%": slow_rows,
        "%%ECLIPSES%%": paras(R.get("eclipses")),
        "%%CHAPTERS%%": "\n".join(chapters_html),
        "%%GOLD_ROWS%%": gold_rows, "%%HOLD_ROWS%%": hold_rows,
        "%%OCC_NAV%%": occ_nav,
        "%%CLOSING%%": paras(R.get("closing")),
        "%%SOURCES%%": "".join(f'<li>{s}</li>' for s in R.get("sources", [])),
        "%%ENGINE%%": esc(data["engine"]), "%%GENERATED%%": esc(data["generated"][:10]),
        "%%EXT_SIGN%%": data["electional_rule"]["external_rising"], "%%INT_SIGN%%": data["electional_rule"]["internal_rising"],
        "%%ORBS%%": ", ".join(f'{k} ≤{v}°' for k, v in data["orbs"].items()),
        "%%NEXT_RETURN%%": esc(data["next_return_local"]),
        "%%PAYLOAD%%": payload_json,
        "%%CSS%%": css, "%%JS%%": JS,
    }
    for k, v in repl.items():
        page = page.replace(k, v)
    return page

CSS = r"""
:root{--cream:#fbfaf7;--paper:#fff;--ink:#1d1d1f;--navy:#26355e;--gold:#a8863d;--gold-deep:#7a5f24;--gold-hi:#e6cf96;--gold-soft:#c9a55c;--line:#e4ddcf;--wash:#f4f0e6;--soft:#656b85;--berry:#9c4460;--serif:"Cormorant Garamond","Didot","Bodoni 72","Hoefler Text",Georgia,serif;--sans:"DM Sans",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;--mono:"DM Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box;margin:0;padding:0}
html{color-scheme:light only;-webkit-text-size-adjust:100%}
body{font-family:var(--sans);color:var(--ink);background:var(--cream);line-height:1.6;font-size:15.5px}
a{color:var(--gold-deep)}
.mast{background:radial-gradient(120% 140% at 50% 30%,#1f2b4e,#101830);color:#f3ecdd;text-align:center;padding:14px 16px 12px;border-bottom:1px solid rgba(201,165,92,.5)}
.mast .wordmark{font-family:var(--serif);letter-spacing:.2em;font-size:15px;color:#f3ecdd}
.mast .medal{display:inline-block;width:34px;height:34px;border:1px solid var(--gold-soft);border-radius:50%;font-family:var(--serif);font-size:13px;line-height:32px;color:var(--gold-hi);margin-bottom:6px;letter-spacing:.06em}
.mast .tag{font-family:var(--serif);font-style:italic;color:var(--gold-soft);font-size:13px;margin-top:2px}
nav.toc{position:sticky;top:0;z-index:20;background:rgba(251,250,247,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:8px 12px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
nav.toc a{color:var(--navy);text-decoration:none;padding:4px 8px;border-radius:6px}
nav.toc a:hover{background:var(--wash)}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px 60px}
.hero{position:relative;text-align:center;padding:54px 0 30px;overflow:hidden}
.hero .constellation{position:absolute;inset:0;width:100%;height:100%;opacity:.55;pointer-events:none}
.hero>*{position:relative}
.eyebrow{font-family:var(--sans);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold-deep)}
.hero h1{font-family:var(--serif);font-weight:400;font-size:clamp(38px,6.5vw,68px);line-height:1.02;color:var(--navy);margin:14px 0 8px}
.hero .sub{font-family:var(--serif);font-style:italic;font-size:clamp(18px,2.6vw,24px);color:var(--gold-deep)}
.hero .moment{margin-top:22px;font-family:var(--mono);font-size:13px;color:var(--soft);letter-spacing:.04em}
.hero .dedication{margin:26px auto 0;max-width:52ch;font-family:var(--serif);font-size:19px;font-style:italic;color:#3a3f55}
.rule{display:flex;align-items:center;gap:10px;margin:26px auto;width:min(420px,80%)}
.rule::before,.rule::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,transparent,var(--gold-soft),transparent)}
.rule .dot{width:5px;height:5px;border-radius:50%;background:var(--gold-soft)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:10px 0 30px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-align:left}
.stat .k{font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-deep)}
.stat .v{font-family:var(--serif);font-size:20px;color:var(--navy);margin-top:4px;line-height:1.25}
section{margin:54px 0}
.section-head{margin-bottom:18px}
.section-head h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4.2vw,44px);color:var(--navy);line-height:1.08;margin-top:6px}
.section-head .lede{font-family:var(--serif);font-size:20px;font-style:italic;color:#3a3f55;margin-top:8px;max-width:64ch}
.prose{max-width:70ch}
.prose p{margin:0 0 15px;font-size:16.5px;line-height:1.72;color:#2b2f3f}
.prose p.big:first-letter,.overture p:first-child:first-letter{font-family:var(--serif);font-size:3.6em;line-height:.85;float:left;padding:6px 8px 0 0;color:var(--gold)}
.prose strong{color:var(--navy)}
.prose em{color:#3a3f55}
.card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:22px}
.two{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:start}
@media(max-width:820px){.two{grid-template-columns:1fr}}
.biwheel{width:100%;max-width:680px;height:auto;display:block;margin:0 auto}
.aspgrid{width:100%;max-width:420px;height:auto;display:block;margin:0 auto}
.tbl{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--paper)}
.tbl th{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-deep);text-align:left;padding:9px 10px;border-bottom:1px solid var(--gold-soft);font-weight:600}
.tbl td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.tbl td.g{font-size:17px;color:var(--navy);width:28px}
.tbl .mono{font-family:var(--mono);font-size:12.5px;white-space:nowrap}
.tbl .soft{color:var(--soft)}
.tbl .sab{font-family:var(--serif);font-size:14.5px;color:#3a3f55;font-style:italic}
.tbl .asp{white-space:nowrap}
.tbl .why{color:#3a3f55;font-size:13px}
.tbl tr.ecl td{background:#fbf6ea}
.eclipse{color:var(--berry);font-weight:600}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--paper)}
.stars{color:var(--gold);letter-spacing:.05em;font-size:13px;white-space:nowrap}.stars .dim{color:#e4ddcf}
.sabs{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:18px 0}
.sab-card{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px}
.sab-card .k{font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-deep)}
.sab-card .deg{font-family:var(--serif);font-size:22px;color:var(--navy);margin:4px 0}
.sab-card .img{font-family:var(--serif);font-size:17px;font-style:italic;color:#2b2f3f;line-height:1.4}
.sab-card .refl{margin-top:8px;font-size:13px;color:var(--soft)}
.rooms{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.room{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:20px}
.room-head{display:flex;gap:14px;align-items:flex-start;margin-bottom:10px}
.roman{font-family:var(--serif);font-size:34px;color:var(--gold);line-height:1;min-width:44px}
.room h3{font-family:var(--serif);font-weight:400;font-size:23px;color:var(--navy);line-height:1.1}
.room-meta{font-size:12.5px;color:var(--soft);margin-top:3px}
.room-facts{display:block;font-size:13.5px;margin:10px 0 12px;padding:10px 12px;background:var(--wash);border-radius:10px}
.room-facts dd{margin:0 0 7px;color:#2b2f3f}
.room-facts dt{color:var(--gold-deep);font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding-top:2px}
.room p{font-size:15px;line-height:1.65;color:#2b2f3f;margin:0 0 10px}
.domain{border-top:1px solid var(--line);padding-top:36px}
.domain .eyebrow{color:var(--dom)}
.domain h4{font-family:var(--serif);font-weight:400;font-size:22px;color:var(--navy);margin:26px 0 10px}
.handpicked ul{list-style:none}
.handpicked li{padding:10px 0;border-bottom:1px solid var(--line);font-size:14.5px}
.handpicked li .mono{font-family:var(--mono);font-size:12.5px;color:var(--dom)}
details.more{margin-top:16px}
details.more summary{cursor:pointer;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-deep);padding:8px 0}
.moonglyph{vertical-align:middle}
.chapter{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:24px;margin-bottom:18px}
.chapter-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:14px}
.chapter h3{font-family:var(--serif);font-weight:400;font-size:28px;color:var(--navy)}
.chapter .range{font-family:var(--mono);font-size:12px;color:var(--soft)}
.chapter-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:22px}
@media(max-width:820px){.chapter-grid{grid-template-columns:1fr}}
.chapter-side h4{font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:8px}
.evlist{list-style:none;font-size:13px}
.evlist li{padding:5px 0;border-bottom:1px dotted var(--line);color:#2b2f3f}
.evlist .mono{font-family:var(--mono);font-size:11.5px;color:var(--soft);display:inline-block;min-width:52px}
.bh{margin-top:12px;font-size:13px;line-height:1.9}
.lab{font-size:10px;letter-spacing:.18em;text-transform:uppercase;padding:2px 7px;border-radius:5px;margin-right:6px}
.lab.gold{background:#f6ecd2;color:var(--gold-deep)}.lab.hold{background:#f7e3e8;color:var(--berry)}
.bar{display:inline-block;height:8px;background:linear-gradient(90deg,var(--gold-soft),var(--gold));border-radius:4px;vertical-align:middle;margin-right:6px;max-width:120px}
.bar.hold{background:linear-gradient(90deg,#e6c4cf,var(--berry))}
/* year ring */
.ring-wrap{display:grid;grid-template-columns:1fr 300px;gap:20px;align-items:start}
@media(max-width:820px){.ring-wrap{grid-template-columns:1fr}}
#yearring{width:100%;height:auto;display:block}
.ring-info{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px;font-size:13.5px;min-height:200px}
.ring-info h4{font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin-bottom:6px}
.ring-info .k{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-top:10px}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--soft);margin-top:10px}
.legend span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle;background:var(--lc)}
/* occasions */
.occ-nav{display:flex;flex-wrap:wrap;gap:14px 26px;margin:14px 0 18px}
.occ-glabel{font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:6px}
.occ-btn{display:block;background:var(--paper);border:1px solid var(--line);border-radius:999px;padding:6px 12px;margin:0 6px 6px 0;font-size:13px;cursor:pointer;color:var(--navy);font-family:var(--sans)}
.occ-btn.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.occ-panel{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:22px}
.occ-panel h3{font-family:var(--serif);font-weight:400;font-size:30px;color:var(--navy)}
.occ-panel .notes{font-family:var(--serif);font-style:italic;font-size:17px;color:#3a3f55;margin:6px 0 12px}
.occ-panel .pts{font-size:12.5px;color:var(--soft);margin-bottom:14px}
.heat{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;align-items:center;font-size:12px;margin:14px 0}
.heat .mlab{font-family:var(--serif);color:var(--navy);font-size:15px;width:36px}
.heat .row{display:grid;grid-template-columns:repeat(31,1fr);gap:2px}
.heat .cell{aspect-ratio:1;border-radius:3px;background:var(--wash);cursor:pointer;position:relative}
.heat .cell.sel{outline:2px solid var(--navy)}
.topn{list-style:none;counter-reset:n}
.topn li{display:grid;grid-template-columns:34px 150px 1fr;gap:10px;padding:10px 0;border-bottom:1px solid var(--line);font-size:13.5px;align-items:start}
.topn li .n{font-family:var(--serif);font-size:22px;color:var(--gold);line-height:1}
.topn li .d{font-family:var(--mono);font-size:12.5px;color:var(--navy)}
.topn li .w{color:var(--gold-deep);font-family:var(--mono);font-size:12px}
.topn li .why{color:#2b2f3f}.topn li .why .neg{color:var(--berry)}
.all-table{max-height:520px;overflow:auto;border:1px solid var(--line);border-radius:12px}
.all-table table{font-size:12.5px}
.all-table th{position:sticky;top:0;background:var(--paper);cursor:pointer}
.pill{display:inline-block;font-size:10.5px;letter-spacing:.1em;padding:1px 7px;border-radius:999px;background:var(--wash);color:var(--gold-deep)}
.ledger td{font-size:12.5px}
.method p{font-size:14.5px;color:#3a3f55;max-width:74ch;margin-bottom:10px}
.sources li{font-size:13px;color:#3a3f55;margin-bottom:4px}
footer{border-top:1px solid var(--line);margin-top:60px;padding:24px 0;font-size:12px;color:var(--soft);text-align:center;font-family:var(--serif);font-style:italic}
@media print{nav.toc,.occ-nav,.all-table,.ring-wrap{display:none}section{break-inside:avoid-page}body{font-size:12px}.hero{padding-top:20px}}
"""

JS = r"""
const D = window.__SR__;
const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const fmt = iso => { const [y,m,d] = iso.split("-").map(Number); const dt = new Date(y, m-1, d); return dt.toLocaleDateString("en-US",{weekday:"short",month:"short",day:"numeric",year:"numeric"}); };
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function goldColor(score){ // 0..100 -> wash .. deep gold
  const t = Math.max(0, Math.min(1, score/100));
  const a = [244,240,230], b = [122,95,36];
  const c = a.map((v,i)=>Math.round(v+(b[i]-v)*Math.pow(t,1.35)));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
let current = Object.keys(D.occ)[0];
// ---------- year ring
const ring = document.getElementById("yearring");
const N = D.days.length, cx = 360, cy = 360, R0 = 236, R1 = 300;
function angle(i){ return -Math.PI/2 + (i/N)*2*Math.PI; }
function pt(i, r){ const a = angle(i); return [cx + r*Math.cos(a), cy + r*Math.sin(a)]; }
function drawRing(){
  let s = "";
  // month labels + separators
  const mcount = {}; D.days.forEach(d=>{ const k=d.d.slice(0,7); mcount[k]=(mcount[k]||0)+1; });
  D.days.forEach((d,i)=>{ if(d.d.slice(8,10)==="01"||i===0){ const [x1,y1]=pt(i,R0-6),[x2,y2]=pt(i,R1+4); s += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#a8863d" stroke-width="0.8"/>`;
      const k = d.d.slice(0,7); if(mcount[k] < 12) return; const mi = Number(d.d.slice(5,7))-1; const [lx,ly] = pt(i+mcount[k]/2, R1+18); s += `<text x="${lx}" y="${ly}" font-size="11" text-anchor="middle" dominant-baseline="central" fill="#7a5f24" letter-spacing="1.5" font-family="Cormorant Garamond,Georgia,serif">${MONTHS[mi].toUpperCase()} ${d.d.slice(0,4)}</text>`; } });
  const occ = D.occ[current];
  D.days.forEach((d,i)=>{
    const sc = occ.days[i][0]; const a0 = angle(i), a1 = angle(i+1); const r0 = R0, r1 = R0 + 14 + (R1-R0-14)*sc/100;
    const p = [ [cx+r0*Math.cos(a0), cy+r0*Math.sin(a0)], [cx+r1*Math.cos(a0), cy+r1*Math.sin(a0)], [cx+r1*Math.cos(a1), cy+r1*Math.sin(a1)], [cx+r0*Math.cos(a1), cy+r0*Math.sin(a1)] ];
    s += `<path class="day" data-i="${i}" d="M ${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)} L ${p[1][0].toFixed(1)} ${p[1][1].toFixed(1)} L ${p[2][0].toFixed(1)} ${p[2][1].toFixed(1)} L ${p[3][0].toFixed(1)} ${p[3][1].toFixed(1)} Z" fill="${goldColor(sc)}" stroke="#fff" stroke-width="0.4"><title>${fmt(d.d)} · ${occ.meta.label.split(" · ")[0]} · score ${sc} · rank #${occ.days[i][1]}</title></path>`;
  });
  // event markers inside the ring
  const idx = {}; D.days.forEach((d,i)=>idx[d.d]=i);
  D.events.lunations.forEach(l=>{ const i = idx[l.d]; if(i===undefined) return; const [x,y] = pt(i, R0-16);
    if(l.k==="new"||l.k==="full"){ s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${l.ecl?5.5:3.6}" fill="${l.k==="full"?"#f3e3b3":"#26355e"}" stroke="${l.ecl?"#9c4460":"#a8863d"}" stroke-width="${l.ecl?1.6:0.8}"><title>${l.k} Moon ${l.deg}${l.ecl?" — "+l.ecl+" "+l.kind_e+" eclipse":""} · ${fmt(l.d)}</title></circle>`; } });
  D.events.stations.forEach(st=>{ const i = idx[st.d]; if(i===undefined) return; const [x,y] = pt(i, R0-32);
    s += `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="9" text-anchor="middle" dominant-baseline="central" fill="${st.t==="retrograde"?"#9c4460":"#3d5c3a"}">${({Mercury:"☿",Venus:"♀",Mars:"♂",Jupiter:"♃",Saturn:"♄",Uranus:"♅",Neptune:"♆",Pluto:"♇"})[st.b]}${st.t==="retrograde"?"℞":"D"}<title>${st.b} stations ${st.t} at ${st.deg} · ${fmt(st.d)}</title></text>`; });
  D.events.returns.forEach(r=>{ const i = idx[r.d]; if(i===undefined) return; const [x,y] = pt(i, R0-48);
    s += `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${r.b==="Jupiter"?15:11}" text-anchor="middle" dominant-baseline="central" fill="#a8863d">✦<title>${r.b} Return (${r.p}) · ${fmt(r.d)}</title></text>`; });
  s += `<text x="${cx}" y="${cy-14}" text-anchor="middle" font-size="12" letter-spacing="3" fill="#7a5f24" font-family="Cormorant Garamond,Georgia,serif">THE YEAR</text>`;
  s += `<text x="${cx}" y="${cy+8}" text-anchor="middle" font-size="18" fill="#26355e" font-family="Cormorant Garamond,Georgia,serif" font-style="italic">${esc(occ.meta.label.split(" · ")[0])}</text>`;
  s += `<text x="${cx}" y="${cy+28}" text-anchor="middle" font-size="10.5" fill="#656b85" font-family="DM Sans,sans-serif">taller and deeper gold = better day</text>`;
  ring.innerHTML = s;
  ring.querySelectorAll(".day").forEach(el=>{ el.addEventListener("mouseenter", ()=>showDay(Number(el.dataset.i))); el.addEventListener("click", ()=>{ showDay(Number(el.dataset.i)); selectHeat(Number(el.dataset.i)); }); });
}
function showDay(i){
  const d = D.days[i]; const o = D.occ[current].days[i]; const ov = D.overall[d.d] || [0,0];
  const box = document.getElementById("ringinfo");
  box.innerHTML = `<h4>${fmt(d.d)}</h4>
    <div><strong>${esc(D.occ[current].meta.label.split(" · ")[0])}</strong>: score ${o[0]} · rank #${o[1]} of ${N} · ${"★".repeat(o[2])}<span style="color:#e4ddcf">${"★".repeat(5-o[2])}</span></div>
    ${o[3]?`<div class="k">Best window</div><div>${esc(o[3])}</div>`:""}
    <div class="k">Why</div><div>${o[4].map(x=>"+ "+esc(x)).join("<br>")}${o[5].length?"<br><span style='color:#9c4460'>"+o[5].map(x=>"− "+esc(x)).join("<br>")+"</span>":""}</div>
    <div class="k">The Moon</div><div>${d.moon} · ${d.mp} (${d.il}%) · your ${d.mh}${ordSfx(d.mh)} house${d.voc.length?"<br>void "+d.voc.map(v=>v[0]+"–"+v[1]).join(", "):""}</div>
    <div class="k">Rising windows</div><div>${D.rule.external_rising}: ${(d.win[D.rule.external_rising]||[]).map(w=>w[0]+"–"+w[1]).join(", ")||"—"}<br>${D.rule.internal_rising}: ${(d.win[D.rule.internal_rising]||[]).map(w=>w[0]+"–"+w[1]).join(", ")||"—"}</div>
    <div class="k">Day</div><div>${d.dr}'s day${d.rx.length?" · "+d.rx.join(", ")+" ℞":""}${d.sh?" · Mercury shadow":""}${d.ecl?" · <span style='color:#9c4460'>"+d.ecl+" eclipse near</span>":""} · overall day score ${ov[0]} (#${ov[1]})</div>`;
}
function ordSfx(n){ return (n%100>=11&&n%100<=13)?"th":({1:"st",2:"nd",3:"rd"})[n%10]||"th"; }
// ---------- occasion panel
function renderOcc(){
  const occ = D.occ[current]; const meta = occ.meta;
  document.querySelectorAll(".occ-btn").forEach(b=>b.classList.toggle("on", b.dataset.key===current));
  const rows = occ.days.map((r,i)=>({i, score:r[0], rank:r[1], stars:r[2], win:r[3], plus:r[4], minus:r[5], d:D.days[i].d}));
  const top = rows.slice().sort((a,b)=>a.rank-b.rank).slice(0,12);
  let html = `<h3>${esc(meta.label)}</h3><div class="notes">${esc(meta.notes)}</div>
  <div class="pts"><span class="pill">${meta.kind==="external"?D.rule.external_rising+" rising · worldly":D.rule.internal_rising+" rising · inner"}</span> &nbsp; Natal points weighed: ${meta.points.join(", ")} · Moon applies to ${meta.benefics.join("/")} · avoids ${meta.malefics.join("/")}${meta.phase?" · "+meta.phase+" Moon":""} · days of ${meta.day_rulers.join(", ")}</div>`;
  // heat calendar
  const months = {}; D.days.forEach((d,i)=>{ const k = d.d.slice(0,7); (months[k]=months[k]||[]).push(i); });
  html += `<div class="heat">`;
  Object.keys(months).forEach(k=>{ const [y,m] = k.split("-"); html += `<div class="mlab">${MONTHS[Number(m)-1]}<span style="font-size:10px;color:#656b85"> ’${y.slice(2)}</span></div><div class="row">`;
    const first = Number(D.days[months[k][0]].d.slice(8,10));
    for(let b=1;b<first;b++) html += `<div></div>`;
    months[k].forEach(i=>{ const r = rows[i]; html += `<div class="cell" data-i="${i}" style="background:${goldColor(r.score)}" title="${fmt(r.d)} · ${r.score} · #${r.rank}"></div>`; });
    html += `</div>`; });
  html += `</div>`;
  html += `<h4 style="font-family:var(--serif);font-weight:400;font-size:22px;color:#26355e;margin:18px 0 8px">The twelve best days of the year</h4><ol class="topn">` + top.map(r=>`<li><span class="n">${r.rank}</span><div><div class="d">${fmt(r.d)}</div><div class="w">${esc(r.win||"")}</div></div><div class="why">${r.plus.map(esc).join(" · ")}${r.minus.length?` <span class="neg">· but ${r.minus.map(esc).join(", ")}</span>`:""}</div></li>`).join("") + `</ol>`;
  html += `<details style="margin-top:14px"><summary style="cursor:pointer;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#7a5f24">All ${N} days, ranked (click a header to sort)</summary><div class="all-table"><table class="tbl" id="alltable"><thead><tr><th data-s="rank">Rank</th><th data-s="date">Date</th><th data-s="score">Score</th><th>Window</th><th>Why</th></tr></thead><tbody></tbody></table></div></details>`;
  document.getElementById("occpanel").innerHTML = html;
  document.querySelectorAll(".heat .cell").forEach(c=>{ c.addEventListener("mouseenter",()=>showDay(Number(c.dataset.i))); c.addEventListener("click",()=>{showDay(Number(c.dataset.i)); selectHeat(Number(c.dataset.i));}); });
  let sortKey = "rank";
  const fill = ()=>{ const sorted = rows.slice().sort((a,b)=> sortKey==="date"? a.d.localeCompare(b.d) : sortKey==="score" ? b.score-a.score : a.rank-b.rank);
    document.querySelector("#alltable tbody").innerHTML = sorted.map(r=>`<tr><td class="mono">#${r.rank}</td><td class="mono">${fmt(r.d)}</td><td><span class="bar" style="width:${Math.max(r.score,2)*0.9}px"></span>${r.score}</td><td class="mono" style="white-space:normal">${esc(r.win||"")}</td><td class="why">${r.plus.map(esc).join("; ")}${r.minus.length?` <span style="color:#9c4460">(${r.minus.map(esc).join("; ")})</span>`:""}</td></tr>`).join(""); };
  fill();
  document.querySelectorAll("#alltable th[data-s]").forEach(th=>th.addEventListener("click",()=>{ sortKey = th.dataset.s; fill(); }));
  drawRing();
}
function selectHeat(i){ document.querySelectorAll(".heat .cell").forEach(c=>c.classList.toggle("sel", Number(c.dataset.i)===i)); }
document.querySelectorAll(".occ-btn").forEach(b=>b.addEventListener("click",()=>{ current = b.dataset.key; renderOcc(); }));
// ---------- ledger
(function(){ const tb = document.querySelector("#ledger tbody"); if(!tb) return;
  tb.innerHTML = D.days.map((d,i)=>{ const ov = D.overall[d.d]||[0,0]; return `<tr><td class="mono">${fmt(d.d)}</td><td>${d.moon}<br><span style="color:#656b85">${d.mp} ${d.il}% · your ${d.mh}${ordSfx(d.mh)}</span></td><td>${d.voc.length?d.voc.map(v=>v[0]+"–"+v[1]).join("<br>"):"—"}</td><td>${d.dr}</td><td class="mono">${(d.win[D.rule.external_rising]||[]).map(w=>w[0]+"–"+w[1]).join("<br>")||"—"}</td><td class="mono">${(d.win[D.rule.internal_rising]||[]).map(w=>w[0]+"–"+w[1]).join("<br>")||"—"}</td><td>${d.rx.length?d.rx.join(", ")+" ℞":""}${d.sh?"<br>Mercury shadow":""}${d.ecl?"<br><span style='color:#9c4460'>"+d.ecl+" eclipse</span>":""}</td><td><span class="bar" style="width:${Math.max(ov[0],2)*0.8}px"></span>${ov[0]}</td></tr>`; }).join("");
})();
renderOcc(); showDay(0);
"""

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>%%TITLE%%</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>%%CSS%%</style>
</head>
<body>
<div class="mast"><div class="medal">XII</div><div class="wordmark">THE TWELVE ROOMS</div><div class="tag">The whole sky, written for you.</div></div>
<nav class="toc"><a href="#moment">The moment</a><a href="#chart">The chart</a><a href="#rooms">Twelve rooms</a><a href="#money">Money</a><a href="#career">Career</a><a href="#love">Love</a><a href="#family">Family</a><a href="#body_spirit">Body & spirit</a><a href="#home">Home</a><a href="#sky">The sky's calendar</a><a href="#chapters">Twelve chapters</a><a href="#elections">Elections</a><a href="#golden">Golden days</a><a href="#ledger">Ledger</a><a href="#method">Method</a></nav>
<main class="wrap">

<header class="hero" id="moment">
%%CONSTELLATION%%
<div class="eyebrow">A solar return · year book</div>
<h1>%%TITLE%%</h1>
<div class="sub">%%SUBTITLE%%</div>
<div class="moment">%%MOMENT%% · %%PLACE%%<br>%%PLANETARY_HOUR%%</div>
<div class="dedication">%%DEDICATION%%</div>
<div class="rule"><span class="dot"></span></div>
</header>

<div class="stats">%%HERO_STATS%%</div>

<section class="overture">
<div class="section-head"><span class="eyebrow">I · The moment</span><h2>The Sun comes home</h2></div>
<div class="prose">%%OVERTURE%%</div>
<div class="sabs">%%SABIANS%%</div>
</section>

<section id="chart">
<div class="section-head"><span class="eyebrow">II · The chart</span><h2>The return, laid over the birth</h2><p class="lede">Outer ring: the sky at the moment of return. Inner ring: the sky you were born under. Houses counted from the return Ascendant, one sign per house.</p></div>
<div class="two">
<div class="card">%%BIWHEEL%%</div>
<div>
<div class="prose">%%CHART_ARGUMENT%%</div>
<div class="card" style="margin-top:14px;font-size:13.5px"><div class="eyebrow">Angular</div><div>%%ANGULAR%%</div><div class="eyebrow" style="margin-top:10px">On an angle</div><div>%%ON_ANGLE%%</div><div class="eyebrow" style="margin-top:10px">Balance</div><div>%%BALANCE%%</div></div>
</div>
</div>
<h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:30px 0 10px">Positions of the return</h4>
<div class="scroll">%%SR_TABLE%%</div>
<div class="two" style="margin-top:22px">
<div><h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:0 0 10px">Return to natal, tightest first</h4><div class="scroll"><table class="tbl"><thead><tr><th>Return</th><th>Aspect</th><th>Natal</th><th>Orb</th><th></th></tr></thead><tbody>%%SN_ROWS%%</tbody></table></div></div>
<div><h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:0 0 10px">Inside the return chart</h4><div class="card">%%ASPGRID%%</div><div class="scroll" style="margin-top:12px"><table class="tbl"><thead><tr><th></th><th>Aspect</th><th></th><th>Orb</th></tr></thead><tbody>%%SR_ASP_ROWS%%</tbody></table></div></div>
</div>
<details class="more"><summary>Your natal chart, for reference</summary><div class="scroll">%%NATAL_TABLE%%</div></details>
</section>

<section id="rooms">
<div class="section-head"><span class="eyebrow">III · The twelve rooms of the year</span><h2>Where the year lives</h2><p class="lede">Each room is one house of the return chart: its sign, who is in it, where its ruler went, and which of your natal planets it holds.</p></div>
<div class="rooms">%%ROOMS%%</div>
</section>

%%DOMAINS%%

<section id="sky">
<div class="section-head"><span class="eyebrow">IX · The sky's calendar</span><h2>Lunations, eclipses, stations, ingresses</h2></div>
<div class="prose">%%ECLIPSES%%</div>
<h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:22px 0 10px">New and Full Moons</h4>
<div class="scroll"><table class="tbl"><thead><tr><th></th><th>When</th><th>Lunation</th><th>Degree</th><th>House</th><th>Sabian symbol</th></tr></thead><tbody>%%LUN_ROWS%%</tbody></table></div>
<h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:22px 0 10px">Stations</h4>
<div class="scroll"><table class="tbl"><thead><tr><th>When</th><th>Station</th><th>Degree</th><th>Your house</th><th>Sabian symbol</th></tr></thead><tbody>%%ST_ROWS%%</tbody></table></div>
<h4 style="font-family:var(--serif);font-weight:400;font-size:24px;color:var(--navy);margin:22px 0 10px">Mercury retrograde, with shadows</h4>
<div class="scroll"><table class="tbl"><thead><tr><th>Pre-shadow from</th><th>Stations retrograde</th><th>Stations direct</th><th>Post-shadow until</th></tr></thead><tbody>%%SH_ROWS%%</tbody></table></div>
<details class="more"><summary>Every ingress this year</summary><div class="scroll"><table class="tbl"><thead><tr><th>When</th><th>Ingress</th><th>House</th></tr></thead><tbody>%%ING_ROWS%%</tbody></table></div></details>
<details class="more"><summary>Slow transits within one degree of your natal points</summary><div class="scroll"><table class="tbl"><thead><tr><th>Window</th><th>Transit</th><th></th></tr></thead><tbody>%%SLOW_ROWS%%</tbody></table></div></details>
<details class="more"><summary>Sensitive-degree windows</summary><div class="scroll"><table class="tbl"><thead><tr><th>Window</th><th>Body</th><th>Zone</th><th></th></tr></thead><tbody>%%SENS_ROWS%%</tbody></table></div></details>
</section>

<section id="chapters">
<div class="section-head"><span class="eyebrow">X · The year in twelve chapters</span><h2>Month by month</h2></div>
%%CHAPTERS%%
</section>

<section id="elections">
<div class="section-head"><span class="eyebrow">XI · The elections</span><h2>Every day of the year, ranked for every occasion</h2><p class="lede">Choose an occasion. The ring and the calendar recolor; the twelve best days appear with their exact local windows, and every one of the year's days is listed underneath, ranked, with its reasons.</p></div>
<div class="occ-nav">%%OCC_NAV%%</div>
<div class="ring-wrap"><svg id="yearring" viewBox="0 0 720 720" role="img" aria-label="The year as a ring, each day colored by its score"></svg><div class="ring-info" id="ringinfo"></div></div>
<div class="legend"><span style="--lc:#26355e">New Moon</span><span style="--lc:#f3e3b3">Full Moon</span><span style="--lc:#9c4460">Eclipse ring</span><span style="--lc:#a8863d">✦ Planetary return</span><span style="--lc:#3d5c3a">℞ / D stations</span></div>
<div class="occ-panel" id="occpanel" style="margin-top:18px"></div>
<p class="prose" style="margin-top:12px;font-size:13px;color:var(--soft)">Windows follow the Ascendant rule: worldly matters when <strong>%%EXT_SIGN%%</strong> rises, inner work when <strong>%%INT_SIGN%%</strong> rises, narrowed to the planetary hour that fits the matter and to waking hours. Where the rising window falls at night, the best fitting daytime planetary hour is given instead.</p>
</section>

<section id="golden">
<div class="section-head"><span class="eyebrow">XII · Golden days and hold days</span><h2>The year's finest days, and the ones to sit out</h2><p class="lede">Averaged across every worldly occasion. Golden days are the ones to spend; hold days are for rest, drafts, and not signing anything.</p></div>
<div class="two">
<div class="scroll"><table class="tbl"><thead><tr><th></th><th>Golden day</th><th>Score</th><th>What's happening</th></tr></thead><tbody>%%GOLD_ROWS%%</tbody></table></div>
<div class="scroll"><table class="tbl"><thead><tr><th></th><th>Hold day</th><th>Score</th><th>What's happening</th></tr></thead><tbody>%%HOLD_ROWS%%</tbody></table></div>
</div>
</section>

<section id="ledger">
<div class="section-head"><span class="eyebrow">XIII · The ledger</span><h2>Every day, on one page</h2></div>
<details class="more"><summary>Open the 366-day ledger</summary><div class="scroll" style="max-height:600px;overflow:auto"><table class="tbl ledger" id="ledger"><thead><tr><th>Date</th><th>Moon</th><th>Void of course</th><th>Day of</th><th>%%EXT_SIGN%% rising</th><th>%%INT_SIGN%% rising</th><th>Retrograde</th><th>Day score</th></tr></thead><tbody></tbody></table></div></details>
</section>

<section id="method" class="method">
<div class="section-head"><span class="eyebrow">XIV · Method</span><h2>How this was made</h2></div>
<div class="prose">%%CLOSING%%</div>
<p><strong>Engine.</strong> %%ENGINE%%. Whole-sign houses throughout; the Ascendant and Midheaven kept as sensitive points by exact degree. The solar return is cast for the instant the Sun returns to its natal longitude, to the second, for the place named above. Sabian symbols round up to the next whole degree. Return-to-natal orbs: %%ORBS%%. Next return: %%NEXT_RETURN%%.</p>
<p><strong>Ranking.</strong> Each day is scored for each occasion from the Moon's phase, sign, and house, its void-of-course share of the working day, the Moon's exact applications that day, every transit in orb to the occasion's natal points (benefics soft, malefics hard, tighter is stronger), the day's mundane weather, retrogrades and shadows, eclipse proximity, the planetary day and hour, and the Ascendant rule. Scores are scaled 0–100 within each occasion and ranked; the "why" lists the strongest contributors. This ranks the sky against your chart; it does not replace preparation, and it is not advice about money, health, or law.</p>
<h4 style="font-family:var(--serif);font-weight:400;font-size:22px;color:var(--navy);margin:18px 0 8px">Sources for the current-sky color</h4>
<ul class="sources">%%SOURCES%%</ul>
<p style="margin-top:14px;font-size:12.5px;color:var(--soft)">Computed %%GENERATED%%. Birth data is used in memory to compute this page and is not stored anywhere else.</p>
</section>

</main>
<footer>The Twelve Rooms · a year book for %%FIRST%% · the whole sky, written for you.</footer>
<script>window.__SR__ = %%PAYLOAD%%;</script>
<script>%%JS%%</script>
</body>
</html>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--reading", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = json.load(open(a.data))
    reading = json.load(open(a.reading)) if a.reading else {}
    Path(a.out).write_text(build(data, reading))
    print(f"wrote {a.out} ({Path(a.out).stat().st_size/1e6:.2f} MB)")

if __name__ == "__main__":
    main()
