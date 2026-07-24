#!/usr/bin/env python3
"""Generate Sabian symbol pages: the reusable template + generation approach
for The Twelve Rooms' Sabian symbol series.

PROOF BATCH (Jul 24 2026): Aries only, 30 degrees, for Shannon's review
before scaling to the remaining 330 (Taurus through Pisces). See
SABIAN-PROOF-README.md in this folder for what to review and how to
extend this to the other 11 signs.

Structure produced (URL, via Vercel cleanUrls):
  /sabian-symbols                    hub: all 12 signs, Aries live, rest "coming soon"
  /sabian-symbols/aries               Aries index: all 30 degrees
  /sabian-symbols/aries-1 .. aries-30 one page per degree

CORRECTNESS: the degree->symbol mapping (SIGNS["Aries"]["degrees"] below,
the `image` field) is the canonical Jones/Wheeler 1925 Sabian symbol,
one per whole zodiac degree, numbered 1-30 within the sign. It was
cross-verified against multiple independent published sources (not
generated or guessed) before being hand-typed here. See the delivery
report for the source list and verification method. Do NOT extend the
`degrees` lists for other signs without the same verification discipline:
fewer verified degrees beats any guessed ones.

COPYRIGHT: `image` is a plain, original restatement of the traditional
degree picture (the widely-reproduced factual image, e.g. "a woman rises
from the sea"), not a verbatim quote of Marc Edmund Jones' 1953 book or
Dane Rudhyar's "An Astrological Mandala" (1973) wording. `meaning`,
`colors`, and `reflection` are original Twelve Rooms interpretation,
written fresh for this project; none of it is copied from Jones or
Rudhyar.

Run: python3 bin/gen_sabian_pages.py   (writes hub + sign index + all degree pages)
"""
import html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent


def esc(s):
    return html.escape(str(s), quote=True)


# Zodiac glyphs and slugs for the 12-sign hub. Only Aries has `degrees` filled
# in for this proof batch; every other sign is rendered as "coming soon" in
# the hub until its own 30 degrees are verified and written the same way.
#
# GLYPH RENDERING: each glyph carries a trailing U+FE0E (VS15, text
# presentation selector). Without it, Apple platforms render these specific
# codepoints (U+2648-U+2653) via Apple Color Emoji as fixed multicolor
# (purple-ish) badges that ignore CSS color entirely, clashing with brand
# gold. VS15 forces the text-glyph presentation, which is a plain glyph the
# `.toolgrid .glyph` rule can color with `--gold` like every other icon in
# this toolgrid (see index.html's ✶ ✧ ☽ ☉ etc., none of which have this
# emoji-presentation problem). Do not remove the VS15 suffix.
SIGNS = [
    {"name": "Aries", "slug": "aries", "glyph": "♈︎", "live": True},
    {"name": "Taurus", "slug": "taurus", "glyph": "♉︎", "live": False},
    {"name": "Gemini", "slug": "gemini", "glyph": "♊︎", "live": False},
    {"name": "Cancer", "slug": "cancer", "glyph": "♋︎", "live": False},
    {"name": "Leo", "slug": "leo", "glyph": "♌︎", "live": False},
    {"name": "Virgo", "slug": "virgo", "glyph": "♍︎", "live": False},
    {"name": "Libra", "slug": "libra", "glyph": "♎︎", "live": False},
    {"name": "Scorpio", "slug": "scorpio", "glyph": "♏︎", "live": False},
    {"name": "Sagittarius", "slug": "sagittarius", "glyph": "♐︎", "live": False},
    {"name": "Capricorn", "slug": "capricorn", "glyph": "♑︎", "live": False},
    {"name": "Aquarius", "slug": "aquarius", "glyph": "♒︎", "live": False},
    {"name": "Pisces", "slug": "pisces", "glyph": "♓︎", "live": False},
]

# The 30 degrees of Aries. `image` is the verified traditional symbol,
# restated plainly (not a verbatim quote of any single copyrighted source).
# `meaning`, `colors`, `reflection` are original Twelve Rooms prose.
ARIES = [
    {"degree": 1, "image": "A woman rises from the sea; a seal surfaces and embraces her.",
     "meaning": "This is the first degree of the entire zodiac, so of course it is a birth: a form breaking the surface of the water it came from, met at once by a creature that already belongs to both worlds. Aries opens the year the way this image opens the round: with an emergence, not a plan. Nothing here is fully formed yet, and that is the point; every chart, and this reading, starts in exactly this kind of unfinished water. The seal is not a threat, it is instinctive company arriving before the woman has even found her footing. Read plainly, the degree says life meets you before you are ready, and meets you kindly.",
     "colors": "A planet or point at Aries 1 begins its whole expression here, before it has proven itself to anyone, including its owner. It behaves like an instinct that has not yet been examined: quick to appear, quick to act, uninterested in permission. The Sun here shows a self that keeps being reborn into new starts; the Moon, a feeling life that surfaces before it can be named; the Ascendant, a person the world meets mid-emergence, already met with unexpected welcome.",
     "reflection": "What in you is only now breaking the surface, and who is already there to meet it?"},
    {"degree": 2, "image": "A comedian entertains a crowd.",
     "meaning": "One degree in and the self already needs an audience: this is Aries learning that identity is also a performance, that being seen is not vanity but confirmation. The comedian's craft is timing and the nerve to say the true thing sideways so a room can bear it. Underneath the laughter sits something serious: comedy is often the safest way to tell people what they already suspect about themselves. This degree carries both the gift and the exposure of that work, the need to be liked braided together with the willingness to risk the room going quiet.",
     "colors": "Wherever this degree falls, expect a talent for reading a room and adjusting to it fast, plus a private hunger to know the adjustment landed. Mercury here often signals real wit, quick and warm rather than cruel. Venus can bring charm that performs itself without meaning to. On an angle, it shows someone who has learned early that entering a room is itself an act, and a well-timed one.",
     "reflection": "Where are you performing what you actually believe, and is the room laughing with you, or just laughing?"},
    {"degree": 3, "image": "A cameo profile of a man, shaped like the outline of his own country.",
     "meaning": "Identity, at this degree, is inseparable from where it comes from. The man's silhouette and his homeland's map have become the same line: he did not choose this resemblance, he grew into it, the way anyone eventually starts to look like the place and the era that raised them. This is Aries discovering that the self is never purely self-made; it is carved partly by the ground it stands on. There is quiet pride here, and a little confinement too, since a cameo is a fixed profile, not a moving face.",
     "colors": "A planet at this degree tends to express through inherited shape: family reputation, cultural identity, an image handed down rather than chosen from nothing. Saturn here can mean carrying a legacy with real seriousness. The Sun can show a person whose sense of self is bound tightly to origin, for better and for harder. It rewards knowing your own outline well enough to use it on purpose.",
     "reflection": "What have you inherited so thoroughly that you mistake it for something you invented?"},
    {"degree": 4, "image": "Two lovers walk a secluded path.",
     "meaning": "After three degrees of the self alone, Aries finds another person, and immediately wants privacy for it. This is not the public partnership of Libra's opposite point; it is the walk before any of that, chosen ground away from witnesses, where two people can be exactly as unfinished as they are. The secrecy is not shame, it is protection: some things need to be tested without an audience before they can survive one.",
     "colors": "Wherever this degree lands, closeness tends to want a private setting before a public one. Venus here often shows someone who falls in love away from crowds, needing the walk before the introduction. On a relationship point like the seventh house or its ruler, it suggests intimacy built in unhurried, undisclosed stretches rather than declared all at once.",
     "reflection": "What relationship in your life is still walking its secluded stretch, and does it need more privacy, or is it finally ready for a witness?"},
    {"degree": 5, "image": "A triangle with wings.",
     "meaning": "Geometry meets flight: a stable, three-sided shape given the means to leave the ground. This degree holds structure and freedom in the same image without asking either to apologize for the other. Aries is usually read as pure impulse, but here impulse has found a form sturdy enough to actually go somewhere instead of just igniting and burning out. The triangle is also, historically, a symbol of idea and ideal, three points meeting at a single vision; winged, that vision travels.",
     "colors": "A planet at Aries 5 often carries ideas that want structure enough to be built, and enough lift to leave the drawing board. Mercury here favors concepts that actually deploy, not just theorize. On the Midheaven, it can describe a career built from a stable core that nonetheless keeps moving, expanding, or traveling outward from that base.",
     "reflection": "What structure have you built that is finally sturdy enough to risk giving it wings?"},
    {"degree": 6, "image": "A square, one side of it lit bright.",
     "meaning": "A shape with four equal sides, and only one of them singled out by light. This degree asks what happens when a whole, balanced thing gets one part of itself illuminated at the expense of the rest: is that emphasis, or a distortion of the square's real symmetry? Aries here practices selective attention, the discipline of choosing where the light goes rather than trying to shine everywhere at once. There is a caution folded in too, since a square known only by its lit face is only partly known.",
     "colors": "A planet at this degree tends to bring focus and a very specific kind of visibility, one facet catching all the notice while the rest of the structure holds quietly in shadow. The Sun here can describe someone known for one clear thing, whose fuller self stays less public. Useful for anyone whose gift is doing one part of the job so well it eclipses the others.",
     "reflection": "Which one side of you gets all the light, and what does the rest of the square hold that no one sees?"},
    {"degree": 7, "image": "A man expresses himself fully in two different fields at once.",
     "meaning": "This degree refuses the idea that a life has to specialize to be whole. Two realms, run at full expression simultaneously, without either one being the hobby or the compromise. It takes real capacity to do this rather than collapse into one lane, and this degree seems to trust that the capacity exists. Aries usually drives toward one clean assertion of self; here it multiplies instead, insisting identity can hold two true shapes without splitting.",
     "colors": "Wherever it falls, expect someone who resists being defined by a single occupation or role, and who is often better for it: the second field feeds the first. Mercury or the Midheaven here can describe a genuinely dual career, or a public identity that is legitimately two things, not one thing with a side project. The risk is thinning attention; the strength is a fuller, less brittle self.",
     "reflection": "What second realm are you already fully living in, even if your resume only lists the first?"},
    {"degree": 8, "image": "A woman's wide-brimmed hat, its streamers blown by an east wind.",
     "meaning": "Fashion caught mid-motion by weather it did not choose: the hat is deliberate, dressed for the occasion, and the wind is entirely uninvited, doing whatever it wants with the streamers anyway. This degree is about composure meeting circumstance, the poised self getting visibly ruffled by something outside its control, and staying recognizably itself regardless. An east wind, traditionally, is the wind of new beginnings; even glamour gets swept into whatever is arriving next.",
     "colors": "A planet here often shows a put-together exterior that circumstances keep gently testing. Venus can describe beauty or style that reads as more interesting for being a little wind-blown rather than perfectly still. On the Ascendant, it suggests someone whose composed first impression always has one detail the world got to touch first.",
     "reflection": "What part of your composure has the wind already gotten into, and can you let it show?"},
    {"degree": 9, "image": "A crystal gazer.",
     "meaning": "The gazer looks into clear stone and reads what is not yet visible to everyone else. This is intuition given a formal practice, a discipline built around trusting the image that arrives rather than only the fact that can be checked. Ninth-degree Aries turns the sign's raw instinct toward genuine foresight: not guessing, but a trained way of seeing ahead of the evidence. The crystal itself is passive; all the meaning gets made by the one looking into it.",
     "colors": "A planet at this degree often carries real perceptiveness, the kind that reads a situation before the facts confirm it. Neptune or the Moon here can indicate a strong intuitive sense, sometimes formalized (astrology itself, a reading practice), sometimes simply trusted privately. It rewards taking that seeing seriously instead of dismissing it as guesswork.",
     "reflection": "What have you already seen clearly, that you are waiting for proof of before you'll believe it?"},
    {"degree": 10, "image": "A teacher recasts old symbols into new form.",
     "meaning": "Nothing here is invented from nothing; the teacher works with what tradition already handed down, and the achievement is fresh shape, not fresh material. This degree honors continuity and reinvention at once, the two things Aries rarely holds together this comfortably. Real teaching, at this level, is translation: taking a symbol gone stale from repetition and giving it a form the current room can actually receive.",
     "colors": "A planet here often shows an ability to make old material feel newly relevant, rather than a need to originate everything from scratch. Mercury or Jupiter at this degree can favor teaching, writing, or any work that renews a tradition instead of discarding it. On the Midheaven, it suggests a career built on exactly this kind of translation.",
     "reflection": "What old symbol, in your own life or field, is waiting for you to give it a form people can actually use now?"},
    {"degree": 11, "image": "The ruler of a nation.",
     "meaning": "Pure authority, unshared, answerable mostly to itself. This degree is Aries at its most concentrated: one figure, one will, deciding for the many. It is a heavy image on purpose, since real rule always is; the degree does not soften the isolation that comes with sitting at the top of a structure. There is dignity here, and also the loneliness that dignity of this kind always carries with it.",
     "colors": "A planet at this degree often brings a natural claim to authority, sometimes welcomed and earned, sometimes simply assumed by others before it is chosen. The Sun or Saturn here can describe someone who ends up in charge, in a family, a company, a room, more often than they set out to be. The work of the degree is ruling well, not just ruling.",
     "reflection": "Where has authority already landed on you, whether or not you asked for it, and how are you carrying it?"},
    {"degree": 12, "image": "A flock of wild geese, in flight formation.",
     "meaning": "Individual birds holding a shared shape without a single leader micromanaging the line: this is collective movement built on instinct, not command. The formation does real work, cutting the wind for the birds behind, so no one member holds the whole burden alone. Aries, usually so solitary, here discovers a version of the self that moves better inside a group built for exactly this kind of shared momentum.",
     "colors": "A planet at this degree often favors belonging to a group in motion toward the same distant point: a team, a cohort moving together. Jupiter or an eleventh-house connection here can indicate real strength drawn from formation rather than from standing alone. It is a good degree for anyone whose instinct is to go it alone, learning what shared lift actually feels like.",
     "reflection": "What formation are you flying in right now, and who is currently cutting the wind for you?"},
    {"degree": 13, "image": "An unexploded bomb, quietly defused.",
     "meaning": "Danger that was real, and did not happen. This degree carries the particular relief of a disaster caught in time, plus the residual unease of knowing how close it came. Nothing about the image says the threat wasn't serious; it says the outcome, this time, was safety, quietly and without fanfare. Thirteenth degrees across the zodiac often carry a charged, crisis-adjacent energy, and Aries meets it here with something closer to relief than triumph.",
     "colors": "A planet at this degree can indicate a life that has weathered a close call, sometimes literally, sometimes as a near-miss with a much worse version of events. Mars or Pluto here often shows real capacity to defuse volatile situations rather than detonate them, a steadiness under pressure that isn't obvious until it's tested. Worth naming the near-misses instead of only ever moving past them silently.",
     "reflection": "What almost went off in your life, and what actually kept it from happening?"},
    {"degree": 14, "image": "A serpent coils near a man and a woman.",
     "meaning": "An old story, told without its usual moral: temptation, knowledge, and the two people it arrives for, with the serpent simply present rather than actively striking. This degree holds the charge of a garden without insisting on a fall; it is possibility coiled nearby, dangerous and generative at once, waiting to see what the two people do with it. Aries rarely pauses, but this degree makes you notice the coil before you decide how to move.",
     "colors": "A planet here often signals real awareness of risk and temptation living close to a relationship or a decision, not as external bad luck but as something coiled right there in the situation. Pluto or Mars at this degree can describe a talent for sensing where danger and desire overlap. The degree rewards clear eyes rather than pretending the snake isn't in the garden.",
     "reflection": "What is coiled quietly near your closest relationships right now, neither striking nor leaving?"},
    {"degree": 15, "image": "A weaver at work on a ceremonial blanket.",
     "meaning": "Pattern made by hand, with intention, for a purpose bigger than decoration: this is craft as ritual, not just skill. Every thread in a ceremonial blanket carries meaning the weaver knows even if the viewer doesn't, and the whole comes together slowly, row by row, with no shortcuts available. Aries, usually fast, slows all the way down here to do something correctly rather than quickly.",
     "colors": "A planet at this degree often favors patient, meaningful craftsmanship, work built thread by thread toward something that will be used in a real occasion of someone's life, not shelved as mere decoration. Venus or Saturn here can indicate a maker whose slow, careful work carries weight beyond its materials. It is a strong degree for anyone whose hands need to be doing the thinking.",
     "reflection": "What are you weaving right now, thread by thread, that is meant for an occasion bigger than an ordinary day?"},
    {"degree": 16, "image": "Nature spirits dance in the light of the setting sun.",
     "meaning": "A threshold hour, and creatures that only really show themselves in it: not full daylight, not night, the brief gold window when the ordinary rules loosen a little. This degree favors the liminal, the almost-unseen layer of life that operates just past what practical daytime attention usually notices. Aries meets its own wilder, less literal edge here, the part of instinct that borders on enchantment rather than mere drive.",
     "colors": "A planet at this degree often brings sensitivity to atmosphere, timing, and the parts of a moment that don't show up on a schedule. Neptune or the Moon here can describe someone genuinely attuned to twilight states, transitions, the in-between of any process. It rewards paying attention right at the edges of things, not only their broad daylight middle.",
     "reflection": "What part of your life only really shows itself in the in-between hours, and are you there to see it?"},
    {"degree": 17, "image": "Two proper spinsters sit together in silence.",
     "meaning": "Company that needs no talking to be real company. This degree honors a kind of relationship built entirely on shared presence and restraint, propriety held not as coldness but as its own form of intimacy. There is dignity in the silence, not loneliness; two people who have long since said what needed saying, now simply, comfortably, in the room together. Aries, so often about declaring the self loudly, finds here a quieter, equally valid way to be known.",
     "colors": "A planet at this degree often favors companionship that doesn't need constant conversation to feel close, and a comfort with restraint that some read, wrongly, as distance. Saturn here can describe relationships built on long, steady, undemonstrative loyalty. It is a good degree for anyone whose closest bonds run quiet rather than expressive.",
     "reflection": "Which relationship in your life is closest precisely because it no longer needs words to prove itself?"},
    {"degree": 18, "image": "An empty hammock, strung between two trees.",
     "meaning": "Rest, set up and waiting, with no one in it yet. This degree is potential leisure, an invitation the self hasn't accepted, structure for ease that has been built but not yet used. There is something almost wistful in the image: the hammock did its part, hung there between two solid trees, ready; whether anyone actually lies down in it is a separate question entirely. Aries, which struggles to stop moving, gets handed exactly this kind of unclaimed invitation to pause.",
     "colors": "A planet at this degree can indicate rest that keeps getting deferred, an ease that is available and structurally sound but somehow never quite taken. Venus or a fourth-house connection here can favor someone very good at creating restful spaces for others, and slower to use them. The degree rewards actually getting in the hammock.",
     "reflection": "What rest have you already built for yourself, and what is stopping you from lying down in it?"},
    {"degree": 19, "image": "A magic carpet.",
     "meaning": "Transport without ordinary machinery, distance covered by something closer to belief than to engineering. This degree carries real wonder, the sense that a life can move faster and farther than the visible means would explain, if the right unlikely vehicle shows up. It's also, honestly, a degree of borrowed transportation: the carpet takes you somewhere, but it isn't yours to keep, and the journey depends on trusting something you can't fully verify.",
     "colors": "A planet at this degree often shows sudden, seemingly improbable movement in a life: opportunities that arrive faster than logic predicts, travel or advancement that looks charmed from the outside. Jupiter or Uranus here can indicate real luck of this exact kind. Worth remembering the carpet is a gift, not a guarantee, so it rewards gratitude more than entitlement.",
     "reflection": "What has moved you further, faster, than you can actually explain, and have you thanked it yet?"},
    {"degree": 20, "image": "A young girl feeds birds in winter.",
     "meaning": "Small, unglamorous care, offered in a season that makes it matter more. Nothing about this image is dramatic; a child, some seed, a handful of birds who would otherwise go hungry. Aries usually wants its gestures big and immediate, but here the degree insists that quiet, regular tending, done without an audience, is its own real form of strength. Winter is the setting for a reason: this is care offered precisely when conditions are hardest.",
     "colors": "A planet at this degree often shows genuine nurturing instinct expressed in small, consistent acts rather than grand gestures, tending to whoever or whatever needs it most in a lean season. The Moon or Venus here can indicate someone whose care is most present exactly when things are hardest for others. It is a strong degree for steady kindness that never announces itself.",
     "reflection": "Who, or what, are you quietly feeding through their winter, without expecting anyone to notice?"},
    {"degree": 21, "image": "A boxer steps into the ring.",
     "meaning": "The moment before the fight starts, when all the training either counts or it doesn't yet. This degree is preparation meeting its actual test, the self stepping deliberately into a contest it chose. There is no ambiguity in a boxing ring: someone wins, someone doesn't, and both parties agreed to find out. Aries is built for exactly this kind of direct, consenting confrontation, one where the outcome is earned in full view rather than left to interpretation.",
     "colors": "A planet at this degree often brings a real appetite for direct competition and a willingness to be tested openly rather than quietly. Mars here, unsurprisingly, is very much at home: courage under real, agreed-upon pressure. On an angle, it can describe someone who is at their most themselves the moment the contest actually starts, nerves included.",
     "reflection": "What ring have you already agreed to step into, and are you as ready as you think?"},
    {"degree": 22, "image": "The gate to a garden of every desire fulfilled.",
     "meaning": "Not the garden itself, only its threshold: this degree is the moment of arrival at something that promises everything you've wanted, before you've actually walked through and found out what fulfillment costs. There is real hope in a gate like this, and also real caution, since a promise this total is exactly the kind that asks the most careful look before stepping in. Aries wants the garden immediately; this degree asks it to notice the gate first.",
     "colors": "A planet at this degree often indicates arriving, again and again, at thresholds of major fulfillment, career, love, creative work, that seem to promise everything at once. Jupiter or Venus here can describe genuine access to abundance, alongside a real need to walk through deliberately rather than assume the promise is automatic. It rewards checking what “every desire” actually costs before entering.",
     "reflection": "What gate are you standing in front of right now, and have you actually looked at what's on the other side, or only imagined it?"},
    {"degree": 23, "image": "A woman in pastel dress carries a heavy, valuable, and veiled load.",
     "meaning": "Something significant is being carried, and deliberately kept from view. The lightness of the dress and the weight of the load don't match, on purpose: this degree is about a burden or a private matter held with composure, visible effort hidden under a calm exterior. There is discretion here, maybe even protection, the veil doing real work rather than just decoration. Aries, usually transparent about its impulses, learns here what it means to carry something heavy gracefully and privately.",
     "colors": "A planet at this degree often describes someone managing a significant private weight, a responsibility, a secret, a nurturing of something not yet ready to be seen, while presenting calm to the world. The Moon or Neptune here can indicate real discretion around what is carried, sometimes protectively, sometimes at real personal cost. It rewards asking what's under the veil before assuming lightness is the whole story.",
     "reflection": "What are you carrying right now that looks lighter, from the outside, than it actually is?"},
    {"degree": 24, "image": "An open window; the curtain, blown by the wind, takes the shape of a horn of plenty.",
     "meaning": "Ordinary air moving through an ordinary opening, and abundance appears in the shape it happens to make. Nothing here was engineered for effect; the wind simply did what wind does, and the curtain, doing what curtains do, briefly became a symbol of everything overflowing. This degree suggests that plenty often arrives this way: not summoned, just noticed in the accidental shapes that ordinary circumstance keeps making, if you're watching for them.",
     "colors": "A planet at this degree often brings unplanned abundance, opportunity, or resource that shows up through open, receptive conditions rather than direct pursuit. Jupiter or Venus here can indicate a genuine talent for noticing plenty in what looks like coincidence. It rewards leaving windows open rather than only ever chasing the horn of plenty directly.",
     "reflection": "What has the wind already shaped into abundance nearby, that you haven't looked at closely enough to notice?"},
    {"degree": 25, "image": "A double promise.",
     "meaning": "Two commitments, made at once, and this degree does not say whether they agree with each other. A double promise can be a rich thing, one vow reinforcing another, or it can be the beginning of a real conflict, two loyalties that will eventually ask something incompatible. The degree simply names the doubling and leaves the reader to look honestly at their own promises: do they run in the same direction, or has one been made without checking on the other?",
     "colors": "A planet at this degree often shows a life carrying two significant commitments at once, to two people, two paths, two versions of the self, that need regular, honest checking against each other. Mercury or Venus here can indicate real skill at holding both, or real difficulty when they start to pull apart. It rewards naming both promises out loud, at least to yourself.",
     "reflection": "What two promises are you currently keeping, and do you actually know if they still agree with each other?"},
    {"degree": 26, "image": "A man holds more gifts than his arms can carry.",
     "meaning": "Genuine abundance, arriving faster than the capacity to manage it gracefully. This is not a story about too little; it's a story about too much all at once, and the very real, very human problem of dropping something valuable simply because both hands were already full. Aries, always reaching for more, meets here the practical limit of its own arms, and the useful lesson that a gift set down carefully is not a gift lost.",
     "colors": "A planet at this degree often describes real, sometimes almost overwhelming, natural gifting, talent, opportunity, resource, more than one lifetime can fully use without some kind of triage. Jupiter here is especially at home: an abundance that needs organizing more than it needs increasing. It rewards choosing what to set down, rather than trying to hold every gift at once.",
     "reflection": "What gift are you currently at risk of dropping, simply because your arms are already full of others?"},
    {"degree": 27, "image": "A lost opportunity is regained, through imagination.",
     "meaning": "Not everything that's gone stays gone. This degree insists that imagination is a genuine tool for recovery, not mere daydreaming about what could have been: a chance that seemed closed can reopen because someone was willing to picture it differently, and then act from that picture. Aries's usual instinct is forward motion only, but here it circles back, and finds that going back through imagination is itself a form of forward motion.",
     "colors": "A planet at this degree often shows a real capacity for second chances, especially ones built by re-imagining a past setback rather than simply repeating the same approach. Neptune or the Moon here can indicate genuine creative recovery from earlier loss. It rewards trusting that a door once closed can be reopened by picturing it open first.",
     "reflection": "What did you once consider a lost opportunity, that your imagination might actually be able to reopen?"},
    {"degree": 28, "image": "A large audience faces a performer who has disappointed its expectations.",
     "meaning": "Expectation, and the gap between it and what actually arrived. This degree carries the particular discomfort of a public failure to deliver, everyone watching, no way to quietly correct course before the room notices. It is not a gentle image, but it is an honest one: sometimes the self does not meet the moment, and the size of the audience only makes the gap more visible. Aries risks this exact scenario every time it moves fast and loud in front of others.",
     "colors": "A planet at this degree can indicate real anxiety around public performance, or actual experience of not meeting expectations in a visible setting. Saturn here often shows someone who has learned, the hard way, what it costs to disappoint a room, and who takes preparation seriously because of it. The degree rewards recovering the relationship with an audience rather than avoiding audiences altogether.",
     "reflection": "Where did you once disappoint a room, and has that room actually kept score longer than you have?"},
    {"degree": 29, "image": "A celestial choir sings: the music of the spheres.",
     "meaning": "The last full degree before Aries becomes Taurus reaches for something beyond the personal entirely: harmony that isn't made by any single voice, sound as evidence of an order larger than the self. This is Aries, of all signs, arriving at something genuinely transcendent, proof that even the most self-focused sign in the zodiac has a note in it that points past itself. The choir doesn't need an audience to be real; the music of the spheres plays whether or not anyone below is listening.",
     "colors": "A planet at this degree often indicates a real sense of participating in something larger than personal ambition, a calling, a harmony, a purpose that doesn't require individual credit to feel true. Neptune or Jupiter here can describe genuine spiritual or artistic attunement. It rewards listening for the larger harmony rather than insisting on being the only voice in the piece.",
     "reflection": "What larger harmony are you already part of, whether or not anyone credits your single voice in it?"},
    {"degree": 30, "image": "A duck pond, with its brood.",
     "meaning": "The final degree of Aries, and the sign's whole restless momentum settles, for a moment, into something small, contained, and quietly thriving. A pond is not the ocean it started from in degree one; it is modest, bounded, and entirely sufficient for the life it holds. The brood, newly hatched, is proof that everything this sign spent thirty degrees becoming has actually produced something: not a grand finale, just a calm, complete little scene of new life doing fine on its own pond.",
     "colors": "A planet at this degree often shows contentment achieved in a modest, self-contained sphere rather than a sprawling one, and a genuine ease raising or tending what has newly come into being. The Moon here is especially at home: nurturing that doesn't need a bigger stage to feel finished. It rewards recognizing when “enough” has actually already arrived.",
     "reflection": "What small pond have you built that is already, quietly, enough?"},
]

assert len(ARIES) == 30, f"expected 30 Aries degrees, found {len(ARIES)}"
assert [d["degree"] for d in ARIES] == list(range(1, 31)), "Aries degrees out of order"


def degree_page(sign_name, sign_slug, entry, total):
    n = entry["degree"]
    slug = f"{sign_slug}-{n}"
    prev_link = (f'<a href="/sabian-symbols/{sign_slug}-{n-1}">← {sign_name} {n-1}°</a>'
                 if n > 1 else f'<a href="/sabian-symbols/{sign_slug}">← All of {sign_name}</a>')
    next_link = (f'<a href="/sabian-symbols/{sign_slug}-{n+1}">{sign_name} {n+1}° →</a>'
                 if n < total else f'<a href="/sabian-symbols">Explore other signs →</a>')
    title = f"{sign_name} {n}° Sabian Symbol: {esc(entry['image']).rstrip('.')} · The Twelve Rooms"
    desc = (f"The Sabian symbol for {sign_name} {n}°: {entry['image']} What it means, how it "
            f"colors a planet or point at this exact degree, and a reflection to sit with.")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols/{slug}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{sign_name} {n}° Sabian Symbol","author":{{"@type":"Organization","name":"The Twelve Rooms"}},"about":"Sabian symbol for {sign_name} degree {n}"}}
</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <p class="hint"><a href="/sabian-symbols">Sabian Symbols</a> &middot; <a href="/sabian-symbols/{sign_slug}">{sign_name}</a> &middot; Degree {n} of {total}</p>
  <h1>{sign_name} {n}&deg;</h1>
  <p class="lede">The traditional symbol for this degree, one of the 360 Sabian symbols first recorded in 1925: <strong>&ldquo;{esc(entry['image'])}&rdquo;</strong></p>

  <div class="card">
    <p class="kicker">THE SYMBOL</p>
    <p class="big" style="font-size:19px;line-height:1.45">&ldquo;{esc(entry['image'])}&rdquo;</p>
    <p class="hint">{sign_name} {n}&deg; &middot; Sabian symbols, devised 1925 (Marc Edmund Jones, clairvoyant Elsie Wheeler)</p>
    <p class="hint">Remember to round up: a planet or point at 9&deg;30&prime; takes the 10&deg; symbol, not the 9&deg; one.</p>
  </div>

  <section class="prose">
    <h2>What this degree describes</h2>
    <p>{entry['meaning']}</p>
    <h2>When a planet or point falls here</h2>
    <p>{entry['colors']}</p>
  </section>

  <div class="card" style="text-align:center">
    <p class="hint" style="font-style:italic;font-size:14px">{entry['reflection']}</p>
  </div>

  <div class="cta">
    <h2>Find your own Sabian symbols</h2>
    <p>Your Sun, Moon, Ascendant, and every planet each sit at their own exact degree. Cast a free natal chart to find yours, or let a full reading trace what they mean together.</p>
    <a href="/natal-chart">Cast your free chart</a>
  </div>

  <p class="hint" style="display:flex;justify-content:space-between;gap:12px;margin-top:18px">
    <span>{prev_link}</span><span>{next_link}</span>
  </p>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols" / f"{slug}.html").write_text(page)
    return slug


def sign_index_page(sign_name, sign_slug, entries):
    cards = "\n".join(
        f'    <a class="almanac-card" href="/sabian-symbols/{sign_slug}-{e["degree"]}">'
        f'<h3>{sign_name} {e["degree"]}&deg;</h3><p>{esc(e["image"])}</p></a>'
        for e in entries)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{sign_name} Sabian Symbols: All 30 Degrees &middot; The Twelve Rooms</title>
<meta name="description" content="Every Sabian symbol in {sign_name}, degree by degree: the traditional 1925 image for each of the sign's 30 degrees, with an original Twelve Rooms meaning for each.">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols/{sign_slug}">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <p class="hint"><a href="/sabian-symbols">Sabian Symbols</a> &middot; {sign_name}</p>
  <h1>{sign_name}: all 30 Sabian symbols</h1>
  <p class="lede">Every whole degree of {sign_name} has its own Sabian symbol, a small traditional picture first recorded in 1925. Find the exact degree of your Sun, Moon, Ascendant, or any planet in {sign_name}, and read what that degree adds to it.</p>

  <div class="almanac-grid">
{cards}
  </div>

  <section class="prose">
    <h2>Don't know your exact degree?</h2>
    <p>A Sabian symbol is specific to the whole degree a planet or point occupies, so you need the exact placement, not just the sign, to find yours. Cast a free <a href="/natal-chart">natal chart</a> to see every planet's precise degree, then look up its Sabian symbol here.</p>
  </section>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols" / f"{sign_slug}.html").write_text(page)


def hub_page(signs):
    cards = []
    for s in signs:
        if s["live"]:
            cards.append(
                f'    <a href="/sabian-symbols/{s["slug"]}"><span class="glyph" aria-hidden="true">{s["glyph"]}</span>'
                f'<h2>{s["name"]}</h2><p>All 30 degrees, symbol and meaning.</p></a>')
        else:
            cards.append(
                f'    <div class="soon"><span class="glyph" aria-hidden="true">{s["glyph"]}</span>'
                f'<h2>{s["name"]}</h2><p>30 degrees, in progress.</p><span class="tag gold">Coming soon</span></div>')
    grid = "\n".join(cards)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sabian Symbols: The Meaning of Every Zodiac Degree &middot; The Twelve Rooms</title>
<meta name="description" content="The Sabian symbols: a traditional picture for each of the 360 degrees of the zodiac, devised in 1925. Aries is live, all 30 degrees; the rest of the signs are coming soon.">
<link rel="canonical" href="https://thetwelverooms.com/sabian-symbols">
<link rel="stylesheet" href="/tools.css">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"What is a Sabian symbol?","acceptedAnswer":{{"@type":"Answer","text":"A Sabian symbol is a short traditional picture assigned to each of the 360 whole degrees of the zodiac, one degree at a time. They were received by clairvoyant Elsie Wheeler and recorded by astrologer Marc Edmund Jones in 1925. Astrologers use them to add texture to a planet or point's exact degree, beyond its sign alone."}}}},
{{"@type":"Question","name":"How do I find my Sabian symbol?","acceptedAnswer":{{"@type":"Answer","text":"You need the exact degree of a planet or point, not just its sign, since each of the 30 degrees in a sign has its own symbol. Cast a free natal chart to see every planet's precise degree, then look it up in the sign's list here."}}}},
{{"@type":"Question","name":"Are all 360 Sabian symbols here?","acceptedAnswer":{{"@type":"Answer","text":"Not yet. This is a proof batch: all 30 degrees of Aries are live and complete. The remaining 11 signs are being written to the same standard and will publish as they're finished."}}}}
]}}
</script>
</head>
<body>
<div id="masthead"></div>
<main class="wrap">
  <h1>The Sabian symbols</h1>
  <p class="lede">A short traditional picture for each of the 360 whole degrees of the zodiac, one per degree, first recorded in 1925. Every planet and point in a chart sits at one exact degree; its Sabian symbol adds a layer of meaning beyond the sign alone. Aries is complete, all 30 degrees; the rest of the wheel is being written to the same standard.</p>

  <div class="toolgrid">
{grid}
  </div>

  <div class="card">
    <p class="kicker">HOW TO FIND YOUR DEGREE</p>
    <p class="hint" style="font-size:14px;line-height:1.6;color:#33384a">Sabian symbols belong to whole degrees, and the convention is to round up: a planet or point at 9&deg;30&prime; Aries takes the <strong>Aries 10&deg;</strong> symbol, not the 9&deg; one. So find your planet's exact degree, round up to the next whole degree, and look that number up in the sign's list below.</p>
  </div>

  <section class="prose">
    <h2>Where the Sabian symbols come from</h2>
    <p>In 1925, astrologer Marc Edmund Jones worked with clairvoyant Elsie Wheeler in Balboa Park, San Diego, showing her blank flash-cards and recording the image each one brought to mind, one degree at a time, until all 360 were captured. The result, later published by Jones in 1953 and given a literary expansion by Dane Rudhyar in 1973, became one of the most widely used systems for reading the exact degree of a planet or point, not just its sign.</p>
    <h2>How to use one</h2>
    <p>Sabian symbols are precise: they describe a single whole degree, so the symbol for 14&deg; is not the symbol for 15&deg;. You need an exact birth time and a cast chart to know which degree your Sun, Moon, Ascendant, or any planet actually occupies. Once you have that degree, the symbol adds color and image to what the sign and house already tell you, a closer read of one specific point in the chart.</p>
  </section>

  <div class="cta">
    <h2>Find your own exact degrees</h2>
    <p>Cast a free natal chart to see every planet's precise degree, then explore what each one's Sabian symbol adds. For the whole chart read as one story, The Twelve Rooms writes it by hand.</p>
    <a href="/natal-chart">Cast your free chart</a>
  </div>

  <div id="site-footer"></div>
</main>
<script src="/tools.js"></script>
</body>
</html>
"""
    (OUT / "sabian-symbols.html").write_text(page)


def main():
    (OUT / "sabian-symbols").mkdir(exist_ok=True)
    for entry in ARIES:
        degree_page("Aries", "aries", entry, len(ARIES))
    sign_index_page("Aries", "aries", ARIES)
    hub_page(SIGNS)
    print(f"wrote {len(ARIES)} Aries degree pages, 1 sign index, 1 hub page")


if __name__ == "__main__":
    main()
