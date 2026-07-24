"""Sabian symbol data for Pisces.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against four
independent published sources (kerykeion.net's foundation-sabian-pisces
page, jamesburgess.com / Sacred 7 Academy's pisces-sabians list,
astronarrative.com's pisces.html, and cafeastrology.com's
sabiansymbols_degreemeanings.html) before being hand-typed; all four agree
on all 30 degrees with no unresolved conflicts. Degree-labeling offset was
explicitly checked: astronarrative.com and cafeastrology.com both label
degrees on the "N-1 to N" convention (e.g. their "0-1" bucket is this
file's degree 1, their "29-30" bucket is this file's degree 30), while
kerykeion.net and jamesburgess.com label degrees 1-30 directly; the actual
symbol content in each bucket was confirmed to match across both
conventions at every degree, so no off-by-one occurred. Pisces 30, "the
great stone face," was further confirmed via jamesburgess.com's dedicated
the-great-stone-face.html page, which quotes Rudhyar's full original
wording ("A majestic rock formation resembling a face is idealised by a
boy who takes it as his ideal of greatness, and as he grows up, begins to
look like it"), matching cafeastrology's "29-30" entry exactly. Do NOT
extend this list, or write a new sign's list, without the same
verification discipline: fewer verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a public
market"), not a verbatim quote of Marc Edmund Jones' 1953 book or Dane
Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`, `colors`,
and `reflection` are original Twelve Rooms interpretation, written fresh
for this project; none of it is copied from Jones or Rudhyar.

DATED IMAGERY: Pisces 21's 1925 original names a "Chinese servant"
watching over the girl and lamb. Per Shannon's standing policy, the
canonical mapping is kept, but `image` restates it respectfully without
the ethnic label (as "a gentle household caretaker"), and a `note` field
is attached below the symbol card. See SCHEMA.md for the full policy.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Pisces", "slug": "pisces", "glyph": "♓︎", "order": 12}

# The 30 degrees of Pisces, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and (only on degree 21) note (str). See SCHEMA.md for
# what each field means.
ENTRIES = [
    {'degree': 1,
     'image': 'A crowded public market, farmers and merchants laying out every kind of '
              'goods at once.',
     'meaning': "Aries opened the zodiac alone, meeting a single companion by the sea. "
                "Pisces, the sign that closes the circle, opens instead onto a whole "
                "market: everyone's harvest and handiwork laid out together, farmers "
                'and middlemen mixed shoulder to shoulder with no real wall between '
                "them. This is Pisces's first instinct made plain, before any of the "
                "sign's more private, oceanic imagery arrives: what one person makes, "
                'the community holds in common. Nothing here is hoarded, nothing kept '
                'off to the side; abundance means little to this degree until it has '
                'actually been shared out.',
     'colors': 'A planet at Pisces 1 often shows a life oriented toward the common pool '
               'from the very start, resources, ideas, or care that circulate rather '
               'than stay privately held. Venus here can indicate real skill at '
               "exchange, knowing what everyone in the room actually needs. The Sun or "
               "Jupiter at this degree can describe someone whose personal abundance "
               "only feels complete once it has been laid out for others to draw from.",
     'reflection': 'What have you been quietly holding back from the shared table, '
                   'that was never actually yours to keep to yourself?'},
    {'degree': 2,
     'image': 'A squirrel hides from hunters, staying perfectly still until the danger '
              'passes.',
     'meaning': 'One degree into its final sign, the zodiac remembers that softness '
                'needs a survival instinct too. The squirrel is not brave in any showy '
                'sense, it simply knows exactly how not to be seen, and that quiet, '
                'practiced stillness is its whole defense. Pisces is often read as pure '
                'permeability, absorbing everything without a boundary, but this '
                'degree insists the sign also knows how to disappear when '
                'disappearing is what safety actually requires.',
     'colors': 'A planet at this degree often shows real instinct for self-protection '
               'through invisibility rather than confrontation, a nervous system that '
               'knows exactly when to go still. The Moon here can indicate genuine '
               'sensitivity to danger long before it is consciously named. It rewards '
               'trusting the freeze response as wisdom, not weakness.',
     'reflection': 'What danger are you currently sensing correctly, even though '
                   'going still is the only response you have found for it yet?'},
    {'degree': 3,
     'image': 'Petrified tree trunks lie broken across a stretch of desert sand.',
     'meaning': 'Wood that has turned entirely to stone, in a landscape now too dry to '
                'have grown it. This degree holds an ocean of time compressed into '
                'geology, life that lived, died, and was slowly replaced mineral by '
                'mineral until only its exact shape remained, hard where it used to be '
                'pliant. Pisces spends much of the zodiac dissolving; this degree '
                'shows the opposite motion, softness gradually crystallizing into '
                'something that will now outlast the very desert around it.',
     'colors': 'A planet at this degree often shows feeling or memory that has hardened '
               'over long stretches of time into something permanent, still '
               'unmistakably shaped by what it once was. Saturn here can indicate real '
               'endurance built from something originally much softer. It rewards '
               'recognizing the fossil in yourself as proof of an entire lost forest, '
               'not evidence that nothing ever grew there.',
     'reflection': 'What softness in you has, over enough time, turned to stone, and '
                   'what is it still shaped like underneath?'},
    {'degree': 4,
     'image': 'Heavy traffic crowds a narrow strip of land connecting two seaside '
              'towns.',
     'meaning': 'A single thin passage, asked to carry far more than it was built for, '
                'water pressing in on both sides. This degree is Pisces meeting its '
                'own bottleneck: two whole worlds trying to move through one narrow '
                'connection at once, everyone needing to get from one shore to the '
                'other along the same crowded strip. There is real tension in an '
                'isthmus like this, since the very thing that makes it valuable, that '
                'it connects two seas, is also exactly what makes it so congested.',
     'colors': 'A planet at this degree often shows real pressure at a single '
               'connecting point in a life, one relationship, one decision, one '
               'narrow channel expected to carry everything through at once. Mercury '
               'or Saturn here can indicate real skill managing bottlenecks that '
               'cannot simply be widened. It rewards patience with a passage that is '
               'doing more work than its size suggests it should.',
     'reflection': 'What narrow connection in your life is currently carrying far '
                   'more traffic than it was ever built to hold?'},
    {'degree': 5,
     'image': 'A church holds a bazaar, faith and commerce set up side by side.',
     'meaning': "Devotion, paying its own way: nothing here treats fundraising as "
                'beneath the sacred, the church simply opens its doors and lets the '
                'congregation buy and sell in service of something larger than any '
                'single sale. Pisces rarely gets credit for practicality, but this '
                'degree shows the sign perfectly capable of it, generosity organized '
                'into stalls and price tags without losing any of its actual warmth.',
     'colors': 'A planet at this degree often shows real comfort raising resources for '
               'a cause through community effort rather than solitary sacrifice. '
               'Jupiter or Venus here can indicate genuine skill turning collective '
               'goodwill into something tangible and useful. It rewards trusting '
               'that faith and fundraising are not actually in tension.',
     'reflection': 'What cause do you believe in enough to actually set up a table '
                   'for it?'},
    {'degree': 6,
     'image': 'A column of army officers marches past in full dress uniform.',
     'meaning': 'Order, displayed rather than merely followed: every rank visible at '
                'once, the whole hierarchy walking past in a single coordinated line. '
                'This degree gives Pisces, a sign usually described as boundaryless, '
                'a picture of real structure held with total discipline, each officer '
                'answering to the rank above and beneath in a formation that leaves '
                "nothing to individual improvisation. There is a kind of beauty in "
                "structure this complete, the sign's usual fluidity temporarily given "
                'a very firm shape.',
     'colors': 'A planet at this degree often shows genuine respect for rank, '
               'ceremony, and earned hierarchy, expressed outwardly rather than only '
               'privately felt. Saturn here can indicate real comfort inside a '
               'clearly ordered chain of command. It rewards recognizing that some '
               'structure, worn well, is its own kind of dignity.',
     'reflection': 'What formation are you currently marching in, and do you '
                   'actually know where you rank inside it?'},
    {'degree': 7,
     'image': "A shaft of light falls on a large cross lying across rocks at the sea's "
              'edge, mist rising around it.',
     'meaning': "One of Pisces's own defining images: sacrifice, illuminated rather "
                'than hidden, set right where solid ground meets open water. The '
                'cross is not standing upright in a church, it lies among the rocks, '
                'weathered by the same sea the sign is always returning to, and the '
                'light finds it anyway. This degree holds the whole Piscean theme of '
                'redemptive suffering in a single frame, loss transfigured, briefly, '
                'into something visibly touched by grace.',
     'colors': 'A planet at this degree often shows a life genuinely marked by '
               'sacrifice that later reveals its own meaning, suffering that the '
               'light eventually finds and reframes. Neptune here is especially at '
               'home, real capacity for transcendence through what was given up '
               'rather than what was gained. It rewards trusting that the mist will '
               'eventually clear enough to see what the light was actually resting '
               'on.',
     'reflection': 'What sacrifice in your own life is still lying in the mist, '
                   'waiting for its meaning to actually become visible?'},
    {'degree': 8,
     'image': 'A young girl blows a bugle, sounding a call.',
     'meaning': 'One small figure, and a sound built to carry much further than she '
                'is. The bugle does not ask permission to be heard, and neither, in '
                'this moment, does she: an unmistakable signal sent out plainly, meant '
                'to gather or warn or wake whoever is in range of it. Pisces is often '
                'soft-spoken, but this degree shows the sign perfectly capable of a '
                'clear, carrying call when the moment actually requires one.',
     'colors': 'A planet at this degree often shows real capacity to sound a clear '
               'signal at exactly the right moment, a voice that carries further than '
               "its owner's stature would suggest. Mercury or Mars here can indicate "
               'someone who knows how to call a room, or a crowd, to attention. It '
               'rewards trusting that your call is worth sounding, even before you '
               'know who will answer it.',
     'reflection': 'What call have you been quietly rehearsing that actually needs '
                   'to be sounded out loud?'},
    {'degree': 9,
     'image': 'A jockey urges his horse forward, determined to outrun every other '
              'rider.',
     'meaning': 'Pure competitive will, riding something far stronger than itself '
                'toward a finish line that only one of them will reach first. This '
                'degree gives usually diffuse Pisces a moment of total focus, the '
                "sign's normally wide attention narrowed down to a single track and a "
                'single outcome. There is real risk in urgency this sharp, but also '
                'real aliveness, the sign discovering that it, too, can want to win.',
     'colors': 'A planet at this degree often shows a competitive drive that can '
               'surprise people who expect only softness from this part of a chart. '
               'Mars here can indicate real hunger to be first, sharpened rather than '
               'dulled by the stakes. It rewards channeling that urgency toward an '
               'actual finish line instead of a vague, restless push.',
     'reflection': 'What race are you currently riding all-out, and have you actually '
                   'let yourself want to win it?'},
    {'degree': 10,
     'image': 'A pilot presses on through thick, ground-hiding cloud, trusting the '
              'instruments.',
     'meaning': 'Faith, made mechanical and literal: the aviator cannot see the '
                'ground, cannot see much of anything, and keeps flying anyway, '
                'trusting instruments and training over the evidence of the eyes. '
                'This is Pisces at its most genuinely spiritual, moving forward '
                'through real confusion because something more reliable than sight '
                'has taken over the navigation. Nothing here denies how disorienting '
                'the cloud actually is; the degree simply insists the flight '
                'continues regardless.',
     'colors': 'A planet at this degree often shows real capacity to keep moving '
               'through genuine confusion, trusting inner instruments over what the '
               'eyes can currently confirm. Neptune or Uranus here can indicate '
               'someone who navigates uncertainty better than they navigate clear '
               'skies. It rewards trusting the instrument panel when the view '
               'outside has gone entirely white.',
     'reflection': 'What are you currently flying through blind, trusting '
                   'instruments you cannot actually see the results of yet?'},
    {'degree': 11,
     'image': 'A line of men walks a narrow path, each one searching for '
              'enlightenment.',
     'meaning': 'Seeking, made communal and physical: a whole line of travelers, each '
                'pursuing the same illumination, sharing one narrow trail because the '
                'way apparently only runs one width wide. This degree honors real '
                'spiritual discipline, walking toward understanding rather than '
                'simply waiting for it, and it is honest that the way is narrow, that '
                'this kind of seeking rarely allows for wandering off in ten '
                'directions at once.',
     'colors': 'A planet at this degree often shows genuine, disciplined spiritual '
               'seeking, a willingness to stay on one narrow path rather than '
               'sampling every possible route. Jupiter or Neptune here can indicate '
               'real, sustained pursuit of understanding. It rewards trusting that a '
               'path this narrow was chosen for a reason.',
     'reflection': 'What narrow path are you still walking, in search of an '
                   'illumination you have not yet actually reached?'},
    {'degree': 12,
     'image': 'In a private lodge, new members of an esoteric order are questioned '
              'and tested.',
     'meaning': 'Entry into hidden knowledge has a price, and this degree names it '
                'plainly: examination, character tested before deeper access is '
                'granted. Pisces holds real affinity for the occult and the unseen, '
                'but this degree insists that even mystical belonging has to be '
                'earned, that a brotherhood built on secrecy still has real standards '
                'for who it lets all the way in.',
     'colors': 'A planet at this degree often shows genuine respect for initiation, '
               'understanding that real depth of belonging has to be tested rather '
               'than simply assumed. Pluto or Saturn here can indicate someone who '
               'has actually passed through this kind of scrutiny to reach what they '
               'now hold. It rewards remembering that the test was never cruelty, it '
               'was the door.',
     'reflection': 'What examination have you already passed, that you have not yet '
                   'given yourself credit for actually earning?'},
    {'degree': 13,
     'image': 'An old sword that saw many battles now rests behind glass in a '
              'museum.',
     'meaning': 'Violence, retired into artifact: the blade did real work once, and '
                'now it simply sits, studied rather than swung, its danger converted '
                'entirely into history. This degree carries something quietly moving '
                'about weapons that outlive their wars, evidence that even the '
                'sharpest conflict eventually settles into something that can be '
                'looked at calmly, from a safe distance, by people who never had to '
                'face it.',
     'colors': 'A planet at this degree often shows a life that has moved a former '
               'battle into memory, kept and honored rather than still actively '
               'fought. Mars or Saturn here can indicate someone who has genuinely '
               'laid an old weapon down. It rewards trusting that displaying the '
               'sword is not the same as still needing to use it.',
     'reflection': 'What old battle of yours has actually earned its case in the '
                   'museum, instead of still hanging on your wall, ready?'},
    {'degree': 14,
     'image': 'A woman wears a wide stole of fox fur, wrapped close against the '
              'cold.',
     'meaning': 'Warmth borrowed from an animal known for its cunning, worn now as '
                'pure comfort and status. This degree is Pisces meeting luxury and '
                'self-protection at once, instinct tamed into something soft enough '
                "to wear close to the skin. There is real vanity in it, and real "
                "practicality too, since a fox's coat was built for exactly this "
                'kind of insulation long before it became anyone\'s fashion.',
     'colors': 'A planet at this degree often shows a taste for comfort that is also, '
               'quietly, armor, softness chosen deliberately for the protection it '
               'provides. Venus here can indicate real elegance built around genuine '
               'self-care rather than display alone. It rewards admitting that '
               'looking good and staying warm were never actually separate goals.',
     'reflection': 'What have you wrapped yourself in lately that is doing more real '
                   'protecting than it gets credit for?'},
    {'degree': 15,
     'image': 'An officer drills his men through a mock assault under real, live '
              'artillery fire.',
     'meaning': 'The midpoint of the sign, and it lands on the hardest kind of '
                'preparation there is: rehearsal made as real as danger itself, so '
                'that when the actual moment comes, the body already knows what to '
                'do. This degree refuses to let readiness stay theoretical. Pisces '
                'can drift toward hoping things simply work out; this degree insists '
                'that real courage gets built in advance, under conditions that do '
                'not pretend to be gentle.',
     'colors': 'A planet at this degree often shows genuine discipline built through '
               'realistic, high-stakes rehearsal rather than comfortable practice. '
               'Mars or Saturn here can indicate someone who trains for the worst '
               'case specifically so the real case will not overwhelm them. It '
               'rewards trusting the drill, even while the shells are actually '
               'live.',
     'reflection': 'What real danger have you actually rehearsed for, rather than '
                   'simply hoped you would handle when it arrived?'},
    {'degree': 16,
     'image': 'Alone in a quiet study, a writer or artist feels inspiration arrive.',
     'meaning': "This is Neptune's own gift, given a room and a moment to land in: "
                'something arrives from somewhere the conscious mind did not build, '
                'and the only real work left is receiving it without getting in its '
                "own way. Pisces's whole reputation for imagination rests on exactly "
                "this degree, the sign's basic trust that not everything worth "
                'making has to be forced, some of it simply has to be let in.',
     'colors': 'A planet at this degree often shows real receptivity to inspiration '
               'that arrives from outside deliberate effort, ideas that seem to '
               'descend rather than get built. Neptune or the Moon here can indicate '
               'a genuinely porous, permeable creative channel. It rewards '
               'protecting the quiet a flow like this actually needs to arrive.',
     'reflection': 'What has been trying to arrive in your own quiet study, that you '
                   'have been too busy or too loud to actually receive?'},
    {'degree': 17,
     'image': 'A crowd walks an Easter promenade, dressed for the occasion of new '
              'life.',
     'meaning': 'Renewal, made public and communal: a whole street of people, dressed '
                'brightly, walking together specifically to mark the return of life '
                'after a long dormant season. This degree gives Pisces, so '
                'associated with endings, a genuine picture of what comes after one: '
                'not private relief, but a shared, visible celebration, everyone '
                'choosing to be seen at exactly the moment resurrection is being '
                'marked.',
     'colors': 'A planet at this degree often shows real capacity to celebrate '
               'renewal openly and communally rather than only privately. Venus or '
               'Jupiter here can indicate a genuine gift for marking new beginnings '
               'with real, visible joy. It rewards trusting that some resurrections '
               'are actually meant to be walked in public.',
     'reflection': 'What return or renewal in your own life deserves an actual '
                   'promenade, instead of a quiet private acknowledgment?'},
    {'degree': 18,
     'image': 'Inside an enormous tent, a well-known preacher holds a crowd with a '
              'dramatic revival meeting.',
     'meaning': 'Faith, staged for maximum effect, and genuinely moving people '
                'anyway: the tent is huge on purpose, the performance is deliberate, '
                'and the emotion in the crowd is nonetheless real. This degree asks '
                'Pisces to hold two truths that usually feel opposed, that showmanship '
                'and sincerity can occupy the exact same tent, that a crowd swept up '
                'by spectacle can still be having a real spiritual experience '
                'underneath the theater of it.',
     'colors': 'A planet at this degree often shows genuine charisma capable of '
               'moving a large group emotionally, sincerity and performance working '
               'together rather than against each other. Neptune or the Sun here can '
               'indicate real gifts for public, large-scale inspiration. It rewards '
               'checking, honestly, whether the feeling being stirred is actually '
               'true, not just theatrical.',
     'reflection': 'Where in your own life are real feeling and real performance '
                   'currently happening at the exact same time, and are you sure '
                   'which one is leading?'},
    {'degree': 19,
     'image': 'A teacher works closely with a single student, passing on what they '
              'know.',
     'meaning': 'Wisdom, handed down one person at a time: after a crowded tent, this '
                'degree narrows all the way down to a single relationship, one '
                'master and one disciple, learning that actually happens best at '
                'this intimate a scale. Pisces holds real reverence for lineage, for '
                'knowledge that gets carried forward specifically because someone '
                'experienced took the time to carry it to someone specific.',
     'colors': 'A planet at this degree often shows real capacity for close, '
               'one-on-one mentorship, either giving it or genuinely receiving it. '
               'Mercury or Saturn here can indicate a teacher-student bond that '
               "shapes a whole life's direction. It rewards trusting that this kind "
               'of transmission cannot actually be rushed or scaled up.',
     'reflection': 'Who is currently teaching you, one on one, in a way you have not '
                   'yet thanked them properly for?'},
    {'degree': 20,
     'image': 'A table is set for dinner, ready for the people who will gather '
              'around it.',
     'meaning': 'Preparation made for company that has not yet arrived: the places '
                'are set, the meal is ready, and the whole scene exists purely in '
                'anticipation of the people who are about to sit down together. This '
                'degree honors hospitality as its own real work, the quiet labor of '
                'getting a table ready specifically so that connection, when it '
                'comes, has somewhere comfortable to happen.',
     'colors': 'A planet at this degree often shows real talent for creating the '
               'conditions where genuine gathering and nourishment can happen. Venus '
               'or the Moon here can indicate someone who instinctively knows how to '
               'prepare a welcome before it is even asked for. It rewards trusting '
               'the table you have already set, instead of anxiously re-checking '
               'it.',
     'reflection': 'Who have you already set a place for, that you are still '
                   'waiting, a little nervously, to actually arrive?'},
    {'degree': 21,
     'image': 'A gentle household caretaker looks on as a young girl cuddles a small '
              'white lamb.',
     'meaning': 'Innocence, twice protected: the lamb by the girl, and the girl, in '
                'turn, by someone older and watchful standing quietly nearby. This '
                "degree is one of the sign's purest pictures of tenderness, softness "
                'held safely inside softness, nothing here asked to defend itself '
                'alone. Pisces understands, better than most signs, that real '
                'innocence needs real supervision to actually survive intact.',
     'colors': 'A planet at this degree often shows genuine tenderness that depends '
               'on, and deserves, real protection around it. The Moon or Venus here '
               'can indicate someone whose gentlest qualities were, at some point, '
               "carefully safeguarded by another person's watchfulness. It rewards "
               'extending that same quality of care to whatever in your life is '
               'currently this unguarded.',
     'reflection': 'What tenderness in your life is currently being kept safe only '
                   'because someone else is quietly watching over it?',
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 22,
     'image': 'A prophet carries tablets of new law down a mountainside.',
     'meaning': 'Revelation, brought back down into the world: whatever happened at '
                'the top of that mountain, in solitude, now has to be carried into a '
                'community that was not there for it, on tablets solid enough to '
                'survive the descent. This degree captures something essential about '
                'Pisces, that real spiritual experience does not stay useful until '
                'someone actually brings it back down and hands it to people who '
                'need it.',
     'colors': 'A planet at this degree often shows a real calling to bring private '
               'spiritual insight into public, usable form. Jupiter or Uranus here '
               'can indicate someone who returns from genuine solitary revelation '
               'with something concrete enough to actually share. It rewards '
               'trusting the descent as much as you trusted the climb.',
     'reflection': 'What have you received in private that is still sitting at the '
                   'top of the mountain, waiting for you to actually carry it down?'},
    {'degree': 23,
     'image': 'A medium conducts a seance, claiming to summon a visible presence '
              'from beyond.',
     'meaning': 'The boundary between the living and the dead, tested directly, in a '
                'darkened room, in front of witnesses who came specifically hoping it '
                "would give way. This degree sits at Pisces's most literal edge, the "
                "sign's deep interest in what lies past ordinary perception, staged "
                'here as an actual, watchable event. Whether or not the room '
                'believes what it sees, the hunger behind the seance, to touch what '
                'is supposedly gone, is entirely real.',
     'colors': 'A planet at this degree often shows real fascination with contact '
               'across the boundary between the visible and the unseen. Neptune or '
               'Pluto here can indicate genuine sensitivity to what most people '
               'dismiss as impossible to reach. It rewards staying honest about what '
               'is actually being contacted, and what is simply being performed.',
     'reflection': 'What do you find yourself still trying to reach, across a '
                   'boundary most people have already accepted as final?'},
    {'degree': 24,
     'image': 'On a small island ringed by open ocean, everyone lives in close, '
              'constant contact.',
     'meaning': "Isolation and intimacy, produced by the exact same water: the sea "
                'that cuts this community off from everywhere else is also what '
                'forces its people into such close, continuous relationship with one '
                'another. Pisces knows the ocean better than any other sign, and '
                'this degree shows one of its quieter effects, how being surrounded '
                'on all sides by something vast can actually draw a small group '
                'closer together rather than apart.',
     'colors': 'A planet at this degree often shows real closeness born from limited '
               'scale and shared boundary, a life lived in tight, constant contact '
               'with a small, chosen group. The Moon here can indicate someone who '
               'thrives specifically inside this kind of contained, interdependent '
               'community. It rewards trusting that the smallness of your world may '
               'be exactly what makes it this close.',
     'reflection': 'What small, surrounded world are you actually living inside, and '
                   'how much of your closeness to the people in it comes from its '
                   'very size?'},
    {'degree': 25,
     'image': 'A religious community manages to purify itself of corrupt practices '
              'and false ideals.',
     'meaning': 'Reform, achieved from the inside: not abandonment of the faith, but '
                'an honest reckoning with what had gone wrong inside it, and the '
                'real work of clearing it back out. This degree trusts that '
                'institutions built around real belief can still lose their way, and '
                'that recovering integrity is possible, though never automatic. '
                'Pisces, so often associated with faith itself, here takes on the '
                'harder, more practical job of keeping that faith honest.',
     'colors': 'A planet at this degree often shows real capacity to reform '
               'something from within rather than simply walking away from its '
               'failures. Saturn or Pluto here can indicate someone willing to do '
               'the difficult, unglamorous work of restoring integrity to a belief '
               'system or institution. It rewards trusting that purification is '
               'possible without needing to burn the whole structure down.',
     'reflection': 'What belief or practice in your own life needs this same kind of '
                   'honest reform, rather than either blind loyalty or total '
                   'abandonment?'},
    {'degree': 26,
     'image': 'At sunset, different people watch the same thin crescent moon and '
              'each decide it is time to act.',
     'meaning': 'One shared sign in the sky, read privately by many separate people, '
                'each finding in it permission for a project entirely their own. '
                'This degree honors the moon as a kind of common calendar, the same '
                'slender crescent giving different observers, in different lives, '
                'the exact same message: begin now. Pisces trusts timing that '
                'arrives this way, collectively visible, individually interpreted.',
     'colors': 'A planet at this degree often shows real sensitivity to timing '
               'signals that are available to everyone but noticed, and acted on, by '
               'very few. The Moon here is especially at home, an instinct for '
               'exactly when a new cycle has quietly begun. It rewards trusting your '
               'own reading of the sky, even if no one else around you has acted on '
               'it yet.',
     'reflection': 'What thin crescent have you already noticed, that is quietly '
                   'telling you it is time to actually begin?'},
    {'degree': 27,
     'image': 'A full harvest moon lights up a clear autumn sky.',
     'meaning': "Culmination, made visible: this is the year's fullest, most "
                'generous light, arriving exactly when the season\'s work is ready '
                'to be gathered in. Nothing about this degree is subtle, the moon is '
                'simply enormous and the sky is simply clear, and together they let '
                'an entire harvest be seen all at once, in full. Pisces, nearing its '
                'own late degrees, gets this rare moment of complete, undimmed '
                'illumination.',
     'colors': 'A planet at this degree often shows a life or project reaching '
               'visible, well-lit culmination right when it is most needed. Jupiter '
               'or the Moon here can indicate real abundance made fully visible '
               'rather than left half-seen. It rewards trusting the clarity of a '
               'harvest this bright, instead of second-guessing what it plainly '
               'shows you.',
     'reflection': 'What in your life is fully ripe right now, lit clearly enough '
                   'that you no longer have any excuse not to see it?'},
    {'degree': 28,
     'image': 'Under a full moon, a fertile garden shows off a wide variety of '
              'ripened vegetables.',
     'meaning': 'Abundance, this time literally underfoot rather than overhead: the '
                'moon simply provides enough light to actually see what the garden '
                'has already produced, row after row of different, fully grown '
                'food. This degree trusts that plenty, once it has been properly '
                'tended, does not need daylight to prove itself, moonlight is more '
                'than enough to reveal how much is actually there.',
     'colors': 'A planet at this degree often shows real, tangible abundance '
               'produced through patient, sustained tending rather than sudden '
               'windfall. Venus or Jupiter here can indicate someone whose garden, '
               'of whatever kind, has genuinely come in full. It rewards actually '
               'walking the rows at night to see everything that has quietly '
               'ripened.',
     'reflection': 'What have you been patiently tending that has already, quietly, '
                   'come in full, whether or not you have walked out to actually '
                   'look at it yet?'},
    {'degree': 29,
     'image': 'White light passes through a prism and splits into a full spread of '
              'color.',
     'meaning': 'One degree from the end of the entire zodiac, and the image is '
                'almost a diagram of the whole wheel: a single source of light, '
                'refracted into every distinct color at once, none of them false, '
                "all of them the same light seen differently. This is Pisces's "
                'closest approach to naming its own function directly, the sign '
                'that absorbs everything the other eleven signs were, and shows, in '
                'one clear image, that unity and multiplicity were never actually '
                'in conflict.',
     'colors': 'A planet at this degree often shows real capacity to hold many '
               'different expressions of the same underlying truth without needing '
               'to collapse them into one. Neptune here is especially at home, '
               'genuine range that all still traces back to a single, coherent '
               'source. It rewards trusting that the spectrum and the single light '
               'were always the same thing.',
     'reflection': 'What single truth in your life is currently showing up as many '
                   'different colors, and can you see all of them as coming from '
                   'the same source?'},
    {'degree': 30,
     'image': 'A boy comes to idealize a massive rock formation shaped like a face, '
              'and slowly, as he grows, begins to resemble it.',
     'meaning': 'The very last degree of the entire zodiac, and it closes not with '
                'an ending but with a becoming: a shape in stone, admired quietly '
                'enough and long enough that a whole life eventually grows to match '
                "it. This is the sign's real answer to the question every other "
                'degree has been circling, that what you steadily idealize is what '
                "you slowly turn into. The wheel that opened with Aries's woman "
                'rising newly formed from the sea closes here with a face fully, '
                'finally arrived at, thirty signs and three hundred sixty degrees of '
                'becoming resolved into one completed likeness, already carrying '
                'the whole cycle back toward its own beginning.',
     'colors': 'A planet at this final degree often shows a life quietly, steadily '
               'shaped by whatever it has chosen to hold up as its own ideal of '
               'greatness. The Sun or Saturn here can indicate someone whose '
               'character has visibly grown to match a model they admired long '
               'enough to actually become. It rewards choosing that ideal with real '
               'care, since this degree promises you will eventually look like it.',
     'reflection': 'What have you been idealizing long enough that you have already, '
                   'quietly, begun to grow into its likeness?'},
]

assert len(ENTRIES) == 30, f"expected 30 Pisces degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Pisces degrees out of order"
