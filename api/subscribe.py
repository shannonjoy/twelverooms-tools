"""POST /api/subscribe {email, website, source} — Monthly Sky Forecast list opt-in.

Provider-agnostic on purpose: the platform decision (Beehiiv free tier per
Shannon's Jul 23 direction vs the Resend MVP per email-list-strategy-0721)
is settled by which env vars exist, checked in this order:
  1. BEEHIIV_API_KEY + BEEHIIV_PUBLICATION_ID  -> Beehiiv subscription
  2. RESEND_API_KEY + RESEND_AUDIENCE_ID       -> Resend audience contact
With neither configured the endpoint answers 503 ("list not open yet"), so
it is safe to deploy before the account exists. Nothing is stored here; the
address goes straight to the platform. The front-end module (tools.js
signupHTML/initSignup) stays hidden until SIGNUP_ON flips, so the 503 path
is a belt-and-suspenders guard, not a user-visible state.

`website` is a honeypot: a real visitor never sees or fills that field
(tools.css hides it off-screen, not display:none). If it arrives non-empty,
this is a bot filling every field it can see in markup -- we answer with the
same 200 {"ok": True} a genuine signup gets (never call the provider, never
tip the bot off that it was caught) rather than a visible rejection.
"""
import json
import os
import re
import urllib.request
from http.server import BaseHTTPRequestHandler

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _post(url, headers, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def subscribe(email, source):
    """Returns True (added), False (platform rejected), None (unconfigured)."""
    bh_key = os.environ.get("BEEHIIV_API_KEY")
    bh_pub = os.environ.get("BEEHIIV_PUBLICATION_ID")
    if bh_key and bh_pub:
        status = _post(
            f"https://api.beehiiv.com/v2/publications/{bh_pub}/subscriptions",
            {"Authorization": f"Bearer {bh_key}"},
            {"email": email, "reactivate_existing": True,
             "utm_source": source or "site"})
        return status < 300
    rs_key = os.environ.get("RESEND_API_KEY")
    rs_aud = os.environ.get("RESEND_AUDIENCE_ID")
    if rs_key and rs_aud:
        status = _post(
            f"https://api.resend.com/audiences/{rs_aud}/contacts",
            {"Authorization": f"Bearer {rs_key}"},
            {"email": email, "unsubscribed": False})
        return status < 300
    return None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
            email = str(body.get("email") or "").strip()[:254]
            website = str(body.get("website") or "").strip()  # honeypot
            source = str(body.get("source") or "")[:40]
            if website:
                # Bot filled the hidden field. Answer like a real signup so
                # nothing tips it off; never touch the provider.
                code, out = 200, {"ok": True}
            elif not EMAIL_RE.match(email):
                code, out = 400, {"error": "invalid email"}
            else:
                ok = subscribe(email, source)
                if ok is None:
                    code, out = 503, {"error": "list not open yet"}
                elif ok:
                    code, out = 200, {"ok": True}
                else:
                    code, out = 502, {"error": "platform rejected the request"}
        except Exception as e:  # malformed JSON, network trouble
            code, out = 500, {"error": str(e)[:200]}
        b = json.dumps(out).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
