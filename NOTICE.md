# The Twelve Rooms — Free Web Tools: Notices & Attribution

This web application is free software, released under the GNU Affero
General Public License v3.0 (see LICENSE). Because it is offered over a
network, the AGPL requires that its complete corresponding source be
available to users. The source is published at:

  https://github.com/shannonjoy/twelverooms-tools

## Astronomical engine

Planetary and house calculations are performed with the **Swiss
Ephemeris** by Astrodienst AG (https://www.astro.com/swisseph/), via the
`pyswisseph` Python binding. The Swiss Ephemeris is dual-licensed under
the AGPL or a commercial license; this deployment complies via the AGPL
path by making its own complete source available under the same license.

Swiss Ephemeris derives its data from NASA JPL ephemerides. This project
uses the built-in Moshier semi-analytic model (no external data files).

## City database

`api/_data/cities.csv` is derived from the GeoNames geographical database
(https://www.geonames.org/), licensed under Creative Commons Attribution
4.0 (CC-BY 4.0). Columns retained: name, admin1, country, latitude,
longitude, timezone.

## What this covers

The four tools (Moon status, natal chart, synastry grid, electional
window finder) and their shared astrology engine modules
(`compute_sky`, `compute_factsheet`, `gen_wheel`, `synastry`,
`electional`) are all AGPL-3.0. The Twelve Rooms brand identity, name,
wordmark, the XII medallion mark, palette, and marketing copy are NOT
covered by the AGPL and remain the property of Shannon Owens / The
Twelve Rooms. Reuse the code freely under the AGPL; do not reuse the
brand.
