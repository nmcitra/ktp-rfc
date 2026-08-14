# Kinetic Trust Protocol (KTP) — RFC Series

**Version**: 2.0.0 *Gödel* · **Status**: Draft specification — NMCITRA  
**First published**: November 2025 · **This release**: 14 August 2026

Draft specifications developed by the New Mexico Cyber Intelligence & Threat
Response Alliance (NMCITRA). They have not been submitted to the IETF and do
not represent an Internet Standard or the consensus of any standards body.

## Read the specifications

The specifications live in [**`rfcs-md/`**](rfcs-md/), rendered by GitHub. Start
there — every document below is a link into that directory, readable in the
browser without cloning anything. It is generated from `rfc-src/`; edit the
source, never the render.

The same set renders as a documentation site at
<https://nmcitra.github.io/ktp-rfc/>; the schemas are published at
<https://kinetic-trust-protocol.net/specs/schemas/v2/>.

## What KTP specifies

Authorization derived from the environment rather than issued in advance. The
question is not *does this agent hold a permission* but *can these conditions
support this action right now* — and the answer is recomputed continuously
instead of being settled once at grant time.

Three assumptions in conventional authorization are what force the change:

1. **The passport fallacy** — possession of a credential is treated as proof
   of identity.
2. **The static fallacy** — a permission verified at time T is treated as
   valid at T+1.
3. **The vacuum fallacy** — the system is treated as independent of the
   conditions it runs in.

Agents acting at machine speed break all three.

### The Zeroth Law

```
A <= E

  A = Autonomy — the intrinsic risk of the requested action
  E = Environment — what current conditions can support
```

An agent's autonomy must never exceed the stability of the environment it acts
in. Every other requirement in the series is downstream of that constraint.

### The Trust Score

```
E_trust = E_base × (1 - R)

  E_base  = earned standing, 0–100
  R       = the risk aggregate, 0–1
  E_trust = what the environment currently allows, 0–100
```

`E_base` is what an agent has earned along its trajectory. `R` deflates it by
what the environment is doing. When `A > E_trust` the action is denied without
appeal — the Silent Veto. Denial is a consequence of the arithmetic, not a
judgment about the agent.

### Trust tiers

| Tier | `E_trust` | Capability |
|---|---|---|
| Admin Mode | ≥ 85 | Full infrastructure control |
| Operator Mode | ≥ 72 | Service management, configuration changes |
| Analyst Mode | ≥ 58 | Data query, read-only operations |
| Observer Mode | ≥ 22 | Logging, monitoring, heartbeat |
| Hibernation | < 22 | Heartbeat only, await recovery |

Admin Mode is offered only by zones whose ceiling can deliver it; a zone with a
lower ceiling cannot reach the tier at any generation.

## The measurement layer

Two separate things, deliberately kept apart.

**Context Signals** — the catalogue of what can be measured. 1,644 signals
across seven domains, canonical as JSON in [`catalog/`](catalog/):

| Domain | Signals | Domain | Signals |
|---|---:|---|---:|
| `world` | 369 | `relational` | 238 |
| `information` | 336 | `body` | 157 |
| `time` | 275 | `meta` | 17 |
| `soul` | 252 | **total** | **1,644** |

**Risk Factors** — the scoring layer that turns measurements into `R`. Six
weighted inputs, named by their JSON keys:

| Key | What it carries |
|---|---|
| `evidence_density` | Weight and density of presence in the environment |
| `trust_trend` | Rate and direction of change in standing |
| `adversarial_pressure` | Measured adversarial stress |
| `moment_criticality` | Criticality of the moment or phase — cutovers, deadlines, protected periods |
| `update_resistance` | How hard the trust value is to move: the depth of evidence behind current standing |
| `attestation_coverage` | How much of the agent's activity is witnessed and attestable |

Plus the **Soul veto** — `soul` is not a seventh weighted input. It is
evaluated before aggregation, and a violated sovereignty constraint forbids the
action regardless of `E_trust`. This is where Traditional Knowledge Labels,
OCAP® and CARE, and sacred-land constraints bind. Six weighted inputs and a
veto, never seven weights.

## The specifications

27 documents. Five are filed as Internet-Drafts and carry a generated `.txt`
in [`rfcs-txt/`](rfcs-txt/); the other 22 are Markdown only. Every link below
points into [`rfcs-md/`](rfcs-md/), the generated render.

### Foundation

| Specification | What it covers |
|---|---|
| [KTP-Core](rfcs-md/ktp-core.md) **·** *filed* | The Zeroth Law, Trust Score calculation, Trust Proof tokens, the Silent Veto, anti-Goodhart measures |
| [KTP-Identity](rfcs-md/ktp-identity.md) **·** *filed* | Vector Identity, trajectory chains, Proof of Resilience, sponsorship, NIST SP 800-63 proofing |
| [KTP-Problems](rfcs-md/ktp-problems.md) **·** *filed* | Known limits, anticipated critiques, what the series does not claim to solve |
| [`constitution.txt`](constitution.txt) | Preamble and ten articles, the governing frame the series answers to |

### Measurement

| Specification | What it covers |
|---|---|
| [KTP-Signals](rfcs-md/ktp-signals.md) | The Context Signals catalogue: what is measurable, and how a signal is specified |
| [KTP-Sensors](rfcs-md/ktp-sensors.md) | Sensor specifications, normalization, staleness, domain profiles |
| [KTP-Information](rfcs-md/ktp-information.md) | Information-environment measurement, truth conditions, epistemic health |

### Enforcement and audit

| Specification | What it covers |
|---|---|
| [KTP-Enforce](rfcs-md/ktp-enforce.md) **·** *filed* | Policy Enforcement Points, trust tiers, adaptive dormancy, ceilings |
| [KTP-Attenuation](rfcs-md/ktp-attenuation.md) | Capability attenuation: constraint types and real-time application |
| [KTP-Audit](rfcs-md/ktp-audit.md) | Flight Recorder, decision geometry, immutable logging, counterfactual analysis |
| [KTP-Emergency](rfcs-md/ktp-emergency.md) | Emergency levels, circuit breakers, graceful degradation, zone collapse |

### Zones and federation

| Specification | What it covers |
|---|---|
| [KTP-Zones](rfcs-md/ktp-zones.md) | Blue Zones, zone types from Deep Blue to Wild, discovery, ingress and egress |
| [KTP-Federation](rfcs-md/ktp-federation.md) | Inter-zone trust, cross-attestation, federation governance |
| [KTP-Oracle](rfcs-md/ktp-oracle.md) | Trust Oracle mesh, consensus, threshold signatures, accountability |

### Infrastructure

| Specification | What it covers |
|---|---|
| [KTP-Crypto](rfcs-md/ktp-crypto.md) | Algorithms, key management, HSM requirements, post-quantum strategy |
| [KTP-Transport](rfcs-md/ktp-transport.md) | Wire formats, REST and gRPC interfaces, streaming |
| [KTP-Threat-Model](rfcs-md/ktp-threat-model.md) | STRIDE analysis, attack trees, risk assessment, security requirements |
| [KTP-Conformance](rfcs-md/ktp-conformance.md) **·** *filed* | Conformance levels, testing requirements, interoperability |

### Operations

| Specification | What it covers |
|---|---|
| [KTP-Recovery](rfcs-md/ktp-recovery.md) | Backup and restore, key ceremonies, zone recovery, split-brain resolution |
| [KTP-Migration](rfcs-md/ktp-migration.md) | Adoption pathways and staged deployment |
| [KTP-Legacy](rfcs-md/ktp-legacy.md) | OAuth 2.0, OIDC, SAML and mTLS bridges; trust equivalence mapping |
| [KTP-Deprecation](rfcs-md/ktp-deprecation.md) | Deprecation timelines, trajectory preservation, knowledge transfer |

### People and governance

| Specification | What it covers |
|---|---|
| [KTP-Human](rfcs-md/ktp-human.md) | Humans as agents, collaboration patterns, system ethics |
| [KTP-Relational](rfcs-md/ktp-relational.md) | Relational dynamics, repair, ceremony |
| [KTP-Governance](rfcs-md/ktp-governance.md) | Stewardship council, amendment process, anti-capture provisions |

### Privacy and provenance

| Specification | What it covers |
|---|---|
| [KTP-Privacy](rfcs-md/ktp-privacy.md) | GDPR, CCPA, ICCPR Article 17, privacy-preserving computation, data minimization |
| [KTP-Provenance](rfcs-md/ktp-provenance.md) | Data provenance, consent status, Indigenous data principles, capability lineage |

### Special topics

| Specification | What it covers |
|---|---|
| [KTP-Celestial](rfcs-md/ktp-celestial.md) | Interplanetary trust under light-delay, and the wayfinding traditions it draws on |

## What v2.0.0 renamed

v2 renamed several constructs after what they are rather than what they
resembled. Implementations pinned to v1.0.1 keep working — a published tag is
never moved — but v2 text uses these names only.

| v1 | v2.0.0 | Where it bites |
|---|---|---|
| `tethered` | `sponsored` | Lineage enum, agent identifier strings, protobuf member names |
| `divergent` | `independent` | Same |
| `persistent` | `guarantor` | Same |
| God Mode *(retired)* | **Admin Mode** | `TRUST_TIER_ADMIN`, OpenAPI `admin` |
| Single-letter input symbols | The JSON key **is** the name | `risk_factors`, six named keys, `soul` as veto |

[`MIGRATION.md`](MIGRATION.md) sorts every change into wire-format breaks,
behavior breaks, and prose changes. [`CHANGELOG.md`](CHANGELOG.md) records what
forced each one, and [`RELEASE-NOTES-v2.0.0.md`](RELEASE-NOTES-v2.0.0.md) is
the release narrative.

## Schemas

Seven JSON Schemas in [`schemas/`](schemas/), published under
`https://kinetic-trust-protocol.net/specs/schemas/v2/`, which is the `$id` of
each file:

`trust-proof` · `risk-factors` · `soul-constraint` · `sensor-config` ·
`sponsorship-bond` · `transaction-record` · `deployment-profile`

## Repository map

| Path | What it is |
|---|---|
| [`rfcs-md/`](rfcs-md/) | The 27 specifications as clean Markdown — the reading surface, and the GitHub Pages source. **Generated** from `rfc-src/` by `scripts/gen-rfcs-md.py` — never hand-edited. Replaces a hand-authored `rfcs/` retired 2026-08-14: it drifted (missing an entire section) with no gate able to see the omission — two independently-maintained representations is the drift class this release exists to kill, and it should not survive here either |
| [`rfc-src/`](rfc-src/) | kramdown-rfc source for all 27; authored here, and the only place a specification is edited |
| [`rfcs-txt/`](rfcs-txt/) | The five filed Internet-Drafts. **Generated** from `rfc-src/` by `scripts/gen-rfc-txt.sh` — never hand-edited |
| [`catalog/`](catalog/) | The Context Signals catalogue: seven domain files plus the index, canonical as JSON, Markdown tables generated |
| [`schemas/`](schemas/) | The seven JSON Schemas. A wire artifact, so it sits at the root rather than inside site content |
| [`specifications/`](specifications/) | The two normative documents that are not RFCs — the Kinetic Envelope and the deployment profile — and in `conformance/`, the reference vectors they are conformed against |
| [`docs/`](docs/) | Documentation-site content, and nothing else |
| [`scripts/`](scripts/) | The gates — vocabulary, summary/source parity, repo hygiene, declarations, and the generate-and-diff check for the filed set |
| [`CHANGELOG.md`](CHANGELOG.md) | Every normative change and what forced it |
| [`MIGRATION.md`](MIGRATION.md) | What a v1.0.1 implementation has to do |
| [`RELEASE-NOTES-v2.0.0.md`](RELEASE-NOTES-v2.0.0.md) | The v2.0.0 release notes |
| [`SECURITY-NOTES.md`](SECURITY-NOTES.md) | Errata for published tags, recorded when found rather than held for the next release |
| [`VERSIONING.md`](VERSIONING.md) | How the series versions as a set, and why tags are never moved |
| [`CITATION.cff`](CITATION.cff) · [`PROVENANCE.md`](PROVENANCE.md) | Citation metadata and attribution norms |
| [`glossary.md`](glossary.md) · [`constitution.txt`](constitution.txt) | Term glossary; the governing frame |

The gates run on pull requests. They are executable rather than aspirational:
if a check cannot fail, it is not a criterion.

## Versioning

The series versions **as a set**, so an implementation names one version and
knows which text every specification refers to. Tags are bare and numeric
(`v2.0.0`); descriptive names live in the release title, never in the tag.
Published tags are never moved. See [`VERSIONING.md`](VERSIONING.md).

## Citing

KTP is free to use, implement, modify, and commercialize under Apache 2.0.
When your work materially uses or discusses KTP's named constructs, equations,
or distinctive architecture, please cite it — see
[`CITATION.cff`](CITATION.cff) and [`PROVENANCE.md`](PROVENANCE.md).

`CITATION.cff` carries no `identifiers:` block yet. The archive deposit is part
of what a release is, and the identifier is added there when the deposit for
that version exists — never guessed ahead of it.

## Contributing

Issues, pull requests, and discussion all go through
[github.com/nmcitra/ktp-rfc](https://github.com/nmcitra/ktp-rfc); see
[`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

Specifications are edited in [`rfc-src/`](rfc-src/), never in `rfcs-txt/` or `rfcs-md/` — both are generated.
Where the work is most useful right now:

- A reference implementation.
- Test vectors for conformance testing.
- Formal verification of the core properties.
- Domain profiles for the Context Signals catalogue.
- Deployment experience from real zones.
- Answers to anything in [KTP-Problems](rfcs-md/ktp-problems.md).

## Related standards and sources

- RFC 7519 — JSON Web Token (JWT)
- RFC 8693 — OAuth 2.0 Token Exchange
- RFC 9396 — OAuth 2.0 Rich Authorization Requests
- NIST SP 800-63 — Digital Identity Guidelines
- Local Contexts — Traditional Knowledge Labels
- OCAP® Principles — First Nations Information Governance Centre
- CARE Principles for Indigenous Data Governance

## Authors and license

Chris Perkins, New Mexico Cyber Intelligence & Threat Response Alliance
(NMCITRA) — <cperkins@nmcitra.org>

Released under the Apache License, Version 2.0. See [`LICENSE`](LICENSE) and
the attribution notice in [`NOTICE`](NOTICE).
