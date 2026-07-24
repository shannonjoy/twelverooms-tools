"""Sabian symbol data for Cancer.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. Each of the 30 was cross-verified
against multiple independent published sources (cafeastrology.com,
sabian-calculator.com, jamesburgess.com/Sacred 7 Academy, astronarrative.com,
kerykeion.net, and Blain Bovee's Sabian Symbol Specialist archive) before
being hand-typed here. Do NOT extend this list, or write a new sign's list,
without the same verification discipline: fewer verified degrees beats
any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a hen scratches
the ground to feed her chicks"), not a verbatim quote of Marc Edmund Jones'
1953 book or Dane Rudhyar's "An Astrological Mandala" (1973) wording.
`meaning`, `colors`, and `reflection` are original Twelve Rooms
interpretation, written fresh for this project; none of it is copied from
Jones or Rudhyar.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Cancer", "slug": "cancer", "glyph": "♋︎", "order": 4}

# The 30 degrees of Cancer, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str). See SCHEMA.md for what each field means.
ENTRIES = [
    {
        "degree": 1,
        "image": "An old flag is lowered from a ship's mast, and a new one raised in its place.",
        "meaning": "Cancer opens with a formal changing of the watch rather than a first breath: "
                   "the vessel does not change, only what flies from it changes, a signal to "
                   "everyone watching that authority, mood, or belonging has shifted hands. This "
                   "is the sign's first lesson, that home is not a fixed banner but one you keep "
                   "replacing as you become someone new, while the actual ship of self sails on "
                   "unbroken underneath. There is ceremony in it, not carelessness, since a flag "
                   "lowered gets folded before the next one goes up.",
        "colors": "A planet at Cancer 1 often marks a deliberate turning point in how someone "
                  "signals belonging, family name, home base, primary loyalty, changed on purpose "
                  "rather than drifted into. The Moon here can show someone who consciously "
                  "chooses, more than once, what home means to her. On an angle, it suggests a "
                  "person the world reads through whichever flag is currently flying, aware a "
                  "past one still sits folded and kept.",
        "reflection": "What flag are you currently flying, and did you fold the last one with "
                      "care before you raised it?",
    },
    {
        "degree": 2,
        "image": "A figure hovers motionless on a magic carpet, taking in a vast, level "
                 "landscape below.",
        "meaning": "Suspended above ordinary ground, this degree offers perspective without "
                   "participation, a view of the whole terrain that only distance can grant. "
                   "Cancer, so identified with the close and the intimate, briefly rises above "
                   "its own turf to see the larger shape of the emotional land it lives in. The "
                   "carpet is a borrowed vehicle, not a permanent post, a visit to overview, not "
                   "a new home. Still, the stillness matters: nothing here rushes to land, the "
                   "value is entirely in staying up long enough to actually look.",
        "colors": "A planet at this degree often grants real perspective on family or home "
                  "patterns, the capacity to see the whole layout instead of only the room "
                  "currently occupied. Neptune or the Moon here can describe someone who "
                  "periodically needs to rise above domestic closeness in order to understand it "
                  "clearly. It rewards taking the aerial view seriously instead of only ever "
                  "being down in the rooms.",
        "reflection": "What would you finally see clearly about your own home ground, if you "
                      "let yourself hover above it for a while?",
    },
    {
        "degree": 3,
        "image": "A person bundled in fur leads a shaggy reindeer through a cold, dim "
                 "northern canyon.",
        "meaning": "Warmth here is manufactured, not ambient: the furs are chosen, layered, "
                   "deliberate protection against a landscape that offers none on its own. This "
                   "is Cancer's instinct for shelter taken outdoors, proof that the sign's famous "
                   "need for a cozy interior can travel into genuinely hostile terrain when it "
                   "has to. The reindeer, native to this cold in a way the person is not, becomes "
                   "a guide as much as a companion, animal instinct leading human effort through "
                   "ground it actually knows.",
        "colors": "A planet at this degree often shows someone who builds real protection for "
                  "themselves and others before venturing into difficult territory, rather than "
                  "hoping conditions improve on their own. Saturn or the Moon here can describe "
                  "nurturing that shows up as preparation, layers, provisions, a companion who "
                  "knows the terrain. It rewards trusting a guide who belongs to the cold more "
                  "than you do.",
        "reflection": "What difficult ground are you currently crossing, and have you actually "
                      "dressed for it, or are you hoping it warms up?",
    },
    {
        "degree": 4,
        "image": "A hungry cat argues earnestly with the mouse she intends to catch.",
        "meaning": "Appetite and reasoning tangle together here, the cat not simply pouncing but "
                   "making a case first, as if instinct wanted the mouse's cooperation rather "
                   "than only its capture. This is a strange, almost comic degree, since a "
                   "predator rarely bothers explaining itself, and the effort to persuade "
                   "suggests something in Cancer that wants its wants to be understood, not just "
                   "satisfied. There's an honesty under the comedy: hunger can dress itself up as "
                   "conversation, but the outcome the cat is after doesn't actually change.",
        "colors": "A planet at this degree can indicate real skill at rationalizing an appetite, "
                  "wanting something and building the argument for why wanting it is reasonable. "
                  "Venus or Mars here often shows charm used in service of a very specific need, "
                  "persuasive rather than blunt. It rewards noticing when you are actually just "
                  "hungry, underneath the argument you are making.",
        "reflection": "What are you currently arguing for, that you would probably just take if "
                      "you let yourself admit you wanted it?",
    },
    {
        "degree": 5,
        "image": "A car races a train to the crossing and loses; the driver does not survive.",
        "meaning": "This is one of the zodiac's starkest images, and Cancer, a sign that prefers "
                   "caution, gets handed a warning about the exact opposite impulse: the reckless "
                   "dare against something far bigger and more fixed in its course than you are. "
                   "A train does not swerve, its schedule and its weight are absolute, and racing "
                   "it is really a contest against inevitability itself, dressed up as a contest "
                   "of speed. The degree does not moralize so much as report the outcome plainly.",
        "colors": "A planet at this degree can indicate a real tendency toward high-stakes "
                  "urgency, especially around home, family, or timing, that benefits enormously "
                  "from slowing down before a fixed deadline rather than gambling against it. "
                  "Mars or Uranus here often shows a need to test speed against something "
                  "immovable. The degree rewards yielding to what will not yield, rather than "
                  "proving a point no one survives.",
        "reflection": "What immovable thing are you currently racing, that you would be wiser to "
                      "simply let pass first?",
    },
    {
        "degree": 6,
        "image": "Wild birds gather soft material to feather their nests in the first flush "
                 "of spring.",
        "meaning": "This is Cancer doing exactly what Cancer does best, uncomplicated by irony "
                   "or danger: pure, seasonal, instinctive home-building, undertaken because "
                   "spring itself says it is time. Nothing here is reluctant, the birds aren't "
                   "debating whether to nest, they are simply gathering, trip by trip, everything "
                   "soft enough to make the next generation comfortable. There's real tenderness "
                   "in the repetition, in how many separate small trips it takes to make one nest "
                   "actually ready.",
        "colors": "A planet at this degree often brings a strong, unforced instinct toward "
                  "home-building and preparing for new life, a nurturing impulse that doesn't "
                  "need convincing or permission. The Moon here is especially at home, quite "
                  "literally, expressing a natural talent for making a place ready before anyone "
                  "asks. It rewards trusting the instinct to gather rather than overthinking the "
                  "plan.",
        "reflection": "What nest are you currently, quietly, feathering, one small gathered "
                      "thing at a time?",
    },
    {
        "degree": 7,
        "image": "Two nature spirits dance together by moonlight.",
        "meaning": "This degree slips past the practical and the visible entirely, into a realm "
                   "that only shows itself at night, to those willing to believe it's there. Two "
                   "spirits, not one, dancing rather than working, this is Cancer's private, "
                   "enchanted register, the part of home life that has nothing to do with chores "
                   "and everything to do with the magic that happens after the ordinary day ends. "
                   "Moonlight is the sign's own light; nothing here needed the sun's permission "
                   "to exist.",
        "colors": "A planet at this degree often carries a genuine feel for the enchanted, "
                  "playful undercurrent of domestic or emotional life, the part that isn't "
                  "productive and doesn't need to be. Venus or Neptune here can describe someone "
                  "whose closest bonds have a private, almost otherworldly quality, real intimacy "
                  "built after dark. It rewards keeping some part of home life unexplained, even "
                  "to yourself.",
        "reflection": "What dance happens in your life only after the ordinary day has ended, "
                      "and only for those who still believe in it?",
    },
    {
        "degree": 8,
        "image": "A procession of rabbits, dressed in human clothes, walks as if on parade.",
        "meaning": "Domestic life, dressed up and put on display: this degree takes something "
                   "inherently soft and burrow-bound and gives it costume, formation, an "
                   "audience. There's real charm here, and a little absurdity too, since rabbits "
                   "in clothing are still rabbits underneath, however dignified the parade looks. "
                   "Cancer's homebodies get their moment of public presentation in this image, "
                   "proof that even the most private creatures can enjoy being seen, "
                   "occasionally, on their own terms.",
        "colors": "A planet at this degree often shows a talent for presenting home or family "
                  "life with real charm and polish, a domestic world that knows how to look good "
                  "in public without losing its softness underneath. Venus here can indicate "
                  "genuine flair for making the ordinary look festive. It rewards letting the "
                  "private world come out and be admired sometimes, costume and all.",
        "reflection": "What part of your home life would look wonderful in a parade, if you "
                      "finally let it out of the burrow?",
    },
    {
        "degree": 9,
        "image": "A small, unclothed child reaches into the water, trying to catch a fish.",
        "meaning": "Pure, uninstructed effort meets an element that doesn't cooperate: the child "
                   "hasn't learned yet that fish are fast, that hands alone rarely work, and "
                   "reaches anyway, undiscouraged. This is Cancer at its most elemental, water as "
                   "the medium of feeling itself, and a very young, very direct attempt to grasp "
                   "something that lives entirely inside it. Nothing about the image says she'll "
                   "succeed; everything about it says she'll try again the moment this attempt "
                   "fails.",
        "colors": "A planet at this degree often shows an unguarded, persistent reach into "
                  "emotional depths, trying to catch and hold feelings that are, by nature, "
                  "slippery and quick. The Moon or Neptune here can indicate someone who keeps "
                  "reaching for emotional connection with real innocence, undeterred by how often "
                  "the fish gets away. It rewards patience with your own early, clumsy attempts.",
        "reflection": "What feeling do you keep reaching into the water for, undiscouraged by "
                      "how many times it's slipped through your hands?",
    },
    {
        "degree": 10,
        "image": "A large diamond, still rough, in the earliest stage of being cut.",
        "meaning": "Value that already exists, waiting on the careful, deliberate work that will "
                   "actually reveal it. This degree is patient about worth: the diamond was never "
                   "not valuable, but its full brilliance depends entirely on someone willing to "
                   "do the slow, precise cutting rather than rush the stone to market rough. "
                   "Cancer knows this instinctively about people, that raw potential and finished "
                   "radiance are not the same thing, and that the gap between them takes real, "
                   "unhurried craft.",
        "colors": "A planet at this degree often indicates genuine, substantial worth that is "
                  "still early in its process of being refined, a gift not yet fully cut to its "
                  "own best expression. Saturn or Venus here can describe someone whose real "
                  "value only shows itself slowly, through deliberate work rather than a single "
                  "dramatic reveal. It rewards trusting the early, unfinished stage rather than "
                  "judging the stone by how it looks rough.",
        "reflection": "What in you is already valuable, long before anyone has finished the "
                      "careful work of cutting it?",
    },
    {
        "degree": 11,
        "image": "A clown makes faces, exaggerating the mannerisms of people everyone "
                 "recognizes.",
        "meaning": "Recognition turned into performance, love turned into a slightly merciless "
                   "mirror: this degree takes the familiar, the people or patterns everyone "
                   "already knows by heart, and holds them up in exaggerated form until the "
                   "resemblance gets a laugh. There's affection buried in the mockery, since "
                   "caricature only works on faces the audience already loves enough to recognize "
                   "instantly. Cancer, so devoted to the familiar, discovers here that "
                   "familiarity itself can become material, gently roasted rather than only "
                   "protected.",
        "colors": "A planet at this degree often shows a sharp, affectionate eye for the "
                  "recognizable quirks of family or close community, and real skill at "
                  "reflecting those patterns back in a way that lands as funny rather than cruel. "
                  "Mercury here can indicate a natural mimic, someone who captures a household's "
                  "rhythms precisely enough to make everyone in it laugh at themselves. It "
                  "rewards keeping the exaggeration kind.",
        "reflection": "Whose familiar mannerisms have you gotten good enough at reading that you "
                      "could do the whole room in impression?",
    },
    {
        "degree": 12,
        "image": "A woman nurses an infant whose quiet glow marks it as an old soul, "
                 "returned.",
        "meaning": "The most ordinary act of care, nursing a baby, carries something "
                   "extraordinary hidden inside it: this particular child is understood, "
                   "somehow, to be more than new, a teacher come back around rather than a blank "
                   "beginning. Cancer's core devotion, feeding and holding a small life, gets "
                   "elevated here into something closer to reverence, the daily task and the "
                   "sacred purpose sharing the exact same gesture. Nothing about the caregiving "
                   "changes because of what the child secretly is; the woman still just feeds "
                   "the baby.",
        "colors": "A planet at this degree often shows real devotion to nurturing something, or "
                  "someone, whose eventual significance exceeds what the daily caregiving alone "
                  "reveals. The Moon or Jupiter here can describe someone raising, mentoring, or "
                  "tending a person or project destined for more than its current small size "
                  "suggests. It rewards taking ordinary daily care seriously, since it may be "
                  "carrying more than it looks like.",
        "reflection": "What are you quietly feeding right now that might turn out to be far more "
                      "significant than the daily task lets on?",
    },
    {
        "degree": 13,
        "image": "A hand is held out for examination, its thumb unusually strong and "
                 "prominent.",
        "meaning": "A single detail, isolated and studied, turns out to say more than the whole "
                   "hand would at a glance. The thumb, the part that lets a hand actually grip, "
                   "build, and hold, gets singled out here as the feature worth noticing, "
                   "practical strength foregrounded over the hand's more decorative fingers. "
                   "Cancer, a sign of instinct and feeling, gets a degree about the physical, "
                   "gripping, capable part of care, the part that actually does the holding "
                   "rather than just wanting to.",
        "colors": "A planet at this degree often indicates real, practical capability, "
                  "especially the specific strength that lets someone actually hold onto what "
                  "matters to them, literally or otherwise. Mars or Saturn here can describe a "
                  "grip, on a relationship, a resource, a responsibility, that is stronger than "
                  "it first appears. It rewards noticing your own most capable feature instead "
                  "of only your more visible ones.",
        "reflection": "What is the equivalent of your thumb, the unglamorous part of you that "
                      "actually does the holding?",
    },
    {
        "degree": 14,
        "image": "A very old man stands facing an immense stretch of darkness to the "
                 "northeast.",
        "meaning": "Age meets scale here, a whole lifetime's accumulated experience set directly "
                   "against a vastness it cannot fully see into. The direction matters, "
                   "northeast carries a sense of what's still ahead, still unknown, even at the "
                   "very end of a long life; there is no arrival where everything finally gets "
                   "explained. Cancer, so oriented toward the past and the remembered, faces here "
                   "the genuinely unremembered, the part of existence that stays dark no matter "
                   "how long you've lived and looked.",
        "colors": "A planet at this degree often shows someone who carries real, hard-won "
                  "wisdom, alongside an honest acknowledgment that some things stay unknown "
                  "regardless of age or experience. Saturn or Neptune here can describe a person "
                  "whose depth includes comfort with genuine mystery, rather than the pretense "
                  "of having it all figured out. It rewards facing what you still can't see, "
                  "instead of only reciting what you already know.",
        "reflection": "What vast dark space are you still facing, no matter how much you've "
                      "already lived and learned?",
    },
    {
        "degree": 15,
        "image": "A group of people who have eaten far past fullness, and enjoyed every bite "
                 "of it.",
        "meaning": "This is indulgence without apology, plenty enjoyed all the way past the "
                   "point of restraint, and the degree refuses to scold anyone for it. Cancer's "
                   "whole orientation is toward feeding and being fed, toward the table as the "
                   "center of belonging, and this image takes that instinct to its most "
                   "unguarded extreme: everyone at this table got exactly as much as they "
                   "wanted, and no one is pretending otherwise. There's real permission in it, "
                   "alongside a quieter question about what happens the next morning.",
        "colors": "A planet at this degree often shows genuine capacity for enjoyment, "
                  "feasting, hosting, being fed, without the usual self-consciousness about "
                  "excess. Jupiter or Venus here can indicate real generosity around food, "
                  "comfort, and abundance, shared freely rather than rationed. It rewards "
                  "actually enjoying the table you've set, instead of monitoring everyone's "
                  "portions including your own.",
        "reflection": "Where in your life have you finally stopped counting, and just let "
                      "yourself enjoy the plenty?",
    },
    {
        "degree": 16,
        "image": "A man sits before a square shape, an old handwritten scroll unrolled in "
                 "front of him.",
        "meaning": "Structure and inherited text meet here, the square offering a stable form "
                   "to work within while the scroll supplies the accumulated knowledge of "
                   "everyone who studied before him. This is Cancer's relationship to lineage "
                   "made almost literal: you don't invent your understanding from nothing, you "
                   "sit down with what the family, the tradition, the past already wrote, and "
                   "you do the slow work of actually reading it. Nothing about the image is "
                   "fast; a scroll gets unrolled a little at a time, the same way inherited "
                   "wisdom gets absorbed.",
        "colors": "A planet at this degree often favors deep, patient study of tradition, "
                  "family history, or inherited method, using it deliberately rather than "
                  "reinventing everything from scratch. Mercury or Saturn here can describe "
                  "genuine scholarly devotion to understanding where you actually came from. It "
                  "rewards sitting with the old scroll long enough to really read it, instead of "
                  "skimming for the parts you already agree with.",
        "reflection": "What old scroll, literal or inherited, have you been meaning to actually "
                      "sit down and read?",
    },
    {
        "degree": 17,
        "image": "A single seed pushes upward, becoming, in time, both knowledge and life "
                 "itself.",
        "meaning": "This is Cancer's whole philosophy compressed into one image: something "
                   "small and buried does not stay small if it is given time, and what it grows "
                   "into is not just size but understanding. The seed doesn't know in advance "
                   "what it's becoming, it simply keeps unfolding, one stage at a time, toward a "
                   "form its beginning never fully predicted. There's real trust required here, "
                   "trust that slow, invisible growth underground is not failure, just the "
                   "necessary first half of the process.",
        "colors": "A planet at this degree often indicates real, steady development, of a "
                  "skill, a relationship, an understanding, that starts small and keeps "
                  "compounding rather than arriving all at once. Jupiter or the Moon here can "
                  "describe someone whose growth has been genuinely gradual and genuinely real, "
                  "not staged for effect. It rewards trusting the parts of your own growth that "
                  "are still underground and invisible.",
        "reflection": "What seed in your life is already growing into knowledge and life, even "
                      "though you can't see it above ground yet?",
    },
    {
        "degree": 18,
        "image": "A hen scratches at the ground, working to find food for the chicks behind "
                 "her.",
        "meaning": "Unglamorous, repetitive, entirely necessary labor: this degree is Cancer's "
                   "daily maintenance work, the scratching and searching that happens every "
                   "single day so that smaller, dependent lives get fed. No one applauds a hen "
                   "for scratching the ground; it simply has to happen, over and over, for the "
                   "chicks to survive the week. There's dignity in the repetition itself, in a "
                   "creature that keeps doing the unremarkable task because the remarkable "
                   "outcome, healthy chicks, depends entirely on it.",
        "colors": "A planet at this degree often shows steady, unglamorous provision for "
                  "dependents, the daily work of feeding and caring for others that rarely gets "
                  "noticed but never stops mattering. The Moon here is especially at home, "
                  "describing a caretaker whose devotion shows up as consistency rather than "
                  "drama. It rewards recognizing your own daily scratching for what it actually "
                  "is: real, sustaining work.",
        "reflection": "What daily, unglamorous scratching are you doing right now that someone "
                      "smaller is quietly depending on?",
    },
    {
        "degree": 19,
        "image": "A priest conducts a wedding, joining two people in front of witnesses.",
        "meaning": "A private bond gets formalized here, made public and sanctioned by ritual "
                   "and community rather than kept as a purely personal understanding between "
                   "two people. Cancer, usually protective of intimacy, gets a degree about the "
                   "moment intimacy chooses to step into the open and ask for recognition. The "
                   "priest is a stand-in for everyone else, the family, the tradition, the wider "
                   "structure, that now formally witnesses and blesses what had, until this "
                   "moment, belonged only to the couple.",
        "colors": "A planet at this degree often shows a real need to formalize commitments, to "
                  "move a bond from private understanding into public, recognized structure. "
                  "Venus or Jupiter here can indicate someone for whom ritual, ceremony, and "
                  "community witness genuinely deepen a relationship rather than merely decorate "
                  "it. It rewards letting an important bond be seen and blessed, not just "
                  "privately known.",
        "reflection": "What private bond in your life might actually be ready for a witness?",
    },
    {
        "degree": 20,
        "image": "Gondoliers sing to their passengers as the boats move through the evening "
                 "canals.",
        "meaning": "Work and romance share the same oar here, the gondolier's job literally is "
                   "to move people through beautiful water while making the passage feel like an "
                   "occasion rather than a commute. Cancer's gift for atmosphere gets full "
                   "expression in this image, proof that a practical task, ferrying someone from "
                   "one place to another, can be performed with enough warmth and music that it "
                   "becomes memorable rather than merely functional. Nothing about the "
                   "destination matters as much as how the journey there felt.",
        "colors": "A planet at this degree often brings real talent for making an ordinary "
                  "passage, a commute, a transition, a shared errand, feel warm, musical, even "
                  "romantic. Venus or Neptune here can describe someone who instinctively adds "
                  "atmosphere to whatever task is at hand. It rewards singing through the parts "
                  "of life that could otherwise be treated as mere transport.",
        "reflection": "What ordinary passage in your life could use a little more music while "
                      "you're moving through it?",
    },
    {
        "degree": 21,
        "image": "A celebrated singer performs alone before a full, attentive audience.",
        "meaning": "The private, emotional voice Cancer usually keeps close gets its full "
                   "public moment here, one figure, trained and ready, carrying an entire room's "
                   "attention on breath and feeling alone. This is vulnerability turned into "
                   "mastery: nothing hides a prima donna, her instrument is her own body, and "
                   "the performance only works if the feeling underneath is genuinely there and "
                   "genuinely controlled at the same time. Cancer's emotional depths, usually "
                   "private, learn here what it costs, and gives, to let them be heard by "
                   "everyone in the house.",
        "colors": "A planet at this degree often shows real talent for expressing deep feeling "
                  "in a way that reaches, and holds, a large audience rather than only a close "
                  "circle. The Sun or Venus here can indicate someone built for exactly this "
                  "kind of emotionally exposed, technically mastered performance. It rewards "
                  "trusting your own trained voice enough to let the whole room hear it.",
        "reflection": "What feeling have you fully trained and mastered enough to finally "
                      "perform in front of the whole room?",
    },
    {
        "degree": 22,
        "image": "A woman stands at the water's edge, watching for the sailboat that is "
                 "coming.",
        "meaning": "This is expectant waiting, not passive but focused, the woman's whole "
                   "attention pointed at a horizon where something she's counting on has not yet "
                   "arrived. Cancer knows this particular ache well, the watching that comes "
                   "with loving someone who has to cross water to get back to you. There's faith "
                   "here as much as anxiety: she hasn't left the shore, hasn't given up on the "
                   "boat showing up, she's simply standing in the one place she'll be able to "
                   "see it the moment it does.",
        "colors": "A planet at this degree often shows genuine capacity for devoted, patient "
                  "waiting, especially for someone or something that has to travel some distance "
                  "before it can return. The Moon or Neptune here can indicate real faithfulness "
                  "during periods of separation, watching without abandoning the post. It "
                  "rewards staying at your own water's edge a little longer, if you still "
                  "believe the boat is coming.",
        "reflection": "What are you currently standing at the water's edge for, and do you "
                      "still believe it's on its way?",
    },
    {
        "degree": 23,
        "image": "Members of a literary society gather for their regular meeting.",
        "meaning": "Shared devotion to words becomes its own kind of family here, a group that "
                   "has chosen each other specifically around a love of reading and discussing "
                   "rather than blood or geography. Cancer's instinct for belonging doesn't "
                   "require a household, this degree proves; a circle that meets regularly to "
                   "talk about books can become just as real a home as any kitchen table. "
                   "There's structure in it too, a standing meeting, a habit of return, the kind "
                   "of ritual gathering that turns acquaintance into something closer to kin.",
        "colors": "A planet at this degree often shows real belonging found through shared "
                  "intellectual or creative interest, a chosen circle that gathers with real "
                  "regularity and real warmth. Mercury or the Moon here can describe someone "
                  "whose truest sense of home comes from a group built around ideas rather than "
                  "lineage. It rewards taking your own chosen circle as seriously as any family "
                  "table.",
        "reflection": "What regular gathering in your life has quietly become as much a home as "
                      "your actual household?",
    },
    {
        "degree": 24,
        "image": "A woman and two men, stranded together on a small island, share the same "
                 "sunlit patch of land.",
        "meaning": "Circumstance, not choice, has put these three people together, and the "
                   "island is small enough that there's no real option but to make something "
                   "workable out of the arrangement. Cancer's whole project is belonging, and "
                   "this degree tests it under pressure: can a family be formed out of whoever "
                   "happens to be stranded with you, rather than whoever you would have picked. "
                   "The sunlight matters, this isn't a grim shipwreck scene, it's survivable, "
                   "even oddly peaceful, three people making do together in decent conditions.",
        "colors": "A planet at this degree often shows real adaptability in forming close bonds "
                  "with whoever circumstance actually puts nearby, rather than insisting on a "
                  "chosen ideal. Venus or the Moon here can indicate found family built from "
                  "proximity and necessity that becomes genuinely warm over time. It rewards "
                  "making real peace with your own island, and the people who happen to be on "
                  "it with you.",
        "reflection": "Who did circumstance strand you with, that has slowly become closer to "
                      "family than you expected?",
    },
    {
        "degree": 25,
        "image": "A sudden dark shadow, like a heavy cloak, falls across a man's right "
                 "shoulder.",
        "meaning": "Something larger than the man himself descends here, uninvited and "
                   "immediate, a weight or a presence that arrives from outside his own will and "
                   "settles directly onto him. This isn't tragedy exactly, it reads more like "
                   "being marked, singled out by something with real gravity, whether that turns "
                   "out to be a burden, a calling, or both at once. Cancer, so attuned to what "
                   "moves through a household unseen, gets a degree about the exact moment an "
                   "outside force stops being abstract and lands, specifically, on one person's "
                   "shoulder.",
        "colors": "A planet at this degree often indicates being suddenly, unmistakably marked "
                  "by something larger than personal will, a responsibility, a legacy, an "
                  "inheritance that arrives all at once rather than gradually. Saturn or Pluto "
                  "here can describe real weight taken on abruptly, and often the strength that "
                  "comes with actually carrying it. It rewards recognizing the shadow as "
                  "significant rather than simply unlucky.",
        "reflection": "What descended on you suddenly, that you're still learning whether to "
                      "call a burden or a calling?",
    },
    {
        "degree": 26,
        "image": "In a wealthy home's library, guests sit among the cushions, reading.",
        "meaning": "This is comfort and intellect sharing the same room, real luxury measured "
                   "not by spectacle but by the simple fact that people are allowed to be quiet, "
                   "seated, and absorbed in a book. Cancer's love of shelter reaches its most "
                   "refined form here, a home so secure that its guests can afford to do nothing "
                   "more urgent than read. There's a warning folded gently into the ease, too, "
                   "since a room this comfortable can also become a room no one ever feels the "
                   "need to leave.",
        "colors": "A planet at this degree often shows real appreciation for intellectual "
                  "comfort, a home life rich enough, in resources or simply in peace, to make "
                  "quiet reading feel like the natural use of an afternoon. Venus or Jupiter "
                  "here can indicate genuine ease and cultural refinement enjoyed at home. It "
                  "rewards using the comfort for something, reading, thinking, resting well, "
                  "rather than only accumulating it.",
        "reflection": "What have you built a comfortable enough home to finally have the quiet "
                      "to actually read?",
    },
    {
        "degree": 27,
        "image": "A fierce storm tears through a canyon lined with costly, secluded homes.",
        "meaning": "Wealth and shelter turn out not to be weatherproof, this degree insists, as "
                   "nature moves through a landscape of privilege with the same force it would "
                   "use anywhere else. Cancer's deep investment in home and safety meets its "
                   "limit here: no amount of expensive seclusion actually controls the sky. "
                   "There's real humility in the image, a reminder that the most "
                   "protected-looking lives are still, underneath the landscaping, subject to "
                   "the same forces as everyone else's.",
        "colors": "A planet at this degree often shows real vulnerability breaking through even "
                  "well-defended, well-resourced circumstances, a reminder that no home is "
                  "actually storm-proof. Uranus or Pluto here can indicate sudden upheaval "
                  "reaching places that looked secure from the outside. It rewards building real "
                  "resilience, not just comfortable appearances, into whatever home you've made.",
        "reflection": "What storm has already reached your most carefully sheltered ground, no "
                      "matter how secure it looked from outside?",
    },
    {
        "degree": 28,
        "image": "A Native woman, educated away from her tribe, returns and presents her "
                 "partner to her people.",
        "meaning": "Two worlds meet in one act of introduction here, the education and "
                   "experience gained elsewhere brought home and offered up for the original "
                   "community's blessing. This degree is about the real, sometimes tender labor "
                   "of bridging where you came from and who you've since become, asking the "
                   "people who knew you first to accept the life you've built since. Cancer "
                   "knows this bridge intimately, the work of staying loyal to your roots while "
                   "still bringing something, or someone, genuinely new back to them.",
        "colors": "A planet at this degree often shows someone actively working to reconcile "
                  "two different worlds, an origin community and a life built elsewhere, "
                  "bringing them into honest relationship with each other rather than keeping "
                  "them separate. Venus or the Moon here can indicate real courage in "
                  "introducing a new bond to an original, more traditional circle. It rewards "
                  "the vulnerability of actually asking for that blessing, instead of avoiding "
                  "the introduction.",
        "reflection": "What two worlds of your own life are you still working up the courage to "
                      "introduce to each other?",
        "note": "Note: the 1925 original for this degree used dated ethnic imagery; the picture "
                "above keeps its meaning in respectful, modern terms.",
    },
    {
        "degree": 29,
        "image": "A Greek muse holds newborn twins on a golden scale, weighing them.",
        "meaning": "Even brand-new life gets measured here, assessed by something wiser and "
                   "more mythic than the twins themselves could know to expect. This isn't cold "
                   "judgment, a muse weighs with purpose, likely discerning gift, calling, or "
                   "fate rather than simply ranking one twin against the other. Cancer's "
                   "devotion to the newly born meets, in this next-to-last degree, something "
                   "larger than pure nurture: the recognition that even the youngest life is "
                   "already being weighed for what it will become.",
        "colors": "A planet at this degree often shows an early, almost uncanny sense of what a "
                  "new beginning, a child, a project, a relationship, is actually weighted "
                  "toward, gift or difficulty made visible before much time has passed. Jupiter "
                  "or Neptune here can describe genuine discernment applied gently, without "
                  "harshness, to something very new. It rewards trusting your own early read on "
                  "what's just been born.",
        "reflection": "What new beginning in your life have you already, quietly, started "
                      "weighing, and what do you sense the scale is telling you?",
    },
    {
        "degree": 30,
        "image": "A woman descended from patriots walks proudly to the podium at her "
                 "society's meeting.",
        "meaning": "The final degree of Cancer closes the sign's long meditation on home and "
                   "lineage with public pride rather than private retreat: this woman's whole "
                   "identity is bound up in an inheritance she did not create but carries "
                   "forward with real confidence. Nothing about this walk to the podium is "
                   "uncertain, generations of belonging stand behind every step. Cancer, which "
                   "spent twenty-nine degrees learning to nurture, protect, and remember, ends "
                   "by standing up in front of a room and claiming that lineage out loud.",
        "colors": "A planet at this degree often shows genuine pride in inherited identity, "
                  "family history, or lineage worn confidently and publicly rather than kept "
                  "quiet. The Sun or Saturn here can describe someone whose sense of self draws "
                  "real, steady strength from where they come from. It rewards standing up and "
                  "claiming your own inheritance instead of only tending it privately.",
        "reflection": "What inheritance are you finally ready to walk to the podium and claim "
                      "out loud?",
    },
]

assert len(ENTRIES) == 30, f"expected 30 Cancer degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Cancer degrees out of order"
