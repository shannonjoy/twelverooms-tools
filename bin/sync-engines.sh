#!/bin/sh
# Copy the canonical engines into api/_engines for Vercel bundling.
# Re-run whenever an engine file changes. The copies are generated; never
# edit them here.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/api/_engines"
FACTSHEET="$HOME/orchestrator/ventures/astrology-storefront/factsheet"
LUNA="$HOME/orchestrator/luna-astrologer-plugin/luna-astrologer/scripts"
STUDIO="$HOME/orchestrator/apps/twelve-rooms-studio"

mkdir -p "$DEST"
for f in "$FACTSHEET/compute_factsheet.py" "$FACTSHEET/gen_wheel.py" \
         "$FACTSHEET/saturn_return.py" \
         "$LUNA/compute_sky.py" \
         "$STUDIO/synastry.py" "$STUDIO/electional.py"; do
  base="$(basename "$f")"
  { echo "# GENERATED COPY. Do not edit. Source: $f"
    echo "# Re-sync with bin/sync-engines.sh"
    cat "$f"; } > "$DEST/$base"
done
echo "synced $(ls "$DEST" | grep -c '\.py$') engine files -> api/_engines/"
