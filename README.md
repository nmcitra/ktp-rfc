# Kinetic Trust Protocol (KTP) - RFC Series

**Status**: Draft Specification - NMCITRA  
**Version**: 0.1  
**Date**: November 2025

This repository contains draft specifications developed by the New Mexico
Cyber Intelligence & Threat Response Alliance (NMCITRA). These documents
have not been submitted to the IETF and do not represent Internet Standards
or consensus of any standards body.

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

This repository contains 19 RFC documents comprising the complete KTP specification:

### Foundational Documents

| Document | Title | Lines | Description |
|----------|-------|-------|-------------|
| [Constitution](constitution.txt) | Constitution of Digital Physics | 693 | Preamble and 10 Articles defining the governing framework |
| [KTP-CORE](rfcs/ktp-core.txt) | Core Protocol | 2,038 | Trust Score, Context Tensor, Trust Proof, Silent Veto, Anti-Goodhart measures |

### Identity & Trust

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-IDENTITY](rfcs/ktp-identity.txt) | Vector Identity | 1,512 | Trajectory Chains, Proof of Resilience, Sponsorship, NIST 800-63 Identity Proofing |
| [KTP-SENSORS](rfcs/ktp-sensors.txt) | Context Tensor Sensors | 1,050 | Sensor specifications, Risk Domains (Node/Neighborhood/Global), normalization, domain profiles |

### Enforcement & Audit

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-ENFORCE](rfcs/ktp-enforce.txt) | Enforcement Layer | 1,186 | Policy Enforcement Points, Trust Tiers, Adaptive Dormancy, Mass Ceiling |
| [KTP-AUDIT](rfcs/ktp-audit.txt) | Flight Recorder | 876 | Decision Geometry, immutable logging, forensics, counterfactual analysis |

### Zones & Federation

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-ZONES](rfcs/ktp-zones.txt) | Blue Zone Discovery | 1,176 | Zone types (Deep Blue → Wild), discovery protocols, ingress/egress |
| [KTP-FEDERATION](rfcs/ktp-federation.txt) | Trust Federation | 904 | Inter-zone trust, cross-attestation, federation governance |

### Technical Infrastructure

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-CRYPTO](rfcs/ktp-crypto.txt) | Cryptographic Specification | 1,456 | Algorithms, key management, HSM requirements, post-quantum strategy |
| [KTP-TRANSPORT](rfcs/ktp-transport.txt) | Transport Layer | 1,398 | Wire formats, REST/gRPC APIs, real-time protocols, WebSocket streams |
| [KTP-THREAT-MODEL](rfcs/ktp-threat-model.txt) | Threat Model | 1,756 | STRIDE analysis, attack trees, risk assessment, security requirements |

### Operations & Recovery

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-RECOVERY](rfcs/ktp-recovery.txt) | Disaster Recovery | 932 | Backup/restore, key ceremonies, zone recovery, split-brain resolution |
| [KTP-MIGRATION](rfcs/ktp-migration.txt) | Migration Guide | 1,042 | Adoption pathways, legacy integration, staged deployment |

### Human & Governance

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-HUMAN](rfcs/ktp-human.txt) | Human Integration | 1,178 | Humans as agents, collaboration patterns, system ethics |
| [KTP-GOVERNANCE](rfcs/ktp-governance.txt) | Specification Governance | 654 | Stewardship council, amendment process, anti-capture provisions |

### Privacy & Compliance

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-PRIVACY](rfcs/ktp-privacy.txt) | Privacy Framework | 2,382 | GDPR, CCPA, ICCPR Article 17, privacy-preserving computation, data minimization |
| [KTP-CONFORMANCE](rfcs/ktp-conformance.txt) | Conformance Requirements | 906 | Certification levels, testing requirements, interoperability |

### Special Topics

| RFC | Title | Lines | Description |
|-----|-------|-------|-------------|
| [KTP-CELESTIAL](rfcs/ktp-celestial.txt) | Celestial Wayfinding | 1,153 | Interplanetary trust, light-cone model, Polynesian navigation philosophy |
| [KTP-PROBLEMS](rfcs/ktp-problems.txt) | Open Problems | 2,448 | Known limitations, anticipated critiques, honest assessment, call for collaboration |

### Summary Statistics

- **Total RFC Documents**: 19
- **Total Specification Lines**: ~24,000
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

| Dimension | Symbol | Physics Equivalent | Measures | Sensors |
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
├── GAP-ANALYSIS.md           # Development roadmap and gaps
├── constitution.txt          # The Constitution of Digital Physics
├── rfcs/                     # RFC specifications (19 documents)
│   ├── ktp-core.txt          # Core protocol specification
│   ├── ktp-identity.txt      # Vector identity and trajectory
│   ├── ktp-sensors.txt       # Context Tensor sensors
│   ├── ktp-enforce.txt       # Enforcement layer
│   ├── ktp-audit.txt         # Flight Recorder
│   ├── ktp-zones.txt         # Blue Zone discovery
│   ├── ktp-federation.txt    # Trust federation
│   ├── ktp-crypto.txt        # Cryptographic specification
│   ├── ktp-transport.txt     # Transport layer
│   ├── ktp-threat-model.txt  # Security threat model
│   ├── ktp-recovery.txt      # Disaster recovery
│   ├── ktp-migration.txt     # Migration guide
│   ├── ktp-human.txt         # Human integration
│   ├── ktp-governance.txt    # Specification governance
│   ├── ktp-privacy.txt       # Privacy framework
│   ├── ktp-conformance.txt   # Conformance requirements
│   ├── ktp-celestial.txt     # Interplanetary trust
│   └── ktp-problems.txt      # Open problems and limitations
└── schemas/                  # JSON schemas
    ├── trust-proof.json      # Trust Proof token schema
    ├── context-tensor.json   # Context Tensor schema
    ├── soul-constraint.json  # Soul constraint schema
    └── sensor-config.json    # Sensor configuration schema
```

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
