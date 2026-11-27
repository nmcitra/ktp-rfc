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

The clock starts when the proposal is published (§1). The workflow reads
the later of the two labels, `decision-needed` and `class:*`, as its record
of that day — apply both on the day of publication, or the mechanism will
close the window late. When a proposal passes its review window still marked
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
2026-09-09 · Editorial
Source: PR #123; SN-004
Decision: The Trust Tier glossary names Hibernation as the fifth tier rather
than leaving it implied by the threshold table.

### D-008 · Process labels become contributor labels; this file exists
2026-09-17 · Editorial · clock not run
Source: this PR
Decision: Contributor-facing labels and this file are added; `CONTRIBUTING.md`
points here.

### D-009 · An infrastructure execution profile
Published 2026-09-16 · MINOR · floor 2026-10-07 · review-by 2026-10-28 · approved 2026-10-14
Source: issue #124; PR #131
Decision: Approved as proposed. The software-substrate execution profile enters
`specifications/` with v3.0.0; PR #131 merges in the order the v3.0.0 release
proposal states.
Provenance: proposed by Mike Storm; built first as KIL.
Corrected before release in PR #233: three out-of-domain vectors, S54 to S56.

### D-010 · The consolidation block
Published 2026-09-09 · class MAJOR · clock 2026-09-09 → floor 2026-10-23 → review-by 2026-12-06 · approved 2026-10-23
Source: PR #122; CHANGELOG § Unreleased
Text landed on `main` via PR #123 (2026-09-09), ahead of the floor.
Decision: Approved as landed. The block stays unreleased on `main` until the
v3.0.0 tag and ships with it. PR #122 is closed as superseded by the landed
text. A later proposal that alters a sentence in this block says so in its
own entry; approval here does not freeze the text.

### D-011 · Supplier-neutral illustrative examples
2026-09-20 · Editorial · no clock
Source: issue #132; PR #133
Decision: Named companies in a hypothetical hardware-lock-in critique and in
the OUI tooltip are replaced with supplier-independent wording; the affected
RFC views are regenerated from source. Proposed by Mike Storm.

### D-012 · Consequential-action execution and evidence
Published 2026-09-18 · MINOR · floor 2026-10-09 · review-by 2026-10-30 · approved 2026-10-14
Source: issue #129; PR #139
Decision: Approved as proposed. The consequential-action execution and
evidence specification, its schema and its vectors enter the set with v3.0.0;
PR #139 merges in the order the v3.0.0 release proposal states.
Provenance: proposed by Mike Storm; KAG as the reference implementation.
Corrected before release in PR #233: thirteen schema vector ids numbered J12 to
J24, the fingerprint digest's schema member named, and MIGRATION's `no_effect`
sentence.

### D-013 · Three Risk Factor formulas no longer weight the Soul veto
Published 2026-10-05 · Clarification · clock 2026-10-05 → floor 2026-10-12 · review-by 2026-10-19 · approved 2026-10-14
Source: issue #142; the clarification PR opened with this record
Decision: The descriptive formulas in ktp-signals, ktp-attenuation and
ktp-oracle that still carried a Soul term inside the weighted sum become
cross-references to ktp-core's aggregation, with one line recording that the
weighted form was retired at v2.0.0. No conformant implementation changes.

### D-014 · R is defined once; Risk Domains become an informative technique
Published 2026-10-05 · MINOR · clock 2026-10-05 → floor 2026-10-26 · review-by 2026-11-16 · approved 2026-10-27
Source: issue #144; the PR opened with this record
Decision: Shape A, retire. Core Section 5.2 is the one definition of the
Risk Factor; Sensors 2.3 keeps the node, neighborhood and global levels as an
informative technique for one input, Conformance drops the Risk Domain
requirements, and CT-S-002 is retired.

### D-015 · L23: a number that is digested or compared has no single written form
Published 2026-10-30 · Clarification · clock 2026-10-30 → floor 2026-11-06 · review-by 2026-11-13 · approved 2026-11-07
Source: issue #211; PR #212
Decision: Approved as proposed. L23 enters KTP-CORE's named limits with
v3.0.0 and adds no requirement. PR #212 merges after #209 in the order the
v3.0.0 release proposal states.
Provenance: proposed by Chris Perkins, from a gap @martherus found
implementing the published vectors.

### D-016 · Induced Conservatism named in the threat model: TM-D-005
Published 2026-10-07 · Clarification · clock 2026-10-28 → floor 2026-11-04 · review-by 2026-11-11 · approved 2026-11-07
Source: issue #146; PR #208
Decision: Approved as proposed. KTP-THREAT-MODEL names Induced Conservatism
as TM-D-005, and no conformant implementation changes. The first review window
closed by mechanism on 2026-10-23 and the clock restarted on 2026-10-28.
PR #208 merges with this record.
Provenance: proposed by @kimosmond-del; carried into PR #208 by the maintainer.

### D-017 · KTP-CELESTIAL's exponential degradation curve decays
Published 2026-11-10 · Clarification · floor 2026-11-17 · review-by 2026-11-24 · approved 2026-11-18
Source: issue #221; PR #222
Decision: Approved as proposed. The exponential curve's constant is
`ln(2) / half_life`, so e_trust halves every half-life, and "(more
conservative)" is removed. The defect is in every release since v1.0.0 and is
recorded as SN-006; no conformant implementation changes. PR #222 merges with
this record.
Provenance: proposed and carried into PR #222 by the maintainer.

### D-018 · A delegation's bounds are the ones it states
Published 2026-11-14 · Clarification · floor 2026-11-21 · review-by 2026-11-28 · approved 2026-11-24
Source: issue #223; PR #224
Decision: Approved as proposed. In KTP-HUMAN, a parameter or limit that a
delegation does not state, or a numeric limit that is not a finite,
non-negative number, is an undefined input under KTP-CORE Section 6.8, and
text that accompanies a request is not a statement of the delegation. A
cumulative limit is evaluated across every request made under the
delegation. No conformant implementation changes. PR #224 merges with this
record.
Provenance: proposed and carried into PR #224 by the maintainer.

### D-019 · Nested zones: rings, enclosure depth, and the Enclosure Domain
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #159; PR #160
Decision: Approved as proposed. KTP-ZONES defines nested zones as rings with
an enclosure depth, an ingress path and egress shaping. KTP-SENSORS adds the
Enclosure Domain, and KTP-FEDERATION retires Hierarchical Federation. *Parent*
and *child* leave the zone vocabulary, with the migration notes a vocabulary
change requires. PR #160 merges with this record.
Provenance: proposed and carried into PR #160 by the maintainer.

### D-020 · A person is a subject of the protocol; the External Root is a person
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #162; PR #165
Decision: Approved as amended on 2026-11-08. A person is a subject of the
protocol as an account in a zone. A person's standing is composed from the
acts the person signed and bears on nothing outside the protocol. Behind every
root instrument stands a person, and behind the person an employer, a
licensing body or a board. People sponsor people, and persons stake on agents.
The vocabulary mapping is in MIGRATION. PR #165 merges with this record.
Provenance: proposed and carried into PR #165 by the maintainer.

### D-021 · `moment_criticality` leaves the Risk Factor
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #161; PR #164
Decision: Approved as proposed. The Risk Factor aggregates five weighted
inputs. `moment_criticality` becomes a declared demand-side input that raises A
only and never enters R, and an absent or stale value reads as the most
critical moment. L14 states the rule for a demand input. The weight profiles
and worked examples are renormalized over five inputs. PR #164 merges with
this record.
Provenance: proposed and carried into PR #164 by the maintainer.

### D-022 · Conformance is claimed, not certified
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #163; PR #166
Decision: Approved as proposed. In KTP-CONFORMANCE, Status Label, Conformance
Claim and Independent Party replace Certification, Self-Certification and
Third-Party Certification. Claim Status replaces the Certification Process,
and the maintainer's own runs are never independent. The old-to-new mapping is
in MIGRATION. The Standard Oracle-mesh row reads four nodes, as its
requirement already did. PR #166 merges with this record.
Provenance: proposed and carried into PR #166 by the maintainer.

### D-023 · L11: normative content restricts and never widens
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #167; PR #168
Decision: Approved as proposed. Under KTP-CORE L11, norm content restricts
and never widens any outcome the specification orders. A favorable verdict
satisfies only the gate it answers, for the whole action and the actor it
adjudicated. A rail releases only the increment it raised, and never below the
level derived from the environment. The adjudication token schema and its vectors enter the set. PR #168 merges with
this record.
Provenance: proposed and carried into PR #168 by the maintainer.

### D-024 · L15: composition across requests is not yet required
Published 2026-10-13 · MAJOR · floor 2026-11-26 · review-by 2027-01-09 · approved 2026-11-26
Source: issue #169; PR #170
Decision: Approved as proposed. KTP-CORE L15 states that evaluation runs one
request at a time and that nothing yet bounds the combined consequence of a
split across requests. A per-request limit MUST NOT be presented as a bound on
combined consequence. PR #170 merges with this record.
Provenance: proposed and carried into PR #170 by the maintainer.

### D-025 · Every Proof of Resilience friction boundary is exact
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #150; PR #193
Decision: Approved as proposed. KTP-IDENTITY places each friction boundary in
exactly one interval, from CALM (0 ≤ R ≤ 0.3) to CRISIS (0.9 ≤ R ≤ 1.0). An R
that is out of range or not finite is rejected, and so is a declared category
that does not match its interval. GOODHART-003's thresholds become inclusive.
The friction-boundary vectors enter the set. PR #193 merges in the order the
v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #193.

### D-026 · A sponsor reference is not a sponsor's Agent URI
Published 2026-10-10 · Vocabulary · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #149; PR #194
Decision: Approved as proposed. KTP-IDENTITY gives the Agent identifier a
grammar and byte equality. The sponsored identifier's first segment becomes
`sponsor_ref`, an opaque reference that MUST NOT establish sponsorship.
Sponsorship binds only through a complete sponsor URI, of an agent or a
person. The old-to-new mapping is in KTP-IDENTITY and MIGRATION. PR #194 merges
in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #194.

### D-027 · One canonical v3 Trust Proof
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #151; PR #195
Decision: Approved as proposed. The Trust Proof specification, its schema and
its vectors enter the set as the one definition of the v3 Trust Proof: the
media type `application/ktp-trust-proof+jwt`, a header of `alg`, `kid` and
`typ` only, a lifetime of at most ten seconds, size limits, the gate states
`clear`, `veto` and `undetermined`, and ordered verification stages with
stable reasons. KTP-CORE points to it in place of its own claim list. PR #195
merges in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #195.

### D-028 · External Root variants and their projection into the proof
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #157; PR #201
Decision: Approved as proposed. The External Root specification, the
root-instrument schema and their vectors enter the set. A Trust Proof declares
whether its subject is a software agent or a person, and a root instrument's
projection names the person behind it and the terminator. A subject with no
root credit has its E_base capped at 70 and carries the
`external_root_missing` ceiling. This carries D-020 into the proof. PR #201
merges in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #201.

### D-029 · An ordinary request is bound to its Trust Proof evidence
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #152; PR #196
Decision: Approved as proposed. The request-binding specification, its two
schemas and its vectors enter the set. Ordinary software authorization MUST
use the canonical request binding, and the PEP takes Soul status from the
proof that the association step verified. PR #196 merges in the order the
v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #196.

### D-030 · A canonical Decision Geometry record
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #153; PR #197
Decision: Approved as proposed. The Decision Geometry specification, its
record and carrier schemas and its vectors enter the set. Decision Geometry is
the portable, deterministic evaluation record. It is distinct from Flight
Recorder storage, from a Trajectory Chain record and from the execution
outcome. A consumer MAY tighten a result and MUST NOT lower a veto. PR #197
merges in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #197.

### D-031 · Native v3 retires the stale v1 Transport wire definitions
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #156; PR #200
Decision: Approved as proposed. Native v3 transport MUST support the
`ktp-json-jws-v1` base profile of the native-transport specification, which
enters the set with its vectors. KTP-TRANSPORT's v1 encoding block is removed.
PR #200 merges in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #200.

### D-032 · A per-operation demand supplier contract
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #147; PR #202
Decision: Approved as proposed. The demand-supplier specification, its
schemas and its vectors enter the set. A deployment that uses
`moment_criticality` declares its supplier, who is neither the requester nor a
party acting for it, with the supplier's profile, source, unit, range,
freshness and verification profile; an undeclared input that an operation
requires reads as unavailable. KTP-CORE L14 is converted by this contract. PR #202 merges in the order the
v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #202.

### D-033 · One missing-evidence contract, from feed to Risk Factor
Published 2026-10-10 · MAJOR · floor 2026-11-23 · review-by 2027-01-06 · approved 2026-11-26
Source: issue #148; PR #203
Decision: Approved as proposed, with the backup-continuity requirements added
to PR #203 on 2026-11-17. The missing-evidence specification, the
evidence-state schema and their vectors enter the set. Missing members and
their weights are not dropped. Slots and weights are fixed before evaluation,
with a finite, positive denominator. A backup fills a slot only with coverage
established as independent and equivalent, and one observation never fills
two slots. PR #203 merges in the order the v3.0.0 release proposal states.
Provenance: proposed by @martherus, who wrote PR #203.
