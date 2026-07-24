# Newsletter Signup — Setup Needed Before Launch (STAGED, NOT LIVE)

Status as of Jul 24 2026: the code is built and committed to the working tree,
but the list is **not live**. Nothing sends until Shannon creates the Beehiiv
publication and sets two env vars in Vercel. Until then `/api/subscribe`
answers `503 {"error": "list not open yet"}` for every real signup, so it is
safe to deploy before the account exists.

## What's built

- **Capture block** — `TR.signupHTML()` / `TR.initSignup()` in `tools.js`,
  styled in `tools.css` (`.signup`, `.signup-form`, `.hp-field`). Rendered on:
  - `/` (homepage, after the "whole chart" CTA)
  - `/natal-chart` (inline, right after a chart renders — highest-intent moment)
  - `/forecast` (dedicated landing page)
  - Every page's shared footer links to `/forecast`.
- **Honeypot** — a `website` field, visually hidden off-screen (not
  `display:none`, since some bots skip fields hidden that obviously) via the
  `.hp-field` class. A real visitor never sees or fills it. If the server
  receives it non-empty, `api/subscribe.py` answers the same `200 {"ok": true}`
  a genuine signup gets and never calls Beehiiv — bots get a fake success
  instead of a tell.
- **`api/subscribe.py`** — Vercel Python function, matches the site's other
  `api/*.py` handlers (`BaseHTTPRequestHandler`, stdlib only, no new deps in
  `requirements.txt`). Validates the email with a regex, checks the honeypot,
  then POSTs to Beehiiv v2. Reads only `os.environ`, no hardcoded key anywhere.
  It's written provider-agnostic (Beehiiv first, Resend as a fallback path if
  those env vars ever exist instead) so the file survives either platform
  call without a rewrite, but Beehiiv is the one Shannon actually needs to
  set up per her Jul 23 direction — the Resend path is dormant unless
  `RESEND_API_KEY`/`RESEND_AUDIENCE_ID` get set.

## What Shannon needs to do

### 1. Create the Beehiiv publication
- Sign up (or log in) at beehiiv.com — the free tier covers this.
- Create a publication named **The Twelve Rooms — Monthly Sky Forecast**
  (or whatever title she prefers; it's what subscribers see as the sender name).
- Grab two values from the Beehiiv dashboard:
  - **Publication ID** — under Settings → Publication (starts with `pub_`).
  - **API key** — under Settings → Integrations → API (starts with a secret
    token; treat it like a password, never paste it into chat, a doc, or a
    commit).

### 2. Set the two env vars in Vercel
In the Vercel dashboard for this project (or `vercel env add`, run by Shannon,
not this session — no `vercel` commands were run here):
| Variable | Value | Scope |
|---|---|---|
| `BEEHIIV_API_KEY` | the API key from step 1 | Production (and Preview if she wants to test signups pre-launch) |
| `BEEHIIV_PUBLICATION_ID` | the `pub_...` ID from step 1 | same scopes |

Neither var exists yet. Until both are set, every real signup gets the
graceful `503 "list not open yet"` response — the capture block is visible
but functionally a no-op, which is the intended safe-before-launch state.

### 3. Deploy
This session made source changes only — no deploy, no `vercel` command, no
git push. When Shannon is ready:
```
vercel --scope shanjoy          # preview, verify the env vars took
vercel --prod --scope shanjoy   # production
```
(Per the repo's own README deploy section.) Verify end-to-end by submitting
a real email on `/forecast` against the preview deploy once the env vars are
set, and confirm it appears as a subscriber in the Beehiiv dashboard.

## What this session verified locally (no network)
- `python3 -m py_compile api/subscribe.py` — passes.
- The capture markup (`TR.signupHTML()` call + `#signup-slot`) is present in
  `index.html`.
- The honeypot field and its hiding rule are present in `tools.js`/`tools.css`.

What this session could **not** verify, because it requires the live keys and
a deploy (both Shannon's to do): the actual Beehiiv API round trip, the
honeypot's real-world bot-catch rate, and the double opt-in / welcome-email
experience a real subscriber sees.
