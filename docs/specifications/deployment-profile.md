# The Deployment Profile

**The declaration surface for a KTP deployment.** Status: v0.1 (interface + conformance). Canonical KTP specification.

The specification series keeps requiring declarations rather than publishing constants — the peer-signal share, the sponsorship chain's terminator and hop bound, the normalization function behind every synthetic score, which member of an alias set a deployment populates, the signals behind each Risk Factor. Each of those obligations was ruled separately, and until this document none of them had a place to be discharged: **a framework that requires declarations and provides no declaration site has an obligation nobody can discharge** (nmcitra/ktp-rfc#108, consolidating #101 and #106).

This document is that site. It defines one object — the **deployment profile** — carrying every deployment-level declaration the series requires, so that the alias declarations, the Risk Factor bridge, and the feed mapping are one schema rather than three that have to agree. The machine form is `docs/schemas/deployment-profile.json`; `scripts/check-declarations.py` validates a profile instance against both the schema and the catalogue.

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
| `standing_decay_rate` | the standing decay rate, in PoR points per year of inactivity | yes |
| `envelope_thresholds` | the supervision thresholds `m_veto < m_allow` | optional; absent = v1 binary behavior |

## Risk Factors — the bridge

`[KTP-CORE]`'s bridge law (D2): **each Risk Factor is a named aggregation over a declared subset of Context Signals. A deployment MUST declare which signals feed which factor and by what aggregation.** The catalogue names what can be measured; the six factors are what the decision consumes; this section is the only place the two meet.

The shape is fixed by #83: **six weighted inputs to R, plus the Soul veto, which is evaluated before aggregation and is not a term in it.** The six factor keys are `evidence_density`, `trust_trend`, `adversarial_pressure`, `update_resistance`, `attestation_coverage`, `moment_criticality` — all six are required, and the schema's `required` array is exactly that list. Each factor declares:

- `signals` — Context Signal IDs from `catalog/`, the declared subset;
- `aggregation` — the named aggregation over them (method plus its parameters);
- `weight` — the factor's weight in `R = sum(w_i * s_i)`.

Constraints, all quoted from their rulings:

- *a Risk Factor aggregation MUST NOT include more than one ID from an alias set* (`catalog/index.md` §7);
- a signal that does not declare its envelope slots for its observation class MUST NOT be used in a Risk Factor aggregation (`catalog/index.md` §3–§4);
- a synthetic bare-`0-1` signal MUST have a `normalization` entry to aggregate (§6); a categorical signal MUST have a `label_sets` entry to aggregate (§5);
- every term is a stress term whatever it is named: the substitute for an unobservable term is 1.0, never 0 (`ktp-core` §5.2, per #80).

### The Soul veto

`soul_veto` declares the sovereignty frameworks queried per `[KTP-SENSORS]` §4.3. It is not a weighted term: a sufficiently good score must not be able to outvote a sovereignty constraint (#83). If ANY framework returns veto, S = 1; if ANY query is UNDETERMINED — unreachable, error, timeout, or empty — S = 1, one branch, no separation (`ktp-sensors` §4.3, per #105). Only an answering framework returns a clearance.

## Feeds — how the wire reaches the catalogue

The wire and the catalogue name different objects: `[KTP-SENSORS]` §2.2 configures **feeds**, `[KTP-TRANSPORT]` §9.2/§9.3 carry feed readings, and the catalogue names 1,627 **signals**. One feed can populate many signals; one signal can be fed by many feeds. Until the correspondence is declared, the three-layer missing-data rule (`ktp-core` §5.2: feed · signal · term, which do not collapse) is written across a mapping that does not exist — *a signal can be unavailable while every feed populating it is healthy*, and nothing could compute which (#106, opened by #60 and #72).

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

## Standing decay

`standing_decay_rate` declares #59's rate: **PoR points lost per year of inactivity**, within the normative range **[2, 20]**, RECOMMENDED **16**. The mechanism derives `λ = 10^(−D/3650))` and is specified in `[KTP-IDENTITY]` §5.3; evaluation is lazy, so the declared rate plus the record's timestamps reproduce any value deterministically.

## Envelope thresholds

*A deployment MUST declare its profile thresholds `M_veto < M_allow`; a deployment that declares none evaluates with `M_veto = M_allow = 0`, which reproduces the binary v1 behavior* (`ktp-core` §6.6, per #82). The section is optional for exactly that reason; when present, both fields are required and `m_veto < m_allow` is a conformance check.

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
5. `envelope_thresholds.m_veto < m_allow` where declared.

A deployment that omits an optional section takes that section's stated default. A deployment that omits a required declaration is not a partial conformer — it is **unassessable** (#94's rule: declare your instance, or there is nothing to assess).

## Owed to this surface, not yet in it

Named so it is discovered here rather than re-derived. Each lands in this document when its owner executes; none is ruled by this document.

| owed declaration | owner |
|---|---|
| the zone R budget — *a published tier names a zone it is reachable in at its declared R budget; the R budget is declared, not published* | #109 M2/M3's edit list |
| the retention floor for the measurement-envelope log | #72 *What this opens* — a number nobody has chosen |
| Trust Proof carriage of the declared rate, exposure, capacity, terminator, hop bound, applicable ceilings, and instrument status | the #71/#83 schema gate (wave 6) |
| the reference label-set identifier and whether it becomes a registry | #68 *What this opens*, interacts with OTCS |
| the episode identity tuple's declaration surface | #81 *Opens* (v2.1 mechanism ticket) |
| the existing Silent Veto's wire visibility (`TRUST_INSUFFICIENT` ships wire-visible; `KINETIC_CAPACITY_EXCEEDED` registered evidence-only) | flagged to #108 by #82 — a ruling owed, not a field |
