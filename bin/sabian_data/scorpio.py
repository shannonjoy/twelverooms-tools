"""Sabian symbol data for Scorpio.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (kerykeion.net, astronarrative.com,
jamesburgess.com / Sacred 7 Academy, sabian-calculator.com,
boveeastrology.com / Blain Bovee's Sabian Symbol archive,
sabiansymbologist.wordpress.com, judithdehaan.substack.com, and, for two
degrees checked further, astrologyweekly.com's forum quoting Jones'
original wording directly) before being hand-typed. astronarrative.com
labels degrees on the "N-1 to N" convention (e.g. its "3-4" is this file's
degree 4); confirmed degree 1 aligns correctly across all sources with no
offset issue. Scorpio 21 was double-checked because sources phrase it two
ways, "a soldier derelict in his duty" (Jones' original, negative framing)
versus "obeying his conscience, a soldier resists orders" (a later,
positive-framing elaboration); both describe the identical scene, a
soldier who refuses to carry out an order, confirmed by 8+ mutually
agreeing sources. Scorpio 30 was likewise double-checked because kerykeion
paraphrases it verbosely ("Children in Halloween Costumes Indulge in
Various Pranks") while five-plus other independent sources (jamesburgess,
astronarrative, sabian-calculator, boveeastrology, sabiansymbologist) give
the standard short title "The Halloween jester" for the same image; this
is the same degree and the same picture, not a conflicting symbol. Do NOT
extend this list, or write a new sign's list, without the same
verification discipline: fewer verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a sight-seeing
bus"), not a verbatim quote of Marc Edmund Jones' 1953 book or Dane
Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`, `colors`,
and `reflection` are original Twelve Rooms interpretation, written fresh
for this project; none of it is copied from Jones or Rudhyar.

DATED IMAGERY: Scorpio 26's 1925 original names "Indians making camp" and
Scorpio 29's names "an Indian squaw pleading to the chief for the lives of
her children" (the latter using a term now recognized as a slur). Per
Shannon's standing policy, the canonical mapping is kept on both, but
`image` restates each respectfully without the ethnic label or the slur,
and a `note` field is attached below each symbol card. See SCHEMA.md for
the full policy.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Scorpio", "slug": "scorpio", "glyph": "♏︎", "order": 8}

# The 30 degrees of Scorpio, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and (only on degrees 26 and 29) note (str). See
# SCHEMA.md for what each field means.
ENTRIES = [
    {'degree': 1,
     'image': 'A crowded sightseeing bus moves through city streets, everyone aboard '
              'looking out at the same passing view.',
     'meaning': "Scorpio's own reputation is all interiority, and yet its very first "
                'degree opens facing outward: a busload of strangers, riding together, '
                'watching the same city slide by through glass. Nothing here is private '
                'yet, nothing has been entered. This is Scorpio before it has gone '
                'anywhere alone, still taking in the surface of things the way any tourist '
                'does, one pass through a place that has not yet asked anything real of '
                'it. There is a quiet foreshadowing in the image too: a bus tour only ever '
                'shows the outside of a city, and this whole sign is about to spend '
                'twenty-nine more degrees getting off the bus and going in.',
     'colors': 'A planet at Scorpio 1 tends toward wide, unfocused awareness before any '
               'single fixation sets in, cataloguing a scene before choosing where to '
               'look closely. Mercury here often gives a broad, accurate first read of a '
               'room. The Moon can show sensitivity to shared atmosphere, feeling with a '
               'group before knowing anything individually and privately.',
     'reflection': 'What are you currently watching pass by at a comfortable distance, '
                   'that this sign is eventually going to ask you to get off the bus and '
                   'enter?'},
    {'degree': 2,
     'image': 'A bottle breaks, and the perfume inside spills out all at once, filling '
              'the surrounding air.',
     'meaning': "Something once carefully sealed releases suddenly and completely, and "
                "there is no putting the scent back once it has filled the room. This "
                'degree names the essential Scorpio anxiety and thrill in the same breath: '
                'what happens when a contained thing breaks open and floods everything '
                'around it without asking permission first. Perfume is meant to be worn '
                'sparingly, a controlled accent; here it saturates instead, total rather '
                'than measured. The image does not moralize about the waste, it simply '
                'shows, honestly, what pours out once a vessel can no longer hold what was '
                'inside it.',
     'colors': 'A planet here often shows intensity that, once it finally releases, comes '
               'out all at once rather than in a slow, manageable leak. Venus at this '
               'degree can indicate love or desire that, once spoken, cannot be walked '
               'back or diluted. Mars or Pluto here suggests feeling with no polite '
               'half-measure the moment the seal actually breaks.',
     'reflection': 'What have you been keeping carefully bottled, that would completely '
                   'change the air in the room the instant it broke open?'},
    {'degree': 3,
     'image': 'A house-raising: neighbors gather to build a home together in a single '
              'day.',
     'meaning': 'Labor pooled fast, many hands framing walls that no one of them could '
                'have raised alone. Scorpio is so often read as self-sufficient and '
                'solitary that this early degree comes as a genuine correction: real '
                'shelter, here, depends on trusting a whole community enough to let them '
                'literally build the place you will live your most private life inside. '
                'There is real vulnerability folded into that trust, and the degree treats '
                'it as strength rather than exposure, since the house standing by evening '
                'is proof the trust was warranted.',
     'colors': 'A planet at this degree often favors building something durable through '
               'shared labor rather than insisting on solo effort. Saturn here can '
               'indicate real structural support drawn from community. On the fourth '
               'house, it favors a home literally secured or sustained by the goodwill of '
               'people outside the immediate family.',
     'reflection': 'What has been raised for you by other hands, that you have been slow '
                   'to credit as a shared structure rather than something you built '
                   'entirely alone?'},
    {'degree': 4,
     'image': 'A young man carries a lit candle carefully through a solemn ceremony.',
     'meaning': 'Fire held with both hands, walked slowly, shielded from nothing but '
                'steady attention. This degree honors devotion made physical rather than '
                'only felt privately: a small, vulnerable flame carried deliberately '
                "through a room, extinguishable at every step, entrusted to someone "
                "young enough that the responsibility itself is part of the rite. "
                "Scorpio's usual intensity reads as heat that consumes; here the heat is "
                'carried gently, on purpose, toward something the carrier has agreed to '
                'treat as sacred.',
     'colors': 'A planet at this degree often shows devotion made visible and literal, a '
               'private flame carried into a public or ceremonial setting. Neptune or the '
               'Sun here can indicate real reverence expressed through careful, exact '
               'action rather than through words alone.',
     'reflection': 'What small flame are you currently carrying through a room, careful '
                   'that nothing puts it out before it arrives where it is going?'},
    {'degree': 5,
     'image': 'A massive rocky shore takes the pounding of the sea, wave after wave, and '
              'holds.',
     'meaning': 'Endurance tested continuously rather than once, and proven only by '
                'repetition. Neither the rock nor the water backs down: the sea keeps '
                'arriving, the shore keeps absorbing it, and over enough time both are '
                'genuinely altered by the encounter even though neither one concedes. '
                "Scorpio's strength is frequently exactly this kind, not a single "
                'dramatic stand but a willingness to keep meeting the same relentless '
                'force, degree after degree, letting the shape change slowly rather than '
                'breaking all at once.',
     'colors': 'A planet at this degree often shows resilience under pressure that does '
               'not let up, strength built by repeated impact rather than a single test. '
               'Saturn here favors real, tested endurance. Pluto can indicate a person '
               'genuinely shaped, over years, by whatever kept arriving.',
     'reflection': 'What has been pounding at you steadily, and what shape has that '
                   'actually carved you into, whether or not you ever agreed to it?'},
    {'degree': 6,
     'image': 'A gold rush pulls people from their homes, chasing a fortune still buried '
              'underground.',
     'meaning': 'Desire strong enough to uproot an entire life for something not yet '
                'found, only rumored to be there. This degree names Scorpio\'s appetite for '
                'buried value plainly: real material stakes, a willingness to leave '
                'ordinary safety behind for the chance at what has not been proven to '
                'exist yet. Not everyone who goes looking finds gold, and the degree is '
                'honest about that gamble even while it honors the hunger that sends '
                'people digging in the first place.',
     'colors': 'A planet here often shows real willingness to abandon safety for a chance '
               'at buried value, material, emotional, or otherwise. Jupiter can indicate '
               'genuine fortune actually found this way. Mars here shows the raw drive to '
               'go looking regardless of the odds against it.',
     'reflection': 'What fortune, still entirely unproven, are you currently willing to '
                   'leave safe, settled ground to go dig for?'},
    {'degree': 7,
     'image': 'Deep-sea divers descend below the surface light, working in dark, '
              'pressurized water.',
     'meaning': "This is Scorpio's own imagery in its most literal form: going under, "
                'past where light easily reaches, doing real, trained work at a depth '
                "most people never choose to enter. The descent is not reckless, it is "
                'equipped and deliberate, a decision that the valuable work actually '
                'happens below the surface everyone else stays at. There is professional '
                'discipline in it, not just daring, the difference between drowning and '
                'diving being almost entirely a matter of preparation.',
     'colors': 'A planet here often shows comfort and real skill operating in genuinely '
               'deep or high-pressure territory, psychological, financial, sexual. Pluto '
               'or Saturn can indicate real expertise doing work most people avoid '
               'because it is too far down to be comfortable.',
     'reflection': 'What are you currently equipped and willing to go get, that most '
                   'people around you would not follow you down for?'},
    {'degree': 8,
     'image': 'Moonlight lies flat and calm across the surface of a still lake.',
     'meaning': 'A rare, total pause: reflected light instead of direct heat, water so '
                'undisturbed it can hold a whole reflection without distortion. After a '
                'gold rush and a dive into dark water, this degree hands Scorpio '
                'something it rarely gets credit for wanting, real stillness, the kind of '
                'calm that only shows up once the day\'s intensity has actually passed and '
                'nothing is left stirring the surface.',
     'colors': 'A planet at this degree often shows emotional calm that arrives '
               'specifically after intensity, or specifically at night. The Moon, '
               'unsurprisingly, is very much at home here, a feeling life that finds its '
               'clearest reflection in quiet rather than in crisis.',
     'reflection': 'When was the last time your own surface was calm enough to actually '
                   'hold a clear reflection?'},
    {'degree': 9,
     'image': 'A dentist works carefully inside a patient\'s mouth, repairing what has '
              'gone wrong beneath the surface.',
     'meaning': 'Necessary, precise, uncomfortable work performed in one of the body\'s '
                'most guarded openings. No one looks forward to this appointment, and '
                "avoiding it only lets the problem worsen where it cannot be seen. Scorpio "
                "understands, better than most signs, that real repair sometimes only "
                'happens by going directly into the tender, defended place and doing the '
                'exact, unglamorous work the moment actually requires.',
     'colors': 'A planet here often shows real willingness to do precise, uncomfortable '
               'repair work at close range on something sensitive. Saturn or Mars can '
               'indicate a talent for actually fixing what is broken, rather than merely '
               'numbing the pain around it.',
     'reflection': 'What overdue, uncomfortable repair have you been postponing, that '
                   'only gets worse the longer you avoid the appointment?'},
    {'degree': 10,
     'image': 'Old friends gather again around a shared table, breaking bread together.',
     'meaning': 'Relationship resumed exactly where it left off, nourishment doubling as '
                'reconnection. At the close of the sign\'s first third, Scorpio gets a '
                'genuinely warm degree: not crisis, not intensity, just people who know '
                'each other well, gathered again, fed. Trust like this does not need to be '
                'rebuilt from nothing, it was banked long ago and simply gets picked back '
                'up the moment everyone sits back down.',
     'colors': 'A planet here often shows real capacity for loyal, long-running '
               'friendship that survives distance and time apart without souring. Venus '
               'or Jupiter can indicate relationships that reliably, dependably feed you '
               'whenever you return to them.',
     'reflection': 'Which old table are you overdue to sit back down at?'},
    {'degree': 11,
     'image': 'A drowning man is pulled from the water and saved just in time.',
     'meaning': 'Crisis met by intervention, danger real enough that the outcome could '
                'genuinely have gone the other way. Scorpio knows something about being '
                'in over your head, about needing another hand to arrive at exactly the '
                'right moment rather than a moment too late. The degree does not pretend '
                'the near-loss was not real; it simply insists that the rescue, when it '
                'comes, is every bit as real as the danger was.',
     'colors': 'A planet here can indicate real experience of being helped through a '
               'genuine crisis, or of being the one who does the helping. Neptune or Mars '
               'here often shows someone who either once truly needed saving, or has '
               'become genuinely skilled at doing the saving for others.',
     'reflection': 'Who pulled you out of water that was actually closing over your head, '
                   'and have you actually thanked them for it?'},
    {'degree': 12,
     'image': 'Diplomats and dignitaries mingle in formal splendor at an embassy ball.',
     'meaning': "Intimacy conducted at the most guarded social register there is, "
                'alliances made and quietly tested over champagne, every gesture read for '
                'what it actually signals about who holds leverage over whom. Scorpio '
                'understands that even the most glittering social occasion can be doing '
                'real strategic work underneath the music. This is not cynicism, it is '
                'clear sight into what a formal room is actually negotiating while '
                'everyone smiles.',
     'colors': 'A planet at this degree often shows fluency in high-stakes social '
               'diplomacy, reading what is genuinely being negotiated beneath polite '
               'conversation. Venus or Mercury can indicate real skill at building '
               'alliances inside formal, closely watched settings.',
     'reflection': 'What is actually being negotiated at the next formal gathering you '
                   'attend, underneath the small talk everyone is making?'},
    {'degree': 13,
     'image': 'An inventor runs an experiment in the laboratory, testing an idea against '
              'reality.',
     'meaning': "A hypothesis meets actual conditions, and the inventor is willing to be "
                "wrong in service of finding out what is genuinely true. Scorpio's "
                'investigative hunger takes a methodical, literal form here: not guessing, '
                'testing, and testing again if the first result disappoints, until the '
                'answer is real rather than merely assumed. There is real patience under '
                'the intensity, since a good experiment cannot be rushed into confirming '
                'what the inventor already hoped.',
     'colors': 'A planet here often shows a genuine appetite for rigorous testing rather '
               'than settling for untested theory. Uranus or Mercury can indicate real '
               'inventive capacity and comfort with a trial that might not work the '
               'first time.',
     'reflection': 'What theory of your own are you still avoiding actually testing '
                   'against reality?'},
    {'degree': 14,
     'image': 'Linemen work high above the street, running new telephone connections '
              'between poles.',
     'meaning': 'Literal wiring for communication, dangerous work performed overhead so '
                "that distant voices can eventually reach each other. Scorpio's gift for "
                'real, unguarded intimacy depends on exactly this kind of unglamorous '
                'infrastructure: the connection has to actually be built and maintained by '
                'someone willing to climb up and string the line, not simply wished into '
                'existence.',
     'colors': 'A planet here often shows real skill establishing durable channels of '
               'communication between people, or between systems. Mercury or Uranus can '
               'indicate a genuine talent for literally wiring people together across '
               'real distance.',
     'reflection': 'What connection have you been meaning to actually run the line for, '
                   'instead of hoping the signal reaches on its own?'},
    {'degree': 15,
     'image': 'Children play together around five small mounds of sand.',
     'meaning': 'The exact midpoint of the sign, and it lands somewhere unexpectedly '
                'light: simple shared play, small hills built and knocked down and built '
                'again, with no real stakes attached to any of it. After crisis, '
                'diplomacy, and careful experiment, Scorpio gets a genuine rest here, '
                'nothing to fix, protect, or transform, just five mounds of sand and some '
                'children enjoying exactly what is in front of them.',
     'colors': 'A planet here often shows a real capacity for low-stakes, unburdened play '
               'even inside an otherwise intense life. The Moon or Venus can indicate '
               'genuine ease returning to something simple whenever the heavier work '
               'allows it.',
     'reflection': 'What small, unburdened pleasure have you not let yourself enjoy '
                   'lately, because it did not feel important enough to earn the time?'},
    {'degree': 16,
     'image': "A girl's face breaks slowly into a smile.",
     'meaning': 'An internal shift becoming visible in real time, feeling surfacing '
                "plainly on the face before words have caught up to explain it. Scorpio "
                'usually guards its expressions with real care; this degree offers '
                'something rarer, an unguarded moment where whatever is happening inside '
                'simply shows, unfiltered and warm, without the sign\'s customary '
                'management of what gets seen.',
     'colors': 'A planet here often shows real capacity for spontaneous, unguarded '
               'warmth breaking through an otherwise careful exterior. Venus or the Sun '
               'can indicate genuine, visible delight that does not get held back once it '
               'arrives.',
     'reflection': 'What is currently breaking, slowly, into a smile in you, whether or '
                   'not you have let anyone else see it yet?'},
    {'degree': 17,
     'image': 'A woman, entirely her own source, becomes the parent of her own child.',
     'meaning': 'Creation without needing another party to complete it, self-generated '
                'and self-sufficient, the whole act contained inside one person\'s will. '
                "This is one of Scorpio's most striking images of sovereign power: a new "
                'life produced from a single source, answerable to nothing outside '
                'itself, needing no outside collaborator\'s permission to exist. It is '
                'less about literal biology than about the degree\'s larger claim, that '
                'real creation sometimes only requires one committed source.',
     'colors': 'A planet here often shows real capacity for self-originated creation, '
               'projects, art, an entire identity, built from personal will rather than '
               'needing outside collaboration to begin. Pluto or the Sun can indicate '
               'someone who generates their own next chapter without waiting for anyone\'s '
               'permission.',
     'reflection': 'What have you been waiting for someone else\'s involvement to start, '
                   'that you actually already have everything you need to generate on '
                   'your own?'},
    {'degree': 18,
     'image': 'A path runs through woods lit up in full, brilliant autumn color.',
     'meaning': 'Beauty tied specifically to a season of dying back, the most vivid color '
                'arriving right before the leaves fall entirely. Scorpio understands this '
                'paradox intimately: that things often become most striking exactly at '
                'the point they are ending, that decline and radiance are not opposites '
                'here but the very same moment, seen from two different angles.',
     'colors': 'A planet here often shows beauty or intensity that peaks specifically '
               'during a transition or an ending. Neptune or Venus can indicate someone '
               'whose most vivid work, or most vivid feeling, arrives right at a closing '
               'chapter rather than at its beginning.',
     'reflection': 'What in your life is currently at its most vivid, precisely because '
                   'it is also ending?'},
    {'degree': 19,
     'image': 'A parrot listens closely, then repeats back exactly what it overheard.',
     'meaning': 'Information absorbed and returned faithfully, sometimes without any real '
                'understanding of what it actually means. This degree carries a genuine '
                'caution about repeating what was only overheard rather than truly '
                'understood, right alongside real respect for the raw capacity to absorb '
                'and reproduce something with total accuracy, word for word.',
     'colors': 'A planet here often shows a gift for accurate mimicry or reporting, '
               'sometimes running ahead of real comprehension. Mercury can indicate a '
               'quick, accurate ear, genuinely useful, and occasionally risky if repeated '
               'without the context that gave it meaning.',
     'reflection': 'What have you been repeating lately that you actually overheard, '
                   'rather than understood firsthand?'},
    {'degree': 20,
     'image': 'A woman draws back two dark curtains, opening onto whatever lies beyond '
              'them.',
     'meaning': 'Concealment lifted on purpose, both hands doing the work rather than a '
                "single hasty tug. This is one of Scorpio's clearest self-portraits: the "
                'willingness to actually open what has been kept dark, deliberately, and '
                'see what is really there instead of guessing about it forever. Nothing '
                'in the image says what waits behind the curtains is comfortable, only '
                'that it is finally, fully in view.',
     'colors': 'A planet here often shows real courage to open what has been '
               'deliberately kept hidden, a conversation, a truth, a locked room. Pluto '
               'or the Moon can indicate someone specifically gifted at drawing back what '
               'everyone else leaves curtained.',
     'reflection': 'What dark curtain are you finally ready to draw back with both '
                   'hands, instead of just peering through the gap between them?'},
    {'degree': 21,
     'image': 'A soldier disobeys an order, refusing to carry it out.',
     'meaning': "Two readings sit inside the same image: dereliction, if you judge only "
                "by the broken chain of command, or genuine conscience, if you judge by "
                "what the soldier actually refused to do and why. Scorpio's whole "
                'relationship to authority runs through this degree, since real integrity '
                'sometimes means refusing what you have been told, trusting your own read '
                'of right and wrong over the safety of simple compliance, and accepting '
                'whatever penalty follows that choice.',
     'colors': 'A planet here often shows real willingness to break with expected '
               'obedience when conscience genuinely demands it. Saturn or Mars can '
               'indicate someone who has paid an actual cost for refusing an order they '
               'believed was wrong, and would refuse again.',
     'reflection': 'What order are you currently following only because refusing it '
                   'would cost you something you are not yet willing to lose?'},
    {'degree': 22,
     'image': 'Hunters set out at dawn after wild ducks.',
     'meaning': "Purposeful pursuit, timed precisely to the hour when the target is "
                "actually findable. This is Scorpio's hunting instinct in its plainest "
                'form, not aimless wandering but a deliberate, well-timed setting-out '
                'after something specific, patience and skill both required for the '
                'morning to actually produce anything.',
     'colors': 'A planet here often shows real skill at timed, deliberate pursuit of a '
               'specific goal rather than constant, unfocused effort. Mars or Jupiter can '
               'indicate someone who knows exactly when to set out after what they '
               'actually want.',
     'reflection': 'What have you been meaning to set out after at the right hour, '
                   'instead of waiting for it to simply arrive on its own?'},
    {'degree': 23,
     'image': 'An ordinary rabbit transforms into a small nature spirit.',
     'meaning': 'The everyday revealed as more than it first appeared, magic located '
                "inside something entirely common rather than exotic. Scorpio's gift for "
                'seeing beneath the surface finds one of its gentlest expressions here, '
                'not excavating something dark, just noticing that the plain animal '
                'sitting right in front of you was always a little more than it looked.',
     'colors': 'A planet here often shows a gift for finding real enchantment inside '
               'ordinary, easily overlooked things. Neptune or Venus can indicate someone '
               'who sees the extraordinary hiding inside the plainest available '
               'material.',
     'reflection': 'What ordinary thing in your life might actually be more enchanted '
                   'than you have been giving it credit for?'},
    {'degree': 24,
     'image': 'Crowds come down from the mountain to hear a single man speak.',
     'meaning': "Many people, drawn by one voice, willing to leave higher, safer ground "
                "and gather to listen. This degree is about real magnetism, not "
                'manufactured, since no one in the crowd was forced down the slope, but a '
                'pull genuine enough that people chose the descent for the sake of '
                'hearing what one person actually had to say.',
     'colors': 'A planet here often shows real, earned magnetism, the capacity to draw '
               'people toward a single message or presence without needing to force the '
               'gathering. Jupiter or the Sun can indicate someone whose voice is worth '
               'an actual crowd making the trip down to hear.',
     'reflection': 'What have you had to say that would genuinely be worth someone '
                   'else\'s whole descent from the mountain to come hear?'},
    {'degree': 25,
     'image': 'An X-ray photograph reveals the structure hidden beneath the skin.',
     'meaning': "A direct image of exactly what Scorpio spends its whole sign seeking, "
                'not a guess, an actual picture of the interior, made visible without '
                'needing to cut anything open to get it. This is diagnostic, clinical '
                'seeing, straight past the surface, useful precisely because it does not '
                'flinch from whatever it finds underneath.',
     'colors': 'A planet here often shows real capacity to see straight through surface '
               'presentation to the actual structure underneath it. Pluto or Mercury can '
               'indicate a mind that diagnoses accurately rather than guessing from '
               'appearances alone.',
     'reflection': 'If someone took an honest X-ray of your current situation, what '
                   'structure would it actually reveal underneath the skin of it?'},
    {'degree': 26,
     'image': 'A group makes camp quickly, settling into unfamiliar new territory.',
     'meaning': 'Adaptability tested by real displacement: the group has not chosen '
                'comfort, only survival, and manages it with real, practiced skill, '
                'working with whatever the new ground actually offers instead of waiting '
                'for ideal conditions that are not coming. This degree honors '
                'resourcefulness under genuine unfamiliarity, the capacity to make a real '
                'home out of wherever you actually are, rather than out of wherever you '
                'wish you were instead.',
     'colors': 'A planet here often shows real resourcefulness settling into unfamiliar '
               'circumstances, making do with what is actually at hand rather than '
               'waiting for better conditions to arrive first. Saturn or Mars can '
               'indicate someone who adapts fast and effectively to genuinely new '
               'territory.',
     'reflection': 'What unfamiliar territory are you currently standing in, that you '
                   'could actually start making real camp in, instead of waiting to feel '
                   'more settled first?',
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 27,
     'image': 'A military band marches loudly through the city streets.',
     'meaning': 'Rhythm and order, sound loud enough that everyone for blocks can hear '
                'it approaching before they ever see it. This degree honors the public '
                'display of collective discipline, not stealth, the opposite of it, a '
                'whole coordinated group announcing itself boldly, marching in step, '
                'entirely unmissable on purpose.',
     'colors': 'A planet here often shows real comfort with loud, coordinated public '
               'presence rather than quiet, private operation. Mars or Jupiter can '
               'indicate someone whose cause or group marches proudly through the '
               'street rather than hiding its intentions.',
     'reflection': 'What have you been keeping quiet, that might actually deserve its '
                   'own marching band down the street?'},
    {'degree': 28,
     'image': 'The King of the fairies approaches the edge of his own kingdom.',
     'meaning': 'Authority returning to territory that already belongs to it, sovereignty '
                'over a realm most people cannot even perceive, let alone enter. This '
                "degree gives Scorpio's relationship to hidden power one of its most "
                'literal pictures: rule over an entire domain that operates by rules the '
                'ordinary daylight world neither recognizes nor needs to.',
     'colors': 'A planet here often shows real authority over a realm others do not '
               'fully perceive, the unconscious, the occult, an inner life that runs by '
               'its own laws. Neptune or Pluto can indicate genuine command over '
               'territory that stays largely invisible to everyone standing outside it.',
     'reflection': 'What domain do you actually already rule, that most people around you '
                   'do not even know exists?'},
    {'degree': 29,
     'image': "A mother makes an urgent appeal to her community's leader, pleading for "
              'her children\'s lives.',
     'meaning': 'Love pressed into its most desperate, most necessary form, not romantic, '
                'maternal, willing to stand directly before real power and ask, plainly, '
                'for mercy. This degree carries the full weight the sign has been '
                'building toward across its whole back half: stakes that are genuinely '
                'life and death, and a love fierce enough to face authority head-on '
                'rather than staying silent and hoping for the best.',
     'colors': 'A planet here often shows real willingness to advocate fiercely, '
               'publicly, for someone vulnerable who cannot advocate for themselves. The '
               'Moon or Mars can indicate a protective love, maternal or otherwise, that '
               'will stand before real power rather than staying quiet out of fear.',
     'reflection': 'Who are you currently pleading for, in front of whatever power '
                   'actually holds their fate in its hands?',
     'note': 'Note: the 1925 original for this degree used a dated, now-offensive ethnic '
             'term; the picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 30,
     'image': 'A jester in Halloween costume lets loose one night of sanctioned '
              'mischief.',
     'meaning': 'The final degree of the sign, and after twenty-nine degrees of real '
                'intensity, Scorpio closes by letting the mask come off in play instead of '
                'confession, permission, for one night, to be someone else entirely, '
                'harmlessly, with everyone in on the joke. This is transformation treated '
                'lightly at last: the very same gift the sign has spent its whole arc '
                'taking dead seriously, here let loose as pure, sanctioned mischief with '
                'nothing underneath it required to be true.',
     'colors': 'A planet here often shows real capacity to treat transformation and '
               'disguise as play, not only as depth work, a lightness about masks that '
               'balances out the sign\'s more serious relationship to them. Mercury or '
               'Venus can indicate genuine wit and delight in costume, performance, and '
               'sanctioned, harmless mischief.',
     'reflection': 'What mask would you actually enjoy putting on tonight, just for the '
                   'plain pleasure of being someone else for a few hours?'},
]

assert len(ENTRIES) == 30, f"expected 30 Scorpio degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Scorpio degrees out of order"
