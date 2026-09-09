# Emergency Capabilities and Protected Policy Changes

**Status: unreleased normative companion.** This document governs separately authorized emergency actions when ordinary Trust Proof issuance is unavailable. Declaring an emergency grants no authority.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Ordinary authorization continues to expire

Ordinary Trust Proofs MUST satisfy `0 < exp - iat <= 10` seconds and `iat <= current_time < exp`. A future-issued or expired proof MUST NOT authorize an action. These requirements apply to every zone, conformance level, existing session, cached proof, queued operation, and continuing action. An outage, surrounding session token, human approval, or low-risk label MUST NOT extend a proof. Invalid timestamps, unverifiable time, or clock rollback MUST NOT manufacture additional validity.

An operation that loses authorization MUST cease protected execution through its previously declared, bounded safe transition. A safe transition is an explicitly authorized action with its own limits, not permission to finish arbitrary work. Independent physical safeguards remain part of the substrate's safety design; this protocol does not assume that abruptly removing power is always safe.

## Separate authority, fixed scope

An emergency capability is a separate authorization for a named safety or recovery operation. It MUST NOT be a replacement Trust Proof, a general administrator credential, or a retry of a denied candidate with its checks removed. Ordinary work still requires ordinary authorization.

The default is disabled. A deployment that enables this capability MUST pin an approved policy's ID, version, and digest in its deployment profile and enforcement configuration. Missing, invalid, unapproved, suspended, revoked, or unverifiable policy state MUST deny emergency execution. The schema-valid declaration alone confers no authority.

Every permitted entry MUST name an exact action, authenticated subject, resource, operation, parameter set, execution budget, and evaluation-profile digest. Wildcards, inherited administrator rights, and open-ended terms such as "essential operations" or "life-safety actions" do not identify a permission. Requests MUST match the whole entry, including absence of undeclared parameters; identifiers are compared literally after the evaluation profile's fixed resource resolution, never interpreted as glob patterns. Parameters in this initial declaration format are exact-match JSON scalars; a deployment needing ranges must declare separate bounded entries or a subsequently specified format.

The evaluation-profile digest MUST bind the complete executable evaluation and enforcement configuration: demand and capacity measurement, units and thresholds, evidence sources and freshness limits, sovereignty checks, identity and resource resolution, and bounded safe transitions. Changing code, bindings, or configuration that affects those checks is a policy change. A mutable URL or registry name alone is insufficient. Independently available local evidence MAY support an emergency operation, but an expired ordinary proof MUST NOT be substituted for current evidence.

The existing sovereignty veto, capacity check, margin rules, and tighten-only supervision remain binding for each emergency candidate. `A > E`, zero capacity, an unresolved sovereignty constraint, or an existing veto MUST NOT be overridden by emergency credentials. If the declared evaluation cannot establish the required inputs, it MUST deny execution. Approval does not increase capacity. A different safety action must be evaluated on its own actual parameters.

## Declaration

[`emergency-policy.json`](../schemas/emergency-policy.json) constrains the declaration. It contains no self-certifying approval count or signature field:

| Field | Meaning |
|---|---|
| `policy_id`, `version`, `zone_id` | The policy lineage, monotonically increasing version, and deployment boundary |
| `predecessor_digest` | Digest of the installed predecessor; null only for the first version |
| `custodians` | At least three named, independently controlled principals, their pinned key identifiers, and control domains |
| `change_control` | Amendment approval threshold, review and ratification periods, and required external review |
| `activation` | Activation threshold, maximum duration, and prohibition on automatic renewal |
| `actions` | Exact permissions, budgets, and bound evaluation profiles |
| `logging` | Durable evidence required before execution |

Distinct strings do not prove independence. A deployment MUST establish the principals' identities, key custody, and independent control through its existing trusted governance registry. One person or control domain MUST NOT count more than once by holding several keys. A deployment unable to establish at least three independent custodians cannot enable this emergency capability.

## Changing or installing policy

Every installation, replacement, restoration, or amendment MUST pass the following process during verified normal operation. This includes first installation and changes to subjects, resources, operations, parameters, budgets, duration, evaluation profiles, custodians, keys, activation rules, amendment rules, deployment references, or the enforcement trust anchors that govern them.

1. Record the complete proposal and its exact digest, predecessor, rationale, impact assessment, and independent external review. Existing charter proposal requirements also apply.
2. Publish notice and provide the complete proposal to the authorized reviewers for at least **90 days**. The notice identifies the fixed digest; any change to the proposal restarts review. Sensitive operational details may be access-controlled without concealing the proposed authority change from those entitled to review it.
3. Obtain verified signatures from at least **90% of the full established governing custodian body**, rounded upward, and at least three independent custodians. Count the incumbent roster, not the subset reachable during a failure or the roster proposed by the candidate. A deployment's stricter existing threshold also applies.
4. After the last required approval and external review, wait at least **14 further days** for ratification. Any outstanding objection requiring resolution under the charter blocks installation.
5. Verify the amendment evidence, signatures, predecessor, time periods, and policy/configuration digests, then install atomically with an immutable audit record and monotonic version state.

These are emergency-policy minimums, stricter than the ordinary charter amendment example in `[KTP-GOVERNANCE]`. Stricter charter requirements remain binding. A constitutional amendment still requires the full process in Constitution Article VII, including Oracle consensus and federated ratification; this companion cannot waive it.

The installed policy and independently pinned incumbent governance registry determine who may approve a successor. A candidate MUST NOT appoint its own approving electorate. For first installation, the roster MUST already be established by the deployment's normal charter process; creating it during the emergency does not qualify. Changing a policy ID, substituting a deployment profile, replacing a verifier, rotating keys, or deleting local state MUST NOT bypass the same controls. The installed and candidate control rules both apply; the stricter requirement wins.

No policy installation, amendment, restoration, key-roster expansion, or authority expansion is permitted during an outage or emergency. Normal operation MUST be established by the pre-existing recovery checks, including restored ordinary verification and governance/audit services. An incident commander's declaration alone is insufficient. Reduced Oracle quorums MUST NOT be used to approve changes or issue ordinary Trust Proofs.

In-place editing and rollback to an older policy are prohibited. A correction uses a new version linked to the current predecessor and follows this process. Loss of the installed version, revocation state, or trusted time MUST disable emergency execution until that state is securely recovered; it MUST NOT reset the system to a permissive first-installation state.

The sovereignty, capacity, expiration, independence, minimum review, minimum approval, audit, and no-outage-amendment requirements of this document cannot be weakened by a deployment policy. Making the amendment rule easier is itself an amendment, subject to the incumbent rule and these fixed protocol minimums.

## Signed evidence and protected state

Digests use `sha256:` followed by 64 lowercase hexadecimal digits or `sha384:` followed by 96 lowercase hexadecimal digits. Policy digests cover the exact UTF-8 policy bytes. Level 3 deployments MUST use SHA-384 for every emergency security binding, including policy, predecessor, evaluation configuration, incumbent roster, and review evidence, as required by `[KTP-CRYPTO]`. The independently trusted deployment profile determines that level; a candidate MUST NOT select a lower level or algorithm. Implementations MUST reject duplicate JSON object names and nonfinite numbers. They MUST verify the digest over the stored bytes rather than parse and reserialize before verification.

Amendment and activation evidence MUST use distinct signed payload purposes. Use JWS as specified in [RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html), with signature algorithms and key validation satisfying `[KTP-CRYPTO]`; ES256 support is REQUIRED, but its use is insufficient where the trusted deployment's cryptographic profile requires stronger signing. Each counted signature MUST cover the same complete evidence payload. `alg`, `kid`, and `typ` MUST be protected headers. The respective `typ` values are `ktp-emergency-amendment+jws`, `ktp-emergency-activation+jws`, and `ktp-emergency-revocation+jws`; they MUST NOT be accepted as ordinary Trust Proofs. `none`, shared-secret signatures counted as independent approvals, and candidate-supplied trust anchors are prohibited.

An amendment payload MUST bind the policy digest, ID, version, zone, predecessor digest, incumbent roster digest, proposal identifier, review-start time, approval time, earliest installation time, and external-review digest. The verifier MUST authenticate the underlying notice, review, and ratification evidence; signed claims about dates alone do not prove that the process occurred.

An activation payload MUST bind the policy digest, ID, version, zone, incident identifier, selected action IDs and narrower budgets, an unpredictable activation identifier, issuance time, and expiration. A revocation payload MUST bind the policy lineage, affected version or activation, issuer, time, reason, and unique revocation identifier. Key validity and revocation MUST be checked against the independently trusted registry, not against assertions inside these payloads.

Approval receipts, the installed digest and version, trusted roster, suspension/revocation state, activation identifiers, and consumed budgets MUST be protected against unilateral replacement and rollback. A writable configuration file with a signature check that its editor can disable does not meet this requirement. Deployment commissioning MUST verify that the same protected change process controls the verifier, its trust anchors, and the policy binding.

## Activation and execution

Activation selects an already installed policy; it does not amend it. At least **two independent custodians** MUST approve the exact activation, or more if the policy requires. An authenticated incident trigger alone does not satisfy this approval rule. Activation lasts no longer than the declared limit, with an absolute maximum of **four hours**, and ends earlier on revocation or loss of a required condition.

Automatic renewal is prohibited. Repeated activation, another incident label, process restart, or a second PEP MUST NOT reset the time or execution budgets for the same continuing incident. The absolute incident deadline is the first activation's issuance time plus the approved maximum duration; pauses and subsequent activations do not move that deadline. Each activation MUST establish issuance_time <= current_time < expiration, with expiration no later than that deadline. Per-action execution limits apply cumulatively across activations for the incident. Evidence that an incident ended and normal operation was restored is required before a new incident can establish new budgets. Emergency operators cannot create that evidence merely by closing a ticket.

Before each execution, the verifier MUST:

1. Verify the installed policy, amendment evidence, activation signatures, subject authentication, exact request match, and all applicable revocation state.
2. Verify trusted time, the activation's remaining duration, and atomically reserve from its remaining shared execution budget. If replay or budget state cannot be verified or coordinated, deny the action.
3. Evaluate the bound local evidence, sovereignty, capacity, margin, and supervision checks for this candidate; any veto remains a veto.
4. Durably record the intent, policy and activation digests, incident, request, evidence, checks, and budget reservation before allowing execution; append the result afterward. An unavailable remote Flight Recorder MAY be replaced by the preapproved tamper-evident local recorder. If neither can durably record, deny execution.

Ordinary denied requests MUST NOT automatically fall through to this path. The caller must request the separately declared action, and the verifier must establish its independent authorization and conditions. Emergency credentials cannot change standing, sign replacement ordinary proofs, reduce quorum, or edit their own policy.

Authorization and the required evidence checks MUST remain valid throughout a continuing emergency operation, not only at admission. At activation expiration, the incident deadline, revocation, or loss of a required condition, protected execution MUST cease through its predeclared bounded safe transition. One long-running invocation MUST NOT continue the original task beyond those limits. The evaluation profile MUST declare how the substrate enforces these boundaries and the bounded transition; an implementation unable to enforce them cannot authorize that action.

## Suspension and revocation

Any authenticated incumbent custodian MAY immediately suspend or revoke the policy or an activation. An automatic protection MAY also suspend execution. These operations remove authority and do not wait for the amendment period. They MUST be durably recorded and enforced before further execution.

A request denial, an evidence refresh failure, or the normal end of an activation does not by itself suspend or revoke the installed policy. A policy-level lock is an explicit recorded operation, distinct from stopping an individual action or activation. This distinction MUST be visible to operators before they choose a policy-level suspension or revocation.

Suspension or revocation is sticky across process restart, failover, and replay. It MUST NOT automatically restore prior permissions on a timer. Restoring a suspended or revoked policy requires a new approved version through the full amendment process in normal operation. Revoking one activation cannot be bypassed by immediately issuing another for the same incident.

## Conformance and verification limits

[`outage-safety-v1.json`](conformance/outage-safety-v1.json) defines mandatory downstream boundary cases. The declaration checker and its regression tests verify shape, finite values, roster/count constraints, fixed control minimums, and bounded scopes. They do not verify signatures, identity independence, review history, protected installation, revocation distribution, time, or runtime decisions.

A deployment claiming emergency-capability conformance MUST additionally demonstrate the signature, installation, amendment, activation, replay, rollback, budget, logging, and revocation behaviors above, including attempts by a single administrator and during loss of normal services. This repository contains no runtime authorizer; a passing declaration is not evidence that these controls have been implemented.
