"""The three short reads the Big 3 calculator shows, for the share page.

A copy of the SUN, MOON and RISING objects in big-3-calculator.html, so
api/big3.py can render /big-3/<sun>-<moon>-<rising> on the server.
tests/test_growth_features.py fails if the two ever drift apart, so a
change to the calculator's copy is made in both places."""

SUN = {
    "Aries": "a life lit by beginnings: you are here to go first, and courage is the craft you are perfecting.",
    "Taurus": "you are here to build what lasts, and to prove that steadiness is its own kind of genius.",
    "Gemini": "you are here to learn everything twice and say it better: curiosity is the calling itself.",
    "Cancer": "you are here to protect what matters. Care, taken seriously, is your life's work.",
    "Leo": "you are here to shine warmly and be seen doing it: the open heart is the work, not the reward.",
    "Virgo": "you are here to perfect a craft. Your devotion lives in the details no one else would notice.",
    "Libra": "you are here to make things fair and beautiful, and to master the art of the other person.",
    "Scorpio": "you are here to go all the way down: truth matters more to you than comfort, and it shows.",
    "Sagittarius": "you are here for the far horizon. Meaning is your fuel, and honesty is how you travel.",
    "Capricorn": "you are here to climb something worth climbing: time is your ally and mastery is the point.",
    "Aquarius": "you are here to see the circle clearly from just outside it, and then to improve it.",
    "Pisces": "you are here to feel everything and turn it into compassion, or art, or both at once."
}

MOON = {
    "Aries": "you feel fast and first. You settle by acting, not by waiting, and you recover quickly.",
    "Taurus": "you settle through comfort, routine, and things you can touch: peace, for you, is physical.",
    "Gemini": "you process by talking it through. A good conversation is genuine rest.",
    "Cancer": "the Moon is at home here: you need belonging, you remember everything, and you give care back doubled.",
    "Leo": "you need to be met warmly. Being celebrated a little is not vanity: it is how your heart refuels.",
    "Virgo": "order soothes you. A tended list is a tended heart, and being useful is how you love.",
    "Libra": "you settle in balance and lovely surroundings. Conflict costs you more than most people guess.",
    "Scorpio": "you feel in full depth or not at all. Trust is your currency, and you never spend it lightly.",
    "Sagittarius": "you need room to roam, even indoors. Hope is your home base and humor is the door to it.",
    "Capricorn": "you steady yourself by being useful. Feelings arrive on a small delay, and then completely.",
    "Aquarius": "you need air and a little distance to know what you feel. Clarity is your comfort.",
    "Pisces": "you absorb the weather of every room you enter. Solitude and beauty are how you come back to yourself."
}

RISING = {
    "Aries": "you arrive like a headline: people meet your momentum before anything else.",
    "Taurus": "you arrive calm. People read steadiness in you before you have said a word.",
    "Gemini": "you arrive curious and quick: the first thing people meet is the question.",
    "Cancer": "you arrive gently, reading the tide of the room before you fully enter it.",
    "Leo": "you arrive warm and unmistakable. Rooms tilt toward you, and you let them.",
    "Virgo": "you arrive precise and observant. People trust you early, and they are right to.",
    "Libra": "you arrive gracious: ease is the first thing people feel around you.",
    "Scorpio": "you arrive composed, with weather behind the eyes. People sense the depth immediately.",
    "Sagittarius": "you arrive mid-story, candid and warm: people meet your honesty first.",
    "Capricorn": "you arrive credible. People hand you responsibility on sight, and you take it.",
    "Aquarius": "you arrive one clean step outside expectation, and it suits you.",
    "Pisces": "you arrive soft-focus and open. People confide in you within minutes and are never sure why."
}
