# Canonical Decision Geometry

**Proposed, unreleased decision-geometry-v1 normative companion.**

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and
"MAY" are interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## 1. Portable evaluation, separate carriage

Decision Geometry is the deterministic record of the inputs actually evaluated
and the KTP supervision/constraint result. It is not a permit, PEP, execution
receipt, proof of dispatch or non-dispatch, action outcome, Flight Recorder
row, trajectory transition or counterfactual analysis. No decision verb is
stored. Products MAY derive a verb from supervision and tightened constraints;
that projection MUST NOT add permission.

[`decision-geometry.json`](../schemas/decision-geometry.json) defines the closed
unsigned body for local records. A separately purpose-typed signed carrier is
defined below for crossing trust boundaries. Signing proves integrity under an authorized
key; it does not prove that an evaluator's observations were truthful or that
a target obeyed the result.

[`transaction-record.json`](../schemas/transaction-record.json) remains a
**Trajectory Chain record, not Decision Geometry**. It describes a different
lifecycle and signed history. Storage timestamps, chain metadata, retention,
queries, enforcement telemetry, notifications, product extensions and execution
outcomes remain outside this canonical body. A product wrapper may refer to its
digest while retaining the complete canonical bytes; the wrapper is not a
second Decision Geometry format. No trajectory signature or field is changed.

## 2. Identity, profile, association and inputs

The body carries `record_version`, `decision_id`, integer NumericDate
`evaluated_at`, `ktp_release`, `evaluation_profile` (id and digest), `evaluator`,
`subject`, `actor`, `audience`, `association`, `inputs`, `undefined_inputs`,
`gates`, `result` and stable `reason_codes`. Optional fields are conditional
`capacity`, `margin`, `consumer_result`, `embedded_request` and `embedded_proof`.
Every named object is closed except the explicitly typed input value, whose
interpretation is fixed by the installed evaluation profile. All data is signed
when a carrier is used; no extension becomes an unsigned authority input.

The release identifies the immutable specification baseline for the installed
profile. An unreleased profile MUST identify itself as such; a baseline tag is
not a claim this new record format existed at that tag. The fixtures use
`v2.1.0` and a proposed named profile. The expected release, profile id/digest,
evaluator, actual requester/executor, audience and evaluation time MUST come
from independently authenticated context. The record cannot select its own
policy, trusted source, keys, evidence state or historical verification time.

The association is the exact closed value from
[request-binding-v1](request-binding.md), including complete request/proof
digests and verified jti. If binding cannot be established, use a failed binding
gate, null association and a veto result; do not invent digests or embedded
bodies. That branch is a local rejection record and cannot be used as a
cross-boundary decision prerequisite.

A passed binding gate means the actual request, complete proof bytes, identity,
issuer/audience/time and digest association were established. It does **not**
assert RB_BOUND, replay reservation success or permission: request association contract's gate/replay/
carriage checks remain mandatory for any authorizing use. A verified proof that
reports veto or undetermined can therefore support a binding-complete rejection
record whose Soul gate stops the evaluation. Invalid proof/association MUST NOT
be labeled passed. Optional embedded bodies MUST match the exact association
preimages, the actual invocation and the trusted proof, not just their labels.

Each input names `name`, `layer`, `state`, intended/actual `source`, and
`evidence_digests`. `observed`, `modeled` and `estimated` inputs require their
exact `value` and at least one resolvable authenticated evidence digest. A model
or conservative estimate MUST NOT be called an observation. `absent`,
`unanswered`, `stale` and `undefined` inputs MUST NOT carry a value masquerading
as a current measurement. A stale historical observation can be retained as
separate evidence; it is not the current input. Source identifiers alone do not
authenticate values. Record enough profile, source and evidence information to
reproduce every evaluated value; unresolved references cannot establish it.

Names/layers MUST be unique as pairs. The profile MUST fix their canonical
list order, and the record MUST preserve it; that order need not be the
chronological order of source queries. Evidence digests within an input are
lexicographically sorted; undefined_inputs follows its matching inputs order. The installed profile defines required
inputs, interpretation, units, evidence admissibility and deterministic
resolution; the record MUST cover every input actually used. Do not include
fabricated downstream outputs after an early stop. A profile with undeclared
or unverifiable required inputs cannot produce an authorizing result. The
fixture profile uses Soul, demand, capacity, Risk Factor terms and a grant
ceiling; it does not standardize formulas behind A or E.

`undefined_inputs` retains the released shape exactly: `{input, layer, state}`,
with layer `feed|signal|term|query` and state
`absent|unanswered|stale|undefined`. It is always an array, empty if none. Every
undefined input that restricted evaluation MUST have a matching entry. The
profile may distinguish modeled/estimated values from the undefined upstream
inputs that caused their conservative resolution. No unknown becomes zero by
omission. A sovereignty query that is unanswered is distinct from a witnessed
framework veto even though both stop the action.

`moment_criticality` is a separately declared demand-side input, excluded from
the five weighted Risk Factors. When used in demand classification, its
supplied value and provenance belong in the input record; the fixtures name
that input `demand.moment_criticality` to distinguish it from weighted factors.
Its presence MUST NOT add a sixth term to R or relax supplier verification.

## 3. Ordered gates and conditional result

The gate keys, in order, are `binding`, `soul`, `prior`, `inputs`, `capacity`, `envelope`,
`consumer`. Values are `passed`, `failed`, `undetermined`, `not_evaluated`, as
permitted by the branch. After a stopping gate, every later gate MUST be
`not_evaluated`; uncomputed capacity and margin MUST be absent, never null,
zero or a fabricated pass. Soul is the first substantive gate after binding.
The independent profile/key/schema validity prerequisites are not waivable by
a recorded gate value.

| Stopping branch | Required record behavior |
|---|---|
| Binding unavailable/invalid | Binding failed, association null, no later computation; silent_veto, BINDING_INVALID |
| Known Soul veto | Soul failed, later gates not_evaluated; silent_veto, SOVEREIGNTY_CONSTRAINT |
| Unresolved Soul | Soul undetermined with released undefined entry; later gates not_evaluated; silent_veto, SOVEREIGNTY_UNDETERMINED |
| Inherited veto | Prior gate failed, a sourced prior_supervision = silent_veto, later gates not_evaluated; no invented numeric failure; silent_veto, PRIOR_VETO |
| No valid finite common-scale A/E | Inputs failed/undetermined, no capacity or margin; silent_veto, INPUT_UNAVAILABLE |
| E = 0 or A > E | Capacity failed with relation zero/over; no margin or envelope/consumer calculation; silent_veto, TRUST_INSUFFICIENT |
| A = E > 0 | Capacity passed with relation within; margin zero is present; existing margin policy veto remains, consumer not_evaluated |
| Capacity check passed | Carry A, E, common unit, capacityKnown, relation within and computed margin; evaluate the installed envelope profile |

The prior gate records independently authenticated preexisting supervision and
restriction state. A known prior veto can short-circuit arithmetic without
claiming malformed or unavailable numeric inputs. Other existing supervision
levels remain floors on the produced result. Unavailable required prior state
is recorded as undefined and cannot be assumed stable.

A and E are the **validated values actually used**, not a new computation from
this schema. Demand MUST match the canonical request/classifier. Software
capacity MUST not exceed the standing supported by the verified proof or other
applicable ceilings. Estimates retain capacityKnown = false. Existing Core and
Kinetic Envelope arithmetic/order applies; this proposal adds no A/E formula.
The fixture profile uses the existing margin relation in binary64 with exact
JCS-encoded expected values; numerical conventions of another installed profile
MUST be explicit, reproducible and no more permissive at normative boundaries.

`result` is exactly `{supervision, tightenedConstraints}`. Supervision is one of
stable, metacognitive, assisted, regulated, silent_veto. A consumer can raise it
and cannot lower a prior floor. Unknown/estimated capacity clamps it to at least
assisted; it never lowers regulated or silent_veto. At an early veto,
tightenedConstraints MAY carry an empty ceiling list for no additional envelope
calculation: the veto still stops use, and existing grants/restrictions remain
in force. An empty list is not an empty set of restrictions or permission.

The constraint object uses the existing camelcase interface:
`{profile, ceilings:[{magnitude,max}]}`. Its profile MUST match the installed
evaluation profile. Magnitudes/units must be declared there, names unique,
values finite and no ceiling above the actual grant/prior envelope. Products
MUST NOT reinterpret a magnitude's direction or unit to make it looser.

Optional `consumer_result` records a tighter local projection, not a target
outcome or a second permit. Its gate is passed only when that projection was
actually evaluated. It MUST retain every producer ceiling at the same or lower
value and may only add declared restrictions; supervision cannot decrease.
A producer veto cannot be relaxed. A later consumer record can preserve the
original geometry separately; it cannot silently rewrite signed original bytes.
Stable reason codes describe evaluation only; no ALLOW/DENY/VETO/SHAPE or other
stored verb, executed flag, dispatch receipt or notification field is admitted.

## 4. Canonical body digest

Use strict UTF-8 JSON and RFC 8785 JCS with canonical Trust Proof contract's safe-integer/finite-number
restrictions, duplicate rejection, exact strings, array order and no Unicode
normalization. Incoming body JSON may differ in whitespace/key order; canonical
body bytes are JCS of the complete body, including optional embeddings and any
consumer result. No field is excluded. Integer controls use integer tokens,
not booleans or fractional spellings. Schema defaults/coercions/field removal
MUST NOT alter evaluation or the signed body.

```text
geometry_preimage = ASCII("KTP/decision-geometry-v1") || 00 || JCS(body)
geometry_digest = algorithm + ":" + lowercase_hex(H(geometry_preimage))
```

`00` is exactly one NUL byte. The installed cryptographic profile selects
SHA-256 or SHA-384, including all binding/evidence digests needed under its
strength requirements; a received prefix cannot select or downgrade it. The
preimage does not change by algorithm. This digest is different from the
trajectory record_hash, readiness digests, request digest and raw proof digest.
Never substitute one because the strings look alike.

Proposed bounds: canonical/input geometry body at most 262,144 UTF-8 bytes,
container depth at most 32, URI identifiers at most 2,048 characters and decision
ID at most 255 characters. Apply canonical Trust Proof contract/request association contract's own limits to embedded artifacts;
carrier size cannot enlarge them. Reject rather than truncate.

## 5. Signed boundary carrier

The separate payload schema is
[`decision-geometry-carrier.json`](../schemas/decision-geometry-carrier.json):

```text
{carrier_version: "decision-geometry-carrier-v1",
 geometry_digest, geometry: <complete body>, expires_at}
```

Sign exact JCS bytes of the complete payload as compact JWS. The protected
header is exactly alg, kid, typ; typ is `ktp-decision-geometry-v1` (a distinct
purpose from Trust Proofs, trajectory and readiness artifacts). The issuer is
the body's evaluator; the audience, requester and executor are carried in the
complete body and MUST match trusted actual request context. The signature
covers every gate, input/provenance/undefined state, request/proof digest and
jti, evaluation time/profile, supervision, tightened constraint and embedding.
There is no signature field in the body and no cyclic hash exclusion rule.

Reuse canonical Trust Proof contract's strict canonical JWS/base64url, algorithm/key-type/curve, low-s,
revocation and no-embedded-key rules, with the **different evaluator role and
purpose**. ES256 is the base capability; stronger installed Crypto profiles
remain binding. A trusted Oracle key is not thereby an authorized evaluator
key. The record/headers cannot appoint trust anchors or enable algorithms.
Limits: decoded header 1,024 bytes, decoded carrier payload 393,216 bytes,
complete compact JWS 524,288 ASCII bytes; depth 32. Carrier headers/payload
MUST already be JCS, not just semantically equivalent JSON.

For current cross-boundary use, require independently trusted now, healthy
clock, authorized key/role/evaluator/audience/profile, current revocation state,
a verified complete proof and request association, and recomputed geometry
digest. Require `evaluated_at <= now < expires_at`, with integer times, no
skew/grace, and expiry no later than the proof, evaluator-key validity, profile
validity or any other supporting prerequisite. Reject unbound/null association.
No carrier can extend the ordinary proof's ten-second window. Required request association contract
replay/association checks and all grants/readiness/use-time constraints still
apply; a successful carrier check does not reserve or consume execution.

For historical reconstruction, a body/signature may be verified only against
independently authenticated historical evidence/time/key/profile context. Such
verification records historical evidence and MUST NOT restore current authority.
A signed timestamp does not prove when execution happened, and a past valid
geometry does not prove an action was carried out or withheld.

## 6. Verification results and evidence limits

Reject in this order: bounded strict encoding (`DG_ENCODING`), version/closed
schema (`DG_SCHEMA`), independently expected identity/time/release/profile
(`DG_CONTEXT`), complete request/proof/embedding association (`DG_BINDING`),
input/evidence/undefined-state reproduction (`DG_INPUTS`), ordered branch and
capacity/margin result (`DG_ORDER`), then tighten-only producer/consumer result
(`DG_CONSTRAINTS`). `DG_VALID` means a valid evaluation record only.

Carrier checks precede body acceptance: encoding/header/purpose/profile
(`DG_CARRIER_FORMAT`), trusted evaluator key/role/revocation
(`DG_CARRIER_KEY`), signature (`DG_CARRIER_SIGNATURE`), closed payload and
complete geometry digest (`DG_CARRIER_BINDING`), current validity
(`DG_CARRIER_TIME`), then full body checks above. `DG_CARRIER_VALID` likewise
means a verified carrier, not an executable permit. Preserve earlier failures
and prior vetoes; never derive a later permissive result from malformed data.

[Deterministic fixtures](conformance/decision-geometry-v1.json) cover early stops,
undefined provenance, complete evaluation, capacity boundaries, tightening and
binding/schema/carrier failures, including base ES256 signatures and
SHA-256/SHA-384 golden digests. Implementations MUST validate fixture signatures,
exact preimages and declared input/result consistency against independently
authenticated profile, source and invocation contexts. These fixtures are not
evidence of complete stronger-profile support, an A/E provider, actual sensors
or classification, durable audit/replay storage, enforcement, target behavior
or independent interoperability. Evidence digests and fixture contexts model
already verified evidence; unresolved runtime inputs cannot be assumed true.
A production integration MUST implement and test the whole carrier/association
contract, including request association contract's atomic replay reservation and the target-execution evidence contract;
matching a fixture result alone is insufficient.

No first-conformance or reference implementation
claim. The migration keeps legacy records immutable without invented inputs;
ratification and the decision record remain the maintainer's.
