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

    `schemas/` is IN, .md AND .json, from the v2 layout move. Scope here is by
    PATH, so when the wire artifacts left docs/ they would have left
    jurisdiction with it — silently, which is the failure mode this file
    exists to refuse. Extending the scope rather than following the old path
    also closed a gap that predates the move: docs/ is scanned for .md only,
    so no schema was ever read. The first run under the new scope found four
    retired-vocabulary descriptions inside sensor-config.json, a published
    v2 artifact that every other gate called clean. A `description` in a
    schema is prose a reader cites, and it is shipped further than any page.

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

SCOPE = [("rfcs", (".md",)), ("rfcs-txt", (".txt",)), ("docs", (".md",)),
         ("schemas", (".md", ".json")), ("catalog", (".md", ".json"))]

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
         why="the headline was not derived from its parts. Subgroups summed "
             "to 1,627 and four domain totals were corrected; tracker#18 then "
             "adopted the meta domain and the count is 1,644. Both later "
             "numbers are re-derived from catalog/*.json; 1,707 never was."),
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


def scheme():
    """The D1a symbol scheme, which a term-by-term scan cannot see (#68).

    RETIRED above catches words. The letter scheme was not a word — it was six
    single characters used as JSON keys, and no pattern over prose can find
    `"m": 0.45` without also finding every other `m` in the corpus. That is why
    "the vocabulary work is done" could read clean while every machine-readable
    example in the set still shipped the scheme it retired. This function is
    the missing half: it decides on SHAPE, not on words.

    D1a, ruled: the JSON key IS the name. The six weighted inputs are
    evidence_density, trust_trend, adversarial_pressure, moment_criticality,
    update_resistance and attestation_coverage; the veto is `soul`; the object
    that carries them is `risk_factors`, never `context_tensor`.

    TWO SIGNATURES, both deliberately narrow

        1. A letter-keyed object. Three or more DISTINCT keys from the retired
           set within one 240-character window of whitespace-collapsed text.
           The window is what makes the rule survivable: it reads the same
           whether the object is pretty-printed one key per line or inlined on
           one, and it cannot fire on a lone letter key that means something
           else. Two survivors depend on that: ktp-zones' Shamir "m"-of-"n"
           threshold and the catalogue's per-signal "p" flag are each a single
           distinct letter and are invisible here, by construction rather than
           by an exemption anyone has to maintain.

        2. `context_tensor` as an identifier. The underscore form only — the
           object's name in code. The hyphenated form was a path and a filename
           and is gone; where it survives it is prose about a rename, which is
           a claim about history and not an identifier.

    SCOPE includes rfc-src/, which the retired-term scan does not. That is not
    a quiet re-ruling of #64, D: rfc-src/ did not exist as the authored source
    when that scope was set (#78/#108 made it one afterward). A scheme that
    ships from the source the five filed Internet-Drafts are generated from has
    shipped, whatever rfcs/ says, so the gate reads the source too.

    HISTORICAL alone is not enough to excuse the scheme, because "previously"
    appears all over live prose. A hit is excused only when it sits in a
    paragraph that speaks about v1 — which is where the letter scheme lived,
    and where the Changes from v1 appendices record it on purpose.

    The exemption is read over the PARAGRAPH, not the line. The .txt half is
    wrapped at 72 columns, so a marker and the thing it marks routinely land on
    different lines; a line-scoped exemption would refuse the appendix that
    exists to make the record, and — the same failure inverted — a line-scoped
    *detector* would miss a term split across a wrap. #68 found three of those
    hiding in the filed drafts. Paragraph scope is the fix for both directions.
    """
    letters = "mpvhtios"
    key = re.compile(r'"([%s])"\s*:' % letters)
    tensor = re.compile(r"\bcontext_tensor\b")
    v1 = re.compile(r"\bv1\b|Changes from v1", re.I)
    window = 240
    scope = SCOPE + [("rfc-src", (".md",))]

    bad = []
    for sub, exts in scope:
        root = os.path.join(HERE, sub)
        if not os.path.isdir(root):
            continue
        for dp, _, fs in os.walk(root):
            for f in sorted(fs):
                if not f.endswith(exts):
                    continue
                path = os.path.join(dp, f)
                rel = os.path.relpath(path, HERE)
                lines = open(path, errors="replace").read().split("\n")

                # the paragraph each line belongs to, for the v1 exemption
                para = [""] * len(lines)
                i = 0
                while i < len(lines):
                    if not lines[i].strip():
                        i += 1
                        continue
                    j = i
                    while j < len(lines) and lines[j].strip():
                        j += 1
                    block = " ".join(l.strip() for l in lines[i:j])
                    for k in range(i, j):
                        para[k] = block
                    i = j

                # signature 2 — the identifier
                for i, line in enumerate(lines, 1):
                    if tensor.search(line) and not v1.search(para[i - 1]):
                        bad.append((rel, i, "context_tensor identifier",
                                    line.strip()[:70]))

                # signature 1 — the shape, decided over a sliding window that
                # ignores where the line breaks fall
                flat, pos = [], []
                off = 0
                for i, line in enumerate(lines, 1):
                    t = line.strip()
                    flat.append(t)
                    pos.append((off, i))
                    off += len(t) + 1
                text = " ".join(flat)
                found = [(m.start(), m.group(1)) for m in key.finditer(text)]
                reported = set()
                for a in range(len(found)):
                    seen = {found[a][1]}
                    for b in range(a + 1, len(found)):
                        if found[b][0] - found[a][0] > window:
                            break
                        seen.add(found[b][1])
                    if len(seen) < 3:
                        continue
                    line_no = 1
                    for start, i in pos:
                        if start <= found[a][0]:
                            line_no = i
                        else:
                            break
                    if line_no in reported:
                        continue
                    reported.add(line_no)
                    if v1.search(para[line_no - 1]):
                        continue
                    bad.append((rel, line_no, "letter-keyed object",
                                "keys " + ",".join(sorted(seen))))
                    break
    return bad


def main():
    verbose = "--verbose" in sys.argv
    hits = scan()
    named = filenames()
    scheme_hits = scheme()

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

    print(f"{'D1a symbol scheme':<24}{len(scheme_hits):>14}"
          f"{'' if not scheme_hits else '  <-'}   the JSON key IS the name; "
          "six letters and context_tensor retire")
    if scheme_hits:
        print()
        print("Letter scheme still on the wire (#68). The six weighted inputs are "
              "evidence_density,")
        print("trust_trend, adversarial_pressure, moment_criticality, "
              "update_resistance and")
        print("attestation_coverage; the veto is soul; the object is risk_factors:")
        for rel, i, kind, text in scheme_hits[:25]:
            print(f"  {rel}:{i}  {kind}: {text}")
        if len(scheme_hits) > 25:
            print(f"  … {len(scheme_hits)-25} more")
    print()

    total = len(hits)
    print(f"[{total} unmarked occurrence(s) in normative text, "
          f"{len(named)} retired path(s) present, "
          f"{len(scheme_hits)} letter-scheme occurrence(s)]")
    print(f"[in scope: {' '.join(sub + '/' for sub, _ in SCOPE)} — they have "
          "to match; the scheme check adds rfc-src/, the authored source]")
    print("[exempt by design: the essay/drafts corpus IN FULL (voice, no "
          "publication gate), ktp/src/content (mirror), rest of ktp/src "
          "(separate pass)]")
    if "--baseline" in sys.argv:
        return 0
    return 1 if (total or named or scheme_hits) else 0


if __name__ == "__main__":
    sys.exit(main())
