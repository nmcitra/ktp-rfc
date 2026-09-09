# Historical Resilience and Current Operational Readiness

**Status: unreleased normative companion.** This contract preserves verified historical achievements and separately requires current, independently assessed readiness for each governed operation. Readiness is a scoped prerequisite for authority. It does not issue a permission, create standing, or establish capacity by itself.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

Human principals use [human-eligibility.md](human-eligibility.md); this software-agent
readiness contract still applies to the actual automated executor under human
delegation or supervision. Its history-preservation requirements do not impose
indefinite retention of personal evidence: [privacy-evidence.md](privacy-evidence.md)
governs authorized correction and erasure, including unavailable verification
after disposition. Unavailable evidence cannot satisfy a current verification
requirement, and erasure cannot clear revocation or create fresh standing.

## History and current authority

An authenticated Proof of Resilience remains historical evidence of the event it records. Elapsed time alone MUST NOT subtract its contribution, erase the event, or convert its history into a failed assessment. A finding that evidence was forged, incorrectly attributed, or otherwise invalid MAY correct its admissibility through the existing accountable process. The finding, correction, and affected history MUST remain auditable; preserving history is not a promise to preserve false evidence as valid.

Readiness MUST NOT be added to Proof of Resilience, the External Root, peer contributions, or any other component of E_base. Assessment completion, a successful heartbeat, re-signing, and readiness renewal MUST NOT mint standing. Other existing standing, accountability, loss, and ceiling rules remain binding. Historical standing and readiness for a named operation MUST be distinguishable in operator displays and audit records.

For an ordinary governed operation, the enforcer MUST establish a valid matching readiness assessment in addition to all existing authorization conditions. An absent operation entry, absent assessment, failed verification, expiry, invalidation, or unresolved required readiness state MUST deny that operation. Missing readiness MUST NOT select an unrestricted default, a lower supervision substitute, or a legacy profile.

Passing readiness only satisfies this prerequisite for the exact approved scope. It cannot widen an existing grant, increase environmental capacity, remove an applicable ceiling, lower a supervision floor, or override Soul, `A > E`, zero capacity, or any earlier veto. A narrow assessment MUST NOT reactivate every operation supported by the subject's historical standing.

## Installed profile and independent assessment

The active deployment profile MUST declare its standing policy as the exact object:

```text
standing_policy = {
  "mode": "history-with-scoped-readiness-v1",
  "profile_id": <installed readiness profile ID>,
  "version": <installed readiness profile version>,
  "digest": <installed readiness profile digest>
}
```

The readiness profile is a separate complete object:

```text
{
  "profile_version": "ktp-readiness-profile-v1",
  "profile_id": <ID>, "version": <version>,
  "conformance_level": <trusted level>,
  "assessor_registry_digest": <pinned registry digest>,
  "operations": [{
    "operation_id": <ID>, "scope": <exact scope>,
    "assessment_spec_digest": <pinned assessment specification>,
    "max_age_seconds": <declared positive bounded maximum age>,
    "required_checks": <nonempty set of check IDs>,
    "assessor_ids": <authorized assessors for this operation>
  }]
}
```

Installation MUST authenticate the complete deployment and readiness profiles, their relationship, and the assessor registry through pre-existing governance trust anchors. A candidate request, profile, or assessor MUST NOT appoint its own approving authority. No universal readiness score, lifetime, or assessment formula is defined here. The deployment MUST justify and declare the assessment requirements and maximum age appropriate to each scope before use.

The pinned assessment specification MUST define the required challenges, checks, evidence, acceptance criteria, limitations, and the operations its results support. Its scope mapping MUST be independently reviewed. A basic availability or connectivity check cannot establish readiness for an operation whose failure modes it does not examine. The specification MUST identify assumptions about the environment and parameters that a verifier must check at use.

That pinned specification MUST also identify the separately authorized safe assessment route: its approving authority, capability and facility bindings, allowed assessment operations, limits, and prerequisites. A mutable locator without an authenticated declaration is insufficient. The profile's digest binding makes these declarations part of the approved assessment contract; the reference helper does not execute or certify the route.

Changing the standing policy, readiness scope, criteria, maximum age, assessor registry or enforcement bindings requires an authenticated revision approved by incumbent governance authority before installation. The candidate revision MUST NOT appoint its own approvers. Readiness migration or a profile version increase MUST NOT weaken the protected emergency-policy amendment process when that policy's evaluation binding is affected.

The assessor registry MUST establish identity, relevant competence, permitted assessment scopes, accountable oversight, independence, authorized signing keys, and revocation arrangements. The assessed subject MUST NOT adjudicate its own pass result or choose the passing criteria. Subject-produced observations MAY be inputs, but an independently authorized assessor MUST verify the required evidence. A signature or registry label alone does not prove competence, independence, or that the assessment occurred.

## Exact subject, operation, and environment binding

Every assessment and actual request uses this complete subject object:

```text
subject = {
  "agent_id": <ID>, "lineage_id": <ID>,
  "software_digest": <digest>, "model_digest": <digest>,
  "configuration_digest": <digest>, "toolchain_digest": <digest>,
  "permissions_digest": <digest>
}
scope = {
  "zone_id": <ID>, "resource_id": <ID>,
  "environment_digest": <digest>, "parameters_digest": <digest>
}
```

These digests MUST bind the actual executing artifacts, configuration, toolchain, permissions configuration, resolved environment, and operation parameters. Their referenced contents and measurement path MUST be independently authenticated. Copying matching digest strings from an assessment into a request does not establish that the running subject or target matches them. A version label without an authenticated artifact binding is insufficient.

The reference profile and helper support exact matches only. An implementation supporting a broader or parameterized scope MUST separately specify, review, and test a restrictive matcher and its declared boundaries. It MUST NOT interpret these exact fields as wildcards or infer that a successful assessment covers more resources, environments, parameters, or tools. The actual request's operation, subject, and scope MUST match one installed operation entry and its active assessment.

A software or model upgrade remains a witnessed transition in the same lineage, with the old history retained. A changed subject binding MUST NOT inherit readiness solely because the agent ID is unchanged. Changes outside the assessed scope require a new applicable assessment before dependent operation. A readiness check does not establish independent measurement of all aspects of autonomy or environmental capacity.

## Signed assessment and actual freshness

The assessment attestation contains exactly:

```text
attestation_version = "ktp-readiness-attestation-v1"
attestation_id, subject, deployment_profile_digest, readiness_profile_digest
readiness_epoch, operation_id, scope
challenge = { challenge_id, nonce, issued_at }
assessment_spec_digest
checks = [{ check_id, observed_at, evidence_digest }]
assessed_at, issued_at, expires_at, assessor_id
outcome = "passed"
signature
```

The challenge nonce MUST contain 32 cryptographically random bytes encoded as unpadded canonical base64url. The challenge, assessor, subject, scope, criteria, and required evidence MUST be bound together before assessment. The required check IDs MUST each appear exactly once, with no omitted, substituted, or extra check accepted as a replacement. Each evidence digest MUST resolve to the actual verified evidence for that challenge and binding.

Issuance MUST verify the actual check and assessment times using trusted evidence and time. For every required check, the following ordering and age limits MUST hold:

```text
challenge.issued_at <= check.observed_at <= assessed_at <= issued_at <= now
now < expires_at
expires_at <= oldest_required_check.observed_at + max_age_seconds
```

Thus a newer cheap check cannot refresh an older required check. Re-signing, copying evidence, restarting a process, changing an assessment ID, or emitting heartbeats MUST NOT reset the underlying observation times or permitted validity. A renewed assessment requires the fresh evidence prescribed by the installed specification, not only a new signature or expiration.

The challenge MUST be consumed atomically at issuance. Before ordinary use, the complete signed attestation and its exact digest MUST be durably registered as active under the externally authenticated readiness epoch for that subject, operation, and scope. An unregistered signed assessment does not satisfy readiness. Duplicate challenge use and conflicting registrations MUST fail under the deployment's authenticated state protocol.

The current epoch and complete active-attestation digest MUST be obtained from trusted state, not the candidate. Registration, invalidation, and configuration transitions that form shared Oracle state MUST satisfy [`oracle-consensus.md`](oracle-consensus.md). Signature verification alone neither commits a registration nor establishes its continuing validity.

## Current invalidation, revocation, and safe reassessment

Readiness MUST be invalidated for dependent operations when a required subject or scope binding changes, required criteria cease to be satisfied, the applicable profile or assessment requirements change, or an authorized suspension or revocation takes effect. An established incident may require reassessment under the pinned criteria even if the software digest is unchanged. The deployment MUST define who can suspend or revoke and how an enforcer obtains sufficiently current status.

Known invalidation or revocation MUST prevent further dependent execution. An enforcer unable to establish required current status MUST deny that operation; a still-valid signature does not supply missing status. Invalidation, the accepted epoch, and the active registration MUST survive restart, replay, failover, profile replacement, and restoration from backup. A stale epoch or earlier successful attestation MUST NOT restore readiness.

Reassessment MUST use an independently authorized, bounded assessment capability and environment. The candidate gains only the authority already granted for those assessment actions, subject to existing constraints. The absence of an ordinary readiness entry does not create an assessment capability automatically. Assessment facilities and supervising operators require their own authority for what they perform. Relabeling an ordinary production operation as an assessment MUST NOT change its prerequisites or grant the missing authority.

A test that cannot safely run without the candidate's missing production authority MUST stop; the test MUST NOT borrow that authority in order to establish it. An authorized operator may provision an appropriate isolated facility through its own normal process. Neither an assessment credential nor a new attestation is an emergency override. Restoring current readiness requires the prescribed assessment and authenticated activation, not resurrection of the previous record.

## Ordinary proofs and the signed decision sidecar

Ordinary proofs retain `0 < exp - iat <= 10` seconds and `iat <= now < exp`. Every dependent action requires both a fully verified ordinary proof and currently valid matching readiness. The proof's expiration MUST NOT extend beyond the readiness on which its dependent authority relies. A longer assessment validity does not lengthen the ordinary proof lifetime.

The exact actual request object used for readiness binding is:

```text
{ request_id, subject, operation_id, scope,
  deployment_profile_digest, readiness_profile_digest }
```

The enforcer MUST derive it from the authenticated invocation and resolved actual subject, operation, environment, and parameters. `request_id` identifies that invocation under the deployment's replay controls. A supplied request digest or claimed parameters digest MUST NOT replace this construction and verification.

The signed readiness decision sidecar contains exactly:

```text
decision_version = "ktp-readiness-decision-v1"
request_digest, proof_digest, attestation_digest
readiness_profile_digest, deployment_profile_digest, readiness_epoch
evaluated_at, expires_at, issuer_id, signature
```

Its authorized issuer MUST verify the complete request, ordinary proof, installed profiles, active assessment, evidence bindings, and current epoch/status. Decision expiration MUST be no later than the ordinary proof expiration, readiness expiration, or applicable issuer/assessor key-validity end. The evaluation time MUST be established and must not be in the future. Known revocation or invalidation can terminate use earlier than any signed expiration.

A sidecar binds an already complete ordinary proof; it neither replaces that proof nor grants permission by itself. The enforcer MUST recheck required readiness status for each dependent action and during continuing operations as required by their execution contract. Upon expiration or loss of a required condition, execution must cease through the existing predeclared bounded safe transition. A sidecar cannot authorize arbitrary task completion after that point.

The complete signed decision is recorded in the existing signed trajectory `action.details.readiness` object under [`trajectory-signatures.md`](trajectory-signatures.md). No unsigned top-level extension is added. The sidecar MUST NOT depend on the final hash or signature of the trajectory record that will contain it. Existing trajectory signing, final-head anchoring, audit, and execution replay/budget rules remain binding.

## Canonicalization, signatures, and digest boundaries

The readiness-v1 schemas constrain the named objects above. Objects MUST NOT acquire undeclared fields or be silently normalized by dropping fields. The complete attestation or decision payload is JCS of the object excluding exactly `signature`. Every other field and nested value is included. The compact JWS protected header contains exactly `alg`, `kid`, and `typ`, using JCS bytes; `typ` is respectively `ktp-readiness-attestation-v1` or `ktp-readiness-decision-v1`.

The strict UTF-8, JCS, canonical base64url, signature encoding, integer-range, low-s, and trusted algorithm/key requirements in the trajectory companion apply. Readiness-v1 times are nonnegative Unix seconds represented as JSON integer tokens, not the trajectory format's UTC strings. Profile version numbers, maximum ages, and readiness epochs MUST be positive integer tokens; booleans and floating representations are invalid. All integer controls and times are bounded by 2^53 - 1. No detached or compressed payload, unprotected header, embedded key, remote key locator, `none`, shared-secret algorithm, or alternate role is accepted. The assessor or decision issuer MUST be authorized for the exact role and scope. The issuing key's authorized validity MUST cover issuance through the artifact's expiry; both the start and end of that interval require independent verification, and known revocation still takes precedence.

The trusted conformance level selects the digest algorithm: SHA-256 for Levels 1 and 2, SHA-384 for Level 3. Stricter cryptographic requirements remain binding; support for one classical signature does not establish compliance with threshold, hybrid, custody, or other requirements the deployment needs.

Digest inputs are unambiguous:

- Readiness profile: JCS of the complete profile object.
- Attestation and decision: JCS of the complete signed object, including `signature`.
- Request: JCS of the exact actual request object defined above.
- Ordinary proof: the complete ASCII compact JWS bytes, including header, payload, and signature.
- Deployment profile: the exact installed profile bytes under its existing binding contract.

Other evidence and artifact digests MUST bind the exact contents identified by their pinned specifications and trusted configuration. Verifiers MUST authenticate those contents and their meaning. A string with the correct digest shape is not evidence that the referenced artifact, assessment, or environment was checked.

## Version migration and conformance limits

The active deployment profile uses the v3 schema and the mandatory `history-with-scoped-readiness-v1` standing policy. The published original v2 deployment schema remains archived for interpreting its original records. A v2 profile MUST NOT be silently reinterpreted as readiness-enabled, and its absence of readiness declarations MUST NOT imply readiness.

Activation MUST install a durable authenticated floor for the accepted deployment-profile version, standing-policy mode, readiness profile, evidence format, and current epoch. Existing agents retain admissible historical PoR but start with current readiness unestablished for dependent scopes until assessed and activated. Legacy profiles, prior proofs, missing operation entries, outages, and rollback MUST NOT provide a compatibility path around that floor. A changed lineage or profile identifier cannot erase migration or invalidation state.

The reference module `scripts/readiness.py` and `scripts/test-readiness.py` exercise declaration/semantic checks and supported cryptographic bindings using supplied trusted context. They do not authenticate registries or running artifacts, conduct real assessments, establish assessor competence, implement durable challenge or epoch stores, execute Oracle consensus, or replace the ordinary authorizer. [`readiness-lifecycle-v1.json`](conformance/readiness-lifecycle-v1.json) defines the downstream lifecycle cases needed to test those deployment mechanisms.

This design refines the concern recorded as graph claim **CL332**: dormant credentials must not preserve current authority indefinitely. It enforces that concern through scoped current readiness rather than an automatic subtraction from historical achievements. **C1121** supplies the witnessed-upgrade principle: same lineage does not make changed code ready. **CL784** identifies how decaying an adversity-fed accumulator can perpetuate unequal evidence opportunities; this contract avoids adding that decay but does not solve the remaining calibration of adversity exposure or prove assessments equally accessible. These are design provenance and remaining measurement obligations, not empirical validation of a universal readiness model.
