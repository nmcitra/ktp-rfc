# Migrating from v1.0.1 to v2.0.0

For implementers pinned to `v1.0.1-provenance`.

v2.0.0 is a MAJOR release under [`VERSIONING.md`](VERSIONING.md). The break is
deliberate and **there is no dual-accept period**: an implementation reads v1
or it reads v2. No rename or negotiation machinery exists anywhere in the set,
so there is nothing to switch on.

Your v1.0.1 pin keeps working. A published tag is never moved, so the text you
built against stays reachable at that tag permanently, and a normative
reference that names v1.0.1 in its title stays accurate for the version it
pins — do not rewrite such a title to match v2 vocabulary, because that
misquotes the tag.

This document has three parts:

1. **[Wire-format breaks](#1-wire-format-breaks)** — a token on the wire
   changes. Your code fails, or worse, silently accepts the wrong thing.
2. **[Behavior breaks](#2-behavior-breaks)** — the shapes are unchanged and the
   numbers are not. Your code runs and computes a different answer.
3. **[Prose changes](#3-prose-changes)** — nothing to implement, but the
   document you cite may have moved or been renamed.

Full detail on what forced each change is in [`CHANGELOG.md`](CHANGELOG.md).
Two defects in v1.0.x that you should treat as live until you migrate are in
[`SECURITY-NOTES.md`](SECURITY-NOTES.md).

---

## 1. Wire-format breaks

### 1.1 The lineage enum

Three values change. The numeric protobuf values are unchanged, so only the
symbol names move.

| v1.0.1 | v2.0.0 |
|---|---|
| `tethered` | `sponsored` |
| `divergent` | `independent` |
| `persistent` | `guarantor` |

This reaches further than a field rename. It affects:

- the `lineage` field in the Trust Proof, the transaction record, and the
  sponsorship bond;
- **agent identifier strings**, which embed the stage:
  `agent:tethered:<sponsor_id>:<agent_name>:<unique_id>` becomes
  `agent:sponsored:...`, and likewise for the other two;
- protobuf `LineageType` **member names**;
- any parser, log filter, dashboard facet, or test fixture matching on the v1
  strings.

An agent identifier re-mints on every generation advance, so existing
identifiers age out rather than needing rewriting. Persisted historical records
keep the v1 strings and should be read as v1 records.

### 1.2 The Trust Tier enum

`God Mode` is renamed `Admin Mode`.

| Surface | v1.0.1 | v2.0.0 |
|---|---|---|
| OpenAPI enum value | `god_mode` | `admin` |
| protobuf member name | `TRUST_TIER_GOD` | `TRUST_TIER_ADMIN` |
| protobuf numeric value | `5` | `5` — unchanged |

The one surviving use of the old phrase is `ktp-governance`'s quoted "God Mode"
antipattern, which is a quotation and not a tier name.

### 1.3 The environmental object: letter keys are gone

The object formerly keyed `context_tensor`, with single-letter keys inside it,
is now `risk_factors`, keyed by name. **The JSON key is the name.**

| v1 key | v1 meaning | v2.0.0 key |
|---|---|---|
| `m` | Mass | `evidence_density` |
| `p` | Momentum | `trust_trend` |
| `h` | Heat | `adversarial_pressure` |
| `t` | Time | `moment_criticality` |
| `i` | Inertia | `update_resistance` |
| `o` | Observer | `attestation_coverage` |
| `s` | Soul | `soul`, and it leaves this object — see 1.4 |

Two traps here:

- **The stray `v`.** `ktp-identity`'s v1 machine-readable examples keyed one
  entry `"v"`, a letter the six-letter scheme never defined. It stood in
  Momentum's slot. If your implementation accepted `"v"`, it was reading
  Momentum whether or not the specification said so; map it to `trust_trend`.
- **`additionalProperties: false`.** `risk-factors.json` rejects unknown keys,
  so a v1 payload does not validate — it fails loudly rather than being
  partially read. That is intended.

### 1.4 Soul leaves the weighted vector

`R` is aggregated over **six** weighted inputs. The Soul veto is evaluated
*before* aggregation and is not a term in it — six-plus-veto, not seven.

- `risk-factors.json` requires six keys, not seven.
- `soul-constraint.json` renames `s` to `soul` and keeps it as
  `integer enum [0, 1]`.
- If you were weighting Soul into `R`, stop. A weighted Soul lets a
  sufficiently good score outvote a sovereignty constraint, which is the one
  outcome a veto exists to prevent.

### 1.5 `sensor_health`

v1 published a flat object with letter-prefixed keys and a
`degraded_dimensions` array:

```json
"sensor_health": {
  "m_feeds_active": 4, "m_feeds_total": 5,
  "p_feeds_active": 3, "p_feeds_total": 3,
  "degraded_dimensions": ["m"]
}
```

v2 nests one health object per input, keyed by the input's name, and renames
the array:

```json
"sensor_health": {
  "evidence_density": { "feeds_active": 4, "feeds_total": 5 },
  "trust_trend":      { "feeds_active": 3, "feeds_total": 3 },
  "degraded_inputs":  ["evidence_density"]
}
```

This was the last place a letter appeared on the wire.

### 1.6 The Trust Proof gains four required claims

| Claim | What it carries |
|---|---|
| `peer_share` | the peer-validation share this deployment declares, in points; `0` where peer validation is not implemented |
| `applicable_ceilings` | every ceiling that applied to this evaluation |
| `advancement_floor` | the deployment's declared per-generation Resilience floor |
| `root_instrument` | the accountability instrument: status, end time, declared exposure, anchored capacity, chain terminator, chain length |

A v2 relying party cannot evaluate `E_base` without these, which is why they
are required rather than optional. In particular, **you MUST NOT compare
`E_base` magnitudes across deployments that declare different `peer_share`
values** — the shares are a declaration, not a constant.

### 1.7 The schema `$id` base moves

| | |
|---|---|
| v1.0.1 | `https://ktp.example.org/schemas/<name>.json` |
| v2.0.0 | `https://kinetic-trust-protocol.net/specs/schemas/v2/<name>.json` |

The v2 base is a versioned path on a domain the project owns and it serves
`application/json`, so the schemas resolve to themselves. If you cached or
vendored schemas by `$id`, repoint. Two of the v1 `$id`s named files that never
existed.

The published set at the new base:

| Schema | Status in v2.0.0 |
|---|---|
| `risk-factors.json` | **new** — replaces `context-tensor.json`, which is deleted |
| `trust-proof.json` | four new required claims, renamed lineage and tier enums |
| `soul-constraint.json` | `s` → `soul` |
| `sensor-config.json` | see 1.8 |
| `transaction-record.json` | **promoted** from a document appendix |
| `sponsorship-bond.json` | **promoted** from a document appendix |
| `deployment-profile.json` | **new** — see 1.9 |

The transaction record's inline letter-keyed environmental object was a
hand-copy that had drifted from the published file in four ways. It is replaced
by a `$ref`, and the field renames to `risk_factors`.

Where an Internet-Draft-formatted specification previously inlined a schema in an appendix, the
appendix now carries the canonical file's location plus a SHA-256 of its
contents. Validate against the file, not against the appendix.

### 1.8 `sensor-config.json`

Three constraints tighten. Two of them correct defects that are live in v1.0.x
— see SN-001 and SN-002 in [`SECURITY-NOTES.md`](SECURITY-NOTES.md).

- **`default_on_failure`** is floored at `0.5`, defaults to `1`, is REQUIRED on
  every dimension that is not veto-aggregated, and is pinned to `const: 1`
  where aggregation is `any_veto`. A v1 configuration setting it to `0`, or
  omitting it, does not validate. It should not have validated in v1 either:
  `0` measures perfect conditions, so a dimension defaulting to `0` on failure
  meant **turning sensors off raised the trust score**.
- **The Stale Behavior column is gone.** A feed whose most recent observation
  has passed its `stale_threshold_ms` is *unavailable*, and the §6.2 failure
  ladder governs it. Do not hold the last known value: whoever can freeze a
  feed also chooses the value it freezes at.
- **`refresh_interval_ms` and `stale_threshold_ms` now admit `0`** and the
  schema says what it means — queried on demand. In v1 the minimums were 100
  and 1000, which is why the schema's own second example never validated
  against it.

### 1.9 New: the deployment profile

`deployment-profile.json` is the surface on which a deployment declares the
parameters the set now requires it to declare. Required: `profile_id`,
`version`, `risk_factors`, `soul_veto`, `peer_share`, `external_root`,
`standing_decay_rate`.

If you ship a KTP deployment, you now publish one of these. If you consume
another deployment's Trust Proofs, its profile is how you interpret them.

### 1.10 Statistics over an empty window

`sample_count` is REQUIRED on an aggregation, and an aggregation over a window
that defines no samples **omits the statistic** rather than reporting one. Do
not emit `0` for a mean over an empty window: an empty denominator is unknown,
not zero.

---

## 2. Behavior breaks

Nothing here changes a field name. Everything here changes a number your code
produces or a branch it takes.

### 2.1 Trust Tier thresholds

| Tier | v1.0.1 | v2.0.0 |
|---|---|---|
| Admin Mode (was God Mode) | `E_trust >= 95` | `E_trust >= 85` |
| Operator Mode | `E_trust >= 85` | `E_trust >= 72` |
| Analyst Mode | `E_trust >= 70` | `E_trust >= 58` |
| Observer Mode | `E_trust >= 50` | `E_trust >= 22` |
| Hibernation | `E_trust < 50` | `E_trust < 22` |

Two values move with them:

- **Hibernation exit**: `E_trust >= 55` becomes `E_trust >= 24`.
- **Admin stable-conditions requirement**: `R < 0.05` becomes `R < 0.10`.

The **generation ceilings are unchanged** — 25 / 35 / 45 / 55 / 65 / 75 / 85
for generations 0 through 6, 100 for generation 7 and above. One table moved,
not two.

If you hardcoded the v1 thresholds, note what they meant: generations 0 through
2 were capped below the lowest threshold, so an agent was in Hibernation by
lineage rather than by environment, and the top tier was unreachable in every
zone class at the specification's own calm worked example.

### 2.2 Admin Mode is not offered everywhere

- **Admin Mode requires a zone Mass Ceiling of at least 95.** A zone with a
  lower ceiling cannot deliver the tier at any generation. Plan capability
  against the zone, not against the tier table.
- **A zone implementing `ktp-enforce` §9.5 progressive trust taxation does not
  offer Admin Mode at all.** Its taxed curve saturates at 87, which under any
  live environmental deflation sits below 85. Such a zone's highest attainable
  tier is Operator Mode, and that is the intended trade rather than an
  accident.

### 2.3 `E_base` is a hundred-point allocation, not a weighted sum

**This is the largest behavior break in the release, and it changes every
`E_base` your implementation computes.**

In v1, `ktp-identity` §5.3 stated Proof of Resilience as a *contribution*
capped at 70, and `ktp-core` §5.1 then multiplied that contribution by a 70%
weight. The same 70, spent twice: a maxed-out Proof of Resilience was worth 49,
and the External Root's 30 was worth 9.

In v2, the weights are gone. Each term contributes at most its declared share,
and the shares MUST sum to 100:

| Component | Share |
|---|---|
| Proof of Resilience | 70 |
| External Root | 30 |
| Peer Signals | declared, and taken proportionally from the other two |

`E_base` is then the minimum of the raw allocation and every applicable
ceiling. If you published a rate, a stake, or a decay parameter calibrated
against the weighted reading, it is wrong by a constant factor — recalibrate
against the allocation.

### 2.4 Ceilings

- Ceilings compose under `min()`. Each states an independent reason to withhold
  trust, and reasons to withhold do not average.
- The **Identity Assurance Level ceilings (40 / 80 / 95) are now in the
  table**. They existed in v1's `ktp-identity` §7.1 and the composition never
  consulted them.
- **Every ceiling applicable to an evaluation MUST be declared** in the Trust
  Proof's `applicable_ceilings`.
- **No grant lifts a ceiling.** Standing issued by fiat — a genesis grant, an
  inheritance bonus — is bounded by the same minimum as standing that was
  earned. Concretely, `ktp-zones` §9.3.6's genesis grant of `E_base` 50 is now
  the generation-0 ceiling of **25**. If you bootstrap zones, this changes what
  a first agent can do: at a ceiling of 25 it clears the Observer floor of 22
  only while `R` stays below 0.12.

### 2.5 The per-tier `Max A` matrix is deleted

v1 published a Capability Matrix mapping each tier to a maximum action risk
(God 100, Operator 85, Analyst 60, Observer 30, Hibernation 5). **It is gone.**

A tier permits action *classes*. `A <= E_trust` is the numeric bound, and it is
the only one. Delete the second check; it was the mechanism that generated the
drift between the two ladders.

A per-phase Trust Tier cap is likewise no longer stated. A phase bounds
`E_base` through the generation ceiling, and the environmental deflator sits
between that and any tier.

### 2.6 Lineage advancement: the 30-day gate is gone

v1 ran two advancement gate families over one lineage, and they disagreed. An
agent at Resilience Score 1,001 on day 31 was Divergent under §8.1 and Tethered
under §8.4.

**The §8.1 and §8.2 `Duration:` gates are deleted.** Delete these conditions
from your implementation:

- *"Until agent accumulates Resilience Score > 1000 AND has operated for > 30
  days"*
- *"Until agent accumulates Resilience Score > 10,000 AND has operated for >
  180 days AND intrinsic E_base > 60"*

§8.4 is the sole advancement rule, and **phase derives from generation**:

| Generations | Phase |
|---|---|
| 0–2 | `sponsored` |
| 3–6 | `independent` |
| 7 and above | `guarantor` |

No agent is in two phases at once.

Generation advances on three conditions, all of which MUST hold:

1. **Time** — a seven-step widening clock replaces the flat 60 days per step:

   | Step | Minimum elapsed | |
   |---|---|---|
   | 0 → 1 | 90 days | |
   | 1 → 2 | 90 days | |
   | 2 → 3 | 365 days | tether release |
   | 3 → 4 | 180 days | |
   | 4 → 5 | 180 days | |
   | 5 → 6 | 180 days | |
   | 6 → 7 | 2,555 days | terminal ceiling |
   | **Total** | **3,640 days** | |

2. **Resilience** — the per-generation quota is now a **declared floor on
   evidence, not the gate**. Time is the primary gate. A deployment MUST
   declare the floor and carry it in the Trust Proof as `advancement_floor`; a
   deployment whose environment produces no attestable friction declares zero,
   and a relying party can then see that this lineage advanced on time alone.
   The published default is recorded as owed work — deriving it needs the
   evidence curve, and a default nobody can derive is not checkable.

3. **Survival** — no CRITICAL violations in the current generation.

### 2.7 A sponsorship bond closes without releasing

v1 released the sponsor's bond on entry to stage 2. **It no longer releases at
any point.**

- The taper holds at a permanent floor of `0.1^depth × stake_amount`. The
  retained share is named **Ancestral Liability**.
- Its collateral **matches the residual permanently**, so the anti-botnet bound
  is cumulative as well as concurrent. An `E_base` 87 sponsor at 10% stake
  exhausts after 100 matured descendants, however well each of them behaved.
- A bond's declared `duration` **binds staked capital only**, not the
  liability. Without this, a one-day bond defeated the taper at creation.
- Ancestral Liability discharges **only** on a for-cause claim surviving
  adjudication. Decommissioning passes the residual **up** the lineage at its
  current value.

The mechanism invents no constant. `0.1^depth` was already the published decay
on Ancestral *Authority*, the credit side. Credit and liability now travel the
same lineage at the same decay.

Two v1 defects go with it: the published stake taper returned **negative** above
`intrinsic_E_base` 80, crediting a sponsor for a descendant's standing; and the
stage-3 threshold was stated twice, twenty points apart, in adjacent
subsections. The threshold is `intrinsic_E_base > 80`.

Note also that the bond halving and the stake taper are **not inputs to the
`E_base` composition**. They are bond accounting. If your implementation fed
either into `E_base`, remove it.

### 2.8 Standing decays

`E_base` no longer only ratchets up. A deployment MUST declare
`standing_decay_rate` in **points of Proof of Resilience lost per year of
inactivity**, within `[2, 20]`, RECOMMENDED `16`. Evaluation is lazy: the
declared rate plus the record's timestamps reproduce any value
deterministically, so there is no sweep to run.

### 2.9 Unobserved means maximum stress, everywhere

- Every weighted Risk Factor term is a **stress term** in [0, 1]. 1 is maximum
  stress, 0 is its absence, whatever the term is named. A term whose name reads
  as a desirable quantity is still a stress term.
- **A deployment MUST NOT substitute 0 for an unobserved term.** The
  conservative substitute is **1.0**. Zero measures perfect conditions, not
  unknown ones.
- Unobservability is checked at **three layers — feed, signal, term — and the
  rule applies at each**. They do not collapse into one another: a signal can
  be unavailable while every feed populating it is healthy. A rate whose set of
  eligible events is empty is unknown, not zero.
- **Undefined fails closed as a class.** An unknown environment reads as low
  capacity, not high. `ktp-recovery`'s "when in doubt, deny" is amended as too
  strong; silence and absence do not separate.
- **An unanswered sovereignty query is not clearance.** `ktp-federation` §4.3
  now has a branch for silence.

### 2.10 `moment_criticality` is supplied, not measured

Five of the six weighted inputs are aggregations over the Context Signals
catalogue. `moment_criticality` is **supplied by the action request**. The
asymmetry is stated at the input's definition and recorded as limit L14. If you
built it as a catalogue aggregation, it is not one.

### 2.11 Normative content enters through a fixed interface

Normative judgment — *ought this happen* — enters the calculation as a **veto**,
a **supplied input**, or a **gate**, and **MUST NOT rewrite the aggregation**.
If you implemented a norm by adjusting weights, move it to one of the three.

---

## 3. Prose changes

No code changes here, but a citation or a link may have moved.

### 3.1 Three specifications are renamed

| v1.0.1 | v2.0.0 |
|---|---|
| `ktp-gravity` | `ktp-attenuation` |
| `ktp-tensors` | `ktp-signals` |
| `ktp-signal` | `ktp-information` |

Each was named for a retired object. No published documentation URL moves — the
summary layer in `rfcs/` is unchanged in location.

### 3.2 Retired vocabulary

"Context Tensor," "Digital Physics," "physics-derived," and the physics claim
itself are out of the normative set. Nothing in the set transforms tensorially.
The catalogue is **Context Signals**; the scoring layer is the **Risk
Factors**.

If your document cites KTP normatively and uses the retired vocabulary in its
own prose, that prose is now describing something the specification does not
call by that name. A normative *reference title* naming v1.0.1 is a different
case and is correct as written — see the note at the top of this document.

### 3.3 The Context Signals catalogue grew

1,627 signals across six domains becomes **1,644 across seven**. The new domain
is **Meta** — 17 signals measuring the quality of the measurement itself, which
previously had no home and was being read out of the Time domain.

Two rules arrive with it:

- **Scope**: the catalogue measures the environment's *present*. The agent's
  trajectory lives in `ktp-identity`.
- **Declared derivatives**: a derivative MUST declare its base signal, its
  form, and the window it is computed over. A derivative is undefined without
  its window, is marked as derived, and is never counted as a new observation
  of the environment.

### 3.4 `ktp-core` section 10: Limits of This Specification

Fourteen entries, L1 through L14, ordered hardest to softest. These are
boundaries fixed in advance rather than answers invented late; several of them
name obligations the specification declares and does not yet mechanize.
Sections 10 through 12 renumber to 11 through 13.

If you are profiling KTP or citing it normatively, read L11 (there are two
SHOULD rails, and only one of them is this specification's) and L14
(`moment_criticality` is externally supplied) first — those two are the ones
most likely to sit under a downstream document's own claims.

### 3.5 Requirements language

Seven documents acquire the BCP 14 requirements-language paragraph:
`ktp-conformance`, `ktp-human`, `ktp-privacy`, `ktp-problems`, `ktp-recovery`,
`ktp-sensors`, `ktp-threat-model`. Their capitalized keywords are keywords now;
in v1 they were capitalized English words.

**`ktp-migration` is informative in full.** It states no normative requirement
and uses no BCP 14 keyword, and where a value in it differs from the normative
set, the normative set governs. Its §5.1.1 role table also loses its Trust Tier
column: no static column can name the tier a given `E_base` produces, because
the deflator is neither in the table nor constant.

### 3.6 The prudence rail has a name

`ktp-enforce`'s graduated mechanisms — throttling, downgrading, deferral,
promotion hysteresis, the risk floor, deautomation, the §9.5 taxation trade —
are one rail answering one amoral question, and the specification now names it.
It stays amoral only while its parameters are declared. An undeclared prudence
constant is a smuggled norm.

### 3.7 Where the text lives

`rfc-src/` is now the single source for all 27 specifications, authored as
kramdown-rfc markdown. Only five ship a `.txt` — `ktp-core`, `ktp-identity`,
`ktp-problems`, `ktp-enforce`, `ktp-conformance` — because generating one
asserts Internet-Draft status, which the other 22 disclaim. The 22 render as
markdown. The summary layer in `rfcs/` is unchanged and **no published URL
moves**.
