"""Sabian symbol data for Libra.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (astronarrative.com, jamesburgess.com
/ Sacred 7 Academy [two separate pages, both matching], cafeastrology.com's
rendering of Dane Rudhyar's "An Astrological Mandala" extended phrasing,
and kerykeion.net for degrees 1-27 and 29-30) before being hand-typed. One
discrepancy surfaced: kerykeion.net's text for degree 28 ("a man alone in
deep gloom, unnoticed angels come to his aid") did not match any other
source consulted and was rejected in favor of the reading confirmed by
astronarrative.com, both jamesburgess.com pages, cafeastrology.com/Rudhyar
("a man becoming aware of spiritual forces surrounding and assisting him"),
and independent confirmation from sabian-calculator.com, boveeastrology.com,
saijin's Sabian Symbol Septenary, and Judith deHaan's Substack, all of which
give "a man in the midst of brightening influences" for Libra 28. Do NOT
extend this list, or write a new sign's list, without the same verification
discipline: fewer verified degrees beats any guessed ones.

DATED-SYMBOL POLICY CHECK: all 30 degrees were reviewed against Shannon's
dated/ethnically-charged-imagery policy (see SCHEMA.md). None of Libra's
traditional 30 images depict a stereotyped ethnic figure, a named literary
slave character, or an ethnic slur of the kind flagged elsewhere in this
project (e.g. Taurus 24/27, Gemini 12/18/27). Degree 20's original text
("a Jewish rabbi") names a religious office respectfully, the same way
other signs' data files name professions (a nurse, a professor, a sea
captain) without a note; it is rendered here as "a rabbi" performing his
ordinary duties. Degree 2's original text references Theosophical "root
race" doctrine ("the light of the sixth race transmuted to the seventh"),
an esoteric evolutionary-era concept, not a real-world ethnic category;
`image` restates its core idea (light transmuted from a completed cycle
into a new one) without reproducing that vocabulary at all. No degree in
this file carries a `note` field.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a canoe glides
out onto calm water after dangerous rapids"), not a verbatim quote of
Marc Edmund Jones' 1953 book or Dane Rudhyar's "An Astrological Mandala"
(1973) wording. `meaning`, `colors`, and `reflection` are original
Twelve Rooms interpretation, written fresh for this project; none of it
is copied from Jones or Rudhyar.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Libra", "slug": "libra", "glyph": "♎︎", "order": 7}

# The 30 degrees of Libra, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str). See SCHEMA.md for what each field means.
ENTRIES = [
    {'degree': 1,
     'image': "A butterfly's wings are pinned into their final, perfect shape by a "
              'dart driven straight through its body.',
     'meaning': 'A creature already whole gets pierced clean through, and only then '
                'counts as finished. Libra opens the wheel of relationship this way on '
                'purpose: harmony is not the absence of a wound, it is what settles '
                'once the wound has actually been taken and the wings still hold their '
                'shape. Nothing about the dart is gentle, and nothing about the '
                'butterfly pretends otherwise. The degree simply insists that some '
                'beauty needs exactly this kind of piercing to become permanent '
                'instead of merely pretty.',
     'colors': 'A planet at Libra 1 often carries beauty, charm, or grace that only '
               'became durable after real damage, elegance that was tested rather '
               'than simply inherited. Venus here favors a poise built through '
               'something sharp, not around it. On an angle, it can describe someone '
               'whose calm reads as effortless because the piercing that produced it '
               'already happened, out of view.',
     'reflection': 'What pierced you cleanly enough to set your shape for good, '
                   'instead of ruining it?'},
    {'degree': 2,
     'image': "A whole era's accumulated light converts, in a single moment, into the "
              'seed-light of the era just beginning.',
     'meaning': 'A stretch of accumulated brightness turns, all at once, into fuel for '
                'whatever comes next, nothing wasted, nothing carried over unchanged '
                'either. This is the first fully Libran move in the sign: not addition '
                'or subtraction, but exchange, one completed thing becoming the raw '
                'material of the thing that follows it. There is no mourning in the '
                'image, only conversion, the sense that endings this clean are rare '
                'enough to be worth noticing when they actually happen.',
     'colors': 'A planet at this degree often shows real capacity to take what an '
               'earlier phase, or self, already built and convert it cleanly into the '
               "next one's fuel, without loss in the transaction. Saturn or the Sun "
               'here can indicate a life that ages by transmutation rather than mere '
               'accumulation, each stage genuinely finishing before the next begins. '
               'On the IC, it can describe inheritance handled so well that nothing of '
               'the original value goes missing.',
     'reflection': "What have you been quietly building long enough that it's finally "
                   'ready to become something else?'},
    {'degree': 3,
     'image': 'Sunrise breaks over a landscape, and every single thing in it looks '
              'different than it did the night before.',
     'meaning': "Morning arrives, and the whole visible world is suddenly a different "
                'one, not because anything was rebuilt overnight but because the light '
                "itself changed what can be seen. This degree trusts that "
                "transformation doesn't always require effort, sometimes it only "
                'requires the sun coming up on a situation that was already different '
                "and simply hadn't been looked at properly yet. Libra, forever "
                'weighing what it perceives, gets here the reminder that perception '
                'itself can be the whole revolution.',
     'colors': 'A planet at this degree often marks sudden clarity or a shift in '
               "outlook that makes a situation genuinely legible in a way it wasn't "
               'the night before. The Sun or Uranus here can indicate real capacity '
               'for abrupt, total reframes rather than slow revision. On the '
               'Ascendant, it can describe someone whose whole presentation seems to '
               'reset overnight, more than once in a life.',
     'reflection': "What already changed, that you're only now, this morning, "
                   'actually able to see?'},
    {'degree': 4,
     'image': 'A circle of young people sit together around a campfire, quietly '
              'attuned to something larger than themselves.',
     'meaning': 'Several people, gathered by a small fire, are present to each other '
                'and to something beyond any one of them alone. This degree is '
                'company at its most Libran: not a crowd, not a pair, a circle, '
                "exactly the shape that lets everyone see everyone else's face by the "
                "same light. What's shared here isn't information, it's presence, the "
                'kind that only happens when a group agrees, wordlessly, to sit still '
                'together instead of scattering.',
     'colors': 'A planet at this degree often favors real belonging inside a small, '
               'intentional circle, connection built on shared attention rather than '
               'shared task. Neptune or Venus here can indicate a genuine gift for '
               'creating the kind of gathering people remember for years afterward. '
               'On the eleventh house, it can describe friendships that function '
               'closer to communion than mere company.',
     'reflection': "Which circle are you actually present in, all the way, rather "
                   'than merely attending?'},
    {'degree': 5,
     'image': 'A teacher lays out for his students, from the ground up, the inner '
              'knowledge a whole new way of living could be built on.',
     'meaning': 'Teaching, here, is not information transfer, it is a foundation laid '
                'in full view so students can build an entire new structure on top of '
                'it later. This degree trusts that some knowledge has to be handed '
                'over completely, first principles included, or the thing being '
                "taught can never actually support what comes next. Libra's fairness "
                'shows up as intellectual generosity: nothing withheld, nothing kept '
                "back to protect the teacher's advantage.",
     'colors': 'A planet at this degree often shows a genuine gift for teaching from '
               'first principles rather than surface technique, building others up '
               'rather than keeping the real knowledge private. Mercury or Jupiter '
               'here can favor a mentor whose students go on to build something the '
               'teacher never got to see finished. On the Midheaven, it can describe '
               'a career defined by what it hands forward, not what it holds back.',
     'reflection': "What foundation have you actually shown someone in full, instead "
                   'of keeping the key piece to yourself?'},
    {'degree': 6,
     'image': 'A man watches an idea he has long held privately finally take on '
              'visible, solid form in front of him.',
     'meaning': 'An inner picture finally hardens into something that can be touched, '
                'and the man gets to witness his own imagining become real while he '
                'watches. This degree honors the quiet drama of hope stopping being '
                'hope and starting to be fact, the gap between wanting and having '
                'closing in real time. Libra prizes exactly this kind of '
                'confirmation, proof that discernment, held patiently enough, '
                'actually produces the thing it pictured.',
     'colors': 'A planet at this degree often shows real ability to manifest a '
               'clearly held vision into concrete form, patient enough to let '
               'imagination finish its work before demanding proof. Venus or Saturn '
               'here can favor someone whose ideals were never naive, only early. On '
               'the second house, it can describe values that eventually, reliably, '
               'become material reality.',
     'reflection': 'Which of your ideals is currently in the middle of becoming '
                   'solid, right in front of you, if you actually watch closely '
                   'enough to notice?'},
    {'degree': 7,
     'image': 'A woman scatters feed for her chickens while keeping a careful eye on '
              'the hawks circling above.',
     'meaning': 'Nourishing and defending happen in the same gesture here, the same '
                'hand that scatters feed also has to watch the sky. This degree '
                'refuses to separate care from vigilance: real tending always '
                'includes a threat assessment, and pretending otherwise just leaves '
                "what you're feeding exposed. Libra's harmony was never passive, and "
                'this is the proof, peace kept by someone actively standing between '
                "what's vulnerable and what would take it.",
     'colors': 'A planet at this degree often shows real capacity to nurture and '
               'defend at once, protection folded into the same instinct as care '
               'rather than treated as a separate job. The Moon or Mars here can '
               'favor someone who feeds people and watches the door for them at the '
               'same time. On the fourth house, it can describe a home life where '
               'tenderness and vigilance were always the same skill.',
     'reflection': 'What are you currently feeding that also needs you watching the '
                   'sky above it?'},
    {'degree': 8,
     'image': 'A fireplace still blazes with warmth inside a house that has been '
              'completely emptied of people.',
     'meaning': "Warmth keeps burning in a house nobody is left in, heat and light "
                'doing their whole job for an audience of no one. This degree carries '
                "real ache: the fire didn't fail, the home did, and the gap between "
                'the two is the entire feeling of the image. Libra, which measures '
                'things by relationship, meets here its opposite, comfort with '
                'nothing left to relate to, and has to reckon honestly with what that '
                'costs.',
     'colors': 'A planet at this degree can indicate warmth or resource that keeps '
               'being generated even after the relationship or household it was '
               'meant for has emptied out. Venus or the fourth house here can '
               'describe someone maintaining a capacity for closeness that currently '
               'has nowhere to land. It rewards asking honestly whether the fire is '
               'still worth tending, or whether it is time to let it go out and '
               'build a new one elsewhere.',
     'reflection': 'What warmth are you still keeping lit for a house that emptied '
                   'out a while ago?'},
    {'degree': 9,
     'image': 'Three works by old master painters hang together in their own '
              'dedicated room of a gallery.',
     'meaning': 'Excellence, hung together on purpose, so it can be studied side by '
                'side instead of admired one canvas at a time. This degree is '
                "Libra's aesthetic judgment at its most disciplined: not just liking "
                'beautiful things, but curating them, deciding which three belong in '
                'the same room because together they teach something none of them '
                'could alone. Comparison, done with real taste, becomes its own form '
                'of insight.',
     'colors': 'A planet at this degree often shows a refined, comparative eye, the '
               'ability to place excellent things next to each other and see exactly '
               "what each one is doing that the others aren't. Venus here favors real "
               'connoisseurship, judgment trained rather than merely inherited. On '
               'the fifth house, it can describe creative work built by studying '
               'masters closely enough to know precisely what to take from each.',
     'reflection': 'Which three influences would you actually hang together in your '
                   'own private gallery, and what would they teach each other?'},
    {'degree': 10,
     'image': 'A canoe, having just come through a stretch of dangerous rapids, '
              'glides out onto calm, safe water.',
     'meaning': 'The hard part is already behind the boat, the water ahead is smooth, '
                'and the degree captures the exact exhale after danger, still close '
                "enough to feel, already far enough to trust. Libra's whole project "
                'is finding the calm water, and this degree shows what it actually '
                'looks like to arrive there, not by avoiding the rapids but by '
                'getting all the way through them intact.',
     'colors': 'A planet at this degree often shows real skill at navigating genuine '
               'danger cleanly enough to reach lasting stability afterward, not luck, '
               'method. Neptune or Mars here can favor someone who steers well under '
               'real pressure and knows the instant the water changes. On the '
               'seventh house, it can describe a partnership that survived its '
               'roughest water and now, provably, floats easily.',
     'reflection': "What rapids are you already through, that you haven't yet let "
                   'yourself fully believe are behind you?'},
    {'degree': 11,
     'image': 'A professor lowers his glasses to look directly, closely, at the '
              'students in front of him.',
     'meaning': "A small, exact gesture, glasses lowered just enough to see clearly, "
                'carries a whole relationship of authority and attention in one '
                "motion. This degree is Libra's discernment made almost precise: not "
                "a lecture, just a look that says the professor is actually paying "
                "attention to who's in the room and how they're doing. Judgment, "
                'here, is careful and completely without theater.',
     'colors': 'A planet at this degree often shows real discernment expressed '
               'through close, individual attention rather than broad instruction, '
               'someone who notices exactly who needs what. Mercury or Saturn here '
               'can favor a teacher, mentor, or evaluator whose judgment is trusted '
               'because it is so specific. On the sixth house, it can describe '
               'expertise applied one careful case at a time.',
     'reflection': 'Who is currently getting your full, close attention, over the '
                   'glasses, rather than your general one?'},
    {'degree': 12,
     'image': 'A group of miners climbs back up out of a deep coal mine and into '
              'daylight.',
     'meaning': 'People who went deep into the dark, doing hard, unglamorous work '
                'below the surface, come back up into the light. This degree marks '
                'the relief of resurfacing, proof that whatever was extracted down '
                'there is now finally being brought where it can actually be used. '
                'Libra rarely goes underground by nature, so this degree matters as '
                'testimony: some balance is only earned after real time spent '
                'somewhere far less balanced.',
     'colors': 'A planet at this degree often shows genuine resilience after '
               'prolonged, difficult, mostly invisible effort, someone who has real '
               'evidence they can go all the way down and still come back. Pluto or '
               'Saturn here can favor depth of experience that only shows once the '
               'person actually surfaces and speaks about it. On the eighth house, it '
               'can describe transformation that happened entirely out of sight '
               'before it became visible.',
     'reflection': 'What have you been quietly mining in the dark that is finally '
                   'ready to come up into the light?'},
    {'degree': 13,
     'image': 'A group of children blow soap bubbles, delighted by each perfect, '
              'short-lived globe.',
     'meaning': 'Something perfect, round, and gorgeous, made from almost nothing, '
                'built to last only seconds before it pops. This degree is pure, '
                "unguarded delight, play that doesn't ask its creation to be "
                "permanent to be worth doing. Libra's love of beauty finds here its "
                'lightest form, symmetry enjoyed purely for the moment it exists, no '
                'attachment required to the moment after.',
     'colors': 'A planet at this degree often shows real pleasure in creating '
               "beautiful, ephemeral things, art or joy that doesn't need to last to "
               'count as successful. Venus or the fifth house here can favor a '
               'playful aesthetic sense, delight taken in the making more than the '
               'keeping. It rewards letting some beautiful things pop without '
               'grieving them.',
     'reflection': 'What have you made recently that was gorgeous, round, and never '
                   'meant to last, and did you enjoy it anyway?'},
    {'degree': 14,
     'image': 'In the full heat of midday, a man stops everything to take a siesta.',
     'meaning': 'The hottest, brightest part of the day gets met with rest instead of '
                'effort, a deliberate pause exactly when the pressure to keep working '
                'is highest. This degree honors timing over willpower: knowing when '
                'not to push is its own discipline, one Libra, tuned to conditions '
                'rather than schedules, understands instinctively. Nothing about the '
                "siesta is laziness, it's precision about when output actually costs "
                "more than it's worth.",
     'colors': 'A planet at this degree often shows real wisdom about pacing, rest '
               'taken deliberately at the point of highest demand rather than after '
               'collapse. The Moon or Saturn here can favor someone who reads their '
               'own limits accurately and honors them on schedule. On the sixth '
               'house, it can describe a work rhythm built around real rest, not '
               'stolen rest.',
     'reflection': 'What is the noon hour in your life right now, and are you '
                   'actually resting through it, or pushing straight past it?'},
    {'degree': 15,
     'image': 'A set of paths curve back on themselves rather than running in a '
              'straight line.',
     'meaning': "Paths that loop rather than run straight, the exact midpoint of "
                "Libra's own thirty degrees, and a shape the sign recognizes "
                'instantly: not a dead end, not a shortcut, a curve that keeps '
                'returning you to somewhere already visited, a little changed each '
                'time. This degree names the whole method of balance itself, not a '
                'single decisive line but a continuous, adjusting circling that '
                'never quite stops correcting course.',
     'colors': 'A planet at this degree often shows a life or a mind that circles a '
               'subject repeatedly rather than settling it once, gaining real '
               'understanding through return rather than through a single pass. '
               'Neptune or Venus here can favor thinking or feeling that works best '
               'in loops, revisiting in order to refine. On an angle, it can '
               'describe someone whose growth looks cyclical rather than linear, and '
               'is no less real for it.',
     'reflection': "What are you circling back to again, and what does this pass "
                   "teach you that the last one didn't?"},
    {'degree': 16,
     'image': 'After a storm has passed, a boat landing is left damaged and waiting '
              'to be rebuilt.',
     'meaning': "Something that used to make arrival possible got damaged by "
                'conditions nobody controlled, and now the real work is rebuilding '
                'the place where people cross from water to solid ground. This '
                'degree is honest about aftermath: Libra prefers calm, but storms '
                'happen anyway, and this one is specifically about the unglamorous, '
                'necessary labor of restoring passage once the weather has already '
                'done its damage.',
     'colors': 'A planet at this degree often shows real capacity to rebuild '
               'connection or access after genuine disruption, patient '
               'reconstruction rather than resentment at the storm. Saturn or Mars '
               'here can favor someone who repairs what breaks rather than '
               'abandoning the crossing point. On the fourth or seventh house, it '
               'can describe a relationship or home rebuilt, structurally, after '
               'real damage.',
     'reflection': 'What landing point in your life is still waiting on you to '
                   'actually rebuild it, the storm long since passed?'},
    {'degree': 17,
     'image': 'A retired sea captain stands on shore, watching ships arrive at and '
              'leave the harbor.',
     'meaning': 'Someone who spent a whole working life at sea now stands on shore '
                'and watches other vessels come and go, done with the voyage but not '
                'with the water. This degree honors expertise that does not '
                'disappear just because the active career ended, a trained eye that '
                "still reads wind and tide correctly from dry land. Libra respects "
                'this kind of earned perspective, judgment that gets sharper with '
                'distance rather than duller.',
     'colors': 'A planet at this degree often shows real authority built from direct '
               'experience, wisdom that keeps being useful long after the active '
               'role has ended. Saturn or Jupiter here can favor a mentor or advisor '
               "whose read on a situation is trusted precisely because they've "
               'actually lived it, not just studied it. On the tenth house, it can '
               "describe a second-act career built entirely on hard-earned "
               "first-act knowledge.",
     'reflection': 'What harbor are you now watching over with earned expertise, '
                   'instead of actively sailing through it yourself?'},
    {'degree': 18,
     'image': 'Two men are taken into custody and placed under arrest.',
     'meaning': "Consequence, applied visibly and without private negotiation, to "
                "more than one person at once. This degree is Libra's justice theme "
                'at its plainest and least comfortable: the sign that loves harmony '
                'also has to hold the moment when harmony gets enforced rather than '
                'simply agreed to. There is no detail here about guilt or innocence, '
                'only the fact of the arrest itself, structure asserting that some '
                'lines, once crossed, get answered.',
     'colors': 'A planet at this degree often shows a strong relationship to '
               'consequence and accountability, sometimes as the one who enforces '
               'it, sometimes as someone who has personally felt structure close '
               'in. Saturn or Pluto here can favor a real, sober respect for the '
               'limits a system actually enforces. On the tenth house, it can '
               'describe a career built around exactly this kind of accountability, '
               'law, compliance, oversight.',
     'reflection': 'Where has structure recently closed in on you, or on someone '
                   "you're watching closely, and was it fair?"},
    {'degree': 19,
     'image': 'A group of robbers hides out, waiting for the attention on their '
              'crime to pass.',
     'meaning': "People who have taken something they weren't owed are lying low, "
                'waiting for attention to move elsewhere before they surface again. '
                'This degree is uncomfortable on purpose: not every actor in a Libra '
                "chart is virtuous, and this one names the shadow side of the sign's "
                'diplomacy directly, the version of cleverness that avoids reckoning '
                'rather than seeking it. Hiding is itself a strategy, and the degree '
                'asks what it actually costs to live inside one.',
     'colors': 'A planet at this degree can indicate real skill at staying under the '
               'radar, sometimes protectively, sometimes evasively, avoiding a '
               'reckoning that may eventually be unavoidable. Pluto or Mercury here '
               'can favor genuine cunning, for better or worse depending on what it '
               'is used to conceal. It rewards honest self-audit: is this hiding '
               'protection, or is it overdue avoidance?',
     'reflection': 'What are you currently keeping hidden that is actually just '
                   'waiting for the attention to pass, rather than truly resolved?'},
    {'degree': 20,
     'image': 'A rabbi carries out the ordinary duties of his office for his '
              'community.',
     'meaning': 'A person entrusted with religious and communal responsibility '
                'simply does the work of the office, day after day, without needing '
                'the moment to be dramatic to matter. This degree honors service '
                'inside a tradition, duty carried out faithfully because the role '
                'itself asks for consistency, not because anyone is watching for a '
                "performance. Libra, which weighs and mediates, finds here its own "
                "instinct professionalized: someone whose whole job is holding a "
                "community's moral and ceremonial balance.",
     'colors': 'A planet at this degree often shows real devotion to duty within a '
               'tradition or structure larger than the self, service performed '
               'reliably rather than for applause. Saturn or Jupiter here can favor '
               'someone who holds a genuine position of trust, spiritual, ethical, '
               'or communal, and takes its ordinary obligations seriously. On the '
               'ninth house, it can describe faith practiced as steady daily '
               'responsibility rather than occasional feeling.',
     'reflection': 'What duty are you quietly, faithfully performing right now, '
                   'whether or not anyone is there to see it?'},
    {'degree': 21,
     'image': 'A large, easy crowd spends a Sunday afternoon enjoying the beach '
              'together.',
     'meaning': 'A great many people, off duty at the same time, choose the same '
                'open stretch of sand and water simply to be pleased in. This degree '
                'is collective ease, not solitude, not a private retreat, joy taken '
                'publicly, side by side with strangers who are all, for one '
                'afternoon, wanting exactly the same uncomplicated thing. '
                "Libra's social instinct shows here at its most relaxed: pleasure "
                'does not need to be exclusive to be real.',
     'colors': 'A planet at this degree often shows genuine comfort taking pleasure '
               'in public, communal settings, at ease being one happy person among '
               'many rather than needing to be singled out. Venus or Jupiter here '
               'can favor real enjoyment of shared leisure, crowds that feel restful '
               'rather than draining. On the eleventh house, it can describe '
               'friendships or community built around simple, repeated shared '
               'enjoyment.',
     'reflection': 'When did you last let yourself be just one happy person in a '
                   'big, easy crowd, instead of needing the day to be about you '
                   'specifically?'},
    {'degree': 22,
     'image': 'A child holds a small bird up to a fountain so it can drink.',
     'meaning': 'A small act of unprompted generosity, offered to a creature with no '
                'way to ask for it directly and no way to repay it. This degree is '
                'kindness in its most uncomplicated form, care given simply because '
                "the need was visible and the water was right there. Libra's "
                'fairness starts, at root, exactly here: noticing what is thirsty, '
                "even when it's small, even when it's not yours to have to notice.",
     'colors': 'A planet at this degree often shows spontaneous, unforced '
               'generosity, especially toward the small and vulnerable, kindness '
               'that does not wait to be asked. The Moon or Venus here can favor a '
               'natural, gentle instinct to tend to whoever, or whatever, needs it '
               'in the moment. On the fifth house, it can describe creativity or '
               'care expressed through small, sincere gestures rather than grand '
               'ones.',
     'reflection': 'What small, thirsty thing near you have you already noticed, '
                   'and have you actually given it the water yet?'},
    {'degree': 23,
     'image': "A rooster's crow rings out, announcing the sunrise before anyone else "
              'is awake to see it.',
     'meaning': "A rooster's crow doesn't cause the sun to rise, but it announces "
                'the rising loudly enough that everyone within earshot knows the day '
                'has arrived. This degree is about voice used to mark a threshold, '
                'not to create it, timing and confidence combined into a single, '
                "unmistakable call. Libra's diplomacy usually softens announcements; "
                'this degree instead lets one be loud, because some mornings '
                'actually deserve the noise.',
     'colors': 'A planet at this degree often shows a real gift for marking '
               'beginnings clearly and confidently, being the one who announces '
               'that something new has actually started. Mars or the Sun here can '
               'favor a natural herald, someone whose voice or presence signals '
               'change is underway before anyone else has noticed it. On the first '
               'house, it can describe someone the world experiences as an '
               'unmistakable announcement in themselves.',
     'reflection': 'What sunrise are you currently the one meant to announce, '
                   'loudly enough for the whole yard to hear it?'},
    {'degree': 24,
     'image': 'A butterfly is seen with an unexpected third wing growing from its '
              'left side.',
     'meaning': 'Something already complete grows an extra piece it never '
                'technically needed, and somehow becomes more itself for having it. '
                "This degree revisits the sign's opening image and complicates it: "
                "perfection, it turns out, doesn't have to stay symmetrical to still "
                "be perfect, sometimes it gets stranger and better at once. Libra's "
                'usual devotion to balance meets its own exception here, proof the '
                'sign can hold asymmetry without losing its poise.',
     'colors': 'A planet at this degree often shows an unusual gift or trait that '
               'does not fit the expected symmetry of a life, and turns out to be an '
               'asset rather than a flaw. Uranus or Venus here can favor beauty or '
               'talent that is genuinely singular, not derivative of a standard '
               'template. On the fifth house, it can describe creative work that '
               'succeeds precisely because it refused to match what everyone '
               'expected.',
     'reflection': 'What extra, unmatched piece of you turned out to be a strength '
                   'instead of the flaw you assumed it was?'},
    {'degree': 25,
     'image': 'The sight of a single falling autumn leaf suddenly answers a question '
              'a wandering pilgrim has been carrying.',
     'meaning': 'A single falling leaf, small and ordinary, delivers a whole '
                'understanding to someone who happened to be paying attention at the '
                "right moment. This degree trusts that big truths don't always need "
                'big deliveries, sometimes a season simply hands you the answer in '
                'its smallest available form, and the only skill required is '
                'noticing it. Libra, so often weighing large questions formally, '
                'gets here the reminder that some answers arrive as almost nothing '
                'at all.',
     'colors': 'A planet at this degree often shows real receptivity to small, '
               'natural signs carrying outsized meaning, insight that arrives '
               'quietly rather than through direct instruction. Neptune or Mercury '
               'here can favor a mind that reads significance into ordinary detail, '
               'correctly, more often than skeptics expect. On the ninth house, it '
               'can describe wisdom gathered from observation of the natural world '
               'rather than from books alone.',
     'reflection': 'What small, ordinary thing recently told you something large, '
                   'if you actually let yourself receive it?'},
    {'degree': 26,
     'image': 'An eagle and a large white dove are seen transforming into one '
              'another, back and forth.',
     'meaning': 'Two birds that usually stand for opposite things, raw power and '
                'pure peace, trade places in front of you, each becoming the other '
                'without either one disappearing. This degree is transformation at '
                'its most Libran: not one side winning, but the two poles proving '
                'they were always more related than opposed, capable of literally '
                'becoming one another when the moment calls for it. Balance, here, '
                "isn't a static midpoint, it is this exact fluency between "
                'extremes.',
     'colors': 'A planet at this degree often shows real fluency moving between '
               'strength and gentleness, force and peace, depending on what a '
               'moment genuinely requires, rather than being stuck performing only '
               'one. Mars and Venus both feel at home here, trading places as '
               'needed. On the seventh house, it can describe a relationship where '
               'power and tenderness keep switching hands, healthily, rather than '
               'one person always holding one role.',
     'reflection': 'When did you last let yourself become the opposite of your '
                   'usual bird, on purpose, because the moment actually called for '
                   'it?'},
    {'degree': 27,
     'image': 'A small plane sails at altitude through a completely clear, open '
              'sky.',
     'meaning': "Distance covered from well above the ground, in conditions clear "
                'enough that nothing obstructs the view in any direction. This '
                'degree is perspective earned through altitude, not detachment, the '
                'plane is not avoiding the world below, it is simply seeing all of '
                "it at once instead of one obstacle at a time. Libra's gift for "
                'seeing both sides gets literalized here: height that lets '
                'everything be weighed in the same glance.',
     'colors': 'A planet at this degree often shows real capacity for broad, '
               'unobstructed perspective, seeing a whole situation clearly rather '
               'than getting caught in its details. Jupiter or Uranus here can '
               'favor genuine big-picture thinking, especially useful for mediating '
               'between positions that look opposed only from ground level. On the '
               'ninth house, it can describe travel, or a way of thinking, defined '
               'by exactly this kind of clear, elevated view.',
     'reflection': 'What looks obstructed from where you are standing right now, '
                   'that would resolve completely if you simply gained some '
                   'altitude?'},
    {'degree': 28,
     'image': 'A man realizes, only after the fact, that unseen, favorable forces '
              'have been quietly assisting him.',
     'meaning': "Something good is already at work on a man's behalf, and the "
                'degree catches the exact moment he becomes conscious of it rather '
                'than the moment it started. This is grace noticed, not grace '
                "summoned, the world's underlying friendliness becoming visible to "
                "someone who happened to be paying attention. Libra's faith in "
                'balance gets confirmed here: help, it turns out, was already '
                'arriving before it was recognized.',
     'colors': 'A planet at this degree often shows real capacity to notice support '
               'and good fortune arriving from unexpected directions, gratitude '
               "that's actually accurate rather than performed. Jupiter or Neptune "
               'here can favor someone unusually alert to help that is already '
               'present but easy to miss. On the eighth or twelfth house, it can '
               'describe unseen assistance, financial, spiritual, relational, '
               'becoming suddenly, gratefully visible.',
     'reflection': 'What brightening influence is already surrounding you right '
                   'now, that you are only just starting to actually notice?'},
    {'degree': 29,
     'image': "Across generations, humanity keeps building toward the same "
              'unfinished bridge of shared knowledge.',
     'meaning': "Not one person's project, an entire species' ongoing attempt to "
                'hand what it has learned to whoever comes next, so nobody has to '
                'start completely over. This degree is patient in a way almost '
                'nothing else in the zodiac is, measured across generations rather '
                'than a single lifetime, a bridge built collectively that nobody '
                "alive will ever see the far end of. Libra's fairness scales all the "
                'way up here, into a commitment that spans far past any one '
                'relationship.',
     'colors': 'A planet at this degree often shows real investment in work that '
               'outlasts a single lifetime, teaching, writing, building institutions '
               'meant to carry forward. Saturn or Jupiter here can favor a genuine '
               'sense of responsibility to whoever inherits the field next, not '
               'just to current peers. On the ninth or tenth house, it can describe '
               'a legacy consciously built to be added to, not just admired.',
     'reflection': 'What are you currently adding to the bridge, that someone you '
                   "will never meet is eventually going to walk across?"},
    {'degree': 30,
     'image': 'Three separate mounds of accumulated knowledge sit piled on top of a '
              "philosopher's head.",
     'meaning': 'The final degree of Libra closes with accumulation made almost '
                'visible, wisdom piled literally on top of the thinker who gathered '
                'it, three distinct heaps rather than one tidy sum. After thirty '
                'degrees of weighing, judging, and balancing, the sign ends holding '
                'real, substantial knowledge, and lets it show plainly instead of '
                'modestly hiding the total. There is something almost playful in '
                'the image, proof that even the most serious accumulation can end '
                'up a little top-heavy, a little absurd, and still entirely '
                'earned.',
     'colors': 'A planet at this degree often shows real, visible depth of '
               'knowledge, built up over enough time that it has become genuinely '
               'part of how a person is recognized. Jupiter or Saturn here can '
               'favor a scholar or advisor whose accumulated understanding is '
               'obvious on sight, not hidden. On the ninth house, it can describe a '
               'mind that has simply kept gathering, mound after mound, and stopped '
               'apologizing for how much it is carrying.',
     'reflection': 'What have you accumulated enough of, finally, that you are '
                   'allowed to let it show instead of carrying it modestly?'},
]

assert len(ENTRIES) == 30, f"expected 30 Libra degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Libra degrees out of order"
