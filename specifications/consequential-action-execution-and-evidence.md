# Consequential-action execution and evidence

**Status: unreleased normative companion.** Decision: D-012 ([#129](https://github.com/nmcitra/ktp-rfc/issues/129)). Release baseline: **KTP `v2.1.0`**. This additive, opt-in contract has no independent release number, tag, or DOI and makes no change to KTP core.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Scope and dependencies

This companion defines execution-time constraints for a consequential action after an installed policy has produced a signed consumption decision. It defines neither an authorization formula nor a way to calculate capacity, supervision, readiness, or consumption. A consumer MUST consume the complete signed consumption decision produced under the [software-substrate profile](software-substrate-execution-profile.md) and its [decision schema](../schemas/software-substrate-decision.json); it MUST NOT rederive, replace, widen, or duplicate any profile calculation.

This companion does not prescribe storage, a target product, KAG, KIL, a queue, a gateway, or a reconciliation implementation. KAG is a future implementation path.

## Release contract

Before releasing a consequential action, an enforcer MUST use trusted context to revalidate the signed consumption decision against the actual action about to be released. This revalidation MUST bind the actual `enforcement_destination`, resolved `authority_class` and operation, complete ordinary proof, `request_id`, installed policy/profile revisions, and every other binding required by the consumed decision. Candidate-supplied identifiers, a prior routing result, or a copied decision digest are insufficient.

Immediately before release, the enforcer MUST revalidate the complete ordinary authorization, installed profile restrictions, required trusted current state, and every required observation; decision binding alone is insufficient. A stale, missing, unavailable, unauthenticated, or conflicting required observation or current-state result MUST withhold the action. This requirement applies even when the signed consumption decision has not expired.

The enforcer MUST release only the action and destination that the consumed decision binds. A redirect, target substitution, resolution change, parameter expansion, or loss of a required current-state observation is a new candidate with a new request identity; it MUST NOT be released under the original identity and requires a fresh applicable decision. A signed consumption decision is not a standalone permission and does not remove any existing proof, veto, supervision, capacity, or target constraint.

## Replay and retry contract

Queue exit MUST trigger fresh validation; permission at enqueue time does not carry forward. Continuing operations MUST declare checkpoints and a bounded safe transition when authority is lost. The target contract MUST declare conditional commit/version-check atomicity, its covered effects and race boundaries. A target without that capability MUST NOT be described as providing commit-time authorization guarantees.

Each consequential request MUST have a durable request identity and a canonical fingerprint of the complete release-relevant request. It is the RFC 8785 canonical profile request-binding object, including `request_id` but excluding the proof and consumed decision; its digest is the profile `request_digest`. The identity and fingerprint MUST survive process restart, retry, failover, restoration, and reconciliation. Identity and checkpoint state MUST survive the declared recovery boundary. A repeated request with the same identity and a different canonical body MUST be rejected; an implementation MUST NOT treat it as a retry, rewrite the stored body, or issue a second release.

A retry MUST preserve the durable identity, canonical operation fingerprint and target/destination binding. Any renewed consumed decision MUST be freshly validated and correlated with that same operation history. A retry that cannot establish this continuity MUST be withheld pending reconciliation and fresh evaluation. Retrying an uncertain outcome MUST NOT presume either non-dispatch or effect confirmation.

## Effect-budget contract

The installed environment MUST declare the replay domain, identity retention window, recovery/replica boundary and target idempotency contract. The retention window MUST cover the longest time a request can be queued, retried or reconciled. A duplicate or uncertain response MUST NOT authorize another invocation by generating a new transport identity. Target idempotency claims require a pinned tested target contract and retention window; no universal exactly-once guarantee is offered. Proof renewal MAY update the consumed decision after fresh evaluation, but MUST preserve the durable operation identity and unresolved dispatch/reservation state.

Where a deployment declares a shared effect budget, it MUST declare consequence units and scoped maxima for each budget scope. After successful revalidation and before dispatch, the enforcer MUST read sufficiently current shared budget state and make a conservative reservation. The budget read and reservation MUST bind the same declared consequence units, scoped maxima, budget scope, action scope, and actual target/destination as the action being released. An unavailable, stale, ambiguous, conflicting, or insufficient budget read MUST withhold the action.

Aggregate reservation authority MUST atomically apply a reservation against the shared limit across every actor, resource, and replica that can release against the same effect; all MUST be included in that scope. Distinct request, actor, resource, or replica identities MUST NOT evade a shared limit. Reservations MUST remain durable until they are reconciled to a restrictive outcome. An implementation MUST NOT double-spend a reservation through concurrent requests, retries, restart, failover, restoration, or a changed request body. This contract defines this atomicity requirement but does not define a budget formula, storage system, coordination protocol, or a shared-load scalar; the profile defines none.

## Evidence contract

An accepted reservation reduces the remaining budget of its scope. Every later request in that scope MUST be evaluated against the remainder; checking only whether that request alone exceeds the maximum is insufficient. The remainder is a further restriction applied on top of the profile decision; E and the profile result are unchanged. Supervision MAY rise as the remainder falls. The installed declaration MUST specify the accounting period and reset conditions; a reset MUST NOT erase unresolved reservations. The declaration MUST specify how resolved dispatched effects are charged and when that charge expires; a dispatched reservation is not released merely because a reset or a no-effect result occurs. A reservation is released only on authenticated protected-path evidence that nothing was dispatched for the bound action and interval. The deployment MUST declare a bounded abandonment deadline and an installed observer/reconciliation procedure to close the protected interval and obtain that evidence for an undispatched request. When the observer is healthy and coverage is complete, that procedure releases the abandoned reservation on the authenticated record. If the source is unavailable, coverage is incomplete, or the disposition remains uncertain, the reservation MUST remain held until reconciliation can establish non-dispatch; the deadline alone cannot free it. Maximum target effects and consequence units MUST be declared. Trust Score, successful execution, proof refresh, restart and retry MUST NOT replenish reservations by themselves. Uncertain effects retain conservative reservations until accountable, authenticated reconciliation establishes their actual disposition.

For this contract, the only execution/effect evidence states are `withheld`, `dispatched`, `effect_confirmed`, `no_effect`, and `unknown`.

- `withheld` means authenticated protected-path non-dispatch evidence establishes that the bound action was not dispatched during a stated interval. That evidence MUST identify its source, protected-path coverage, interval, and provenance.
- `dispatched` means authenticated evidence from the enforcer’s protected dispatch path establishes that it sent the bound action to the bound target or destination; a response status alone is not such evidence and dispatch does not prove an effect.
- `effect_confirmed` means trusted evidence confirms the bound effect at the bound target or destination.
- `no_effect` means authenticated target evidence establishes that a dispatched bound action had no effect. This state alone does not establish non-dispatch or release a reservation.
- `unknown` means the available evidence cannot establish the restrictive conclusion required to classify the outcome as withheld, dispatched, effect confirmed, or no effect.

A denial alone, a timeout, a transport exception, or an HTTP status is insufficient by itself to prove non-dispatch or non-effect. Every action withheld under this contract MUST be recorded as `unknown` unless authenticated protected-path non-dispatch evidence establishes `withheld`. That evidence MUST come from an installed authenticated source covering the complete protected path and interval; the enforcer’s timeout or exception is not such a source. A deployment MAY require a recorder; an unavailable required recorder MUST withhold release. A successful HTTP status is likewise insufficient by itself to prove the bound effect. The evidence record MUST retain the durable request identity, canonical fingerprint, consumed decision binding, actual target/destination binding, reservation reference where applicable, observed evidence, its source, interval, provenance, its state, and coverage where applicable. A recorder reference is retained when applicable.

Reconciliation MUST run across restart, retry, failover, and restoration. It MUST preserve the evidence state and any unresolved reservation, query or otherwise obtain the deployment's trusted evidence where available, and resolve uncertainty conservatively. Reconciliation MUST NOT erase an `unknown` outcome, release a conflicting retry, or infer a target effect from a decision, a denial, or an HTTP status alone.

## Canonicalization, signatures, and digest boundaries

The [evidence schema](../schemas/consequential-action-evidence.json) defines the signed record. Its payload is RFC 8785 canonical UTF-8 JSON of the complete record excluding exactly `signature`. A compact JWS MUST contain exactly the protected header members `alg`, `kid`, and `typ`, encoded as RFC 8785 canonical JSON; `typ` is `ktp-consequential-action-evidence-v1`. The signer MUST be an installed issuer authorized for the evidence role and scope. Apply the strict input, trusted algorithm and key, canonical base64url and signature requirements of the trajectory companion. Verification MUST compare the embedded payload bytes to the canonical record and verify the signer and signature.

`interval_start` and `interval_end` are nonnegative Unix seconds represented as safe integer tokens; the start MUST NOT exceed the end. `consumption_decision_digest` hashes the RFC 8785 canonical complete signed consumption-decision object, including `signature`; the installed profile selects the permitted digest algorithm. The destination member records the authenticated actual `enforcement_destination`. Marker and coverage fields are present only when observed or applicable; the reservation reference and digest occur together when a reservation exists. Schema shape alone does not verify any claim.

## Deterministic vectors and conformance boundary

The conformance suite MUST contain deterministic fixtures for release-time revalidation, changed-body rejection, retry identity preservation, conservative shared reservation, unavailable budget state, each of the five evidence states, and restart reconciliation. A vector runner MAY validate declared fixture shape and the stated expected properties. It MUST NOT claim to execute a real target, prove a real-world effect, or establish runtime certification.

The [suite](conformance/consequential-action-execution-v1.json) publishes modeled contract and schema vectors. `scripts/test-consequential-action-evidence.py` checks contract-fixture integrity and schema mutations only. A declaring implementation MUST separately report each expected/actual semantic outcome against immutable implementation and suite pins; passing this repository's integrity runner does not execute those semantics.

Passing every released vector means only that an implementation satisfies the explicit expectations of those vectors. It does not certify a target product, a deployment, an effect-budget backend, KAG, KIL, or any runtime environment. A vector suite or schema is not released merely because this companion names it.

## Compatibility and provenance (informative)

This companion is additive and opt-in. Existing `v2.1.0` conformant implementations remain conformant without it. Adoption requires a separately approved release that identifies its exact specification, schema, and vector revisions; this companion does not change a KTP release, DOI, or core contract.

The [KIL evidence gate #130](https://github.com/nmcitra/ktp-rfc/issues/130) is independent. It concerns an accessible, pinned, reproducible release and evidence boundary; it does not adopt this companion or turn any implementation into a reference implementation. Provenance for an implementation, vector suite, and release belongs in their separately published records.

KAG is a named implementation path, with no qualified accessible release or conformance run cited here. If existing conformant implementations acquire new mandatory obligations, reclassify under VERSIONING with migration.
