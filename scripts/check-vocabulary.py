#!/usr/bin/env python3
"""Vocabulary tripwire for v2.0.0 "Gödel" — retired terms in normative text.

Success criteria have to be checkable or they are aspirations. Robin's own bar,
stated when he shipped two MUSTs: "both MUSTs because both are checkable." This
script is what makes "the vocabulary work is done" a fact instead of a feeling.

THE RULE — ruled on ticket #64, 2026-08-10

    This checker never decides voice from claim. It cannot, and a script that
    tried would eventually rewrite an essay to satisfy a spec. It decides three
    mechanical things and leaves a residue small enough for a person to read.

    Layer 1 — SURFACE REGISTER, decided by path and declared once (below).
    Layer 2 — RETIRED CONSTRUCTION, never a bare common noun. A term is retired
              when it names a KTP object a reader could cite. Where the word
              also has an innocent everyday sense, a `bound` pattern ties it to
              the retired object; unbound uses are invisible here by design.
              This is why `dimension` is untouchable as a word and retired the
              moment it is bound to a catalogue domain.
    Layer 3 — SUPERSESSION, not silence. Supersede, never rename: the retired
              term MUST still be sayable in the sentence that retires it.

    What survives all three gets BRAND.md §3's test, applied by a human: if a
    skeptical engineer quoted the sentence back in a review, would it need
    defending as an assertion? Then it is a claim.

WHAT IS IN SCOPE

    rfcs/*.md, rfcs-txt/*.txt, and docs/*.md. `docs/` is IN (#64, D): it is the
    same repo as the specs and it is the source the site mirrors, so the two
    have to match. All three make claims, so their vocabulary is a claim.

WHAT IS DELIBERATELY EXEMPT, AND WHY

    The essay corpus and the drafts tree, IN FULL (#64, A) — including the
    research subdirectories (`tfe-research/`, `ostrom-percolation/`,
    `research-dossiers/`, `plans/`), which are claim-register prose but are not
    outbound. Chris's physical-place and physics language there is *voice* — the
    substrate-physics register — not a claim about the world, and shipped essays
    are frozen by choice. A sweep that "fixed" them would destroy the register
    to satisfy a spec rule.

    The accepted cost, recorded rather than discovered later: there is NO
    publication gate. Retired vocabulary can re-enter the corpus when a draft is
    published, and nothing will catch it. That was the ruling, not an oversight.

    `ktp/src/content/` is exempt: it is a committed mirror of `ktp-rfc/docs/`,
    re-synced by sync-content.yml. Editing it is overwritten. Fix docs/; the
    mirror follows. The rest of `ktp/src` is authored and is a SEPARATE pass —
    the site holds both registers (the voyage, the speakeasy, canon/ancestors
    are image; the glossary must keep retired terms and mark them), so no
    directory-level rule works there.

Usage:  python3 scripts/check-vocabulary.py [--baseline] [--verbose]
Exit 1 if any retired term appears in normative text without a historical marker.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCOPE = [("rfcs", (".md",)), ("rfcs-txt", (".txt",)), ("docs", (".md",))]

# Lines carrying one of these are recording history, not making a claim.
HISTORICAL = re.compile(
    r"superseded|formerly|previously|retired|historical|was called|renamed from"
    r"|no longer|deprecat|until v2|v1\.0", re.I)

# The one sentence in which "physics" may still appear (#64, C). The ruling:
# no, the word does not survive in the spec set — except to state plainly that
# the newsletter is called Digital Gravity, and why the old name was removed.
# Naming the newsletter is not enough on its own; the removal has to be marked.
NEWSLETTER = re.compile(r"Digital Gravity", re.I)

# A term is retired because something falsified or replaced it. The reason
# travels with the term so a reader of this file knows why it is here.
#   pat    — what makes the term appear
#   bound  — required on the same line for the hit to count; absent means the
#            term is retired unconditionally
#   allow  — permits the hit despite everything else (layer 3, per-term)
#   exempt — a ruled-correct use of the phrase, live rather than historical;
#            the line falls through to later rules so other retired terms on
#            it are still seen
# First matching rule wins per line, so specific rules precede general ones.
RETIRED = [
    dict(term="Context Tensor",
         pat=r"Context Tensor",
         why="nothing transforms tensorially — the coordinate attack closed it. "
             "Now: Context Signals (catalogue) / Risk Factors (scoring), "
             "bridged by declared aggregation."),
    dict(term="<Domain> Tensor",
         pat=r"\b(Soul|Body|World|Time|Relational|Signal) Tensor\b",
         why="never tensors — they are domains of a catalogue."),
    dict(term="<domain> dimension",
         pat=r"\b(Soul|Body|World|Time|Relational|Signal)\s+[Dd]imensions?\b"
             r"|\b(seven|7|six|6)[- ][Dd]imensions?\b"
             r"|[Dd]imensions?\s+of\s+the\s+(Context\s+)?Tensor"
             r"|\b[Tt]ensor\s+[Dd]imensions?\b",
         why="the catalogue's six are DOMAINS (D2), not dimensions. The word "
             "itself is not retired — it belongs to ARQ (Availability, "
             "Retainability, Quality) and to ordinary mathematics, both of "
             "which this rule leaves alone."),
    dict(term="Accessibility (ARQ)",
         pat=r"\bAccessibilit(y|ies)\b",
         bound=r"ARQ|Retainability|[Dd]imension|E_?base|Meso:|Quality",
         why="ARQ's A is Availability (#64, B). Renamed knowingly into the "
             "existing security-triad sense of the word: capital Availability "
             "is the ARQ dimension, lowercase availability is uptime. Unbound "
             "uses of 'accessible/accessibility' are the ordinary English word "
             "and are not touched."),
    dict(term="physics-derived",
         pat=r"physics[- ]derived",
         why="retired per BRAND.md's claim-vs-image rule — the first "
             "construction to go, and the ancestor of the whole #64 ruling."),
    dict(term="Digital Physics",
         pat=r"Digital Physics",
         allow=NEWSLETTER,
         why="retired as the theory's name and as a masthead (BRAND.md §1). "
             "Sayable only in the sentence naming the newsletter Digital "
             "Gravity and marking why the old name was removed."),
    dict(term="God Mode",
         # No leading \b: TRUST_TIER_GOD_MODE has a word char before "GOD",
         # so an anchored pattern reads zero on the wire value — the exact
         # blind spot #84 recorded for the D1a symbol scheme. Catches the
         # prose name, the protobuf enum, and the OpenAPI string alike.
         pat=r"(?i)god[ _-]?mode",
         exempt=re.compile(r"\"God Mode\""),
         why="retirement ruled — 'retire that phrase everywhere' (Chris). The "
             "name asserts the top tier is unrestricted power; under the "
             "ceilings-minimum architecture it is not — the Mass Ceiling still "
             "binds, the External Root must still be current, and R still "
             "deflates every decision. REPLACEMENT RULED #89 (2026-08-13): "
             "Admin Mode; wire forms TRUST_TIER_ADMIN (= 5, wire-compatible) "
             "and OpenAPI `admin` (breaking, lands in v2.0.0). The one "
             "surviving use is ktp-governance's named antipattern, in "
             "quotation marks — #89 item 2 ruled it survives, and the exempt "
             "pattern encodes that ruling rather than pre-empting it."),
    dict(term="physics",
         pat=r"\bphysics\b",
         allow=NEWSLETTER,
         why="ruled retired in the spec set entire (#64, C) — the RFCs are "
             "claim register, and 'authorization as physics, not policy' is "
             "exactly the sentence a reviewer makes you defend. Survives in "
             "essays and drafts, which are voice and are exempt."),
    dict(term="1,707",
         pat=r"1,?707",
         why="the headline was not derived from its parts. Subgroups sum to "
             "1,627; four domain totals were corrected."),
]


def classify(line):
    """First matching rule wins, so 'Digital Physics' beats bare 'physics'."""
    for rule in RETIRED:
        if not re.search(rule["pat"], line):
            continue
        if "bound" in rule and not re.search(rule["bound"], line):
            continue
        if "exempt" in rule and rule["exempt"].search(line):
            # A ruled-correct live use (#89 item 2: the quoted antipattern).
            # Fall through so other retired terms on the same line still count.
            continue
        if HISTORICAL.search(line):
            # Layer 3: supersession. For terms with their own allowance, the
            # historical marker alone is not enough — the allowance must match.
            if "allow" not in rule or rule["allow"].search(line):
                return None
            continue
        return rule
    return None


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
                    rule = classify(line)
                    if rule:
                        hits.append((rel, i, rule["term"], line.strip()[:90]))
    return hits


def filenames():
    """Paths retired on ticket #65 (2026-08-10). These must stay dead.

    A path is an identifier and a title is a claim; #65 retired both together,
    renamed outright with no redirects. Removing a path is decay, and these
    carried zero measured traffic. If one comes back, the object comes back
    with it — hence a check rather than a note.

    Note what this function must NOT say. It previously asserted that
    ktp-gravity was "named for a retired object" while "Digital Gravity" was
    absent from RETIRED above — a rule no decision record contained. The word
    is not retired. VOCAB-01 kept gravity as conventional network language and
    killed it only as the framework's dynamics, conditioned on whether a given
    surface asserts the strong version. That is why the reason travels with
    each path here: retirement attaches to the assertion, not to the word.
    """
    retired = (
        ("ktp-tensors", "ktp-signals",
         "'Context Tensor' retired by D2 — nothing transforms tensorially."),
        ("ktp-signal", "ktp-information",
         "the domain became `information` and 'Context Signals' now names "
         "the catalogue; the old path was ambiguous, not merely stale."),
        ("ktp-gravity", "ktp-attenuation",
         "the WORD survives (conventional in networking). This document "
         "asserted the killed L4 dynamics across 774 normative lines."),
    )
    bad = []
    for old, new, why in retired:
        for sub, ext in (("rfcs", ".md"), ("rfcs-txt", ".txt")):
            p = os.path.join(HERE, sub, old + ext)
            if os.path.exists(p):
                bad.append((os.path.relpath(p, HERE), f"-> {new}: {why}"))
    return bad


def main():
    verbose = "--verbose" in sys.argv
    hits = scan()
    named = filenames()

    by_term = {}
    for rel, i, term, text in hits:
        by_term.setdefault(term, []).append((rel, i, text))

    print("Vocabulary tripwire — v2.0.0 Gödel\n")
    print(f"{'retired term':<24}{'unmarked hits':>14}   why it is retired")
    print("-" * 100)
    for rule in RETIRED:
        n = len(by_term.get(rule["term"], []))
        flag = "" if n == 0 else "  <-"
        print(f"{rule['term']:<24}{n:>14}{flag}   {rule['why'][:56]}")
    print()
    if named:
        print("Retired spec paths that came back (#65 renamed these outright, "
              "no redirects — a returning path re-asserts the object):")
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
          f"{len(named)} retired path(s) present]")
    print("[in scope: rfcs/ rfcs-txt/ docs/ — they have to match]")
    print("[exempt by design: the essay/drafts corpus IN FULL (voice, no "
          "publication gate), ktp/src/content (mirror), rest of ktp/src "
          "(separate pass)]")
    if "--baseline" in sys.argv:
        return 0
    return 1 if (total or named) else 0


if __name__ == "__main__":
    sys.exit(main())
