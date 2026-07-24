"""Sabian symbol data for Taurus.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against
multiple independent published sources (not generated or guessed) before
being hand-typed. Do NOT extend this list, or write a new sign's list,
without the same verification discipline: fewer verified degrees beats
any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a clear
mountain stream"), not a verbatim quote of Marc Edmund Jones' 1953 book or
Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation,
written fresh for this project; none of it is copied from Jones or
Rudhyar.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Taurus", "slug": "taurus", "glyph": "♉︎", "order": 2}

# The 30 degrees of Taurus, in order 1-30. Each entry is a dict with the
# fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str). See SCHEMA.md for what each field means.
ENTRIES = [{'degree': 1,
  'image': 'A clear mountain stream.',
  'meaning': "After Aries broke the surface, Taurus opens by naming the substance "
             'underneath it: water falling down a mountainside, unforced, following '
             'gravity instead of will. It is clean specifically because it never stops '
             "moving, an early clue that this whole sign's promised stillness is not "
             'actually about staying put. What Aries claimed as pure impulse, Taurus '
             'receives as pure body: breath, blood, appetite, all of it running '
             'continuously and asking nothing of the self except to let it keep '
             'flowing. There is no ownership yet at this degree, no fence around the '
             'water, only the plain fact of its clarity.',
  'colors': 'A planet or point at Taurus 1 tends to carry an early, unearned clearness, '
            'something that has not yet been slowed by possession or effort. The Moon '
            'here often shows feelings that refresh themselves simply by continuing to '
            'move. Mercury can indicate thinking that stays lucid because it keeps '
            'running rather than pooling. It is a useful degree to remember on any '
            'planet that has since gotten complicated: something in you was this clean '
            'before it accumulated anything.',
  'reflection': 'What in you stays clear only because you keep letting it move, instead '
                'of trying to store it?'},
 {'degree': 2,
  'image': 'An electrical storm.',
  'meaning': "One degree into a sign famous for placidity, and the sky splits open "
             "instead. This is Taurus's undercurrent made visible: enormous stored "
             'charge, the kind that builds quietly in a body that looks calm, releasing '
             "all at once when the pressure finally has nowhere else to go. The sign's "
             'reputation for patience is real, but so is this, the reminder that '
             'patience is not the same thing as emptiness, that something is always '
             'accumulating underneath the stillness. Nothing about a storm asks '
             'permission to happen, it simply discharges what was already there.',
  'colors': 'A planet at this degree often carries real force held under an outwardly '
            'steady surface, capable of sudden, dramatic release when enough tension '
            'has gathered. Mars or Uranus here can indicate a temper that seems to come '
            'from nowhere but was actually building for a long time. It rewards '
            'noticing the charge accumulating early, rather than being surprised by the '
            'discharge.',
  'reflection': 'What has been quietly charging in you, underneath the calm, and how '
                'much longer can it wait to discharge?'},
 {'degree': 3,
  'image': 'Natural stone steps lead up to a lawn of clover in bloom.',
  'meaning': 'Not a staircase built by anyone, stone risers that occurred where the '
             'land itself rose, leading somewhere green and flowering as if the ground '
             'had planned the whole ascent. This degree trusts that the right path is '
             'often the one already shaped by the earth rather than the one engineered '
             "over it. Clover in bloom is luck's oldest image, and it arrives here as a "
             'destination reached by unhurried, natural steps rather than a leap. '
             'Taurus finds an early confidence: what is good does not usually require '
             'force to reach, only the patience to keep climbing what is already '
             'there.',
  'colors': 'A planet at this degree often favors advancement that feels organic rather '
            'than forced, one right step leading plainly to the next until abundance is '
            'simply standing there. Venus or Jupiter here can indicate luck that '
            'arrives by unhurried, natural progress instead of any dramatic leap. It '
            'rewards trusting a path that was already shaped, rather than insisting on '
            'building a new one.',
  'reflection': 'What natural step is right in front of you, that you keep looking past '
                'for a harder way up?'},
 {'degree': 4,
  'image': 'A pot of gold waits at the end of a rainbow.',
  'meaning': 'Promise, held at exactly the distance that keeps it a promise: the gold '
             'is real in the story, but the rainbow moves whenever you do, so the '
             "treasure stays perpetually one step beyond reach. This degree names "
             "Taurus's hunger honestly, the sign that wants tangible reward, wants it "
             "badly, and here meets the oldest trick of desire, that the horizon "
             "recedes at the same pace you walk toward it. It is not a cruel image, "
             'only an honest one: some rewards exist mainly to keep you moving in a '
             'good direction.',
  'colors': 'A planet at this degree often shows real motivation built around a '
            "valuable, slightly elusive goal, one that keeps its shine partly because "
            "it hasn't been caught yet. Jupiter or Venus here can indicate genuine "
            "optimism about future abundance, alongside a need to enjoy the walking "
            "and not only the arriving. It rewards noticing what the chase itself has "
            "already been worth.",
  'reflection': 'What rainbow have you been chasing, and has the walking already given '
                'you something the gold at the end never could?'},
 {'degree': 5,
  'image': 'A widow stands at an open grave.',
  'meaning': 'Loss, faced without the ability to look away: an open grave keeps the '
             'loss visible past the point most people would prefer to close it up and '
             'move on. Taurus is a sign built around holding, so this degree tests '
             'exactly that gift against the one thing that can never actually be held '
             "onto, a life that has ended. The widow's grief is not decorative here, it "
             "is the sign's whole orientation toward permanence meeting the one fact "
             'that permanence never wins against. There is real dignity in staying at '
             'the graveside rather than rushing the leaving.',
  'colors': 'A planet at this degree often carries an unusually honest relationship '
            'with loss, an unwillingness to perform recovery faster than it is '
            'actually happening. Saturn or the Moon here can indicate grief handled '
            'with real gravity, sometimes at cost to how quickly life expects a return '
            'to normal. It rewards letting mourning take the actual time it needs, '
            'rather than the time that is convenient.',
  'reflection': "What loss are you still standing at the edge of, refusing to close "
                "the grave before you're ready?"},
 {'degree': 6,
  'image': 'Workers build a bridge across a deep gorge.',
  'meaning': 'Connection, under construction, spanning a gap real enough that falling '
             'would matter. This degree is patient engineering applied to the problem '
             'of distance, the two sides of the gorge staying exactly where they are '
             'while the bridge does all the work of bringing them together. Taurus, so '
             'identified with solid ground, here builds the one structure that has to '
             "trust open air for most of its length before it's finished. Nothing "
             'about a bridge like this gets built quickly, it is planted pier by pier, '
             'over time, until crossing becomes possible instead of a leap of faith.',
  'colors': 'A planet at this degree often shows real capacity to build connection '
            'across a genuine, sometimes dangerous, distance, whether between people, '
            'ideas, or two versions of a life. Saturn here favors patient, '
            'structurally sound work that eventually makes an impossible crossing '
            'ordinary. It rewards trusting the slow, engineered approach over any '
            'shortcut across the gorge.',
  'reflection': "What bridge are you still building, pier by pier, that isn't "
                'finished enough yet to cross?'},
 {'degree': 7,
  'image': 'A woman of Samaria draws water at the ancestral well.',
  'meaning': 'An old story, stripped to its essential image: a woman comes to a well '
             'her people have used for generations, for the plainest of reasons, '
             'because she is thirsty and the well is where water is. This degree '
             "honors ritual that has outlasted anyone's memory of why it started, the "
             'well still doing its one job across centuries because thirst never stops '
             'recurring. Taurus, a sign built on continuity, finds here an image of '
             'exactly that: inherited resource, still reliably giving what it always '
             'gave, met by someone who needs it right now rather than as history.',
  'colors': 'A planet at this degree often draws on resources or traditions inherited '
            'from far earlier than the self, tapping something ancestral for a need '
            'that is entirely present-tense. The Moon or the fourth house here can '
            'indicate real sustenance found in family or lineage, water that was there '
            'before you arrived and will be there after. It rewards going to the old '
            'well instead of only ever digging new ones.',
  'reflection': "What ancestral well are you still allowed to draw from, that you've "
                'been meaning to visit again?'},
 {'degree': 8,
  'image': 'A sleigh sits on bare ground, the snow already gone.',
  'meaning': 'A vehicle built for one specific condition, stranded once that condition '
             'changes. This degree is about timing that slipped, equipment that is not '
             'wrong so much as no longer matched to the season it is actually in. '
             "There's no shame in the image, only a plain mismatch: the sleigh did "
             'nothing wrong, the snow simply left before it was used. Taurus, so '
             'oriented toward the reliable and the seasonal, meets here its own risk, '
             'preparing well for a world that changes anyway, on its own schedule, '
             'without waiting for consent.',
  'colors': 'A planet at this degree can indicate real preparation that arrived a '
            'little out of step with circumstance, tools or plans built for '
            'conditions that shifted before they could be used. Saturn here often '
            'shows someone learning to adapt equipment, or timing, faster than they'
            "'d prefer. It rewards checking the ground before assuming the old plan "
            'still fits it.',
  'reflection': 'What have you kept ready for a season that has already quietly '
                'ended?'},
 {'degree': 9,
  'image': 'A fully decorated Christmas tree.',
  'meaning': 'Abundance, deliberately assembled: nothing on this tree arrived by '
             'accident, every ornament placed by someone who wanted the whole effect '
             'to be complete. This degree is Taurus at its most openly festive, taking '
             'real pleasure in accumulation done well, in a display that exists purely '
             "to be beautiful and shared. There's craft in it too, not just quantity, "
             'a fully decorated tree is the result of care, layer by layer, until '
             'abundance itself becomes the art. Where degree four chased treasure that '
             'kept receding, this one simply has the treasure, hung and lit and '
             'finished.',
  'colors': 'A planet at this degree often shows a genuine gift for gathering and '
            'arranging abundance so it can be enjoyed by everyone in the room, not '
            'hoarded privately. Venus here favors real skill at making a shared space '
            'feel rich and celebratory. It rewards trusting that some abundance exists '
            'purely to be displayed and given away with pleasure.',
  'reflection': "What have you finished decorating, fully, that you haven't yet let "
                'anyone else come see?'},
 {'degree': 10,
  'image': 'A Red Cross nurse.',
  'meaning': 'Care, professionalized and ready wherever it is needed, without waiting '
             'to be personally acquainted with the person in front of her. This degree '
             "turns Taurus's instinct to tend and steady into something disciplined, a "
             'skill trained specifically so it can be trusted in an emergency rather '
             'than only offered casually among friends. The uniform matters here, it '
             'signals competence the same moment it signals compassion, so help '
             'arrives credible as well as kind. Nothing about this care is '
             "sentimental, it is useful, exactly when useful is what's required.",
  'colors': 'A planet at this degree often carries real, trained capacity to steady '
            'other people in crisis, a calm that has been practiced rather than only '
            'felt. Saturn or the Moon here can indicate someone who becomes genuinely '
            'more competent the more urgent the situation gets. It rewards taking that '
            'capacity seriously enough to formalize it, rather than leaving it as '
            'instinct alone.',
  'reflection': 'Where has your instinct to help already become a real, trainable '
                'skill, if you gave it the discipline to match?'},
 {'degree': 11,
  'image': 'A woman waters the flowers in her garden.',
  'meaning': 'Small, daily tending, aimed at something that is already alive and only '
             'needs steady attention to keep thriving. This degree is unglamorous by '
             'design: no dramatic rescue, just a woman with a watering can, doing the '
             'same modest task on the same modest schedule, because that is what '
             "growing things actually require. Taurus's whole philosophy sits inside "
             'this image, that most flourishing is not achieved in a single grand '
             'gesture but maintained, patiently, in a hundred small ones nobody '
             'applauds.',
  'colors': 'A planet at this degree often shows real skill at sustaining something '
            'over time through unremarkable, consistent care rather than occasional '
            'bursts of attention. Venus here favors a garden, literal or otherwise, '
            'that is genuinely well tended. It rewards trusting the daily watering can '
            'over any single dramatic effort.',
  'reflection': 'What have you been watering steadily, in small unglamorous amounts, '
                'that is quietly thriving because of it?'},
 {'degree': 12,
  'image': 'A young couple walks along a street, window-shopping.',
  'meaning': 'Desire, browsed rather than bought: two people looking at what they '
             'might someday want, together, with no transaction actually happening '
             'yet. This degree is Taurus enjoying appetite itself, the pleasure of '
             'imagining ownership before any of it is real, comparing tastes with '
             'someone else and finding out, glass pane by glass pane, whether those '
             "tastes actually align. There's something tender in it too, a "
             'relationship testing its shared future through what it admires rather '
             'than what it commits to yet.',
  'colors': 'A planet at this degree often shows real pleasure taken in possibility '
            'and shared taste, sometimes well ahead of any actual acquisition. Venus '
            'here can indicate a relationship, or a self, that enjoys wanting things '
            'together as much as having them. It rewards letting some desires stay in '
            'the window a while before deciding which ones you actually walk in for.',
  'reflection': 'What are you and someone you love still window-shopping for, and is '
                'it time to go in, or is the looking still doing its work?'},
 {'degree': 13,
  'image': 'A porter carries heavy baggage.',
  'meaning': "Someone else's weight, taken on as a job. This degree is service "
             "rendered through the body, strength offered specifically so another "
             "person doesn't have to strain under what they're carrying. There is "
             "dignity in the porter's work and a clear boundary too, the baggage is "
             'real and heavy, but it was never his to begin with, he sets it down at '
             'the destination and walks back for the next load. Taurus, so associated '
             'with physical endurance, finds here a use for that endurance that is '
             "entirely in service of somebody else's journey.",
  'colors': "A planet at this degree often carries a strong capacity to shoulder "
            "other people's burdens, sometimes literally, sometimes financially or "
            "emotionally, without those burdens becoming permanently the self's own. "
            'Saturn or Mars here can indicate real physical or practical reliability '
            'under load. It rewards remembering that carrying something well still '
            'means setting it down at the right stop.',
  'reflection': "Whose baggage are you currently carrying, and do you know exactly "
                "where you're supposed to set it back down?"},
 {'degree': 14,
  'image': "Children play on the beach while shellfish grope at the water's edge.",
  'meaning': 'Two entirely different kinds of life sharing the same narrow strip of '
             'shore, each going about its business without much awareness of the '
             'other. The children play in full daylight consciousness, the shellfish '
             'work along the tideline by instinct alone, blind and groping, doing '
             'exactly what shellfish do. This degree holds both without asking one to '
             'explain the other, a reminder that consciousness comes in very different '
             'depths even within the same small stretch of world. Taurus, grounded in '
             'the physical, gets an image here of how much life operates well below '
             'awareness and still belongs.',
  'colors': 'A planet at this degree often shows comfort holding both a fully '
            'conscious, playful part of life and a much more primal, instinctive '
            'layer running alongside it, without needing to resolve the two into one '
            'thing. Neptune or the Moon here can indicate real sensitivity to what '
            "moves along the edges, half seen. It rewards noticing what's groping at "
            'the waterline, even while the daylight play continues.',
  'reflection': 'What is working quietly along the edges of your life right now, '
                'mostly unseen, while you play in the open water above it?'},
 {'degree': 15,
  'image': 'A man in a rakish silk hat, muffled against the cold, braves a storm.',
  'meaning': 'Style, insisted on even when the weather has every right to ruin it. '
             'This degree is composure worn deliberately into difficult conditions, '
             'the hat rakish rather than merely practical, proof that the man refuses '
             'to let the storm dictate how he presents himself. There is real grit '
             'under the glamour, since braving a storm in fine dress is harder than '
             'braving it in something disposable, he has more to lose and goes out '
             'anyway. Taurus, so devoted to comfort, finds here its own steel, the '
             'choice to keep standards up precisely when conditions argue for letting '
             'them slip.',
  'colors': 'A planet at this degree often shows a real refusal to abandon personal '
            'style or standards under pressure, treating good presentation as a form '
            'of resilience rather than vanity. Venus or Saturn here can indicate '
            'someone who dresses, or shows up, especially well for the hardest '
            'occasions. It rewards keeping the hat rakish rather than trading it for '
            'something merely functional.',
  'reflection': 'What standard have you kept up, on purpose, in exactly the weather '
                'that would have excused you for dropping it?'},
 {'degree': 16,
  'image': 'An old teacher fails to interest the pupils in traditional knowledge.',
  'meaning': 'Wisdom offered in good faith, and simply not received, at least not '
             'this time, not by this room. This degree does not blame the teacher or '
             'the students outright, it just names the gap, tradition on one side, '
             'attention on the other, and the honest fact that transmission sometimes '
             'fails no matter how real the material is. Taurus, which trusts what has '
             'endured, meets here the limit of endurance alone: a thing being old and '
             'true does not guarantee anyone in the room is ready to hear it yet.',
  'colors': 'A planet at this degree can indicate real, valuable knowledge that keeps '
            'meeting audiences not yet ready for it, teaching offered faithfully into '
            'a room that has not caught up. Saturn or Mercury here often shows someone '
            'who has learned to keep teaching anyway, trusting that timing, not '
            'content, is usually the actual problem. It rewards patience with the gap, '
            'rather than resentment of it.',
  'reflection': "What true thing have you kept offering to a room that isn't ready "
                'yet, and are you still willing to say it when it finally is?'},
 {'degree': 17,
  'image': 'A pitched battle between swords and torches.',
  'meaning': 'Two very different weapons, meeting in the same fight: the blade that '
             'cuts and the flame that burns and illuminates at once. This degree is '
             'conflict between methods as much as sides, force against force, but a '
             'different kind of force each time, steel logic against something closer '
             'to fire and revelation. Taurus rarely seeks battle, but this degree '
             "shows it can't always be avoided, and that even a peace-loving sign has "
             'its version of swords and torches when something essential is actually '
             'being contested.',
  'colors': 'A planet at this degree often shows real capacity to fight for what '
            'matters using a distinct, sometimes unconventional weapon, illumination '
            'rather than only force, or force rather than only persuasion. Mars here '
            'can indicate a fighter who brings something sharper, or something that '
            'reveals, rather than simply outmuscling the other side. It rewards '
            'knowing which weapon, sword or torch, the moment actually calls for.',
  'reflection': "In the battle you're currently in, are you reaching for the sword "
                'or the torch, and is it the right one?'},
 {'degree': 18,
  'image': 'A woman airs an old bag out through a sunny open window.',
  'meaning': 'Something that has been closed and carried finally gets opened to the '
             'light, not thrown out, just aired. This degree is gentle maintenance '
             "applied to what's been held onto for a while, the recognition that even "
             'things worth keeping need to be brought into fresh air occasionally or '
             'they start to smell of their own closed history. Taurus, a sign that '
             'holds on, gets here a lesson in holding well: keep the bag, but open the '
             'window sometimes.',
  'colors': 'A planet at this degree often shows a healthy instinct to periodically '
            'revisit and refresh what has been stored away rather than either '
            'discarding it or leaving it permanently sealed. The Moon here can '
            'indicate emotional material that benefits enormously from being aired '
            'out in daylight instead of kept shut in the dark. It rewards choosing '
            'the sunny window over either extreme, throwing away or keeping shut '
            'forever.',
  'reflection': 'What old bag of yours is overdue for a sunny window, not to empty '
                'it, just to let it breathe?'},
 {'degree': 19,
  'image': 'A new continent rises out of the ocean.',
  'meaning': 'Ground that did not exist yesterday, surfacing all at once from what '
             'was previously only water. This is the most dramatic image Taurus '
             'offers for the thing it usually gets slowest and steadiest, new '
             'territory, arriving here instead in a single geological event. There is '
             'nothing gradual about it, which makes the degree feel almost un-Taurus, '
             'except that what rises stays, the whole point of new land is that once '
             "it's up, it's solid, permanent, ready to be built on. Sudden and "
             'lasting are not actually opposites here.',
  'colors': 'A planet at this degree often shows real capacity for sudden, '
            'large-scale new beginnings that, unlike most quick starts, actually '
            'last and can be built on. Uranus or Jupiter here can indicate a '
            'life-changing opportunity or territory that appears abruptly and then '
            'simply stays. It rewards trusting solid ground even when it arrived '
            'faster than solid ground usually does.',
  'reflection': 'What new ground has recently risen in your life, solid enough now '
                'to actually build on?'},
 {'degree': 20,
  'image': 'Wisps of wing-shaped cloud stream across the sky.',
  'meaning': 'Beauty that exists only because it is already leaving: the clouds are '
             'shaped like wings for the length of a glance, then the wind reshapes '
             'them into something else entirely. This degree asks Taurus, the sign '
             'most invested in permanence, to appreciate something built entirely '
             'from transience, haste made visible and, briefly, gorgeous. There is '
             'real wisdom offered here, that not everything valuable needs to stay '
             'put to be worth noticing, some things are exactly as valuable as their '
             'speed allows.',
  'colors': 'A planet at this degree often shows an unusual comfort with quick '
            'change for a sign that typically resists it, real adaptability when a '
            'moment demands fast, graceful movement. Mercury or Uranus here can '
            'indicate a mind that thinks fastest, and most beautifully, in '
            'transitional or crisis moments. It rewards noticing beauty in what is '
            'already passing, rather than only in what stays.',
  'reflection': 'What is streaming past you right now, wing-shaped and brief, that '
                "is worth watching closely before it becomes something else?"},
 {'degree': 21,
  'image': 'A finger points to a significant passage in an open book.',
  'meaning': 'Someone has already done the underlining work: out of every page and '
             'paragraph available, one line has been singled out as the one that '
             'matters right now. This degree is guidance made simple and specific, '
             'not a whole library handed over, just the exact passage the moment '
             'calls for. Taurus values what is concrete and usable, and this degree '
             'delivers precisely that, meaning distilled down to one legible line '
             'instead of scattered across an entire volume.',
  'colors': 'A planet at this degree often shows real skill at finding, or '
            'receiving, the one relevant piece of information inside a much larger '
            'body of material. Mercury or Jupiter here can indicate a gift for '
            'teaching or research that locates exactly the passage a person actually '
            'needs. It rewards trusting the pointing finger instead of insisting on '
            'reading the whole book yourself.',
  'reflection': 'What passage has already been pointed out to you, clearly, that you '
                "still haven't let yourself fully read?"},
 {'degree': 22,
  'image': 'A white dove flies over troubled waters.',
  'meaning': 'Peace, airborne above conditions that are anything but peaceful: the '
             'water underneath is genuinely rough, and the dove crosses it anyway, '
             'untouched by the turbulence it is flying over. This degree separates '
             'the condition of the world from the condition of the self crossing it, '
             "proof that calm doesn't require calm surroundings, only enough height "
             'to stay above the worst of the churn. Taurus, so rooted in the ground, '
             'finds here an image of staying serene without ever needing to touch '
             'down in the chaos.',
  'colors': 'A planet at this degree often shows a genuine ability to remain '
            'unruffled while conditions around it are turbulent, carrying a kind of '
            "peace that doesn't depend on external calm. Neptune or Venus here can "
            'indicate a person who becomes a literal source of calm for others '
            'during real crisis. It rewards trusting that height, or distance, above '
            'the trouble instead of diving straight into it.',
  'reflection': 'What troubled water are you currently flying over, peacefully, and '
                'who below might need to see that it is possible?'},
 {'degree': 23,
  'image': 'A jewelry shop filled with magnificent gems.',
  'meaning': "Value, concentrated and on display: nothing in this room pretends to "
             "be anything other than precious, and there's a lot of it, gathered in "
             'one place for anyone with the means and the eye to appreciate it. This '
             "degree is Taurus's love of worth taken to its most literal extreme, "
             'beauty that has also been assigned a price, admired for both reasons at '
             'once without embarrassment. There is a discipline hidden in a shop like '
             'this too, since not every stone gets purchased, looking, appraising, '
             'and choosing are their own skill.',
  'colors': 'A planet at this degree often shows a genuine, refined appreciation for '
            'real quality and value, sometimes material, sometimes simply an eye for '
            "what's actually excellent versus merely showy. Venus here is especially "
            "at home, favoring taste that recognizes the finest thing in the room. "
            "It rewards developing real discernment, not just an appetite for "
            "glitter.",
  'reflection': 'What in your life is genuinely a jewel, and have you actually '
                'appraised it, or just assumed the shine?'},
 {'degree': 24,
  'image': 'A mounted warrior rides fiercely into battle, trophies of past victories '
           'hanging at his belt.',
  'meaning': "This is one of the sign's fiercest images, a rider fully committed to "
             'conquest, wearing the evidence of past victories openly rather than '
             'hiding them. There is nothing gentle about this degree, and it is not '
             'meant to be, it names the part of Taurus that will fight hard, and '
             'visibly, for territory and standing once those things are genuinely '
             'threatened. The trophies at his belt are not decoration, they are a '
             'record, proof that this particular fight has been fought and won '
             'before.',
  'colors': 'A planet at this degree often shows real willingness to fight openly, '
            'and successfully, for territory, status, or resources once they are '
            'actually contested. Mars here can indicate a fierce, unapologetic '
            'defender of what has already been earned. It rewards knowing the '
            'difference between defending real ground and simply looking for a '
            'fight.',
  'reflection': 'What ground have you already fought for and won, that you are '
                'allowed to claim without apologizing for the fight it took?',
  'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
          'picture above keeps its meaning in respectful, modern terms.'},
 {'degree': 25,
  'image': 'A large, well-kept public park.',
  'meaning': 'Beauty maintained for everyone, not fenced off for the few who can '
             'afford private grounds. This degree is generosity built into '
             'infrastructure, land set aside and tended specifically so it can be '
             'shared, walked through, and enjoyed without a ticket or an invitation. '
             "Taurus's love of comfort and pleasure expands here past the personal, "
             "into something communal, proving the sign's appetite for good living "
             "doesn't have to be private to be real.",
  'colors': 'A planet at this degree often shows genuine investment in shared, '
            'public forms of beauty and comfort, resources tended not just for '
            'personal enjoyment but for a wider community. Venus or Jupiter here can '
            'indicate real generosity expressed through creating or maintaining '
            'something everyone gets to use. It rewards remembering that well-kept, '
            'shared ground is its own form of wealth.',
  'reflection': 'What have you helped keep well tended for others to enjoy, whether '
                'or not your own name is on it?'},
 {'degree': 26,
  'image': 'A Spaniard serenades his señorita.',
  'meaning': 'Romance, performed openly and with real craft, a specific song for a '
             'specific person, sung where it can actually be heard. This degree is '
             'courtship treated as an art form, effort made visible on purpose '
             'because the whole point is for the beloved to know exactly how much '
             'was put into the gesture. Taurus, ruled by Venus, gets one of its '
             'purest expressions here, love expressed through beauty, music, and '
             'unmistakable, undisguised devotion.',
  'colors': 'A planet at this degree often shows a real talent for romantic '
            'expression, courtship carried out with genuine artistry rather than '
            'left implied or assumed. Venus here is especially at home, favoring '
            'gestures of love that are deliberate, beautiful, and meant to be '
            'witnessed. It rewards not being shy about the serenade.',
  'reflection': 'Who deserves your version of a serenade right now, sung loud enough '
                'for them to actually hear it?'},
 {'degree': 27,
  'image': 'An elderly woman sells handmade beads at a roadside stand.',
  'meaning': 'Small commerce, carried out by someone with decades of practice at '
             'exactly this trade, offering handmade, meaningful goods for whatever a '
             'passerby can pay. This degree honors craft that has been kept alive '
             'across a long life and possibly a long lineage, dignity intact even '
             'when the setting is modest and the stakes are small. Taurus values '
             "what is made by hand and what endures, and this degree shows both at "
             'once, an elder still doing the work, still trading it fairly.',
  'colors': 'A planet at this degree often shows real respect for small-scale, '
            'handmade commerce and the long experience behind it, valuing the maker '
            'as much as the object made. Saturn or Venus here can indicate someone '
            'whose worth was built slowly, trade by trade, over a very long time. It '
            'rewards paying full price for what took a lifetime to learn how to '
            'make.',
  'reflection': 'What have you been quietly making and trading for a long time, that '
                'deserves to be valued at its real worth?',
  'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
          'picture above keeps its meaning in respectful, modern terms.'},
 {'degree': 28,
  'image': 'A mature woman is unexpectedly pursued by new romance.',
  'meaning': 'Love, arriving after the point most people assume it is finished '
             'arriving. This degree refuses the idea that romance belongs only to '
             'youth, insisting instead that desire and being desired can return at '
             'any age, sometimes precisely when a person has stopped waiting for it. '
             'There is real vindication in the image, since being pursued implies '
             "someone else did the noticing first, she didn't have to go looking, "
             'life simply decided she was still very much worth wanting.',
  'colors': 'A planet at this degree often shows real capacity for renewal, '
            'especially in matters of love, well past whatever age convention '
            'suggested that door had closed. Venus here can indicate a second, '
            'sometimes better, chapter of romance arriving on its own timing. It '
            'rewards staying open to being pursued, rather than assuming that season '
            'already ended.',
  'reflection': 'What door did you quietly assume was closed, that might still be '
                'very much open to being knocked on?'},
 {'degree': 29,
  'image': 'Two cobblers work at a table.',
  'meaning': 'Skilled labor, shared side by side rather than performed alone, two '
             'craftspeople doing the same trade at the same table without needing to '
             "compete over it. This degree is Taurus's respect for real work "
             'distilled into companionship, the quiet solidarity of people who '
             "understand exactly how hard the other person's job is because it is "
             'also their own. There is comfort in working next to someone who does '
             'not need the process explained.',
  'colors': 'A planet at this degree often shows real ease working alongside others '
            'in the same trade, finding companionship in shared skill rather than '
            'rivalry over it. Venus or the sixth house here can indicate genuinely '
            'satisfying collegial work, craft practiced in good company. It rewards '
            'seeking out the table where someone else already understands the work '
            'you do.',
  'reflection': 'Who is sitting at your table, doing the same patient work you do, '
                'and have you let that be companionship instead of comparison?'},
 {'degree': 30,
  'image': 'A peacock parades on the terrace of an old castle.',
  'meaning': 'The final degree of Taurus closes on pure, unapologetic display, '
             'beauty shown off against a backdrop that has stood for centuries, as '
             "if to prove that ornament and permanence are not actually in conflict. "
             "The peacock does not need the castle's approval to strut, and the "
             "castle does not need the peacock's color to remain impressive, each "
             'simply makes the other more striking by proximity. After thirty '
             'degrees of accumulating worth, patience, and resource, Taurus ends by '
             'finally, openly showing it off, no apology, full plumage, on ground '
             'old enough to hold the display.',
  'colors': 'A planet at this degree often shows a well-earned comfort with visible '
            'display, beauty or achievement shown openly rather than modestly '
            'hidden, especially once real, lasting foundation is already in place. '
            'Venus or the Sun here can indicate someone who has built enough of '
            'substance to finally let the show happen without guilt. It rewards '
            'remembering that showing off, on solid enough ground, is not vanity, it '
            'is simply the truth on display.',
  'reflection': 'What have you built solidly enough, finally, that you are allowed '
                'to parade it instead of quietly hiding it?'}]

assert len(ENTRIES) == 30, f"expected 30 Taurus degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Taurus degrees out of order"
