# Canonical Trust Proof Contract

**Proposed, unreleased native-v3 normative companion.**

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and
"MAY" are interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## 1. Purpose and authority

A Trust Proof is an Oracle's signed, short-lived assertion about a software
agent's standing and environmental gate state. It is not an action capability
or a human eligibility credential. A valid proof can report `clear`, `veto`,
or `undetermined`; only `clear` permits the relying component to continue the
remaining authorization checks. It never grants execution by itself. The
actual request, capacity, Soul constraints, grants, readiness, topology,
revocations and applicable deployment policy MUST still be checked at execution.
Request association and Decision Geometry are separate decisions (request association contract/Decision Geometry contract).

This document and [`trust-proof.json`](../schemas/trust-proof.json) are the
single native v3 wire contract for every conformance level. The schema fixes
shape; this text fixes verification order and semantic conditions. An
implementation MUST satisfy both. No additional wire claim can become standard
through a copied example. This profile supplies no formula for A or E.

## 2. Envelope, algorithms and trusted context

The media type is `application/ktp-trust-proof+jwt`; the protected `typ` is
exactly `ktp-trust-proof+jwt`. Use the compact JWS serialization of
[RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html), with exactly three
nonempty, unpadded canonical base64url segments and an embedded payload. The
protected header contains exactly `alg`, `kid`, `typ`, all nonempty strings.
No other header member, detached/unencoded/compressed payload, embedded key,
remote key locator, shared-secret signature or `none` algorithm is permitted.

ES256 (P-256/SHA-256) is the mandatory base interoperability capability.
Additional algorithms require an independently installed, named cryptographic
profile authorizing the exact algorithm, curve and Oracle role; a candidate
proof cannot enable one. For Ed25519 the JOSE identifier is `EdDSA`, never
`Ed25519`. An EdDSA profile MUST bind the exact curve, not merely that label.
The per-level algorithm floors in KTP-CONFORMANCE's Signature Algorithms
section still apply: a required additional algorithm requires its named
profile at that level, and a recommended algorithm's profile stays recommended.
Stronger deployment requirements, threshold participation, mesh committed-state
evidence and Crypto key-custody rules remain prerequisites; base verification
MUST NOT be presented as satisfying a stronger selected profile. Threshold
metadata does not prove participation or consensus.

Before parsing a proof for authority, obtain the expected issuer, subject,
audience, issuing zone, trusted current time and clock-health state, installed
cryptographic profile, authorized keys and their role/validity/revocation state,
accepted extension handlers, and authorized topology from authenticated local
configuration/state. Unavailable required state MUST fail closed. A `kid` is
an exact local lookup hint, never permission to retrieve keys from the proof.
The key binding MUST authorize this Oracle issuer, zone and signing purpose,
with validity covering issuance through expiry; known revocation wins.

Header and payload bytes MUST be strict UTF-8, duplicate-free JSON objects in
[RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html) form. Reuse the
strict scalar, finite-number and safe-integer input restrictions of
[complete trajectory signatures](trajectory-signatures.md), without adopting
that artifact's `typ` or timestamp format. No normalization, coercion, default
insertion, field dropping or reparsing into different values is permitted.
Reject lone surrogates, nonfinite values and integer-valued numbers outside
`[-9007199254740991, 9007199254740991]`. Integer controls use integer tokens,
never booleans or floating-point tokens. Limits: 65,536 ASCII wire bytes for
the complete compact JWS, 1,024 decoded header bytes, 49,152 decoded payload
bytes and a maximum JSON container nesting depth of 32 (the root counts as 1).
Larger artifacts require a separately decided profile change, not truncation.

ECDSA uses fixed-width unsigned `R || S` per
[RFC 7518](https://www.rfc-editor.org/rfc/rfc7518.html), not DER, with the
existing Crypto low-s rule. For ES256 the signature is 64 bytes;
`0 < r < n` and `0 < s <= floor(n/2)`. Verify the original compact signing
input, never a reconstructed payload. The published fixtures contain public
TEST keys only; they MUST NOT be trusted by a deployment.

## 3. Claims and conditional shape

The schema `$id` is `https://kinetic-trust-protocol.net/specs/schemas/v3/trust-proof.json`.
Required JWT claims are `iss`, `sub`, `aud`, `iat`, `exp`, `jti`, `ktp`.
`aud` is one exact URI string, not a wildcard or array. `nbf` is optional and,
if present, MUST equal `iat`. `extensions` is the only optional top-level
extension container. All other top-level members are rejected.

`ktp.version` is `ktp-trust-proof-v3`. Required KTP members, their ranges,
optional telemetry, Soul object and conditional branches are defined once by
the schema. `context` contains the five weighted Risk Factor inputs. `moment_criticality`
is a declared demand-side input, never a member of context or a term in R. It references the existing Risk Factor and Soul
schemas by their absolute v2 `$id`s so moving this schema to v3 cannot change
what those references resolve to.

`generation` is required: sponsored 0–2, independent 3–6, guarantor 7 or more.
`sub` MUST identify the same lineage, and a generation encoded in an independent
or guarantor identifier MUST equal the claim. Full identifier grammar and bond
binding remain KTP-IDENTITY/identifier contract; no identity registry is introduced here.
`sponsor` is required only for sponsored lineage and prohibited otherwise.
Optional `resilience_hash`, velocity, volatility and quorum telemetry cannot
replace independently verified standing or authority.

The closed `root_instrument` object is always present. `current` and
`non_renewable` require integer `end_time`; the proof MUST NOT outlive it.
`none` contains only `status`, with no invented instrument details. Other
existing declared fields remain available for active instruments. The complete
variant/lifecycle contract and projection remain External Root projection contract; these shape checks do
not authenticate an external instrument or its capacity.

`applicable_ceilings` is a nonempty list of closed ceiling/value objects. Names
MUST be unique. When numeric, E_base MUST NOT exceed any declared ceiling, and
E_trust MUST NOT exceed E_base. Verifiers MUST additionally establish the list
contains every ceiling required by their installed policy, with its exact
authenticated value, including the existing generation ceiling (25, 35, 45,
55, 65, 75, 85 for generations 0–6; 100 thereafter). A proof cannot
choose a weaker policy by omitting a ceiling. This contract does not prescribe
the scoring computation or assert numerical equality to any formula.

### Gate states

| `gate_state` | Required evidence shape | Meaning after all prior stages pass |
|---|---|---|
| `clear` | Numeric E_base, E_trust, R; complete numeric context; Soul object with `soul = 0` | Continue authorization; no permission is granted |
| `veto` | Soul object with `soul = 1`; unknown scores/context may be null | Authenticated sovereignty veto; deny execution |
| `undetermined` | E_trust is null; Soul is null or a clear Soul object; other unknown measurements may be null | No usable authorizing standing; deny execution |

A known Soul veto MUST be encoded as `veto`, never hidden as `undetermined`.
A numeric zero is a measurement, never a substitute for missing evidence.
Nulls admitted for veto/undetermined are statements of unavailable evidence,
not a change to Risk Factor missing-evidence propagation (missing-evidence contract). A capacity
failure for an actual action is evaluated by the relying component, not
represented here by changing the meaning of the Soul bit.

### Standard nested-zone claim

`ktp.ingress_path` is a standard optional claim, not an extension. Its closed
receipt shape is inherited from proposed nested-zone contract/nested-zone receipt contract: at most five receipts,
outermost first, each carrying `zone_id`, `oracle_kid`, `sub`, `cnf_jkt`, `aud`,
`prev`, `topology_epoch`, `iat`, `exp`, `admission_id`, `sig`. At a ring of
authorized depth d > 0, exactly d receipts are required; at depth 0 the member
is absent, not an empty path. Depth MUST come from the authenticated Topology,
never from path presence. Verify receipt signatures, ancestry, links, epoch,
subject, possession-key/session bindings, audiences and current validity under
KTP-ZONES/nested-zone receipt contract before accepting the proof for further authorization. Shape
alone is insufficient. If that verification is unavailable, fail closed at
`TP_INGRESS`; nested-zone verification remains mandatory when the installed topology requires it.

### Extensions

`extensions` maps absolute namespace URIs to exactly `{ "critical": boolean,
"value": <JSON value> }`. The complete container is signed. The installed
profile, not the proof, selects understood namespaces and their handlers.
Unknown critical entries MUST fail with `TP_EXTENSION_CRITICAL`. Unknown
noncritical entries MUST be ignored for decisions while preserving their exact
signed data. A recognized handler's failed validation fails at that same stage.
Extensions MUST NOT override any standard claim, suppress a failure, weaken a
veto, replace required evidence or enable an algorithm. There are no standard
extension namespaces in this base profile.

## 4. Time

`iat`, `exp`, and optional `nbf` are nonnegative safe integer NumericDates.
Require `0 < exp - iat <= 10`, and `iat <= now < exp`. At `now == exp` the
proof is expired. Maximum accepted clock skew is **zero seconds**. If supplied,
`nbf == iat` is required. A named profile MAY shorten lifetime but MUST NOT
lengthen it or add expiry grace. An untrusted clock, rollback that could revive
expired authority, missing current revocation state or unverifiable validity
MUST prevent use. Sessions, cache entries, queued requests, enclosing tokens,
refresh attempts, outages and emergency declarations cannot extend this window.
Revalidate at execution and during continuing protected operation; retain the
existing bounded safe-stop and separately authorized emergency requirements.

## 5. Ordered verification and stable reasons

Evaluate in this exact order and stop at the first failed condition. Never
return a later-stage reason based on unauthenticated data. Structural parsing
at stage 1 is not acceptance of claims. Reasons are stable protocol identifiers;
applications MAY map them to their existing denial envelope but MUST preserve
the stage/reason in the authenticated audit record. Avoid sensitive diagnostics
on public interfaces. A structurally missing/malformed issuer, audience or time
claim fails at stage 5, before general schema checks.

| Stage | Checks in order | Failure reasons in that order |
|---|---|---|
| 1 | Compact type, size, segment encoding; strict bounded JSON/JCS objects | `TP_FORMAT` |
| 2 | Exact protected `typ`; installed allowed `alg`; exact header member set/types | `TP_TYPE`, `TP_ALGORITHM`, `TP_HEADER` |
| 3 | Trusted `kid`; current revocation; Oracle issuer/zone/purpose role; bound algorithm/key type/curve | `TP_KEY_UNTRUSTED`, `TP_KEY_REVOKED`, `TP_KEY_ROLE`, `TP_KEY_ALGORITHM` |
| 4 | Raw signature encoding, low-s and cryptographic signature | `TP_SIGNATURE` |
| 5 | Exact expected issuer; audience; integer dates, trusted clock, key interval, lifetime and current validity | `TP_ISSUER`, `TP_AUDIENCE`, `TP_TIME` |
| 6 | Closed schema, integer controls and conditional claims; critical extension processing | `TP_SCHEMA`, `TP_EXTENSION_CRITICAL` |
| 7 | Subject/zone/lineage/generation, trust/ceiling/root invariants; required ingress verification | `TP_INVARIANT`, `TP_INGRESS` |
| 8 | Gate state | `TP_CLEAR`, `TP_VETO`, `TP_UNDETERMINED` |

A stage 1–7 failure yields an invalid proof and denial. `TP_VETO` and
`TP_UNDETERMINED` mean a valid signed assertion whose gate prevents execution;
they MUST NOT be confused with an invalid signature. `TP_CLEAR` means only
that the complete remaining action authorization can be attempted. No stage
may undo an earlier failure or a veto from another prerequisite.

## 6. Fixtures, integration and evidence limits

[`trust-proof-v3.json`](conformance/trust-proof-v3.json) publishes complete
signed compact JWS bytes, public test key bindings, independently supplied
verification contexts, and exact expected stage/reason/gate outcomes. Negative
cases are either newly signed mutations or explicit damaged envelopes; the
case description distinguishes them. Fixed fixture bytes are authoritative;
regenerating an equivalent ECDSA signature is not required. Test keys are
publicly reproducible and unsafe outside this suite. Implementations MUST test
ES256 base verification and the named test Ed25519 profile against these
fixtures. This repository publishes the contract and vectors, not an executable
verifier or a designated reference implementation. The fixtures do not
establish runtime consensus, trusted clocks, key custody, topology
receipt cryptography, profile approval, current operational capacity, request
association, replay protection or independent interoperability. Nontrivial
nested-zone acceptance remains dependent on nested-zone receipt contract's own vectors and checks.
All stronger deployment obligations remain. Schema/vector success is modeled
contract evidence, never runtime certification.

Core, Crypto, Transport, Enforce and Conformance cite this contract and its
fixtures. Decoded REST/protobuf/CBOR views or copied summary claims cannot
replace the exact signed native compact JWS. Historical Transport v1 sketches
remain legacy descriptions pending native Transport contract; they are not alternative v3 shapes.

No first implementation or reference implementation is claimed. Migration is
recorded in MIGRATION.md; the decision record remains the maintainer's.
