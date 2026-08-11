#!/usr/bin/env python3
"""Vocabulary tripwire for v2.0.0 "Gödel" — retired terms in normative text.

Success criteria have to be checkable or they are aspirations. Robin's own bar,
stated when he shipped two MUSTs: "both MUSTs because both are checkable." This
script is what makes "the vocabulary work is done" a fact instead of a feeling.

WHAT IS IN SCOPE
    rfcs/*.md and rfcs-txt/*.txt — the normative spec set, and docs/ which the
    site mirrors. These make claims, so their vocabulary is a claim.

WHAT IS DELIBERATELY EXEMPT, AND WHY
    The essay corpus and the drafts tree. Chris's physical-place and physics
    language there is *voice* — the substrate-physics register — not a claim
    about the world, and shipped essays are frozen by choice. A sweep that
    "fixed" them would destroy the register to satisfy a spec rule. This
    exemption is recorded here rather than assumed, so a later pass cannot
    mistake it for an oversight.

    `ktp/src/content/` is also exempt: it is a committed mirror of
    `ktp-rfc/docs/`, re-synced by sync-content.yml. Editing it is overwritten.
    Fix docs/; the mirror follows. Anything else under `ktp/src/` is authored
    and is NOT exempt.

Usage:  python3 scripts/check-vocabulary.py [--baseline] [--verbose]
Exit 1 if any retired term appears in normative text without a historical marker.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCOPE = [("rfcs", (".md",)), ("rfcs-txt", (".txt",)), ("docs", (".md",))]

# A term is retired because something falsified or replaced it. The reason
# travels with the term so a reader of this file knows why it is here.
RETIRED = {
    "Context Tensor": "nothing transforms tensorially — the coordinate attack "
                      "closed it. Now: Context Signals (catalogue) / Risk "
                      "Factors (scoring), bridged by declared aggregation.",
    r"\b(Soul|Body|World|Time|Relational|Signal) Tensor\b":
        "never tensors — they are domains of a catalogue.",
    r"1,?707": "the headline was not derived from its parts. Subgroups sum to "
               "1,627; four domain totals were corrected.",
    r"physics[- ]derived": "retired per BRAND.md's claim-vs-image rule.",
}

# Lines carrying one of these are recording history, not making a claim.
# Supersede, never rename — so the retired term MUST still be sayable in the
# sentence that retires it.
HISTORICAL = re.compile(
    r"superseded|formerly|previously|retired|historical|was called|renamed from"
    r"|no longer|deprecat|until v2|v1\.0", re.I)


def scan():
    hits = []
    for sub, exts in SCOPE:
        root = os.path.join(HERE, sub)
        if not os.path.isdir(root):
            continue
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if not f.endswith(exts):
                    continue
                path = os.path.join(dp, f)
                rel = os.path.relpath(path, HERE)
                for i, line in enumerate(open(path, errors="replace"), 1):
                    if HISTORICAL.search(line):
                        continue
                    for term in RETIRED:
                        if re.search(term, line):
                            hits.append((rel, i, term, line.strip()[:90]))
    return hits


def filenames():
    """A spec named for a retired object is a permanent URL asserting it."""
    bad = []
    for name, why in (("ktp-tensors", "Context Tensor Specification"),
                      ("ktp-gravity", "Digital Gravity Specification"),
                      ("ktp-signal", "Signal Environment Specification")):
        for sub, ext in (("rfcs", ".md"), ("rfcs-txt", ".txt")):
            p = os.path.join(HERE, sub, name + ext)
            if os.path.exists(p):
                bad.append((os.path.relpath(p, HERE), why))
    return bad


def main():
    verbose = "--verbose" in sys.argv
    hits = scan()
    named = filenames()

    by_term = {}
    for rel, i, term, text in hits:
        by_term.setdefault(term, []).append((rel, i, text))

    print("Vocabulary tripwire — v2.0.0 Gödel\n")
    print(f"{'retired term':<34}{'unmarked hits':>14}   why it is retired")
    print("-" * 100)
    for term, why in RETIRED.items():
        n = len(by_term.get(term, []))
        flag = "" if n == 0 else "  <-"
        print(f"{term:<34}{n:>14}{flag}   {why[:52]}")
    print()
    if named:
        print("Spec files named for a retired object "
              "(renaming breaks published URLs — that is a decision, not a fix):")
        for rel, why in named:
            print(f"  {rel:<34} {why}")
        print()
    if verbose:
        for term, rows in by_term.items():
            print(f"\n--- {term} ({len(rows)})")
            for rel, i, text in rows[:25]:
                print(f"  {rel}:{i}  {text}")
            if len(rows) > 25:
                print(f"  … {len(rows)-25} more")

    total = len(hits)
    print(f"[{total} unmarked occurrence(s) in normative text, "
          f"{len(named)} file(s) named for a retired object]")
    print("[exempt by design: the essay/drafts corpus (voice, frozen by "
          "choice) and ktp/src/content (mirror of docs/)]")
    if "--baseline" in sys.argv:
        return 0
    return 1 if (total or named) else 0


if __name__ == "__main__":
    sys.exit(main())
