"""Sabian symbol data for Gemini.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (kerykeion.net, jamesburgess.com /
Sacred 7 Academy, astronarrative.com, sabian-calculator.com, Dane
Rudhyar's "An Astrological Mandala" as hosted at mindfire.ca, and
degree-specific confirmation via Blain Bovee's Sabian Symbol blog,
Saijin's Sabian Symbol Septenary, and Tarot Forum's Sabian Symbols study
group for the two degrees with the widest wording variance, Gemini 11 and
Gemini 22) before being hand-typed. Do NOT extend this list, or write a
new sign's list, without the same verification discipline: fewer
verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a glass-
bottomed boat reveals what lies underwater"), not a verbatim quote of
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
SIGN = {"name": "Gemini", "slug": "gemini", "glyph": "♊︎", "order": 3}

# The 30 degrees of Gemini, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str). See SCHEMA.md for what each field means.
ENTRIES = [
    {'degree': 1,
     'image': 'A boat with a glass bottom lets its passengers watch the underwater '
              'world glide by beneath them.',
     'meaning': "This is Gemini's opening move, announced in a single image: stay on "
                'the surface, and still see clearly all the way down. The boat is the '
                'trick, a vessel built specifically so curiosity never has to get wet '
                'to be satisfied. Nothing about this degree asks you to dive in; it '
                'asks you to build something that lets you look without needing to '
                'submerge. Two levels of reality, held in view at the very same time, '
                'is the whole sign in miniature, right at its first degree.',
     'colors': 'A planet here often grants a gift for seeing beneath the surface of a '
               'situation without disturbing it, a natural researcher or observer. '
               'Mercury at this degree favors a mind built to translate between what '
               'is visible and what is quietly happening underneath it. On an angle, '
               'it can describe someone the world experiences as already seeing what '
               'is really going on.',
     'reflection': "What is gliding along beneath you right now that you've only ever "
                   'watched, never actually touched?'},
    {'degree': 2,
     'image': 'A cloaked figure moves from house to house at night, filling stockings '
              'while everyone sleeps.',
     'meaning': 'Generosity performed with no audience and no credit claimed, the '
                'giver deliberately writing themselves out of the good they just did. '
                "Gemini, usually so eager to talk, discovers here that some of its "
                'best exchanges happen in total silence, entirely unwitnessed by the '
                'one receiving them. Something still moves from one hand to another; '
                'the only thing withheld is the name of who sent it.',
     'colors': 'A planet here often shows real generosity that prefers anonymity, '
               'giving that leaves no trace of its source. Venus at this degree can '
               'favor gift-giving as a genuine love language, done privately rather '
               'than publicly. On the Midheaven, it suggests a reputation built on '
               'uncredited, behind-the-scenes work others quietly depend on.',
     'reflection': "What have you given recently that no one could actually trace "
                   'back to you?'},
    {'degree': 3,
     'image': 'An old engraving shows elegant strollers moving through a formal '
              'palace garden, dressed in the fashion of a vanished era.',
     'meaning': 'A whole disappeared social world, preserved intact in a single '
                'still image: manners, hierarchy, and leisure all legible at a glance '
                "to anyone who knows how to read them. Gemini's mind treats history "
                'itself as a kind of gossip, the past not gone but simply a '
                "conversation that hasn't reached you yet, encoded here in an "
                'artifact rather than a voice. This degree loves the one specific '
                'detail that lets you reconstruct an entire vanished era.',
     'colors': 'A planet here often shows real fluency in reading context from small '
               'clues, period, class, mood, and a taste for elegance recorded rather '
               'than lived firsthand. Venus or Mercury here can favor an aesthetic '
               'sensibility and appreciation for craftsmanship and history. On the '
               'IC, it can describe a family history or inherited refinement that '
               'still shapes taste today.',
     'reflection': 'What old picture of a vanished world do you keep returning to, '
                   'and what does it actually tell you about your life now?'},
    {'degree': 4,
     'image': 'Sprigs of holly and mistletoe, hung again this year, bring back every '
              'Christmas that came before this one.',
     'meaning': 'A repeated, seasonal object doing the quiet work of time travel: '
                'each hanging is this year and, at the same time, every other year '
                "folded invisibly into it. Gemini, usually chasing the newest fact, "
                'pauses here to notice that repetition itself carries real meaning, '
                'that the tenth time you do a thing is not the same as the first, it '
                'is thick with every time in between. Ritual working quietly as '
                'memory.',
     'colors': 'A planet here often shows sentiment triggered by small, recurring '
               'objects or traditions, the associative mind at its most tender. The '
               'Moon at this degree favors nostalgia used well, as genuine '
               'continuity rather than avoidance. On the fourth house, it can '
               'describe a home defined more by its repeated rituals than by any '
               'single event.',
     'reflection': 'What small recurring thing, hung up again this year, would bring '
                   'back every year it has ever marked?'},
    {'degree': 5,
     'image': 'A newly printed pamphlet argues its case and calls its readers to act '
              'right now.',
     'meaning': "Ideas here refuse to stay theoretical; the whole point of writing "
                "this down was to actually move somebody. Gemini's usual mode is "
                "gathering and comparing information neutrally, but this degree "
                'insists that some information is written specifically to end '
                'neutrality, to turn a reader into a participant. There is real '
                'urgency in the image, not a library shelf but a call to arms '
                'printed fast and passed hand to hand.',
     'colors': 'A planet here often carries persuasive, activating language, words '
               'meant to be acted on rather than simply absorbed. Mercury or Mars at '
               'this degree favors a sharp, motivating communicator, a natural '
               'organizer or pamphleteer. On the Midheaven, it can describe a public '
               'voice built around a cause rather than neutral reporting.',
     'reflection': "What have you read recently that you've let stay an opinion, "
                   'when it was actually asking you to act?'},
    {'degree': 6,
     'image': 'A crew works a rig, boring steadily down through rock toward a '
              'reserve of oil they are certain is there.',
     'meaning': "Committed, effortful extraction of something valuable that isn't "
                'visible from where you stand, real labor backed by faith in an '
                "unseen deposit. Gemini's information-gathering usually happens on "
                'the surface, scanning widely; this degree instead goes narrow and '
                'deep, betting everything on one specific spot being right. The '
                'reward, if it comes, is wildly disproportionate to the modest '
                'patch of ground the rig actually occupies.',
     'colors': 'A planet here often shows willingness to commit serious, sustained '
               'effort to a single source rather than spreading attention thin. '
               'Pluto or Mars at this degree favors a genuine capacity for deep, '
               'patient extraction of resources or insight others gave up looking '
               'for. On the second house, it can describe wealth built by working '
               'one vein rather than diversifying early.',
     'reflection': "Where have you been drilling in one spot long enough to "
                   'actually hit what you were after?'},
    {'degree': 7,
     'image': 'A rope and bucket wait at an old well, resting in the cool shade of '
              'tall, long-established trees.',
     'meaning': "A simple, working technology, old enough that the trees around it "
                'have had time to grow tall, still doing its one job long after '
                "whoever built it is gone. Gemini, restless and quick, meets a "
                'different kind of intelligence here: patience proven across '
                'generations, a source that never needed reinventing because it '
                'never stopped working. Shade and water together suggest relief '
                "that has been available all along, if you'd just walk to it.",
     'colors': 'A planet here often favors trusted, time-tested sources of '
               'knowledge or comfort over whatever is newest. Saturn at this degree '
               'shows real respect for enduring methods, and for elders who already '
               'solved the problem once. On the fourth house, it can describe a '
               'family or home life built around something old that still '
               'genuinely nourishes.',
     'reflection': 'What old, unglamorous source have you been walking past, that '
                   'is still fully capable of giving you what you need?'},
    {'degree': 8,
     'image': 'Workers gather outside the factory gates, worked up and refusing to '
              'go back in until conditions change.',
     'meaning': "Collective voice reaching the point where private grievance "
                "becomes a public demand, Gemini's gift for talk turned from "
                'individual chatter into a single, unified shout. This degree marks '
                'the moment talk becomes leverage, enough people saying the same '
                'thing, in the same place, at the same time, that whoever is in '
                'charge has to actually respond. There is real risk in it too, since '
                "a crowd this worked up doesn't fully control its own outcome.",
     'colors': 'A planet here often shows a talent for organizing collective voice, '
               'or a personal history of speaking up loudly once quieter channels '
               'failed. Mars or Uranus at this degree favors real courage in '
               'confrontation, especially around fairness and working conditions. '
               'On the sixth house, it can describe strong opinions about how work '
               'itself should be structured and treated.',
     'reflection': "What have you been saying quietly that's actually ready to be "
                   'said as a group, out loud, at the gate?'},
    {'degree': 9,
     'image': 'A quiver, packed full and ready, holds every arrow that has not yet '
              'been shot.',
     'meaning': 'Pure stored potential, organized and pointed in one direction, '
                "waiting only for the moment of release. Gemini scatters its "
                'attention across many targets; this degree is the counter-note, '
                'all that scattered curiosity finally gathered into a single case, '
                'ready to be used with precision instead of spent at random. A full '
                'quiver is not about owning more arrows than anyone else, it is '
                'about having them all in reach when a real moment actually calls '
                'for one.',
     'colors': 'A planet here often shows real readiness, skills, resources, or '
               'ideas kept prepared rather than scrambled for at the last second. '
               'Sagittarius energy or Mars at this degree favors aim and follow-'
               'through once the quiver has actually been drawn from. On the first '
               'house, it can describe someone who always seems oddly prepared, as '
               'if they saw the moment coming.',
     'reflection': "What have you been quietly preparing, that you still haven't "
                   'actually let fly?'},
    {'degree': 10,
     'image': 'A small plane tips forward and drops fast, nose first, toward the '
              'ground.',
     'meaning': 'Total commitment to a single, high-stakes trajectory, no hedging, '
                "no pulling back mid-drop to reconsider. Gemini usually keeps "
                'multiple options open at once; this degree is the sign\'s opposite '
                'instinct, the moment keeping options open stops being possible and '
                'everything depends on how well this one committed move gets '
                'executed. It is frightening and exhilarating for the same reason: '
                "there's no version of it that's halfway.",
     'colors': 'A planet here often shows a taste for high-risk, high-commitment '
               'moves once a decision is actually made, all in, no partial '
               'measures. Mars or Uranus at this degree favors real nerve under '
               'pressure, a genuine stomach for risk. On an angle, it can describe '
               "someone who reads to others as fearless, even when they don't "
               'feel that way privately.',
     'reflection': 'Where have you already committed to the dive, and are you '
                   'actually flying it, or just falling?'},
    {'degree': 11,
     'image': 'Land that was closed off yesterday stands open today, and the first '
              'ones through are already imagining what to build there.',
     'meaning': 'New ground appearing exactly where there was none, and the '
                'fastest, most curious minds getting there first. This is Gemini at '
                'its most optimistic, not gathering information about the world as '
                'it already is, but rushing toward the part of the map still blank, '
                'purely for the pleasure of being the one who fills it in. Realism '
                'and possibility are not opposites here, they are the same motion: '
                'seeing clearly enough to know the ground is solid, then moving.',
     'colors': 'A planet here often shows a pioneering, first-mover instinct, '
               'especially toward fields, ideas, or markets that have only just '
               'opened up. Uranus or Jupiter at this degree favors a genuine talent '
               'for spotting the frontier before it gets crowded. On the ninth '
               'house, it can describe a real appetite for entirely new territory, '
               'literal or intellectual.',
     'reflection': "What newly opened ground have you noticed, that you haven't "
                   'let yourself walk onto yet?'},
    {'degree': 12,
     'image': 'A young woman held as property speaks up sharply to the one who '
              'claims to own her, and will not be quieted.',
     'meaning': "Voice asserting itself from the one position it's least supposed "
                'to come from, full personhood insisting on itself against a '
                'structure built to deny it. This degree carries real weight: it is '
                'not playful assertiveness, it is dignity refusing to be erased '
                "even when every external condition says it should be. Gemini's "
                'gift for words becomes, here, the one tool still available when '
                'every other form of power has been stripped away.',
     'colors': 'A planet here often shows sharp, unfiltered honesty from someone in '
               'a position that is supposed to keep quiet, a whistleblower\'s '
               'instinct, a refusal to perform smallness. Mercury or Mars at this '
               'degree favors real verbal courage, sometimes costly, always '
               'genuine. On the sixth or twelfth house, it can describe standing up '
               "inside a structure that wasn't built to hear you, and being heard "
               'anyway.',
     'reflection': 'Where are you still expected to stay quiet, and what would it '
                   'actually cost you to speak?',
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 13,
     'image': 'A gifted musician sits at the keyboard, playing with the whole of '
              'their attention.',
     'meaning': 'Total absorption in a single instrument, a single act of '
                'expression, everything else in the room forgotten. Gemini\'s mind '
                'usually holds several threads at once; this degree is total '
                'convergence instead, every faculty the sign has, dexterity, '
                'quickness, feeling, technical memory, focused down into one '
                'continuous stream of sound. Mastery, here, looks like the opposite '
                'of duality: two hands doing entirely different things, both in '
                'total service of a single piece.',
     'colors': 'A planet here often shows real technical gift alongside emotional '
               'depth, the rare combination that makes craft look effortless. '
               'Mercury, Venus, or Neptune at this degree favors musical or '
               'performative talent, precision fused with feeling. On the fifth '
               'house, it can describe creative expression that absorbs the whole '
               'self, not a side hobby.',
     'reflection': 'What is the one instrument you play with your whole attention, '
                   'and when did you last actually sit down at it?'},
    {'degree': 14,
     'image': 'Two people, at a real distance from each other, understand each '
              'other without needing to say a word.',
     'meaning': 'Communication stripped down to its purest form, meaning '
                'transferred with no delay, no translation, no chance of being '
                'misheard. This is the degree Gemini has secretly been reaching '
                'for all along: not more words, but the moment words become '
                'unnecessary because the connection itself is already carrying the '
                "message. It suggests real closeness can shortcut the sign's usual "
                'chattiness entirely.',
     'colors': 'A planet here often shows an uncanny ability to read someone '
               'accurately without much said out loud, genuine intuitive rapport. '
               'Mercury, Neptune, or the Moon at this degree favors a gift for '
               'sensing what a person means before they finish the sentence, '
               'sometimes before they start it. On the seventh house, it can '
               'describe a partnership defined by exactly this kind of wordless '
               'understanding.',
     'reflection': 'Who do you already understand without needing them to explain, '
                   'and are you trusting that as much as you should?'},
    {'degree': 15,
     'image': 'Two children compare notes in their own language, teaching each '
              'other whatever each one already knows.',
     'meaning': "The midpoint of Gemini, and its purest expression: two people, "
                'roughly equal, simply trading what they have got. Neither child is '
                'the teacher; the exchange itself is the point, each one a little '
                'richer for what the other already happened to know. This is '
                'learning at its most natural, unforced by any curriculum, driven '
                'only by two curious minds enjoying having found each other.',
     'colors': 'A planet here often shows real ease in peer-to-peer learning, '
               'trading knowledge horizontally rather than only taking instruction '
               'from above. Mercury or a strong Gemini placement favors natural '
               'collaborators, quick to teach and quick to learn in the same '
               'conversation. On the third house, it can describe siblings, '
               'neighbors, or a local circle that has been a genuine source of '
               'mutual education.',
     'reflection': 'Who is currently trading knowledge with you as an equal, and '
                   'what have you actually learned from them lately?'},
    {'degree': 16,
     'image': 'A woman stands before a crowd, making her case with real feeling, '
              'determined that her cause be heard.',
     'meaning': "Conviction that has stopped waiting for permission and started "
                "demanding an audience. Gemini's usual mode is exchange, back and "
                'forth; this degree is one voice, deliberately amplified, aimed at '
                'changing minds in a single sustained push. There is real '
                'vulnerability in standing up like this, and real power in '
                'refusing to soften the message just to make the room more '
                'comfortable.',
     'colors': 'A planet here often shows a genuine gift for persuasive public '
               "speech, especially in service of a cause bigger than the "
               'speaker\'s own interest. Mars, Mercury, or Jupiter at this degree '
               'favors real oratory skill, conviction that reads as authentic '
               'rather than performed. On the Midheaven, it can describe a public '
               'identity built around advocacy.',
     'reflection': "What cause have you privately been convinced of, that you "
                   'still have not said out loud in a room that could act on it?'},
    {'degree': 17,
     'image': "A strong young face slowly settles into the more thoughtful, "
              'weathered face of someone who has learned to think things through.',
     'meaning': "Vitality maturing into wisdom without losing what made it vital "
                "in the first place, the transformation is an upgrade, not a loss. "
                "Gemini's whole arc, compressed into one image: quick, physical, "
                'reactive intelligence gradually becoming slower, deeper, '
                'considered intelligence. Both faces belong to the same person; '
                'the degree simply names the years it takes to grow from one into '
                'the other.',
     'colors': 'A planet here often shows real intellectual development over time, '
               'someone who becomes noticeably more thoughtful with age rather '
               'than just older. Mercury or Saturn at this degree favors a mind '
               'that keeps upgrading itself, quickness eventually earning real '
               'depth. On an angle, it can describe a person others watch visibly '
               'mature into their thinking self.',
     'reflection': 'Which of your two faces, the quick one or the thoughtful one, '
                   'is actually running things today?'},
    {'degree': 18,
     'image': 'Two men speak their own language together, at home in it, in a '
              'city built around a completely different one.',
     'meaning': "A private fluency preserved intact inside a foreign context, the "
                'whole conversation a small act of belonging to somewhere else '
                "while standing exactly here. Gemini's gift for language usually "
                'means fitting into whatever room it is in; this degree instead '
                "protects a language that doesn't need the room's approval at all. "
                'It is community carried inside two people, portable, '
                'untranslated, entirely theirs.',
     'colors': 'A planet here often shows real comfort maintaining an identity, '
               'dialect, or inside understanding that the surrounding culture '
               "doesn't share or need to access. Mercury at this degree favors "
               'multilingual ease, or simply a private register only certain '
               'people are let into. On the third or eleventh house, it can '
               'describe a specific community whose language, literal or coded, '
               'is a real anchor.',
     'reflection': 'What language, literal or otherwise, do you still speak '
                   "fluently with someone, that the room around you doesn't "
                   'understand?',
     'note': 'Note: the 1925 original for this degree named a specific nationality in '
             'a now-outdated way; the picture above keeps its meaning in respectful, '
             'modern terms.'},
    {'degree': 19,
     'image': 'A huge, ancient book lies open, holding wisdom far older than '
              'anyone currently reading it.',
     'meaning': 'Knowledge that has survived long enough to outlast its original '
                'audience many times over, and is still legible to whoever bothers '
                'to open it. Gemini worships the newest fact; this degree insists '
                'the oldest ones are often still true, sometimes truer, simply '
                'waiting in a form modern hands rarely reach for. Size and age '
                "both signal weight here: this isn't a quick reference, it is a "
                'whole tradition bound into one object.',
     'colors': 'A planet here often shows real respect for tradition, source '
               'material, and long-form knowledge over quick summary. Jupiter, '
               'Saturn, or Mercury at this degree favors scholarly depth, a '
               "genuine researcher's patience with primary sources. On the ninth "
               'house, it can describe education built on foundational texts '
               'rather than trend.',
     'reflection': 'What old, substantial source of wisdom have you been meaning '
                   'to actually open, instead of settling for the summary?'},
    {'degree': 20,
     'image': 'Long tables offer dish after dish, gathered in from many different '
              'places, more choice than anyone could eat.',
     'meaning': 'Abundance organized for easy access, everything laid out at once '
                'so comparison and choice become the whole point of the '
                'experience. Gemini thrives exactly here, not committed to one '
                'dish, but delighted by the sheer range on offer, sampling widely '
                'rather than settling early. The degree is not about excess for '
                "its own sake, it's about a system generous enough to let "
                'curiosity actually range freely.',
     'colors': 'A planet here often shows real appetite for variety, options, '
               'information, and experiences kept plentiful rather than narrowed '
               "too soon. Jupiter or Mercury at this degree favors a collector's "
               'joy in breadth, sampling many things well rather than one thing '
               'exclusively. On the sixth house, it can describe a daily life or '
               'diet built around real variety.',
     'reflection': 'With everything currently laid out in front of you, what have '
                   'you actually tasted, versus just looked at?'},
    {'degree': 21,
     'image': 'A crowd of workers marches together, loud and unified, demanding '
              'to be heard.',
     'meaning': "Individual voices merging into one collective sound loud enough "
                "that it can no longer be ignored one by one. This is degree "
                "eight's strike escalated, and Gemini's usual scattered chatter "
                'concentrated into a single unmistakable message: many mouths, one '
                'sentence. There is real force in this kind of unity, and real '
                'risk too, since a crowd this large and this loud is genuinely '
                'hard to steer once it starts moving.',
     'colors': 'A planet here often shows a strong instinct for collective action, '
               "or a life shaped by being part of something louder than any one "
               'person could be alone. Mars, Uranus, or Jupiter at this degree '
               'favors real conviction that shows up best in numbers, not in '
               'isolation. On the eleventh house, it can describe an identity '
               'bound up with groups organized around a shared demand.',
     'reflection': 'What have you been saying alone, that might actually be truer '
                   'and stronger said together?'},
    {'degree': 22,
     'image': 'Couples fill an old barn, turning the space that stored the '
              'harvest into a floor for dancing.',
     'meaning': "Labor's reward arriving as pure, communal joy, the same building "
                "that held the season's hard-won grain now holds nothing but "
                "music and moving feet. Gemini's love of company finds its "
                'fullest expression here, not a private pairing off, but '
                'everyone, all the partners changing, all the steps shared. The '
                'dance only works because everyone already knows the same steps; '
                'individuality shows up in style, not in going it alone.',
     'colors': 'A planet here often shows real joy in communal celebration, '
               'comfortable moving in and out of many partnerships within a '
               'shared, familiar structure. Venus or Jupiter at this degree '
               'favors social ease, a gift for making a group feel like one '
               'moving thing. On the seventh or eleventh house, it can describe '
               'relationships that thrive inside a wider community rather than '
               'off to the side of it.',
     'reflection': 'What have you recently worked hard enough to earn a real, '
                   'unguarded celebration for, and have you actually taken the '
                   'floor yet?'},
    {'degree': 23,
     'image': 'Three young birds sit crowded together in a nest built high up in '
              'a tree.',
     'meaning': 'Vulnerability held at a height, several small lives depending on '
                "the same fragile structure and each other's warmth until they "
                "are ready to leave it. Gemini's duality becomes multiplicity "
                'here, three instead of two, and the degree asks what changes '
                'when connection has to stretch to hold more than a pair. The '
                "nest is precarious by design; that's not a flaw, it is exactly "
                'what teaches wings to work.',
     'colors': 'A planet here often shows close early bonds with siblings or '
               'peers, formed under conditions that felt higher-stakes than they '
               "looked from outside. The Moon or Mercury at this degree favors "
               'real tenderness toward a small, tightly knit group still finding '
               'its footing. On the fourth or fifth house, it can describe family '
               'or creative work still in its fledgling, not-yet-flown stage.',
     'reflection': 'Who else is still in the nest with you, and what is actually '
                   'keeping all of you up there together?'},
    {'degree': 24,
     'image': 'Children glide across the ice covering a small village pond, '
              'laughing as they go.',
     'meaning': 'Ordinary play made briefly magical by a season that transforms '
                'the everyday landscape into something new to move across. Gemini '
                'finds real delight in exactly this: familiar ground, temporarily '
                'changed, inviting a completely different way of crossing it. The '
                'ice will not last, which is part of the joy, not a flaw in it; '
                'this is pleasure taken fully in a window everyone knows is '
                'limited.',
     'colors': 'A planet here often shows a gift for finding real delight in '
               'temporary, seasonal conditions rather than waiting for permanent '
               'ones. The Moon or Venus at this degree favors playfulness that '
               'thrives on novelty, especially the kind the calendar itself '
               'creates. On the fifth house, it can describe joy taken seriously, '
               "treated as worth showing up for even when it won't last.",
     'reflection': 'What temporary, seasonal window are you currently skating '
                   'across, and are you actually enjoying it, or waiting for it '
                   'to become permanent?'},
    {'degree': 25,
     'image': 'A gardener works carefully through a row of tall palms, trimming '
              'each one back into shape.',
     'meaning': "Ongoing, unglamorous maintenance applied to something that has "
                'already grown large and needs regular attention to stay healthy '
                "rather than overgrown. Gemini's mind loves novelty, but this "
                'degree is entirely about upkeep: going back to the same tall, '
                'established thing again and again, never finished, just tended. '
                'The palms do not need to be replaced, only cared for '
                'consistently.',
     'colors': 'A planet here often shows real discipline around maintaining what '
               'has already been built, rather than constantly starting over. '
               'Saturn or Venus at this degree favors patient, ongoing care for '
               'something of real size and standing, whether a career, a body of '
               'work, or a relationship. On the sixth house, it can describe a '
               'life organized around consistent upkeep rather than dramatic '
               'overhauls.',
     'reflection': 'What tall, already-grown part of your life needs a regular '
                   'trim right now, instead of another fresh start?'},
    {'degree': 26,
     'image': 'Frost coats every branch in the woods overnight, and the whole '
              'forest briefly looks made of glass.',
     'meaning': 'A hard, cold condition that happens to also be beautiful, '
                'arriving overnight without asking permission and transforming '
                "everything it touches. Gemini usually keeps moving to stay warm "
                "and engaged; this degree asks it to stop and actually look at a "
                "season that isn't comfortable, and notice it is stunning "
                'anyway. Frost is temporary too, like the ice of the twenty-'
                'fourth degree, but it carries a harder edge, less playful, more '
                'austere.',
     'colors': 'A planet here often shows an ability to find real beauty in '
               'difficult, cold conditions, grief, scarcity, isolation, without '
               'pretending they are anything other than hard. Saturn or Neptune '
               'at this degree favors an eye for the stark and the lovely '
               'occurring together. On the twelfth house, it can describe a '
               'capacity to sit with a hard season and still see what is fine '
               'about it.',
     'reflection': 'What in your life right now is genuinely cold, and have you '
                   'let yourself notice that it is also, somehow, beautiful?'},
    {'degree': 27,
     'image': 'A wanderer steps out from the trees and stands looking, wide-eyed, '
              'at the open country ahead.',
     'meaning': 'Emergence from enclosure into a view that suddenly contains '
                'everything, the forest did not disappear, it simply stopped '
                "being the whole world. Gemini, always gathering information from "
                'many directions, gets one clean, unobstructed vista here, not '
                'more data, just a wider frame to hold what it already knows. The '
                'wonder in the image is real; nothing about this degree is '
                'jaded.',
     'colors': 'A planet here often shows a genuine capacity for renewed wonder, '
               'especially after a period spent enclosed, isolated, or heads-'
               'down. Jupiter or Uranus at this degree favors real freshness of '
               "perspective, an outsider's eye that still finds the ordinary view "
               'remarkable. On the ninth house, it can describe travel or a '
               'change of setting that reopens real curiosity.',
     'reflection': 'What have you just stepped out of, and what does the view '
                   'actually look like now that you have cleared the trees?',
     'note': 'Note: the 1925 original for this degree used a term for the Romani '
             'people now considered a slur; the picture above keeps its meaning in '
             'respectful, modern terms.'},
    {'degree': 28,
     'image': 'A man walks out of the courthouse having lost everything '
              'financially, feeling both wrecked and oddly ready to begin again.',
     'meaning': 'Total financial collapse, formally acknowledged, and the strange '
                'relief that comes from a burden finally being named instead of '
                "carried privately. This degree doesn't pretend loss doesn't "
                'hurt; it insists that naming a loss completely, in front of '
                "witnesses, is itself the first real step back. Gemini's "
                'information-sharing instinct turns here toward the hardest kind '
                'of disclosure: telling the truth about what is gone, out loud, '
                'so rebuilding can start from solid ground instead of pretense.',
     'colors': 'A planet here often shows real resilience after a documented, '
               'total setback, someone who has learned that starting over '
               'cleanly beats limping along half-ruined. Saturn or Pluto at this '
               'degree favors genuine capacity to rebuild after loss, once the '
               'loss has actually been faced. On the second or eighth house, it '
               'can describe a relationship with money shaped by one honest '
               'reckoning.',
     'reflection': 'What have you been carrying half-acknowledged, that might '
                   'actually be lighter the day you say it plainly, out loud?'},
    {'degree': 29,
     'image': 'High in a still-bare tree, a mockingbird runs through its whole '
              'range of songs before the season has properly turned.',
     'meaning': 'Optimism arriving slightly ahead of the evidence, a full '
                "performance offered before the world has actually caught up to "
                "it. Gemini, always quick, gets its own quickness rewarded here: "
                "the mockingbird doesn't wait for spring to be officially "
                'confirmed, it simply starts singing everything it knows, '
                'trusting the season is close enough. There is real range in the '
                "image too, a mockingbird's gift is imitation and variety, many "
                'songs from one small throat.',
     'colors': 'A planet here often shows an ability to signal hope, or perform '
               'range, before conditions have fully caught up, an early riser, an '
               'early believer. Mercury or Jupiter at this degree favors genuine '
               'versatility, a gift for many registers, sometimes deployed a '
               'little ahead of schedule. On the fifth house, it can describe '
               'creative confidence expressed before external validation '
               'arrives.',
     'reflection': "What are you already singing, even though the season hasn't "
                   'technically turned yet, and does it matter that you are '
                   'early?'},
    {'degree': 30,
     'image': 'A line of women in swimwear parades past the judges and the crowd '
              'gathered at the shore.',
     'meaning': "The final degree of Gemini turns its whole restless curiosity "
                'outward into pure spectacle, display as public entertainment, '
                'judged in the open, no pretense that anyone involved is hiding '
                "anything. This is Gemini's talkative, performative nature at its "
                'most literal: bodies as the message, the crowd as the audience, '
                'approval measured in real time. It closes the sign the way it '
                'opened, with something on public display for anyone willing to '
                'look.',
     'colors': 'A planet here often shows real comfort being visibly evaluated, a '
               'taste for public display and the immediate feedback of a '
               'watching crowd. Venus or the Sun at this degree favors charisma '
               'built for an audience, ease under direct, appraising attention. '
               'On the fifth house or the Ascendant, it can describe someone who '
               'performs a version of themselves in public with genuine '
               'confidence.',
     'reflection': 'What part of yourself are you currently putting on parade, '
                   'and whose judgment are you actually trying to win?'},
]

assert len(ENTRIES) == 30, f"expected 30 Gemini degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Gemini degrees out of order"
