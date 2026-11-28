# JSON Schemas

This section contains the JSON schemas for the Kinetic Trust Protocol.

!!! info "Draft schemas — contributors welcome"
    These schemas are in active draft. If you spot gaps or have suggestions, please open an issue or PR (see [Contributing](https://github.com/nmcitra/ktp-rfc/blob/main/CONTRIBUTING.md)) to collaborate on the structure and fields.

## Available Schemas

Each file sits beside this page, so the listing cannot drift from the
directory. The `$id` of each schema is its canonical URL; these links resolve
the source.

| Schema | File | What it constrains |
|---|---|---|
| Risk Factors v3 (unreleased) | [`risk-factors.json`](risk-factors.json) | The five weighted inputs and the Soul veto, as one scored object |
| Legacy Risk Factors v2 | [`risk-factors-legacy-v2.json`](risk-factors-legacy-v2.json) | Byte-preserved published schema with six weighted inputs, for interpreting v2 proofs and records |
| Root Instrument v1 (proposed) | [`root-instrument.json`](root-instrument.json) | Closed none/bond/attestation proof projection; signatures, lifecycle, lineage and strongest-single selection remain independent checks |
| Component Claim v1 (proposed) | [`component-claim.json`](component-claim.json) | Closed implementer-owned role/build/declaration/tagged-suite metadata; component evidence rules in specifications/component-conformance.md |
| Trust Proof v3 (proposed) | [`trust-proof.json`](trust-proof.json) | Closed canonical Oracle standing assertion; ordered verification and semantics in specifications/trust-proof.md |
| Legacy Trust Proof v2 | [`trust-proof-legacy-v2.json`](trust-proof-legacy-v2.json) | Byte-preserved published schema for interpreting v2 proofs, whose context carries six inputs |
| Evidence State v1 (proposed) | [`evidence-state.json`](evidence-state.json) | Closed per-layer current/unavailable, populated/unknown and observable/unobservable outcomes; restrictive stress is not a measurement |
| Ordinary Request Binding v1 (proposed) | [`request-binding.json`](request-binding.json) | Closed complete ordinary request; requester/executor, demand profile, parameters and replay domain |
| Request/Proof Association v1 (proposed) | [`request-proof-association.json`](request-proof-association.json) | Unsigned request/proof digest and JTI association; no standalone authorization or signed carrier |
| Decision Geometry v1 (proposed) | [`decision-geometry.json`](decision-geometry.json) | Closed portable deterministic evaluation; inputs, undefined states, gates, supervision and tightened constraints; not a permit or execution outcome |
| Decision Geometry Carrier v1 (proposed) | [`decision-geometry-carrier.json`](decision-geometry-carrier.json) | Complete payload of the purpose-typed signed boundary carrier; no independent execution authority |
| Demand Input Contract v1 (proposed) | [`demand-input-contract.json`](demand-input-contract.json) | Closed independently supplied demand declaration; no factor weight or Context Signals |
| Demand Operation v1 (proposed) | [`demand-operation.json`](demand-operation.json) | Exact actual invocation before criticality and final demand calculation |
| Demand Input Value v1 (proposed) | [`demand-input-value.json`](demand-input-value.json) | Authoritative value payload bound to supplier/profiles, time, provenance and actual operation; authentication remains separate |
| Consequential-action evidence (unreleased) | [`consequential-action-evidence.json`](consequential-action-evidence.json) | Correlation shape for request, consumed decision, reservation and observation; authentication and target effects require independent verification |
| Deployment Profile v3 (unreleased) | [`deployment-profile.json`](deployment-profile.json) | Deployment declarations including the mandatory historical-evidence/current-readiness policy binding and explicit human-eligibility profile binding |
| Legacy Deployment Profile v2 | [`deployment-profile-legacy-v2.json`](deployment-profile-legacy-v2.json) | Byte-preserved published schema for interpreting old profiles; no readiness acceptance path |
| Hand-Back (unreleased) | [`hand-back.json`](hand-back.json) | The typed destination of an adverse stop inside a managed relation: recipient, recourse, repair, reissue bound, sealed context |
| Hand-Back (unreleased) | [`hand-back.json`](hand-back.json) | The typed destination of an adverse stop inside a managed relation: recipient, recourse, repair, reissue bound, sealed context |
| Readiness Profile v1 (unreleased) | [`readiness-profile.json`](readiness-profile.json) | Exact assessment criteria, scopes, authorized assessors and bounded evidence age |
| Readiness Attestation v1 (unreleased) | [`readiness-attestation.json`](readiness-attestation.json) | Complete signed assessment, subject configuration, scope, challenge and observations |
| Readiness Decision v1 (unreleased) | [`readiness-decision.json`](readiness-decision.json) | Signed binding of actual request and complete ordinary proof to current readiness evidence |
| Software-substrate consumption decision (unreleased) | [`software-substrate-decision.json`](software-substrate-decision.json) | Separately signed binding of complete ordinary proof, actual destination/class/request, local evidence, prerequisites and current epoch; not standalone permission |
| Emergency Policy | [`emergency-policy.json`](emergency-policy.json) | Exact emergency scope and protected change-control declarations; approval and activation require separate verification |
| Sensor Configuration v3 (unreleased) | [`sensor-config.json`](sensor-config.json) | A feed's identity, refresh and failure behavior; its dimension is one of the five weighted inputs or the veto |
| Legacy Sensor Configuration v2 | [`sensor-config-legacy-v2.json`](sensor-config-legacy-v2.json) | Byte-preserved published schema, whose dimension enum includes moment_criticality, for interpreting v2 configurations |
| Soul Constraint | [`soul-constraint.json`](soul-constraint.json) | The veto: present or absent, never a seventh weight |
| Transaction Record v3 (unreleased) | [`transaction-record.json`](transaction-record.json) | Trajectory Chain record, not Decision Geometry; complete canonical transition and staged JWS envelopes, with separate signature/head verification |
| Legacy Transaction Record v2 | [`transaction-record-legacy-v2.json`](transaction-record-legacy-v2.json) | Byte-preserved historical schema for archive interpretation; not a v3 authority acceptance path |
| Sponsorship Bond | [`sponsorship-bond.json`](sponsorship-bond.json) | What a guarantor stakes, and on whom |
| Adjudication Token (unreleased) | [`adjudication-token.json`](adjudication-token.json) | The normative rail's verdict on a declared gate, bound by digest to the action, actor, grant, evidence, zone and epoch it judged; favorable or not, nothing else |
| Human Eligibility Profile v1 (unreleased) | [`human-eligibility-profile.json`](human-eligibility-profile.json) | Exact operation criteria, permitted issuers, purpose-bearing scopes and governance/review/retention declarations; includes evidence/grant/delegation definitions |
| Human Eligibility Decision Body v1 (unreleased) | [`human-eligibility-decision.json`](human-eligibility-decision.json) | Unsigned prerequisite result bound to current identity, actual actor, request and active evidence; never an authorization token |
| Privacy Evidence Envelope v1 (unreleased) | [`privacy-evidence-envelope.json`](privacy-evidence-envelope.json) | Signed minimal storage envelope with AEAD-protected exact evidence bytes; outer integrity is distinct from original evidence verification |
| Privacy Erasure Receipt Body v1 (unreleased) | [`privacy-erasure-receipt.json`](privacy-erasure-receipt.json) | Unsigned bounded inventory/disposal accounting; actual erasure and authentication require independent deployed evidence |

## Usage

These schemas define the data structures used throughout the KTP implementation. They can be used for validation, code generation, and documentation purposes.
