#!/usr/bin/env python3
"""Put the server-rendered sitewide footer into every static HTML page.

Why this exists, measured 2026-08-10: every page on the site shipped an
empty `<div id="site-footer"></div>` and an empty `<div id="masthead">`,
with the whole navigation assembled client side by tools.js. On the raw
HTML pass, the one Google uses to decide what to crawl and when, no page on
the domain carried a single sitewide link. A breadth-first walk of the
server-rendered link graph put 360 Sabian pages at depth 4, 11 of the 24
electional pages at depth 3, and left /about and /forecast unreachable.

This script fills the footer slot with the real link block from
api/_seo/crawl.py. Same markup the API renderers emit, so a crawler sees the
same footer on a static page and on a per-date page. tools.js now only
injects its own copy when the slot is still empty, so this markup survives.

Idempotent: a page whose footer slot is already filled is left alone.
Usage: python3 bin/apply-static-footer.py [--check]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_seo"))
import crawl  # noqa: E402

EMPTY = '<div id="site-footer"></div>'
FILLED = f'<div id="site-footer">{crawl.FOOTER_HTML}</div>'
CHECK = "--check" in sys.argv


def targets():
    yield from sorted(ROOT.glob("*.html"))
    yield from sorted(ROOT.glob("sabian-symbols/*.html"))


def main():
    changed, already, missing = [], [], []
    for f in targets():
        s = f.read_text(encoding="utf-8")
        if EMPTY in s:
            changed.append(f)
            if not CHECK:
                f.write_text(s.replace(EMPTY, FILLED), encoding="utf-8")
        elif 'id="site-footer"' in s and "footer-nav" in s:
            already.append(f)
        else:
            missing.append(f)

    verb = "would fill" if CHECK else "filled"
    print(f"{verb}: {len(changed)}   already had the footer: {len(already)}   "
          f"no footer slot: {len(missing)}")
    for f in missing:
        print(f"  no slot: {f.relative_to(ROOT)}")
    if CHECK and changed:
        print("FAIL: pages are still shipping an empty footer slot")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
