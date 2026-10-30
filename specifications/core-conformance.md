# One Core, Three Conformance Levels

**Native-v3 common Core contract.**

The key words MUST, MUST NOT, SHOULD and MAY have their BCP 14 meanings.

## Common semantic identity

Basic, Standard and Full MUST use the same Core contract. The following are
inherited requirements at every level, never additional features of a level:

- All five named weighted Risk Factors: `evidence_density`, `trust_trend`,
  `adversarial_pressure`, `update_resistance`, and
  `attestation_coverage`. Weight validation, normalization
  and restrictive undefined-input handling follow KTP-Core. Missing inputs
  MUST NOT silently become a reduced-factor calculation or fabricated zeros.
- Declared demand-side `moment_criticality` follows KTP-Core L14;
  it raises A only and MUST NOT enter R or the weighted input population.
- The independent Soul veto, evaluated before capacity, MUST NOT be weighted
  into R or offset by favorable measurements. Prior vetoes remain binding.
- Core standing, Proof of Resilience, lineage and tier semantics, including
  applicable sponsored-agent limits. A static assignment or level-specific
  tier table MUST NOT replace the native contract.
- The same Core input/output and Kinetic Envelope decision contract, including
  the unconditional capacity gate, declared valid thresholds, supervision and
  `tightenedConstraints`. Derived action verbs cannot add permission.
- The [canonical Trust Proof](trust-proof.md), including required and
  conditional claims, gate state, issuer/audience binding, time checks and the
  ten-second maximum lifetime. An unavailable input cannot become authorizing
  merely because Basic has fewer sensors. A level adds no alternative proof
  shape or interpretation.
- The [ordinary request association](request-binding.md) and canonical
  [Decision Geometry](decision-geometry.md) where those artifacts are used;
  a level introduces neither a second record shape nor an execution permit.

The authoritative calculations and gates remain in KTP-Core and the
[Kinetic Envelope](kinetic-envelope.md); this document adds no formula for A
or E. The level label MUST NOT select weights, thresholds, defaults, input
interpretations or a different output type.

For identical complete Core inputs, installed semantic profile, evidence state,
evaluation time and prior constraints, the Core result MUST be identical at
all three levels. A deployment MAY install a stricter policy or have different
evidence availability; those are changed inputs or additional execution gates,
not exceptions to this invariant. Additional constraints MUST compose
restrictively and MUST NOT overwrite the underlying Core result or remove a
veto. If constraints cannot be composed safely, execution is denied.

## Assurance differences

Levels retain their specified differences in redundancy, reviewed consensus,
threshold signing, key protection, audit durability, replication, federation,
performance, resilience and independent review. A single Oracle is still
permitted at Basic; that does not remove any Core gate. A threshold-signing
configuration is not evidence of Byzantine agreement.

A stronger installed assurance profile MAY shorten proof acceptance or require
stronger named algorithms. It MUST NOT lengthen Core's maximum lifetime,
extend expiration during outages, change signed claims or accept a proof
failing the canonical contract. Shorter acceptance is an additional gate and
can deny an otherwise valid Core result; it does not reinterpret that result.

Component-only claims are specified separately in `specifications/component-conformance.md`.

## Immutable baseline and migration mapping

| v2.1.0 requirement or permission | Native-v3 requirement at every level | Migration consequence |
| --- | --- | --- |
| Basic minimum three weighted inputs | All five, with Core validity and undefined-input rules | Supply all five or apply Core's restrictive missing-input path; never renormalize a reduced model into native R |
| Basic excludes Soul | Independent mandatory Soul gate | Add the gate before capacity; favorable standing cannot offset it |
| Basic binary result and no tiers | Supervision plus `tightenedConstraints`, all five Core tiers | A field rename or allow/deny wrapper is insufficient |
| Basic simplified static E_base | Core standing and applicable lineage/PoR constraints | Replace the shortcut before claiming native v3 |
| Basic maximum sixty-second proof | Canonical proof with maximum ten-second lifetime | Reissue under the new contract; do not relabel old bytes |
| Standard ten-second proof with fuller fields | Same canonical proof as every level | Migrate legacy fields and signatures; retain additional signing assurance |
| Full additional formats/algorithms | Same canonical base artifact with named stronger profiles | Do not treat a Full label as a new wire format or algorithm negotiation |
| Higher-level Soul and complete-input tests | Common Core tests run at every level | Move semantic prerequisites into inherited Basic coverage |
| Single Oracle versus replicated mesh; chained/anchored audit | Deployment assurance differences remain | Evidence for those claims is still required separately |

The historical reduced Basic contract keeps identity `legacy-v2.1-basic`,
interpreted under the immutable v2.1.0 release. It MUST NOT claim native-v3
Basic conformance, and its R, proof and binary result MUST NOT be accepted as
native Core artifacts. A verifier expecting native v3 MUST reject that legacy
identity or explicitly route it to a separately authorized legacy verifier;
no automatic fallback or renaming is permitted. Historical artifacts retain
their original release meaning; this contract does not invalidate that history.

A continuing reduced model outside that historical contract MUST publish a
separately named profile, schema and media type before use. This contract
assigns none. Such a profile MUST NOT claim its R, proof or result is the native
Core artifact; no gateway can gain native authority by copying its fields.

## Vectors and evidence limits

[core-levels-v1.json](conformance/core-levels-v1.json) specifies common boundary
requirements at Basic, Standard and Full. Test notation is not a new wire
schema. Each implementation MUST execute the cases against its actual Core
path for each claimed deployment level, using identical installed semantic
profiles. The complete referenced capacity/proof suites and applicable Core
provider vectors remain required; the cases here do not replace them.

The vectors specify cross-level equality of expectations and reference the
existing capacity boundaries. This repository does not execute a Core provider,
certify assurance bundles or prove runtime interoperability.
Claim status MUST use KTP-CONFORMANCE “Claim Status” as defined in
[source proposal #166](https://github.com/nmcitra/ktp-rfc/issues/166);
schema and vector checks alone do not establish a stronger claim status.
