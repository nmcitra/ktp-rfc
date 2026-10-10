# Consequential-action execution and evidence

**Status: proposal; not adopted or released.** Decision: [#129](https://github.com/nmcitra/ktp-rfc/issues/129); decision-record assignment remains maintainer-owned. Release baseline: **KTP `v2.1.0`**. This is an additive, opt-in contract. It has no independent release number, tag, or DOI, and it makes no change to KTP core. Published 2026-09-18 · MINOR · floor 2026-10-09 · review-by 2026-10-30.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Scope and dependencies

This proposal defines execution-time constraints for a consequential action after an installed policy has produced a signed consumption decision. It defines neither an authorization formula nor a way to calculate capacity, supervision, readiness, or consumption. A consumer MUST consume the complete signed consumption decision produced under [#124](https://github.com/nmcitra/ktp-rfc/issues/124); it MUST NOT rederive, replace, widen, or duplicate any #124 calculation.

The #124 profile and its decision binding are not adopted at the `v2.1.0` baseline. Final binding in this proposal is therefore gated on the disposition of [#122](https://github.com/nmcitra/ktp-rfc/pull/122) and #124. Until both gates clear, this document is a proposal and a vector or schema result under it MUST NOT be represented as a released KTP execution contract.

This proposal does not prescribe storage, a target product, KAG, KIL, a queue, a gateway, or a reconciliation implementation. KAG is a future implementation path.

## Release contract

Before releasing a consequential action, an enforcer MUST use trusted context to revalidate the signed consumption decision against the actual action about to be released. This revalidation MUST bind the actual target or destination, resolved operation class, complete ordinary proof, request identity, installed policy/profile revisions, and every other binding required by the consumed decision. Candidate-supplied identifiers, a prior routing result, or a copied decision digest are insufficient.

Immediately before release, the enforcer MUST revalidate the complete ordinary authorization, installed profile restrictions, required trusted current state, and every required observation; decision binding alone is insufficient. A stale, missing, unavailable, unauthenticated, or conflicting required observation or current-state result MUST withhold the action. This requirement applies even when the signed consumption decision has not expired.

The enforcer MUST release only the action and destination that the consumed decision binds. A redirect, target substitution, resolution change, parameter expansion, or loss of a required current-state observation is a new candidate and MUST be withheld until it receives a fresh applicable decision. A signed consumption decision is not a standalone permission and does not remove any existing proof, veto, supervision, capacity, or target constraint.

## Replay and retry contract

Queue exit MUST trigger fresh validation; permission at enqueue time does not carry forward. Continuing operations MUST declare checkpoints and a bounded safe transition when authority is lost. The target contract MUST declare conditional commit/version-check atomicity, its covered effects and race boundaries. A target without that capability MUST NOT be described as providing commit-time authorization guarantees.

Each consequential request MUST have a durable request identity and a canonical fingerprint of the complete release-relevant request. The identity and fingerprint MUST survive process restart, retry, failover, and reconciliation. A repeated request with the same identity and a different canonical body MUST be rejected; an implementation MUST NOT treat it as a retry, rewrite the stored body, or issue a second release.

A retry MUST preserve the durable identity, canonical operation fingerprint and target/destination binding. Any renewed consumed decision MUST be freshly validated and correlated with that same operation history. A retry that cannot establish this continuity MUST be withheld pending reconciliation and fresh evaluation. Retrying an uncertain outcome MUST NOT presume either non-dispatch or effect confirmation.

## Effect-budget contract

The installed environment MUST declare the replay domain, identity retention window, recovery/replica boundary and target idempotency contract. A duplicate or uncertain response MUST NOT authorize another invocation by generating a new transport identity. Target idempotency claims require a pinned tested target contract and retention window; no universal exactly-once guarantee is offered. Proof renewal may update the consumed decision after fresh evaluation, but MUST preserve the durable operation identity and unresolved dispatch/reservation state.

Where a deployment declares a shared effect budget, it MUST declare consequence units and scoped maxima for each budget scope. Before release, the enforcer MUST make a conservative reservation and MUST read sufficiently current shared budget state before accepting that reservation. The capacity read and reservation MUST bind the same declared consequence units, scoped maxima, budget scope, action scope, and actual target/destination as the action being released. An unavailable, stale, ambiguous, conflicting, or insufficient capacity read MUST withhold the action.

Aggregate reservation authority MUST atomically apply a reservation against the shared limit across every actor, resource, and replica in the declared budget scope. Distinct request, actor, resource, or replica identities MUST NOT evade a shared limit. Reservations MUST remain durable until they are reconciled to a restrictive outcome. An implementation MUST NOT double-spend a reservation through concurrent requests, retries, restart, failover, or a changed request body. This contract defines this atomicity requirement but does not define a budget formula, storage system, coordination protocol, or a shared-load scalar in #124.

## Evidence contract

Budget reservations MUST reduce the available capacity E used to evaluate the next request in the same scope; checking only whether a later request overflows is insufficient. Maximum target effects and consequence units MUST be declared. Trust Score, successful execution, proof refresh, restart and retry MUST NOT replenish reservations by themselves. Uncertain effects retain conservative reservations until accountable, authenticated reconciliation establishes their actual disposition.

For this contract, the only execution/effect evidence states are `withheld`, `dispatched`, `effect_confirmed`, and `unknown`.

- `withheld` means authenticated protected-path non-dispatch evidence establishes that the bound action was not dispatched during a stated interval. That evidence MUST identify its source, protected-path coverage, interval, and provenance.
- `dispatched` means the enforcer has evidence that it sent the bound action to the bound target or destination; it does not prove an effect.
- `effect_confirmed` means trusted evidence confirms the bound effect at the bound target or destination.
- `unknown` means the available evidence cannot establish the restrictive conclusion required to classify the outcome as withheld, dispatched, or effect confirmed.

A denial alone, a timeout, a transport exception, or an HTTP status is insufficient by itself to prove non-dispatch or non-effect. Without the authenticated protected-path non-dispatch evidence required for `withheld`, a denial outcome MUST be `unknown`. A successful HTTP status is likewise insufficient by itself to prove the bound effect. The evidence record MUST retain the durable request identity, canonical fingerprint, consumed decision binding, actual target/destination binding, reservation reference where applicable, observed evidence, its source, coverage, interval, provenance, and its state.

Reconciliation MUST run across restart, retry, failover, and restoration. It MUST preserve the evidence state and any unresolved reservation, query or otherwise obtain the deployment's trusted evidence where available, and resolve uncertainty conservatively. Reconciliation MUST NOT erase an `unknown` outcome, release a conflicting retry, or infer a target effect from a decision, a denial, or an HTTP status alone.

## Deterministic vectors and conformance boundary

The eventual conformance suite MUST contain deterministic fixtures for release-time revalidation, changed-body rejection, retry identity preservation, conservative shared reservation, unavailable capacity state, each of the four evidence states, and restart reconciliation. A vector runner MAY validate declared fixture shape and the stated expected properties. It MUST NOT claim to execute a real target, prove a real-world effect, or establish runtime certification.

The proposed [suite](conformance/consequential-action-execution-v1.json) publishes 20 modeled contract vectors and 11 schema vectors. `scripts/test-consequential-action-evidence.py` checks contract-fixture integrity and schema mutations only. A declaring implementation must separately report each expected/actual semantic outcome against immutable implementation and suite pins; passing this repository's integrity runner does not execute those semantics.

Passing every released vector means only that an implementation satisfies the explicit expectations of those vectors. It does not certify a target product, a deployment, an effect-budget backend, KAG, KIL, or any runtime environment. A vector suite or schema is not released merely because this proposal names it.

## Compatibility and provenance (informative)

This proposal is additive and opt-in. Existing `v2.1.0` conformant implementations remain conformant without it. Adoption requires a separately approved release that identifies its exact specification, schema, and vector revisions; this proposal does not change a KTP release, DOI, or core contract.

The [KIL evidence gate #130](https://github.com/nmcitra/ktp-rfc/issues/130) is independent. It concerns an accessible, pinned, reproducible release and evidence boundary; it does not adopt this proposal or turn any implementation into a reference implementation. Provenance for an eventual implementation, vector suite, and release belongs in their separately published records.

Proposed and edited by Mike Storm following Chris Perkins's guidance. KAG is Mike Storm's named implementation path, with no qualified accessible release or conformance run cited here. Classification and compatibility remain proposed pending maintainer review; if existing conformant implementations acquire new mandatory obligations, reclassify under VERSIONING with migration.
