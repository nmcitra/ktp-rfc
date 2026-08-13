#!/bin/sh
# flip-format-spine.sh — the one coordination step of #78 that #108 staged
# rather than ran. Until this runs, rfcs-txt/ stays the hand-authored
# canonical set and rfc-src/ is derived from it (regenerate with
# worklog/ktp-spec/108-build-rfc-src.py after any rfcs-txt edit). After it
# runs, rfc-src/ is the single source: the five filed .txt are generated, the
# other 22 have no .txt, and every hand edit happens in rfc-src/.
#
# WHY THIS IS A SEPARATE STEP (recorded on nmcitra/ktp-rfc#108):
#   1. Deleting the 22 .txt breaks the ktp site's deep links —
#      ktp/src/data/nav.ts pins REPO_BRANCH="main" and ExternalSpecLink
#      builds rfcs-txt/ URLs. The site must repoint first (#78's named risk,
#      confirmed at nav.ts:41 on 2026-08-13).
#   2. Live parallel sessions carry unapplied edit rows into rfcs-txt/
#      (#109's nine, #90's seven — gated on the owed Mike Storm and Robin
#      messages). Flipping mid-flight forks the source.
#   3. The 22 summary pages in rfcs/ transclude rfcs-txt/*.txt inside
#      fenced blocks; they repoint to rfc-src markdown here, in one commit
#      with the deletions.
#
# Run when the frontier is quiet and the site repoint is merged:
#   scripts/flip-format-spine.sh --yes

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILED="ktp-core ktp-identity ktp-problems ktp-enforce ktp-conformance"

if [ "$1" != "--yes" ]; then
  sed -n '2,24p' "$0"
  exit 1
fi

if ! git -C "$ROOT" diff --quiet; then
  echo "working tree not clean — commit or stash first" >&2
  exit 1
fi

echo "1/4 regenerate rfc-src from rfcs-txt at HEAD (last pre-flip sync)"
python3 "$ROOT/../worklog/ktp-spec/108-build-rfc-src.py"

echo "2/4 generate the five filed I-Ds into rfcs-txt/"
"$ROOT/scripts/gen-rfc-txt.sh"

echo "3/4 delete the 22 non-filed .txt (they assert nothing now)"
for f in "$ROOT"/rfcs-txt/*.txt; do
  n="$(basename "$f" .txt)"
  case " $FILED " in
    *" $n "*) ;;
    *) git -C "$ROOT" rm -q "rfcs-txt/$n.txt" ;;
  esac
done

echo "4/4 repoint the 22 summary transclusions to rfc-src markdown"
python3 - "$ROOT" <<'EOF'
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
filed = {"ktp-core", "ktp-identity", "ktp-problems", "ktp-enforce",
         "ktp-conformance"}
for md in sorted((root / "rfcs").glob("ktp-*.md")):
    if md.stem in filed:
        continue
    t = md.read_text()
    t2 = re.sub(r'--8<-- "rfcs-txt/' + md.stem + r'\.txt"',
                f'--8<-- "rfc-src/{md.stem}.md"', t)
    if t2 != t:
        md.write_text(t2)
        print(f"  repointed rfcs/{md.stem}.md")
EOF

echo
echo "done. Now: update check-repo-hygiene.py (rfcs-txt -> generated),"
echo "run all gates, and commit as one change."
