/* The Twelve Rooms — plain-language interpretation layer.
   Composable, honest teaching of what each real placement means. This is
   the vocabulary, not a holistic reading (that is the craft we sell).
   Every sentence is built from the reader's own computed chart. */
"use strict";
window.TRI = (function () {
  // Each planet: its role in one plain phrase, and a short tag.
  const PLANET = {
    "Sun":        { role: "who you are at your core, your drive and purpose", tag: "core self" },
    "Moon":       { role: "your inner emotional world and what you need to feel safe", tag: "inner life" },
    "Mercury":    { role: "how you think, speak, and make sense of things", tag: "mind" },
    "Venus":      { role: "how you love and what you find beautiful and worth having", tag: "love & values" },
    "Mars":       { role: "how you act, assert yourself, and go after what you want", tag: "drive" },
    "Jupiter":    { role: "where you grow, take heart, and find your luck", tag: "growth" },
    "Saturn":     { role: "where you work hardest, mature, and meet your limits", tag: "discipline" },
    "Uranus":     { role: "where you break the mold and need your freedom", tag: "freedom" },
    "Neptune":    { role: "where you dream, imagine, and let the edges blur", tag: "imagination" },
    "Pluto":      { role: "where you go deep, transform, and reclaim your power", tag: "power" },
    "North Node": { role: "the direction your growth is asking you to move", tag: "growth path" },
    "South Node": { role: "what comes easily from the past, to lean on lightly", tag: "the familiar" },
    "Chiron":     { role: "your tender wound, and where you become a healer for others", tag: "the wound" },
    "ASC":        { role: "how you meet the world and the first impression you make", tag: "rising" },
    "MC":         { role: "your public role, calling, and reputation", tag: "career" },
  };

  // Each sign: how a planet there tends to operate, plus element/mode.
  const SIGN = {
    "Aries":       { style: "boldly and head-on", element: "Fire",  mode: "Cardinal" },
    "Taurus":      { style: "steadily and with the senses", element: "Earth", mode: "Fixed" },
    "Gemini":      { style: "curiously and in many directions at once", element: "Air", mode: "Mutable" },
    "Cancer":      { style: "tenderly and protectively", element: "Water", mode: "Cardinal" },
    "Leo":         { style: "warmly and with the whole heart", element: "Fire", mode: "Fixed" },
    "Virgo":       { style: "precisely and usefully", element: "Earth", mode: "Mutable" },
    "Libra":       { style: "gracefully and with an eye on the other person", element: "Air", mode: "Cardinal" },
    "Scorpio":     { style: "intensely and all the way down", element: "Water", mode: "Fixed" },
    "Sagittarius": { style: "freely and in search of meaning", element: "Fire", mode: "Mutable" },
    "Capricorn":   { style: "seriously and for the long climb", element: "Earth", mode: "Cardinal" },
    "Aquarius":    { style: "originally and on your own terms", element: "Air", mode: "Fixed" },
    "Pisces":      { style: "dreamily and with an open heart", element: "Water", mode: "Mutable" },
  };

  const HOUSE = {
    1: "your body, your identity, and how you arrive",
    2: "your money, your resources, and your sense of worth",
    3: "your mind, your words, and your daily near world",
    4: "your home, your roots, and your family",
    5: "your creativity, your romance, and your play",
    6: "your work, your health, and your routines",
    7: "your partnerships and your closest one-to-one bonds",
    8: "what you share, intimacy, and deep change",
    9: "your beliefs, your travels, and your bigger picture",
    10: "your career, your reputation, and your public life",
    11: "your friendships, your community, and your hopes",
    12: "your inner life, your solitude, and the unseen",
  };

  // Aspect: how the two planets relate, and whether it flows or asks work.
  const ASPECT = {
    "conjunction": { verb: "is fused with", flow: "blend", note: "they act as one force, for better and for more intense" },
    "sextile":     { verb: "gently supports", flow: "flow", note: "an easy opportunity, there when you reach for it" },
    "trine":       { verb: "flows naturally with", flow: "flow", note: "a genuine gift, so easy you may not notice it" },
    "square":      { verb: "pushes against", flow: "grow", note: "friction that becomes strength once you work with it" },
    "opposition":  { verb: "pulls opposite", flow: "grow", note: "two needs to balance rather than pick between" },
    "quincunx":    { verb: "keeps adjusting to", flow: "grow", note: "an odd-couple pairing you learn to fine-tune" },
  };

  function el(planet, sign, house) {
    const p = PLANET[planet]; if (!p) return null;
    const s = SIGN[sign];
    let out = cap(planet) + " is " + p.role + ".";
    if (s) out += " In " + sign + ", it works " + s.style + ".";
    if (house) out += " It lives in the house of " + HOUSE[house] + ".";
    return out;
  }

  function aspect(a, type, b) {
    const A = PLANET[a], B = PLANET[b], asp = ASPECT[type];
    if (!A || !B || !asp) return null;
    return {
      flow: asp.flow,
      plain: "Your " + A.tag + " " + asp.verb + " your " + B.tag + ". " + cap(asp.note) + ".",
      label: cap(a) + " " + type + " " + b,
    };
  }

  function bigThree(sunSign, moonSign, risingSign) {
    let s = "You lead with a <strong>" + sunSign + " Sun</strong>, so at your core you meet life " + (SIGN[sunSign] ? SIGN[sunSign].style : "in your own way") + ". ";
    s += "Underneath, your <strong>" + moonSign + " Moon</strong> means you feel and need " + (SIGN[moonSign] ? SIGN[moonSign].style : "in your own way") + ". ";
    if (risingSign) s += "And you come across, at first, as <strong>" + risingSign + " rising</strong>: " + (SIGN[risingSign] ? SIGN[risingSign].style : "distinctly you") + ".";
    return s;
  }

  const PHASE = {
    "New Moon": "a beginning, a seed in the dark, good for setting intentions",
    "Waxing Crescent": "building, taking the first real steps",
    "First Quarter": "a push, a decision point, act on what you started",
    "Waxing Gibbous": "refining, almost there, adjust and polish",
    "Full Moon": "culmination and full light, things come to a head",
    "Waning Gibbous": "sharing what you have gathered, gratitude and giving back",
    "Last Quarter": "release, a turning point, let go of what is done",
    "Waning Crescent": "rest and surrender before the next cycle",
  };

  function moonMood(sign, phase) {
    let s = "";
    if (SIGN[sign]) s += "With the Moon in " + sign + ", the emotional weather runs " + SIGN[sign].style + ". ";
    if (PHASE[phase]) s += "The " + phase.toLowerCase() + " is " + PHASE[phase] + ".";
    return s;
  }

  function signBlurb(sign) {
    const s = SIGN[sign];
    return s ? sign + " is a " + s.mode + " " + s.element + " sign, so it tends to move " + s.style + "." : "";
  }

  function cap(x) { return String(x).charAt(0).toUpperCase() + String(x).slice(1); }

  return { PLANET, SIGN, HOUSE, ASPECT, PHASE, el, aspect, bigThree, moonMood, signBlurb };
})();
