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
| Deployment Profile | [`deployment-profile.json`](deployment-profile.json) | Every deployment-level declaration the series requires, in one object |
| Sensor Configuration | [`sensor-config.json`](sensor-config.json) | A feed's identity, refresh and failure behaviour |
| Soul Constraint | [`soul-constraint.json`](soul-constraint.json) | The veto: present or absent, never a seventh weight |
| Transaction Record | [`transaction-record.json`](transaction-record.json) | The audited record of a decision |
| Sponsorship Bond | [`sponsorship-bond.json`](sponsorship-bond.json) | What a guarantor stakes, and on whom |

## Usage

These schemas define the data structures used throughout the KTP implementation. They can be used for validation, code generation, and documentation purposes.
