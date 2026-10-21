"""Tagged links to the readings the Etsy shop actually sells.

Added 2026-10-21 (search plan, move 3). The date pages used to promise "a
full electional reading", which is not a product anywhere. Every link from
a date page now names a live listing, and every one carries the same UTM
shape so GA4 and Etsy stats can tell which page sent the visit:

    utm_source=thetwelverooms&utm_medium=referral&utm_campaign=<page>

Listing ids come from ~/orchestrator/ids.json (ventures.listing-*). The
registry wins: if an id there changes, change it here and in
bin/electional_pages.py, which carries the same table for the static pages.
"""
from urllib.parse import quote

LISTINGS = {
    "natal": "4539681166",       # The Natal Deep-Dive, $39
    "year_ahead": "4539692523",  # The Year-Ahead Reading, $45 (listing-solar-return)
    "chart_art": "4539697475",   # Natal Chart Art Print, $15
    "jupiter": "4539867141",     # The Jupiter Return Guide, $30
    "synastry": "4542152602",    # The Synastry Report (two charts)
    "saturn": "4542121325",      # The Saturn Return Report
    "bundle": "4542140694",      # Reading + Print Bundle, $55
}


def etsy_url(product, campaign):
    """Listing URL with the site's referral tags, HTML-attribute safe."""
    return (f"https://www.etsy.com/listing/{LISTINGS[product]}"
            f"?utm_source=thetwelverooms&amp;utm_medium=referral"
            f"&amp;utm_campaign={quote(campaign, safe='-')}")
