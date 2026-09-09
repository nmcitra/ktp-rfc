# The Deployment Profile

**The declaration surface for a KTP deployment.** Status: v0.1 (interface + conformance). Canonical KTP specification.

The specification series keeps requiring declarations rather than publishing constants — the peer-signal share, the sponsorship chain's terminator and hop bound, the normalization function behind every synthetic score, which member of an alias set a deployment populates, the signals behind each Risk Factor. Each of those obligations was ruled separately, and until this document none of them had a place to be discharged: **a framework that requires declarations and provides no declaration site has an obligation nobody can discharge** (nmcitra/ktp-rfc#108, consolidating #101 and #106).

This document is that site. It defines one object — the **deployment profile** — carrying every deployment-level declaration the series requires, so that the alias declarations, the Risk Factor bridge, and the feed mapping are one schema rather than three that have to agree. The machine form is `schemas/deployment-profile.json`; `scripts/check-declarations.py` validates a profile instance against both the schema and the catalogue.

## What a declaration is

A declaration does not fix a value the specification left open by accident — it marks a choice the specification *requires* the deployment to make, makes that choice explicit and machine-readable, and lets a relying party evaluate conformance against it. The pattern is declare-or-it-does-not-count, in force five times before this document existed:

| obligation | source |
|---|---|
| the peer-signal share, declared in the Trust Proof | `ktp-core` §5.1 (per #51) |
| the sponsorship chain's terminator and hop bound, declared or the term is zero | `ktp-core` §5.1 (per #47/#51) |
| a bare-`0-1` synthetic score's normalization function, declared or it MUST NOT aggregate | `catalog/index.md` §6 |
| which ID of an alias set the deployment populates | `catalog/index.md` §7 |
| the undefined state, recorded on the decision record | `ktp-core` §6.7 (per #110/#105) |

## The profile object

A profile is identified by `profile_id` and `version`. Records produced under a profile reference it as `<profile_id>@<version>` — this is the **normalization-profile identifier** that `[KTP-AUDIT]` §3.2's `sensor_health` block carries (per #72), which is how a stored record self-flags the class of unit-mismatch defect that motivated it: a value computed under one profile must not be replayed against another.

The active, unreleased schema identifier is `https://kinetic-trust-protocol.net/specs/schemas/v3/deployment-profile.json`. The byte-preserved published v2 schema remains at [`deployment-profile-legacy-v2.json`](../schemas/deployment-profile-legacy-v2.json), retaining its original v2 identifier and SHA-256 `c0087dc3662b8ef1988f7d612a779ca38f2b771454a45fc33abaaed6f2ebb3f2`. Archival validation does not authorize active use or a fallback from the required standing policy.

| section | declares | required |
|---|---|---|
| `risk_factors` | which Context Signals feed each of the six Risk Factors, by what aggregation, at what weight | yes |
| `soul_veto` | the sovereignty frameworks queried before aggregation | yes |
| `feeds` | which signals each configured feed populates | yes, where feeds are configured |
| `aliases` | which member of each populated alias set this deployment populates | yes, per populated set |
| `normalization` | the normalization function behind each aggregated synthetic score | yes, per aggregated synthetic signal |
| `label_sets` | the label set behind each categorical signal and denominator predicate | yes, per aggregated categorical signal |
| `peer_share` | the peer-signal share of `E_base`, in points | yes (0 where not implemented) |
| `external_root` | the hop bound and the misattestation adjudicator | yes |
| `human_policy` | operation-specific human profile ID, version and canonical digest | required before accepting humans or human-origin delegation; omission disables that path |
| `standing_policy` | the history-with-scoped-readiness mode and exact readiness profile ID, version, and digest | yes in the active v3 profile; `standing_decay_rate` is rejected |
| `envelope_thresholds` | finite supervision thresholds `0 <= m_veto < m_allow` | optional; absent retains the existing zero-margin veto |
| `emergency_policy` | the exact approved emergency policy ID, version, and payload digest | optional; absent disables emergency capability |
| `oracle_consensus` | the reviewed protocol, authenticated member roster and epoch, fault budget, and decision quorum | required for a Byzantine Oracle Mesh agreement claim; absent provides no such claim |

## Risk Factors — the bridge

`[KTP-CORE]`'s bridge law (D2): **each Risk Factor is a named aggregation over a declared subset of Context Signals. A deployment MUST declare which signals feed which factor and by what aggregation.** The catalogue names what can be measured; the six factors are what the decision consumes; this section is the only place the two meet.

The shape is fixed by #83: **six weighted inputs to R, plus the Soul veto, which is evaluated before aggregation and is not a term in it.** The six factor keys are `evidence_density`, `trust_trend`, `adversarial_pressure`, `update_resistance`, `attestation_coverage`, `moment_criticality` — all six are required, and the schema's `required` array is exactly that list. Each factor declares:

- `signals` — Context Signal IDs from `catalog/`, the declared subset;
- `aggregation` — the named aggregation over them (method plus its parameters);
- `weight` — the factor's weight in `R = sum(w_i * s_i)`.

The six factor weights MUST be finite numbers in `(0, 1]` and MUST sum to 1 (`ktp-core` §6.4). This retains the schema's existing positive-weight requirement. Booleans and non-numeric values are invalid. Validate the complete set before computing `R`, including after reconfiguration; an invalid profile MUST be rejected and MUST NOT be silently rescaled or completed with default weights. Soul remains outside the sum. Per-feed aggregation weights are a separate declaration and are not subject to this six-factor sum check.

The declaration checker sums the decimal representations of the parsed numeric values exactly, without a tolerance. This avoids binary addition noise without accepting a non-unit decimal total. The check uses the numbers produced by the JSON parser; it does not preserve the original numeric token's precision. For rounded repeating fractions, declare the rounding remainder explicitly: five weights of `0.16666666666666666` and one of `0.1666666666666667` sum to 1; six copies of the former do not. The checker validates these choices without modifying them.

Constraints, all quoted from their rulings:

- *a Risk Factor aggregation MUST NOT include more than one ID from an alias set* (`catalog/index.md` §7);
- a signal that does not declare its envelope slots for its observation class MUST NOT be used in a Risk Factor aggregation (`catalog/index.md` §3–§4);
- a synthetic bare-`0-1` signal MUST have a `normalization` entry to aggregate (§6); a categorical signal MUST have a `label_sets` entry to aggregate (§5);
- every term is a stress term whatever it is named: the substitute for an unobservable term is 1.0, never 0 (`ktp-core` §5.2, per #80).

### The Soul veto

`soul_veto` declares the sovereignty frameworks queried per `[KTP-SENSORS]` §4.3. It is not a weighted term: a sufficiently good score must not be able to outvote a sovereignty constraint (#83). If ANY framework returns veto, S = 1; if ANY query is UNDETERMINED — unreachable, error, timeout, or empty — S = 1, one branch, no separation (`ktp-sensors` §4.3, per #105). Only an answering framework returns a clearance.

## Feeds — how the wire reaches the catalogue

The wire and the catalogue name different objects: `[KTP-SENSORS]` §2.2 configures **feeds**, `[KTP-TRANSPORT]` §9.2/§9.3 carry feed readings, and the catalogue names 1,644 **signals**. One feed can populate many signals; one signal can be fed by many feeds. Until the correspondence is declared, the three-layer missing-data rule (`ktp-core` §5.2: feed · signal · term, which do not collapse) is written across a mapping that does not exist — *a signal can be unavailable while every feed populating it is healthy*, and nothing could compute which (#106, opened by #60 and #72).

`feeds` declares it: each entry keys a feed `id` — the join key is the feed's `id` in `[KTP-SENSORS]` §2.2 / `sensor-config.json` — and lists the catalogue signal IDs it `populates`. A signal is available when at least one feed declared to populate it is AVAILABLE under `[KTP-SENSORS]` §6.1; a signal none of whose declared feeds is available reports **unknown, not zero** (`catalog/index.md` §4, sixth clause). This mapping is also the input to coverage measurement (#62).

The mapping **stays in configuration and does not ride the wire** — the same bind-don't-carry answer #72 ruled for the measurement envelope, applied to a declaration that is stable per deployment rather than per observation.

## Aliases

For each alias set in `catalog/index.json` (`alias_sets`, sixteen sets in two shapes) of which this deployment populates any member: declare **which** member it populates. *Implementations MUST declare which ID they populate* (`NORMALIZATION-01` §A, normative; #86 extends the mechanism to collision sets, where neither member is canonical and both are legitimate rows of different subjects).

## Normalization

*A signal whose range is a bare `0-1` MUST declare its normalization function … in the deployment profile* (`catalog/index.md` §6) — narrowed by the ruled three-way sort to the **synthetic** rows only, which are marked `zero_one: "synthetic"` in the catalogue JSON. Each entry declares the method and its parameters. Ratio rows declare their denominator as population on the catalogue row, not here; fully determined rows declare neither.

## Label sets

*A signal whose value requires assigning observations to categories MUST declare, in the deployment profile, the label set it populates; a signal with no declared label set MUST NOT be used in a Risk Factor aggregation* (#68; `catalog/index.md` §5). A denominator predicate — `healthy`, `available`, `critical`, `active` — is a label set and is declared here under the signal whose denominator it gates. Derived signals inherit the label set's cardinality.

## Peer share

*The deployment MUST declare the peer share it applies, within the range given in Peer Validation, in the Trust Proof* (`ktp-core` §5.1). The range is `ktp-core` §5.5.5's 10–20 points where peer validation is implemented; a deployment that does not implement it declares zero. A relying party MUST NOT compare `E_base` magnitudes across deployments that declare different shares.

## External Root

Two deployment-level declarations from `ktp-core` §5.1:

- `hop_bound` — the maximum accountability-chain length the deployment accepts. *The length MUST NOT exceed the deployment's declared hop bound, which MUST NOT exceed 12.*
- `adjudicator` — *the deployment MUST declare the adjudicator for findings of misattestation, including for-cause withdrawal claims. The adjudicator MUST be neither the attestor nor the subject agent.*

The attestation-level declarations — terminator, chain length, exposure and its class, anchored capacity, instrument status — ride the attestation and the Trust Proof, not the profile. Their schema carriage rides the #71/#83 schema gate and is listed under *Owed to this surface* below.

## Historical standing and scoped readiness

The active v3 deployment profile MUST declare `standing_policy` with exactly `mode`, `profile_id`, positive integer `version`, and `digest`. The mode is exactly `history-with-scoped-readiness-v1`; the remaining fields identify the independently approved readiness profile defined by [`operational-readiness.md`](operational-readiness.md) and [`readiness-profile.json`](../schemas/readiness-profile.json). Missing or unverifiable policy, a missing declaration, and an older profile MUST NOT select a permissive default. This unreleased schema namespace and policy mode do not announce a production release or authorize installation.

Historical Proof of Resilience is retained without automatic subtraction for elapsed time or inactivity. Authenticated findings may invalidate historical claims through appended corrections; they do not rewrite previously authenticated records. Current readiness is a separate prerequisite for the actual operation and exact subject configuration, not another global score or an additional component of E_base. It is assessed under independently approved criteria by a competent accountable assessor. It adds no standing credit and cannot override any current veto.

The profile MUST define the operation-specific criteria, subject and scope bindings, evidence requirements and freshness, accountable assessment authority, and a separately authorized safe assessment route required by the companion. Evidence-based expiry and actual system, model, tool, configuration, permission, or policy changes control reassessment. Heartbeats, uptime, ordinary activity, re-signing, and ordinary proof refresh MUST NOT renew assessment evidence. Policy installation, revocation, and readiness epochs MUST be authenticated and durable across restore; a candidate's profile reference or a higher version number alone does not authorize a change.

The standing_policy digest binds JCS of the complete readiness profile, while a deployment_profile_digest binds the exact installed deployment-profile bytes. Attestation and decision digests bind their complete signed objects. Their signatures and current registered digest/epoch are independent verification obligations. The reference matcher uses exact subject and scope bindings; broader scope matching requires a separately specified, reviewed restrictive matcher and MUST NOT be inferred from these fields.

The active profile and its readiness policy MUST be installed through incumbent governance authority. Migration durably pins the accepted deployment/profile version, standing-policy mode, evidence format, and readiness epoch. Existing agents keep admissible historical PoR but begin with readiness unestablished for dependent operations until assessed and activated. Referenced declarations and readiness assessments do not authorize themselves.

The decision sidecar defined by [`readiness-decision.json`](../schemas/readiness-decision.json) binds the complete ordinary proof, actual request, complete attestation under [`readiness-attestation.json`](../schemas/readiness-attestation.json), both installed profiles, and current readiness epoch. The PEP MUST match it to the actual operation and live subject at execution while retaining the ordinary ten-second proof limit. A v3 trajectory records the complete sidecar in its existing signed `action.details.readiness` field; this introduces neither a top-level trajectory field nor a hash cycle.

Historical v2 instruction: the published `standing_decay_rate` named a range of 2–20 PoR points per year of inactivity, recommended 16, and suggested a lambda conversion without a complete common recurrence. It is retained only as archive interpretation, not as an active calculation or reproducibility guarantee. The active v3 schema rejects `standing_decay_rate`; migration MUST NOT infer that an old profile authorizes scoped readiness or reuse it as a fallback.

## Envelope thresholds

Declared thresholds MUST be finite JSON numbers satisfying `0 <= m_veto < m_allow` (`ktp-core` §6.6). Both fields are required when the section is present; booleans, non-numeric values, nonfinite values, missing fields, and additional fields are invalid. The schema enforces the per-field lower bounds and shape; `check-declarations.py` also checks finiteness and cross-field ordering. There is no upper bound: a conservative profile may prevent stable operation by requiring an unattainable margin.

Omitting the section retains the existing `M_veto = M_allow = 0` default, including its veto at zero margin. An explicit null or equal pair is invalid and MUST NOT select that default. These requirements preserve the existing equality behavior.

Thresholds only impose further restrictions after the input and independent capacity checks. A request with `A > E`, or with zero capacity, MUST be vetoed before division or threshold evaluation. A profile or a change in supervision MUST NOT override that veto. A revised candidate action requires a new evaluation with its actual parameters.

## Emergency policy binding

`emergency_policy`, when declared, MUST contain exactly `policy_id`, positive integer `version`, and `digest` in `sha256:<64 lowercase hexadecimal digits>` or `sha384:<96 lowercase hexadecimal digits>` form. Level 3 deployments MUST use SHA-384; the trusted deployment's cryptographic profile determines the requirement, not the candidate declaration. `policy_id` is a nonempty literal without whitespace or wildcard/glob/template delimiters. The digest binds the exact UTF-8 policy bytes. Omission disables emergency capability; explicit null is invalid. This reference MUST NOT be accepted as proof of approval or as an activation.

The referenced declaration must satisfy [`emergency-policy.json`](../schemas/emergency-policy.json) and `scripts/check-emergency-policy.py`. Installation, signatures, incumbent authority, activation, suspension/revocation, and runtime enforcement MUST independently satisfy [`emergency-capability.md`](emergency-capability.md). Creating or changing this binding, including selecting an older policy or a different policy ID, is governed by that protected amendment process. Merely incrementing the deployment profile version does not authorize the change.

## Oracle consensus declaration

`oracle_consensus` binds the deployment to the normative [Oracle consensus contract](oracle-consensus.md). It MUST be present for a Byzantine Oracle Mesh agreement claim. Its absence permits no such claim and does not silently select a majority quorum. It does not change Basic single-Oracle operation into Byzantine consensus.

The object contains exactly `protocol_id`, `protocol_version`, `protocol_spec_digest`, `membership_epoch`, `members`, `fault_tolerance`, and `quorum`. The protocol identifier and version are nonempty literal strings without whitespace or wildcard/glob/template delimiters. The digest uses `sha256:<64 lowercase hexadecimal digits>` or `sha384:<96 lowercase hexadecimal digits>` and binds the exact reviewed protocol specification bytes, including its wire format, safety arguments, recovery/reconfiguration rules, and implementation/review references. Level 3 requires SHA-384 under the trusted cryptographic profile; a declaration cannot select a weaker requirement. The positive integer membership epoch identifies the authenticated roster; changing the roster requires a new epoch and the companion's committed transition.

Each member contains exactly `node_id`, `key_id`, and `control_domain`, all nonempty literal strings under the same identifier rule. Each of these fields MUST be unique across the roster. Distinct labels are necessary declaration checks, not evidence that the deployed nodes, keys, or administrators are independent. The fault assessment MUST count every member an attacker can control through a shared administrator, key store, host, or other common dependency.

Let `N` be the roster length, `f = fault_tolerance`, and `q = quorum`. The declaration requires integer controls, with booleans and floating-point representations rejected by the checker, and:

```text
f >= 1
N >= 3*f + 1
floor((N + f) / 2) + 1 <= q <= N - f
```

The default five-member mesh declares `f = 1` and `q = 4`. A seven-member mesh tolerating two Byzantine members requires at least five votes. These are decision quorums; they do not replace a key's separate threshold-signature setting. Existing stricter operation approvals remain required. A protocol may impose stronger requirements; arithmetic validity does not establish that the named protocol supports this configuration.

Every member MUST verify the authenticated configuration and evidence before counting votes. Timeout, reachability, emergency activation, profile version changes, and edits to this declaration do not authorize a new committee or lower threshold. Installation and modification require the companion's authenticated bootstrap or committed transition; a candidate declaration cannot appoint its own voters.

`scripts/check-declarations.py` checks the declaration's shape, distinct labels, and integer inequalities. `scripts/test-oracle-consensus.py` exercises those checks and bounded quorum-set counterexamples. Neither checks cryptographic signatures, actual custody independence, durable storage, safe leader replacement, or a running consensus engine. Runtime claims require the companion's separate evidence and [adversarial conformance cases](conformance/oracle-consensus-v1.json).

## The decision record's undefined-inputs field

`ktp-core` §6.7 requires that *the undefined state MUST be recorded on the decision record*, and #105 requires the recorded state to distinguish a silence-veto from a framework-veto in audit. Until now the obligation had no named field. This document defines it:

```json
"undefined_inputs": [
  { "input": "world.security.open_incident_count",
    "layer": "signal",
    "state": "stale" }
]
```

- `input` — the identifier of what was undefined: a feed `id`, a catalogue signal ID, a Risk Factor key, or a sovereignty framework identifier;
- `layer` — `feed` | `signal` | `term` | `query`, the three layers of `ktp-core` §5.2 plus the sovereignty query of `ktp-sensors` §4.3;
- `state` — `absent` | `unanswered` | `stale` | `undefined`, the four conditions `ktp-core` §6.7 enumerates.

The field MUST appear on any decision record where an undefined input resolved the outcome toward the more restrictive alternative. Schema carriage on the decision-record artifacts (`trust-proof.json`, the audit record) rides the #71/#83 schema gate; this definition is that gate's cargo.

## Conformance

`scripts/check-declarations.py --profile <file>` validates:

1. the instance against `deployment-profile.json` (shape);
2. every declared signal ID against `catalog/*.json` (existence);
3. every aggregation against the alias sets in `catalog/index.json` (at most one member of any set per aggregation, and populated sets declared under `aliases`);
4. every aggregated `zero_one: "synthetic"` signal against `normalization` (entry present);
5. finite `envelope_thresholds` numbers satisfying `0 <= m_veto < m_allow` where declared; omission alone selects the existing default;
6. six finite factor weights in `(0, 1]`, with an exact parsed-decimal total of 1;
7. the shape of an optional `emergency_policy` reference; omission disables that capability;
8. the shape, distinct member labels, integer fault budget, and quorum bounds of an `oracle_consensus` declaration; omission provides no Byzantine Mesh agreement claim;
9. the required `standing_policy` reference to `history-with-scoped-readiness-v1` and rejection of the obsolete `standing_decay_rate` declaration in active v3 profiles.

JSON Schema enforces the factor shapes and individual weight bounds. The unit-sum and finite-number checks require the declaration checker as well. `scripts/test-risk-factor-weights.py` exercises both validators, including the published weight profiles and invalid totals.

A deployment that omits an optional section takes that section's stated default. A deployment that omits a required declaration is not a partial conformer — it is **unassessable** (#94's rule: declare your instance, or there is nothing to assess).

## Owed to this surface, not yet in it

Named so it is discovered here rather than re-derived. Each lands in this document when its owner executes; none is ruled by this document.

| owed declaration | owner |
|---|---|
| the zone R budget — *a published tier names a zone it is reachable in at its declared R budget; the R budget is declared, not published* | #109 M2/M3's edit list |
| the retention floor for the measurement-envelope log | #72 *What this opens* — a number nobody has chosen |
| Trust Proof carriage of exposure, capacity, terminator, hop bound, applicable ceilings, and instrument status | the #71/#83 schema gate (wave 6); the former decay-rate carriage is superseded by the separate readiness decision |
| the reference label-set identifier and whether it becomes a registry | #68 *What this opens*, interacts with OTCS |
| the episode identity tuple's declaration surface | #81 *Opens* (v2.1 mechanism ticket) |
| the existing Silent Veto's wire visibility (`TRUST_INSUFFICIENT` ships wire-visible; `KINETIC_CAPACITY_EXCEEDED` registered evidence-only) | flagged to #108 by #82 — a ruling owed, not a field |

## Human policy binding

An active deployment accepting human actions or human-origin delegation MUST
install `human_policy` with exactly `mode: "operation-eligibility-v1"`,
`profile_id`, positive safe integer `version`, and the JCS digest of the complete
approved [human profile](../schemas/human-eligibility-profile.json). The trusted
conformance level determines the digest strength. Omission disables human
eligibility; it MUST NOT select legacy human scores or exempt a software executor
from readiness. Version floors and current evidence state must be independently
authenticated and durable under [human-eligibility.md](human-eligibility.md).

The deployment digest binds exact installed bytes, so installing or changing the
human binding requires a new deployment version and dependent evidence refresh.
The human profile contains the governing authority, review route, retention
policy, issuer registry, scoped grants and approved qualification criteria.
Profile approval does not establish current individual eligibility. The focused
declaration checker validates this binding's shape; full runtime installation,
policy legitimacy, current qualification, authorization adapter and execution
checks remain separate obligations.
