"""Sabian symbol data for Aquarius.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against four
independent, mutually agreeing published sources before being hand-typed:
jamesburgess.com / Sacred 7 Academy's "Aquarius Sabians List", cafeastrology.com's
"Sabian Symbols Degree Meanings" page (which labels on the "N-1 to N"
degree-area convention, e.g. its "0-1" is this file's degree 1, its "29-30"
is this file's degree 30 -- checked across the offset the same way as
Virgo's and Sagittarius's files), astronarrative.com's "aquarius.html"
(same N-1-to-N convention, independently matching cafeastrology degree for
degree), and kerykeion.net's "foundation-sabian-aquarius" page (full-sentence
Rudhyar-register wording, also matching in order). Degree 30 was additionally
spot-checked against sabian-calculator.com's per-degree page, jamesburgess.com's
dedicated "The field of Ardath in bloom" archive entry, and judithdehaan.substack.com's
dedicated write-up, all agreeing verbatim on wording and all confirming this
is the ORIGINAL 1925 Jones/Wheeler text (Rudhyar's own "spiritual brotherhood
... unanimous consciousness" language, sometimes seen quoted as if it were the
symbol itself, is Rudhyar's later interpretive paraphrase in "An Astrological
Mandala", not the canonical image). Degree 5 was additionally spot-checked
against jamesburgess.com's dedicated "Council of ancestors" archive entry and
sabiansymbols.com's dedicated write-up. Degree 4 was additionally spot-checked
against two independent Sabian-symbol blogs (saijin.wordpress.com and
sabiansymbologist.wordpress.com), both confirming "A Hindu healer" as the
short-form 1925 original. Do NOT extend this list, or write a new sign's list,
without the same verification discipline: fewer verified degrees beats any
guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "two lovebirds
sing together on a fence"), not a verbatim quote of Marc Edmund Jones' 1953
book or Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation, written
fresh for this project; none of it is copied from Jones or Rudhyar.

DATED IMAGERY: Aquarius 4's 1925 original is "A Hindu healer" (also seen as
"a Hindu yogi demonstrates his healing powers"), a symbol tied to a specific
ethnicity/religious identity via an occupational-type descriptor, the same
structural pattern (ethnicity + occupation) as Sagittarius 22's "A Chinese
laundry". Per Shannon's standing policy, the canonical mapping is kept, but
`image` restates it respectfully without the ethnic label (focusing on the
underlying theme of trained, lineage-carried healing skill), and a `note`
field is attached below the symbol card. One other degree was checked
carefully and judged NOT to meet this bar: degree 5 ("A council of
ancestors") names no specific ethnicity or nationality and carries no
occupational stereotype, so it did not receive a `note`.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Aquarius", "slug": "aquarius", "glyph": "♒︎", "order": 11}

# The 30 degrees of Aquarius, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and an optional note (str) on the one degree whose 1925
# original used a dated ethnic/occupational descriptor. See SCHEMA.md for
# what each field means.
ENTRIES = [
    {"degree": 1,
     "image": "An old adobe mission stands weathered but intact in the California hills.",
     "meaning": "Aquarius opens not with a blank page but with a structure that has "
                "already survived generations: walls raised to hold a whole community's "
                "belief and shelter, still standing after the builders themselves are "
                "long gone. This is an unusual way for the sign of the future to begin, "
                "with something old and weathered, but it sets the real terms early. "
                "Aquarius innovation rarely builds from nothing; it inherits a shelter "
                "built for the collective and asks what that shelter still needs to "
                "become. The mission's walls are plain and functional, built for use "
                "rather than admiration, and that plainness is the point: what lasts is "
                "what actually serves the people inside it.",
     "colors": "A planet at Aquarius 1 often shows a person whose individuality is built "
               "on inherited ground, a structure, a cause, a community, that existed "
               "before they arrived and will likely outlast them. Saturn here favors "
               "durable systems built to serve many rather than showcase one. The Sun "
               "can describe someone whose identity is bound up with stewarding "
               "something communal, weathered but still standing, rather than starting "
               "entirely from scratch.",
     "reflection": "What structure, built long before you arrived, are you now "
                   "responsible for keeping standing?"},
    {"degree": 2,
     "image": "An unexpected thunderstorm breaks overhead without warning.",
     "meaning": "No forecast prepared for this: the sky simply changes its mind, and "
                "everything below has to respond in real time. This is Aquarius meeting "
                "the part of the future it cannot actually predict, the disruption that "
                "arrives regardless of how carefully a system was designed. The storm "
                "isn't punishment, it's just weather doing what weather does, "
                "indifferent to anyone's plans; the only real choice available is how "
                "fast you adapt once it starts. Second-degree Aquarius already knows "
                "the sign's real subject is never control, it's responsiveness.",
     "colors": "A planet here often brings sudden shifts a person could not have "
               "reasonably planned for, and a real gift for adapting once they land. "
               "Uranus, unsurprisingly, feels entirely at home at this degree: abrupt "
               "change that reroutes a plan mid-stride. It rewards building enough "
               "flexibility into a life that the unexpected storm becomes survivable "
               "rather than catastrophic.",
     "reflection": "What unexpected weather has already rerouted your plans this year, "
                   "and how well did you actually move with it?"},
    {"degree": 3,
     "image": "A deserter slips away from his post in the navy.",
     "meaning": "Someone was assigned to a structure and simply left it, choosing "
                "personal conscience or survival over the chain of command that "
                "claimed him. This degree carries real risk along with the departure: "
                "desertion has consequences, and the image doesn't pretend otherwise. "
                "But it also insists that Aquarius's loyalty to the collective is never "
                "unconditional; there is a point at which one person's own judgment "
                "overrides the uniform, and this degree is that point, dramatized. The "
                "sea he leaves behind is vast and organized; the decision to walk off "
                "it is small, private, and irreversible.",
     "colors": "A planet at this degree often shows a willingness to break from an "
               "institution or group that no longer earns loyalty, even at real "
               "personal cost. Uranus or Mars here can describe someone whose "
               "rebellion is principled rather than impulsive, a genuine parting of "
               "ways rather than mere restlessness. It rewards being honest about what "
               "the desertion actually costs, rather than romanticizing the walk away.",
     "reflection": "What post are you still technically holding, out of obligation, "
                   "that you privately deserted a long time ago?"},
    {"degree": 4,
     "image": "A healer trained in an ancient lineage channels a rare gift to restore "
              "someone to wholeness.",
     "meaning": "This degree names a specific, disciplined power: not luck, not magic "
                "in the vague sense, but a trained capacity to move something broken "
                "back toward whole. The healer's authority comes from lineage and "
                "practice, generations of accumulated technique passed hand to hand "
                "until it becomes second nature. Aquarius, so often associated with "
                "the untested and the new, meets here an old and thoroughly proven "
                "skill, and has to admit that some innovations were finished a long "
                "time ago. What heals doesn't need to be new to work.",
     "colors": "A planet at this degree often shows real, trained healing capacity, "
               "whether literal or emotional, drawn from a disciplined tradition "
               "rather than improvised in the moment. Neptune or the Moon here can "
               "indicate someone who restores others to wholeness almost as a matter "
               "of course, gift and training working together. It rewards taking that "
               "capacity seriously as a discipline, not dismissing it as a knack.",
     "reflection": "What have you trained long enough to heal, almost without having "
                   "to think about it anymore?",
     "note": "Note: the 1925 original for this degree used dated ethnic imagery; the "
             "picture above keeps its meaning in respectful, modern terms."},
    {"degree": 5,
     "image": "A council of elders gathers to guide a young leader taking on new "
              "responsibility.",
     "meaning": "Authority here is neither solitary nor entirely new: a whole assembly "
                "of accumulated experience convenes specifically to steady one person "
                "stepping into something larger than themselves. This is Aquarius's "
                "collective instinct doing its most practical work, not abstract "
                "humanitarianism but a literal roomful of people who came before, "
                "making sure what they learned doesn't die with them. The young leader "
                "isn't handed the answers outright; the council is there so the effort "
                "can draw on more than one lifetime's worth of memory.",
     "colors": "A planet at this degree often shows a life supported, visibly or "
               "invisibly, by the accumulated wisdom of people who came before, "
               "mentors, family, a whole lineage of guidance available on request. "
               "Jupiter or Saturn here can describe real strength drawn from "
               "intergenerational counsel rather than pure self-invention. It rewards "
               "actually consulting the council instead of assuming the answers have "
               "to be found alone.",
     "reflection": "Whose accumulated wisdom is quietly available to you right now, if "
                   "you were willing to ask for it?"},
    {"degree": 6,
     "image": "A masked figure performs a solemn ritual at the center of a mystery "
              "play.",
     "meaning": "The mask isn't concealment so much as amplification: whoever wears it "
                "stops being only themselves and becomes a vessel for something older "
                "and larger, a role the whole community needs enacted correctly. This "
                "degree is ceremony that matters, not performance for its own sake, "
                "and Aquarius here discovers that some truths only land when they're "
                "staged rather than merely stated. The mystery in a mystery play is "
                "doctrinal, not vague, a sacred story acted out so a group can "
                "experience meaning together rather than just hear it explained.",
     "colors": "A planet at this degree often shows genuine comfort inhabiting a role "
               "larger than personal identity, speaking or acting for something the "
               "whole group needs voiced. Neptune here can describe real skill at "
               "ritual, performance, or ceremony that carries collective meaning. It "
               "rewards taking the mask seriously as a tool, not a disguise to hide "
               "behind.",
     "reflection": "What role have you put on, not to hide yourself, but to say "
                   "something bigger than yourself out loud?"},
    {"degree": 7,
     "image": "A child is born, emerging from an eggshell rather than the usual way.",
     "meaning": "Even birth, in this degree, happens by unfamiliar means: new life "
                "arriving through a process nobody in the room fully expected. This is "
                "one of the most purely Aquarian images in the whole zodiac, since the "
                "sign's real subject is exactly this, life insisting on finding its "
                "own unconventional route into being. The eggshell breaks because "
                "something inside it was ready, not because anyone outside engineered "
                "the moment; true originality this deep in the sign works the same "
                "way, arriving on its own schedule regardless of how strange the "
                "vehicle looks from outside.",
     "colors": "A planet at this degree often shows a life, idea, or identity that "
               "arrived by an unconventional path and needed exactly that path to "
               "exist at all. Uranus here favors genuinely original beginnings, the "
               "kind that don't fit any existing category cleanly. It rewards trusting "
               "an unusual origin rather than apologizing for it.",
     "reflection": "What part of you arrived by a route so strange that you still have "
                   "trouble explaining how it happened?"},
    {"degree": 8,
     "image": "Wax figures in elaborate gowns stand perfectly still on display.",
     "meaning": "Likeness without life: every detail rendered precisely, the drape of "
                "the fabric, the pose, the expression, and none of it breathing. This "
                "degree examines the difference between representation and reality, "
                "the beautifully finished surface that stands in for a person without "
                "actually being one. There's real craft in the wax figures, real value "
                "even, but Aquarius here is being asked to notice what a perfect copy "
                "still lacks: the unpredictable, unfinished quality of an actual life "
                "in motion.",
     "colors": "A planet at this degree can indicate real skill at presentation, "
               "image, and polish, sometimes at the cost of spontaneity or warmth. "
               "Venus here often shows beauty that is genuinely well-made but "
               "occasionally too composed to feel entirely alive. It rewards asking "
               "whether the gorgeous surface still has a living person underneath it.",
     "reflection": "Where in your life is the presentation so polished that it might "
                   "be standing in for something that stopped moving?"},
    {"degree": 9,
     "image": "A flag, caught by the wind, seems to transform into a rising eagle.",
     "meaning": "Cloth becomes creature: what was only a symbol, sewn and hung to "
                "represent an idea, suddenly appears to take on the living force of "
                "the thing it stood for. This degree is about conviction made kinetic, "
                "an ideal that stops being decorative and starts to act like it "
                "actually believes in itself. Aquarius cares about ideals more than "
                "almost any other sign, and this degree shows what happens when an "
                "ideal finally has enough wind under it to leave the pole.",
     "colors": "A planet at this degree often shows an ideal or cause that has "
               "genuinely come alive in someone's actions, not just their stated "
               "beliefs. Jupiter or Uranus here can indicate a real capacity to make a "
               "symbol functional, to turn stated values into visible motion. It "
               "rewards checking whether your own flag is still just fabric, or "
               "whether it has actually started to fly on its own.",
     "reflection": "Which of your stated ideals has actually grown wings, and which "
                   "one is still just cloth on a pole?"},
    {"degree": 10,
     "image": "A person once treated as the living embodiment of a popular ideal "
              "quietly realizes they were never really that ideal.",
     "meaning": "Fame built around a role rather than a person eventually meets the "
                "person underneath it, and the gap between the two becomes impossible "
                "to ignore. This degree is disillusionment aimed inward: not the crowd "
                "losing interest, but the individual finally seeing clearly that they "
                "were only ever standing in for something the crowd needed to believe "
                "in. There's real grief here, and also, quietly, relief; carrying an "
                "ideal you never actually were is exhausting, and putting it down, "
                "even publicly, can be its own kind of freedom.",
     "colors": "A planet at this degree often shows someone who has been cast, by "
               "others, in a role bigger than their actual self, a face of a cause, a "
               "movement, a family's hopes, and who eventually has to separate their "
               "real identity from the projection. The Sun or Neptune here can "
               "describe fame or reputation that outran the person underneath it. It "
               "rewards telling the truth about the gap sooner rather than later.",
     "reflection": "What ideal have people been projecting onto you that you privately "
                   "know you were never actually living up to?"},
    {"degree": 11,
     "image": "In a quiet hour alone, a person receives an inspiration that could "
              "change the direction of their life.",
     "meaning": "Nothing dramatic happens on the outside: just stillness, and then a "
                "single thought that arrives with enough force to reroute everything "
                "after it. This is Aquarius's real genius degree, proof that the "
                "sign's famous originality doesn't require crowds or noise, only "
                "enough silence for a genuinely new idea to be heard clearly. The "
                "inspiration doesn't announce its own importance; it simply lands, and "
                "the life afterward looks different because someone was quiet enough "
                "to actually receive it.",
     "colors": "A planet at this degree often shows real access to sudden, "
               "life-altering insight, especially in solitude rather than through "
               "outside consultation. Uranus or Neptune here can indicate a genuinely "
               "visionary streak, ideas that arrive fully formed rather than built up "
               "gradually. It rewards protecting enough quiet time for these moments "
               "to actually happen.",
     "reflection": "What idea has already arrived in your quietest hour, waiting for "
                   "you to take it seriously?"},
    {"degree": 12,
     "image": "People of every kind stand together on a vast staircase, arranged rung "
              "by rung from bottom to top.",
     "meaning": "A single structure holds an enormous range of humanity at once, "
                "everyone visible, everyone positioned somewhere on the same climb. "
                "This degree is Aquarius's collective vision made almost "
                "architectural: not everyone at the same level, but everyone genuinely "
                "on the same staircase, part of one continuous human project "
                "regardless of where they currently stand on it. There's hierarchy in "
                "the image, and also real unity, since a staircase, unlike separate "
                "rooms, is one connected structure the whole time.",
     "colors": "A planet at this degree often shows a strong awareness of humanity as "
               "one interconnected project, with real attention to where different "
               "people currently stand within it. Jupiter or an eleventh-house "
               "placement here can favor work in social systems, education, or any "
               "structure meant to move a wide range of people upward together. It "
               "rewards remembering that the staircase is shared, even when the "
               "positions on it are not equal.",
     "reflection": "Who is standing several steps below or above you on the same "
                   "staircase, and how much of the whole climb are you actually "
                   "seeing?"},
    {"degree": 13,
     "image": "A barometer registers the coming change in pressure before the weather "
              "itself arrives.",
     "meaning": "This instrument doesn't cause anything; it simply reads what's "
                "already building in the air and reports it honestly, ahead of time. "
                "Aquarius, the sign most associated with foresight and the future, "
                "gets here a literal tool for exactly that gift: sensitivity fine "
                "enough to register a shift before it's obvious to everyone else. The "
                "barometer's value is entirely in its honesty, since a reading that "
                "flatters instead of informs is worse than no instrument at all.",
     "colors": "A planet at this degree often shows genuine sensitivity to shifting "
               "conditions, social, emotional, atmospheric, well before those shifts "
               "become visible to everyone else. Mercury or Uranus here can indicate a "
               "real talent for early, accurate forecasting, in weather, markets, or "
               "mood. It rewards trusting your own readings even when the sky outside "
               "still looks calm.",
     "reflection": "What pressure have you already sensed building, that the people "
                   "around you haven't noticed yet?"},
    {"degree": 14,
     "image": "A train enters a tunnel, and its interior view goes dark.",
     "meaning": "Momentum continues, but visibility disappears entirely: this is a "
                "stretch of the journey that has to be traveled by trust rather than "
                "sight. Aquarius, oriented so strongly toward what's ahead, meets here "
                "a passage where the future is briefly unreadable, and the only real "
                "choice is to keep moving at the same speed rather than stop inside "
                "the dark. The tunnel has an end; the discomfort is temporary, but "
                "it's real while it lasts, and this degree doesn't pretend otherwise.",
     "colors": "A planet at this degree often shows a capacity to keep functioning "
               "through a stretch of genuine uncertainty, trusting the track even when "
               "nothing outside the window confirms it. Pluto or Saturn here can "
               "indicate real resilience through opaque, disorienting transitions. It "
               "rewards staying on schedule through the dark part rather than assuming "
               "the tunnel means the journey has failed.",
     "reflection": "What tunnel are you currently moving through, on trust alone, with "
                   "no clear view of what's on the other side yet?"},
    {"degree": 15,
     "image": "Two lovebirds perch together on a fence, singing.",
     "meaning": "Simple, mutual, unforced companionship: nothing about this image asks "
                "for more than what it already has. The fence itself is a boundary, "
                "ordinary and unremarkable, and the birds have made it into a "
                "perfectly good place to be together. This is the midpoint of "
                "Aquarius, the sign that can run cool and abstract, landing on "
                "something this warm and specific: two beings, side by side, content "
                "in a small shared moment rather than reaching for anything grander.",
     "colors": "A planet at this degree often shows real ease in close, easy "
               "companionship, partnership that doesn't need grand gestures to feel "
               "complete. Venus here is especially at home, favoring relationships "
               "built on simple daily contentment rather than drama. It rewards "
               "noticing when a small, ordinary togetherness is already, quietly, "
               "enough.",
     "reflection": "Which relationship in your life is already the fence and the "
                   "song, needing nothing more added to it?"},
    {"degree": 16,
     "image": "A powerful businessman works alone at his desk, running his "
              "enterprise.",
     "meaning": "Command exercised quietly, through paperwork and decisions rather "
                "than public display: this degree is authority at its most private "
                "and procedural. Nobody is watching the desk directly, and that's "
                "precisely where the real influence gets exercised, deal by deal, "
                "decision by decision. Aquarius's relationship to power is often "
                "collective and idealistic, but this degree insists that some of the "
                "sign's real leverage on the future gets built in exactly this "
                "unglamorous, solitary way.",
     "colors": "A planet at this degree often shows real capacity for sustained, "
               "private command, influence built through consistent work rather than "
               "visible spectacle. Saturn or the Sun here can indicate someone who "
               "runs something substantial and does it mostly out of view. It rewards "
               "respecting the desk work as much as any more visible form of "
               "leadership.",
     "reflection": "What are you quietly running from your own desk, that the world "
                   "has no idea carries as much weight as it does?"},
    {"degree": 17,
     "image": "A watchdog stands alert, guarding his master's home.",
     "meaning": "Loyalty here is vigilance, not affection on display: the dog's whole "
                "purpose is attentiveness to threat, ready to act the instant it's "
                "needed and otherwise simply present. This degree honors protection "
                "as a genuine form of devotion, unglamorous and constant, the kind of "
                "care that mostly goes unnoticed precisely because it's doing its job. "
                "Aquarius can run detached, but this degree shows the sign fiercely "
                "committed to guarding something specific.",
     "colors": "A planet at this degree often shows real protective instinct toward "
               "people, property, or causes, a readiness to act that doesn't require "
               "drama to stay switched on. Mars or Saturn here can indicate someone "
               "reliably alert to threats that others miss entirely. It rewards "
               "recognizing your own vigilance as care, not just as suspicion.",
     "reflection": "What, or who, have you been quietly guarding, without asking for "
                   "any credit for the watching?"},
    {"degree": 18,
     "image": "A man's true motives are exposed, publicly and without his consent.",
     "meaning": "Whatever was hidden behind a careful performance gets pulled into "
                "daylight, and there's no controlling how the room reacts once it's "
                "out. This degree carries real discomfort, since exposure of this "
                "kind is rarely chosen by the person it happens to; it arrives, and "
                "the only remaining choice is how to stand there once it has. "
                "Aquarius values honesty in the abstract, as a principle, and this "
                "degree makes it uncomfortably concrete and personal.",
     "colors": "A planet at this degree can indicate real vulnerability around having "
               "private motives revealed before they're ready to be shared, or "
               "genuine skill at seeing through other people's masks. Pluto or "
               "Mercury here often shows a sharp eye for what's actually driving "
               "someone's behavior underneath their stated reasons. It rewards "
               "getting honest about your own motives before circumstance does it for "
               "you.",
     "reflection": "What motive of yours would genuinely surprise the people who "
                   "think they already understand why you do what you do?"},
    {"degree": 19,
     "image": "A forest fire is finally brought under control through water, "
              "chemicals, and sheer physical effort.",
     "meaning": "Nothing about this containment is elegant; it takes every available "
                "method, applied hard and without much grace, to stop something that "
                "was genuinely threatening to spread past saving. This degree honors "
                "effective crisis response over stylish response, the unglamorous, "
                "all-hands reality of actually putting out what's burning. Aquarius's "
                "instinct toward the collective shows up here in its most practical "
                "form: a whole group, pooling every resource they have, because the "
                "emergency doesn't care how tired anyone already is.",
     "colors": "A planet at this degree often shows real capacity to mobilize "
               "decisively in a genuine emergency, using whatever tools are actually "
               "available rather than waiting for the ideal ones. Mars or Pluto here "
               "can indicate someone effective under real pressure, unbothered by the "
               "mess of the response as long as it works. It rewards trusting brute, "
               "coordinated effort over waiting for a cleaner solution.",
     "reflection": "What is currently burning in your life that needs every available "
                   "resource thrown at it now, gracefully or not?"},
    {"degree": 20,
     "image": "A large white dove flies in, carrying a message.",
     "meaning": "Communication arrives on its own wings, delivered by something whose "
                "whole purpose is safe passage of the word rather than the word "
                "itself. This degree trusts the messenger completely: the dove "
                "doesn't editorialize, it simply carries what it was given and lands "
                "where it's needed. Aquarius, so oriented toward transmission of "
                "ideas across distance, gets here its clearest image of information "
                "traveling cleanly, without static, straight to the person meant to "
                "receive it.",
     "colors": "A planet at this degree often shows real facility as a messenger, "
               "someone information reliably travels through, trusted precisely "
               "because they deliver things intact. Mercury here is especially at "
               "home, favoring clean, honest transmission over distorted or "
               "self-serving relay. It rewards taking the responsibility of carrying "
               "a message seriously, since a dove that drops it partway is no help to "
               "anyone.",
     "reflection": "What message have you been trusted to carry, and are you "
                   "delivering it exactly as it was given to you?"},
    {"degree": 21,
     "image": "A woman, disappointed and disillusioned, faces a life that suddenly "
              "looks empty, and does so with real courage.",
     "meaning": "The hope that organized her expectations has collapsed, and what's "
                "left is bare: no comforting illusion left standing, just the actual "
                "shape of her circumstances. This degree doesn't rush to console; it "
                "sits with real disappointment and asks what courage looks like once "
                "the fantasy is gone. Aquarius's idealism runs high, and this degree "
                "shows what happens when the ideal doesn't arrive, and the sign has "
                "to find out whether its commitment to the future can survive contact "
                "with genuine loss.",
     "colors": "A planet at this degree often shows someone who has faced real "
               "disillusionment and kept standing anyway, courage built specifically "
               "from disappointment rather than in spite of it. Saturn or Chiron here "
               "can describe a hard-won, unsentimental resilience. It rewards "
               "honoring what was actually lost, rather than skipping straight to "
               "forced optimism.",
     "reflection": "What illusion have you already had to let go of, and what does "
                   "your courage actually look like now that it's gone?"},
    {"degree": 22,
     "image": "A soft rug is laid across a nursery floor so children can play in "
              "comfort and warmth.",
     "meaning": "Deliberate, practical tenderness: someone thought ahead about small "
                "knees and bare feet, and did something concrete about it before the "
                "children ever arrived to need it. This degree is care planned in "
                "advance, not care improvised in the moment, the kind of preparation "
                "that makes an ordinary room genuinely safer for whoever is smallest "
                "in it. Aquarius's humanitarian instinct gets its most domestic, "
                "tender expression here, less about grand causes and more about one "
                "warm floor, ready.",
     "colors": "A planet at this degree often shows real foresight in preparing "
               "comfort for others, especially the young or vulnerable, before it's "
               "asked for. The Moon or Venus here can indicate genuine talent for "
               "making an ordinary space feel safe and warm through small, deliberate "
               "choices. It rewards remembering that humanitarian instinct is often "
               "exactly this small and this concrete.",
     "reflection": "What floor have you already softened for someone smaller or more "
                   "vulnerable than you, before they even had to ask?"},
    {"degree": 23,
     "image": "A big bear sits back on its haunches, waving both its paws.",
     "meaning": "Something enormous and genuinely capable of harm chooses, in this "
                "moment, to be almost comic, playful in a way its size makes "
                "disarming rather than threatening. This degree carries real power "
                "held loosely, strength that doesn't need to prove itself through "
                "force because it's secure enough to be silly instead. Aquarius, "
                "which can run cerebral and detached, gets here a reminder that real "
                "strength sometimes looks like play, not display.",
     "colors": "A planet at this degree often shows considerable underlying power "
               "expressed through warmth or humor rather than intimidation. Jupiter "
               "here can indicate someone genuinely formidable who chooses, most of "
               "the time, to be approachable instead. It rewards trusting that your "
               "own strength doesn't need to be constantly demonstrated to be real.",
     "reflection": "Where in your life have you been holding real strength loosely, "
                   "choosing warmth over the display of force you actually have "
                   "available?"},
    {"degree": 24,
     "image": "A man who has mastered his own passions now teaches others, drawing "
              "entirely from what he lived through.",
     "meaning": "Wisdom offered here isn't theoretical; it's the residue of real "
                "struggle, converted into something useful for someone else's "
                "journey. This degree honors the specific authority of lived "
                "experience over borrowed doctrine, a teacher whose only real "
                "credential is having actually gone through it and come out the "
                "other side able to say something true. Aquarius cares about the "
                "future of the whole group, and this degree shows exactly how one "
                "person's hard-won mastery becomes a gift the collective can use.",
     "colors": "A planet at this degree often shows real teaching authority earned "
               "through personal struggle rather than credentialed study alone. "
               "Saturn or Jupiter here can indicate a mentor whose lessons carry "
               "weight precisely because they were lived first. It rewards trusting "
               "your own overcome passions as legitimate material to teach from.",
     "reflection": "What have you already lived through and mastered that could "
                   "genuinely teach someone else, if you were willing to offer it?"},
    {"degree": 25,
     "image": "A butterfly's right wing has formed more perfectly than its left.",
     "meaning": "Even a creature built for symmetry turns out slightly, visibly "
                "uneven, and the imperfection doesn't stop it from flying, it just "
                "changes how the flight looks. This degree quietly argues against the "
                "idea that beauty requires perfect balance; asymmetry here is simply "
                "part of the actual creature, not a flaw waiting to be corrected. "
                "Aquarius, which so often idealizes the perfected future, meets here "
                "a small, honest reminder that real, functioning things are rarely "
                "flawless, and fly anyway.",
     "colors": "A planet at this degree often shows real beauty or capability that "
               "carries a visible, characterful imperfection rather than flawless "
               "symmetry. Venus here can indicate charm that comes specifically from "
               "being a little uneven, not despite it. It rewards trusting that the "
               "less perfect wing still gets you off the ground.",
     "reflection": "What part of you formed a little unevenly, and has it actually "
                   "stopped you from flying?"},
    {"degree": 26,
     "image": "A mechanic tests a car's battery, reading its charge with a "
              "hydrometer.",
     "meaning": "Before anyone trusts the engine to run, someone checks the stored "
                "power directly, measuring what's actually there rather than "
                "assuming based on how the car looks. This degree is diagnostic "
                "honesty applied to potential energy: not romantic, entirely "
                "practical, the unglamorous discipline of testing capacity before "
                "relying on it. Aquarius cares deeply about what the future can run "
                "on, and this degree insists on actually measuring the charge first.",
     "colors": "A planet at this degree often shows a talent for accurately assessing "
               "someone's or something's real reserves, energy, resources, "
               "readiness, before committing to depend on them. Mercury or Saturn "
               "here can indicate genuine diagnostic skill, technical or emotional. "
               "It rewards checking the actual charge rather than assuming the "
               "battery is full.",
     "reflection": "What in your life have you been running on, without ever "
                   "actually testing how much charge is really left?"},
    {"degree": 27,
     "image": "An old pottery bowl, ancient in make, sits filled with freshly cut "
              "violets.",
     "meaning": "Something durable and inherited holds something delicate and brand "
                "new, and the pairing works: the old vessel doesn't diminish the "
                "fresh flowers, it gives them a worthy, proven place to be. This "
                "degree is continuity and renewal held in the same object at once, "
                "tradition offering itself as a container for whatever is currently, "
                "newly, alive. Aquarius, future-facing as it is, is reminded here that "
                "the vessel carrying the new thing forward doesn't have to be new "
                "itself.",
     "colors": "A planet at this degree often shows fresh energy or new beginnings "
               "that thrive specifically because they're held within something older "
               "and more established. Venus or Saturn here can indicate a gift for "
               "pairing tradition with genuine renewal rather than treating them as "
               "opposites. It rewards trusting an old container to actually hold your "
               "newest thing well.",
     "reflection": "What old, proven vessel in your life is currently holding "
                   "something brand new, and holding it well?"},
    {"degree": 28,
     "image": "A tree is cut down and sawed into logs, stored up for winter's "
              "supply.",
     "meaning": "Something living is deliberately ended so that warmth and fuel exist "
                "later, when the season turns hard. This degree doesn't flinch from "
                "the cost: the tree is genuinely gone, and the sawing is real labor, "
                "but the winter ahead is real too, and this is how a household "
                "actually survives it. Aquarius plans for the collective future, and "
                "this degree shows the sign willing to make a hard, concrete choice "
                "now so that a whole household stays warm later.",
     "colors": "A planet at this degree often shows a willingness to make a "
               "difficult, even costly choice now specifically to secure resources "
               "for a harder season ahead. Saturn here is especially at home, "
               "favoring practical foresight over sentimentality when provision is "
               "genuinely at stake. It rewards making the cut before winter arrives, "
               "not scrambling for wood once it has.",
     "reflection": "What have you already had to fell and cut, so that you'd actually "
                   "have enough stored up for what's coming?"},
    {"degree": 29,
     "image": "A butterfly finally breaks free of its chrysalis.",
     "meaning": "The transformation that has been happening invisibly, inside a "
                "sealed case, finally becomes visible: what emerges is not a "
                "repaired caterpillar, it's something entirely different that was "
                "built the whole time it looked like nothing was happening. This is "
                "one of the zodiac's clearest metamorphosis images, and this deep "
                "into Aquarius, the sign that lives for genuine transformation gets "
                "to watch its own patient, private process finally show itself. "
                "Nothing about the chrysalis stage looked like progress from outside; "
                "this degree is proof that it was.",
     "colors": "A planet at this degree often shows a genuine capacity for real "
               "transformation, especially after a long private period that looked, "
               "from outside, like nothing was happening. Uranus or Pluto here can "
               "indicate emergence into a form the person's earlier self would "
               "barely recognize. It rewards trusting the quiet chrysalis stage as "
               "real work, not stalled time.",
     "reflection": "What have you been quietly transforming into, inside your own "
                   "sealed chrysalis, that's finally ready to be seen?"},
    {"degree": 30,
     "image": "A once-barren field from an old story blooms again, and a whole "
              "community gathers there, bound together by something larger than any "
              "one of them.",
     "meaning": "Aquarius closes not with a solitary achievement but with a shared "
                "flowering: ground that was once desolate now blooms, and it isn't "
                "one person's private garden, it's a whole community's renewal, "
                "arrived at together. This final degree is the sign's real "
                "culmination, since everything Aquarius has been reaching for across "
                "the whole thirty degrees, the collective good, the humane future, "
                "minds joined rather than merely adjacent, arrives here as an actual, "
                "visible bloom rather than a stated ideal. It closes the sign, and "
                "closes the story that began with a mission's plain walls in degree "
                "one: from shelter, all the way to a field in flower, tended by "
                "everyone who ever believed it could be.",
     "colors": "A planet at this degree often shows real fulfillment found "
               "specifically in shared, collective flourishing rather than solitary "
               "achievement, a sense of belonging to something whose renewal "
               "outlasts any one person's part in it. Jupiter or Neptune here can "
               "indicate genuine spiritual or communal culmination, arriving late "
               "and earned. It rewards recognizing when the field has actually, "
               "finally, bloomed, and letting yourself stand in it with everyone else "
               "who helped it grow.",
     "reflection": "What field have you been quietly helping tend, that is only now, "
                   "finally, coming into bloom?"},
]

assert len(ENTRIES) == 30, f"expected 30 Aquarius degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Aquarius degrees out of order"
