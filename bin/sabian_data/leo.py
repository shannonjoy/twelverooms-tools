"""Sabian symbol data for Leo.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (jamesburgess.com / Sacred 7
Academy, kerykeion.net, astronarrative.com, cafeastrology.com,
sabian-calculator.com, and, for the two degrees where sources initially
disagreed, additional confirmation via sabiansymbols.com, Blain Bovee's
Sabian Symbol blog/boveeastrology.com, sabiansymbologist.wordpress.com,
and judithdehaan.substack.com) before being hand-typed. Leo 19 was
confirmed as "a houseboat party" (kerykeion's page was the lone outlier,
showing an unrelated "revival meeting" symbol) and Leo 24 was confirmed
as "an untidy, unkempt man" (again the lone kerykeion outlier showed an
unrelated symbol) -- both resolved by 5+ independent, mutually agreeing
sources. Do NOT extend this list, or write a new sign's list, without the
same verification discipline: fewer verified degrees beats any guessed
ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a case of
apoplexy"), not a verbatim quote of Marc Edmund Jones' 1953 book or Dane
Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`, `colors`,
and `reflection` are original Twelve Rooms interpretation, written fresh
for this project; none of it is copied from Jones or Rudhyar.

DATED IMAGERY: Leo 20's 1925 original names a specific real people (the
Zuni) performing a ceremonial sun ritual. Per Shannon's standing policy,
the canonical mapping is kept, but `image` restates it respectfully
without the specific ethnic/tribal label, and a `note` field is attached
below the symbol card. See SCHEMA.md for the full policy.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Leo", "slug": "leo", "glyph": "♌︎", "order": 5}

# The 30 degrees of Leo, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and an optional note (str) on the one degree whose
# 1925 original used dated ethnic imagery. See SCHEMA.md for what each
# field means.
ENTRIES = [
 {'degree': 1,
  'image': "A surge of blood rushes to a man's head as ambition takes hold "
           'of him.',
  'meaning': "This is the first degree of the entire sign, and it opens with "
             'pure, undisguised force: feeling that refuses to stay '
             "contained, color rushing straight to the surface. Nothing "
             "here is subtle or hidden, this is Leo's whole nature "
             'announced at the very start, an inner fire that will not sit '
             'quietly waiting for permission. The rush is a warning as much '
             'as a portrait: intensity this immediate needs somewhere '
             'honest to go, or it becomes its own emergency. The sign that '
             'will spend thirty degrees learning to rule a room begins by '
             'first discovering it cannot yet rule its own pulse.',
  'colors': 'A planet at Leo 1 tends to run hot and immediate, feeling '
            'arriving before thought has caught up to explain it. Mars '
            'here often shows a temper that flares fast and burns clean '
            'rather than smoldering. The Sun at this degree can indicate a '
            'vitality so strong it needs real outlets, physical, '
            'creative, expressive, or it turns inward and works against '
            'its owner.',
  'reflection': 'What in you rushes to the surface the instant you want '
                'something, and where does that heat actually want to go?'},
 {'degree': 2,
  'image': 'Children on a shared holiday come down with mumps together, and '
           'find unexpected fellowship in it.',
  'meaning': 'An illness becomes, unexpectedly, a shared holiday: children '
             'confined together by mumps discover a fellowship an ordinary '
             'school day would never have produced. Leo trusts that even '
             'an inconvenience, shared, can turn into belonging, that '
             'circumstance forcing people into the same room is not '
             'automatically a loss. There is something playful under the '
             "discomfort here, kids making the most of quarantine, "
             'laughter breaking out where boredom was expected. This '
             "degree suggests Leo's gift for turning any gathering, "
             'however accidental its cause, into real warmth.',
  'colors': 'A planet at this degree often shows a talent for finding real '
            'camaraderie in circumstances nobody chose, illness, delay, '
            'disruption, and making the shared inconvenience genuinely '
            'fun. Venus here can indicate friendships forged fast under '
            'odd conditions. Jupiter favors turning any enforced '
            'togetherness into an unexpectedly good time.',
  'reflection': 'What unplanned, mildly inconvenient togetherness has '
                'actually given you real company you would not trade back?'},
 {'degree': 3,
  'image': 'A woman has her hair bobbed, trading an old style for a new one.',
  'meaning': 'A change to nothing more than a hairstyle, and identity '
             'shifts along with it: this degree trusts that outward '
             'reinvention is not vanity, it is a real way of updating who '
             "you are willing to be seen as. Leo cares, honestly and "
             'without apology, about how it is perceived, and this degree '
             'honors that as legitimate work rather than shallow fuss. The '
             'cut itself is small; what it signals, a willingness to leave '
             'an old version of the self behind in favor of a more current '
             'one, is not small at all.',
  'colors': 'A planet at this degree often favors reinvention through '
            'appearance, a genuine, not merely cosmetic, shift in '
            'self-presentation that precedes or announces an inner one. '
            'Venus here can indicate real skill at using style as honest '
            'self-expression rather than disguise. The Ascendant at this '
            'degree suggests someone whose look changes visibly whenever '
            'their sense of self does.',
  'reflection': 'What version of your own appearance are you overdue to '
                'leave behind, on purpose?'},
 {'degree': 4,
  'image': 'A man in formal dress stands beside the antlered trophies of a '
           'hunting expedition.',
  'meaning': 'Success, displayed rather than merely felt: the trophies say '
             'plainly that a real contest happened and this man won it, '
             'and he is dressed for the occasion of being seen having won. '
             "Leo rarely hides its wins, and this degree makes the case "
             'that it should not have to, that pride in an earned '
             'accomplishment is honest rather than boastful when the '
             'accomplishment is real. There is formality here too, a '
             'sense that achievement deserves ceremony, not just a quiet '
             'private satisfaction.',
  'colors': 'A planet at this degree often shows a comfort with visible '
            'achievement, displaying what was earned rather than '
            'downplaying it. The Sun or Jupiter here can indicate someone '
            'who dresses the part for their own victories, unembarrassed '
            'by the trophies. It rewards distinguishing real earned pride '
            'from mere show.',
  'reflection': 'What have you actually earned that you are still, out of '
                'habit, keeping off the wall?'},
 {'degree': 5,
  'image': 'Weathered rock formations tower at the edge of a deep canyon.',
  'meaning': 'Scale, and the kind of grandeur that took ages to carve '
             'rather than a single dramatic gesture: this degree is Leo '
             'meeting a monument nobody built on purpose, stone shaped '
             'slowly by wind and water into something that now simply '
             'commands attention. Not every impressive thing is performed; '
             'some of it is just accumulated time, made visible. Leo, so '
             'oriented toward deliberate display, learns here to also '
             'recognize grandeur that occurred rather than was staged.',
  'colors': 'A planet at this degree often carries a natural, unforced '
            'gravitas, presence that does not need to perform because it '
            'has been built over real time. Saturn here can indicate an '
            'authority that has simply accrued, degree by degree, rather '
            'than been claimed all at once. It rewards trusting weight '
            'that was earned slowly.',
  'reflection': 'What in you has become genuinely impressive not because '
                'you staged it, but simply because you kept standing '
                'through enough weather?'},
 {'degree': 6,
  'image': 'An old-fashioned woman comes face to face with a thoroughly '
           'modern girl.',
  'meaning': 'Two eras, face to face, neither one entirely right: the '
             'old-fashioned woman carries real standards worth keeping, '
             'the modern girl carries real freedoms worth having, and this '
             'degree does not resolve the argument between them. Leo has '
             'its own conservative streak, loyal to what has always '
             'worked, right alongside its appetite for being current, '
             "seen, and relevant. This is the sign meeting its own "
             'internal generational gap, tradition and reinvention sitting '
             'across from each other without either one winning outright.',
  'colors': 'A planet at this degree often shows real tension between '
            'honoring what came before and wanting to be visibly, '
            'fashionably of the moment. The Moon or Saturn here can '
            'indicate loyalty to inherited standards even while genuinely '
            'admiring what is new. It rewards letting both women stay in '
            'the room instead of forcing one to leave.',
  'reflection': 'Where in you are the old standard and the new style still '
                'facing off, and does one of them actually have to win?'},
 {'degree': 7,
  'image': 'The constellations blaze across the night sky.',
  'meaning': 'The whole sky, lit and legible, patterns that have been '
             'named and told as stories for as long as anyone has looked '
             'up. Leo, ruled by the Sun, meets here the vast field of '
             'light that only becomes visible once the Sun has gone down, '
             "a reminder that even the sign of the solar self has a night "
             'version, dazzling in an entirely different register. This '
             'degree is about scale and story at once: countless '
             'individual points of light, and the human habit of '
             'connecting them into meaning.',
  'colors': 'A planet at this degree often shows a gift for seeing pattern '
            'and story across something vast, connecting scattered points '
            'into a single legible shape. Uranus or Jupiter here can '
            'indicate real vision that operates at a genuinely large '
            'scale. It rewards remembering that even brilliance has a '
            'version that only shows itself in the dark.',
  'reflection': 'What scattered points in your own life are actually '
                'already forming a constellation, if you stepped back far '
                'enough to see it?'},
 {'degree': 8,
  'image': 'A political agitator stands before a crowd, spreading his '
           'revolutionary ideas.',
  'meaning': 'Conviction, delivered loudly and on purpose, to whoever will '
             'listen: this degree is belief that refuses to stay private, '
             'certain enough of its own rightness to stand in public and '
             "try to change minds. Leo has real courage for exactly this "
             'kind of visible stance, the willingness to be the one out '
             'front saying the unpopular true thing while a crowd decides '
             'whether to agree. There is real risk in it too, since public '
             'conviction invites public opposition, and this degree does '
             'not pretend otherwise.',
  'colors': 'A planet at this degree often shows genuine conviction that '
            'wants an audience, belief strong enough to be spoken rather '
            'than only privately held. Mars or Uranus here can indicate a '
            'natural agitator for causes they actually believe in. It '
            'rewards making sure the fire is aimed at something worth the '
            'exposure.',
  'reflection': 'What do you believe strongly enough to say out loud in a '
                'room that might disagree?'},
 {'degree': 9,
  'image': 'Glassblowers shape delicate vases with the long, controlled '
           'breath of their craft.',
  'meaning': 'Beauty made from breath and heat, shaped by exactly the '
             'right amount of pressure, not too much, not too little. This '
             'degree honors craft that is inseparable from the body doing '
             "it, the glassblower's own controlled exhale becoming the "
             "very thing that gives the vase its form. Leo's creative "
             'fire, usually big and immediate, learns here a quieter, more '
             'disciplined register: the same heat, applied with real '
             'control, produces something delicate rather than merely '
             'dramatic.',
  'colors': 'A planet at this degree often shows creative expression that '
            'depends on real, practiced control rather than raw impulse '
            'alone. Venus or Mercury here can indicate a gift for shaping '
            'something beautiful and delicate out of considerable inner '
            'heat. It rewards trusting the discipline as much as the '
            'fire.',
  'reflection': 'What are you currently shaping that needs your heat '
                'applied carefully, rather than all at once?'},
 {'degree': 10,
  'image': 'Dew catches the early light across an open field.',
  'meaning': 'Nothing here has been performed yet, this is beauty that '
             'occurs before anyone is watching, before the day has '
             'properly begun. This degree gives Leo, so identified with '
             'the full brightness of noon, a much quieter version of its '
             'own light: sunrise catching moisture that will simply '
             'evaporate once the morning gets going. There is something '
             'honest about beauty this brief, unrepeatable in exactly this '
             'form, gone by the time most people are awake to see it.',
  'colors': 'A planet at this degree often carries a quieter, early kind '
            'of brilliance, gifts that show themselves plainly before the '
            'rest of the day, and the world, catches up. Venus here can '
            'indicate beauty that does not need an audience to be '
            'complete. It rewards noticing what is genuinely lovely before '
            'it insists on being seen.',
  'reflection': 'What in your life has been quietly beautiful lately, '
                'before anyone else was awake to notice it?'},
 {'degree': 11,
  'image': 'Children swing from a rope tied high in an old oak tree.',
  'meaning': 'Play, held by something old and sturdy enough to trust '
             'completely: the oak has been standing for generations, and '
             'children swing from it without a second thought about '
             "whether it will hold. Leo's whole relationship to play lives "
             'in this image, joy that gets to be unguarded because the '
             'structure underneath it is genuinely solid. This is not '
             'reckless play, it is play made possible by real, '
             'long-established support.',
  'colors': 'A planet at this degree often shows real capacity for '
            'unguarded joy, made possible by trusting something solid '
            'underneath it. The Sun or Jupiter here can indicate a '
            'childlike delight that has never actually needed to grow '
            'cautious. It rewards remembering which sturdy things in your '
            'life still let you swing freely.',
  'reflection': 'What old, trustworthy structure in your life still lets '
                'you play without worrying it might give way?'},
 {'degree': 12,
  'image': 'Adults gather for an evening lawn party under strings of '
           'lantern light.',
  'meaning': "Adults, gathered outdoors after dark, lit by something "
             "warmer and more forgiving than daylight. This degree is "
             "Leo's gift for hosting made visible, the instinct to bring "
             'people together somewhere beautiful and let the evening do '
             'the rest of the work. Lantern light flatters everyone '
             'equally, and there is real generosity in choosing exactly '
             'that kind of light for a gathering, one that makes every '
             'guest look and feel their best.',
  'colors': 'A planet at this degree often shows a genuine talent for '
            'hosting, creating an atmosphere warm and flattering enough '
            'that guests relax without needing to be told to. Venus or the '
            'Sun here can indicate real pleasure taken in gathering people '
            'well. It rewards trusting your own instinct for the right '
            'kind of light.',
  'reflection': 'What gathering have you been meaning to host, exactly the '
                'way you know how to light it?'},
 {'degree': 13,
  'image': 'An old sea captain rocks slowly on the porch of his cottage.',
  'meaning': 'A life once lived at real scale, now settled into something '
             'much smaller and steadier: the captain who once commanded a '
             "ship now simply rocks, having earned the right to stillness. "
             "Leo's fire eventually asks what comes after the "
             'performance, and this degree answers plainly, a long, '
             'satisfied rest, memory doing the work that adventure used to '
             'do. There is no diminishment in it, only a different, '
             'well-earned register of the same life.',
  'colors': 'A planet at this degree often shows someone at genuine peace '
            'with a chapter that has closed, content to hold its memory '
            'rather than chase its return. Saturn here can indicate real '
            'dignity in slowing down after a life fully lived at speed. It '
            'rewards trusting that rocking quietly is not the same as '
            'being finished.',
  'reflection': 'What chapter of real adventure have you actually earned '
                'the right to simply sit with now?'},
 {'degree': 14,
  'image': 'A soul waits quietly for its chance to be fully expressed in '
           'the world.',
  'meaning': 'Not yet visible, but entirely ready: this degree holds a '
             'self that exists in full already, waiting only for its '
             "chance to be shown to the world. Leo's whole project is "
             'exactly this, an inner brightness insisting on outward form, '
             'and this degree names the waiting room before that happens, '
             'the real readiness that precedes the debut. Nothing is '
             'missing here except opportunity; the substance is already '
             'whole.',
  'colors': 'A planet at this degree often shows genuine inner readiness '
            'ahead of outer opportunity, a self that is complete before '
            'circumstance catches up to let it show. The Sun here can '
            'indicate someone whose real self is already formed and '
            'simply waiting for its stage. It rewards trusting the '
            'readiness even while the stage is still being built.',
  'reflection': 'What in you is already fully formed, just waiting for the '
                'room that will finally let it show?'},
 {'degree': 15,
  'image': 'A pageant of floats moves down a street lined with cheering '
           'crowds.',
  'meaning': 'The exact midpoint of Leo, and it arrives with a full '
             'parade: spectacle built deliberately, watched by a street '
             'packed with people who came specifically to see it. This is '
             'Leo at its most literal, performance as celebration, '
             'publicly declared and publicly received. There is real '
             'craft behind a pageant like this, months of preparation '
             'compressed into a single triumphant pass down the street, '
             "and the crowd's applause is not incidental, it is the whole "
             'point.',
  'colors': 'A planet at this degree often shows a genuine gift for '
            'spectacle, producing something built specifically to be '
            'watched and celebrated by a crowd. The Sun or Venus here can '
            'indicate real talent for public performance and pageantry. It '
            'rewards remembering that some things are actually meant to '
            'be seen by everyone at once.',
  'reflection': 'What have you built that genuinely deserves its own '
                'parade down the street?'},
 {'degree': 16,
  'image': 'The storm breaks, and brilliant sunshine floods back over '
           'everything.',
  'meaning': 'Relief made visible: the storm actually ends, and the light '
             'that follows feels earned precisely because of what came '
             "before it. This degree trusts that Leo's brightness means "
             'more, and lands harder, once it has been tested by something '
             'genuinely difficult. Nothing about this sunshine is naive, '
             'it has weather behind it, and that is exactly what makes it '
             'worth celebrating rather than taking for granted.',
  'colors': 'A planet at this degree often shows resilience that produces '
            'real, earned brightness on the other side of difficulty. '
            'Jupiter or the Sun here can indicate someone whose optimism '
            'means the most because it survived something real. It '
            'rewards letting the relief be as loud as the storm was.',
  'reflection': 'What storm in your life has just cleared, and have you '
                'actually let yourself enjoy the sunshine after it?'},
 {'degree': 17,
  'image': 'A choir of ordinary volunteers, without robes, sings hymns '
           'together.',
  'meaning': 'Devotion, offered without the usual costume: this choir '
             'sings the same hymns a robed choir would, but stripped of '
             'the formal uniform, the singing itself carries the whole '
             'weight of the offering. Leo, so associated with performance, '
             'meets here a version of expression that needs no polish or '
             'vestment to be completely sincere. The music is real '
             'whether or not the choir looks the part.',
  'colors': 'A planet at this degree often shows heartfelt expression that '
            'does not depend on formal presentation to be genuine. Venus '
            'or Neptune here can indicate real, unpretentious devotion '
            'expressed through voice or craft. It rewards trusting that '
            'sincerity outperforms costume.',
  'reflection': 'What are you currently offering wholeheartedly, even '
                'without the formal trappings that usually go with it?'},
 {'degree': 18,
  'image': 'A teacher runs a chemistry experiment live in front of a room '
           'of students.',
  'meaning': 'Knowledge, demonstrated live rather than just described: the '
             'teacher performs the experiment in front of the room '
             'specifically so the students can watch the reaction happen '
             "in real time. Leo's instinct to perform finds real purpose "
             'here, teaching as a kind of theater with an actual '
             'educational payoff, showmanship in service of genuine '
             'understanding rather than mere display.',
  'colors': 'A planet at this degree often shows a gift for teaching '
            'through demonstration, making an idea vivid and visible '
            'rather than only explained. Mercury or Jupiter here can '
            'indicate real talent for turning instruction into something '
            'the room actually watches, engaged. It rewards performing '
            'your knowledge, not just stating it.',
  'reflection': 'What do you know well enough to demonstrate live, rather '
                'than only explain?'},
 {'degree': 19,
  'image': 'A houseboat party carries on late, its lights scattering '
           'across the water.',
  'meaning': 'Celebration, set loose from solid ground: a houseboat party '
             'gets to be temporary and floating by design, freedom from '
             "the usual rules of a fixed address. Leo's love of a good "
             'gathering meets here its most unmoored version, revelry '
             'that drifts rather than anchors, lit up and visible from '
             'the shore. There is real pleasure in exactly this kind of '
             'loosened structure, festivity without the obligation to '
             'stay put.',
  'colors': 'A planet at this degree often shows a genuine appetite for '
            'celebration untethered from routine, joy that gets to drift '
            'for a while rather than stay fixed. Venus or Jupiter here can '
            'indicate real talent for creating festive, temporary freedom. '
            'It rewards remembering that some good times are meant to '
            'float rather than settle.',
  'reflection': 'Where in your life could you use a little more houseboat, '
                'freedom from routine that still knows how to come back to '
                'shore?'},
 {'degree': 20,
  'image': 'A circle of dancers moves in ceremony, calling up the sun.',
  'meaning': 'A community moves together in ceremony, calling up the sun '
             'with practiced, deliberate steps passed down long before any '
             "of them were born. This degree honors ritual that treats "
             "the Sun, Leo's own ruler, as something worth actively "
             'courting rather than simply assumed to rise. There is real '
             'devotion in choreography this precise, a whole people '
             'trusting that attention, offered in the right form, matters '
             'to the outcome.',
  'colors': 'A planet at this degree often shows genuine devotion to '
            'ritual and rhythm, especially ritual connected to light, '
            'season, or the Sun itself. The Sun or Jupiter here can '
            'indicate someone who honors tradition through active, '
            'embodied practice rather than passive belief. It rewards '
            'taking your own rituals as seriously as this ceremony takes '
            'its own.',
  'reflection': 'What ritual do you still perform, faithfully, to help '
                'call in the light you are hoping for?',
  'note': 'Note: the 1925 original for this degree used dated ethnic '
          'imagery; the picture above keeps its meaning in respectful, '
          'modern terms.'},
 {'degree': 21,
  'image': 'A flock of drunken chickens flaps wildly, trying and failing to '
           'get off the ground.',
  'meaning': 'Effort, thoroughly overmatched by its own condition: the '
             'chickens are trying, genuinely trying, to do something their '
             'current state makes almost impossible. This degree carries '
             'real comedy, and also a fair warning, ambition running well '
             'ahead of capacity in the moment, enthusiasm outpacing '
             "coordination. Leo's confidence is usually earned, but this "
             'degree shows what happens when the confidence arrives a '
             'little before the readiness does.',
  'colors': 'A planet at this degree can indicate enthusiasm that '
            'occasionally outpaces actual capability in the moment, '
            'effort more visible than results. Mercury or Mars here often '
            'shows someone who tries gamely even when the odds, or the '
            'coordination, are clearly against them. It rewards checking '
            'whether you are actually ready for the flight you are '
            'attempting.',
  'reflection': 'Where are you currently flapping hard at something your '
                'present state genuinely is not ready to pull off?'},
 {'degree': 22,
  'image': 'A carrier pigeon flies straight and true to complete its '
           'errand.',
  'meaning': 'A single, clear task, carried out with total reliability '
             'across real distance. The pigeon does not need to '
             'understand the whole context of the message, only to '
             'deliver it faithfully, and this degree honors that kind of '
             'loyalty, purpose reduced to one job, done completely. '
             "Leo's fire usually wants the credit along with the deed, "
             'but this bird performs its whole mission and simply '
             'arrives, message intact, without asking for applause.',
  'colors': 'A planet at this degree often shows real reliability at '
            'carrying something important across distance or difficulty, '
            'completing what was entrusted without needing acknowledgment '
            'along the way. Mercury here can indicate a gift for '
            'faithful, accurate delivery, whether of information, '
            'messages, or promises. It rewards trusting that the job well '
            'done is its own credit.',
  'reflection': 'What have you been faithfully carrying toward its '
                'destination, without needing anyone to watch you do it?'},
 {'degree': 23,
  'image': 'In the circus ring, a bareback rider performs her most '
           'dangerous trick.',
  'meaning': 'Skill, displayed at real risk, in front of a crowd who came '
             "specifically to watch the danger. This is Leo's performance "
             'instinct at its most literal, physical mastery shown off '
             'exactly where it can be seen and appreciated, the applause '
             'and the risk inseparable from each other. There is real '
             'discipline under the glamour, years of practice compressed '
             'into a single, breathtaking pass around the ring.',
  'colors': 'A planet at this degree often shows genuine skill performed '
            'under visible pressure, talent that gets sharper, not '
            'shakier, in front of an audience. Mars or Venus here can '
            'indicate real comfort with calculated risk taken publicly. '
            'It rewards trusting the years of practice underneath the '
            'show.',
  'reflection': 'What skill have you actually practiced enough to risk '
                'performing it in front of everyone watching?'},
 {'degree': 24,
  'image': 'An untidy, unkempt man sits utterly still, indifferent to how '
           'he looks.',
  'meaning': 'Attention, pulled entirely inward, so completely that '
             'outward appearance simply stops mattering. This degree '
             "offers Leo a real counterweight to its own instinct for "
             'polish and display, a figure whose focus has gone somewhere '
             'so private and absorbing that grooming has become '
             'irrelevant. There is real dignity in this neglect, not '
             'carelessness but priority, everything that matters to him '
             'has moved somewhere the mirror cannot reach.',
  'colors': 'A planet at this degree often shows real capacity to let '
            'outward presentation go entirely in service of something '
            'more important happening inside. Saturn or Neptune here can '
            'indicate someone whose focus is so deeply inward that '
            'appearance stops being a priority at all. It rewards asking '
            'what you would be willing to look like, if the inner work '
            'mattered more than the mirror.',
  'reflection': 'What inward work matters enough to you that you would let '
                'your polish slip entirely for it?'},
 {'degree': 25,
  'image': 'A camel crosses a vast, forbidding desert, carrying its load '
           'steadily on.',
  'meaning': 'Endurance, built for exactly this terrain: the camel is not '
             'struggling against the desert, it is simply built to carry '
             'its load across it, steady and unbothered by conditions '
             "that would defeat almost anything else. Leo's stamina "
             'usually shows itself in a burst, but this degree honors the '
             'longer, quieter version, the capacity to keep moving across '
             'genuinely difficult, unglamorous ground for as long as the '
             'crossing takes.',
  'colors': 'A planet at this degree often shows real endurance across '
            'long, difficult stretches, built specifically for conditions '
            'that would exhaust most approaches. Saturn or Mars here can '
            'indicate steady capacity to keep going through genuinely hard '
            'terrain. It rewards trusting the slow, sustained crossing '
            'over any need for a dramatic sprint.',
  'reflection': 'What desert are you currently built to cross steadily, '
                'even though no one is applauding each individual step?'},
 {'degree': 26,
  'image': 'After a heavy storm, a rainbow arcs whole across the sky.',
  'meaning': 'Promise, made visible immediately after real difficulty: the '
             'rainbow only appears because the storm actually happened, '
             'light and water working together at exactly the right angle '
             'to produce something this brief and this beautiful. '
             "Leo's optimism gets a real image here, not blind cheer, but "
             'color that specifically requires weather to exist at all.',
  'colors': 'A planet at this degree often shows optimism that arrives '
            'specifically after real difficulty, hope earned rather than '
            'assumed. Jupiter or Venus here can indicate genuine talent '
            'for producing something beautiful out of exactly what just '
            'went wrong. It rewards trusting the color that shows up '
            'right after the rain.',
  'reflection': 'What rainbow appeared in your life only because a real '
                'storm passed through first?'},
 {'degree': 27,
  'image': "Dawn's first light spreads low along the eastern sky.",
  'meaning': 'Before sunrise proper, the sky already begins to answer: '
             'this degree is anticipation made visible, the earliest '
             "evidence that the Sun, Leo's own ruler, is on its way even "
             'though it has not yet arrived. There is real faith in '
             'reading a sky this early and trusting what it is about to '
             'become, patience rewarded by a promise rather than the '
             'thing itself yet.',
  'colors': 'A planet at this degree often shows real skill at reading '
            'early signs, trusting a beginning before its full evidence '
            'has actually arrived. The Sun or Mercury here can indicate '
            'someone who senses what is coming well ahead of everyone '
            'else in the room. It rewards trusting the first light, not '
            'just the full sunrise.',
  'reflection': 'What early light have you already noticed, well before '
                'whatever it is announcing has actually arrived?'},
 {'degree': 28,
  'image': 'A flock of small birds crowds together on the limb of one '
           'large tree.',
  'meaning': 'Many small lives, all choosing the same solid branch: no '
             'single bird claims the whole tree, but the limb holds every '
             'one of them at once, individual and communal at the same '
             'time. Leo, so identified with the single spotlighted self, '
             'meets here an image of plenty, many bright small presences '
             'sharing one strong support without any of them needing to '
             'be the only one seen.',
  'colors': 'A planet at this degree often shows real comfort sharing a '
            'platform or spotlight with many others, rather than needing '
            'to be the sole presence on the branch. Jupiter or Venus here '
            'can indicate a genuine gift for community that still lets '
            'individual character show. It rewards trusting that the '
            'branch is strong enough to hold everyone at once.',
  'reflection': 'Who else is sharing your branch right now, and does the '
                'tree actually need you to be its only bird?'},
 {'degree': 29,
  'image': 'A mermaid rises out of the waves, ready to be reborn in human '
           'form.',
  'meaning': 'Transformation, chosen and nearly complete: the mermaid is '
             'caught at the exact moment of becoming something she was '
             'not, water giving way to the possibility of walking upright '
             'in a different world entirely. This degree, so near the '
             "sign's own end, carries real courage, leaving behind an "
             'entire native element for the sake of a new, harder, more '
             'fully embodied kind of life.',
  'colors': 'A planet at this degree often shows genuine willingness to '
            'transform completely, trading a familiar element for a '
            'harder, more fully realized one. Neptune or the Moon here '
            'can indicate someone in real, active process of becoming a '
            'truer version of themselves. It rewards trusting the risk of '
            'walking on legs you have never used before.',
  'reflection': 'What familiar element are you nearly ready to leave, for '
                'the sake of becoming something more fully yourself?'},
 {'degree': 30,
  'image': 'A letter full of private news is folded closed, its envelope '
           'left unsealed.',
  'meaning': 'The final degree of Leo closes on something important, '
             'written and folded, but deliberately left open: trust, '
             'extended right at the edge of privacy, a message that could '
             "easily have been sealed shut but was not. This degree "
             "suggests that Leo's whole performance, thirty degrees of "
             'being seen, ends not with a grand final bow but with '
             'something quieter and more vulnerable, real information, '
             'offered honestly, with nothing hidden behind a sealed flap.',
  'colors': 'A planet at this degree often shows real willingness to leave '
            'something important open and legible rather than protected '
            'behind a formal seal. Mercury or the Moon here can indicate '
            'honesty that chooses transparency over the safety of a '
            'closed envelope. It rewards trusting that what you have '
            'written is actually fine being read.',
  'reflection': 'What have you written, or said, that you are ready to '
                'leave unsealed, trusting whoever reads it with the whole '
                'truth?'},
]

assert len(ENTRIES) == 30, f"expected 30 Leo degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Leo degrees out of order"
