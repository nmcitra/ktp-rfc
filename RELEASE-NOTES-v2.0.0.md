# KTP v2.0.0 — Gödel

**Draft release notes.** The full list of changes is in
[`CHANGELOG.md`](CHANGELOG.md); what a v1.0.1 implementer has to change is in
[`MIGRATION.md`](MIGRATION.md). This document is the account of why the release
exists.

---

## The set was contradicting itself, and it could not have told you

v1.0.0 fixed twenty-seven specifications at one point so an implementer could
name a version and know what every document in the set referred to. That worked
for citation. It did not make the documents agree with each other, and this
release began when somebody read two of them side by side.

`ktp-identity` §5.3 stated Proof of Resilience as a *contribution* capped at 70.
`ktp-core` §5.1 then multiplied that contribution by a 70% weight. The same
seventy, spent twice. A maxed-out Proof of Resilience was worth 49 rather than
70; the External Root's thirty was worth nine. Nobody had noticed because
nothing in the repository compared the two sentences — they were in different
files, written months apart, each locally sensible.

That is a type error, not a calibration question, and finding it made the rest
findable. `E_base` had no maximum anywhere, so two different published maxima
were circulating and neither was derivable. Seven separate mechanisms granted
standing outside the composition the composition claimed to bound. An
attestation chain could close on itself. A feed that stopped answering held its
last value forever, and §7.1 of that same document named the attack that makes
possible.

Then somebody checked the tier thresholds against the ceilings.

## Four ladders over one quantity

Trust Tiers are thresholds on `E_trust`. Generation ceilings and zone Mass
Ceilings are bounds on `E_base`. Between them sits the Trust Score,
`E_trust = E_base × (1 − R)`, and the gap between a ceiling and the threshold
it admits *is* an environmental budget. Nobody had ever set one.

The published gaps were 0, 5, −5 and −2, by accident. The consequences:

- **The top tier was unreachable in every zone class.** At the specification's
  own calm worked example, `R = 0.094`, and `95 × 0.906 = 86.1` against a
  threshold of 95.
- **The bottom was worse.** Generation ceilings of 25, 35 and 45 sat *below* the
  lowest threshold of 50, so every agent spent its first 545 to 725 days in
  Hibernation — a tier whose only permitted action is a heartbeat — while §8.1
  of another document said those same agents could act to `A ≤ 50`.
- **The cell was closed, not slow.** Advancement needs attestations,
  attestations need actions, and the tier forbade actions. Exit required ninety
  continuous days of zone-wide crisis at forty-four attested heartbeat-class
  actions a day.

The fix is one table. Thresholds move to **85 / 72 / 58 / 22**, Hibernation is
`E_trust < 22`, and the generation ceilings do not move at all. Two values
travel with it: Hibernation exit goes from 55 to 24, because five points of
hysteresis over a floor of 50 is thirty-three points over a floor of 22; and the
top tier's stable-conditions requirement goes from `R < 0.05` to `R < 0.10`,
because 0.05 was stricter than the calm baseline the set itself illustrates.

An independent check came from a document nobody had reconciled with anything:
`ktp-migration` §5.1.1's role table is three of six rows wrong against the
published thresholds and six of six right against the new ones.

The reason to trust the new numbers is not that they were chosen more carefully.
It is that they are checked by a script. `109-90-reachability.py` compares every
numeric gate in the set against every other at four values of `R`. It fails six
against the published set and zero against this one, and it runs on every
change. A hand-written matrix reproduces the failure that produced the problem
in the first place.

## What the falsification program asked for

Alongside the audit ran a program with a different question: what would this
specification have to say in order to be wrong about something? Several
obligations came back that the set had declared and never discharged.

- **Nothing certifies itself.** `E_base` now carries an anchor invariant: no
  composition may consist entirely of terms the subject measures about itself.
  The accountable party's own accountability must terminate, through a declared
  chain of declared length, at a root outside the agent-trust graph. Undeclared
  terminator, or a chain past the bound, and the term computes as zero.
- **Exposure has to be real to count.** An attestation declares the attestor's
  exposure and the capacity it anchors, and the exposure counts only insofar as
  it cannot be shed by abandoning the attestor's identity. The shell-company
  attack does not stop being possible; it stops being free, and becomes
  attributable and priced.
- **Some questions do not have answers yet, and pretending otherwise is the
  failure mode.** `ktp-core` gains section 10, *Limits of This Specification* —
  fourteen entries, L1 through L14, ordered hardest to softest, from a
  halting-problem reduction to a declared-provenance asymmetry. Declared but
  unmechanized obligations are recorded as owed work rather than shipped as
  MUSTs nobody can verify. A MUST that cannot be checked fails the bar this
  release is trying to set.

L14 is the shape of the whole section. Five of the six weighted Risk Factor
inputs are aggregations over the Context Signals catalogue. `moment_criticality`
is not — it is supplied by the action request, by whoever is asking. That is a
real asymmetry, it is not fixed in this release, and it is now written at the
input's own definition. Declared, it is a limit. Undeclared, it is the next
audit finding.

## Naming things by what they are

Three renames break the wire, and each has a reason that is not taste.

**The lineage stages.** `tethered` / `divergent` / `persistent` become
`sponsored` / `independent` / `guarantor`. The original question was whether
"tethered" collided with a security meaning. The answer inverted it: there is no
*competing* reading, there is an *agreeing* one. In jailbreak and intrusion
vocabulary, a tethered compromise dies at reboot and a persistent one survives a
restart, so the three words together read as a coherent escalation narrative
rather than as a maturity ladder — and the set's own threat model uses
"persistent" that way, four hundred lines from a section describing a fully
matured agent. Stage 3 is now named for what it can be held to rather than what
it is freed of.

**The top tier.** God Mode becomes Admin Mode, `TRUST_TIER_ADMIN`. The ladder
was already an administrative one — Observer, Analyst, Operator, then full
infrastructure control — and a tier name should label rather than teach. Not
Super Admin: "super" means unrestricted wherever it is used, and the Mass
Ceiling still binds. The one surviving use of the old phrase is
`ktp-governance`'s antipattern, in quotation marks, which is where it belongs.

**The letter scheme.** The six weighted inputs were keyed `m`, `p`, `h`, `t`,
`i`, `o` on the wire. The JSON key is now the name: `evidence_density`,
`trust_trend`, `adversarial_pressure`, `moment_criticality`,
`update_resistance`, `attestation_coverage`. The argument is not readability.
A lettered key is a second naming authority, and a second authority drifts —
`ktp-identity`'s machine-readable examples carried a key `"v"` that the
six-letter scheme never defined. It stood in Momentum's slot. Any implementation
that accepted it was reading Momentum whether or not the specification said so.

The Soul veto leaves the weighted vector entirely. `R` aggregates six inputs;
Soul is evaluated before aggregation and is not a term in it. The published
worked examples had always used six and the schema had always required seven,
and the schema was the one that was wrong. A weighted Soul lets a sufficiently
good score outvote a sovereignty constraint, which is the single outcome a veto
exists to prevent.

## What an implementer gets

**Numbers that reach each other.** The tiers are reachable from the ceilings.
Where a tier is *not* reachable, the specification says so and says why: Admin
Mode requires a zone Mass Ceiling of at least 95, and a zone implementing
progressive trust taxation does not offer it at all — that curve saturates at
87, which is below the threshold under any live deflation. This is stated as a
trade a zone makes rather than left as a gap an operator discovers in
production.

**One bound instead of two.** The per-tier `Max A` column is deleted. A tier
permits action classes; `A ≤ E_trust` is the numeric bound, and it is the only
one. Two numeric bounds keyed to each other is how the drift got in.

**Schemas that resolve.** The published `$id` base moves to a versioned path on
a domain the project owns, and serves `application/json`. Two of the v1 `$id`s
named files that did not exist. `risk-factors.json` replaces
`context-tensor.json`; `transaction-record.json` and `sponsorship-bond.json` are
promoted from document appendices to published files; a new
`deployment-profile.json` is the surface on which a deployment declares
everything the set requires it to declare. Where an Internet-Draft-formatted specification
previously inlined a schema, the appendix now carries a location and a SHA-256.
A hand copy drifts silently — this one had, in four ways, while nobody could
validate either side. A hash cannot.

**Failure that fails closed.** Every weighted term is a stress term: 1 is
maximum stress, 0 is its absence, and the substitute for a term that cannot be
observed is 1.0, never 0. The rule is checked at three layers — feed, signal,
term — and they do not collapse, because a signal can be unavailable while every
feed populating it is healthy. Two live defects in v1.0.x close here, both
recorded in [`SECURITY-NOTES.md`](SECURITY-NOTES.md): a stale feed no longer
holds its last value, and `default_on_failure` can no longer be set to zero,
which in v1 meant turning sensors off raised the trust score.

**Requirements language that means something.** Seven documents acquire the
BCP 14 paragraph; between them they carried 132 capitalized keywords and none of
the sentence that makes a keyword a keyword. `ktp-migration` carries no
normative requirement at all and is now marked informative in full, rather than
being read as though it did.

**A wider catalogue, and a rule about what it measures.** Context Signals goes
from 1,627 signals across six domains to 1,644 across seven. The new domain is
Meta: seventeen signals measuring the quality of the measurement itself, which
previously had no home and was being read out of a domain that measures the
environment. The catalogue's scope line is now stated — it measures the
environment's present; the agent's trajectory lives in `ktp-identity` — and both
totals are re-derived mechanically rather than copied.

## What breaks, and why now

Everything above that touches the wire breaks a v1.0.1 implementation, and
**there is no dual-accept period**. That is a decision, not an oversight. No
rename or negotiation machinery exists anywhere in the set; building some would
be new normative surface in a release whose entire argument is that the existing
surface was not checked. The conformant population is small and known, an agent
identifier re-mints on every generation advance, and the cost of breaking rises
with every implementation that ships against the wrong numbers.

Your v1.0.1 pin keeps working. A published tag is never moved, so the text you
built against stays reachable at that tag permanently, and a normative reference
naming v1.0.1 in its title stays accurate for the version it pins.

## The bar

Success criteria for this release were written to be checkable, because a
criterion that is not checkable is an aspiration:

- `check-vocabulary.py` exits 0 — 240 unmarked occurrences of retired
  vocabulary at baseline, zero now, and the checker reads shapes as well as
  words, so a reintroduction cannot pass as clean.
- `check-parity.py` exits 0 — every summary in step with its source.
- `check-declarations.py` and `check-repo-hygiene.py` exit 0 — every required
  declaration present, and only files a future reader needs are tracked.
- `gen-rfc-txt.sh --check` exits 0 — the five Internet-Draft-formatted specifications regenerate
  byte-identical from source.
- `109-90-reachability.py --check` reports zero failures.

The gates caught this release's own editors twice during the final landing
batch, which is the only evidence that matters about whether a gate works.

## Why Gödel

Releases in this series are named for whoever proved the principle the release
turns on. v1.0.0 was Lovelace, for the first specification of a machine that
had not been built.

This one is named for the result that a sufficiently expressive system cannot
establish its own consistency from the inside. The release earned the name
twice. The set could not have told you it was contradicting itself — it took
reading two documents side by side, and then a script, to find out. And the
release's own answer to the problem is the anchor invariant: nothing certifies
itself, and every chain of accountability must terminate outside the graph it
is making claims about.

Section 10 is the same admission, kept honest: fourteen things this
specification does not settle, written down in the specification rather than
discovered by whoever deploys it.
