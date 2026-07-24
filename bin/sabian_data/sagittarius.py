"""Sabian symbol data for Sagittarius.

See bin/sabian_data/SCHEMA.md for the full field-by-field schema, the
canonical 12-sign order, and the procedure for adding a new sign.

CORRECTNESS: the degree->symbol mapping (the `image` field on each entry)
is the canonical Jones/Wheeler 1925 Sabian symbol, one per whole zodiac
degree, numbered 1-30 within the sign. It was cross-verified against four
independent, mutually agreeing published sources (kerykeion.net's
"foundation-sabian-sagittarius" page, astronarrative.com's
"sagittarius.html" -- which labels on the "N-1 to N" convention, e.g. its
"1-2" is this file's degree 2, checked across the offset the same way as
Virgo's file -- jamesburgess.com / Sacred 7 Academy's "sagittarius-sabians"
list, and yourtango.com's Sabian symbols explainer, which independently
reproduces the same full-sentence Rudhyar-register wording) before being
hand-typed. Degrees 1 and 22 were additionally spot-checked against
sabian-calculator.com's per-degree pages, and degree 22 further confirmed
against boveeastrology.com's dedicated "A Chinese laundry" archive entry.
Do NOT extend this list, or write a new sign's list, without the same
verification discipline: fewer verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "two men play a
long game of chess"), not a verbatim quote of Marc Edmund Jones' 1953 book
or Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation,
written fresh for this project; none of it is copied from Jones or
Rudhyar.

DATED IMAGERY: Sagittarius 22's 1925 original is "A Chinese laundry," a
symbol tied to a specific ethnicity via an occupational stereotype from
early-20th-century America. Per Shannon's standing policy, the canonical
mapping is kept, but `image` restates it respectfully without the ethnic
label (focusing on the underlying theme of building a foothold in a new
land through inherited skill and hard work), and a `note` field is
attached below the symbol card. See SCHEMA.md for the full policy. Two
other degrees were checked carefully and judged NOT to meet this bar:
degree 1 ("A Grand Army of the Republic campfire," a U.S. Civil War
veterans' organization) is a period-specific historical reference, not an
ethnic stereotype; degree 23 ("Immigrants entering," i.e. a group of
immigrants fulfilling entrance requirements into a new country) names no
specific ethnicity and carries no stereotype. Neither received a `note`.
"""

# Per-sign metadata. `order` is this sign's 1-12 position in the zodiac
# wheel (Aries=1 ... Pisces=12), used to sort the hub and sign navigation.
# `glyph` carries a trailing U+FE0E (VS15, text presentation selector) so
# it renders as a plain colorable glyph instead of Apple Color Emoji's
# fixed multicolor badge -- see gen_sabian_pages.py for the full rationale.
# Do not remove the VS15 suffix.
SIGN = {"name": "Sagittarius", "slug": "sagittarius", "glyph": "♐︎", "order": 9}

# The 30 degrees of Sagittarius, in order 1-30. Each entry is a dict with
# the fields: degree (int 1-30), image (str), meaning (str), colors (str),
# reflection (str), and (only on degree 22) note (str). See SCHEMA.md for
# what each field means.
ENTRIES = [
    {'degree': 1,
     'image': 'Old soldiers gather at a reunion campfire, telling stories from a '
              'campaign long since decided.',
     'meaning': "This is the first degree of the entire sign, and it opens not with a "
                'fresh departure but with veterans looking backward, turning hard '
                "mileage into story. Sagittarius's real subject is never only the "
                'experience itself, it is the belief and the meaning built from that '
                'experience afterward, around a fire, for whoever is close enough to '
                'hear it. The war is over, the fire is small, but the retelling is '
                'still real work: it is how a hard campaign becomes something '
                'instructive rather than just something survived.',
     'colors': 'A planet at Sagittarius 1 often carries hard-won conviction, the kind '
               'that only sounds simple because the story has been shaped by retelling '
               'many times over. Jupiter or Saturn here can indicate someone who did '
               'the actual campaign and has earned the standing to hold a settled '
               'opinion about it. The Sun here favors a reputation built more on lived '
               'history than on raw talent alone.',
     'reflection': 'What old campaign of yours has become a story worth passing on, and '
                   'who still needs to hear it?'},
    {'degree': 2,
     'image': 'A brisk wind stirs the open sea into scattered, restless whitecaps.',
     'meaning': "Restlessness given visible shape: the wind doesn't ask the ocean's "
                'permission, it simply moves it, and the whole surface answers at once. '
                "This is Sagittarius's native appetite for motion, meeting the vast, "
                'indifferent scale it actually likes testing itself against. Nothing '
                'about a single whitecap lasts, it rises, catches the light, and folds '
                'back under, but the sea in that moment is unmistakably, restlessly '
                'alive.',
     'colors': 'A planet at this degree often shows restless energy that needs a '
               'genuinely large field to move across, since small ponds will not hold '
               'it. Mars or Uranus here favors someone who only really feels like '
               'themselves once conditions get a little unpredictable. It rewards '
               'trusting motion that looks chaotic from the shore but is, up close, '
               'simply the sea being itself.',
     'reflection': 'What in your life has been stirred up lately that was actually '
                   'overdue for some real wind?'},
    {'degree': 3,
     'image': 'Two men, at ease in an old study, settle into a long, unhurried game of '
              'chess.',
     'meaning': 'Not a physical contest, this is a whole campaign fought entirely '
                'inside two minds trying to out-think each other several moves ahead. '
                'Sagittarius is often mistaken for a sign of pure impulse, but here it '
                'slows all the way down into strategy and the pleasure of a long, '
                'honest contest between equals. Every move is a small bet on a belief '
                "about how the other person thinks; the game only works because both "
                "players respect the rules enough to actually play it straight.",
     'colors': 'A planet at this degree often shows a mind that enjoys thinking several '
               'moves ahead, more drawn to the long strategic game than to any quick '
               'win. Mercury or Saturn here can indicate real skill at patient, honest '
               'contest, holding a plan long enough to see whether it actually works. '
               "It rewards a worthy opponent, since the game means little played "
               "against someone who won't really try.",
     'reflection': 'What long game are you currently playing, and are you actually '
                   "respecting your opponent enough to play it honestly?"},
    {'degree': 4,
     'image': 'A small child takes its first unsteady steps while its parents, wisely, '
              'hold back from helping.',
     'meaning': "The very first steps toward the far horizon this sign is famous for "
                'chasing start here, small, wobbling, entirely unglamorous. What makes '
                'the image work is the restraint of the parents, who understand that '
                'learning needs the fall as much as the step, and that help offered too '
                "soon would only rob the child of the actual lesson. Sagittarius's whole "
                'philosophy of freedom is contained in this early scene: real growth '
                'needs room to stumble, not a hand under every arm.',
     'colors': 'A planet at this degree often favors learning through direct, sometimes '
               'clumsy experience rather than being carried through it. Saturn or '
               'Jupiter here can indicate parents, mentors, or a whole approach to life '
               'that trusts the fall as part of the lesson. It rewards resisting the '
               'urge to over-help, in yourself or in whoever you are raising.',
     'reflection': 'Where have you been offered a hand you would actually grow more by '
                   'refusing?'},
    {'degree': 5,
     'image': 'An old owl perches alone, high in the branches of an ancient tree.',
     'meaning': "Wisdom, here, keeps its distance: the owl sits above the rest of the "
                'wood, solitary and patient, seeing further precisely because it is not '
                'down in the middle of things. Sagittarius eventually has to trade raw '
                'appetite for actual perspective, and this degree pictures exactly that '
                'trade, height and stillness in exchange for a wider view. The tree '
                'itself is old too, which matters, since this kind of seeing takes real '
                'years to earn a perch this high.',
     'colors': 'A planet at this degree often shows a genuinely long view, patience '
               'built from real accumulated years rather than borrowed opinion. Saturn '
               'or Jupiter here can indicate someone whose counsel is worth more for '
               'having watched quietly for a long time before speaking. It rewards '
               'trusting solitary observation as its own form of expertise.',
     'reflection': 'What have you seen clearly only because you were willing to sit '
                   'apart from the crowd long enough to actually look?'},
    {'degree': 6,
     'image': 'Players take the field for an unhurried, disciplined match of cricket.',
     'meaning': "A contest with real patience built into its own rules, played out over "
                'hours rather than settled in one dramatic swing. Sagittarius' + "'s "
                'competitive fire usually wants a fast resolution, but this degree '
                'insists that some real victories only arrive after a long, disciplined '
                'innings, sustained effort mattering more than any single lucky strike. '
                'There is real sportsmanship in the image too, a shared code both sides '
                'trust enough to play by for as long as the match actually takes.',
     'colors': 'A planet at this degree often favors sustained effort over a long '
               'contest rather than a single decisive move, stamina paired with genuine '
               'fair play. Mars or Saturn here can indicate real skill at pacing a long '
               'game correctly. It rewards trusting the whole innings, not just the '
               'flashy over.',
     'reflection': 'What long match are you currently in the middle of, that actually '
                   'needs your patience more than your urgency?'},
    {'degree': 7,
     'image': 'Cupid raps plainly at the door of a waiting heart.',
     'meaning': 'Longing here has a knock, not a subtle hint, an actual announcement '
                'that something is arriving whether the door is ready or not. '
                "Sagittarius's optimism about love is exactly this direct: a belief "
                'that the right thing eventually shows up and asks plainly to be let '
                'in, rather than sneaking past unnoticed. There is real vulnerability '
                'in an open door, but this degree trusts the knock is worth answering.',
     'colors': 'A planet at this degree often shows a genuinely direct, hopeful '
               'approach to love, arriving plainly rather than through indirect '
               'signals. Venus here favors real courage to answer the door instead of '
               'pretending not to hear the knock. It rewards trusting arrivals that '
               'announce themselves honestly.',
     'reflection': 'What knock at your door have you been pretending not to hear?'},
    {'degree': 8,
     'image': 'Deep underground, new mineral formations are quietly taking shape '
              'inside old rock.',
     'meaning': 'Nothing about this degree is visible from the surface, growth '
                'happening entirely out of sight, on a timescale that has nothing to do '
                'with human patience. Sagittarius chases the wide-open and the far '
                'horizon so often that it is easy to forget the sign also governs a '
                'slower, buried kind of becoming, belief and meaning crystallizing '
                'gradually under real pressure, long before anyone can see the result. '
                'What eventually gets unearthed here will be worth the wait precisely '
                'because it was not rushed.',
     'colors': 'A planet at this degree often shows real development happening '
               'privately, out of view, well before any outward sign of it shows. '
               'Pluto or Saturn here can indicate a belief system or a body of '
               'knowledge that has been forming quietly under pressure for a long '
               'time. It rewards trusting a process you cannot yet see the results of.',
     'reflection': 'What is currently forming in you, out of sight, that you will only '
                   'recognize once it is finally unearthed?'},
    {'degree': 9,
     'image': 'A mother leads her small children step by step up a steep staircase.',
     'meaning': 'Ascent, here, is a shared project, patient and deliberate, one small '
                'hand held at a time. This degree grounds ' + "Sagittarius's love of "
                'climbing toward something higher in the most ordinary possible scene, '
                'a parent making sure nobody gets left behind on a genuinely difficult '
                'flight of stairs. The height at the top matters less, for now, than '
                'the steady, careful pace it actually takes to get everyone there '
                'together.',
     'colors': 'A planet at this degree often shows real care taken to bring others '
               'along on a difficult climb, rather than simply reaching the top alone. '
               'The Moon or Saturn here can indicate a natural teacher or guide, '
               "someone who paces a hard ascent to the slowest person's steps. It "
               'rewards measuring your climb by who made it up with you.',
     'reflection': 'Who are you currently leading up a steep flight, one careful step '
                   'at a time?'},
    {'degree': 10,
     'image': 'On a stage, an actress plays a golden-haired goddess of opportunity, '
              'offering her gifts to whoever steps forward.',
     'meaning': "Opportunity, dramatized: this degree admits that luck often needs a "
                'little theater to actually be recognized and seized, a costume and a '
                'spotlight helping people believe the chance in front of them is real. '
                "Sagittarius's famous good fortune is not passive here, it is staged, "
                'presented, made vivid enough that someone actually has the nerve to '
                'walk up and take it. The goddess is played by an actress, not a deity, '
                'a reminder that opportunity usually needs a human being willing to '
                'perform the part of stepping forward.',
     'colors': 'A planet at this degree often shows real talent for recognizing and '
               'dramatizing a chance so that others, or the self, can actually see and '
               'take it. Jupiter or Venus here can indicate a gift for making '
               'opportunity feel vivid and available rather than abstract. It rewards '
               'playing your own part in the moment instead of waiting for the goddess '
               'to come find you off-stage.',
     'reflection': 'What opportunity is currently on stage in your life, waiting for '
                   'you to actually walk up and claim it?'},
    {'degree': 11,
     'image': 'In the left wing of an ancient temple, a lamp shaped like a human body '
              'burns steadily.',
     'meaning': "A very old fire, kept for a very specific purpose: enlightenment here "
                "isn't abstract or purely spiritual, it is housed inside something "
                'shaped exactly like a person, physical understanding lit and tended '
                "inside sacred walls. Sagittarius's search for meaning usually reaches "
                'upward and outward, toward doctrine and distant truth; this degree '
                'grounds that search back in the body, insisting real wisdom has to '
                'live somewhere physical to actually mean anything. The temple is '
                'archaic, and the flame has clearly been kept a very long time.',
     'colors': 'A planet at this degree often shows wisdom or belief that stays '
               'genuinely embodied, understanding carried in the body and not just '
               'held as abstract doctrine. Neptune or the Sun here can indicate someone '
               'whose spiritual insight shows up as physical vitality, or vice versa. '
               'It rewards tending the flame steadily rather than letting the temple '
               'go dark.',
     'reflection': 'What understanding have you kept burning quietly in your own body, '
                   'long after the doctrine around it went out of fashion?'},
    {'degree': 12,
     'image': 'A flag on its pole suddenly becomes a crowing eagle.',
     'meaning': 'A symbol becomes the actual thing it always stood for: cloth and '
                'color turn into feather and voice, announcement made suddenly, '
                'unmistakably alive. Sagittarius deals constantly in banners, ideals, '
                'causes worth rallying under, and this degree insists the ideal can '
                'genuinely become real, not just a decoration people salute out of '
                'habit. The crow at the end is the whole point, proof loud enough that '
                'no one in earshot can pretend not to have heard it.',
     'colors': 'A planet at this degree often shows a belief or cause that has stopped '
               'being merely symbolic and become something the person actually lives '
               'out loud. Jupiter or Uranus here can indicate real conviction that '
               'announces itself, unmistakably, rather than staying quietly decorative. '
               'It rewards trusting that your own flag might actually have a voice, if '
               'you let it.',
     'reflection': 'What ideal of yours has been hanging quietly on its pole, that '
                   'might be ready to actually crow?'},
    {'degree': 13,
     'image': "A widow's hidden past is uncovered and brought fully into the open.",
     'meaning': "Sagittarius trusts, on principle, that the truth eventually surfaces, "
                'and this degree hands the sign a genuinely difficult version of that '
                'faith: a private history, kept quiet out of grief or discretion, '
                "exposed regardless of whether its owner was ready. There is no "
                'cruelty required in the image, only inevitability, the sign\'s honest '
                'conviction that concealment has a shelf life. What gets revealed may '
                'complicate the mourning underway, but the degree trusts the fuller '
                'truth is still worth more than the comfortable, partial story.',
     'colors': 'A planet at this degree often shows real willingness to let an old, '
               'private history come to light, even at real emotional cost. Pluto or '
               'the Moon here can indicate someone whose past eventually gets known '
               'more fully than they originally intended. It rewards meeting the '
               'exposure honestly, rather than fighting a truth that has already '
               'decided to surface.',
     'reflection': 'What part of your own past is quietly due to come to light, '
                   'whether or not you are the one who chooses the moment?'},
    {'degree': 14,
     'image': 'The Great Pyramids stand beside the watching Sphinx.',
     'meaning': 'Two kinds of monument, side by side, one built entirely to be '
                'understood and one built specifically to keep a riddle. This degree '
                "honors Sagittarius's real relationship to ancient wisdom: some of it "
                'is architecture you can walk into and measure, and some of it is a '
                'question that has outlasted every attempt to answer it definitively. '
                'The sign that wants to know everything meets, here, a structure that '
                'has survived thousands of years by refusing to fully explain itself.',
     'colors': 'A planet at this degree often shows a genuine draw toward ancient '
               'knowledge, both the kind that can be studied directly and the kind '
               'that stays deliberately mysterious. Saturn or Neptune here can indicate '
               'real reverence for what has endured across enormous stretches of time. '
               'It rewards respecting the riddle instead of insisting on solving it.',
     'reflection': 'What old question in your own life has earned the right to stay a '
                   'little unsolved?'},
    {'degree': 15,
     'image': 'On Groundhog Day, a groundhog emerges from its burrow to look for its '
              'shadow.',
     'meaning': 'The midpoint of Sagittarius, and the whole sign\'s relationship to '
                'forecasting gets a small, folkloric test: a creature that reads its '
                'own shadow to predict how much winter is left. There is real humility '
                'in the ritual, since the groundhog does not actually control the '
                'season, it only reads the available sign and reports back. Sagittarius '
                'loves a confident prediction, and this degree keeps that appetite '
                'honest by tying it to something as plain and checkable as whether the '
                'sun happened to be out that morning.',
     'colors': 'A planet at this degree often shows a genuine gift for reading early '
               'signs and forecasting what is coming, held with appropriate humility '
               'about how much is actually in anyone\'s control. Mercury or the Moon '
               'here can indicate someone whose predictions are taken seriously '
               'precisely because they do not overclaim. It rewards checking your own '
               'forecast against the actual weather instead of your hopes for it.',
     'reflection': 'What shadow have you been reading lately to predict how much '
                   'longer your own winter is going to last?'},
    {'degree': 16,
     'image': 'Gulls circle and trail a ship, watching for whatever it gives up.',
     'meaning': "Opportunism, here, is a survival skill rather than a flaw: the gulls "
                'have not done any of the work of the voyage, but they have learned '
                "exactly where to be when the ship's business produces something worth "
                "having. Sagittarius's optimism about the world providing is met, in "
                'this degree, by a more practical cousin, the instinct to actually '
                'position yourself where the provision is likely to show up. Nothing '
                'about following the ship is dishonest, it is simply reading where the '
                'real activity is and staying close to it.',
     'colors': 'A planet at this degree often shows a practical instinct for staying '
               'near wherever real opportunity or resource is actively being '
               'generated. Mercury or Jupiter here can indicate someone who reads a '
               'situation correctly enough to be in the right place when something '
               'valuable surfaces. It rewards trusting your own read on where the ship '
               'is actually headed.',
     'reflection': 'What ship have you positioned yourself near, trusting that staying '
                   'close to real activity will eventually pay off?'},
    {'degree': 17,
     'image': 'A crowd gathers on a hillside at dawn for an Easter sunrise service.',
     'meaning': 'Faith, here, gets up early and climbs to a real vantage point to meet '
                'the light directly, rather than waiting for a more convenient hour '
                "indoors. This degree is Sagittarius's spiritual appetite at its most "
                'communal and most literal, a whole crowd choosing to be present for '
                'the exact moment belief and daybreak arrive together. There is real '
                'effort in the gathering, the climb, the early hour, that makes the '
                'eventual light feel earned rather than simply given.',
     'colors': 'A planet at this degree often shows genuine devotion expressed through '
               'shared ritual and real physical effort, not just private belief held '
               'quietly. Jupiter or the Sun here can indicate someone who draws real '
               'meaning from being present, in a crowd, for a significant threshold '
               'moment. It rewards showing up early for what actually matters to you.',
     'reflection': 'What dawn have you been meaning to actually show up for, instead '
                   'of just believing in from further off?'},
    {'degree': 18,
     'image': 'Small children play on the beach, their heads shaded by wide '
              'sunbonnets.',
     'meaning': 'Protection and freedom share the same scene here: the children get '
                "the whole beach to run in, and the bonnets make sure the sun's "
                "generosity doesn't turn into harm. Sagittarius loves wide-open space "
                'and unstructured play, and this degree quietly insists that real '
                'freedom is best enjoyed with just enough sensible shelter built in. '
                'Nothing about the bonnets restrains the play, they simply make the '
                'whole afternoon last longer.',
     'colors': 'A planet at this degree often shows real enjoyment of open, expansive '
               'freedom, paired with just enough sensible protection to sustain it. '
               'Venus or the Moon here can indicate someone who has learned to build '
               'simple safeguards into their biggest adventures rather than treating '
               'caution as the opposite of fun. It rewards packing the bonnet before '
               'you actually need it.',
     'reflection': 'What wide-open freedom in your life would last a lot longer with '
                   'one small, sensible piece of shelter built in?'},
    {'degree': 19,
     'image': 'A colony of pelicans, crowded out by human activity along the shore, '
              'relocates together to a new stretch of coast.',
     'meaning': "Sometimes the far horizon isn't chosen for adventure, it is chosen "
                'because the old ground has actually become unlivable. This degree '
                "gives Sagittarius's instinct to move on a harder edge, relocation not "
                'as romance but as a genuinely necessary response to a place that has '
                'stopped working. There is real resilience in the choice, no grievance '
                'dwelt on, just a whole colony finding the next viable shore and '
                'getting on with living there.',
     'colors': 'A planet at this degree often shows a real capacity to leave a '
               'depleted situation cleanly, without excessive mourning, and find '
               'workable ground elsewhere. Uranus or Saturn here can indicate someone '
               'whose moves are practical responses to real conditions rather than '
               'pure wanderlust. It rewards trusting your own read that a place has '
               'actually stopped supporting you.',
     'reflection': 'What ground in your life has quietly become unlivable, that you '
                   'have permission to simply leave for better shore?'},
    {'degree': 20,
     'image': 'In an old northern village, men cut blocks of ice from a frozen pond to '
              'store away for summer.',
     'meaning': "Provision, here, is planned a full season ahead: the pond is coldest "
                'and hardest exactly when it is least convenient to work it, and the '
                "whole point is stocking up for a warmth that hasn't arrived yet. "
                'Sagittarius trusts the future in the abstract, but this degree asks '
                'for the harder, more practical version of that trust, real labor done '
                "now for a benefit that won't be needed or felt for months. Nothing "
                'about cutting ice in winter is glamorous, but the summer only stays '
                'comfortable because someone did this cold work on time.',
     'colors': 'A planet at this degree often shows real discipline around '
               'provisioning ahead, doing the unglamorous work now for a need that has '
               'not arrived yet. Saturn here is especially at home, favoring practical '
               'foresight over abstract optimism alone. It rewards trusting the cold '
               "labor as much as you trust the summer it's actually for.",
     'reflection': 'What ice are you currently cutting, unglamorously, for a summer '
                   "comfort you won't actually feel the benefit of for months?"},
    {'degree': 21,
     'image': 'A child and a dog both peer through a pair of borrowed eyeglasses.',
     'meaning': 'Neither one of them actually needs the prescription, but both are '
                'curious enough to try on a different way of seeing anyway. This '
                "degree is Sagittarius's appetite for new perspective at its most "
                "playful, trying on a lens that isn't yours just to find out what the "
                'world looks like from inside it. There is real comedy in the image, '
                "and a real point too, understanding sometimes starts exactly this "
                "casually, borrowing someone else's exact vantage point for a minute "
                'before handing it back.',
     'colors': "A planet at this degree often shows real curiosity about how the world "
               "looks through someone else's exact point of view, tried on playfully "
               'rather than adopted permanently. Mercury or Uranus here can indicate a '
               'gift for temporarily seeing through a lens that is not native to you. '
               "It rewards trying on the borrowed glasses before deciding your own "
               'prescription is the only right one.',
     'reflection': "Whose exact point of view have you been curious enough to actually "
                   'try on lately, even briefly?'},
    {'degree': 22,
     'image': 'In a new land, a small laundry business built on inherited skill and '
              'unrelenting hours keeps its doors open long after the street outside '
              'has gone quiet.',
     'meaning': "Sagittarius is often read as pure outward motion, but this degree "
                "shows what the sign's real optimism looks like once it has actually "
                'landed somewhere foreign and has to build a life from scratch. '
                'Nothing here is romantic, the hours are long and the work is '
                'repetitive, but there is real dignity in taking whatever skill and '
                'background you arrived with and turning it, patiently, into a genuine '
                "foothold. This is the far horizon's unglamorous aftermath: having "
                'actually arrived, and doing the steady work of belonging.',
     'colors': 'A planet at this degree often shows a genuine capacity to build real '
               'security in unfamiliar territory, using whatever background or skill '
               'is actually on hand rather than waiting for ideal conditions. Saturn '
               'or Venus here can indicate someone who thrives precisely by adapting '
               'steadily rather than by force. It rewards respecting the quiet, '
               'unglamorous labor that most real belonging is actually built from.',
     'reflection': 'What foothold have you built for yourself in unfamiliar territory, '
                   'using nothing more than what you actually brought with you?',
     'note': 'Note: the 1925 original for this degree used dated ethnic imagery; the '
             'picture above keeps its meaning in respectful, modern terms.'},
    {'degree': 23,
     'image': 'A line of new arrivals waits to complete the paperwork that will let '
              'them enter a new country.',
     'meaning': 'Every threshold this sign loves crossing eventually has an actual '
                'line to stand in, a form to fill out, a stranger with a stamp '
                "deciding whether the crossing counts. Sagittarius's love of the far "
                'horizon meets, here, the very real bureaucratic weight of actually '
                'getting there, patience tested by process rather than by distance. '
                'There is hope all through the image too, everyone in that line chose '
                'this, believed the new country was worth the wait at the desk.',
     'colors': 'A planet at this degree often shows real patience with the practical, '
               'sometimes tedious process required to actually complete a major '
               'transition, not just the desire for the transition itself. Saturn or '
               'Jupiter here can indicate someone willing to do the paperwork of a big '
               'change rather than only dreaming about the destination. It rewards '
               'trusting that the line is temporary and the country on the other side '
               'is not.',
     'reflection': 'What line are you currently standing in, patiently, for a '
                   'crossing you already know is worth it?'},
    {'degree': 24,
     'image': 'A bluebird lands at the gate of a small cottage, right at the threshold '
              'of the door.',
     'meaning': 'Good fortune, here, arrives modestly, no fanfare, just a small bright '
                'bird choosing exactly this gate to land on. ' + "Sagittarius's "
                'reputation for luck usually imagines something larger and more '
                "dramatic, but this degree insists the sign's real generosity often "
                "shows up at an ordinary threshold, easy to miss if no one's actually "
                'looking out the window. The cottage is humble, and that is precisely '
                'the point, luck does not wait for a grander house to visit.',
     'colors': 'A planet at this degree often shows genuine good fortune that arrives '
               'in modest, easily overlooked form rather than with any announcement. '
               'Jupiter or Venus here can indicate a life where luck shows up '
               'reliably at the door, small and real, if someone remembers to '
               'actually look. It rewards noticing the bluebird instead of only '
               'waiting for a bigger sign.',
     'reflection': 'What small, ordinary bit of luck has already landed at your gate, '
                   'that you might not have noticed yet?'},
    {'degree': 25,
     'image': 'A round-cheeked little boy rocks happily on his wooden hobby-horse.',
     'meaning': 'The whole grown adventure this sign is famous for starts, honestly, '
                'in exactly this kind of small, imaginary gallop, a child fully '
                'convinced the wooden horse under him is really going somewhere. '
                'Sagittarius never really outgrows this particular joy, the pleasure '
                'of imagined distance covered from a completely safe, stationary spot. '
                'There is nothing to correct in the image, the horse does not need to '
                'be real for the delight to be.',
     'colors': 'A planet at this degree often shows a genuinely undamaged capacity for '
               'imaginative joy, adventure that does not require literal travel to '
               'feel completely real. Venus or the Moon here can indicate someone who '
               'has kept real, uncomplicated delight in play well into adulthood. It '
               'rewards trusting that the imagined gallop is still doing real work in '
               'you.',
     'reflection': 'What wooden horse are you still happily riding, that has never '
                   'once needed to be a real one to bring you joy?'},
    {'degree': 26,
     'image': 'Amid a battle, a soldier carries the flag forward, unarmed but '
              'unmistakable.',
     'meaning': "Conviction, carried in the most exposed position on the field, on "
                'purpose: the flag-bearer does not fight directly, they simply make '
                'sure the cause stays visible to everyone, friend and enemy both, '
                "through the worst of the fighting. Sagittarius's belief system "
                'usually gets expressed in words, but this degree asks for a more '
                'physical, more dangerous kind of witness, standing for what you '
                'believe in plain view when it would be safer to duck down with '
                'everyone else. There is real courage in refusing to let the banner '
                'drop, regardless of what is happening around it.',
     'colors': 'A planet at this degree often shows real willingness to be visibly '
               'identified with a cause, even at personal risk, when others might '
               'prefer to stay anonymous. Mars or the Sun here can indicate someone '
               'whose conviction shows up as literal, physical visibility rather than '
               'private belief alone. It rewards keeping your own flag up exactly '
               'when it would be easier to lower it.',
     'reflection': 'What cause of yours have you kept visibly raised, even when the '
                   'fighting around it got genuinely dangerous?'},
    {'degree': 27,
     'image': 'A sculptor works steadily at a block of stone, slowly shaping a figure '
              'into being.',
     'meaning': "Vision, here, meets real material resistance: the figure the sculptor "
                'sees already exists in their mind, but getting it out of the stone '
                'takes actual, patient, physical labor, one careful strike at a time. '
                'Sagittarius is full of big ideas and bigger beliefs, and this degree '
                'grounds all of that in craft, insisting the vision only becomes real '
                'through sustained, disciplined work on something genuinely hard. '
                'Nothing about the finished figure will look rushed, because none of '
                'it was.',
     'colors': 'A planet at this degree often shows real capacity to turn a large, '
               'abstract vision into something concrete through sustained, patient '
               'effort. Saturn or Venus here can indicate a genuine talent for giving '
               'belief actual physical form rather than leaving it purely conceptual. '
               'It rewards trusting the slow, strike-by-strike work as much as the '
               'original vision.',
     'reflection': 'What vision have you been carrying in your mind that is ready for '
                   'you to actually pick up the chisel?'},
    {'degree': 28,
     'image': 'An old stone bridge, built long ago, still carries travelers across a '
              'beautiful stream every day.',
     'meaning': 'Some crossings get built once and simply keep working, structure so '
                'sound that generations later, people are still relying on it without '
                'giving its age a second thought. Sagittarius is drawn to new '
                'horizons, but this degree honors the old, well-built passage that '
                'makes crossing to any new horizon possible in the first place. There '
                'is real beauty in the stream underneath too, a reminder that the '
                'bridge was built to serve something worth crossing toward, not just '
                'to span an obstacle.',
     'colors': 'A planet at this degree often shows real reliance on something old and '
               'well-built, a belief, a relationship, a piece of infrastructure, that '
               'continues to work exactly as intended long after it was made. Saturn '
               'here is especially at home, favoring durable structures over flashy '
               'new ones. It rewards trusting the old bridge instead of always '
               'looking for a newer crossing.',
     'reflection': 'What old, sturdy crossing in your life are you still relying on '
                   'every day, without ever quite thanking it?'},
    {'degree': 29,
     'image': 'A heavyset boy pushes a mower across the lawn of a handsome house on a '
              'quiet suburban street.',
     'meaning': 'Ordinary chores, done in comfortable circumstances: nothing about '
                'this scene is a struggle exactly, the house is elegant and the '
                'street is quiet, but there is still real, unglamorous effort in '
                'getting the actual work done. Sagittarius likes to imagine itself '
                'always reaching for something distant, but this degree, so near the '
                "sign's own end, brings the sign back down to a plain Saturday "
                'afternoon and a task that simply needs doing. There is a quiet '
                'dignity in doing the ordinary job well, even when nothing about the '
                'circumstances demands heroics.',
     'colors': 'A planet at this degree often shows real willingness to do ordinary, '
               'unglamorous work even when circumstances are comfortable enough that '
               'it would not strictly be necessary. Saturn or Venus here can indicate '
               'someone who takes plain tasks seriously rather than only rising to '
               'dramatic ones. It rewards finishing the lawn instead of waiting for a '
               'more meaningful job to show up.',
     'reflection': 'What ordinary task, in comfortable circumstances, have you been '
                   'putting off simply because nothing about it feels urgent enough?'},
    {'degree': 30,
     'image': 'The Pope stands at a window above the square, blessing the crowd '
              'gathered below.',
     'meaning': 'The final degree of Sagittarius closes the sign on its highest, most '
                'public expression of faith: one figure, speaking for a belief system '
                'far larger than himself, offering a blessing to everyone who '
                "gathered specifically to receive it. This is the sign's whole "
                'thirty-degree search for meaning arriving at its most institutional, '
                'most authoritative form, conviction so settled it can now be offered '
                'outward, freely, to a crowd rather than just held privately. Nothing '
                'about the moment is casual, the height of the window, the scale of '
                'the square, the formality of the gesture, all of it says this '
                'blessing has real weight behind it.',
     'colors': 'A planet at this degree often shows real authority around matters of '
               'belief and meaning, a capacity to offer guidance or blessing that a '
               'genuine crowd actually wants to receive. Jupiter or Neptune here can '
               'indicate someone whose spiritual or philosophical conviction has '
               'become substantial enough to be shared publicly, at scale. It rewards '
               'remembering that a blessing this size is only real if the belief '
               'underneath it was actually earned.',
     'reflection': 'What conviction of yours has grown solid enough that you could '
                   'offer it, freely, to a whole crowd gathered to receive it?'},
]

assert len(ENTRIES) == 30, f"expected 30 Sagittarius degrees, found {len(ENTRIES)}"
assert [d["degree"] for d in ENTRIES] == list(range(1, 31)), "Sagittarius degrees out of order"
