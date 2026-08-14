#!/bin/sh
# gen-rfc-txt.sh — generate the five Internet-Draft-formatted specifications from rfc-src/.
#
# Only the I-D-formatted set gets a .txt (#78 decision 3): generating one asserts
# Internet-Draft status, so the other 22 rfc-src sources render as markdown
# and never pass through here.
#
#   scripts/gen-rfc-txt.sh            generate into rfcs-txt/
#   scripts/gen-rfc-txt.sh --check    generate to a temp dir; after the
#                                     format-spine flip (rfcs-txt/ holds only
#                                     the five generated files) diff against
#                                     rfcs-txt/ and fail on any difference —
#                                     #78's generate-and-diff gate. Before
#                                     the flip, only verifies generation.
#
# Reproducibility: each rfc-src front matter pins a full `date:`, which fixes
# the derived Expires: header — verified byte-identical across build runs
# (#108). Bump the date when the content changes.

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KRAMDOWN="${KRAMDOWN_RFC:-$HOME/.gem/ruby/4.0.0/bin/kramdown-rfc}"
XML2RFC="$ROOT/venv/bin/xml2rfc"
FILED="ktp-core ktp-identity ktp-problems ktp-enforce ktp-conformance"

MODE="generate"
[ "$1" = "--check" ] && MODE="check"

OUTDIR="$ROOT/rfcs-txt"
if [ "$MODE" = "check" ]; then
  OUTDIR="$(mktemp -d)"
fi

for n in $FILED; do
  "$KRAMDOWN" --v3 "$ROOT/rfc-src/$n.md" > "$OUTDIR/$n.xml.tmp" 2>"$OUTDIR/$n.kram.log"
  "$XML2RFC" --text "$OUTDIR/$n.xml.tmp" -o "$OUTDIR/$n.txt" >/dev/null 2>"$OUTDIR/$n.xml.log"
  rm -f "$OUTDIR/$n.xml.tmp" "$OUTDIR/$n.kram.log" "$OUTDIR/$n.xml.log"
  echo "  generated $n.txt"
done

if [ "$MODE" = "check" ]; then
  TXT_COUNT=$(ls "$ROOT/rfcs-txt"/*.txt 2>/dev/null | wc -l | tr -d ' ')
  if [ "$TXT_COUNT" -gt 5 ]; then
    echo "pre-flip: rfcs-txt/ still holds the hand-authored set ($TXT_COUNT files);"
    echo "generation verified, diff skipped. The diff gate arms at the flip."
    exit 0
  fi
  RC=0
  for n in $FILED; do
    if ! diff -q "$OUTDIR/$n.txt" "$ROOT/rfcs-txt/$n.txt" >/dev/null 2>&1; then
      echo "STALE: rfcs-txt/$n.txt differs from regenerated output" >&2
      RC=1
    fi
  done
  [ $RC -eq 0 ] && echo "rfcs-txt/ in step with rfc-src/ (five I-D-formatted specs)"
  exit $RC
fi
