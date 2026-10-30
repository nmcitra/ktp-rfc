# Per-operation Demand Supplier Contract

**Unreleased demand supplier contract.**

`moment_criticality` is a declared demand-side input, never a weighted Risk
Factor. The Risk Factor aggregates five weighted inputs; this contract adds
no formula for A, R or E.

The key words MUST, MUST NOT, REQUIRED, SHOULD and MAY have BCP 14 meanings.

## 1. Declared supplier, optional activation

A deployment that uses `moment_criticality` MUST install its complete declaration
under `demand_inputs.moment_criticality` in the deployment profile. A deployment
that uses none may omit demand_inputs under [Core L14](../rfc-src/ktp-core.md#l14-the-criticality-of-the-moment-is-a-demand-side-input-and-the-specification-says-so). Omission is not a way to
ignore an input required for an actual operation: that required but undeclared
input is unavailable and receives the restrictive reading below.

The closed [declaration schema](../schemas/demand-input-contract.json) requires:

- `supplier`: stable identity of the authorized supplying party, independently
  established to be neither the requester nor a party acting for it.
- `supplier_profile`: stable profile URI and SHA-256/SHA-384 digest of its exact
  canonical RFC 8785 profile payload. It fixes the supplier's scale, source
  interpretation and declared production contract; no production formula is
  standardized here.
- `unit` and `range`: the named common unit convention and inclusive [0,1]
  native criticality range, where 1 is the most critical moment. Values from
  different conventions MUST NOT be silently converted or compared.
- `source`: the configured supplier feed/system/record, not a candidate-selected
  endpoint or arbitrary Context Signal.
- `freshness`: authenticated UTC clock, observed_at basis, and positive
  max_age_seconds within the JSON safe-integer range. Its age limit is the
  deployment's declared decision; this contract prescribes no production value.
- `verification_profile`: stable profile URI and canonical payload digest
  fixing approved issuer roles/keys, signatures or authenticated-channel
  evidence, provenance checks, source access and current revocation rules.
- `authoritative_location: demand-input-value-v1`: the complete value payload
  defined below is the authoritative record, not a copied request field,
  catalogue signal, optional logging annotation or unbound scalar.

The installed declaration, supplier and verification profiles MUST be approved
and authenticated independently of the operation candidate. Profile digests
bind exact configuration; they do not establish its trustworthiness. A profile
change increments the deployment version and invalidates values bound to the
old deployment digest. The declaration digest is the independently selected
SHA-256/SHA-384 hash of the entire RFC 8785 deployment-profile payload, excluding
any outer signature envelope. Candidate-selected algorithms or downgrade are
forbidden. The declaration MUST NOT contain signals, aggregation or weight.
Five ordinary factors keep their signal aggregation shape and unit-sum rule.

## 2. Authoritative supplied-value payload

[demand-input-value.json](../schemas/demand-input-value.json) defines the closed
payload: value_version, input, supplier, supplier_profile, declaration_digest,
unit, value, observed_at, issued_at, provenance and operation_digest. The input
is moment_criticality; no arbitrary additional factor is created.

The verification profile MUST authenticate the complete payload, including all
nested profile/provenance/digest fields, against its independently installed
supplier/source bindings. It fixes the exact signature/channel encoding; this
proposal defines no universal production signing envelope. An unprotected value
or a candidate's assertion that a signature passed is insufficient. Missing
approved encoding or verification context makes the value unavailable.

Values MUST be acquired or independently corroborated through the declared
supplier path. A requester relay, even of plausible signed bytes, cannot alone
establish that path or supplier independence. A caller may name a value for
lookup, but cannot supply its authority or choose a verifier. Supplier acting-
for relationships require independently established context, not a string test.

`observed_at` and `issued_at` are integer NumericDates on the declared clock.
Required time conditions are observed_at <= issued_at <= evaluation_time and
0 <= evaluation_time - observed_at <= max_age_seconds. The exact maximum-age
boundary is accepted; the next instant is stale. Unknown/unhealthy clock,
future observation or issuance, negative age, missing times and exceeded age
make the value unavailable. A newer signature/issued_at MUST NOT refresh an
old observation. There is no additional clock-skew allowance.

`provenance` carries an identifying URI and digest of the complete referenced
evidence bytes. Verification MUST establish those bytes, their authorized
source, meaning and current admissibility under the installed profile; a URI,
JSON schema pass or digest alone is insufficient. Neither missing provenance
nor supplier/profile/units/declaration mismatch can be interpreted as a valid
low-criticality reading. Booleans, nonfinite numbers and out-of-range values
are invalid, never clamped into a plausible measurement.

## 3. Exact preclassification operation binding

[demand-operation.json](../schemas/demand-operation.json) fixes the complete
operation descriptor before final demand computation: actual authenticated
subject/requester, actor/executor, audience, operation, resolved resource,
complete security-relevant parameters with explicit defaults, request_id and
replay_domain. Actor/subject may coincide; delegation remains an independent
prerequisite. Include resolved scope, tool/target choices and implicit defaults
in parameters wherever they affect the actual operation. A candidate digest,
partial action name or session identity cannot substitute for this descriptor.

The trusted adapter and supplier construct the same descriptor from the actual
invocation. Security-relevant invocation data that cannot be represented or
whose authoritative resolution is unknown makes binding unavailable. A changed
resource, parameter/default, identity, audience, operation, request id or replay
domain changes the binding. The complete deployment digest separately binds the
installed classification and supplier policy.

The operation digest is H(ASCII("KTP/demand-operation-v1") || NUL || JCS(complete
descriptor)), with H selected independently by installed cryptographic policy.
Only strict UTF-8 JSON, unique member names, finite numbers and RFC 8785 safe
integer/canonicalization rules are accepted. Property order/whitespace have no
semantic effect; do not normalize Unicode strings or collapse explicit values.
The exact preimage includes one zero byte after the ASCII prefix.

The descriptor deliberately excludes the supplied criticality value and final
computed A: hashing either into the input needed to compute A would be circular.
A later canonical authorization request MUST independently bind its final
classified demand and the same resolved invocation fields. Where canonical request association is
composed, construct both bindings from that single actual invocation; the
preclassification digest does not replace the complete canonical request/proof digest,
replay reservation or use-time checks. See [Core Section 6.6](../rfc-src/ktp-core.md#66-decision-contract) for the decision contract.

Digest matching admits a value only for evaluation of that exact operation.
It is not a capability, replay reservation, dispatch promise or execution
receipt. Missing actual invocation data cannot be supplied by the value itself.

## 4. Restrictive evaluation and record

After declaration, supplier, complete authentication, provenance, time and
operation binding pass, consume the supplied value only on the demand or
supervision side under [Core L14](../rfc-src/ktp-core.md#l14-the-criticality-of-the-moment-is-a-demand-side-input-and-the-specification-says-so). It MUST NOT enter R, change E_base or
E_trust, lower A, lower existing supervision, remove constraints or reverse
Soul/capacity/prior vetoes. No Context Signal subset is fabricated for it.

An absent, stale, unverifiable, differently bound, improperly sourced or otherwise
invalid value is unavailable: read the required input as the most critical
moment (1 in the native declared range). This is a restrictive decision reading,
not a fabricated observed value. Preserve the unavailable state, cause and
provenance in the evaluation record; do not replace the signed payload with 1
or represent 1 as the supplier's observation. The producer's original bytes
remain immutable. In `undefined_inputs`, record `layer: term`,
`input: moment_criticality`, and `state: absent`, `unanswered`, `stale` or
`undefined` according to the actual cause: missing input, no usable answer,
expired observation, or failed validation/binding respectively.

Evaluation may proceed with that restrictive reading only if the installed
contract can establish a finite conservative demand on the common scale.
Otherwise deny execution under Core's undefined-input rule. Neither a missing
supplier declaration nor an invalid profile permits silent disabling, a calm
zero, reuse of an old value or fallback to a requester-provided alternative.
The largest reading does not itself grant permission or require executing an
operation. Existing grants, proofs, readiness, replay and all vetoes remain due.

Record the exact declaration/supplier/verification profile bindings, complete
value evidence or its absence, provenance outcome, evaluation time and operation
digest, accepted/unavailable status and restrictive reading separately from the
observed scalar. Where Decision Geometry is composed, use its existing input,
undefined-state, source/evidence and gate fields; do not invent a second result
schema or weaken its record/carrier contract.

## 5. Migration, vectors and evidence limits

[demand-supplier-v1.json](conformance/demand-supplier-v1.json) complements the Core demand-input
[demand-input-v1.json](conformance/demand-input-v1.json) with complete declaration,
operation, signed test value, golden SHA-256/SHA-384 preimages, and positive/
negative supplier, time, provenance and operation-binding cases. Its signing
profile and unsafe public test key are fixture-only, not a production envelope.
These are modeled boundary requirements, not supplier authentication or runtime
certification. Implementations must exercise the actual supplier/verifier path.

Migrate generic six-factor declarations under [Core L14](../rfc-src/ktp-core.md#l14-the-criticality-of-the-moment-is-a-demand-side-input-and-the-specification-says-so), then install the
complete supplier contract and new deployment digest. Reacquire and authenticate
per-operation values under that configuration; never rename catalogue signals
or old request-supplied scalars into valid demand evidence. Historical profiles,
values and signatures remain under their original release. Explicit legacy
handling cannot bypass the new active declaration and binding requirements.

Schemas and external fixture checks still do not establish supplier independence, live clocks,
provenance truth, calibration or actual enforcement. No public reference
implementation or first-conformance claim is offered.
