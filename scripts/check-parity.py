#!/usr/bin/env python3
"""check-parity.py — the summary/source drift gate, now closed by construction.

Formerly a word-drift tripwire between rfcs/*.md (a hand-authored MkDocs
summary) and rfc-src/*.md (the kramdown-rfc source): it flagged a summary
asserting a term — physics, gravity, tensor — that the source didn't carry.
One-directional by design, and the direction it didn't check is what broke
it: rfcs/ went stale missing the entire Limits section (L1-L14) and nothing
here could see an omission, only an over-claim.

rfcs/ was retired 2026-08-14. rfcs-md/ replaces it as GENERATED output —
mechanically derived from rfc-src/ by gen-rfcs-md.py, so drift in either
direction is impossible by construction rather than merely gated. This
script is now a thin, stable entry point onto that generator's own
--check, kept so CI and the release paperwork naming "check-parity.py"
as one of the four gates don't need to be hunted down and re-pointed.

Usage: python3 scripts/check-parity.py
Exit 0 if rfcs-md/ matches what rfc-src/ generates, 1 otherwise.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "gen-rfcs-md.py"), "--check"])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
