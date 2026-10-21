# Native JSON/JWS Transport

**Proposed, unreleased ktp-json-jws-v1 transport contract.**

The key words MUST, MUST NOT, REQUIRED, SHOULD and MAY have BCP 14 meanings.

## 1. One interoperable base

Native v3 implementations MUST support the JSON/JWS base profile
`ktp-json-jws-v1`. Its `v1` versions this transport profile only. It does not
identify KTP v1, a KTP release tag, an artifact schema version or an HTTP API.
The profile is proposed until published in an immutable KTP release.

The base carries the owning artifacts without restating their members:

| Artifact | Owning contract and schema | Base representation |
| --- | --- | --- |
| Trust Proof | [trust-proof.md](trust-proof.md), [trust-proof.json](../schemas/trust-proof.json) | Exact compact JWS; bare body media type `application/ktp-trust-proof+jwt` |
| Ordinary request | [request-binding.md](request-binding.md), [request-binding.json](../schemas/request-binding.json) | Complete canonical JSON request; `application/json` |
| Request/proof association | Same contract, [request-proof-association.json](../schemas/request-proof-association.json) | Exact association value, local unsigned prerequisite; no independent authorization |
| Local Decision Geometry | [decision-geometry.md](decision-geometry.md), [decision-geometry.json](../schemas/decision-geometry.json) | Canonical JSON body; `application/json`; no execution permission |
| Boundary decision | Same contract, [decision-geometry-carrier.json](../schemas/decision-geometry-carrier.json) | Complete purpose-typed compact JWS; bare body `application/jose` |

Media types describe representation, not approval, trust or authorization.
application/jose does not choose a signing purpose or role: the independently
expected protected purpose and evaluator key binding remain mandatory. This
proposal uses an existing JWS media type and makes no new IANA registration.

An authenticated HTTP API binding MUST identify the complete canonical request,
where the exact complete proof bytes are carried, the expected response artifact,
and how the actual invocation maps to them under request-binding.md. This
proposal does not invent a request/proof wrapper, header name, server API or
new signed preimage. A JSON wrapper is usable only where an installed binding
explicitly defines it and preserves the exact JWS string. Arbitrary candidate
headers, copied claims or digests MUST NOT select the binding or supply missing
invocation context. If no complete mapping is installed, evaluation/use fails
closed; a plausible `/authorize` route is not a mapping.

Strict JSON, canonical bytes, bounds, signed NumericDates and binary encodings
follow the owning contracts. Decoding a proof for display is permitted; the
view MUST NOT become an independent authority source. A flat proof whose fields
conflict with its signed JWS MUST be rejected as a native proof envelope, even
if the JWS alone would pass. There is no native flat-proof/JWS dual authority.
Do not repair the conflict by choosing one copy or rewriting signed bytes.

The canonical result remains supervision plus `tightenedConstraints` with all
applicable prior restrictions. Enum-only authorization responses and generic
HTTP success MUST NOT substitute for it. A carrier crossing a boundary MUST
bind the complete evaluation and actual request/proof association. Signed
carriage, including a correctly typed carrier, is still not execution permission.
No callback, deferred authorization, retry, target-effect or execution-receipt
contract is defined here. Existing use-time, replay and safe-stop obligations
remain in force across all transports.

## 2. Version namespace inventory and selection

Every version-bearing token in the legacy Transport text belongs to one of
the following namespaces. Repeated route occurrences share the same rule.

| Token or family | Namespace and native-v3 treatment |
| --- | --- |
| Immutable `v2.1.0` tag | KTP specification set; historical compatibility baseline, not native-v3 negotiation |
| Installed immutable native-v3 release | KTP semantic set; fixes the owning artifact contracts; distinct from profile/API versions |
| `ktp-json-jws-v1` | Proposed base transport profile; its version is independent of the KTP set |
| `ktp.v1` protobuf package and `ktp/v1/*.proto` imports | Legacy v2.1 protobuf profile; not a native-v3 type or a rename target |
| `Sec-WebSocket-Protocol: ktp.v1` | Legacy stream binding; not native-v3 negotiation; this decision allocates no replacement stream token |
| `ktp-core-v1`, `ktp-federation-v1`, `ktp-celestial-v1` | Historical capability identifiers; none identifies the JSON/JWS base or native-v3 semantic compatibility |
| `/api/v1` and every `/v1/...` HTTP path, including `/v1/ws` and `/v1/events` | HTTP API route namespace only; may remain if independently documented; cannot select KTP semantics |
| OpenAPI `info.version: 1.0.0` | Legacy API-description version; not the KTP release or a native profile |
| Oracle status `version: 1.0.0` | Oracle implementation version; not semantic negotiation |
| Artifact versions such as `request-binding-v1`, `decision-geometry-v1`, `ktp-trust-proof-v3` | Owning artifact contracts; preserved exactly and not inferred from a route/profile suffix |

Peers MUST establish an unambiguous compatible tuple of immutable KTP release,
named/versioned transport profile and expected artifact contracts using
independently authenticated configuration or explicit authenticated negotiation.
An API version MAY also be declared but cannot stand in for any tuple member.
A bare `v1`, a route suffix, content type or old capability list is insufficient.
Unauthenticated discovery is a hint; it MUST NOT install an acceptance policy.
This table specifies semantic selection obligations, not a new negotiation wire
schema. A deployment lacking that authenticated agreement cannot claim native
artifact exchange merely because it sends JSON.

The independently installed expected tuple cannot be downgraded by a candidate
message, Accept header, subprotocol offer, peer-supplied version string or a
failed parse. Unknown profiles, conflicting artifact versions and ambiguous
selection MUST fail before authority is inferred. Lack of a compatible profile
ends native exchange rather than activating the legacy adapter. HTTP media-type
failure uses 406 or 415 as appropriate; these statuses do not replace semantic
failure handling or disclose protected internal evaluation reasons.

Notifications over WebSocket, SSE or future gRPC streams are hints rather than
fresh authority. A complete native streaming binding requires its own named
profile, envelope, authentication and interoperability vectors; it is not
created by renaming `ktp.v1`. Proof pushes retain exact signed bytes and require
current independent validation; a push, heartbeat or summary cannot refresh
old expiration or prove that a cache is current.

## 3. Retired alternatives and future profiles

The complete legacy protobuf, abbreviated OpenAPI, flat proof and authorization
enum remain accessible only through the immutable
[v2.1.0 Transport source](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-transport.md)
and migration references. Their removal from native recommendations does not
rewrite published history or assert that anybody deployed them.

A future protobuf/gRPC or OpenAPI alternative is a separate decision. Before
being used or recommended for native artifact exchange it MUST have:

1. A distinct profile identifier and independent version, published at an
   immutable release, with its supported KTP releases/artifact contracts.
2. Complete machine-readable artifacts, including every required schema and
   service/envelope mapping; an abbreviated appendix or missing external file
   cannot satisfy this requirement.
3. Deterministic lossless mappings to the owning canonical schemas, exact
   signed JWS bytes, five named weighted factors, independent Soul gate and
   normative supervision plus tightened constraints. A translated display
   MUST NOT become a second signed authority object.
4. Positive and negative interoperability vectors for complete signatures,
   all nested bindings, omitted/default/unknown/duplicate fields, invalid
   numbers, version confusion, veto preservation and constraint preservation.
5. A named builder and evidence identifying what was specified, executed and
   independently reproduced; schema/vector publication alone establishes no
   working implementation.

Changing `ktp.v1` to `ktp.v3`, changing field names or translating an enum is
insufficient. No new protobuf, OpenAPI service, optional encoding assurance or
implementation is offered here. CBOR likewise cannot be used to reinterpret
proof/request/decision artifacts without a separately versioned mapping;
independent non-authority sensor telemetry is outside that artifact mapping.

## 4. Negotiated migration and vectors

A legacy v2.1 adapter MAY remain only when explicitly enabled, identified as
legacy and isolated from native acceptance. It MUST NOT activate after native
validation or negotiation fails. It MUST NOT label a legacy R, proof or enum
result as the native artifact. Preserve stored legacy bytes, signatures and
release provenance. Migration requires fresh native issuance and evaluation of
the actual request under current constraints; field copying cannot mint missing
Soul, association, supervision or constraint evidence. No in-flight legacy
permission is carried forward as native authority.

[native-transport-v1.json](conformance/native-transport-v1.json) publishes
modeled selection, rejection and migration requirements, including retired
factor objects, enum-only results, conflicting flat/JWS fields and ambiguous
version negotiation. References select complete existing fixtures; placeholders
are never native proof bytes. Fixture notation is not a new wire schema.
Implementers MUST run the cases on their actual adapters and exercise the
complete owning suites; this repository publishes no transport implementation.
These vectors do not establish actual network interoperability, key custody,
authenticated negotiation, enforcement, durable replay or successful migration.

No first builder or public reference
implementation is claimed. Maintainer ratification remains separate.
