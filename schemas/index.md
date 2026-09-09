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
| Risk Factors | [`risk-factors.json`](risk-factors.json) | The six weighted inputs and the Soul veto, as one scored object |
| Trust Proof | [`trust-proof.json`](trust-proof.json) | The token an agent presents, and the claims it must carry |
| Deployment Profile v3 (unreleased) | [`deployment-profile.json`](deployment-profile.json) | Deployment declarations including the mandatory historical-evidence/current-readiness policy binding and explicit human-eligibility profile binding |
| Legacy Deployment Profile v2 | [`deployment-profile-legacy-v2.json`](deployment-profile-legacy-v2.json) | Byte-preserved published schema for interpreting old profiles; no readiness acceptance path |
| Readiness Profile v1 (unreleased) | [`readiness-profile.json`](readiness-profile.json) | Exact assessment criteria, scopes, authorized assessors and bounded evidence age |
| Readiness Attestation v1 (unreleased) | [`readiness-attestation.json`](readiness-attestation.json) | Complete signed assessment, subject configuration, scope, challenge and observations |
| Readiness Decision v1 (unreleased) | [`readiness-decision.json`](readiness-decision.json) | Signed binding of actual request and complete ordinary proof to current readiness evidence |
| Emergency Policy | [`emergency-policy.json`](emergency-policy.json) | Exact emergency scope and protected change-control declarations; approval and activation require separate verification |
| Sensor Configuration | [`sensor-config.json`](sensor-config.json) | A feed's identity, refresh and failure behaviour |
| Soul Constraint | [`soul-constraint.json`](soul-constraint.json) | The veto: present or absent, never a seventh weight |
| Transaction Record v3 (unreleased) | [`transaction-record.json`](transaction-record.json) | Complete canonical record and staged JWS envelopes; signatures and authenticated head evidence require separate verification |
| Legacy Transaction Record v2 | [`transaction-record-legacy-v2.json`](transaction-record-legacy-v2.json) | Byte-preserved historical schema for archive interpretation; not a v3 authority acceptance path |
| Sponsorship Bond | [`sponsorship-bond.json`](sponsorship-bond.json) | What a guarantor stakes, and on whom |
| Human Eligibility Profile v1 (unreleased) | [`human-eligibility-profile.json`](human-eligibility-profile.json) | Exact operation criteria, permitted issuers, purpose-bearing scopes and governance/review/retention declarations; includes evidence/grant/delegation definitions |
| Human Eligibility Decision Body v1 (unreleased) | [`human-eligibility-decision.json`](human-eligibility-decision.json) | Unsigned prerequisite result bound to current identity, actual actor, request and active evidence; never an authorization token |
| Privacy Evidence Envelope v1 (unreleased) | [`privacy-evidence-envelope.json`](privacy-evidence-envelope.json) | Signed minimal storage envelope with AEAD-protected exact evidence bytes; outer integrity is distinct from original evidence verification |
| Privacy Erasure Receipt Body v1 (unreleased) | [`privacy-erasure-receipt.json`](privacy-erasure-receipt.json) | Unsigned bounded inventory/disposal accounting; actual erasure and authentication require independent deployed evidence |

## Usage

These schemas define the data structures used throughout the KTP implementation. They can be used for validation, code generation, and documentation purposes.
