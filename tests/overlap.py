"""Shared-sentence overlap between rendered pages.

overlap(a, b) = share of page a's distinct sentences that also appear,
verbatim, on page b. Only the page's own text counts: scripts, styles,
the site masthead and the shared footer link block are removed first,
since every page on the site carries those by design. Sentences are
compared verbatim by default; mask_numbers=True also treats sentences
that differ only in their digits as the same (the stricter reading)."""
import html as _html
import re

_DROP = [re.compile(p, re.S | re.I) for p in (
    r"<script\b.*?</script>", r"<style\b.*?</style>", r"<head\b.*?</head>",
    r'<div id="site-footer">.*?</div>\s*</main>', r'<footer\b.*?</footer>',
    r'<nav\b.*?</nav>')]
_BLOCK = re.compile(r"</?(?:p|li|td|th|tr|h[1-6]|div|section|ul|ol|table|dt|dd|br|summary|details)\b[^>]*>", re.I)
_TAG = re.compile(r"<[^>]+>")
_SPLIT = re.compile(r"(?<=[.!?])\s+")
_NUM = re.compile(r"\d+")


def sentences(page_html, mask_numbers=False):
    t = page_html
    for rx in _DROP:
        t = rx.sub(" ", t)
    t = _BLOCK.sub("\n", t)
    t = _html.unescape(_TAG.sub(" ", t))
    out = set()
    chunks = []
    for line in t.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            chunks.extend(_SPLIT.split(line))
    for s in chunks:
        s = s.strip()
        if len(s.split()) < 4:
            continue
        out.add(_NUM.sub("#", s) if mask_numbers else s)
    return out


def overlap(a_html, b_html, mask_numbers=False):
    a, b = sentences(a_html, mask_numbers), sentences(b_html, mask_numbers)
    return len(a & b) / len(a) if a else 0.0


def family_overlap(pages, mask_numbers=False):
    """Mean overlap of each page with its neighbour in the list (the pair a
    reader or crawler is most likely to compare), and the max pair."""
    vals = [overlap(pages[i], pages[i + 1], mask_numbers) for i in range(len(pages) - 1)]
    return sum(vals) / len(vals), max(vals)
