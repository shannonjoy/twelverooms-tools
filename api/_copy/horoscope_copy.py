"""Interpretation copy for the daily horoscope.

Hand-written (not a synced engine). The ephemeris decides WHAT is happening and
WHEN; this module decides how it reads. Two layers:

  1. CURATED — (aspect, natal point) lines for the combinations that carry a day.
  2. COMPOSED — a point phrase joined to an aspect frame, for everything else.

House rules, inherited from the Luna voice: calm, never alarmist, hard transits
named plainly and held gently. No fortune-telling, no fake precision. A
retrograde contact is a revisit, never a launch signal.
"""

POINT_PRETTY = {"ASC": "Ascendant", "MC": "Midheaven",
                "North Node": "North Node", "South Node": "South Node"}

# What surfaces when a transit touches this natal point. Written as a noun
# phrase so it can sit inside any aspect frame below.
POINT_FEEL = {
    "Sun":        "your sense of self, and what you are here to become",
    "Moon":       "your inner weather, and what you actually need",
    "Mercury":    "your thinking, your plans, and how you say things",
    "Venus":      "affection, taste, and what you value",
    "Mars":       "your drive, and how you take action",
    "Jupiter":    "your appetite for more, and where you look for meaning",
    "Saturn":     "your responsibilities, and the structures you have built",
    "Uranus":     "your need for room to be yourself",
    "Neptune":    "your imagination, and what you long for",
    "Pluto":      "your deepest motives, and what is being rebuilt",
    "Chiron":     "the old wound, and the skill it taught you",
    "North Node": "the direction you are growing toward",
    "South Node": "the habit you are ready to set down",
    "ASC":        "how you meet the world, and how you come across",
    "MC":         "your work, your calling, and your public role",
}

# The aspect's shape. {x} takes a POINT_FEEL phrase.
ASPECT_FRAME = {
    "conjunction": "{x} comes right to the surface.",
    "sextile":     "a small opening around {x} — modest effort, real return.",
    "square":      "friction around {x}; it asks for a choice, not a fix.",
    "trine":       "{x} moves without forcing.",
    "opposition":  "{x} pulls against something else and asks for balance.",
    "quincunx":    "{x} sits at an awkward angle — adjust rather than push.",
}

# How the aspect tends to feel, used for tone and for window logic.
FLOWING = {"trine", "sextile"}
HARD = {"square", "opposition"}
NEUTRAL = {"conjunction", "quincunx"}

GLYPH = {"Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀",
         "Mars": "♂", "Jupiter": "♃", "Saturn": "♄",
         "Uranus": "♅", "Neptune": "♆", "Pluto": "♇",
         "North Node": "☊", "South Node": "☋", "Chiron": "⚷",
         "ASC": "AC", "MC": "MC"}
ASPECT_GLYPH = {"conjunction": "☌", "sextile": "⚹", "square": "□",
                "trine": "△", "opposition": "☍", "quincunx": "⚻"}

# What each transiting body brings, for the composed non-Moon lines.
BODY_THEME = {
    "Sun":     "attention and vitality",
    "Mercury": "thinking and talk",
    "Venus":   "warmth, ease, and appetite",
    "Mars":    "drive and heat",
    "Jupiter": "expansion and permission",
    "Saturn":  "weight, testing, and structure",
    "Uranus":  "disruption and awakening",
    "Neptune": "softening and dissolving",
    "Pluto":   "pressure and deep change",
}

# ---- Layer 1: curated Moon lines, the spine of a day ----------------------
# Keyed (aspect, natal point). The Moon is the fastest body, so these are the
# lines a reader actually feels on the clock.
MOON_LINES = {
    ("conjunction", "Sun"):   "You and your own mood are in the same room. Whatever you are, you are it fully right now.",
    ("conjunction", "Moon"):  "Your monthly reset. Feelings run close to the surface and true — a good hour to notice what you need.",
    ("conjunction", "Mercury"): "Mind and mood speak the same language. Say the thing while it is clear.",
    ("conjunction", "Venus"): "Affection and comfort come easily. Good for warmth, food, beauty, someone you like.",
    ("conjunction", "Mars"):  "Feeling arrives with heat behind it. Useful for effort; watch the short fuse.",
    ("conjunction", "Saturn"): "A sober hour. Not sadness so much as gravity — take it as focus, not verdict.",
    ("conjunction", "Jupiter"): "Room to breathe. Generosity, appetite, and a wider view of the same problem.",
    ("conjunction", "ASC"):   "You are unusually legible right now. What you feel shows on the outside.",
    ("conjunction", "MC"):    "Feelings and work occupy the same seat. What you care about becomes visible.",

    ("square", "Sun"):        "A pull between what you want and what you need. Neither is wrong; pick one for now.",
    ("square", "Moon"):       "Restless. Something is out of step with your own rhythm — small adjustment, not overhaul.",
    ("square", "Mercury"):    "Words come out sharper or vaguer than intended. Reread before you send.",
    ("square", "Venus"):      "A small snag in comfort or affection. Ordinary friction; do not make it a referendum.",
    ("square", "Mars"):       "Irritability with somewhere to go. Move your body before you answer anyone.",
    ("square", "Saturn"):     "Heaviness with an early hour to it. It lifts. Do not make decisions from underneath it.",
    ("square", "Jupiter"):    "Wanting more than the hour can hold. Enjoy the appetite, right-size the plan.",
    ("square", "ASC"):        "You do not quite land the way you mean to. Slow the first sentence down.",
    ("square", "MC"):         "Work asks for one thing, your inner life another. The tension is the information.",

    ("trine", "Sun"):         "You are on your own side. Easy confidence, nothing to prove.",
    ("trine", "Moon"):        "Your own weather agrees with you. Rest lands, company lands.",
    ("trine", "Mercury"):     "Clear thinking with feeling behind it. Good for writing and honest conversation.",
    ("trine", "Venus"):       "Grace. Pleasure without guilt, connection without effort.",
    ("trine", "Mars"):        "Effort feels good. Do the physical thing you have been putting off.",
    ("trine", "Saturn"):      "Steady. Boring in the best way — good for the thing that needs patience.",
    ("trine", "Jupiter"):     "Ease and optimism return. A soft place to land a busy day.",
    ("trine", "ASC"):         "You come across well without managing it.",
    ("trine", "MC"):          "What you feel and what you do point the same way. Useful for visible work.",

    ("sextile", "Sun"):       "A door, slightly open. Step through and it stays open.",
    ("sextile", "Moon"):      "A kind hour, if you take it. Small comforts pay well.",
    ("sextile", "Mercury"):   "Ideas arrive in usable size. Write them down.",
    ("sextile", "Venus"):     "Reach out. Warmth offered now is received.",
    ("sextile", "Mars"):      "A window for the first small step. Momentum is cheap right now.",
    ("sextile", "Saturn"):    "Good for one dull, structural task. It will take less than you fear.",
    ("sextile", "Pluto"):     "Emotional depth and insight open up. Good for the honest conversation.",
    ("sextile", "MC"):        "A quiet opening in work. Send the message.",

    ("opposition", "Sun"):    "You see yourself from the outside for an hour. Uncomfortable, useful.",
    ("opposition", "Moon"):   "Full-feeling. Something reaches its own high-water mark and asks to be witnessed.",
    ("opposition", "Mercury"): "A conversation needs two sides today; leave room for the other one.",
    ("opposition", "Venus"):  "Wanting closeness and wanting space at once. Both are allowed.",
    ("opposition", "Mars"):   "Pushback. Meet it with steadiness rather than more force.",
    ("opposition", "Saturn"): "The limit shows itself plainly. Respect it and it stops arguing.",
    ("opposition", "ASC"):    "Other people are the mirror this hour. Listen to what comes back.",
    ("opposition", "MC"):     "Home and work stand opposite each other. Name which one you are choosing.",
}

# A few non-Moon curated lines, where the composed version would undersell it.
BODY_LINES = {
    ("Mars", "square", "MC"): "A hard push against your work and public role. Real drive to move something that has stalled — and a real risk of forcing it. Confidence runs high; if it turns to irritation, keep it out of the house.",
    ("Mars", "conjunction", "ASC"): "You arrive with heat. Excellent for effort, poor for diplomacy.",
    ("Venus", "square", "Neptune"): "Judgement softens where it should stay clear. Enjoy the mood; do not sign anything to it.",
    ("Saturn", "conjunction", "Sun"): "Weight on your own name. Slow, clarifying, and not a punishment.",
    ("Jupiter", "trine", "Sun"): "The sky is on your side. Ask for the thing.",
}


def pretty(point):
    return POINT_PRETTY.get(point, point)


def headline(body, aspect, point):
    """'Moon square your Midheaven' — plain, no jargon stacking."""
    return f"{body} {aspect} your {pretty(point)}"


def symbol(body, aspect, point):
    return f"{GLYPH.get(body, body)} {ASPECT_GLYPH.get(aspect, '')} {GLYPH.get(point, point)}".strip()


def line(body, aspect, point, retro=False, stationary=False):
    """One sentence on how this contact feels. Curated where we have it,
    composed where we do not. Retrograde and stationary are named, because
    they change what the contact means."""
    text = None
    if body == "Moon":
        text = MOON_LINES.get((aspect, point))
    if text is None:
        text = BODY_LINES.get((body, aspect, point))
    if text is None:
        feel = POINT_FEEL.get(point, "this part of your chart")
        frame = ASPECT_FRAME.get(aspect, "{x} is touched.").format(x=feel)
        theme = BODY_THEME.get(body)
        text = frame[0].upper() + frame[1:]
        if theme and body != "Moon":
            text = f"{body} brings {theme} here — " + frame

    if stationary:
        text += " This one is nearly standing still: slower and heavier than sharp."
    elif retro:
        text += " Retrograde, so read it as a second pass — revisit, do not launch."
    return text


def tone(aspect):
    if aspect in FLOWING:
        return "flowing"
    if aspect in HARD:
        return "hard"
    return "neutral"


# ---- The day's framing ----------------------------------------------------

def sky_summary(moon, positions, web):
    """The collective half: Moon sign and any ingress, plus the tightest one or
    two aspects among the transiting planets. No personal claims here."""
    bits = []
    sign = moon.get("start_sign")
    if sign:
        line = f"The Moon runs through {sign}"
        if moon.get("ingress_sign") and moon.get("ingress_local"):
            line += f" and crosses into {moon['ingress_sign']} at {moon['ingress_local']}"
        bits.append(line + ".")

    tight = [w for w in web if abs(w["orb"]) <= 2.0 or w.get("exact_today")][:2]
    if tight:
        phrases = []
        for w in tight:
            p = f"{w['a']} {w['aspect']} {w['b']}"
            if w.get("exact_today"):
                p += " (exact today)"
            elif abs(w["orb"]) <= 1.0:
                p += " (tight)"
            phrases.append(p)
        held = " and ".join(phrases) if len(phrases) == 2 else phrases[0]
        verb = "sit" if len(phrases) == 2 else "sits"
        bits.append(f"{held} {verb} over everyone, not just you.")
    else:
        bits.append("Nothing among the planets is tight enough to dominate, so the "
                    "collective weather is mild.")

    retro = [p for p, i in positions.items() if i.get("retro") and p != "North Node"]
    if retro:
        bits.append("Retrograde now: " + ", ".join(retro) + ".")
    return " ".join(bits)


def arc_line(ctx):
    """Where today sits: the live lunation arc. One or two lines, then stop."""
    parts = []
    last, nxt = ctx.get("last_lunation"), ctx.get("next_lunation")
    if last and nxt:
        parts.append(f"You are between the {last['event']} on {last['date_local']} "
                     f"and the {nxt['event']} on {nxt['date_local']}.")
    elif nxt:
        parts.append(f"Next up: the {nxt['event']} on {nxt['date_local']}.")
    return " ".join(parts)


def windows(ledger):
    """Best hours and one caution, both anchored to computed times only.
    Never invents a range that no aspect supports."""
    timed = [e for e in ledger if e.get("time_minutes") is not None]
    flowing = [e for e in timed if e["tone"] == "flowing"]
    hard = [e for e in timed if e["tone"] == "hard"]
    out = []

    if flowing:
        first, last = flowing[0], flowing[-1]
        if first is last:
            out.append({"kind": "best", "label": "Best hour",
                        "anchor": first["time_local"],
                        "text": f"The hour around {first['time_local']} carries the day's "
                                f"easiest contact — {first['headline']}. Put what matters "
                                f"most there."})
        else:
            out.append({"kind": "best", "label": "Best stretch",
                        "anchor": f"{first['time_local']} – {last['time_local']}",
                        "text": f"From {first['time_local']} ({first['headline']}) through "
                                f"{last['time_local']} ({last['headline']}), the day is on "
                                f"your side. Meetings, asks, first steps."})
    else:
        out.append({"kind": "best", "label": "Best hour", "anchor": None,
                    "text": "No flowing contact perfects today, so no hour stands out as "
                            "easy. Work with the day's structure rather than its mood."})

    if hard:
        worst = max(hard, key=lambda e: e["weight"])
        out.append({"kind": "caution", "label": "Handle with care",
                    "anchor": worst["time_local"],
                    "text": f"Around {worst['time_local']}, {worst['headline']} brings the "
                            f"day's friction. Not a reason to hide — just a poor moment for "
                            f"a decision you cannot easily revisit."})
    return out


def note(day_label, engine):
    return (f"Computed for {day_label} with {engine}, from your own chart in whole-sign "
            f"houses. Times are exact to the minute for the Moon and inner planets; "
            f"slower planets hold an aspect for days, so they are marked in orb rather "
            f"than given a false minute.")
