# Daily Horoscope Feature — Implementation Guide

## Overview

A personalized daily horoscope tool that computes exact transit times for any date based on a user's natal chart. Users enter their birth details once, pick a date, and receive a narrative horoscope with:

- **Exact times** for fast-moving planets (Moon, Sun, Mercury, Venus, Mars)
- **Timeline view** ("Your Day, Hour by Hour") organized chronologically
- **Specific descriptions** of what each transit means for them
- **Action windows** suggesting best hours for different types of work
- Full **Twelverooms design system** (navy + gold, vintage-feminine, Apple-minimal)

## Architecture

### Files Added

1. **`daily-horoscope.html`**
   - Interactive form for birth data input (with persistent storage via `TR.rememberBirth()`)
   - Date picker for horoscope dates (past, present, or future)
   - Results display area with narrative horoscope rendering
   - Integrated into Twelverooms nav under "Your chart" → "Daily horoscope"

2. **`api/horoscope.py`**
   - Python backend endpoint: `POST /api/horoscope`
   - Input: `{date, time?, tz, lat, lon, horoscope_date}`
   - Output: Personalized transit data with exact times and descriptions
   - Uses Swiss Ephemeris (via `engines` module) for all calculations

3. **`tools.js`** (modified)
   - Added `/daily-horoscope` link to navigation

## How It Works

### User Flow

1. User visits `/daily-horoscope`
2. Enters birth date, time (optional), and birthplace
3. System remembers birth data for future sessions
4. Picks a date using the calendar picker
5. Clicks "Read My Day"
6. Backend computes transits for that date
7. Frontend renders personalized horoscope narrative

### Data Flow

```
User Input (birth data + date)
    ↓
HTML Form (daily-horoscope.html)
    ↓
fetch("/api/horoscope", {...})
    ↓
Backend (api/horoscope.py)
    ├─ Parse birth data
    ├─ Compute natal chart (engines.compute_natal)
    ├─ Compute transits for the specified date
    └─ Return transit data with times + descriptions
    ↓
Frontend Render
    ├─ Hero section: day's overarching energy
    ├─ Featured transit (the main story)
    ├─ Timeline: all transits chronologically
    ├─ Action windows: best hours for different work
    └─ Background context
```

## Implementation Status

### ✅ Complete

- HTML page layout and form
- Navigation integration
- API endpoint skeleton with proper request/response handling
- Design system integration (Twelverooms styling)
- Frontend rendering logic

### 🔄 Needs Completion

1. **Backend Transit Computation** (`api/horoscope.py`)
   - The `_find_moon_aspects()` method needs to:
     - Iterate through the day (hourly or finer resolution)
     - Calculate Moon's position at each point
     - Check for aspects (conjunction, sextile, square, trine, opposition) with natal points
     - Return exact times for each aspect
     - Flag void-of-course status
   
   - The `_find_body_aspects()` method needs to:
     - Calculate positions of Sun, Mercury, Venus, Mars transiting through the day
     - Check for major aspects to natal planets/angles
     - For fast movers, compute exact minute of perfection
     - For slower planets, mark as "in orb, no exact time"

2. **Aspect Descriptions** (`_moon_aspect_description` and `_body_aspect_description`)
   - Expand the dictionaries with interpretations for all possible combinations
   - Currently has only a few examples; needs ~40-50 curated descriptions
   - Should match the tone in the prototype (personal, actionable, not generic)

3. **Narrative Generation** (frontend, `renderHoroscope()`)
   - Currently hardcoded example text ("Mars Square MC", "You're fired up...")
   - Should dynamically generate:
     - "Today's Sky" summary based on featured transit
     - "How to Work With Today" windows based on computed times
     - Featured transit selection (highest-orb or angle contact)

4. **Error Handling & Validation**
   - Birth time validation (reject times outside 00:00-23:59)
   - Timezone validation (verify against IANA tz database)
   - Date range validation (allow reasonable past/future range)
   - API error messages should be user-friendly

## Extending the Feature

### Phase 2: Themes & Personalization

- Store user birth data to Notion for repeat visitors
- Allow saving favorite dates/horoscopes
- Email delivery of daily horoscope at chosen time
- Week-ahead and month-ahead summaries

### Phase 3: Synastry & Comparison

- Compare two birth charts against a day's transits
- "You and them" daily compatibility score
- Couple's daily forecast

### Phase 4: Planetary Hours

- Integrate with existing planetary hours tool
- Show which planetary hour overlaps each transit
- Suggest optimal times based on both transit + planetary hour

## Testing Checklist

- [ ] Form remembers birth data between page loads
- [ ] Date picker accepts dates 1 year past to 1 year future
- [ ] API correctly parses birth data and horoscope date
- [ ] Natal chart computation works (compare against existing tools)
- [ ] Transit computation returns times within ±1 minute of ephemeris
- [ ] Moon transits show exact times
- [ ] Slower planets marked "in orb" when not exact today
- [ ] Void-of-course Moon correctly identified
- [ ] Timeline sorts by time (earliest to latest)
- [ ] Descriptions render without errors
- [ ] Mobile layout responsive
- [ ] Analytics tracking works (`TR.trackToolUse("daily-horoscope")`)

## Integration Notes

### With Existing Tools

- **Natal Chart**: Both use `engines.compute_natal()` — ensures consistency
- **Transit Timeline**: Daily horoscope is the per-day view; timeline shows 3-year view
- **Planetary Hours**: Both compute planetary hours; could show hourly rulers on daily
- **Moon Right Now**: Daily horoscope includes full Moon transit data; "now" is a special case

### With Paid Readings

- Free tool: computed sky + template interpretations
- Paid reading: human-written synthesis + guidance
- CTA at bottom directs to Etsy shop for "full year-ahead reading"

## Code Quality

- Follow existing patterns from `natal-chart.html` and `api/natal.py`
- No external dependencies beyond `pyswisseph` (already in use)
- All calculations deterministic (no randomness)
- Birth data never logged or stored (privacy by design)
- Timezone handling via `zoneinfo` (Python 3.9+)

## Future Enhancements

1. **PDF Export**: Save horoscope as shareable PDF
2. **Comparison Mode**: "Compare two people's transits for today"
3. **Retro Digest**: Weekly summary of retrograde activity
4. **Alert System**: "Notify me when Venus enters my 7th house" or "Big transit day"
5. **Aspect Strength**: Visual bar showing orb and exact moment

---

## Questions?

This feature integrates deeply with the Swiss Ephemeris computations used throughout Twelverooms. Refer to:
- `api/_engines/compute_sky.py` for transit computation patterns
- `api/transits.py` for multi-year transit data structure
- `api/natal.py` for birth chart computation pattern
