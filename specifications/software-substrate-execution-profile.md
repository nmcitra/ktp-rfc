# Software-substrate execution profile

**Status: proposal; not adopted or released.** Decision: [#124](https://github.com/nmcitra/ktp-rfc/issues/124), D-009. Release baseline: **KTP `v2.1.0`**. This optional profile declares the software substrate anticipated by the kinetic envelope. Its identifier is `software-substrate-execution`; it has no independent release number, tag or DOI. A release of the KTP set must identify the exact specification, schema and vector revisions it contains.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Scope and existing contracts

This profile fixes software demand magnitudes, capacity-reducing conditions, local evidence freshness, and a signed consumption-decision binding. Computation behind A and E remains implementation-defined. It does not prescribe a gateway, provider, identity product, network substrate, storage service or research formula. Any implementation meeting the published contract and vectors may implement it.

Existing requirements are incorporated by reference, not replaced:

| Existing contract | Released reference | What this profile adds |
|---|---|---|
| Supervision is a floor; constraints tighten only; undefined inputs resolve restrictively | [Core §6.6–§6.7](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-core.md#aggregation-algorithm) | Names local software observations and the scope/freshness under which they can restrict consumption. |
| PEP intercepts and validates each protected action; proof, Soul, tier and capacity conditions remain binding | [Enforce §3.1, §4.1 and §11.2](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-enforce.md#enforcement-flow) | Explicit enforcement destination and authority/action class, bound to the actual resolved request. |
| Substrate declaration, result interface and implementation-independent decision contract | [Kinetic envelope](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/specifications/kinetic-envelope.md) | Declares software magnitudes, capacity conditions and named vectors. |
| Ordinary proof claims and identity/session authentication | [Core §7](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-core.md#trust-proof-token), [Identity](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-identity.md), [Transport](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-transport.md) | Binds the complete proof artifact without adding claims or making the consumption decision a replacement proof. |
| Decision recording and bounded conformance claims | [Audit](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-audit.md), [Conformance](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-conformance.md) | Records the consumed signed artifact and undefined/restrictive inputs; does not infer target effects from a decision. |

The separately signed [readiness decision](../schemas/readiness-decision.json) and [operational-readiness contract](operational-readiness.md) are **unreleased precedents**, absent from `v2.1.0`. Their complete-proof/actual-request binding pattern informs this proposal. This profile does not edit that closed schema or assert its availability in the release baseline. Where an installed policy requires readiness or other prerequisites, the consumer must establish them under their actual adopted contract; this decision cannot satisfy them by itself.

Consequential-action release, queues, retries, replay, shared effect budgets, commit-time target contracts, non-invocation evidence and reconciliation belong to the separate [execution/evidence proposal #129](https://github.com/nmcitra/ktp-rfc/issues/129). This profile does not claim those semantics merely by issuing a signed decision. The reproducible KIL reference contribution is [#130](https://github.com/nmcitra/ktp-rfc/issues/130).

## Software declaration

A declaring provider MUST use the envelope's existing `ActionContext` and `KineticEnvelopeResult` contracts. The deployment MUST install an authenticated declaration before use, containing the profile identifier and digest, applicable operation classes, scale identifier, margin/supervision thresholds, magnitude scope mappings, required evidence sources and maximum ages, trusted issuers, current-state/revocation authority, and bounded safe-transition/checkpoint requirements. Candidate workloads MUST NOT select or downgrade those expectations.

### Demand magnitudes and ceilings

This profile declares three autonomy-demand magnitudes. Larger values MUST NOT decrease A when all other inputs are fixed. Each returned ceiling is a maximum over the same named magnitude, unit and exact operation scope:

| Magnitude | Unit | Required meaning |
|---|---|---|
| `effectBytes` | bytes | Maximum bytes released or modified by the requested operation, including declared expansion/encoding effects. |
| `affectedObjects` | objects | Maximum independently affected logical objects under the installed operation mapping. |
| `fanoutTargets` | targets | Maximum distinct target recipients/resources reached by that operation under the installed mapping. |

Values MUST be nonnegative safe integer tokens; booleans, fractions, negative values and unknown effect bounds are not measured zero. An operation MUST declare all three bounds, including a justified zero where applicable. The installed mapping MUST identify what constitutes an object and target and how aliases, indirect effects and expansion are bounded. If an actual effect bound or its enforcement cannot be established, the original operation MUST NOT be authorized. A separately scoped bounded candidate may be evaluated afresh.

The output MUST name this profile and include exactly one ceiling for each declared magnitude, no additional or duplicate magnitudes. Every ceiling MUST be a nonnegative safe integer no greater than the corresponding requested bound or any already applicable ceiling. A tightening that changes the operation's actual scope or parameters requires evaluation and binding of that revised candidate; an enforcer cannot forward the original unbounded operation by attaching a lower number.

These are per-operation magnitudes. They are not a global budget, a Trust Score, a storage topology or a promise that distinct requests share limits. Aggregate reservation and reconciliation semantics remain #129's separate decision.

### Capacity-reducing conditions

E MUST NOT increase as any declared condition worsens, with other inputs fixed:

| Condition | Unit/domain | Worsening direction and source |
|---|---|---|
| `resourcePressure` | finite number, 0 through 1 | Increasing pressure on the declared target/enforcement resource, from an authenticated scoped observation. |
| `controlLatencyMs` | nonnegative safe integer milliseconds | Increasing observed detection-to-enforcement delay on the declared control path; declare measurement endpoints and uncertainty. |
| `irreversibility` | finite number, 0 through 1 | Increasing inability to reverse the declared effect, from an installed target/operation assessment. |
| `novelty` | finite number, 0 through 1 | Increasing departure from the declared validated operation/environment domain. An undeclared domain is unknown, not zero novelty. |

All conditions are required. Missing, unauthenticated or stale observations invoke the envelope/Core undefined-input rules. A declared conservative estimate retains `capacityKnown = false` and at least the existing assisted floor, preserving any higher floor or veto. If no usable numeric pair or required authorization prerequisite remains, the original operation is withheld. A and E MUST use the same installed scale; the consumer MUST NOT mix quantities from different scale declarations. No computation formula is specified here.

## Local evidence and freshness

Local evidence may restrict otherwise current authoritative state. It MUST NOT create standing, replenish authority, lower supervision, raise a ceiling, clear Soul or another veto, satisfy a missing prerequisite, or extend an ordinary proof. The profile recognizes these evidence classes:

| Class | Required attributable source/scope | Consumption rule |
|---|---|---|
| `resource_pressure` | Installed observer; exact resource/control-path mapping | Worsening pressure can only narrow the result. |
| `control_latency` | Installed timing observer; declared control-path endpoints | Excess delay or unavailable measurement restricts the dependent operation. |
| `operation_assessment` | Authorized assessment; exact operation/environment revision | Required irreversibility and novelty observations; a revision or unknown domain cannot inherit an older safe assessment. |
| `invalidation` | Installed authority; actor/class/resource and current epoch | Known revocation, changed binding or unresolved restriction blocks dependent use. |

An observation record MUST contain its class, source identifier, authenticated scope, sequence/epoch, underlying observation time, maximum age, value with declared units and evidence digest. The installed declaration chooses the expected source, scope and positive bounded maximum age; the candidate observation cannot choose its own trust or freshness. The consumer MUST establish observation authenticity, source health, trusted current time and the declared scope before consumption. A signature or matching digest string alone does not establish measurement quality or current state. `operation_assessment` contains both irreversibility and novelty for the same declared revision; invalidation status is verified separately even when other numeric conditions are known.

An observation is fresh only while trusted time is at or after its underlying observation time and strictly before its declared freshness deadline. Exact equality at the deadline is stale. Re-signing, delivery, cache refill, proof refresh and restart MUST NOT reset the observation time. Future observations, gaps or rollback in a required sequence/epoch, inaccessible current status and inconsistent sources are undefined; their state MUST be recorded and MUST NOT resolve toward permission. Event-only invalidation sources require an authenticated current-status/health mechanism; silence is not a fresh no-revocation observation.

The effective decision MUST preserve all already applicable restrictions. When a restriction is unresolved, expiration of its source observation or arrival of a fresh ordinary proof MUST NOT erase it. Resolution requires a separately authenticated, current decision by the installed authority that addresses the restriction and its cause; it never overrides an independent veto or grants missing permission. Current epochs and unresolved restrictions MUST survive the declared restart/failover/restoration boundary. A consumer unable to establish that continuity MUST withhold dependent use. This is a required state contract, not a mandated new service or datastore.

Authoritative proof refresh and local per-action consumption are separate clocks. Revalidation is required at use and at declared checkpoints during continuing operations. Neither clock alone establishes a sub-second deadline or deployment qualification.

## Signed consumption decision

KIL's research notation `Q_i,c` identifies the actor/class consumption state motivating this contract. It is recorded here as a **separately signed decision bound to existing artifacts**, not a new Trust Proof extension, an independent permission token, or an implementation-local opaque authority. The experimental `kil.q-state.v0` format is not relabeled as a conforming ordinary proof or adopted schema.

The proposed [consumption-decision schema](../schemas/software-substrate-decision.json) fixes the machine shape. Its request binding comprises:

- authenticated actor and actual executing workload;
- exact authority/action class, operation and resource;
- exact enforcement destination, including the resolved service/tenant/route identity under the installed mapping;
- resolved parameters digest and identity/session binding digest;
- installed execution-profile and policy digests.

The enforcer MUST derive and authenticate these values from the actual invocation and installed expectations, not accept a candidate's matching strings. Destination matching is literal under an authenticated installed mapping; a URL, DNS name or address string alone does not authenticate the destination. A change to destination, class, actor, workload, session, parameters, policy or profile invalidates use of the earlier decision.

The decision binds the complete ASCII compact-JWS ordinary proof, the RFC 8785 canonical request-binding object, the complete local evidence set, the current consumption epoch, its evaluation/expiration times, authorized issuer and the exact envelope result. Complete required prerequisite artifacts are digest-bound in `prerequisite_digests`; omission is permitted only when installed policy requires none. If readiness is required, bind its complete signed decision and verify its existing contract independently. A refreshed proof requires a matching consumption decision without renewing evidence by itself.

The request and evidence digests use RFC 8785 canonical JSON. The evidence set is the complete array of required authenticated observation records in the order fixed by the installed declaration; omitted, duplicate or substituted required records are rejected. Every record's evidence digest resolves to its actual signed/source-authenticated evidence under that source's declared representation. The ordinary proof digest covers its complete unchanged ASCII serialization, including signature. A prerequisite digest covers its complete signed artifact under that artifact's specified canonical representation. The installed declaration fixes the required prerequisite order and completeness. The installed declaration selects SHA-256 or stronger, and MUST retain stronger requirements of every applicable contract; SHA-384 is required where an applicable Level 3 contract requires it. The candidate MUST NOT choose weaker verification expectations.

Every decision member except `signature` is covered by one RFC 8785 canonical signed payload. The signature is a compact JWS produced by an installed authorized issuer, with protected algorithm/key identifiers and keys satisfying the applicable adopted KTP signing contract. Reject unapproved algorithms/keys, unsigned or detached payloads, noncanonical encodings and payload/object mismatch. The issuer MUST authenticate and evaluate all required inputs before signing. The enforcer MUST verify the signature and independently recheck current bindings, epoch, validity, prerequisite status and restrictions before use. The `evidence_digest` is not usable without resolving and verifying the bound evidence set.

### Repair-path and supervision availability

The signed `result` MUST include boolean `repairPathVerified` and `supervisionAvailable` values. Before setting `repairPathVerified = true`, the issuer MUST establish from an installed, authenticated source the applicable repair path for the exact request, target revision and declared recovery boundary. The enforcer MUST recheck that establishment at use and at every declared checkpoint; a changed request, target revision or recovery boundary invalidates the earlier result. `repairPathVerified = false` withholds any repair-dependent action.

Before setting `supervisionAvailable = true`, the issuer MUST establish from an installed, authenticated source that the supervision required by the installed profile is available for the exact request, target revision and declared recovery boundary. The enforcer MUST recheck that availability at use and at every declared checkpoint; a changed request, target revision or recovery boundary invalidates the earlier result. `supervisionAvailable = false` prevents escalation and withholds the action. These fields preserve, rather than replace, every independent veto, expiration, binding, freshness, prerequisite and restriction-continuity requirement; a true value does not override any of them.

These fields do not specify or prove a repair workflow, target effect, human presence, provider, queue or budget guarantee. Their values are bounded signed availability assertions under the installed source and exact binding only.

Validity MUST end no later than the ordinary proof, any required prerequisite, any required observation freshness deadline, or issuer key validity. Ordinary proofs remain limited to ten seconds; a sidecar cannot prolong one. Evaluation time MUST NOT be in the future; use at exact expiration is refused. Invalid, unavailable or rolled-back trusted time MUST NOT restore authority. Earlier revocation or invalidation terminates use regardless of signed expiration. A valid signature is not evidence that the state remains active.

Schema validation is a shape prerequisite. It does not authenticate a source, verify a JWS, establish current state or authorize target release. Ingestion MUST reject duplicate JSON keys, nonfinite numbers, unsafe integers, invalid Unicode and unknown fields; integer control/count/time fields MUST reject booleans and fractional or integral float tokens. JSON Schema alone does not enforce all these representation rules. No decision verb enumeration replaces Core's result: supervision and tightened constraints remain normative. A consumer MAY further restrict them, never loosen them. The complete verified decision and bound evidence references are recorded under existing Audit semantics without introducing an unsigned proof claim or relying on the final hash of a record that will contain the decision. Target-effect and non-invocation attestations remain #129's separate evidence contract.

## Deterministic vectors and conformance boundary

[`conformance/software-substrate-execution.json`](conformance/software-substrate-execution.json) follows the ROS2 set's `profile`, `vectors`, `request`, and `expect` form. Fixed modeled inputs include already evaluated envelope values and authenticated-status fixtures; they do not define A/E computation or stand in for real signatures/status acquisition. `decision` is a vector reading (allow/escalate/deny), not a normative wire decision enumeration. Supervision and `tightenedAtMost` fix the result contract. Rejected bindings or prerequisites, an unverified repair path, or unavailable supervision require withholding and never become an allow through escalation.

The suite defines an identical-input determinism check; demand/capacity monotonic pairs; no-loosen composition; class/destination/proof/profile/request/evidence substitution; exact freshness/proof-expiration boundaries; revocation, refresh and restart continuity; undefined observations and veto preservation. Monotonic pairs use `supervisionAtLeast` and `decisionNotLooserThan` relative to the named baseline; a tighter result is permitted. The same file publishes a synthetic `schemaFixture` and 26 `schemaVectors`; apply each specified path mutation independently to a fresh fixture and compare schema acceptance, never use the fixture as authority. Providers MUST also satisfy all applicable existing envelope and KTP requirements. The suite does not test #129's queue/replay/budget/target-effect contract.

A conformance report MUST pin the adopted KTP release, execution-profile/schema/vector digests and independently accessible implementation release; report every expected and actual result; distinguish modeled inputs, observed execution and validated findings. Vector/schema checks are prerequisites, never runtime certification, production safety or proof of historical prevention. This draft's vector publication alone does not establish implementation conformance.

## Compatibility and provenance (informative)

This is proposed additive opt-in material against `v2.1.0`: existing implementations that do not declare it acquire no new required wire processing. No ordinary proof claims, released core formula, release tag or DOI are changed. A declaring implementation gains new interface and evidence obligations and cannot claim conformance merely because it previously consumed KTP. If review would require a formerly conforming implementation to change, VERSIONING requires MAJOR classification and migration. Compatibility is proposed, not certified.

The unreleased readiness work is explicitly a precedent, not a shipped v2.1.0 prerequisite. Any final normative dependence on that work must name the release that actually adopts it and reassess compatibility. Repository placement and a draft PR are not adoption. D-009 records an approval floor of 2026-10-07 and review-by of 2026-10-28; the maintainer controls the clock and the A/B/C decision.

Proposed by Mike Storm; text edited by Codex for Mike Storm, following Chris Perkins's placement guidance. KIL was built first as the experimental precursor, permanently recorded separately from standards ownership. [#130](https://github.com/nmcitra/ktp-rfc/issues/130) records experimental source `514e910ea9427e0497c4fe8a1ec279b554e75176` and the **open accessible, pinned, reproducible release gate**. No qualifying release is currently cited, and this draft does not ask reviewers to rely on private implementation evidence. First conformance to this proposed profile is unestablished. Computation research remains external to normative text. Other implementations may conform on equal terms.
