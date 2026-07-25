# Daily Horoscope — how it works

A daily reading computed against the visitor's own natal chart, for any date
within five years either way. Free, no account, same Swiss Ephemeris the rest of
the site runs on.

Live at `/daily-horoscope`. In the nav under **Your chart**, and on the homepage
tool grid.

## Files

| File | Role |
| --- | --- |
| `daily-horoscope.html` | The page: birth form, date picker, day navigation, rendering |
| `api/horoscope.py` | `POST /api/horoscope` — natal chart, the day's sky, the ledger |
| `api/_copy/horoscope_copy.py` | Every word of interpretation. Hand-written, not a synced engine |
| `tools.css` | `.ledger` / `.led-*`, `.lead-card`, `.win*` (search "daily horoscope") |

Nothing new was added to `api/_engines/` — `bin/sync-engines.sh` owns that
directory and overwrites its named files. The copy module lives in `api/_copy/`,
which Vercel still bundles via the existing `includeFiles: "api/_*/**"` glob.

## Request and response

```
POST /api/horoscope
{
  "date": "1988-09-01",        // birth date, required
  "time": "14:30",             // birth time, optional — see "untimed" below
  "tz":   "America/Chicago",   // birth timezone, required
  "lat":  41.8781,             // required
  "lon":  -87.6298,            // required
  "day":  "2026-07-25",        // the date to read, required
  "view_tz": "Europe/London"   // optional; times are rendered in this zone
}
```

`view_tz` defaults to the birth zone. The page sends the browser's zone from
`Intl.DateTimeFormat().resolvedOptions().timeZone`, so times land where the
reader actually is rather than where they were born.

Response (abridged):

```jsonc
{
  "day_label": "Saturday, July 25, 2026",
  "timezone": "America/Chicago",
  "timed": true,                    // false => no birth time, no angles
  "sky":  "The Moon runs through Sagittarius. Neptune sextile Pluto …",
  "arc":  "You are between the New Moon in Cancer on July 14 …",
  "featured": { … },                // the day's headline contact, or null
  "ledger":   [ { … }, … ],         // contacts that perfect today, clock order
  "background": { … } | null,       // one slow contact in orb, no time
  "windows":  [ { kind, label, anchor, text }, … ],
  "moon":     { sign, ingress_sign, ingress_local, house },
  "natal_used": { "Sun": "Virgo 9°13'", … },
  "note": "Computed for … with the Swiss Ephemeris …"
}
```

Every ledger entry carries `body`, `aspect`, `point`, `headline`, `symbol`,
`line`, `tone` (`flowing` / `hard` / `neutral`), `time_local`, `time_minutes`,
`retro`, `stationary`, `weight`.

Errors come back as `{"error": "..."}` with a 400 and a message written for a
human, because the page renders it verbatim.

## What the endpoint does

1. `cf.build_natal(order)` — the same call `/api/natal` makes, so the free chart
   and the daily reading can never disagree about where a planet is.
2. `_natal_points(natal)` — absolute longitudes for the ten planets, Chiron and
   the North Node. **ASC and MC only when the chart is timed.**
3. `cs.positions_at(jd_noon)` — the day's positions, retrograde and stationary
   flags, whole-sign house per body.
4. `cs.moon_aspects_to_natal(...)` — Moon contacts, each bisected to the minute.
5. `cs.slow_contacts_to_natal(...)` — everything else in orb; the inner planets
   that genuinely perfect today get a real time, the rest are marked in orb.
6. `build_ledger(...)` — see below.
7. `pick_featured(...)`, `hc.windows(...)`, `hc.sky_summary(...)`, `hc.arc_line(...)`.

Runs in about 0.1 s, well inside any Vercel function limit.

## The ledger rule

Only contacts that **actually perfect on the day** get a place on the clock. A
contact that is merely nearing belongs to the day it perfects, not to today, so
it is dropped — otherwise every reading silently fills up with the same slow
aspects for weeks and the timed ones stop standing out.

The single exception is `background`: the heaviest applying slow or stationary
contact, shown with **no time at all** under "Sitting over the day". That keeps
a Saturn opposition to the Midheaven visible without pretending it has a minute.

`pick_featured` takes the heaviest contact that perfects. Weight already favours
the angles, the Sun and Moon, the slower bodies, and the hard aspects, so a 3am
Moon contact does not outrank Saturn on the Midheaven. When nothing perfects at
all, the background line becomes the headline; when there is neither, the page
says so plainly instead of inventing something.

## Where the words come from

`api/_copy/horoscope_copy.py`, in two layers:

1. **Curated** — `MOON_LINES`, keyed `(aspect, point)`, covers the Moon's
   contacts to the nine points a day actually turns on; `BODY_LINES` covers a
   handful of non-Moon combinations the composer would undersell. The Moon is
   the fastest body, so these are the lines a reader feels on the clock. They
   are worth writing by hand.
2. **Composed** — everything else joins a `POINT_FEEL` phrase ("affection,
   taste, and what you value") to an `ASPECT_FRAME` ("friction around {x}; it
   asks for a choice, not a fix"), with the transiting body's theme in front.
   Coverage is total: any body against any point returns a sentence, including
   points the table has never heard of.

Retrograde and stationary are appended rather than baked in, because they change
what a contact *means*: a retrograde contact is a second pass, never a launch
signal, however flowing the aspect.

To improve the copy, add to `MOON_LINES` / `BODY_LINES`. Nothing else has to
change — the composer is the floor, not the ceiling.

## Untimed charts

No birth time means no Ascendant and no Midheaven; they move about a degree
every four minutes and cannot be guessed. `_natal_points` leaves them out, so no
angle contact can be reported, and the page shows a notice saying exactly that
rather than quietly returning a thinner reading. The natal Moon is also
approximate on an untimed chart, which shifts its contact times.

## The calendar

Three ways to move between days, all client-side against the same endpoint:

- **`.daynav`** — previous / today / next, rendered above and below the reading.
- **`.datebrowse` chips** — today, tomorrow, then twelve more days, with the
  current one marked `aria-current`.
- **The date field** in the form, for anything further out.

Each re-reads through `read(day)` and scrolls the result into view. `shiftDay`
walks local dates through a `Date` built from parts, so it never trips over the
UTC-parsing behaviour of `new Date("YYYY-MM-DD")`.

## Verified

Driven in Chromium against a local server mirroring Vercel's routing
(`cleanUrls`, `api/<name>.py` → `handler`):

- Form → API → render: 200, ledger populated, no console errors.
- Prev/next day and chip navigation both re-read and re-render.
- No horizontal scroll at 760 px or 390 px; the ledger stacks on mobile.
- `view_tz` shifts every time correctly (3:06 AM Chicago → 8:06 AM UTC).
- Untimed chart drops the angles and shows the notice.
- 120 dates scanned: the no-flowing-aspect branch fires on 5 of them and reads
  correctly ("no hour stands out as easy").
- Degenerate cases return safely: `pick_featured([], None) → None`,
  `build_ledger([], []) → ([], None)`, `windows([])` → the honest fallback.
- Bad timezone, bad date, out-of-range date, and unparseable coordinates all
  return a 400 with a message written for a reader.

One thing worth knowing when testing: `TR.birthDateField` replaces the birth
date input with three required Month / Day / Year controls and keeps the
original as a hidden field. Setting the hidden field alone leaves the visible
controls empty and native validation silently blocks submit. Fill the widget.

`bin/gen-sitemap.py` includes `/daily-horoscope` (daily, 0.9); re-run it to
regenerate `sitemap.xml`.

## Worth building next

- **Per-date pages.** `/daily-horoscope/YYYY-MM-DD` server-rendered like
  `/moon/:date`, for the collective half only — the personal half cannot be
  static. Real SEO surface for "horoscope for [date]".
- **Planetary hours overlay.** `api/planetary_hours.py` already computes them;
  showing which hour each contact falls in would deepen the timing without new
  math.
- **Email.** The Monthly Sky Forecast signup is already on the page; a daily
  send is the same ledger with a different renderer.
- **Widen `MOON_LINES`.** The outer-planet points still fall through to the
  composer. Curating those is pure copy work, no code.
