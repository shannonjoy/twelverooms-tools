# Sabian symbol sign-data schema

This folder holds one Python data file per zodiac sign for The Twelve
Rooms' Sabian symbol pages. `bin/gen_sabian_pages.py` discovers whatever
files exist here, generates pages for the signs that are complete, and
renders every other sign as "Coming soon" on the hub. This lets multiple
signs be written in parallel, each in its own file, without anyone
editing `gen_sabian_pages.py` itself, and lets the build be re-run at any
time to pick up newly finished signs (nothing about it depends on running
the signs in order or all at once).

## File naming

One file per sign, named `<slug>.py`, e.g. `bin/sabian_data/aries.py`,
`bin/sabian_data/taurus.py`. The slug is the lowercase English sign name,
used directly in URLs (`/sabian-symbols/<slug>`, `/sabian-symbols/<slug>-<n>`).

## Required exports

Each sign file must export two names:

### `SIGN` (dict)

Per-sign metadata:

```python
SIGN = {"name": "Aries", "slug": "aries", "glyph": "♈︎", "order": 1}
```

- `name` (str): display name, e.g. `"Aries"`.
- `slug` (str): lowercase URL slug, e.g. `"aries"`. Must match the filename.
- `glyph` (str): the zodiac glyph, **with a trailing U+FE0E (VS15) text
  presentation selector**. Without VS15, Apple platforms render glyphs
  U+2648-U+2653 as fixed multicolor Apple Color Emoji badges that ignore
  CSS color, clashing with the site's brand gold. VS15 forces plain-glyph
  presentation so `.toolgrid .glyph` can color it like every other icon
  in the toolgrid. Do not drop the VS15 suffix.
- `order` (int, 1-12): the sign's position in the zodiac wheel, Aries=1
  through Pisces=12. Used to sort the hub and degree-page navigation.

`SIGN` is cross-checked against the canonical 12-sign table baked into
`gen_sabian_pages.py` (see "Canonical sign order" below); it does not
override that table, it just makes each data file self-contained and
readable on its own.

### `ENTRIES` (list of 30 dicts)

The sign's 30 whole-degree entries, **in order, degrees 1 through 30**.
Each entry is a dict with exactly these fields (same field names the
generator has always used — do not rename them):

| Field        | Type | What it is |
|--------------|------|------------|
| `degree`     | int  | The whole degree within the sign, 1-30. |
| `image`      | str  | The traditional Sabian symbol for this degree: a plain, original restatement of the widely-reproduced factual picture (e.g. "A woman rises from the sea; a seal surfaces and embraces her."). This is the canonical Jones/Wheeler 1925 symbol for the degree — see "Correctness" below. Not a verbatim quote of Marc Edmund Jones' 1953 book or Dane Rudhyar's *An Astrological Mandala* (1973); an original restatement of the same traditional image. |
| `meaning`    | str  | Original Twelve Rooms prose (2-6 sentences) interpreting what the degree/symbol describes on its own terms — the image read as a small story or character, not a dictionary definition. |
| `colors`     | str  | Original Twelve Rooms prose (2-4 sentences) on how this degree "colors" a planet or point that falls there — i.e. what it adds to a Sun, Moon, Mercury, an angle, etc. sitting at that exact degree. Often names a planet/point that resonates especially strongly with the degree. |
| `reflection` | str  | One original line, phrased as a question, for the reader to sit with. |
| `note`       | str, optional | **Only present on degrees whose 1925 original used dated or ethnically charged imagery** (e.g. a stereotyped "Indian warrior/squaw" picture, a named literary slave character, a slur like "gypsy" or "Chinaman"). Shannon's policy: keep the respectful restatement in `image` as-is, and add this one-line, non-preachy acknowledgment beneath the symbol card. Standard line: `"Note: the 1925 original for this degree used dated ethnic imagery; the picture above keeps its meaning in respectful, modern terms."` May be tailored per degree if a more specific line reads better, but keep it short (one sentence) and matter-of-fact, never a lecture. Omit the field entirely on every other degree -- do not add an empty string. |

Minimal example (values shortened for illustration; real entries are
full prose):

```python
ENTRIES = [
    {"degree": 1, "image": "A woman rises from the sea; a seal surfaces and embraces her.",
     "meaning": "This is the first degree of the entire zodiac...",
     "colors": "A planet or point at Aries 1 begins its whole expression here...",
     "reflection": "What in you is only now breaking the surface...?"},
    # ... degrees 2 through 30, in order
]
```

## Correctness and copyright discipline (applies to every sign, not just Aries)

**CORRECTNESS:** the degree -> symbol mapping (the `image` field) must be
the canonical Jones/Wheeler 1925 Sabian symbol for that exact degree,
cross-verified against multiple independent published sources — never
generated, guessed, or paraphrased from memory. Fewer verified degrees
beats any guessed ones: a sign file with fewer than 30 verified entries
should not be written at all yet (the generator will correctly leave the
sign as "Coming soon" until all 30 are present and valid — see below —
but a *partial, unverified* file sitting in this folder is worse than no
file, since a careless future edit could complete it with guesses. Do not
commit a sign file until all 30 degrees are individually verified).

**COPYRIGHT:** `image` must be a plain, original restatement of the
traditional degree picture, never a verbatim quote of Jones (1953) or
Rudhyar (1973). `meaning`, `colors`, and `reflection` must be original
Twelve Rooms interpretation, written fresh — never copied or lightly
adapted from Jones, Rudhyar, or any other published source.

## Validation the generator applies

A sign is treated as **LIVE** (pages generated, hub card links out) only
if its data file:

1. exists at `bin/sabian_data/<slug>.py`,
2. exports `ENTRIES` as a list of exactly 30 dicts,
3. has `degree` values that are exactly `1, 2, 3, ... 30` in order, and
4. every entry has all five required fields (`degree`, `image`,
   `meaning`, `colors`, `reflection`).

If a file is missing, or present but fails any of those checks, the sign
renders as "Coming soon" in the hub instead of erroring the whole build —
so an in-progress or broken sign file never blocks the other signs from
building. The generator prints a warning to stderr when a file exists but
fails validation, so a broken file doesn't fail silently.

## Canonical sign order

The 12 signs, in zodiac order (this table lives in `gen_sabian_pages.py`
as `CANONICAL_SIGNS` and does not need to change when adding a sign's
data — it already lists all 12):

| order | name        | slug          | glyph (with VS15) |
|-------|-------------|---------------|--------------------|
| 1     | Aries       | `aries`       | ♈︎ |
| 2     | Taurus      | `taurus`      | ♉︎ |
| 3     | Gemini      | `gemini`      | ♊︎ |
| 4     | Cancer      | `cancer`      | ♋︎ |
| 5     | Leo         | `leo`         | ♌︎ |
| 6     | Virgo       | `virgo`       | ♍︎ |
| 7     | Libra       | `libra`       | ♎︎ |
| 8     | Scorpio     | `scorpio`     | ♏︎ |
| 9     | Sagittarius | `sagittarius` | ♐︎ |
| 10    | Capricorn   | `capricorn`   | ♑︎ |
| 11    | Aquarius    | `aquarius`    | ♒︎ |
| 12    | Pisces      | `pisces`      | ♓︎ |

## Procedure to add a sign

1. Verify all 30 degree symbols for the sign against multiple independent
   published sources (never from memory, never generated).
2. Write original `meaning`, `colors`, and `reflection` prose for each of
   the 30 degrees, to the same depth and standard as `bin/sabian_data/aries.py`.
3. Create `bin/sabian_data/<slug>.py` exporting `SIGN` and `ENTRIES` in
   the format above. Use the slug and glyph from the canonical table.
4. Run `python3 bin/gen_sabian_pages.py` from the repo root (`webtools/`).
   This regenerates the hub, every live sign's index page, and every live
   sign's degree pages — it is safe to re-run any time, for any subset of
   signs present, in any order signs were added.
5. Spot-check the sign's index page and a couple of degree pages, and
   confirm the hub now shows the sign as live instead of "Coming soon."

No other file needs to change. Multiple signs can be written and dropped
into this folder in parallel by different people or agents, since each
sign's file is independent and the generator never needs edits to pick
up a new one.
