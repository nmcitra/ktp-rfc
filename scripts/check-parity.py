#!/usr/bin/env python3
"""check-parity.py — drift tripwire for rfcs/*.md vs rfc-src/*.md.

Repointed under #78/#108: rfc-src/ is the authored source, rfcs/*.md are the
MkDocs summary pages. (The docstring this replaced claimed "only 3 of 28
transclude their .txt" — that was false, all 27 transclude; #78 correction 2.
The real drift class is narrower: summary prose asserting what the normative
text does not carry — the `G ∝ Mass` failure this was written for.) This flags
terms that appear in a summary but not in its source.

Usage: python3 scripts/check-parity.py [--terms a,b,c]
Exit 0 always (report-only); prints findings.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD, TXT = os.path.join(ROOT, "rfcs"), os.path.join(ROOT, "rfc-src")
DEFAULT = ["physics", "gravity", "tensor", "mass", "momentum", "inertia",
           "heat", "velocity", "spacetime", "curvature", "thermodynamic"]


def main():
    terms = DEFAULT
    for i, a in enumerate(sys.argv):
        if a == "--terms" and i + 1 < len(sys.argv):
            terms = [t.strip() for t in sys.argv[i + 1].split(",") if t.strip()]
    findings = 0
    for f in sorted(os.listdir(MD)):
        if not f.endswith(".md") or f == "index.md":
            continue
        txt = os.path.join(TXT, f)
        if not os.path.exists(txt):
            print(f"  !! {f}: no rfc-src counterpart")
            findings += 1
            continue
        m = open(os.path.join(MD, f), errors="ignore").read().lower()
        x = open(txt, errors="ignore").read().lower()
        for t in terms:
            pat = r"\b" + re.escape(t) + r"\b"
            in_md, in_txt = len(re.findall(pat, m)), len(re.findall(pat, x))
            if in_md and not in_txt:
                print(f"  DRIFT {f}: '{t}' x{in_md} in summary, absent from rfc-src")
                findings += 1
    print(f"\n{findings} drift finding(s). Summaries must not assert what the RFC does not.")


if __name__ == "__main__":
    main()
