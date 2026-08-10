#!/usr/bin/env python3
"""QA gate for the crawlability of The Twelve Rooms.

Re-runs the measurement that produced the 2026-08-10 diagnosis, so the
numbers in that diagnosis can be re-tested rather than believed.

It builds the link graph from server-rendered HTML only. Anchors inside
`<script>` blocks are stripped first, on purpose: that is the graph Google
walks on the raw HTML pass, which is the pass that decides what gets
crawled and when. Before this branch, that graph had no sitewide links at
all, because the entire navigation was assembled client side.

Checks, each of which failed on main at the time of writing:
  1. Every static page carries the server-rendered footer link block.
  2. api/_seo/crawl.py and seo-window.json name the same indexable window.
  3. Every sitemap URL carries a lastmod.
  4. No sitemap URL is orphaned from the server-rendered graph.
  5. Nothing in the sitemap sits deeper than MAX_DEPTH clicks from the home
     page.
  6. Every electional page has at least MIN_ELECTIONAL_INBOUND inbound
     links from other pages, not counting its own canonical.

Usage: python3 bin/check-seo.py
Exit status 0 when every check passes, 1 otherwise.
"""
import collections
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api" / "_seo"))
import crawl  # noqa: E402

BASE = "https://thetwelverooms.com"
MAX_DEPTH = 3
MIN_ELECTIONAL_INBOUND = 3

SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.S | re.I)
HREF_RE = re.compile(r'<a\b[^>]*?href\s*=\s*"([^"]+)"', re.I)
LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
URL_RE = re.compile(r"<url>.*?</url>", re.S)

# Paths served by a rewrite in vercel.json rather than by a file on disk.
DYNAMIC_PREFIXES = ("/moon/", "/void-of-course-moon/", "/saturn-return/")


def normalise(href):
    href = href.split("#")[0].split("?")[0]
    if href.startswith(BASE):
        href = href[len(BASE):]
    if not href.startswith("/"):
        return None
    if href.endswith(".html"):
        href = href[:-5]
    if len(href) > 1 and href.endswith("/"):
        href = href[:-1]
    return href or "/"


def page_paths():
    for f in sorted(ROOT.glob("*.html")):
        yield ("/" if f.name == "index.html" else "/" + f.stem), f
    for f in sorted(ROOT.glob("sabian-symbols/*.html")):
        yield "/sabian-symbols/" + f.stem, f


def build_graph():
    """Outbound links per page, from server-rendered anchors only."""
    out = {}
    for path, f in page_paths():
        body = SCRIPT_RE.sub(" ", f.read_text(encoding="utf-8", errors="replace"))
        links = {normalise(h) for h in HREF_RE.findall(body)}
        out[path] = {h for h in links if h and h != path}
    return out


def footer_outlinks():
    """The per-date and per-year pages are rendered by Python, not files.

    Model them from the renderers: each one emits the shared footer, and a
    dated page also links its neighbours inside the indexable window, so the
    graph reaches them the way a crawler would.
    """
    return {h for h in (normalise(a) for a in HREF_RE.findall(crawl.FOOTER_HTML)) if h}


def main():
    failures = []
    notes = []

    # 1. server-rendered footer on every static page
    no_footer = [p for p, f in page_paths()
                 if "footer-nav" not in f.read_text(encoding="utf-8", errors="replace")]
    if no_footer:
        failures.append(f"{len(no_footer)} pages ship no server-rendered footer, "
                        f"first: {no_footer[:3]}")
    else:
        notes.append(f"footer: server-rendered on all {len(list(page_paths()))} static pages")

    # 2. window constants agree
    window = json.loads((ROOT / "seo-window.json").read_text())
    if (date.fromisoformat(window["index_from"]) != crawl.INDEX_FROM
            or date.fromisoformat(window["index_to"]) != crawl.INDEX_TO):
        failures.append(
            f"indexable window disagrees: seo-window.json says "
            f"{window['index_from']}..{window['index_to']}, api/_seo/crawl.py says "
            f"{crawl.INDEX_FROM}..{crawl.INDEX_TO}")
    else:
        notes.append(f"indexable window: {crawl.INDEX_FROM} to {crawl.INDEX_TO}, "
                     f"agreed by seo-window.json and api/_seo/crawl.py")

    # 3. sitemap lastmod on every URL
    sitemap = (ROOT / "sitemap.xml").read_text()
    entries = URL_RE.findall(sitemap)
    urls = [normalise(u) for u in LOC_RE.findall(sitemap)]
    without_lastmod = [e for e in entries if "<lastmod>" not in e]
    if without_lastmod:
        failures.append(f"{len(without_lastmod)} of {len(entries)} sitemap URLs have no lastmod")
    else:
        notes.append(f"sitemap: {len(entries)} URLs, all carrying lastmod")

    # sitemap must stay inside the indexable window
    outside = []
    for u in urls:
        m = re.match(r"^/(?:moon|void-of-course-moon)/(\d{4}-\d{2}-\d{2})$", u)
        if m and not crawl.in_index_window(date.fromisoformat(m.group(1))):
            outside.append(u)
    if outside:
        failures.append(f"{len(outside)} sitemap URLs fall outside the indexable "
                        f"window and would be served noindex, first: {outside[:3]}")

    # 4 and 5. orphans and depth, over the server-rendered graph
    out = build_graph()
    footer_links = footer_outlinks()
    for u in urls:
        if u.startswith(DYNAMIC_PREFIXES) and u not in out:
            out[u] = set(footer_links)
            m = re.match(r"^(/moon|/void-of-course-moon)/(\d{4}-\d{2}-\d{2})$", u)
            if m:
                d = date.fromisoformat(m.group(2))
                for nb in (d.toordinal() - 1, d.toordinal() + 1):
                    nbd = date.fromordinal(nb)
                    if crawl.in_index_window(nbd):
                        out[u].add(f"{m.group(1)}/{nbd.isoformat()}")

    depth, queue = {"/": 0}, collections.deque(["/"])
    while queue:
        u = queue.popleft()
        for v in out.get(u, ()):
            if v not in depth:
                depth[v] = depth[u] + 1
                queue.append(v)

    orphans = [u for u in urls if u not in depth]
    if orphans:
        failures.append(f"{len(orphans)} sitemap URLs are unreachable from / over "
                        f"server-rendered links, first: {orphans[:3]}")
    else:
        notes.append(f"reachability: all {len(urls)} sitemap URLs reachable from /")

    too_deep = [u for u in urls if depth.get(u, 99) > MAX_DEPTH]
    if too_deep:
        failures.append(f"{len(too_deep)} sitemap URLs sit deeper than {MAX_DEPTH} "
                        f"clicks from /, first: {too_deep[:3]}")
    dist = collections.Counter(depth.get(u, "unreachable") for u in urls)
    notes.append("depth from /: " + ", ".join(
        f"{k}={v}" for k, v in sorted(dist.items(), key=lambda x: (x[0] == "unreachable", x[0]))))

    # 6. inbound links to the gate-metric pages
    inbound = collections.Counter()
    for src, dests in out.items():
        for dst in dests:
            inbound[dst] += 1
    electional = sorted(u for u in urls if u.startswith("/best-"))
    thin = [(u, inbound[u]) for u in electional if inbound[u] < MIN_ELECTIONAL_INBOUND]
    if thin:
        failures.append(f"{len(thin)} electional pages have fewer than "
                        f"{MIN_ELECTIONAL_INBOUND} inbound links, first: {thin[:3]}")
    if electional:
        counts = [inbound[u] for u in electional]
        notes.append(f"electional pages: {len(electional)}, inbound links "
                     f"min={min(counts)} median={sorted(counts)[len(counts) // 2]} "
                     f"max={max(counts)}")

    for n in notes:
        print(f"  ok   {n}")
    for f in failures:
        print(f"  FAIL {f}")
    print()
    print("PASS" if not failures else f"FAIL: {len(failures)} check(s) failed")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
