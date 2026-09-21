# Decisions

How decisions on this specification are made, and where each one landed.
Append-only. One entry per decision. A dispute is a new entry, never an edit
to an old one.

This file is the public record. Working notes behind a decision may live
elsewhere; nothing in them binds anyone. What binds is here.

## 1. The rule

Nothing changes by seniority, volume, or urgency. It changes by a published
proposal, on a clock, through three questions answered separately.

**The clock binds the maintainer or it binds nobody.** A floor is a minimum
elapsed time, counted from the day a concrete proposal is published in the
open, before anything in its class can be approved. Nothing is approved early
because the answer is obvious.

Every decision carries a review-by date. A proposal that reaches its review-by
date without a decision returns to discussion. Nothing passes by default.

## 2. Clocks by consequence

Classes are the ones [`VERSIONING.md`](VERSIONING.md) already defines. The
clock attaches to the class.

| Class | What it covers | Floor | Review window |
|---|---|---|---|
| Editorial | typo, wording, checker fix; rides `main` per VERSIONING | none | none |
| Clarification | states a requirement the set already implied; no conformant implementation changes | 7 days | 14 days |
| MINOR | a specification, profile, or optional feature enters the set | 21 days | 42 days |
| MAJOR | a conformant implementation stops conforming | 30 days notice, then 14 days ratification | 88 days |
| Vocabulary | a term is added, removed, split, or changes meaning | as MAJOR, plus migration notes and an old-to-new mapping | 88 days |
| Emergency | a security correction | immediate | expires in 7 days unless approved on the normal clock |

The MAJOR floor uses the notice and ratification periods
[`ktp-governance`](rfcs-md/ktp-governance.md) requires of a zone charter
amendment. The repository holds itself to the shape it specifies.

The review window is twice the floor. It is the outer bound, not a target.

A proposal tagged `blocked-on-evidence` is waiting on a fact, not on time.
The clock keeps running. Both must clear.

## 4. Labels and the clock

Labels on this repository speak to contributors. The clock reads them.

| Label | Meaning |
|---|---|
| `needs-triage` | New. A maintainer has not read it yet |
| `discussion` | Open. No decision requested |
| `decision-needed` | A concrete proposal is published. Paired with a class label, this starts the clock |
| `class:clarification` · `class:minor` · `class:major` · `class:vocabulary` · `class:emergency` | The clock class |
| `blocked-on-evidence` | Waits on reproducible evidence. Does not stop the clock |
| `accepted` | Decided yes. A PR is welcome or in progress |
| `declined` | Decided no. The reason is in the thread and in this file |

The clock starts on the later of the two labels, `decision-needed` and
`class:*`. When a proposal passes its review window still marked
`decision-needed`, a workflow removes that label, applies `discussion`, and
says so in the thread. That is the window closing by mechanism, not by hand.
Re-applying `decision-needed` restarts the clock. The workflow is
[`.github/workflows/decision-clock.yml`](.github/workflows/decision-clock.yml).

## 5. Emergencies

A security correction may land immediately. It must be limited to the defect,
recorded here, and it expires seven days later unless approved on the normal
clock. The record says who acted, what changed, why, and on what evidence.

## 6. Provenance

Building something first earns credit, not ownership. Every entry that
produces a specification keeps these apart:

- who proposed it
- who edited the text
- who built it first
- whose implementation is the reference
- who else has built a conforming one

The first implementer is recorded as such, permanently. The specification stays
governed by this file.

## 7. Entry shape

```
### D-NNN · <title>
Date · Class · Clock start → floor → review-by
Source: <issue, PR, tag, or CHANGELOG section>
Decision: <what was decided, in one or two sentences>
```

Entries before 2026-09-17 are back-filled from the public record: tags, merged
pull requests, and [`CHANGELOG.md`](CHANGELOG.md). Their clocks were not run;
the entries say so. From D-009 forward, the clock is live.

## 8. The record

### D-001 · v1.0.0 "Lovelace": the first fixed point
2025-12-01 · MAJOR · clock not run (predates this file)
Source: tag `v1.0.0`; CHANGELOG § 1.0.0
Decision: The series gets a first citable fixed point. Two defects found after
publication are recorded as SN-001 and SN-002 in `SECURITY-NOTES.md` and
corrected in 2.0.0; the tag stays as published.

### D-002 · Provenance infrastructure and the versioning policy
2026-07-18 and 2026-08-08 · Editorial · clock not run
Source: PR #40, PR #45; tag `v1.0.1-provenance`; CHANGELOG § 1.0.1
Decision: `NOTICE`, `CITATION.cff`, `PROVENANCE.md` and `VERSIONING.md` enter
the repository. Tags are the version, bare and numeric; published tags are
never moved. The one descriptive tag suffix is left in place for that reason.

### D-003 · The Kinetic Envelope enters the set
2026-07-23 · MINOR · clock not run
Source: PR #44; `specifications/kinetic-envelope.md`;
`specifications/conformance/ros2-reference-v0.1.json`
Decision: The set fixes the interface, the decision contract, and the
conformance suite for the envelope, and leaves the formula for A and E
implementation-defined. Two systems conform if they produce the same decisions
on the published vectors.

### D-004 · v2.0.0 "Gödel": the deliberate break
2026-08-14 · MAJOR · clock not run
Source: PR #116; tag `v2.0.0`; CHANGELOG § 2.0.0; four *Changes from v1*
appendices
Decision: Headline moves: `E_base`
becomes a hundred-point allocation; tier thresholds move; God Mode becomes
Admin Mode; lineage stages are renamed `sponsored → independent → guarantor`;
the Soul veto leaves the weighted vector; the letter scheme leaves the wire;
`ktp-core` gains a *Limits of This Specification* section. The full list is
CHANGELOG § 2.0.0.

### D-005 · Post-tag editorial residue rides `main`
2026-08-14 · Editorial · clock not run
Source: PR #118
Decision: Bare physics words surviving as live input names in prose after the
tag are editorial. Per VERSIONING they accumulate on `main` and ride the next
bundle. The tag, Release, and DOI stay exactly as published.

### D-006 · v2.1.0: an erratum classed MINOR, not PATCH
2026-09-03 · MINOR · clock not run
Source: PR #120, PR #121; tag `v2.1.0`; CHANGELOG § 2.1.0; SN-003
Decision: `ktp-enforce` §9.1's Hibernation threshold sentence moves from the
v1 value 50 to 22, matching three other normative locations.
Provenance: finding reported by Mike Storm from a shipping v2.0.0 Risk Factor
producer; text edited by the maintainer.

### D-007 · Hibernation is the fifth tier, named
2026-09-09 · Clarification · clock not run
Source: PR #123; SN-004
Decision: The Trust Tier glossary names Hibernation as the fifth tier rather
than leaving it implied by the threshold table.

### D-008 · Process labels become contributor labels; this file exists
2026-09-17 · Editorial · clock not run
Source: this PR
Decision: Contributor-facing labels and this file are added; `CONTRIBUTING.md`
points here.

### D-009 · An infrastructure execution profile (open)
Published 2026-09-16 · MINOR · floor 2026-10-07 · review-by 2026-10-28
Source: issue #124
Decision: pending.
Provenance: proposed by Mike Storm; built first as KIL.

### D-010 · The consolidation block (open)
Published 2026-09-09 · class pending
Source: PR #122; CHANGELOG § Unreleased
Decision: pending.

### D-011 · Supplier-neutral illustrative examples
2026-09-20 · Editorial · no clock
Source: issue #132; PR #133
Decision: Named companies in a hypothetical hardware-lock-in critique and in
the OUI tooltip are replaced with supplier-independent wording; the affected
RFC views are regenerated from source. Proposed by Mike Storm.
