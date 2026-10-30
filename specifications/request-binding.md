# Ordinary Request and Trust Proof Association

**Proposed, unreleased request-binding-v1 normative companion.**

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and
"MAY" are interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## 1. Boundary and identity

A proof remains evidence, not permission. Each ordinary authorization evaluation
MUST associate the exact actual request with a complete verified
[canonical Trust Proof](trust-proof.md). A matching subject or a matching JTI
alone cannot establish that association. The association never replaces the
remaining capacity, Soul, grants, readiness, supervision or execution checks.

`subject` is the independently authenticated requester; `actor` is the software
executor. Both are explicit, including when equal. The Trust Proof's `sub`
MUST equal `actor`, never a delegator's identity or score. When subject and actor
differ, independently verify current delegation, subject eligibility where
applicable, actor authentication and the restrictive intersection of applicable
grants under the installed policy. Their strings alone establish none of this.
This profile is not a human proof format or a replacement human authorization adapter.

This is the ordinary evaluation-time association contract. It does not define
software-substrate consumption, effect budgets, queue/retry handling, target
idempotency, exactly-once execution, release-time revalidation or target-effect
evidence. The signed decision carrier is the separate [Decision Geometry decision](decision-geometry.md) (Decision Geometry (specifications/decision-geometry.md)).

## 2. Complete canonical request

[`request-binding.json`](../schemas/request-binding.json) is the closed request
body schema. The body contains exactly:

| Member | Meaning |
|---|---|
| `version` | Exact `request-binding-v1` |
| `subject`, `actor` | Authenticated requester and actual software executor |
| `audience` | Exact logical relying audience URI |
| `operation`, `resource` | Exact operation identifier URI and evaluated resource identifier URI |
| `parameters` | Complete inline object of security-relevant parameters |
| `demand` | Closed `{value, unit}`; finite value on [0,100], unit `urn:ktp:unit:action-risk-points` |
| `classification_profile` | Closed `{id, digest}` identifying the independently installed demand classifier |
| `request_id` | Unique invocation identifier within the replay domain |
| `replay_domain` | Authenticated replay-authority domain URI |

A trusted adapter MUST construct this body from the actual authenticated
invocation, executor, resolved evaluation-time resource/operation, complete
parameters and independently classified demand. It MUST NOT trust a supplied
body or digest instead of that construction. The profile identifier/digest,
unit, audience, replay domain and actual subject/actor MUST match independently
authorized context; the request cannot select its own classifier or replay scope.
This contract fixes the classifier's declared output and unit, not a formula.

Defaults that affect required authority or requested effects MUST be resolved
explicitly into parameters before binding. Omitted versus explicit parameters
are different requests; an omitted required default fails against the actual
invocation, not a guessed value. Unknown or incomplete adapter mappings MUST
fail closed. A header, display label, ambient variable, transport default or
post-binding parameter cannot change what is evaluated. All inputs capable of
changing authority or requested effect MUST be represented in the body. This
base profile admits complete inline parameters, not an unverified parameter
hash standing in for unknown content. It standardizes no new target resolver.

## 3. Canonical bytes and digest preimages

Parse strict UTF-8 JSON: reject duplicate names at every depth, invalid Unicode
including lone surrogates, nonfinite numbers and unsafe integer-valued numbers.
Apply the finite-number/safe-integer restrictions of
[complete trajectory signatures](trajectory-signatures.md). Integer-valued
numbers outside ±9007199254740991 MUST NOT be rounded into range. No coercion,
Unicode normalization, field dropping or default insertion is permitted after
construction. Preserve string contents and array order. The numeric semantics
are JCS/binary64; an adapter needing exact larger quantities MUST bind strings
with interpretation fixed by its classification profile.

Canonical bytes are **RFC 8785 JCS of the complete request body**, with no
excluded members. Input object-member order and insignificant JSON whitespace
may vary; they do not change the digest. Array order and distinct Unicode scalar
sequences do change it. Incoming requests need not already have JCS ordering;
a producer or verifier MUST derive the same JCS bytes. Ordinary sorted-key JSON
or transport serialization is not a substitute. Do not replace preserved
canonical bytes later with a second parse that has different semantics.

Let `C` be those exact UTF-8 JCS bytes and `P` be the exact complete ASCII compact
JWS Trust Proof, including both periods and the signature segment. Let `||`
mean byte concatenation. Each prefix below is literal ASCII followed by exactly
one byte `00` (NUL), with no length field or trailing newline:

```text
request_preimage = ASCII("KTP/request-binding-v1") || 00 || C
proof_preimage   = ASCII("KTP/trust-proof-v3")     || 00 || P
request_digest   = algorithm + ":" + lowercase_hex(H(request_preimage))
proof_digest     = algorithm + ":" + lowercase_hex(H(proof_preimage))
```

The independently installed cryptographic profile selects H: base SHA-256
(`sha256`), or SHA-384 (`sha384`) where required by a stronger selected profile.
Both association digests and the classification-profile digest MUST use that
selected algorithm. A candidate's digest prefix MUST NOT select or downgrade
it. No other algorithm is defined here. The profiles choose algorithm strength,
not different preimages. Decoding/re-encoding a proof, hashing only its payload,
dropping its signature, or signing it again produces a different association.

Limits in this proposed base profile: 65,536 incoming request UTF-8 bytes, 65,536 association UTF-8 bytes, and
65,536 resulting canonical bytes, container nesting depth at most 32 (root is
1), identifier URIs at most 2,048 characters and request_id at most 255 characters.
These limits do not extend Canonical Trust Proof Contract (specifications/trust-proof.md)'s proof limits. Association containers also
retain the depth-32 limit. Reject rather than truncate.

## 4. Association and proof verification

[`request-proof-association.json`](../schemas/request-proof-association.json)
defines the closed, **unsigned internal value**:

```text
{ version: "request-proof-association-v1",
  request_digest, proof_digest, proof_jti }
```

Independently reconstruct the actual canonical request and compare its complete
bytes with the supplied request's canonical bytes. Recompute both digests from
the exact inputs and compare them literally with the association. Verify the
complete proof under Canonical Trust Proof Contract (specifications/trust-proof.md)'s ordered contract and trusted key, issuer, audience,
clock, revocation, topology and profile context. The proof's audience MUST equal
the request audience; its subject MUST equal the actor. Its issuer MUST match
the expected authenticated Oracle binding. `proof_jti` MUST equal the verified
proof's jti. Do not adopt any of those expectations from the untrusted proof.

Only TP_CLEAR permits association to proceed. TP_VETO and TP_UNDETERMINED are
valid evidence but prevent an authorizing association; invalid/expired proofs
fail as well. Preserve the proof's first stable validation reason. A successful
association is only a prerequisite to evaluating this actual request. It does
not authorize even a zero-demand request or override a prior restriction.

An Oracle state proof MAY be associated with distinct requests during its valid
window, each with independently constructed canonical bytes and a fresh request
ID. Reusing its jti is not per-request permission and is not inherently replay.
Within the authenticated replay authority, a known `(proof issuer, proof jti)`
MUST identify exactly one complete proof digest. Observed conflicting bytes
under the same issuer/jti fail as `RB_JTI_COLLISION`; do not guess which is valid.

## 5. Decision carriage across a trust boundary

Within one protected process, a decision MAY retain the association as an
immutable internal value bound to the actual evaluation. An unsigned association
received from another process is only data and MUST NOT authorize an action.

Before using a decision that crosses a trust boundary, verify an approved signed
carrier that covers at least the complete request-binding digest, complete
Trust Proof digest and jti, decision time, evaluation-profile digest, supervision
and every tightened constraint. Its authenticated signer/role, issuer, audience,
subject/actor and scope MUST be authorized by installed policy and match this
association and actual evaluation. Decision validity MUST NOT outlive the proof
or other supporting prerequisites. It MUST preserve prior vetoes and tightening;
a carrier cannot change the associated request or turn missing evidence into
permission. Carrier replay and freshness obligations remain binding.

The signed [Decision Geometry carrier](decision-geometry.md#5-signed-boundary-carrier)
uses these request/proof preimages without redefining them. Verify that carrier
under the installed, reviewed profile satisfying the bindings above. If the
required verification is unavailable or fails, cross-boundary use MUST fail as
`RB_CARRIER`; an unsigned association, generic JWT, caller-supplied digest or
claimed `verified` flag is not a replacement. Local reevaluation of the actual
request with a newly verified proof remains subject to the same checks.

## 6. Replay-domain uniqueness and collisions

The active replay domain MUST be authenticated and authorized for the actual
caller, audience and operation context. A request cannot invent a domain to
escape prior state. Domain retirement/replacement requires authenticated
activation and a persistent accepted-domain floor; retired domains cannot
reappear after restart or rollback. Loss or uncertainty of required replay
state fails closed. This specifies required state properties, not a database,
replication architecture or durable retry protocol.

At association acceptance, atomically check and reserve the key
`(replay_domain, request_id)` together with the request/proof digests and
issuer/jti mapping. Competing evaluations cannot both win. A known key with
different request or proof content fails as `RB_COLLISION`; the same key and
same association fails as `RB_REPLAY`, never as cached permission. A different
proof or signature does not make an old request ID new. Preserve reservations
for the full active lifetime of the replay domain; safe bounded retention uses
an authenticated new domain and irrevocably retires the old domain before
state is discarded. Do not expire request IDs merely because their proofs end.

Distinct authorized domains separate request-ID namespaces. They do not remove
the independent issuer/jti collision check within their replay authority. A
changed classification/evaluation profile, actor, demand, resource or parameter
set requires fresh evaluation and a fresh request ID. Refreshing evidence or
receiving an equivalent request is not proof of target idempotency or an
exactly-once effect. Those guarantees require the separately installed execution profile.

## 7. Ordered association failures

Stop at the first failure in this order; never resolve a failure toward
permission. Record the stable reason and applicable underlying proof reason
in the authenticated audit record without exposing sensitive diagnostics.

| Stage | Checks in order | Stable reasons |
|---|---|---|
| 1 | Bounded strict JSON/Unicode and canonicalization | `RB_ENCODING` |
| 2 | Exact request and association version | `RB_VERSION` |
| 3 | Closed request and association schemas | `RB_SCHEMA` |
| 4 | Complete actual invocation, authenticated subject/actor/delegation, audience and replay-domain match; installed classifier/demand/unit and digest algorithm match | `RB_CONTEXT`, `RB_PROFILE` |
| 5 | Recomputed complete request/proof digests | `RB_DIGEST` |
| 6 | Canonical Trust Proof Contract (specifications/trust-proof.md) proof validation, then verified jti association, then clear gate | `RB_PROOF` (with TP reason), `RB_MATCH`, `RB_GATE` (with TP reason) |
| 7 | Protected local carriage or reviewed authenticated signed carrier | `RB_CARRIER` |
| 8 | Current authoritative replay state, request collision, exact replay, issuer/jti collision, atomic reservation | `RB_REPLAY_STATE`, `RB_COLLISION`, `RB_REPLAY`, `RB_JTI_COLLISION` |

`RB_BOUND` means only that the association prerequisite passed. A receiver MUST
NOT silently rebuild it from a different request representation or reinterpret
an invalid association as a request to use whichever proof it can find. Changes
require an explicitly new ordinary evaluation under the same complete checks.

## 8. Composition, vectors and evidence limits

Readiness decisions retain their existing purpose-specific request body and
raw-proof digest preimages in [operational readiness](operational-readiness.md).
Those `request_digest`/`proof_digest` fields are not aliases for this profile's
domain-separated digests. An adapter applying both MUST independently construct
both bindings from the same complete actual invocation and same exact proof,
and verify both contracts; matching digest labels alone is insufficient. The
readiness software subject MUST be this request's actor, not its delegating
requester. Neither
sidecar may choose different actor, operation, resolved scope or parameters, and
this association never supplies missing readiness. This profile does not revise
the existing signed readiness wire format or retroactively relabel its hashes.

[`request-binding-v1.json`](conformance/request-binding-v1.json) publishes fixed
canonical bytes/digests and request/proof substitution, Unicode, replay and
profile cases. Implementations MUST execute them against the complete signed
proof contract and their request-binding path. The modeled replay sequences
do not establish a durable/concurrent replay store, actual delegation,
classifier correctness, live keys/clocks, target effects, release-time
freshness, or the separate readiness adapter obligations. These modeled
decisions are contract prerequisites, not runtime certification.

No first implementation or reference
implementation is claimed. MIGRATION.md records the transition; DECISIONS.md
approval remains the maintainer's.
