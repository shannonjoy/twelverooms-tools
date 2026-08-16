"""Interpretation copy for the daily horoscope.

HAND-WRITTEN. Unlike its neighbours here, this file is NOT a generated copy:
bin/sync-engines.sh only rewrites the seven files it names, so this one and
engines.py both survive a re-sync. Edit it here.

It lives in _engines rather than a directory of its own only because
vercel.json bundles api/_*/** and this path is the one already proven to ship.

The ephemeris decides WHAT is happening and WHEN; this module decides how it
reads. Two layers:

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

    # Quincunxes: the awkward 150 degree angle. Each point gets its own, so a day
    # with several of them reads as distinct fidgets, not one repeated sentence.
    ("quincunx", "Sun"):      "A small misfit between how you feel and who you are today. Adjust the plan, not the mood.",
    ("quincunx", "Moon"):     "Your needs and your circumstances are half a size off. Tend the small discomfort; do not overhaul the day for it.",
    ("quincunx", "Mercury"):  "A thought that will not sit quite right. Reword it rather than abandon it.",
    ("quincunx", "Venus"):    "Comfort and wanting point slightly different ways. Take the smaller pleasure, the one that costs no rearranging.",
    ("quincunx", "Mars"):     "Your drive is aimed a few degrees off the target. Redirect the effort instead of pushing harder.",
    ("quincunx", "Saturn"):   "A duty that does not fit the hour. Do the piece that fits; defer the rest without guilt.",
    ("quincunx", "Jupiter"):  "An appetite that does not match the moment. Want it, right-size it, come back to it later.",
    ("quincunx", "ASC"):      "How you come across and how you feel are slightly out of register. Let the first impression be imperfect.",
    ("quincunx", "MC"):       "What the work wants and what you have to give sit a notch apart. Trim the task rather than strain to meet it.",
    ("quincunx", "North Node"): "The way forward asks for a small correction, not a leap. Nudge the wheel and keep going.",
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


# U+FE0E forces text presentation. Venus and Mars default to emoji on Apple
# platforms; the rest of the set does not, but applying it to every glyph is
# cheaper than maintaining a list of which ones need it.
VS = "\ufe0e"


def _g(name):
    """A glyph for `name`, pinned to text presentation. Falls back to the name."""
    return GLYPH[name] + VS if name in GLYPH else name


def symbol(body, aspect, point):
    return f"{_g(body)} {ASPECT_GLYPH.get(aspect, '')} {_g(point)}".strip()


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


# ---- Sky events: lunations, ingresses, stations --------------------------
# The loudest things the sky does. Each is a first-class line on the clock,
# not a boundary sentence buried at the edge of the day.

HOUSE_THEME = {
    1: "you, your body, and how you begin things",
    2: "money, resources, and what you value",
    3: "talk, siblings, and the everyday mind",
    4: "home, family, and your roots",
    5: "romance, children, and play",
    6: "work, health, and daily routine",
    7: "partnership and the close other",
    8: "intimacy, shared resources, and depth",
    9: "meaning, travel, and the wider view",
    10: "career, reputation, and public role",
    11: "friends, networks, and what is next",
    12: "rest, the inner life, and what is hidden",
}

LUNATION_COPY = {
    "New Moon": "A New Moon resets the lunar month in {sign}. This is the seed point: dark, low, better for naming an intention than launching one. What you begin near it tends to grow as the Moon fills.",
    "Full Moon": "The lunar month reaches its peak: a Full Moon in {sign}. Illumination and release, the point where something reaches its high-water mark and asks to be seen, finished, or set down. Feelings run bright and close to the surface.",
}

MOTION_GLYPH = {"retrograde": "℞", "direct": "D"}
PHASE_GLYPH = {"New Moon": "●", "Full Moon": "○"}


def event_headline(ev):
    t = ev["type"]
    if t == "lunation":
        return f"{ev['kind']} in {ev['sign']}"
    if t == "ingress":
        return f"{ev['body']} enters {ev['to_sign']}"
    return f"{ev['body']} stations {ev['direction']}"


def event_symbol(ev):
    t = ev["type"]
    if t == "lunation":
        return f"{PHASE_GLYPH.get(ev['kind'], '')} {_g('Moon')}".strip()
    if t == "ingress":
        return f"{_g(ev['body'])} → {ev['to_sign']}"
    return f"{_g(ev['body'])} {MOTION_GLYPH.get(ev['direction'], '')}".strip()


def event_line(ev, house=None):
    t = ev["type"]
    if t == "lunation":
        text = LUNATION_COPY[ev["kind"]].format(sign=ev["sign"])
        if house:
            text += f" For you it lands in your {_ord(house)} house: {HOUSE_THEME.get(house, 'this part of your life')}."
        return text
    theme = BODY_THEME.get(ev["body"], "its own themes")
    if t == "ingress":
        return (f"{ev['body']} leaves {ev['from_sign']} for {ev['to_sign']}, so {theme} "
                f"takes on a new colour for as long as it stays. A change of register, "
                f"not a single event to catch.")
    if ev["direction"] == "retrograde":
        return (f"{ev['body']} turns retrograde in {ev['sign']}: {theme} turns inward for "
                f"review. Over the coming weeks its themes double back. Revisit, do not launch.")
    return (f"{ev['body']} turns direct in {ev['sign']}: {theme} resumes forward motion after "
            f"its review. What had stalled begins to move again.")


def event_tone(ev):
    if ev["type"] == "lunation":
        return "event"
    return "event"


# ---- House tag for an ordinary contact ------------------------------------

def _ord(n):
    v = n % 100
    suf = "th" if 11 <= v <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def house_tag(house):
    """'your 10th house, career, reputation, and public role' or None."""
    if not house:
        return None
    return f"your {_ord(house)} house: {HOUSE_THEME.get(house, 'this part of your life')}"


# ---- The bridge: a public event, placed inside one private chart ----------

# How the event meets the natal point. Written as a verb so the clause can
# carry a subject; ASPECT_FRAME above is written to END a sentence, these are
# written to continue one.
BRIDGE_VERB = {
    "conjunction": "sits right on top of",
    "sextile":     "reaches toward",
    "square":      "squares",
    "trine":       "trines",
    "opposition":  "opposes",
    "quincunx":    "sits at an awkward angle to",
}
BRIDGE_SHAPE = {
    "conjunction": "bringing {x} right to the surface",
    "sextile":     "opening a little room around {x}",
    "square":      "asking a question of {x}",
    "trine":       "letting {x} move without forcing",
    "opposition":  "pulling {x} against something else",
    "quincunx":    "asking you to adjust {x} rather than push it",
}

def _art(body):
    """'the ' for the luminaries, nothing for the planets: "the Sun moving into
    Virgo", but "Venus moving into Virgo"."""
    return "the " if body in ("Moon", "Sun") else ""


_EVENT_SUBJECT = {
    "lunation": lambda ev: f"the {ev['kind']} in {ev['sign']}",
    "ingress":  lambda ev: f"{_art(ev['body'])}{ev['body']} moving into {ev['to_sign']}",
    "station":  lambda ev: f"{_art(ev['body'])}{ev['body']} turning {ev['direction']}",
}


def bridge_line(ev, house=None, hit=None):
    """The one sentence the whole reading exists to write: today's public
    event, placed inside this particular chart.

    `hit` is (point, aspect) for the tightest contact the event makes to a
    natal point, or None. Returns None when the event touches neither a house
    nor a point, because a bridge with nothing on either bank is just the sky
    restated, and the reader already has that above.
    """
    subject = _EVENT_SUBJECT.get(ev["type"], lambda e: "the sky today")(ev)

    where = None
    if house:
        where = (f"lands in your {_ord(house)} house: "
                 f"{HOUSE_THEME.get(house, 'this part of your life')}")

    touch = None
    if hit:
        point, aspect = hit
        verb = BRIDGE_VERB.get(aspect, "touches")
        shape = BRIDGE_SHAPE.get(aspect, "reaching {x}").format(
            x=POINT_FEEL.get(point, "this part of your chart"))
        touch = f"{verb} your {pretty(point)}, {shape}"

    if where and touch:
        return f"For you, {subject} {where}. It also {touch}."
    if where:
        return f"For you, {subject} {where}. That is the part of your life it lights."
    if touch:
        return f"For you, {subject} {touch}."
    return None


# ---- Energy of the day: one synthesized line ------------------------------

_COUNT_WORD = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
_PATTERN_ASK = {
    "quincunx": "small course-corrections rather than one big move",
    "square": "choices made under a little friction",
    "trine": "ease you can actually use if you take it",
    "sextile": "small openings that reward a little effort",
    "opposition": "balance between two pulls",
    "conjunction": "single-pointed focus on what merges",
}
# The Moon's phase as an adjective, so a sentence reads "the Moon is full in
# Aquarius", never the broken "a Full Moon Moon".
PHASE_DESC = {
    "New Moon": "new", "Waxing Crescent": "a waxing crescent",
    "First Quarter": "at first quarter", "Waxing Gibbous": "waxing gibbous",
    "Full Moon": "full", "Waning Gibbous": "waning gibbous",
    "Last Quarter": "at last quarter", "Waning Crescent": "a waning crescent",
}
_LUNATIONS = ("Full Moon", "New Moon")


def _plural_aspect(asp, n):
    word = _COUNT_WORD.get(n, str(n))
    plural = "quincunxes" if asp == "quincunx" else f"{asp}s"
    return f"{word} {plural}"


def energy_line(featured, ledger, phase, has_lunation):
    """The one read of the whole day: the biggest thing, the Moon's phase, and
    the shape of the personal threads underneath. One to three short sentences."""
    if not featured:
        return (f"A quiet day. The Moon is {PHASE_DESC.get(phase['name'], phase['name'].lower())} "
                f"in {phase['sign']}, and nothing perfects sharply to your chart, so the day "
                f"takes its shape from your own plans rather than the sky's.")

    is_lunation = featured.get("event_kind") in _LUNATIONS
    if is_lunation:
        sentences = [f"Today turns on the {featured['headline']}."]
    elif featured.get("is_event"):
        sentences = [f"Today's headline is {featured['headline']}."]
    else:
        sentences = [f"The day leans on {featured['headline']}."]

    if not is_lunation:
        sentences.append(f"The Moon is {PHASE_DESC.get(phase['name'], phase['name'].lower())} "
                         f"in {phase['sign']}.")

    personal = [e for e in ledger if e.get("time_minutes") is not None and not e.get("is_event")]
    if personal:
        counts = {}
        for e in personal:
            counts[e["aspect"]] = counts.get(e["aspect"], 0) + 1
        asp, n = max(counts.items(), key=lambda kv: kv[1])
        if n >= 3:
            sentences.append(f"Underneath, {_plural_aspect(asp, n)} thread the hours: "
                             f"{_PATTERN_ASK.get(asp, 'small repeated notes')}.")

    return " ".join(sentences)


def closing_line(windows, featured):
    """One practical, non-prescriptive takeaway, anchored only to computed hours."""
    best = next((w for w in windows if w["kind"] == "best" and w.get("anchor")), None)
    caution = next((w for w in windows if w["kind"] == "caution" and w.get("anchor")), None)
    if best and caution:
        return (f"Put what matters near {best['anchor']}, and give {caution['anchor']} a lighter "
                f"touch. Nothing here is fate; it is the grain of the day, and you decide how to cut it.")
    if best:
        return (f"Aim the day's real work at {best['anchor']}, when the sky is most on your side. "
                f"The rest is yours to shape.")
    if caution:
        return (f"Go gently around {caution['anchor']}, the one rough patch, and let the rest of the "
                f"day run on your own plans rather than the sky's mood.")
    if featured and featured.get("event_kind") in _LUNATIONS:
        return (f"The day turns on the {featured['headline']} at {featured.get('time_local')}. No "
                f"single hour reads as purely easy or hard, so let the lunation set the tone and "
                f"work your own plans around it.")
    return ("No hour stands out sharply today, easy or hard, so work from your own structure and "
            "let the day be what you make it.")


# ---- Teach-on-tap definitions ---------------------------------------------
# Plain-language glossary. The frontend shows only the terms a given day uses,
# so a newcomer can learn the craft without the page turning into a textbook.

DEFINITIONS = {
    "conjunction": "Two points at the same degree. Their meanings merge and amplify each other.",
    "sextile": "Points 60 degrees apart. An easy, optional opening that helps if you take it.",
    "square": "Points 90 degrees apart. Productive friction that forces a choice or an action.",
    "trine": "Points 120 degrees apart. A smooth, flowing channel between two parts of the chart.",
    "opposition": "Points 180 degrees apart. Two needs face each other and ask to be balanced.",
    "quincunx": "Points 150 degrees apart. An awkward, off-register angle: adjust rather than force.",
    "orb": "How far from exact an aspect is. The tighter the orb, the stronger the effect.",
    "applying": "The aspect is still tightening toward exact, so it is building rather than fading.",
    "separating": "The aspect is past exact and loosening, so its effect is winding down.",
    "retrograde": "A planet appearing to move backward from Earth. A time to review, not launch.",
    "stationary": "A planet nearly paused as it changes direction. Its themes come into sharp focus.",
    "Full Moon": "The Moon opposite the Sun: the lunar month's peak. Culmination and release.",
    "New Moon": "The Moon meeting the Sun: the month's dark reset. A seed point for intentions.",
    "Ascendant": "The sign rising at your birth. How you meet the world and first come across.",
    "Midheaven": "The top of your chart. Your career, calling, and public role.",
    "whole-sign houses": "A house system where each zodiac sign is one whole house of your life.",
}

# Which glossary terms a contact or event brings to the surface.
def terms_for_aspect(aspect):
    return [aspect]


def definitions_for(terms):
    """Return {term: definition} for the terms actually shown, in a stable order."""
    order = list(DEFINITIONS.keys())
    seen = [t for t in order if t in set(terms)]
    return [{"term": t, "def": DEFINITIONS[t]} for t in seen]
