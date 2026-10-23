# The Twelve Rooms (thetwelverooms.com) — builder instructions

You are building thetwelverooms.com, the free astrology tools that feed the
Etsy shop. Scope is this repo only. Do not read or edit another venture's
repo, `~/orchestrator` or `~/.orchestrator`, except the Wire and Open Items
helpers and the pin generator Peggy owns
(`../brand-assets/gen_pins.py`, when the task is a pin). The rules in
`~/CLAUDE.md` apply here too. You are not Rory.

## Where truth lives

- Status, host, IDs: `~/ventures/sites/twelverooms/manifest.yaml`
- How to deploy: this file ("Going live")
- Identity: `~/ventures/sites/twelverooms/brand.md` — LOCKED. Never edit it; flag it.
- What to build, in rank order: `~/ventures/factory/backlog/twelverooms.json` (if missing, ask Tess)
- The traffic goal and its targets: `~/ventures/factory/strategy/twelverooms-traffic-goal.md`
- What has happened: `~/ventures/factory/ventures-log/twelverooms.md`
- IDs: `~/orchestrator/ids.json`

## Writing on this site

Dates and positions come from the engine (Swiss Ephemeris), never typed by
hand: regenerate a date page rather than edit it. Never "entertainment
purposes only", never "horoscope"; MC and Ascendant need a birth time, so say
so. Public copy states the current facts; no "Updated <month>" notes.

## Loop (site-creator ITERATE)

1. Name the item and what done looks like, and plan it. New features wait for
   Shannon's yes; fixes and follow-through on approved work don't (`~/CLAUDE.md`,
   "Close out what you find").
2. Branch `site-creator/<topic>-<mmdd>` off `main`. One item per branch.
3. Run the checks below. Commit site changes on their own.
4. Stop at the built artifact and report: branch, commit, what is built, what
   is NOT live.
5. Add a dated entry to the build log and post one Wire line.

Limits: at most three open branches, at most one built-not-live branch waiting
on Shannon. Delete a branch in the session that merges it. No new dependency
or env var without naming it in the report.

## Checks

`/usr/bin/python3 -m unittest discover -s tests`, then `/usr/bin/python3 bin/check-seo.py`.
Open each changed page in a browser; there is no build step.

## Measurement

GA4, Microsoft Clarity and a Search Console domain property are standard and
stay on. They are injected at runtime by `tools.js`, so a `curl` won't show
them; that is by design. Never write copy that promises limits on collection
("what we keep", "nothing else", "no analytics", "no cookies"), and never hold
a tag back over privacy copy.

## Going live

Host: Vercel, git-connected: a push to `main` on `shannonjoy/twelverooms-tools`
deploys. There is no standing authorization for this repo: nothing goes live
unless Shannon, live in the session, says to push or deploy. Show her the
commits going live first; the permission prompt is her yes; one yes = one push;
never `--force`. Then verify on https://thetwelverooms.com and log it.
Rollback: `git revert <sha>`, push (on her word).

After a deploy she approved, `node bin/indexnow.mjs <paths>` tells Bing what
changed (outbound; part of that same approval, never on its own).

## Wire

```bash
bash /Users/shannonowens/orchestrator/bin/wire.sh grep twelverooms 14
bash /Users/shannonowens/orchestrator/bin/wire.sh post site-creator twelverooms <what changed>
```

## Lessons

- 2026-10-21 · The Vercel Hobby plan allows 12 serverless functions and `api/*.py` already has 12. A 13th fails the deploy; fold a new endpoint into an existing function as a mode or parameter (big3 lives in saturn, solar return in natal).
- 2026-10-21 · Google held the site back for look-alike template pages (46 Saturn year pages shared 79% of their sentences). Before adding a page family, check how much text its pages share; under 20% is the bar we got to.
- 2026-10-22 · Hand-entered dates drift from the engine (the July 2027 wedding rows said April 8; the engine says April 13). Generate every date from bin/ scripts and fix the generator, not the page.
- 2026-10-22 · Tests that hard-code the sitemap count break on every new page. Update the count in the same commit as the page.
