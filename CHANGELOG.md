# Changelog

What changed between releases of the KTP RFC series, and what forced each
change.

This file records **normative** changes: an entry is here if a conformant
implementation of the previous release stops being conformant, or if new
required behavior appears. Editorial work — reflow, link repair, prose that
changes no requirement — is not listed.

Every entry names the finding behind it. A change with no finding behind it is
a preference, and preferences do not belong in a normative set. Three findings
account for most of v2.0.0, and they are named throughout:

- **the reachability matrix** — `109-90-reachability.py`, which checks every
  numeric gate in the set against every other at four values of `R`. It was
  written because three arithmetic defects had already been found by hand, one
  at a time.
- **the falsification program** — the comparison corpus that asked what the
  specification would have to say to be wrong about something, and produced
  obligations the set had not discharged.
- **the corpus audit** — reading the files. Most of what follows was found by
  one document being read next to another that contradicted it.

Read alongside [`VERSIONING.md`](VERSIONING.md) (what MAJOR, MINOR and PATCH
mean here, and why a published tag is never moved),
[`SECURITY-NOTES.md`](SECURITY-NOTES.md) (defects in a published version,
recorded when found rather than held for the release that corrects them), and
[`MIGRATION.md`](MIGRATION.md) (what a v1.0.1 implementer has to change).

---

## 2.0.0 — Gödel

**Date:** 2026-08-14 · **Previous:** 1.0.1 (`v1.0.1-provenance`, 2026-07-18)

MAJOR. The break is deliberate and there is no dual-accept period: an
implementation reads v1 or it reads v2. No rename machinery exists anywhere in
the set, the conformant population is small and known, and an agent identifier
re-mints on every generation advance, so the cheap moment to break is now.

Four documents carry a *Changes from v1* appendix — `ktp-core`, `ktp-identity`,
`ktp-enforce`, `ktp-conformance`. `ktp-problems` changed nothing normatively
and takes none.

### Trust Score calculation

- **`E_base` is a hundred-point allocation. The domain weights are removed;
  each term contributes at most its declared share, and the shares MUST sum to
  100.** *Forced by:* the corpus audit — `ktp-identity` §5.3 states Proof of
  Resilience as a *contribution* capped at 70, and `ktp-core` §5.1 then
  multiplied that contribution by a 70% weight. The same 70, spent twice: a
  maxed-out Proof of Resilience was worth 49 rather than 70, and the External
  Root's 30 was worth 9. It is a type error, not a calibration question.
- **Proof of Resilience is stated once. `ktp-core` no longer restates
  `ktp-identity`'s formula.** *Forced by:* the corpus audit — one quantity had
  two signatures in two documents, and neither cited the other.
- **The External Root term is fixed at a share of 30 and is subject to an
  anchor invariant: no composition of `E_base` may consist entirely of terms
  the subject measures about itself.** *Forced by:* the falsification program's
  no-self-certification obligation, which ships as limit L2.
- **An attestation MUST declare its chain terminator and chain length, the
  length MUST NOT exceed the deployment's declared hop bound, and the hop bound
  MUST NOT exceed 12. An undeclared terminator or an over-long chain computes
  the term as zero.** *Forced by:* the falsification program — a cycle of
  agents attesting for one another satisfied the published text.
- **An attestation MUST declare the attestor's exposure and the capacity it
  anchors, and the exposure MUST be irrecoverable and non-transferable — it
  cannot be shed by abandoning the attestor's identity. An attestation
  declaring no exposure computes as zero; a declared exposure found not to
  exist, or found transferable, is misattestation.** *Forced by:* the
  falsification program's root-mass obligation. The shell-company attack
  becomes attributable and priced rather than free.
- **Concurrent attestations score as the maximum single instrument, never a
  sum.** *Forced by:* the falsification program — concurrency is redundancy
  against withdrawal, and summing turned a hedge into an increase.
- **Attestation withdrawal is split by cause: for-cause zeroes the instrument
  immediately; without-cause makes the attestation irrevocably non-renewable
  and it holds to its declared expiry. The attestor MUST state which, the
  deployment MUST declare an adjudicator that is neither attestor nor subject,
  and a for-cause claim that does not survive scrutiny is misattestation.**
  *Forced by:* the corpus audit — v1 priced issuance and left withdrawal
  unpriced, which made withdrawal a weapon.
- **Peer signals occupy a distinct declared term and MUST NOT be folded into
  Proof of Resilience or the External Root. The deployment declares its peer
  share in the Trust Proof, and a relying party MUST NOT compare `E_base`
  magnitudes across deployments declaring different shares.** *Forced by:* the
  §5.1 rewrite — under the allocation rule an undeclared peer term silently
  moves the other two.
- **Ceilings compose under `min()`, the Identity Assurance Level ceilings
  (40 / 80 / 95) join the table, and every ceiling applicable to an evaluation
  MUST be declared in the Trust Proof.** *Forced by:* the corpus audit — real
  ceilings existed in `ktp-identity` §7.1 that the composition never consulted.
- **No class of grant lifts a ceiling. Maturity raises a ceiling; it does not
  contribute standing.** *Forced by:* the corpus audit — seven mechanisms
  granted `E_base` outside the composition, including `ktp-zones` §9.3.6's
  genesis grant of 50 against a generation-0 ceiling of 25.

### Trust Tiers

- **Thresholds move: Admin 95 → 85, Operator 85 → 72, Analyst 70 → 58,
  Observer 50 → 22, Hibernation < 50 → < 22.** *Forced by:* the reachability
  matrix. Four ladders run over one quantity — tier thresholds on `E_trust`,
  generation ceilings and zone Mass Ceilings on `E_base` — with `E_trust =
  E_base × (1 − R)` between them, and the gap between a ceiling and the
  threshold it admits is an `R` budget nobody had ever set. The published gaps
  were 0, 5, −5 and −2 by accident. Admin was unreachable in all four zone
  classes at the corpus's own calm worked example (`R = 0.094`, 95 × 0.906 =
  86.1), and generation ceilings of 25 / 35 / 45 sat *below* the lowest
  threshold of 50, so every agent spent its first 545–725 days in Hibernation,
  whose only permitted action is a heartbeat. The generation ceilings are
  unchanged: one table moved, not two.
- **Hibernation exit moves from `E_trust >= 55` to `E_trust >= 24`.** *Forced
  by:* the same ruling — five points of hysteresis over a floor of 50 is
  thirty-three points over a floor of 22.
- **The Admin stable-conditions requirement moves from `R < 0.05` to
  `R < 0.10`.** *Forced by:* the reachability matrix — 0.05 is stricter than
  the calm baseline the corpus itself illustrates.
- **God Mode is renamed Admin Mode. `TRUST_TIER_ADMIN`; the OpenAPI enum value
  `god_mode` becomes `admin`; the protobuf numeric value is unchanged.**
  *Forced by:* the vocabulary sweep — the set was already an admin ladder
  (Observer → Analyst → Operator → full infrastructure control), and a tier
  name should label rather than teach. The `ktp-governance` antipattern
  survives in quotation marks, which is the only remaining use.
- **Admin Mode is available only in zones whose Mass Ceiling is at least 95.**
  *Forced by:* the reachability matrix — the tier's threshold is derived from
  that ceiling at its declared `R` budget, and a lower-ceiling zone cannot
  deliver it at any generation. The last reachability failure closes as a
  declaration rather than as a silent gap.
- **A zone implementing `ktp-enforce` §9.5 progressive trust taxation does not
  offer Admin Mode; such a zone's capability planning MUST proceed from
  Operator Mode as the highest attainable tier.** *Forced by:* the reachability
  matrix — the taxed curve saturates at 87, which under any live deflation sits
  below 85. The section exists to discourage accumulation and the top tier *is*
  accumulation, so the trade is stated instead of hidden inside a curve.
- **The per-tier `Max A` capability matrix is deleted.** *Forced by:* the
  corpus audit — a tier permits action classes, `A <= E_trust` is the numeric
  bound, and a second numeric bound keyed to the thresholds was the mechanism
  that generated the drift in the first place.
- **A per-phase Trust Tier cap is no longer stated.** *Forced by:* the same —
  a phase bounds `E_base` through the generation ceiling, and the environmental
  deflator sits between that and any tier.

### Lineage and identity

- **The three lineage stages are renamed: `tethered` → `sponsored`,
  `divergent` → `independent`, `persistent` → `guarantor`. This affects agent
  identifier strings, the `lineage` enum, and the protobuf `LineageType` member
  names; the numeric protobuf values are unchanged.** *Forced by:* the corpus
  audit — the v1 words each carry a security reading that *agrees* with the
  wrong meaning rather than competing with it. In jailbreak and intrusion
  vocabulary "tethered" is a compromise that dies at reboot and "persistent" is
  one that survives a restart, so the three together read as an escalation
  narrative rather than a maturity ladder. The same document's threat model
  uses "persistent" that way, unremarked. Stage 3 is now named for what it can
  be held to rather than what it is freed of.
- **The rank scaffolding is removed with the stages — Apprentice, Journeyman,
  Master, the emoji, and "Special privileges".** *Forced by:* the same ruling.
- **Lineage phase derives from generation: 0–2 sponsored, 3–6 independent,
  7 and above guarantor. The §8.1 and §8.2 `Duration:` gates are deleted, and
  §8.4 is the sole advancement rule.** *Forced by:* the corpus audit — two
  advancement gate families ran over one lineage and disagreed. An agent at
  Resilience Score 1,001 on day 31 was Divergent under §8.1 and Tethered under
  §8.4. No agent is in two phases at once, which the identifier format
  requires.
- **The generation clock changes from a flat 60 days per step to a seven-step
  widening clock: 90, 90, 365, 180, 180, 180, 2,555 days — 3,640 days in
  total.** *Forced by:* the reachability matrix's companion ruling — a step's
  cost scales with whether it changes kind or amount, and the two regime
  changes are tether release at 2 → 3 and the terminal ceiling at 6 → 7. The
  survival condition is a claim about the absence of a rare event, which cannot
  be observed over a window shorter than its return period.
- **The per-generation Resilience quota demotes from a gate to a declared
  floor, with time as the primary gate. A deployment MUST declare the floor and
  the Trust Proof MUST carry the declared value; a deployment whose environment
  produces no attestable friction declares zero.** *Forced by:* the same
  ruling. The published default is recorded as owed work — deriving it needs
  the evidence curve, and a default nobody can derive is not checkable.
- **A Sponsorship Bond closes without releasing. The taper holds at a floor of
  `0.1^depth × stake_amount` and the floor never lifts; the retained share is
  named Ancestral Liability.** *Forced by:* the corpus audit — §6.4 returned
  the sponsor's stake at stage-2 entry while §8.2's taper still charged 50% of
  it at that exact point. The fix invents no constant: §8.5 already gave an
  ancestor's *credit* to its descendants forever at `0.1^depth`, and the set
  was taking the credit permanently while releasing the liability at stage 2.
  Credit and liability now travel the same lineage at the same decay.
- **Ancestral Liability's collateral matches the residual permanently, so the
  anti-botnet bound becomes cumulative as well as concurrent.** *Forced by:*
  the same ruling — exposure that is not funded is not exposure.
- **A bond's declared `duration` binds staked capital only, not the liability.**
  *Forced by:* the same ruling — `duration` is sponsor-declared, so without
  this a one-day bond defeats the taper at creation.
- **Ancestral Liability discharges only on a for-cause claim surviving
  adjudication. Decommissioning passes the residual up the lineage at its
  current value.** *Forced by:* the same ruling — recomputing at the receiving
  depth would make retirement a 90% exit.
- **The stage-3 threshold is `intrinsic_E_base > 80`.** *Forced by:* the corpus
  audit — it was stated twice, twenty points apart, in adjacent subsections.
- **The published stake taper no longer returns negative above
  `intrinsic_E_base` 80.** *Forced by:* the same read — at 100 it credited the
  sponsor `−0.25 × stake` for a descendant's standing, unevaluated only because
  the bond was declared released before it could bite.
- **The bond halving and the stake taper are scoped to bond accounting and are
  not inputs to the `E_base` composition.** *Forced by:* the §5.1 rewrite — a
  fourth sponsor-contribution formula was found by reading the file, in no
  ticket and no prior record.
- **Sponsor-initiated bond termination is specified, split by cause.** *Forced
  by:* the corpus audit — v1 specified only the sponsored agent's exit.
- **Standing decays. A deployment MUST declare `standing_decay_rate` in points
  of Proof of Resilience lost per year of inactivity, within [2, 20],
  RECOMMENDED 16; evaluation is lazy, so the declared rate and the record's
  timestamps reproduce any value deterministically.** *Forced by:* the corpus
  audit — `E_base` only ratcheted up. The parameter is stated in the units of
  the thing it moves: because the contribution is logarithmic, exponential
  decay of the evidence is linear decay of the points, at a slope independent
  of the agent's standing.
- **`ktp-zones` §9.3.6's genesis grant of `E_base` 50 becomes the generation-0
  ceiling of 25, and the nursery consequence is stated: at that ceiling a
  genesis agent clears the Observer floor of 22 only while `R` stays below
  0.12.** *Forced by:* the corpus audit — being first in a zone is not evidence
  of resilience, and the grant was reaching past every ceiling.

### Risk Factors

- **The Soul veto leaves the weighted vector. `R` aggregates six weighted
  inputs; Soul is evaluated before aggregation and is not a term in it —
  six-plus-veto, not seven.** *Forced by:* the corpus audit — the published
  examples used six and the schema required seven. A weighted Soul lets a
  sufficiently good score outvote a sovereignty constraint, which is the one
  thing a veto exists to prevent.
- **The letter scheme leaves the wire: the JSON key is the name. The object is
  `risk_factors`, never `context_tensor`.** *Forced by:* the vocabulary sweep —
  a lettered key is a second naming authority, and it drifted. `ktp-identity`'s
  own machine-readable examples carried a key `"v"` that the six-letter scheme
  never defined; it stood in Momentum's slot, and a v1 implementation that
  accepted it was reading Momentum whether or not the specification said so.
- **The six weighted inputs are renamed to what they measure:**

  | v1 letter | v1 name | v2.0.0 key |
  |---|---|---|
  | `m` | Mass | `evidence_density` |
  | `p` (and the stray `v`) | Momentum | `trust_trend` |
  | `h` | Heat | `adversarial_pressure` |
  | `t` | Time | `moment_criticality` |
  | `i` | Inertia | `update_resistance` |
  | `o` | Observer | `attestation_coverage` |
  | `s` | Soul | `soul` — veto, not a weighted term |

  *Forced by:* the vocabulary sweep. Physics words survive only on
  `Analogy (informative):` lines.
- **Every weighted term is a stress term in [0, 1]: 1 is maximum stress, 0 is
  its absence, whatever the term is named. A deployment MUST NOT substitute 0
  for an unobserved term; the conservative substitute is 1.0.** *Forced by:*
  the corpus audit — with the renames, several inputs read as desirable
  quantities, and the direction had never been stated for the class.
- **Unobservability is checked at three layers — feed, signal, term — and a
  deployment MUST apply the rule at each. The layers do not collapse: a signal
  can be unavailable while every feed populating it is healthy.** *Forced by:*
  the corpus audit — the rule existed at the feed layer only, and a rate over
  an empty set of eligible events has no failed feed in it anywhere.
- **Undefined fails closed as a class, ruled once rather than per surface: an
  unknown environment reads as low capacity, not high.** *Forced by:* the
  corpus audit — the rule existed four times in four vocabularies, binding
  nothing, which is why four separate tickets each had to ask again.
  `ktp-recovery`'s "when in doubt, deny" is amended as too strong: silence and
  absence do not separate.
- **An unanswered sovereignty query is not clearance. `ktp-federation` §4.3
  gains the branch for silence.** *Forced by:* the same class ruling.
- **An aggregation over a window that defines no samples omits the statistic
  rather than reporting one. `sample_count` is REQUIRED.** *Forced by:* the
  corpus audit — `ktp-core` §5.9 already prohibited substituting a measured
  value for an undefined one "including zero", and a mean over an empty window
  is exactly that substitution.
- **`moment_criticality` is declared externally supplied — it arrives with the
  action request rather than as an aggregation over the catalogue, and the
  asymmetry is stated at its definition.** *Forced by:* the falsification
  program. Declared, it is a limit (L14); undeclared, it is the next audit
  finding.
- **The carriage interface for normative content is fixed: norms enter as a
  veto, a supplied input, or a gate, and MUST NOT rewrite the aggregation.**
  *Forced by:* the falsification program's two-rails finding — an amoral
  prudence rail whose disputes resolve by measurement, and a normative rail
  authored outside whose disputes resolve only by governance. Shipped as limit
  L11.
- **`sensor_health` reshapes from flat letter-prefixed keys to a keyed object:
  one health object per input, keyed by the input's name, and
  `degraded_dimensions` becomes `degraded_inputs`.** *Forced by:* the
  vocabulary sweep — this was the last letter residue on the wire.

### Sensors

- **The Stale Behavior column is deleted. A feed whose most recent observation
  has passed its `stale_threshold_ms` is unavailable, and §6.2's existing
  failure ladder governs.** *Forced by:* the corpus audit, recorded as
  [SN-001](SECURITY-NOTES.md). §6.1's "use last known" and §6.2's maximum
  stress value answered the same question differently, eleven lines apart, and
  §7.1 of the same document already named the attack that "use last known"
  enables. No new machinery: `stale_threshold_ms` shipped in v1.0.0 and was
  never given a behavior.
- **`default_on_failure` is floored at 0.5, defaults to 1, is REQUIRED on every
  dimension that is not veto-aggregated, and is pinned to `const: 1` where
  aggregation is `any_veto`.** *Forced by:* the corpus audit, recorded as
  [SN-002](SECURITY-NOTES.md). The published schema described the field as a
  conservative default and permitted 0, so a schema-valid one-key configuration
  scored an unmonitored environment as risk-free — turning sensors off raised
  the trust score.
- **`sensor-config.json` admits `0` for `refresh_interval_ms` and
  `stale_threshold_ms` and states that it means queried on demand.** *Forced
  by:* the same read — the schema's own second example had never validated
  against the schema publishing it.

### Context Signals catalogue

- **A seventh domain, Meta, is added: 17 signals measuring the quality of the
  measurement itself. The catalogue moves from 1,627 signals across six domains
  to 1,644 across seven.** *Forced by:* the corpus audit — measurement freshness
  and coverage had no home and were being read out of the Time domain, which
  measures the environment rather than the instrument.
- **The catalogue is its own object: `catalog/*.json` is canonical and the
  markdown tables are generated from it.** *Forced by:* the corpus audit — the
  headline count was a copy in fifteen places, which is exactly the shape of the
  earlier defect where a published total was never derived from its parts. Both
  1,627 and 1,644 are re-derived mechanically, and the class census closes
  exactly on all seven domains.
- **The per-signal measurement envelope is adopted: subject, population and
  observation window are MUST slots, and a signal's shape class decides which
  further slots bind.** *Forced by:* the falsification program — a quantity
  without a population and a window is not measurable, and the set was
  publishing signals that could not be checked. The envelope does not ride the
  wire; it stays with the aggregator.
- **The declared-derivatives rule: a derivative MUST declare its base signal,
  its form, and the window it is computed over — a derivative is undefined
  without its window — and derivatives are marked as derived and never counted
  as new observations of the environment.** *Forced by:* the falsification
  program's time-shape gap. The Meta domain's refresh signals are what make the
  window checkable.
- **The catalogue's scope line: it measures the environment's present. The
  agent's trajectory lives in `ktp-identity`.** *Forced by:* the same ruling —
  the boundary was assumed everywhere and stated nowhere.
- **The missing-data rule gains a cross-class clause: a signal reporting unknown
  MUST NOT contribute as though it observed zero risk, and an empty denominator
  is unknown rather than zero.** *Forced by:* the corpus audit — the rule was
  carried for one shape class while 68 of the Soul domain's 78 bare 0–1 rows are
  ratios over eligible-event sets that can be empty, and none of them is in that
  class.
- **Unit and range corrections land across the catalogue, and four
  identical-name pairs are aliased rather than merged.** *Forced by:* the
  normalization audit; the corrections are count-neutral.

### Enforcement and the envelope

- **The decision contract is the envelope result, and the four decision verbs
  derive from it.** *Forced by:* the corpus audit — the verbs were used
  throughout the set and defined nowhere.
- **The kinetic envelope's provider interface is declared rather than assumed,
  and two of its six provider properties are marked declare-your-instance
  rather than fixed.** *Forced by:* the corpus audit — two properties were
  substrate-bound to one robotics stack and unmarked, so a conformant
  implementation on any other substrate was impossible to write.
- **`ktp-enforce`'s introduction names the prudence rail and states its
  condition: it stays amoral only while its parameters are declared, and an
  undeclared prudence constant is a smuggled norm.** *Forced by:* the
  falsification program's two-rails finding.

### Limits

- **`ktp-core` gains section 10, *Limits of This Specification*: fourteen
  entries, L1 through L14, ordered hardest to softest — from a halting-problem
  reduction to a declared-provenance asymmetry.** *Forced by:* the falsification
  program, and by the release's own success criterion that every normative MUST
  be checkable. Declared-but-unmechanized obligations are recorded as owed work
  rather than shipped as unverifiable MUSTs, and open questions ship as
  boundaries fixed in advance rather than as answers invented under tag
  pressure.

  | | |
  |---|---|
  | L1 | Pre-execution episode classification is undecidable |
  | L2 | No self-certification |
  | L3 | Level-independence is conditional |
  | L4 | The judgment term is exposed to metric gaming (open) |
  | L5 | The terminal generation ceiling never binds arithmetically |
  | L6 | Episode overlap has no declared precedence mechanism (staged) |
  | L7 | Some catalogued quantities are named, not measured |
  | L8 | A value that encodes a classification is not an observation |
  | L9 | Declared non-coverage |
  | L10 | E carries no cardinal consequence units |
  | L11 | There are two SHOULD rails, and only one of them is this specification's |
  | L12 | The privacy marker has no stated rule |
  | L13 | The resilience evidence curve is uncalibrated |
  | L14 | One Risk Factor is externally supplied, and the specification says so |

  Sections 10 through 12 renumber to 11 through 13.

### Schemas

- **The published `$id` base moves from `https://ktp.example.org/schemas/` to
  `https://kinetic-trust-protocol.net/specs/schemas/v2/` — a versioned path on
  a domain the project owns, serving `application/json`.** *Forced by:* the
  corpus audit — two published `$id`s named schemas that did not exist and a
  third was a drifted hand-copy. The schemas now resolve to themselves.
- **`context-tensor.json` is deleted. `risk-factors.json` replaces it, with the
  six named keys and `additionalProperties: false`.** *Forced by:* the
  six-plus-veto ruling and the vocabulary sweep.
- **`trust-proof.json` gains four required claims: `peer_share`,
  `applicable_ceilings`, `advancement_floor`, and `root_instrument`.** *Forced
  by:* the §5.1 rewrite and the advancement-floor ruling — each is a value a
  relying party must have to evaluate `E_base` at all, and none of them was on
  the wire.
- **`transaction-record.json` and `sponsorship-bond.json` are promoted from
  document appendices to published schemas.** *Forced by:* the corpus audit —
  the transaction record's inline letter-keyed environmental object was the
  drifted hand-copy, and the field renames to `risk_factors` with a `$ref` in
  its place.
- **`soul-constraint.json` renames `s` to `soul` and keeps it as
  `integer enum [0, 1]`; `sensor-config.json` gains a named dimension enum.**
  *Forced by:* the letter-scheme retirement.
- **`deployment-profile.json` is added: the declaration surface for every
  parameter the set requires a deployment to declare. `profile_id`, `version`,
  `risk_factors`, `soul_veto`, `peer_share`, `external_root` and
  `standing_decay_rate` are required.** *Forced by:* the accumulation of
  declare-or-be-penalized rulings across the release — each created an
  obligation to declare, and none of them had a surface to declare on.
- **The four inline appendix schemas in the Internet-Draft-formatted specifications become a
  reference plus a SHA-256 of the canonical file.** *Forced by:* the corpus
  audit — a hand copy drifts silently and this one had, disagreeing with the
  published file in four ways while nobody could validate either. A hash cannot
  drift silently.

### Requirements language and document scope

- **Seven documents acquire the BCP 14 requirements-language paragraph —
  `ktp-conformance`, `ktp-human`, `ktp-privacy`, `ktp-problems`, `ktp-recovery`,
  `ktp-sensors`, `ktp-threat-model` — and `ktp-conformance` moves RFC 8174 from
  informative to normative references.** *Forced by:* the release's success
  criterion that every normative MUST be checkable. Between them these
  documents carried 132 normative keywords and none of the paragraph that gives
  those keywords meaning; the largest was `ktp-conformance` at 47, which is the
  document the criterion is evaluated through.
- **`ktp-migration` is marked informative in full. It states no normative
  requirement and uses no BCP 14 keyword, and where a value in it differs from
  the normative set, the normative set governs.** *Forced by:* the same read.
- **`ktp-migration` §5.1.1's role table loses its Trust Tier column.** *Forced
  by:* the reachability matrix — no static column can name the tier a given
  `E_base` produces, because the deflator is neither in the table nor constant.
  Three of six rows named a tier their own number could not reach under the
  conditions the set's own worked examples use.
- **Three specifications are renamed for what they contain rather than for a
  retired object: `ktp-gravity` → `ktp-attenuation`, `ktp-tensors` →
  `ktp-signals`, `ktp-signal` → `ktp-information`.** *Forced by:* the vocabulary
  sweep.
- **The retired vocabulary is out of the normative set: Context Tensor, Digital
  Physics, "physics-derived", and the "physics" claim itself.** *Forced by:* the
  vocabulary sweep — nothing in the set transforms tensorially, and the
  coordinate attack that name invited was never answerable. `scripts/check-vocabulary.py`
  is the authority, and it reads shapes as well as words.

### Repository and format

Not normative, but it changes how the set is consumed.

- **`rfc-src/` is the single source. All 27 specifications are authored as
  kramdown-rfc markdown; `rfcs/*.md` remains the summary layer and no published
  URL moves.**
- **Only five specifications ship a `.txt` — `ktp-core`, `ktp-identity`,
  `ktp-problems`, `ktp-enforce`, `ktp-conformance` — generated by
  `scripts/gen-rfc-txt.sh` and never hand-edited.** The toolchain has no non-I-D
  mode, so generating a `.txt` *asserts* Internet-Draft status; the other 22
  disclaim it and render as markdown. The 22 hand-authored `.txt` files are
  deleted, and a generate-and-diff gate is armed over the five.
- **The gates are executable:** `check-vocabulary.py`, `check-parity.py`,
  `check-declarations.py`, `check-repo-hygiene.py`, `gen-rfc-txt.sh --check`,
  and the reachability matrix's `--check`. Checkable, or they are aspirations.

---

## 1.0.1 — Provenance infrastructure

**Tag:** `v1.0.1-provenance` · **Date:** 2026-07-18

No normative change. `NOTICE`, `CITATION.cff` and `PROVENANCE.md` added; README
link and count repair; `ktp-problems.txt` synchronized to v0.2. The descriptive
tag suffix was a one-time deviation from the tag rule and is left in place,
because published tags are not moved.

## 1.0.0 — Reference Implementation (Lovelace)

**Tag:** `v1.0.0`

The first fixed point for the series. Two defects found in it after
publication are recorded in [`SECURITY-NOTES.md`](SECURITY-NOTES.md) as SN-001
and SN-002; both are corrected in 2.0.0.
