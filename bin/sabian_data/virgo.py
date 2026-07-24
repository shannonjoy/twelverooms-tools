"""Sabian symbol data for Virgo.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (kerykeion.net, astronarrative.com,
jamesburgess.com / Sacred 7 Academy, sabian-calculator.com, Blain Bovee's
Sabian Symbol blog, and Dane Rudhyar's "An Astrological Mandala" wording as
quoted/discussed on mindfire.ca and sabiansymbol.typepad.com) before being
hand-typed. astronarrative.com labels degrees on the "N-1 to N" convention
(e.g. its "3-4" is this file's degree 4); every entry below was checked
across the offset to confirm the same image lands on the same whole
degree in every source. Do NOT extend this list, or write a new sign's
list, without the same verification discipline: fewer verified degrees
beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a portrait
idealizes one figure's most telling feature"), not a verbatim quote of
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
SIGN = {"name": "Virgo", "slug": "virgo", "glyph": "♍︎", "order": 6}

# The 30 degrees of Virgo, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and (only on degree 4) note (str). See SCHEMA.md for
# what each field means.
ENTRIES = [
    {'degree': 1,
     'image': "A portrait draws out and idealizes one figure's single most telling "
              'feature.',
     'meaning': "Virgo opens with an act of selection: not the whole face at once, but "
                'the one detail worth keeping, isolated and given enough light to stand '
                'for everything else. This is discernment as the sign\'s very first '
                'gesture, before craft, before service, before any of the more famous '
                'Virgo virtues get named. A portrait like this does not lie exactly, it '
                'simply decides what mattered most and gives that the emphasis. Aries '
                'began the zodiac by breaking the surface; Virgo, six signs later, '
                'begins by finding the line worth drawing.',
     'colors': 'A planet or point at Virgo 1 tends to know instinctively which detail of '
               'a person, or a situation, actually carries the meaning, and which is '
               'just noise around it. Mercury here favors real skill at editing: a mind '
               'that can throw out the ninety percent that does not matter. On the '
               'Ascendant, it can describe someone the world reads accurately from one '
               'unmistakable trait, rather than needing the whole picture.',
     'reflection': 'What single feature of yourself, if someone drew only that, would '
                   'still say everything that needed saying?'},
    {'degree': 2,
     'image': 'A large white cross stands raised over the land, visible from every '
              'direction.',
     'meaning': "After the private act of the portrait, Virgo's second degree puts "
                'something public and structural on the horizon: a fixed point of '
                'belief, tall enough that the whole landscape has to orient around it '
                'whether it agrees or not. This is commitment made architecture, a '
                'conviction built high enough to become a landmark rather than staying '
                "a private opinion. There is nothing subtle about this degree, and "
                'Virgo, usually so quiet about its convictions, gets one moment of '
                'putting the structure of its faith in plain view.',
     'colors': 'A planet at this degree often shows a belief system, or a code, sturdy '
               'enough to organize an entire life around, visible to everyone even when '
               'never explained. Saturn here favors real structural devotion, a '
               'framework that holds under weight. Neptune or Jupiter can indicate '
               'faith raised high enough to guide others simply by being seen. On the '
               'Midheaven, it can describe a public reputation built on one unmistakable, '
               'unmoving principle.',
     'reflection': 'What have you raised high enough in your own life that everyone '
                   'around you now navigates by it, whether you meant them to or not?'},
    {'degree': 3,
     'image': 'Two guardian figures stand watch, keeping careful protection over someone.',
     'meaning': "Not one guardian but two, which changes the character of the watching: "
                'this is protection thorough enough to cover more than a single angle, '
                "care doubled rather than left to chance. Virgo's instinct to notice "
                'what could go wrong, and quietly prevent it, gets its purest early '
                'picture here, vigilance offered without needing to be asked for or even '
                'seen. There is tenderness under the discipline: guarding someone well '
                'means paying a kind of attention most people never register receiving.',
     'colors': 'A planet at this degree often shows real protective instinct, care '
               'extended before trouble arrives rather than only after. The Moon or '
               'Saturn here can indicate someone who quietly runs interference for '
               'people they love, catching problems upstream. On the fourth or twelfth '
               'house, it favors a home or inner life that has always felt, correctly, '
               'more looked after than it appeared.',
     'reflection': 'Who has been standing guard over you without your ever quite '
                   'noticing, and have you thanked them for the trouble they prevented?'},
    {'degree': 4,
     'image': 'Children of different backgrounds play together, easy and unbothered by '
              'the lines the adults around them draw.',
     'meaning': 'This degree insists on something plain and true underneath every '
                'social division adults invent: kinship that has not yet learned to '
                'sort itself, joy that does not check credentials before joining a '
                'game. Virgo is often mistaken for a sign obsessed with categories and '
                'correct order, but this degree shows the deeper commitment underneath '
                'that reputation, that the actual order beneath all the surface '
                'distinctions is simpler and kinder than the ones people build. Nothing '
                'here needed to be taught; it only needed the adults to step back.',
     'colors': 'A planet at this degree often shows a genuine, uncomplicated ease '
               'crossing lines that others treat as fixed, a real gift for finding '
               'common ground before anyone points out the differences. Venus or '
               'Jupiter here can indicate warmth that includes rather than sorts. On '
               'the eleventh house, it can describe friendships or communities built on '
               'exactly this kind of instinctive, pre-verbal welcome.',
     'reflection': 'What line, drawn by people older or more anxious than you, have you '
                   'never actually felt the need to honor?',
     'note': 'Note: the 1925 original for this degree used dated racial imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 5,
     'image': 'A man becomes quietly aware of nature spirits and other unseen presences '
              'moving around him.',
     'meaning': 'Perception extends here past the edge of what is provable, into a '
                'layer of the world that has always been there and simply was not being '
                "noticed. Virgo's discernment is usually trained on the visible, on what "
                'can be measured and corrected; this degree turns the same close '
                'attention toward what only shows itself to someone quiet and patient '
                'enough to look. It is not fantasy, in the logic of the image, it is '
                'observation finally sensitive enough to register a frequency it had '
                'been missing.',
     'colors': 'A planet at this degree often shows real sensitivity to the subtle layer '
               'of a place or situation, information other people simply do not '
               'register. Neptune or the Moon here can indicate a genuinely porous, '
               'perceptive awareness, sometimes formalized as intuition or craft. It '
               'rewards trusting a kind of noticing that will never fully explain itself '
               'in ordinary language.',
     'reflection': 'What have you been quietly aware of, at the edge of things, that you '
                   'have not yet said out loud because you cannot prove it?'},
    {'degree': 6,
     'image': 'A merry-go-round turns, the same riders circling past the same painted '
              'horses again and again.',
     'meaning': 'Repetition here is not failure to progress, it is a structure built '
                'specifically to be ridden more than once, pleasure designed around the '
                "return rather than despite it. Virgo's relationship to routine gets its "
                'clearest picture in this degree: the value is not in novelty but in '
                'doing the familiar circuit well, noticing what changes slightly each '
                'time even when the horses do not move. A ride like this rewards '
                'attention precisely because nothing about it is urgent.',
     'colors': 'A planet at this degree often shows comfort with structured repetition, '
               'finding real richness in a routine rather than restlessness inside one. '
               'Saturn or Venus here can indicate someone who does their best, most '
               'refined work inside a familiar, repeating form. On the sixth house, it '
               'favors a daily practice that keeps yielding something new from the same '
               'circuit.',
     'reflection': 'What familiar circuit are you still riding, and what have you '
                   'actually noticed on this pass that you missed the last dozen times '
                   'around?'},
    {'degree': 7,
     'image': 'A household is run to look after many people at once, each given her own '
              'formal place within it.',
     'meaning': 'Order applied to abundance: this degree is not really about the number '
                'of people under one roof, it is about the discipline required to give '
                'each one real, individual attention inside a single, shared structure. '
                "Virgo's gift for organizing complexity finds a demanding test here, "
                'since a household this size does not run itself, it runs because '
                'someone is quietly tracking who needs what and when. There is richness '
                'in the image too, resource and relationship both plentiful, provided '
                'the order holding them together stays intact.',
     'colors': 'A planet at this degree often shows a real capacity to tend multiple '
               'significant relationships or responsibilities at once, without letting '
               'any one of them go neglected. Venus or Saturn here can indicate someone '
               'whose care runs wide as well as deep, structured enough to actually '
               "sustain it. It rewards keeping the household's order current rather than "
               'letting any one claim quietly go untended.',
     'reflection': 'Which of your many claims on your attention have you been keeping in '
                   'its proper place, and which one has quietly gone untended?'},
    {'degree': 8,
     'image': "A five-year-old takes her very first formal dancing lesson.",
     'meaning': "Craft begins here at its most literal starting point: a small body, "
                'unpracticed, learning the first positions of a discipline it will '
                "spend years refining. Virgo's whole relationship to skill is contained "
                'in this early picture, that mastery starts exactly this humbly, with a '
                "beginner's stiff, careful steps and a teacher's patient correction. "
                "Nothing about the lesson is glamorous yet; the degree simply insists "
                'that the glamour, later, will have been built on exactly this kind of '
                'unglamorous start.',
     'colors': 'A planet at this degree often shows real respect for foundational '
               'training, technique learned properly and early rather than skipped in '
               'favor of raw talent alone. Mercury or Venus here can favor a lifelong '
               'relationship with craft that began, formally, in childhood. It rewards '
               'returning to fundamentals, especially once skill has grown advanced '
               'enough to start cutting corners.',
     'reflection': 'What first position are you still, quietly, practicing, long after '
                   'everyone assumed you had already mastered it?'},
    {'degree': 9,
     'image': 'An artist sketches in a bold, unconventional style, reaching for a shape '
              'no one has drawn quite this way before.',
     'meaning': "Virgo's reputation is for careful, exacting technique, so it is easy to "
                'miss how much genuine experimentation the sign is actually capable of, '
                'once the craft underneath is solid enough to risk breaking form. This '
                'degree is that risk taken seriously: real skill used not to reproduce '
                'what already exists cleanly, but to chase a shape that has not been '
                'rendered correctly yet by anyone. The result may look rough to an '
                "untrained eye, but the eye that matters here is the artist's own, "
                'already several steps ahead of what the hand has managed to catch up '
                'to.',
     'colors': 'A planet at this degree often shows a genuine appetite for formal '
               'experimentation, technical skill pointed toward something ahead of '
               'current convention rather than behind it. Uranus or Mercury here can '
               'indicate a mind that innovates specifically because the fundamentals '
               'are already so well learned. It rewards trusting a shape that has not '
               'been fully seen yet, rather than smoothing it into something more '
               'familiar too soon.',
     'reflection': 'What are you still sketching in a form no one quite recognizes yet, '
                   'that your own eye can already see clearly?'},
    {'degree': 10,
     'image': 'Two faces look outward, their gaze reaching past the shadows just in '
              'front of them.',
     'meaning': 'This degree asks for vision that refuses to stop at the nearest '
                'obstruction, two vantage points instead of one, doubling the odds that '
                "something real gets seen past whatever is currently blocking the view. "
                "Virgo's discernment usually works close up, sorting fine detail; here "
                'it is asked to work at range instead, looking past the immediate dark '
                'toward whatever is actually out there. Two heads, rather than one, '
                'suggests this kind of seeing is rarely a solitary skill, it improves '
                "with a second, corroborating set of eyes.",
     'colors': 'A planet at this degree often shows real capacity to see past an '
               'immediate obstacle or confusion toward what is actually coming next. '
               'The Moon or Uranus here can indicate perceptiveness that works best in '
               "partnership, one person's blind spot covered by another's clearer "
               'sightline. On the third house, it favors thinking that keeps looking '
               'past the nearest shadow instead of stopping there.',
     'reflection': 'What shadow, directly in front of you, is someone else already '
                   'seeing past, if you let them help you look?'},
    {'degree': 11,
     'image': 'A boy grows into the shape of the hopes his mother once held for him.',
     'meaning': 'Identity, at this degree, arrives partly pre-formed, carried by someone '
                "else's longing before the child had any say in the matter. This is not "
                'necessarily a burden in the image, though it could become one; mostly '
                'it is simply true, that we are shaped early by expectations we did not '
                'choose and only later learn to examine. Virgo, so devoted to refining '
                "the self on purpose, meets here the part of the self that was refined "
                "by someone else's devotion first.",
     'colors': "A planet at this degree often shows a life meaningfully shaped by a "
               "parent's, especially a mother's, hopes, sometimes gratefully fulfilled, "
               'sometimes still being sorted out from one\'s own actual wishes. The Moon '
               'or Saturn here can indicate real tenderness, or real tension, around '
               'inherited expectation. It rewards taking an honest inventory of which '
               'hopes are still yours to carry, and which were only ever borrowed.',
     'reflection': 'Which of your current ambitions did you choose yourself, and which '
                   'one were you simply, lovingly, handed?'},
    {'degree': 12,
     'image': "Just after the ceremony, the bride's veil is lifted away at last.",
     'meaning': 'Ritual concealment has a built-in expiration, and this degree is the '
                'moment it runs out: whatever the veil was protecting or postponing is '
                'now, finally, in full view. There is nothing gentle required about the '
                'gesture, it happens decisively, the way a truth arrives once its '
                'proper occasion has been reached rather than dragged out any further. '
                'Virgo values discretion, but this degree reminds the sign that '
                'discretion is only ever a phase, not a permanent state, meant to end '
                'at exactly the right moment.',
     'colors': 'A planet at this degree often shows something concealed for good reason '
               'finally being revealed at precisely the right, socially sanctioned '
               'moment. Mars or Venus here can indicate a decisive unveiling, in love '
               'or otherwise, timed rather than delayed indefinitely. On the seventh '
               'house, it favors a relationship reaching the point where its full '
               'reality finally gets to be seen.',
     'reflection': 'What have you been keeping veiled well past the ceremony that was '
                   'actually supposed to end that concealment?'},
    {'degree': 13,
     'image': 'A steady, capable leader calms a crowd that has worked itself into '
              'panic.',
     'meaning': 'Public fear, met by someone whose composure has not caught the same '
                'contagion: this degree is authority earning its keep exactly when it '
                'matters most, not in ordinary times but in the moment a room, or a '
                "country, has genuinely lost its head. Virgo's calm under pressure is "
                'not passive here, it is actively steadying, applied on purpose to a '
                'situation that badly needs it. The strength in the image is less about '
                'force than about simply not panicking when everyone around you already '
                'has.',
     'colors': 'A planet at this degree often shows genuine steadiness in a crisis, the '
               'rare capacity to stay clear-headed exactly when a group most needs '
               'someone to be. Saturn or the Sun here can indicate real, tested '
               'leadership under real pressure, not just confidence in calm '
               'conditions. It rewards being the one who does not join the panic, even '
               'when joining it would be easier.',
     'reflection': 'Where is a version of you needed right now, specifically because '
                   'everyone else in the room has already lost their composure?'},
    {'degree': 14,
     'image': 'A family tree spreads across the page, branch after branch of names.',
     'meaning': 'Lineage, laid out and made legible: every branch on this tree required '
                'someone to trace it, prune the confusion out of it, and set it down in '
                "an order that can actually be read. Virgo's talent for organizing "
                'complexity into clear, usable form gets applied here to something as '
                'tangled as inheritance itself, turning a mess of names and relations '
                'into a structure anyone in the family can actually follow. There is '
                'devotion in the labor, not just record-keeping, since a tree this '
                'carefully drawn is really an act of care for everyone who comes after.',
     'colors': 'A planet at this degree often shows real interest in lineage, '
               'inheritance, and the patterns that repeat across a family line, along '
               'with a genuine skill for making that pattern legible. Saturn here can '
               'indicate someone who takes family history and its structure seriously '
               'enough to actually document it. On the fourth house, it favors a '
               "strong, well-understood sense of where one's own branch fits on the "
               'larger tree.',
     'reflection': 'What branch of your own family tree have you never actually traced, '
                   'that might explain more about you than you realize?'},
    {'degree': 15,
     'image': 'A piece of fine lace, made purely for beauty, is worked into a delicate '
              'handkerchief.',
     'meaning': "Halfway through the sign, Virgo produces its purest object: something "
                'entirely functional in theory, a handkerchief, made so exquisitely '
                'that its actual use becomes almost beside the point. This degree '
                'honors craft carried past necessity into devotion, hours of fine, '
                'patient work invested in something small enough to disappear into a '
                'pocket. There is real philosophy in the image: usefulness and beauty '
                'are not actually in competition, and the most ordinary object can '
                'become the site of the most careful attention a maker has.',
     'colors': 'A planet at this degree often shows a gift for elevating something small '
               'and practical into something genuinely beautiful, care applied at a '
               'scale most people would consider too minor to bother with. Venus here '
               'is especially at home, favoring fine, exacting handwork. It rewards '
               'remembering that the smallest objects in a life often carry the largest '
               'amount of love actually put into them.',
     'reflection': 'What small, ordinary object in your life has, quietly, the most '
                   'careful attention ever put into it?'},
    {'degree': 16,
     'image': 'Children at the zoo come face to face with an orangutan, watching each '
              'other across the glass.',
     'meaning': 'Civilized curiosity meets something wilder and older, close enough to '
                'really look at, safe enough not to have to look away. This degree is a '
                'controlled encounter with instinct, the part of nature that has not '
                'been domesticated, met without danger but also without pretending the '
                'difference is not real. Virgo, so oriented toward order and '
                'refinement, gets a useful reminder here: the wild version of a thing '
                'is still worth studying directly, not just managing from a distance.',
     'colors': 'A planet at this degree often shows real fascination with instinct and '
               'the more primal layer of behavior, in oneself or others, approached '
               'with genuine curiosity rather than only discomfort. Mars or Pluto here '
               'can indicate someone drawn to study what is unrefined rather than '
               'avoid it. On the twelfth house, it favors real insight gained by '
               'looking directly at what usually stays behind glass.',
     'reflection': 'What wilder, less domesticated part of yourself have you been '
                   'watching from a safe distance, that might be worth a closer look?'},
    {'degree': 17,
     'image': 'A volcano erupts, releasing pressure that had been building far beneath '
              'the surface.',
     'meaning': 'Everything Virgo usually keeps composed and contained finds its '
                'counterweight here: force that was never actually gone, only stored, '
                'breaking through with more power for having waited. This degree is a '
                'genuine warning against mistaking quiet for absence, since what looks '
                'like calm ground can be sitting directly on top of real heat. There is '
                'something almost cleansing in the eruption too, pressure this old does '
                'not want to be managed forever, it wants an actual release.',
     'colors': 'A planet at this degree often shows real intensity held under a composed '
               'exterior, capable of sudden, dramatic release once enough has built up '
               'underneath. Pluto or Mars here can indicate emotion or force that has '
               'been quietly accumulating far longer than it appears. It rewards '
               'finding a release valve before the pressure decides to find its own.',
     'reflection': 'What has been building underneath your composure for far longer '
                   'than anyone watching you would guess?'},
    {'degree': 18,
     'image': 'A small group gathers around a board, waiting to see what an unseen hand '
              'will spell out.',
     'meaning': 'Structure gets applied here to something that resists proof entirely, '
                'a formal method for asking questions of whatever cannot simply be '
                'interrogated directly. Virgo likes a system, a set of rules, a '
                'repeatable procedure, and this degree hands the sign exactly that in '
                'service of the least provable subject there is. The image carries real '
                'caution along with its curiosity: a method this open to suggestion '
                'needs a steady, skeptical hand on it, or the answer says more about '
                'the asker than about anything actually beyond them.',
     'colors': 'A planet at this degree often shows an interest in structured ways of '
               'approaching the unknown, divination, research into the unproven, '
               'formal method applied to mystery. Neptune or Mercury here can indicate '
               'real sensitivity to messages that arrive through indirect or ambiguous '
               'channels. It rewards keeping a clear, discerning mind at the table, '
               'especially when the answer is the one you were already hoping for.',
     'reflection': 'What question have you been asking an unseen hand, that you could '
                   'actually just ask yourself directly?'},
    {'degree': 19,
     'image': 'Swimmers race side by side, each one measured against the water and the '
              'clock.',
     'meaning': 'Competition here is stripped down to something almost entirely '
                'private: no opponent to outmaneuver, only your own effort against a '
                "measurable, indifferent element. Virgo's relationship to discipline is "
                'exactly this kind, self-improvement tracked in real numbers, progress '
                'that either shows up on the clock or it does not. There is real '
                'humility built into a race like this, since water does not care about '
                'excuses, and neither does time.',
     'colors': 'A planet at this degree often shows genuine discipline around '
               'self-measured improvement, training tracked honestly against a '
               'standard rather than only against other people. Mars or Saturn here '
               'can indicate real commitment to getting measurably better at something '
               'over time. On the sixth house, it favors a fitness or work practice '
               'built around honest, ongoing self-comparison.',
     'reflection': 'What are you currently measuring yourself against, honestly, rather '
                   'than comparing yourself to everyone else in the next lane?'},
    {'degree': 20,
     'image': 'A group of children rides together to the same destination, ferried by a '
              'rotation of parents taking their turn.',
     'meaning': 'Care, here, gets distributed rather than carried by one person alone: '
                'the same daily task, shared out across several willing drivers so '
                'that no single household bears the whole weight of it. '
                "Virgo's gift for logistics finds one of its warmest expressions in "
                'this degree, ordinary service organized so well that it becomes, '
                'almost invisibly, a form of community. Nobody in the image is doing '
                'anything heroic, and that is exactly the point, reliable, shared, '
                'unglamorous care is its own kind of strength.',
     'colors': 'A planet at this degree often shows real skill at organizing shared '
               'responsibility, splitting an ongoing task so it stays sustainable for '
               'everyone involved rather than exhausting one person. Mercury or the '
               'Moon here can indicate a genuine talent for cooperative logistics, '
               'especially around children or daily routine. It rewards trusting the '
               'rotation instead of quietly trying to drive every leg of it yourself.',
     'reflection': 'What task have you been carrying alone, that would actually work '
                   'better shared out across a rotation of willing hands?'},
    {'degree': 21,
     'image': "A girls' basketball team runs a coordinated play, each player moving "
              'exactly where the pattern needs her.',
     'meaning': 'Individual skill only matters here in service of shared timing: a team '
                'like this wins not because any one player is unstoppable alone, but '
                'because everyone has learned precisely where to be when the ball '
                "arrives. Virgo's discipline usually looks solitary, but this degree "
                'insists the same precision can be built collectively, five separate '
                'practices converging into one moving structure. There is real joy in '
                'the coordination too, the pleasure of a pattern executed cleanly by '
                "people who trust each other's timing completely.",
     'colors': 'A planet at this degree often shows real ease contributing individual '
               'skill to a tightly coordinated group effort, timing that depends on '
               'trusting others as much as trusting oneself. Mars or Jupiter here can '
               'indicate a genuine talent for team dynamics, especially in structured '
               'competition. On the eleventh house, it favors belonging to a group '
               'whose shared discipline outperforms any single member alone.',
     'reflection': "What pattern are you currently part of, where trusting someone "
                   "else's timing matters as much as trusting your own?"},
    {'degree': 22,
     'image': 'A royal coat of arms hangs on display, its surface set with precious '
              'stones.',
     'meaning': 'Ordinary heraldry gets elevated here past mere symbol into something '
                'genuinely valuable in its own right, meaning and material worth fused '
                'into a single object. This degree suggests that service, done at a '
                'high enough level for long enough, eventually earns exactly this kind '
                'of recognition: not just an emblem, but one worth something on its own '
                "terms. Virgo's humility about its own work meets, in this degree, the "
                'moment that work has actually accumulated enough weight to be honored '
                'openly.',
     'colors': 'A planet at this degree often shows recognition or status earned '
               'through long, careful service rather than claimed prematurely, worth '
               'that has genuinely accumulated rather than only been announced. '
               'Jupiter or Venus here can indicate real, well-deserved honor arriving '
               'eventually. On the Midheaven, it favors a reputation built slowly '
               'enough that, once achieved, it is entirely secure.',
     'reflection': 'What careful, long service of yours is finally worth putting some '
                   'actual jewels on, instead of downplaying it any further?'},
    {'degree': 23,
     'image': 'An animal trainer works with a full-grown lion, holding its attention '
              'through precise, practiced skill.',
     'meaning': 'Discipline gets tested here against something genuinely capable of '
                'doing real damage, and the safety in the room exists entirely because '
                "of technique, not because the danger has been removed. Virgo's craft "
                'is often applied to gentle, low-stakes material; this degree raises '
                'the stakes considerably, asking whether the same precision holds up '
                'when the margin for error actually matters. Real courage in the image '
                'is quiet, mostly invisible, expressed as competence rather than as '
                'bravado.',
     'colors': 'A planet at this degree often shows genuine composure and skill applied '
               'to something authentically dangerous or volatile, control that comes '
               'from technique rather than dominance. Mars, Saturn, or Pluto here can '
               'indicate real capacity to hold a high-stakes situation steady through '
               'sheer, practiced precision. It rewards trusting the training in exactly '
               'the moment it is most tempting to panic instead.',
     'reflection': 'What genuinely high-stakes situation are you currently holding '
                   'steady, through skill rather than through luck?'},
    {'degree': 24,
     'image': 'A shepherd tends a single small lamb, gentle and completely attentive to '
              'it.',
     'meaning': 'Devotion narrows all the way down here, to one small, dependent '
                'creature and the person who has made its care their whole focus. This '
                "is Virgo's service reduced to its simplest possible form, no "
                'institution, no audience, just consistent attention given to '
                'something that genuinely could not manage without it. There is '
                'nothing complicated about the image, and that is the entire lesson: '
                'sometimes the most meaningful service is the smallest, most singular '
                'one.',
     'colors': 'A planet at this degree often shows real devotion to one particular '
               'person, creature, or cause, attention given completely rather than '
               'divided across many claims. The Moon or Venus here can indicate a '
               'caretaking instinct that is happiest focused narrowly rather than '
               'spread wide. On the sixth house, it favors work or care built around '
               'genuine, undivided attentiveness to what depends on you.',
     'reflection': 'What single, small charge in your life deserves your full, '
                   'undivided attention right now, instead of a share of it?'},
    {'degree': 25,
     'image': 'A flag flies at half-mast in front of a large public building.',
     'meaning': 'Grief, here, gets acknowledged formally, in public, by an institution '
                'that keeps functioning even as it marks the loss. This degree is '
                'mourning integrated into ordinary structure rather than set apart from '
                'it: the building does not close, the flag simply flies lower, and '
                'everyone passing by understands exactly what that means without a '
                "word needing to be said. Virgo's respect for correct form finds one of "
                'its most moving expressions here, ritual precise enough to hold real '
                'feeling without collapsing under it.',
     'colors': 'A planet at this degree often shows real capacity to honor loss through '
               'proper, visible form, grief expressed correctly rather than either '
               'suppressed or theatrically overdone. Saturn or the Moon here can '
               'indicate someone who instinctively knows the right, dignified gesture '
               'for a hard moment. On the tenth house, it favors a public role that '
               'includes, gracefully, the responsibility of marking loss for others.',
     'reflection': 'What loss in your life still deserves its flag lowered properly, '
                   'rather than quietly taken down without ceremony?'},
    {'degree': 26,
     'image': 'A boy carries the incense at the altar, moving carefully through his '
              'small part of the larger ceremony.',
     'meaning': 'The sacred, here, depends on someone very young getting a very '
                'specific, very small job exactly right: the whole ritual around him is '
                'large and old, and his role in it is modest, precise, and essential '
                'anyway. Virgo finds one of its most direct expressions of faith in '
                'this degree, service to something greater than yourself, carried out '
                'through careful attention to the smallest assigned task rather than '
                'through any grand gesture. There is real dignity in being trusted with '
                'the little part.',
     'colors': 'A planet at this degree often shows genuine devotion expressed through '
               'small, precise, faithfully repeated duties within a larger structure or '
               'tradition. Mercury or Saturn here can indicate someone who takes their '
               'modest role in something bigger seriously enough to do it exactly '
               'right, every time. It rewards trusting that the small task, done with '
               'real attention, is itself a form of the sacred.',
     'reflection': 'What small, precise task have you been given inside something '
                   'larger than yourself, that deserves your full attention rather than '
                   'your impatience to do something bigger?'},
    {'degree': 27,
     'image': 'A group of formally dressed women meets for tea, observing every rule of '
              'the occasion.',
     'meaning': 'Ceremony, here, is the whole content of the gathering: what gets said '
                'matters less than the fact that every gesture, every cup lifted at the '
                'right moment, is performed correctly according to a shared, unspoken '
                "code. Virgo's respect for exact form reaches its most social "
                'expression in this degree, manners as a kind of craft, precision '
                'applied not to an object but to an occasion. There is real skill in '
                'doing this well, and real belonging offered to whoever can perform it '
                'fluently.',
     'colors': 'A planet at this degree often shows genuine fluency in social ritual and '
               'correct form, comfort with occasions that run on precise, agreed-upon '
               'etiquette. Venus or Saturn here can indicate someone who moves easily '
               'through formal social structure, at home in its exact rules. On the '
               'eleventh house, it favors belonging to a circle where form itself is '
               'part of the welcome.',
     'reflection': 'What formal occasion in your life have you been performing '
                   'correctly, and what would it actually mean to you if someone '
                   'finally saw through the form to what you meant underneath it?'},
    {'degree': 28,
     'image': 'A man with a shaved, unadorned head has just taken hold of real power.',
     'meaning': 'Nothing here is ornamented, and that is the point: authority arrives '
                'stripped down to its plainest possible appearance, no crown, no '
                'elaborate signal, just the fact of the power itself, freshly seized. '
                "Virgo's usual instinct is toward refinement and decoration done "
                'carefully; this degree instead rewards a kind of authority that needs '
                'no adornment to be recognized as real. There is something almost '
                'startling in how little display the moment actually requires.',
     'colors': 'A planet at this degree often shows real, unadorned authority, power '
               'that does not need embellishment to be taken seriously once it has '
               'actually been claimed. Mars, Pluto, or Saturn here can indicate someone '
               'whose command comes from substance rather than presentation. It rewards '
               'trusting that the plainest version of your authority may already be the '
               'most convincing one.',
     'reflection': 'Where have you been dressing up an authority that would actually be '
                   'more convincing left plain?'},
    {'degree': 29,
     'image': 'A student sits alone with an old scroll, gaining knowledge meant to stay '
              'hidden from most people.',
     'meaning': 'Study, here, happens in private, and the knowledge involved is not the '
                'kind handed out freely, it has to be sought, sat with, and earned '
                "through the reading itself. Virgo's discipline turns inward at this "
                'next-to-last degree, toward the kind of learning that cannot be '
                'rushed or crowdsourced, only slowly extracted from an old, difficult '
                'source by someone patient enough to actually sit with it. There is '
                'real solitude in the image, and real reward for tolerating it.',
     'colors': 'A planet at this degree often shows a genuine capacity for solitary, '
               'deep research, especially into material most people never bother to '
               'access directly. Mercury, Neptune, or Pluto here can indicate real '
               'aptitude for study that requires real patience with old or difficult '
               'sources. It rewards trusting the slow extraction over any faster, '
               'secondhand version of the same knowledge.',
     'reflection': 'What old, difficult source have you been meaning to sit with '
                   'directly, instead of settling for what other people say it '
                   'contains?'},
    {'degree': 30,
     'image': 'Fully absorbed in an urgent task, someone does not even register the '
              'distraction calling for their attention.',
     'meaning': 'The final degree of Virgo closes the sign on its purest possible '
                'expression: total, undivided attention given entirely to the work in '
                'front of you, so complete that anything else trying to pull focus '
                'simply does not register at all. Every earlier degree in this sign, '
                'the craft, the discernment, the small precise service, arrives here '
                'at its natural conclusion, absorption so total it functions as its '
                'own kind of peace. Nothing about this final image is frantic; it is '
                'simply finished, entirely present, undistractable.',
     'colors': 'A planet at this degree often shows a genuine capacity for total focus '
               'once real work is underway, distraction that simply fails to land '
               'because the attention is already completely spoken for. Mars or Saturn '
               'here can indicate someone whose concentration, once engaged, is '
               'essentially unbreakable. It rewards protecting that state rather than '
               'apologizing for how completely it shuts out everything else.',
     'reflection': 'What task, right now, deserves the kind of attention that would '
                   'make everything else simply fail to reach you?'},
]

assert len(ENTRIES) == 30, f"expected 30 Virgo degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Virgo degrees out of order"
