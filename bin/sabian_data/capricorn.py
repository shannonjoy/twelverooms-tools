"""Sabian symbol data for Capricorn.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (kerykeion.net,
astronarrative.com, jamesburgess.com / Sacred 7 Academy,
sabian-calculator.com, and, for the two degrees carrying dated ethnic
imagery plus the tea-leaves degree, additional confirmation via
sabiansymbologist.wordpress.com, saijin.wordpress.com,
judithdehaan.substack.com, boveeastrology.com, and astromatrix.org)
before being hand-typed. All 30 degrees agreed across every source
checked, with no unresolved conflicts. Do NOT extend this list, or write
a new sign's list, without the same verification discipline: fewer
verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "an angel
carrying a harp"), not a verbatim quote of Marc Edmund Jones' 1953 book
or Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation,
written fresh for this project; none of it is copied from Jones or
Rudhyar.

DATED IMAGERY: Capricorn 1's 1925 original names a stereotyped "Indian
chief" figure, and Capricorn 5's names stereotyped "Indians" performing
a war dance. Per Shannon's standing policy, the canonical mapping is
kept for both, but `image` restates each respectfully without the
ethnic label, and a `note` field is attached below each symbol card. See
SCHEMA.md for the full policy. (Capricorn 29's original title, "A Woman
Reading Tea Leaves," was separately checked for a variant "gypsy tea
room" phrasing sometimes seen in secondary write-ups; the canonical
Jones/Wheeler title carries no such term, so no note is attached there,
and the word does not appear in this file's restatement either way.)
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Capricorn", "slug": "capricorn", "glyph": "♑︎", "order": 10}

# The 30 degrees of Capricorn, in order 1-30. Each entry is a dict with
# the fields: degree (int 1-30), image (str), meaning (str), colors
# (str), reflection (str), and an optional note (str) on the two degrees
# whose 1925 originals used dated ethnic imagery. See SCHEMA.md for what
# each field means.
ENTRIES = [
    {'degree': 1,
     'image': 'A tribal leader stands before the assembled council, coldly and regally '
              'demanding recognition.',
     'meaning': 'Capricorn opens the sign the way it opens every ambition it will ever '
                'have: with an unapologetic claim. There is no warm-up here, no '
                'introduction, only a leader walking in front of the whole gathered '
                'group and stating, plainly, what is owed. Cardinal Capricorn asserts '
                'at the very first degree that authority is not requested, it is '
                'claimed, and the claiming itself is the first real act of rule. The '
                'coldness in the picture is deliberate: recognition sought this early '
                'cannot yet lean on rapport, it has to stand on the bare fact of '
                'capability alone.',
     'colors': 'A planet at Capricorn 1 tends to walk into a room already expecting to '
               'be taken seriously, ahead of any relationship built to earn that '
               'expectation. Saturn here often shows authority claimed early and then '
               'spent a lifetime justifying. The Sun at this degree can indicate '
               "someone whose presence itself functions as an announcement: attention "
               'now, credentials to follow.',
     'reflection': 'What have you already claimed out loud, before the room had fully '
                   "earned its way to believing you?",
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 2,
     'image': 'Three stained-glass windows glow in an old cathedral; the light through '
              'the center one has been broken by war.',
     'meaning': 'Two windows still cast their old colored light and the third stands '
                'damaged, proof that even the most carefully built structures take '
                'real hits and keep standing anyway. This second degree is about '
                'durability under damage: not everything that gets built survives '
                'whole, and Capricorn\'s task is keeping the building consecrated even '
                'with one window cracked. Nothing here is a picture of ruin, it is a '
                'picture of a structure absorbing a wound and remaining a cathedral '
                'regardless.',
     'colors': 'A planet at this degree often shows an institution, a family, or a body '
               'of work that has taken a real hit and kept functioning, scarred rather '
               'than destroyed. Saturn here can indicate resilience proven by damage '
               'survived, not merely claimed in advance. On the fourth house, it '
               'favors a foundation that stayed structurally sound through something '
               'that genuinely could have brought it down.',
     'reflection': 'Which window in your own cathedral got broken, and have you '
                   'actually let the light back in through it, cracked as it still is?'},
    {'degree': 3,
     'image': 'A soul, eager for new experience, reaches to take on a body and grow.',
     'meaning': 'Before Capricorn builds anything external, it names the hunger '
                'underneath all the building: a soul that wants, plainly and '
                'legitimately, to grow through actual lived experience rather than '
                'theory. This degree is appetite honored before the sign\'s famous '
                'restraint arrives to shape it, avidity given its due on its own '
                'terms. Capricorn is so often read as pure control that it is easy to '
                'forget it started, at degree three, exactly as hungry as every other '
                'sign.',
     'colors': 'A planet at this degree often shows real hunger for embodied '
               'experience, growth that wants to be lived rather than only studied '
               'from a safe distance. Jupiter or the Moon here can indicate an appetite '
               'for direct participation in life that outruns caution. It rewards '
               'trusting the eagerness itself as legitimate fuel, not something to '
               'immediately discipline out of yourself.',
     'reflection': 'What new experience is your soul actually reaching for right now, '
                   'underneath whatever restraint you have already applied to it?'},
    {'degree': 4,
     'image': 'Supplies get loaded into a large canoe as a group readies itself for a '
              'crossing by water.',
     'meaning': 'Preparation, done thoroughly, before a single paddle stroke: this '
                'degree honors the unglamorous labor of outfitting, checking supplies, '
                'making sure the vessel can actually hold everyone who intends to '
                'travel in it. Capricorn\'s discipline shows up here as logistics, the '
                'real work that happens before any journey looks impressive to an '
                'onlooker. Loading a canoe is not dramatic, and that is exactly the '
                'point: the drama of the crossing depends entirely on how well this '
                'quiet stage got done.',
     'colors': 'A planet at this degree often shows real competence at preparation, the '
               'unglamorous groundwork that makes a later journey or venture actually '
               'survivable. Saturn or Mercury here can indicate someone trusted '
               'specifically to get the outfitting right before anyone else boards. It '
               'rewards taking the loading as seriously as the voyage itself.',
     'reflection': 'What are you currently, carefully loading into the canoe, ahead of '
                   'a journey everyone else is still only imagining the arrival of?'},
    {'degree': 5,
     'image': 'A crew rows a loaded canoe hard toward battle, while others aboard dance '
              'a war dance.',
     'meaning': 'Physical labor and spiritual preparation happen in the same boat at '
                'the same time: some hands pull the paddles while other bodies dance '
                'the dance that readies the mind for what is coming. Capricorn '
                'mobilizes exactly like this, the practical and the ceremonial working '
                'side by side rather than in sequence, both necessary before the '
                'actual conflict arrives. This degree insists that getting ready is '
                'not only logistics, it is also, just as seriously, working the nerve '
                'up.',
     'colors': 'A planet at this degree often shows real capacity to mobilize on two '
               'fronts at once, doing the practical work while also, deliberately, '
               'building the resolve to see it through. Mars here is especially at '
               'home, favoring aggressive, coordinated leadership toward a shared, '
               'high-stakes goal. It rewards trusting that the dance is not a '
               'distraction from the rowing, it is part of the same preparation.',
     'reflection': 'What are you currently rowing toward, and what dance are you doing '
                   'alongside the rowing to actually be ready when you arrive?',
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 6,
     'image': 'Ten logs lie stacked beneath a dark archway that opens onto darker '
              'woods.',
     'meaning': 'Raw material, gathered and ready, sitting right at the threshold of '
                'something considerably less lit. This degree pairs resource with '
                'warning: the logs are useful, real, countable, and they are '
                "positioned exactly where the path gets harder to see. Capricorn's "
                'respect for what is tangible meets, here, a genuine caution about '
                'what lies past the visible edge of the stockpile. Ten is a full, '
                'round number: enough to build with, not enough to pretend the dark '
                'ahead does not matter.',
     'colors': 'A planet at this degree often shows real resources gathered and ready, '
               'positioned right at the edge of something that will require more '
               'courage than accounting to enter. Saturn or Pluto here can indicate '
               'material readiness for a genuinely difficult passage still ahead. It '
               'rewards counting what you have honestly before stepping into the part '
               'of the woods you cannot yet see.',
     'reflection': 'What have you already stacked and readied, right at the edge of a '
                   'darker stretch you have not yet actually entered?'},
    {'degree': 7,
     'image': 'A veiled prophet speaks, seized by the power of a god moving through '
              'them.',
     'meaning': 'The voice here is not entirely the speaker\'s own; something larger '
                'has taken hold and is using the prophet as its instrument, the veil '
                'marking the difference between the ordinary person and the office '
                'they are, in this moment, channeling. Capricorn understands authority '
                'as something that can be inhabited as well as personal, a role '
                'stepped into that is bigger than the individual wearing it. There is '
                'real submission in the image alongside the power: to speak with this '
                'kind of force, the prophet has had to get out of the way of the '
                'message.',
     'colors': 'A planet at this degree often shows real capacity to speak or act with '
               'an authority that feels larger than personal opinion, channeling '
               'something the speaker did not simply invent. Neptune or Jupiter here '
               'can indicate genuine spiritual or visionary conviction delivered with '
               'real force. On the Midheaven, it favors a public role experienced as a '
               'calling rather than a preference.',
     'reflection': 'What have you said recently that felt like it was coming through '
                   'you, more than simply from you?'},
    {'degree': 8,
     'image': 'In a sunlit house, tame birds sing without any apparent reason to hold '
              'back.',
     'meaning': 'Nothing here is performing for an audience; the birds sing because the '
                'house is warm and they are safe in it, joy with no occasion required '
                'beyond the ordinary comfort of home. Capricorn, so associated with '
                'effort and climb, gets a rare picture of achievement already arrived, '
                'contentment that does not need to be earned again today. This is the '
                "reward sitting quietly inside the domestic structure the sign spends "
                'so much of its energy building.',
     'colors': 'A planet at this degree often shows real, uncomplicated contentment '
               'inside a well-built domestic life, joy that does not require an '
               'external occasion to justify itself. Venus or the Moon here can '
               'indicate a home genuinely warm enough that everyone in it, without '
               'prompting, is glad to be there. On the fourth house, it favors a '
               'household whose comfort was actually built, not simply inherited by '
               'luck.',
     'reflection': 'What in your own house is singing right now, simply because the '
                   'conditions you built for it are finally good enough?'},
    {'degree': 9,
     'image': 'An angel stands holding a harp, its strings waiting quietly under '
              'ready fingers.',
     'meaning': 'Beauty and message travel together here, an instrument in the hands '
                'of a messenger, sound as the actual form the communication is about '
                "to take. Capricorn's structure meets something genuinely celestial in "
                'this degree, proof that discipline and devotion, carried far enough, '
                'can produce something as light and as moving as music. The harp is '
                'not decoration in this image, it is the point: whatever the angel has '
                'to say, it says by playing.',
     'colors': 'A planet at this degree often shows real capacity to deliver something '
               'meaningful through beauty itself, message and craft fused rather than '
               'kept separate. Venus or Neptune here can indicate a genuinely inspired '
               'gift for making difficult truths land gently, through art rather than '
               'argument. It rewards trusting the instrument as much as the message it '
               'is carrying.',
     'reflection': 'What have you been trying to say, that might actually land better '
                   'played than spoken?'},
    {'degree': 10,
     'image': 'A great seabird glides in close and feeds directly from a sailor\'s '
              'outstretched hand.',
     'meaning': 'A wild creature, one built for open ocean and enormous distance, comes '
                'close enough to be fed directly, trust extended across a real gap '
                'between two very different kinds of life. This degree honors the '
                'moment discipline and patience actually earn something wilder than '
                'Capricorn usually keeps close: not a tamed bird, a wild one that has '
                'simply decided to trust this particular hand. There is real '
                'achievement in this, since the bird does not need the sailor, it is '
                'choosing the encounter.',
     'colors': 'A planet at this degree often shows an ability to earn the trust of '
               'something, or someone, that does not actually need to be tamed, only '
               'convinced. Jupiter or Venus here can indicate real luck or grace that '
               'arrives specifically because something wild chose to draw near. It '
               'rewards remembering that trust like this is a gift, not a possession.',
     'reflection': 'What wild, independent part of your life has recently decided, on '
                   'its own terms, to come close enough to eat from your hand?'},
    {'degree': 11,
     'image': 'A large flock of pheasants gathers across a private, carefully kept '
              'estate.',
     'meaning': 'Abundance here is deliberately managed, a landscape maintained '
                'specifically so that this much plenty can actually thrive in it. '
                "Capricorn's relationship to wealth shows itself plainly in this "
                'degree: it is not an accident, it is the result of real, ongoing '
                'stewardship, ground kept in exactly the condition that lets a flock '
                'this size flourish. The birds did not simply appear, the estate was '
                'built to hold them.',
     'colors': 'A planet at this degree often shows real capacity to build and '
               'maintain conditions where abundance can actually gather and stay, '
               'rather than pass through and leave. Jupiter or Saturn here can '
               'indicate wealth or resource that is well-tended, not merely '
               'accumulated. It rewards asking whether your own ground is actually '
               'kept well enough to hold what you hope will gather there.',
     'reflection': 'What have you been quietly maintaining, well enough and long '
                   'enough, that abundance has actually started to settle into it?'},
    {'degree': 12,
     'image': 'A lecturer illustrates a talk on natural science, showing the room '
              'something about life it did not already know.',
     'meaning': 'Structure applied to raw observation produces, here, real revelation: '
                'the lecturer has taken the wildness of the natural world and '
                'organized it into something a room full of people can actually learn '
                "from in a single sitting. Capricorn's discipline turns toward "
                'teaching in this degree, proof that mastery is not complete until it '
                'has been made transmissible to someone else. The illustration matters '
                'as much as the lecture, since insight this real deserves to be '
                'shown, not only described.',
     'colors': 'A planet at this degree often shows a genuine gift for making complex, '
               'natural material legible to others, teaching built on real expertise '
               'rather than borrowed talking points. Mercury or Jupiter here can '
               'indicate someone whose authority comes specifically from having done '
               'the observation themselves. It rewards illustrating what you know, not '
               'just asserting it.',
     'reflection': 'What do you actually understand well enough right now to teach it '
                   'to a room, with real evidence, rather than just describe it?'},
    {'degree': 13,
     'image': 'A fire worshipper sits in meditation on the deepest realities of '
              'existence.',
     'meaning': 'Devotion here is aimed at the largest possible questions, not the '
                'daily ones: the worshipper has turned toward fire, an old and '
                'elemental object of attention, specifically to sit with what is '
                "ultimate rather than what is urgent. Capricorn's seriousness finds "
                'one of its purest expressions in this degree, discipline pointed not '
                'at achievement but at genuine metaphysical inquiry. There is real '
                'patience required here, since ultimate realities do not resolve on '
                'any practical schedule.',
     'colors': 'A planet at this degree often shows a genuine pull toward the largest '
               'questions, meditation or inquiry that is not interested in quick '
               'answers. Neptune or Pluto here can indicate real depth of '
               'contemplative practice, seriousness applied to existence itself rather '
               'than only to career or structure. It rewards protecting time for '
               'exactly this kind of unhurried, elemental attention.',
     'reflection': 'What ultimate question have you been sitting with lately, without '
                   'rushing yourself toward a tidy answer?'},
    {'degree': 14,
     'image': 'An old bas-relief, carved in stone, still stands as evidence of a '
              'culture long since gone.',
     'meaning': 'What outlasts a civilization, this degree suggests, is often the '
                'object made with the most care, stone patient enough to survive '
                'everything that surrounded it when it was made. Capricorn\'s '
                'relationship to time is entirely at home here: build carefully '
                'enough, in durable enough material, and the work itself becomes the '
                'witness long after every other record of the era has vanished. There '
                'is real gravity in the image, and real hope too, since something did '
                'survive.',
     'colors': 'A planet at this degree often shows work built specifically to last '
               'past its own era, made durable on purpose rather than for immediate '
               'use. Saturn here is especially at home, favoring legacy achieved '
               'through material seriousness. On the tenth house, it favors a body of '
               'work meant to outlive the career that produced it.',
     'reflection': 'What are you currently carving carefully enough that it might '
                   'still be legible long after everything around it has worn away?'},
    {'degree': 15,
     'image': 'A children\'s hospital ward is stocked full of toys.',
     'meaning': 'The exact midpoint of Capricorn softens its usual seriousness into '
                'something tender: even in the hardest setting, room has been made for '
                'play, and made generously. This degree insists that structure and '
                'mastery are not the whole story, that real care includes providing '
                'joy specifically where it is least expected and most needed. '
                'Capricorn spends so much of its energy on discipline that this degree '
                'reads almost as relief, proof the sign knows exactly when rigor '
                'should step aside for comfort.',
     'colors': 'A planet at this degree often shows real tenderness expressed inside a '
               'serious or difficult structure, care that insists on making room for '
               'lightness precisely where it is hardest to find. The Moon or Jupiter '
               'here can indicate someone who brings genuine warmth into clinical or '
               'demanding settings. It rewards remembering that discipline and delight '
               'are not actually opposites.',
     'reflection': 'Where in your most serious responsibilities have you made real '
                   'room for something purely joyful?'},
    {'degree': 16,
     'image': 'A school yard fills with boys and girls, all dressed for gymnasium '
              'class.',
     'meaning': 'Uniform structure, applied evenly to everyone present, and inside '
                'that structure real vitality and play still happen freely. This '
                'degree honors the discipline of shared form, everyone dressed the '
                'same, everyone following the same schedule, without that sameness '
                "actually flattening anyone's individual energy. Capricorn often gets "
                "read as rigid, but this degree shows the sign's structure functioning "
                'exactly as it should: a container sturdy enough that real movement '
                'and growth can happen safely inside it.',
     'colors': 'A planet at this degree often shows comfort operating inside shared, '
               'standardized structure, without losing real individual vitality to '
               'the uniform. Mars or Mercury here can indicate someone who thrives '
               'specifically because a clear, common framework has been provided. It '
               'rewards trusting that the right structure enables energy rather than '
               'suppressing it.',
     'reflection': 'What shared structure in your life is currently giving your own '
                   'energy somewhere safe to actually move?'},
    {'degree': 17,
     'image': 'A long-repressed woman finds a genuine sense of release, briefly free '
              'of every rule.',
     'meaning': 'Restraint held too long finds, in this degree, its necessary '
                'counterweight: a real, if temporary, escape from every expectation '
                "that has been quietly accumulating. Capricorn knows discipline better "
                "than any other sign, and this degree is the sign's own honest "
                'admission that discipline held without relief eventually needs an '
                'outlet, or it curdles into something worse than the rules it was '
                'protecting. There is nothing shameful in the image, only relief, '
                'finally taken.',
     'colors': 'A planet at this degree often shows a real need for periodic, honest '
               'release from accumulated structure and expectation, not indulgence '
               'but necessary relief. Uranus or Venus here can indicate someone who '
               'functions far better once they have permitted themselves a genuine, '
               'unashamed break from the rules. It rewards taking the release '
               'seriously instead of feeling guilty about needing it.',
     'reflection': 'What rule have you been quietly, faithfully keeping for so long '
                   'that you are actually overdue a real, unashamed break from it?'},
    {'degree': 18,
     'image': "A ship's flag flies from the mast of a warship crossing open water.",
     'meaning': 'Identity here is announced from a distance, visible long before the '
                'vessel itself can be fully seen: a flag says exactly which structure, '
                'which allegiance, which authority this ship answers to. Capricorn '
                'cares, more than most signs will admit, about exactly this kind of '
                'legible affiliation, the emblem that tells everyone watching '
                'precisely where you stand and whom you represent. There is real '
                'pride in the image, and real responsibility too, since flying a flag '
                'this recognizable means living up to what it promises.',
     'colors': 'A planet at this degree often shows a strong, visible sense of '
               'institutional or national identity, allegiance worn plainly rather '
               'than kept private. Saturn or the Sun here can indicate someone whose '
               'reputation is closely bound to the structure or tradition they '
               'represent. On the Midheaven, it favors a public role that is instantly '
               'legible by its association alone.',
     'reflection': 'What flag are you currently flying, and does it still say exactly '
                   'what you actually stand for?'},
    {'degree': 19,
     'image': 'A very young child carries a bag of groceries far heavier than she is '
              'used to.',
     'meaning': 'Responsibility arrives here before it is entirely age-appropriate, a '
                'small body taking on a real, tangible weight because the task needed '
                "doing and she was the one available. Capricorn's whole arc is early "
                'maturity, competence assumed ahead of schedule, and this degree '
                'pictures exactly that, plainly and without sentimentality. There is '
                'real strain in the image, and also real capability, since the child '
                'is managing the bag, even if it is heavier than it should be for '
                'her.',
     'colors': 'A planet at this degree often shows real responsibility taken on '
               'earlier than expected, competence that developed out of necessity '
               'rather than at a comfortable pace. Saturn here is especially at home, '
               'favoring someone who grew capable fast because the task simply needed '
               'doing. It rewards acknowledging the weight, even while still managing '
               'to carry it well.',
     'reflection': 'What responsibility did you pick up earlier than you should have '
                   'had to, and have you ever actually set it down long enough to '
                   'feel how heavy it was?'},
    {'degree': 20,
     'image': 'During a service, a choir sings from somewhere out of sight.',
     'meaning': 'The music is real and moving precisely because its source stays '
                'hidden, devotion offered without needing to be seen offering it. '
                "Capricorn's discipline usually wants visible credit for visible "
                'effort, and this degree offers a genuine counterpoint: service '
                'rendered from concealment, its value entirely unaffected by '
                'anonymity. The congregation is moved by the sound alone, which is, '
                'in its way, the purest possible test of whether the offering was '
                'actually good.',
     'colors': 'A planet at this degree often shows a real capacity for devoted, '
               'high-quality work offered without needing visible credit for it. '
               'Neptune or Saturn here can indicate someone whose best contribution '
               'happens specifically out of sight. It rewards trusting that unseen '
               'work, done this well, still counts completely.',
     'reflection': 'What are you currently contributing from somewhere the room '
                   'cannot actually see you standing?'},
    {'degree': 21,
     'image': 'Baton in hand, one runner sprints to close the gap and pass it to the '
              'next in a relay race.',
     'meaning': 'No single runner covers the whole distance; the achievement belongs '
                'to the sequence, each leg only as good as the handoff that connects '
                'it to the next. Capricorn, so often pictured as a solitary climber, '
                'meets here a genuinely collective version of ambition, where the win '
                'depends on trusting someone else with exactly the right moment of '
                'transfer. There is real vulnerability in a handoff, a beat where the '
                'baton belongs to no one fully, and this degree asks Capricorn to '
                'trust that beat completely.',
     'colors': 'A planet at this degree often shows real capacity to contribute one '
               'leg of a longer, shared effort, and to trust the handoff to someone '
               'else without needing to run the whole race personally. Mars or '
               'Mercury here can indicate genuine skill at exactly the moment of '
               'transition between people or phases. It rewards trusting your '
               "teammates with the baton as much as you trust your own leg of the "
               'race.',
     'reflection': 'Where in your life are you currently mid-handoff, and are you '
                   'actually trusting the exchange, or still gripping the baton a '
                   'beat too long?'},
    {'degree': 22,
     'image': 'A defeated general accepts the loss with real, visible grace.',
     'meaning': 'Character, this degree insists, shows up most clearly not in the '
                'winning but in exactly how a real loss gets carried. The general does '
                'not pretend the defeat did not happen, and does not collapse under '
                'it either, meeting the outcome with a dignity that costs '
                "considerably more than victory ever would have. Capricorn's whole "
                'relationship to achievement gets tested here, since the sign\'s '
                'authority is built on winning, and this degree asks what remains of '
                'that authority when winning is, honestly, no longer available.',
     'colors': 'A planet at this degree often shows genuine nobility in the face of '
               'real setback, dignity that holds up specifically when a loss is '
               'unavoidable and visible to everyone watching. Saturn here can '
               'indicate someone whose true character is most legible in exactly how '
               'they handle failure. It rewards trusting that grace under defeat is '
               'its own, separate kind of authority.',
     'reflection': 'What loss are you currently carrying, and is the way you are '
                   'carrying it actually the version of yourself you would want '
                   'remembered?'},
    {'degree': 23,
     'image': 'A soldier receives two medals for bravery shown in battle.',
     'meaning': 'Recognition, doubled, for courage that was tested more than once: '
                'this degree honors sustained bravery, proven under real, repeated '
                'pressure rather than a single lucky moment. Capricorn respects earned '
                'achievement above almost anything else, and this degree gives the '
                'sign a genuinely earned image, honor that came from actual risk '
                'survived, twice validated rather than merely claimed. There is real '
                'weight to wearing two medals instead of one, since it says the '
                'courage was not a fluke.',
     'colors': 'A planet at this degree often shows achievement or recognition earned '
               'through repeated, tested courage rather than a single moment of luck. '
               'Mars or the Sun here can indicate someone whose reputation for bravery '
               'has genuinely been proven more than once. It rewards trusting '
               'recognition that arrived because the risk was real and repeated.',
     'reflection': 'What have you actually risked more than once, that has genuinely '
                   'earned you the credit you are still, quietly, carrying?'},
    {'degree': 24,
     'image': 'A woman walks through the convent doors, choosing a life set apart.',
     'meaning': 'This degree pictures a deliberate, formal narrowing: one path chosen '
                'completely, at the cost of every other path that will now go '
                "unlived. Capricorn understands sacrifice as structure, a life given "
                'real shape precisely by everything it has decided to exclude. There '
                'is nothing tragic in the image on its own terms, only decisiveness, '
                "the sign's own gift for committing fully once a direction has "
                'actually been chosen rather than hedging every door open '
                'indefinitely.',
     'colors': 'A planet at this degree often shows real capacity for total, formal '
               'commitment to a single path, chosen deliberately and without '
               'half-measures. Saturn or Neptune here can indicate a life genuinely '
               'organized around one central devotion. It rewards trusting that the '
               'doors you have closed on purpose are part of what gives the open one '
               'its actual meaning.',
     'reflection': 'What have you committed to fully enough that you have genuinely '
                   'stopped grieving the paths it required you to close?'},
    {'degree': 25,
     'image': 'A shop stands full, floor to ceiling, with fine, richly patterned rugs.',
     'meaning': 'Value, here, has been gathered patiently from far away and laid out '
                'for anyone with the eye to actually recognize it. Capricorn\'s '
                'relationship to material wealth shows itself plainly in this degree: '
                'not flashy accumulation, but real, discerning collection, each rug '
                'chosen for genuine craft rather than mere volume. There is expertise '
                'required simply to run a shop like this well, knowing what is '
                'actually fine from what only looks fine.',
     'colors': 'A planet at this degree often shows real discernment around material '
               'value, an eye trained well enough to tell genuine craft from mere '
               'appearance. Venus or Saturn here can indicate a gift for accumulating '
               'quality deliberately, over real time, rather than quickly or '
               'carelessly. It rewards trusting your own trained eye over the easier, '
               'louder claims of a room.',
     'reflection': 'What have you collected slowly enough, and with a good enough eye, '
                   'that its actual value is finally starting to show?'},
    {'degree': 26,
     'image': 'A water spirit dances in the shimmering mist thrown up by a waterfall.',
     'meaning': "Even Capricorn's mountain terrain produces something this "
                'unguarded: a spirit made entirely of movement and light, dancing in '
                'exactly the spray that a hard, falling force of water throws into '
                'the air. This degree suggests that where the ground gets steepest '
                'and the water falls hardest, something genuinely magical gets '
                'generated as a byproduct, unplanned and lovely. Capricorn rarely '
                'trusts anything this ungoverned, and this degree asks it to notice '
                'the enchantment the climb itself keeps producing.',
     'colors': 'A planet at this degree often shows real, unexpected magic generated '
               'by difficulty itself, a lightness that appears specifically at the '
               'site of real force or hardship. Neptune here is especially at home, '
               'favoring genuine enchantment found in demanding, elemental '
               'conditions. It rewards watching for the mist your own hardest efforts '
               'have been quietly throwing off.',
     'reflection': 'What unexpected lightness has your hardest, most demanding work '
                   'actually been generating, right in its own spray?'},
    {'degree': 27,
     'image': 'Pilgrims climb a long, steep stairway toward a shrine set high on a '
              'mountain.',
     'meaning': 'The climb itself is the discipline here, each worn step a small act '
                'of devotion repeated by countless travelers before this one. '
                "Capricorn's whole nature is contained in this image, the mountain as "
                'destination and as method both, arrival meaning nothing without the '
                'deliberate, difficult ascent that earns it. This degree honors '
                'effort undertaken specifically because the goal is sacred, not '
                'merely because the goal is high.',
     'colors': 'A planet at this degree often shows real willingness to undertake a '
               'long, demanding ascent toward something genuinely meaningful, '
               'discipline in service of devotion rather than mere achievement. '
               'Saturn or Jupiter here can indicate someone for whom the difficulty of '
               'the climb is inseparable from the value of the destination. It '
               'rewards trusting that the steps themselves are part of what you came '
               'for.',
     'reflection': 'What mountain are you currently climbing, one worn step at a time, '
                   'because the destination is actually sacred to you, not just '
                   'impressive?'},
    {'degree': 28,
     'image': 'A large aviary attached to a country house hums with the singing of '
              'many contented birds.',
     'meaning': 'Structure, built with real intention, creates the exact conditions '
                'where song can flourish safely: the aviary did not happen by '
                'accident, someone designed it specifically so this much life could '
                "be contained and still be genuinely happy inside the containment. "
                "Capricorn's gift for building shows itself at its warmest here, "
                'proof that a well-made structure is not a cage, it is what actually '
                'lets abundant, singing life thrive rather than scatter.',
     'colors': 'A planet at this degree often shows a real talent for building '
               'structures generous enough that whoever lives inside them actually '
               'flourishes, rather than merely survives. Venus or Jupiter here can '
               'indicate someone whose careful containers produce real, contented '
               'abundance. It rewards trusting that the right structure is what makes '
               'the singing possible, not what silences it.',
     'reflection': 'What structure have you built well enough that everyone inside it '
                   'is actually, audibly, thriving?'},
    {'degree': 29,
     'image': 'A woman reads the shapes left in a cup of tea leaves for someone eager '
              'to know what is coming.',
     'meaning': 'Near the very end of the sign, Capricorn allows itself something it '
                'usually distrusts entirely: reading toward the future by a method '
                'that cannot be proven, only interpreted. This degree honors '
                'intuition given real, if informal, structure, a practiced eye '
                'applied to an ordinary cup in order to say something about what has '
                'not happened yet. There is real vulnerability in seeking this kind of '
                'reading, wanting to know, and real skill in offering it honestly '
                'rather than only telling people what they hope to hear.',
     'colors': 'A planet at this degree often shows a genuine, trained sensitivity to '
               'pattern and omen, insight offered through an informal but real '
               'practice. Neptune or the Moon here can indicate someone whose '
               'intuitive reading of a situation deserves to be taken as seriously as '
               'any more official forecast. It rewards trusting a reading, your own '
               'or someone else\'s, that was actually done with skill and care.',
     'reflection': 'What has someone recently read correctly in the ordinary '
                   'leftovers of your life, that you are still deciding whether to '
                   'believe?'},
    {'degree': 30,
     'image': 'In a paneled, richly furnished boardroom, a handful of powerful people '
              'have quietly convened.',
     'meaning': 'Capricorn closes exactly where it opened, with authority, except now '
                'the claim from degree one has become an entire apparatus: a room '
                'built for exactly this purpose, decisions being made that will '
                'ripple outward to people who will never see the room itself. This is '
                'structure completed, power no longer demanding recognition but '
                'simply, quietly, exercising itself. The secrecy is not shame, it is '
                'how consequential decisions have always actually been made, mostly '
                'out of public view, by people who built their way into the room over '
                'real time.',
     'colors': 'A planet at this degree often shows real, consolidated authority, '
               'influence that no longer needs to announce itself because the '
               'structure around it already does. Saturn or Pluto here can indicate '
               'someone whose power operates mostly out of sight, effective precisely '
               'because it does not need display. It rewards being honest with '
               'yourself about which rooms you are actually already sitting in.',
     'reflection': 'What quiet room have you already earned a seat at, whether or not '
                   'anyone outside it knows your name yet?'},
]

assert len(ENTRIES) == 30, f"expected 30 Capricorn degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Capricorn degrees out of order"
