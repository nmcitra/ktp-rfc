#!/usr/bin/env bash
# check-rfc-sync.sh — keep rfcs/*.md and rfcs-txt/*.txt from drifting apart.
#
# Two checks:
#   1. Version parity (always): the "**Version** | X.Y" declared in each
#      rfcs/<name>.md must equal the "Version: X.Y" header in
#      rfcs-txt/<name>.txt.
#   2. Touch parity (only when a base ref is given, e.g. in PR CI): any
#      commit range that modifies one side of a pair must modify the
#      other side too. Catches content drift that never bumps a version.
#
# Usage:
#   scripts/check-rfc-sync.sh              # version parity only
#   scripts/check-rfc-sync.sh origin/main  # + touch parity vs that ref
#
# NOTE (2026-07-18, corrected diagnosis): the ten .txt files touched by
# branch commit 59cb0fa (2026-03-26) are NOT stale — they already carry
# the expanded specs. 59cb0fa holds the kramdown-rfc (IETF Internet-
# Draft) SOURCE versions of those same specs, stranded on
# chore/docs-nav-refresh and slightly newer in places (e.g. relational's
# THRIVING row, governance's PROHIBITED row). Rescuing those sources
# onto main is tracked separately.

set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

# ── Check 1: version parity ─────────────────────────────────────────────
for md in rfcs/*.md; do
  base=$(basename "$md" .md)
  [ "$base" = "index" ] && continue
  txt="rfcs-txt/$base.txt"
  if [ ! -f "$txt" ]; then
    echo "FAIL: $md has no matching $txt"
    fail=1
    continue
  fi
  mdv=$(grep -m1 -oE '\*\*Version\*\* \| [0-9]+\.[0-9]+' "$md" | grep -oE '[0-9]+\.[0-9]+' || true)
  txtv=$(grep -m1 -oE 'Version: [0-9]+\.[0-9]+' "$txt" | grep -oE '[0-9]+\.[0-9]+' || true)
  if [ -z "$mdv" ] || [ -z "$txtv" ]; then
    echo "WARN: could not parse version in ${mdv:+$txt}${mdv:-$md}"
    continue
  fi
  if [ "$mdv" != "$txtv" ]; then
    echo "FAIL: version mismatch for $base — md=$mdv txt=$txtv"
    fail=1
  fi
done

# ── Check 2: touch parity (PR mode) ─────────────────────────────────────
# Escape hatch: a commit in the range whose message contains [rfc-sync]
# marks a deliberate one-sided catch-up (bringing a stale side back into
# parity). Version parity above still applies.
if [ $# -ge 1 ]; then
  baseref="$1"
  if git log --format=%s "$baseref"...HEAD | grep -q '\[rfc-sync\]'; then
    echo "NOTE: [rfc-sync] catch-up commit in range — skipping touch parity"
    exit "$fail"
  fi
  changed=$(git diff --name-only "$baseref"...HEAD -- 'rfcs/*.md' 'rfcs-txt/*.txt' || true)
  for f in $changed; do
    case "$f" in
      rfcs/index.md) continue ;;
      rfcs/*.md)
        base=$(basename "$f" .md)
        if ! echo "$changed" | grep -q "^rfcs-txt/$base.txt$"; then
          echo "FAIL: $f changed but rfcs-txt/$base.txt did not — sync the txt or bump both versions"
          fail=1
        fi ;;
      rfcs-txt/*.txt)
        base=$(basename "$f" .txt)
        if ! echo "$changed" | grep -q "^rfcs/$base.md$"; then
          echo "FAIL: $f changed but rfcs/$base.md did not — sync the md or bump both versions"
          fail=1
        fi ;;
    esac
  done
fi

if [ "$fail" -eq 0 ]; then
  echo "OK: rfcs/ and rfcs-txt/ are in sync"
fi
exit "$fail"
