# Complete Trajectory Record Signatures

**Status: unreleased normative companion.** This document defines the `ktp-trajectory-v3` record format and its explicit transition from archived legacy records. It is a breaking wire-format change. The record-format identifier and schema namespace do not themselves announce a protocol release or authorize deployment.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Complete records and trusted verification context

The active [`transaction-record.json`](../schemas/transaction-record.json) schema defines the v3 record. Its named objects are closed: an implementation MUST reject undeclared fields rather than silently discard them before verification. Explicitly extensible data, including `action.details`, remains part of the signed record, recursively and without exclusions. A new field cannot acquire authorization meaning through an unsigned extension.

Before accepting a record for authority, a verifier MUST obtain the expected agent, zone, chain, installed evaluation-profile digest, conformance level, minimum accepted record format, predecessor/head state, and authorized key bindings from independently authenticated configuration or state. The candidate record MUST NOT choose those expectations, its trusted keys, its verification mode, or whether legacy compatibility is enabled. Missing required external state MUST prevent authoritative acceptance.

The record's identities, profile, level, and format MUST match that trusted context. The agent key MUST be bound to the expected agent and signing role; the Oracle key MUST be bound to the named Oracle and its authorized zone and role. Each algorithm and key type MUST satisfy the trusted cryptographic profile and applicable key-validity and revocation policy. An identifier or timestamp asserted inside the candidate is not evidence that a key was authorized at that time.

Signature verification establishes integrity under those key bindings. It does not establish that a claimed state transition was permitted, a sensor was truthful, consensus committed the record, or the record is the unique current chain head. Those checks remain separate prerequisites for authority.

## Parsing and canonical bytes

Records, signed payloads, and protected headers MUST use strict UTF-8 JSON and the [JSON Canonicalization Scheme, RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), called JCS below. Verifiers MUST reject duplicate object names, invalid UTF-8, invalid Unicode including lone surrogates, nonfinite numbers, and values outside the v3 schema's ranges. They MUST preserve string contents without Unicode normalization, preserve array ordering, and apply JCS property ordering recursively.

JSON numeric values MUST be representable under JCS's binary64 number model. Integer values MUST be within `[-9007199254740991, 9007199254740991]`; a larger integer MUST NOT be silently rounded into the accepted range. Fields defined as integer controls, including sequence, generation, and conformance level, MUST use integer tokens in their permitted ranges. Booleans and floating-point tokens such as `1.0` are invalid for those fields. Fractional measurement fields retain their schema-defined numeric semantics. Schema defaults, coercion, field removal, and post-verification reinterpretation MUST NOT change the evaluated data.

The safe-integer bound also applies to integer-valued decimal and exponent tokens, including those inside action details. Thus `9007199254740993.0` and `1e30` are rejected as v3 numbers even though JCS can serialize some large binary64 values. Applications needing exact large values MUST declare them as strings with their interpretation bound by the profile. This restriction is a v3 input constraint in addition to JCS; it prevents large integer assertions from collapsing to the same rounded signed value.

`JCS(x)` denotes the exact canonical UTF-8 bytes of x. Ordinary JSON serialization with sorted keys is not a substitute. A received embedded JWS payload MUST equal the exact recomputed JCS payload bytes, not merely parse into an apparently equivalent object. The protected header MUST likewise be the JCS bytes of the required header object.

Timestamps use UTC with uppercase `T` and `Z`, seconds, and optional one-to-six fractional digits. Calendar dates MUST be valid. Leap-second spellings and greater fractional precision are unsupported in this format and MUST be rejected rather than rounded. Oracle attestation time MUST NOT precede the event timestamp; trusted clock and evidence-validity checks remain independent.

## JWS envelope and algorithms

Signatures use the compact serialization in [RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html): three nonempty, unpadded, canonical base64url segments separated by two periods. The protected header MUST contain exactly `alg`, `kid`, and `typ`, with a trusted algorithm, a nonempty authorized key identifier, and the appropriate purpose below. No unprotected header, detached payload, compressed payload, embedded key, remote key locator, `crit`, or `b64=false` extension is permitted. `none` and shared-secret algorithms are prohibited.

| Signing role | Exact protected `typ` |
|---|---|
| Agent record signature | `ktp-trajectory-agent-v3` |
| Oracle record attestation | `ktp-trajectory-oracle-v3` |
| Migration checkpoint | `ktp-trajectory-migration-v3` |

The role and version are part of the signed JWS input. An agent signature MUST NOT be accepted as an Oracle attestation or migration approval, even if a key happens to be present in more than one registry. Each role requires its own authorized binding.

The reference helper supports ES256 with P-256, ES384 with P-384, and EdDSA with Ed25519 or Ed448. ECDSA signatures MUST use the JWS fixed-width `R || S` representation, not ASN.1 DER. An algorithm label cannot override the trusted key's type, curve, role, or profile. For Level 3, the helper's supported classical signature choices are ES384 or Ed448, and security-binding digests use SHA-384. Unsupported or weaker choices MUST fail rather than cause profile downgrade.

ECDSA signatures MUST also satisfy KTP-Crypto's low-s rule: `0 < r < n` and `0 < s <= floor(n/2)`, where n is the curve's subgroup order. Base64url encodings MUST decode and re-encode identically; padding and alternative spellings are rejected. Neither low-s normalization nor canonical envelopes eliminate the need to select a unique final head when a signer produces another valid signature for the same payload.

These supported algorithms do not establish compliance with every KTP-Crypto requirement. Threshold participation, required hybrid signatures, key custody, and other stronger requirements of the trusted deployment remain binding. A deployment requiring an unsupported combination cannot treat successful verification by this helper as full conformance.

## Agent and Oracle signing payloads

Let B be the complete top-level record body after excluding exactly `agent_signature`, `oracle_attestation`, and `record_hash`. B contains all of the following fields, with their full nested values:

```text
record_version = "ktp-trajectory-v3"
record_id, agent_id, zone_id, chain_id, sequence, timestamp
previous_hash, previous_state, current_state, action, friction, velocity
conformance_level, evaluation_profile_digest, migration_checkpoint
```

No other field is excluded. `migration_checkpoint` is null for an ordinary record and may contain a checkpoint digest only for an explicitly migrated new genesis under the rules below. The agent signs `JCS(B)` using the agent JWS purpose. The resulting complete compact JWS string is stored verbatim in `agent_signature`.

Let O be `oracle_attestation` after excluding exactly `oracle_signature`. O contains `oracle_id`, `attestation_time`, and the complete `risk_factors` object. The Oracle signs the following payload using the Oracle JWS purpose:

```text
P = {
  "record_body": B,
  "agent_signature": <the exact complete agent compact JWS string>,
  "attestation": O
}
oracle_signature = CompactJWS(oracle_key, JCS(P))
```

The Oracle MUST first validate the agent signature, full proposed body, attestation inputs, authorized state transition, and any required consensus evidence. It MUST NOT change B after the agent signs. It MUST retain the exact agent signature string when constructing P; re-encoding or replacing a valid agent signature changes the Oracle signing payload. The final Oracle compact JWS string is stored in `oracle_attestation.oracle_signature`.

This construction covers chain identity, sequence, previous and current state, all action details, measurements, profile bindings, the agent signature, and all Oracle attestation metadata. It avoids self-signing: neither signature is part of its own payload, and the final record hash is computed afterward.

## Commitment, final hash, and chain head

Define `Digest(x)` as the trusted level's hash of bytes x, encoded as `sha256:` plus 64 lowercase hexadecimal digits for Levels 1 and 2, or `sha384:` plus 96 lowercase hexadecimal digits for Level 3. The record's asserted level MUST NOT select the algorithm independently of the trusted context. Newly computed v3 record, commitment, and migration bindings MUST use the algorithm required for the target level. A checkpoint's `legacy_record_hash` preserves the exact authenticated historical value and its original algorithm; it MUST NOT be relabeled as a stronger historical hash. The new archive and checkpoint bindings apply the target level's algorithm to the preserved evidence.

The proposed consensus intent is:

```text
commit_intent = Digest(JCS({
  "purpose": "ktp-trajectory-commit-v3",
  "payload": P
}))
```

Where Oracle mesh agreement is required, the external commit certificate MUST satisfy [`oracle-consensus.md`](oracle-consensus.md) and bind this intent to the full authenticated consensus context. It is not embedded in P or in either signature payload. In particular, P MUST NOT contain the digest of the certificate that commits P. Verification of a certificate requires its actual authenticated protocol evidence, not a candidate's `committed` assertion.

After the required commitment and Oracle signature, let F be the complete record, including both signature strings, excluding exactly its own `record_hash`. The final hash is `record_hash = Digest(JCS(F))`. Verifiers MUST recompute it. A record's `previous_hash` MUST reference the exact accepted final hash of its predecessor; hashing only a subset or only the unsigned body is invalid.

Before a record can become authoritative, the final head MUST be uniquely and durably anchored under the applicable Oracle agreement rules. That anchor MUST bind the agent, zone, chain, sequence, predecessor hash, final `record_hash`, and `commit_intent`. In a mesh it requires the F01 consensus contract, including durable state and valid configuration evidence. A sole mutable pointer or ordinary signature is not a substitute for the required agreement.

This final selection is necessary even when the proposed payload is already committed: valid signatures or their encodings must not create competing final hashes for one chain position. Recovery MUST recover the selected final record and anchor. It MUST NOT re-sign a committed record and silently replace the selected hash. Failure to establish the required unique head MUST pause authoritative use.

For a continuing chain, sequence MUST increase by exactly one, `previous_hash` MUST match the accepted predecessor, `previous_state` MUST equal its `current_state`, and timestamps MUST satisfy KTP-Identity's ordering rules. A genesis uses sequence zero and null predecessor hash and state. Genesis sponsorship, identity continuity, state-transition validation, and current authorization requirements remain binding; valid signatures do not waive them.

## Legacy archive and explicit migration

[`transaction-record-legacy-v2.json`](../schemas/transaction-record-legacy-v2.json) preserves the legacy schema for archive interpretation. A legacy record MUST NOT be converted, reformatted, relabeled, or re-signed and then presented as verified v3 history. A valid legacy signature does not retroactively cover fields its original signing contract omitted. Archived evidence may remain useful, but its limitations remain attached to it.

A deployment accepting v3 for authority MUST establish its accepted-format floor and cutover state outside candidate records, protected against rollback. Missing `record_version`, an old configuration, unavailable migration services, restored backups, or a caller's compatibility flag MUST NOT re-enable legacy authority. Archive inspection MUST remain distinguishable from acceptance for current authority.

Migration requires an externally authorized checkpoint, signed with the migration JWS purpose. Its payload MUST contain exactly:

```text
checkpoint_version = "ktp-trajectory-migration-v3"
checkpoint_id, agent_id, zone_id, issued_at, expires_at
legacy_chain_id, legacy_sequence, legacy_record_hash, legacy_archive_digest
new_chain_id, new_genesis_record_id, new_genesis_timestamp
conformance_level, evaluation_profile_digest
approved_state, revalidation_evidence_digest
```

The incumbent governance and identity authorities MUST authenticate the legacy lineage and exact accepted legacy head, pin the archived evidence bytes through `legacy_archive_digest`, independently establish the carried `approved_state`, and verify the referenced revalidation evidence. An asserted legacy `record_hash` alone cannot establish the integrity of previously unsigned state fields. Candidate-supplied `verified` values or fresh signatures over old assertions are insufficient. The helper can check externally authenticated facts supplied to it; it does not conduct that revalidation or establish the approvers' authority.

The new chain MUST differ from the legacy chain. The checkpoint MUST pin the exact new genesis identity, timestamp, target profile and level, and approved initial state. Issuance, expiration, and activation time MUST satisfy `issued_at <= activation_time < expires_at`, with a positive validity interval, under trusted time and policy. The target conformance level and evaluation-profile digest MUST match externally authorized migration settings. If migration also changes Oracle membership, keys, or consensus configuration, the existing authenticated F01 transition requirements still apply.

Define the migration checkpoint digest as `Digest(ASCII(the complete compact migration JWS string))`, using the new target level's algorithm. This binds the protected header, exact checkpoint payload, and signature. The new genesis body's `migration_checkpoint` MUST equal that digest; its identities, record ID, timestamp, profile, level, and `current_state` MUST exactly match the checkpoint, with sequence zero and null predecessor hash and state.

The checkpoint is signed before the new genesis and therefore does not include the final genesis hash. Once the genesis is fully signed, its exact final hash and commitment intent MUST be selected by the final-head anchoring procedure above. A checkpoint alone does not create an authoritative new chain.

Migration activation MUST atomically and durably bind the legacy lineage and accepted head to the single authorized new chain. The uniqueness check MUST cover the lineage and its migration state, not only `checkpoint_id`; another checkpoint ID, a reissued signature, a stale legacy head, or restart MUST NOT create a second migrated successor. Checkpoint expiration is checked at activation. Later verification of an already activated history uses authenticated activation evidence and MUST NOT require renewal or treat checkpoint expiration as erasing that durable lineage binding.

The migration registry, format floor, checkpoint consumption, and final head MUST survive restart, replay, and failover. If their authenticated state is unavailable, authoritative acceptance MUST stop. The old archive remains historical evidence; the migration checkpoint establishes the independently approved starting state of a new chain, not the truth or completeness of every old record.

## Verification coverage and limits

[`trajectory-signatures-v3.json`](conformance/trajectory-signatures-v3.json) contains executable cryptographic fixtures using public test keys, never production credentials. Tests MUST cover valid signatures, modification of every protected record and attestation field, incorrect key/role/profile bindings, malformed encodings, canonicalization boundaries, and altered final hashes. A test that merely recomputes an unsigned hash does not establish signature coverage.

[`trajectory-lifecycle-v3.json`](conformance/trajectory-lifecycle-v3.json) defines mandatory downstream lifecycle cases for consensus commitment, unique final heads, replay, cutover, migration, and durable recovery. The reference helper validates supported cryptography, canonical payloads, hashes, and supplied authenticated context. It does not implement a consensus engine, governance review, state revalidation service, migration registry, or production head store. Passing its tests MUST NOT be represented as verification of those external mechanisms or every Level 3 deployment requirement.

## Personal evidence storage and disposition

[privacy-evidence.md](privacy-evidence.md) defines a separate versioned encrypted
storage envelope for exact original signed bytes. Its signature does not replace
either trajectory signature, and its hash is not the trajectory `record_hash`.
Corrections and dispositions MUST be new authenticated events; signed fields
MUST NOT be redacted in place. Legacy wrapping does not erase old plaintext or
upgrade old assertions. Verification and reconstruction claims MUST state when
payloads, keys, or retained chain segments are unavailable after authorized
erasure. Retaining signed history while required does not create an indefinite
personal-data retention exemption or an erasure-based authority reset.
