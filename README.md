# Kinetic Trust Protocol (KTP) - RFC Series

**Status**: Draft Specification — NMCITRA  
**First published**: November 2025  
**Last updated**: July 2026

This repository contains draft specifications developed by the New Mexico
Cyber Intelligence & Threat Response Alliance (NMCITRA). These documents
have not been submitted to the IETF and do not represent Internet Standards
or consensus of any standards body.

> **Documentation site:** the full specifications render at
> <https://nmcitra.github.io/ktp-rfc/>. Each RFC below links to its
> summary page in `rfcs/`, which embeds the complete specification text
> from `rfcs-txt/`.

> **Citing KTP:** KTP is free to use, implement, and commercialize under
> Apache 2.0. When your work materially uses KTP's named constructs or
> architecture, please cite it — see [`CITATION.cff`](CITATION.cff) and
> [`PROVENANCE.md`](PROVENANCE.md).

> *"We cannot command Nature except by obeying her."* — Francis Bacon

## Overview

The Kinetic Trust Protocol (KTP) is a framework for dynamic, physics-based authorization of autonomous agents. It replaces static permission models with environmental constraints that adapt in real-time to system conditions.

**The Core Insight**: Instead of asking "Does this agent have permission?", KTP asks "Can this environment safely support this action?"

## The Problem

Traditional authorization systems suffer from three fatal assumptions:

1. **The Passport Fallacy**: Possession of a credential equals proof of identity
2. **The Static Fallacy**: Permissions verified at time T remain valid at T+1
3. **The Vacuum Fallacy**: Digital systems operate independent of physical reality

In the age of autonomous agents operating at machine-speed, all three assumptions fail catastrophically.

## The Solution: Digital Physics

KTP introduces a physics-based model where:

- **Trust is Mass**: Earned through survival, not assigned by fiat
- **Risk is Friction**: Environmental stress that constrains movement
- **Authorization is Motion**: The result of mass overcoming friction
- **Identity is Trajectory**: A vector of movement, not a static credential

## The Zeroth Law

The foundational constraint of all KTP systems:

```
A ≤ E

Where:
  A = Autonomy (intrinsic risk of the requested action)
  E = Environment stability (current Trust Score)
```

This is not a policy. It is a physical constraint enforced by cryptography.

## RFC Series

This repository contains 27 RFC documents plus the Constitution, comprising
the complete KTP specification. Each link points to the RFC's summary page in
`rfcs/`, which embeds the full specification text.

### Foundational Documents

| Document | Title | Lines | Description |
|----------|-------|-------|-------------|
| [Constitution](constitution.txt) | Constitution of Digital Physics | 781 | Preamble and 10 Articles defining the governing framework |
| [KTP-Core](rfcs/ktp-core.md) | Core Protocol | 1,761 | Trust Score, Context Tensor, Trust Proof, Silent Veto, Anti-Goodhart measures |

### Identity & Trust

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Identity](rfcs/ktp-identity.md) | Vector Identity | 1,472 | Trajectory Chains, Proof of Resilience, Sponsorship, NIST 800-63 Identity Proofing |
| [KTP-Tensors](rfcs/ktp-tensors.md) | Context Tensor Specification | 840 | The measurement framework: dimensions across the six domains |
| [KTP-Sensors](rfcs/ktp-sensors.md) | Context Tensor Sensors | 984 | Sensor specifications, Risk Domains, normalization, domain profiles |
| [KTP-Signal](rfcs/ktp-signal.md) | Signal Environment | 599 | Information-environment measurement, truth conditions, epistemic health |

### Enforcement & Audit

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Gravity](rfcs/ktp-gravity.md) | Digital Gravity | 774 | Gravity wells, constraint types, real-time enforcement, the physics of denial |
| [KTP-Enforce](rfcs/ktp-enforce.md) | Enforcement Layer | 1,234 | Policy Enforcement Points, Trust Tiers, Adaptive Dormancy, Mass Ceiling |
| [KTP-Audit](rfcs/ktp-audit.md) | Flight Recorder | 1,044 | Decision Geometry, immutable logging, forensics, counterfactual analysis |
| [KTP-Emergency](rfcs/ktp-emergency.md) | Emergency & Circuit Breakers | 1,110 | Emergency levels, circuit breakers, graceful degradation, zone collapse |

### Zones & Federation

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Zones](rfcs/ktp-zones.md) | Blue Zones & Trust Boundaries | 1,273 | Zone types (Deep Blue → Wild), discovery protocols, ingress/egress |
| [KTP-Federation](rfcs/ktp-federation.md) | Trust Federation | 1,124 | Inter-zone trust, cross-attestation, federation governance |
| [KTP-Oracle](rfcs/ktp-oracle.md) | Oracle Mesh | 1,000 | Trust Oracle mesh, consensus, threshold signatures, accountability |

### Technical Infrastructure

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Crypto](rfcs/ktp-crypto.md) | Cryptographic Specification | 1,538 | Algorithms, key management, HSM requirements, post-quantum strategy |
| [KTP-Transport](rfcs/ktp-transport.md) | Transport Layer | 1,423 | Wire formats, REST/gRPC APIs, real-time protocols, WebSocket streams |
| [KTP-Threat-Model](rfcs/ktp-threat-model.md) | Threat Model | 1,580 | STRIDE analysis, attack trees, risk assessment, security requirements |

### Operations & Recovery

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Recovery](rfcs/ktp-recovery.md) | Disaster Recovery & Resilience | 1,174 | Backup/restore, key ceremonies, zone recovery, split-brain resolution |
| [KTP-Migration](rfcs/ktp-migration.md) | Migration Guide | 1,216 | Adoption pathways, staged deployment |
| [KTP-Legacy](rfcs/ktp-legacy.md) | Legacy System Integration | 870 | OAuth 2.0 / OIDC / SAML / mTLS bridges, trust equivalence mapping |
| [KTP-Deprecation](rfcs/ktp-deprecation.md) | End-of-Life Specification | 785 | Deprecation timelines, trajectory preservation, knowledge transfer |

### Human & Governance

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Human](rfcs/ktp-human.md) | Human Integration | 1,305 | Humans as agents, collaboration patterns, system ethics |
| [KTP-Relational](rfcs/ktp-relational.md) | Relational Dynamics | 381 | The Va, indigenous relational concepts, relationship repair, ceremony |
| [KTP-Governance](rfcs/ktp-governance.md) | Specification Governance | 890 | Stewardship council, amendment process, anti-capture provisions |

### Privacy & Compliance

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Privacy](rfcs/ktp-privacy.md) | Privacy Framework | 2,255 | GDPR, CCPA, ICCPR Article 17, privacy-preserving computation, data minimization |
| [KTP-Provenance](rfcs/ktp-provenance.md) | Provenance & Knowledge Debt | 1,103 | Data provenance, consent status, indigenous data principles, capability lineage |
| [KTP-Conformance](rfcs/ktp-conformance.md) | Conformance Requirements | 1,228 | Certification levels, testing requirements, interoperability |

### Special Topics

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-Celestial](rfcs/ktp-celestial.md) | Celestial Wayfinding | 1,125 | Interplanetary trust, light-cone model, Polynesian navigation philosophy |
| [KTP-Problems](rfcs/ktp-problems.md) | Open Problems | 2,471 | Known limitations, anticipated critiques, honest assessment, call for collaboration |

### Summary Statistics

- **Total RFC Documents**: 27
- **Total Specification Lines**: ~33,000 (RFCs + Constitution)
- **JSON Schemas**: 4
- **Constitutional Articles**: 10

## Quick Start

### The Trust Equation

```
E_trust = E_base × (1 - R)

Where:
  E_base  = Agent's intrinsic capability (0-100)
  R       = Risk factor from Context Tensor (0-1)
  E_trust = What the environment allows (0-100)
```

### The Context Tensor

Seven dimensions of environmental reality:

| Dimension | Symbol | Analogy (informative) | Measures | Sensors |
|-----------|--------|-------------------|----------|---------|
| Mass | M | Density/Mass | Physical density | CO2, LIDAR, RF noise, device count |
| Momentum | P | Kinetic Energy | Data flow velocity | TPS, link saturation, packet velocity |
| Heat | H | Entropy/Temperature | Adversarial pressure | WAF blocks, anomaly rates, CPU temps |
| Time | T | Temporal Phase | Moment criticality | Event countdown, maintenance windows |
| Inertia | I | Inertial Mass | Blast radius | Topology centrality, dependency depth |
| Observer | O | Frame of Reference | Who is watching | VIP presence, regulatory jurisdiction |
| **Soul** | **S** | **Cosmological Constant** | **Sovereignty constraints** | **TK Labels, OCAP/CARE, Sacred Land geofences** |

**The Soul Veto**: Unlike the first six dimensions (which contribute weighted values to the Risk Factor), Soul acts as a **binary veto**. If sovereignty constraints are violated (S = 1), the action is forbidden regardless of Trust Score. This operationalizes Indigenous Data Sovereignty, cultural heritage protections, and other immutable constraints.

### Trust Tiers

| Tier | E_trust | Capabilities |
|------|---------|--------------|
| God Mode | ≥ 95 | Create, destroy, mutate infrastructure |
| Operator Mode | ≥ 85 | Restart services, read configs |
| Analyst Mode | ≥ 70 | Query data, read-only access |
| Observer Mode | ≥ 50 | Emit logs only |
| Hibernation | < 50 | Heartbeat only, await recovery |

### The Silent Veto

When A > E_trust, the action is denied automatically. No human intervention. No appeal. No exception.

This is not punishment. It is physics.

## Blue Zones

Blue Zones are network segments where Digital Physics is enforced—safe harbors on the internet where humans and agents can operate with cryptographic trust guarantees.

```
┌─────────────────────────────────────────────────────┐
│                     BLUE ZONE                       │
│  ┌───────────────────────────────────────────────┐  │
│  │           Trust Oracle Mesh                   │  │
│  │   [Oracle 1] ←→ [Oracle 2] ←→ [Oracle 3]      │  │
│  └───────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌───────────────────────────────────────────────┐  │
│  │         Context Tensor Sensors                │  │
│  │   [M] [P] [H] [T] [I] [O] [S]                 │  │
│  └───────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌───────────────────────────────────────────────┐  │
│  │      Policy Enforcement Points                │  │
│  │   [API GW] [Service Mesh] [IAM] [DB Proxy]    │  │
│  └───────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌───────────────────────────────────────────────┐  │
│  │          Agent Population                     │  │
│  │   [Tethered] [Divergent] [Persistent]         │  │
│  └───────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌───────────────────────────────────────────────┐  │
│  │           Flight Recorder                     │  │
│  │   [Immutable Audit Log - Decision Geometry]   │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                         ↕
                [ZONE GATEWAY]
                         ↕
┌─────────────────────────────────────────────────────┐
│                WILD INTERNET                        │
│     (Static credentials, binary permissions)        │
└─────────────────────────────────────────────────────┘
```

## Key Innovations

### 1. Vector Identity
Identity is a trajectory, not a credential. You are not what you hold; you are where you've been and how you moved.

### 2. Proof of Resilience
Trust is earned through survival under stress, not granted by authority. An agent that has weathered storms carries more weight than one with a pristine but untested history.

### 3. Sponsorship Model
New agents enter through sponsorship. A sponsor stakes their own trust, creating accountability without requiring pre-existing reputation.

### 4. Anti-Goodhart Measures
Comprehensive countermeasures against gaming the Trust Score, including multi-dimensional scoring, behavioral unpredictability, adversity requirements, and peer validation.

### 5. Indigenous Data Sovereignty
The Soul dimension operationalizes TK Labels, OCAP/CARE principles, and sacred land protections as immutable constraints that cannot be overridden by operational convenience.

### 6. Honest Uncertainty
KTP-PROBLEMS explicitly documents what we don't know how to solve, inviting collaboration rather than claiming false completeness.

## Repository Structure

```
ktp-rfc/
├── README.md                 # This file
├── NOTICE                    # Apache 2.0 attribution notice
├── CITATION.cff              # Machine-readable citation metadata
├── PROVENANCE.md             # Attribution & citation norms
├── LICENSE                   # Apache License 2.0
├── constitution.txt          # The Constitution of Digital Physics
├── glossary.md               # Term glossary
├── rfcs/                     # RFC summary pages (27 documents, Markdown)
│   ├── ktp-core.md           #   each summary embeds its full text from
│   ├── ktp-identity.md       #   rfcs-txt/ via a snippet include
│   └── ...                    #   (see the RFC Series table above)
├── rfcs-txt/                 # Full RFC specification text (27 documents)
│   ├── ktp-core.txt
│   ├── ktp-identity.txt
│   └── ...
├── docs/                     # MkDocs documentation site sources
│   └── schemas/              # JSON schemas
│       ├── trust-proof.json      # Trust Proof token schema
│       ├── context-tensor.json   # Context Tensor schema
│       ├── soul-constraint.json  # Soul constraint schema
│       └── sensor-config.json    # Sensor configuration schema
├── scripts/                  # Repo tooling (e.g. rfcs↔rfcs-txt sync check)
└── mkdocs.yml                # Documentation site configuration
```

The paired `rfcs/*.md` (summary) and `rfcs-txt/*.txt` (full text) files are
kept in sync by `scripts/check-rfc-sync.sh`, enforced on pull requests.

## Contributing

This specification is in active development. Contributions welcome:

1. **RFC Review**: Submit issues for clarifications or improvements
2. **Implementation**: Reference implementations in any language
3. **Sensor Profiles**: Domain-specific Context Tensor configurations
4. **Blue Zone Pilots**: Real-world deployment experiences
5. **Open Problems**: Solutions to challenges documented in KTP-PROBLEMS

### Priority Areas

- Reference implementation (Rust or Go recommended)
- Test vectors for conformance testing
- Formal verification of core properties
- Privacy-preserving computation integration
- Real-world sensor integration examples

## Philosophy

> *"Freedom is the recognition of necessity."* — Baruch Spinoza

KTP is built on the insight that true autonomy requires constraint. An agent is not free because it can do anything—it is free because it acts within the bounds of what the environment can safely support.

The wayfinders of Polynesia crossed the Pacific not by conquering the ocean but by learning to read it. They didn't fight the swells; they joined them. They became part of the system they navigated.

We are applying the same principle to code.

We are not building a prison for AI. We are building physics for the digital world.

## Authors

Chris Perkins  
New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)  
Email: cperkins@nmcitra.org

## License

This specification is released under the Apache License, Version 2.0.

## References

### Foundational Articles

1. "The Missing Law of Motion" — The Zeroth Law and Digital Physics
2. "The Ghost in the Machine" — The Data Compass and environmental sensing
3. "Sailing by Starlight" — Trust as mass, gravitational routing
4. "The Constitution of Digital Physics" — Ten immutable laws
5. "Proof of Physics" — Vector Identity and trajectory
6. "The Tether" — The Context Tensor and sensor aggregation

### Related Standards

- RFC 7519 — JSON Web Token (JWT)
- RFC 8693 — OAuth 2.0 Token Exchange
- RFC 9396 — OAuth 2.0 Rich Authorization Requests
- NIST SP 800-63 — Digital Identity Guidelines
- Local Contexts — Traditional Knowledge Labels
- OCAP® Principles — First Nations Information Governance
- CARE Principles — Indigenous Data Governance

### Academic Foundations

- Goodhart, C. (1984) — "Problems of Monetary Management"
- Spinoza, B. (1677) — "Ethics" (conatus)
- Bacon, F. (1620) — "Novum Organum"

---

*"We do not ask permission to implement gravity. We do not negotiate with entropy. We do not appeal to friction. We build the physics. The physics does the rest."*
