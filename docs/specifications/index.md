# Specifications

*The complete technical blueprint for the Kinetic Trust Protocol*

---

The KTP specification suite defines every aspect of the protocol—from cryptographic primitives to governance mechanisms. These documents are the authoritative reference for implementers, auditors, and researchers.

!!! info "Where the specifications live"
    Every normative artifact is in the repository, outside this documentation site: the RFC set in `rfcs/`, the two standalone normative documents in `specifications/`, the wire schemas in `schemas/`. This site describes them and links to them. Where the two disagree, the repository is right.

<div class="grid cards" markdown>

-   :material-github:{ .lg .middle } **RFCs on GitHub**

    ---

    27 Request for Comments documents covering every protocol component. Browse the source.

    [:octicons-arrow-right-24: Browse RFCs](https://github.com/nmcitra/ktp-rfc/tree/main/rfcs-txt){ target="_blank" }

-   :material-robot-industrial:{ .lg .middle } **Kinetic Envelope**

    ---

    A ≤ E evaluated per action against the kinematics of the request: graduated deautomation, the kinematic veto, and a seven-vector conformance suite.

    [:octicons-arrow-right-24: Read the spec](https://github.com/nmcitra/ktp-rfc/blob/main/specifications/kinetic-envelope.md)

-   :material-clipboard-check:{ .lg .middle } **Deployment Profile**

    ---

    The declaration surface: one object carrying every declaration the series requires of a deployment — the Risk Factor bridge, feed mapping, aliases, normalization, and the declared parameters.

    [:octicons-arrow-right-24: Read the spec](https://github.com/nmcitra/ktp-rfc/blob/main/specifications/deployment-profile.md)

-   :material-code-json:{ .lg .middle } **Schemas**

    ---

    The seven wire schemas — Risk Factors, Trust Proof, deployment profile, and the rest — with their absolute `$id` URLs.

    [:octicons-arrow-right-24: View Schemas](https://github.com/nmcitra/ktp-rfc/tree/main/schemas)

-   :material-shield-check:{ .lg .middle } **Blue Zones**

    ---

    A pointer to KTP-Zones: the zone gradient, what an operator guarantees, and how trust crosses a border.

    [:octicons-arrow-right-24: Blue Zones](blue-zones.md)

-   :material-fingerprint:{ .lg .middle } **Identity**

    ---

    A pointer to KTP-Identity: identity as a trajectory, the proof carried for it, attestation and revocation.

    [:octicons-arrow-right-24: Identity](identity.md)

</div>

---

## Choose Your Path

Different readers need different entry points. Select the journey that matches your goals:

!!! abstract "🏗️ Implementer's Path"
    Building a KTP-compliant system? Follow this sequence:
    
    **Foundation** → **Identity** → **Environment** → **Compliance**
    
    1. [KTP-Core](../rfcs/ktp-core.md) → [KTP-Crypto](../rfcs/ktp-crypto.md) → [KTP-Transport](../rfcs/ktp-transport.md)
    2. [KTP-Identity](../rfcs/ktp-identity.md) → [KTP-Signals](../rfcs/ktp-signals.md)
    3. [KTP-Zones](../rfcs/ktp-zones.md) → [KTP-Federation](../rfcs/ktp-federation.md)
    4. [KTP-Conformance](../rfcs/ktp-conformance.md) → [KTP-Audit](../rfcs/ktp-audit.md)

!!! info "🔍 Auditor's Path"
    Validating a KTP implementation? Focus on these areas:
    
    **Compliance** → **Security** → **Governance**
    
    1. [KTP-Conformance](../rfcs/ktp-conformance.md) → [KTP-Audit](../rfcs/ktp-audit.md)
    2. [KTP-Threat-Model](../rfcs/ktp-threat-model.md) → [KTP-Crypto](../rfcs/ktp-crypto.md)
    3. [KTP-Governance](../rfcs/ktp-governance.md) → [KTP-Human](../rfcs/ktp-human.md)

!!! tip "🎓 Researcher's Path"
    Understanding the theory behind KTP? Explore:
    
    **Philosophy** → **Mechanics** → **Innovation**
    
    1. [KTP-Core](../rfcs/ktp-core.md) (Sections 1-4) → [Constitution](../learn/constitution.md)
    2. [KTP-Signals](../rfcs/ktp-signals.md) → [KTP-Attenuation](../rfcs/ktp-attenuation.md) → [KTP-Information](../rfcs/ktp-information.md)
    3. [KTP-Oracle](../rfcs/ktp-oracle.md) → [KTP-Celestial](../rfcs/ktp-celestial.md)

---

## Specifications by Domain

=== ":material-axis-arrow: Foundation"

    The bedrock protocols that define KTP's core architecture.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Core](../rfcs/ktp-core.md) | :material-check-circle:{ .stable } Stable | The Zeroth Law, Trust Scores, A ≤ E constraint |
    | [KTP-Crypto](../rfcs/ktp-crypto.md) | :material-check-circle:{ .stable } Stable | Cryptographic primitives and algorithms |
    | [KTP-Transport](../rfcs/ktp-transport.md) | :material-check-circle:{ .stable } Stable | Network transport and messaging protocols |
    | [KTP-Identity](../rfcs/ktp-identity.md) | :material-check-circle:{ .stable } Stable | Vector Identity and trajectory-based authentication |
    
    !!! note "Start Here"
        If you're new to the specifications, begin with **KTP-Core**. It establishes the foundational concepts that all other RFCs build upon.

=== ":material-scale-balance: Trust Mechanics"

    How trust is measured, computed, and flows through the system.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Signals](../rfcs/ktp-signals.md) | :material-check-circle:{ .stable } Stable | Context Signals specification (1,644 signals) |
    | [KTP-Attenuation](../rfcs/ktp-attenuation.md) | :material-progress-clock:{ .draft } Draft | Digital Gravity enforcement mechanisms |
    | [KTP-Information](../rfcs/ktp-information.md) | :material-progress-clock:{ .draft } Draft | Trust signal propagation and analysis |
    | [KTP-Relational](../rfcs/ktp-relational.md) | :material-progress-clock:{ .draft } Draft | Agent-to-agent trust relationships |
    | [KTP-Oracle](../rfcs/ktp-oracle.md) | :material-flask:{ .experimental } Experimental | Trust oracles and external attestation |
    
    ??? info "Understanding Trust Flow"
        Trust in KTP flows through a measurement → computation → enforcement pipeline:
        
        - **Signals** capture the 1,644-signal environmental state
        - **Signal** propagates trust changes through the network
        - **Gravity** enforces constraints as agents approach limits
        - **Relational** tracks inter-agent trust dynamics

=== ":material-shield-home: Environment"

    Where agents operate and how trust boundaries are established.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Zones](../rfcs/ktp-zones.md) | :material-progress-clock:{ .draft } Draft | Blue Zone architecture and governance |
    | [KTP-Federation](../rfcs/ktp-federation.md) | :material-progress-clock:{ .draft } Draft | Cross-domain trust federation |
    | [KTP-Sensors](../rfcs/ktp-sensors.md) | :material-progress-clock:{ .draft } Draft | Environmental sensor requirements |
    | [KTP-Celestial](../rfcs/ktp-celestial.md) | :material-flask:{ .experimental } Experimental | Universal time and coordination |
    
    ??? info "The Zone Gradient"
        Environments range from maximum constraint to no enforcement:
        
        - **Deep Blue**: Maximum constraint, cryptographic guarantees
        - **Blue**: High constraint, monitored operations
        - **Cyan**: Moderate constraint, verified agents
        - **Green**: Light constraint, basic verification
        - **Wild**: No KTP enforcement

=== ":material-gavel: Governance"

    Rules, oversight, and compliance mechanisms.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Governance](../rfcs/ktp-governance.md) | :material-progress-clock:{ .draft } Draft | Protocol governance and amendment |
    | [KTP-Human](../rfcs/ktp-human.md) | :material-check-circle:{ .stable } Stable | Human oversight requirements |
    | [KTP-Enforce](../rfcs/ktp-enforce.md) | :material-progress-clock:{ .draft } Draft | Enforcement mechanisms |
    | [KTP-Conformance](../rfcs/ktp-conformance.md) | :material-check-circle:{ .stable } Stable | Conformance testing requirements |
    | [KTP-Audit](../rfcs/ktp-audit.md) | :material-check-circle:{ .stable } Stable | Audit trail and non-repudiation |
    
    ??? info "Governance Hierarchy"
        KTP governance follows a clear hierarchy:
        
        1. **Constitution** — Immutable foundational law
        2. **Core RFCs** — Stable specifications requiring deprecation process
        3. **Extended RFCs** — Evolving specifications under active development
        4. **Implementation Guidance** — Non-normative best practices

=== ":material-refresh-circle: Lifecycle"

    Evolution, resilience, and system maintenance.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Migration](../rfcs/ktp-migration.md) | :material-progress-clock:{ .draft } Draft | Version migration protocols |
    | [KTP-Recovery](../rfcs/ktp-recovery.md) | :material-progress-clock:{ .draft } Draft | Trust recovery after incidents |
    | [KTP-Emergency](../rfcs/ktp-emergency.md) | :material-progress-clock:{ .draft } Draft | Emergency response procedures |
    | [KTP-Deprecation](../rfcs/ktp-deprecation.md) | :material-check-circle:{ .stable } Stable | Deprecation and sunset process |
    | [KTP-Legacy](../rfcs/ktp-legacy.md) | :material-progress-clock:{ .draft } Draft | Legacy system integration |
    | [KTP-Provenance](../rfcs/ktp-provenance.md) | :material-progress-clock:{ .draft } Draft | Model and data provenance tracking |
    
    ??? info "Lifecycle Principles"
        KTP systems must plan for change:
        
        - **Migration**: Smooth transitions between protocol versions
        - **Recovery**: Rebuilding trust after compromise
        - **Emergency**: Rapid response to active threats
        - **Deprecation**: Graceful retirement of old features

=== ":material-alert-circle: Security"

    Threat modeling and security analysis.
    
    | Specification | Status | Description |
    |--------------|--------|-------------|
    | [KTP-Threat-Model](../rfcs/ktp-threat-model.md) | :material-check-circle:{ .stable } Stable | Comprehensive threat analysis |
    | [KTP-Problems](../rfcs/ktp-problems.md) | :material-progress-clock:{ .draft } Draft | Known issues and mitigations |
    | [KTP-Privacy](../rfcs/ktp-privacy.md) | :material-progress-clock:{ .draft } Draft | Privacy-preserving computations |
    
    ??? warning "Security Considerations"
        Every KTP implementation must address:
        
        - **Gaming**: Agents attempting to inflate trust scores
        - **Collusion**: Coordinated attacks across agent networks
        - **Sybil**: Fake identity proliferation
        - **Oracle Manipulation**: Corrupting external trust sources

---

## Specification Status Guide

| Status | Icon | Meaning |
|--------|------|---------|
| **Stable** | :material-check-circle:{ .stable } | Production-ready. Breaking changes require formal deprecation process. |
| **Draft** | :material-progress-clock:{ .draft } | Under active development. May change significantly before stabilization. |
| **Experimental** | :material-flask:{ .experimental } | Research stage. Not recommended for production use. |

---

---

## Risk Factors Schema

The Risk Factors object — formerly the Context Tensor; renamed `risk-factors.json` by the v2 schema rewrite — carries the six weighted inputs to the risk aggregate `R`. Six keys, each a number in `[0, 1]`, all required, no others accepted:

| Key | What it measures |
|-----|------------------|
| `evidence_density` | Weight and density of presence in the environment |
| `trust_trend` | Rate of change of standing, and its direction |
| `adversarial_pressure` | Measured adversarial stress on the environment |
| `moment_criticality` | Criticality of the current moment or operational phase |
| `update_resistance` | How hard the trust value is to move — the depth of the evidence base behind current standing |
| `attestation_coverage` | How much of the agent's activity is witnessed and attestable |

The Soul veto is evaluated before aggregation and is not a term in it — six plus a veto, never seven. It has its own schema, [`soul-constraint.json`](https://github.com/nmcitra/ktp-rfc/blob/main/schemas/soul-constraint.json).

For the full JSON schema definition, see [risk-factors.json](https://github.com/nmcitra/ktp-rfc/blob/main/schemas/risk-factors.json).

## Quick Reference

!!! quote "Most Referenced"
    [KTP-Core](../rfcs/ktp-core.md) · [KTP-Identity](../rfcs/ktp-identity.md) · [KTP-Zones](../rfcs/ktp-zones.md) · [KTP-Signals](../rfcs/ktp-signals.md)

!!! example "Complete RFC Index"
    For a flat listing of all specifications, visit the [GitHub RFC directory](https://github.com/nmcitra/ktp-rfc/tree/main/rfcs){ target="_blank" }.

---

## Where to Go Next

<div class="grid cards" markdown>

-   :material-shield-home:{ .lg .middle } **Deep Dive: Blue Zones**

    ---

    Understand the architecture of trust environments in detail.

    [:octicons-arrow-right-24: Blue Zones](blue-zones.md)

-   :material-code-json:{ .lg .middle } **Data Structures**

    ---

    Explore the JSON schemas that define KTP's core data formats.

    [:octicons-arrow-right-24: Schemas](https://github.com/nmcitra/ktp-rfc/tree/main/schemas)

-   :material-book-open-variant:{ .lg .middle } **Back to Basics**

    ---

    Need a conceptual refresher before diving into specs?

    [:octicons-arrow-right-24: Core Concepts](../learn/core-concepts.md)

-   :material-hammer-wrench:{ .lg .middle } **Start Building**

    ---

    Ready to implement? Get the developer guide.

    [:octicons-arrow-right-24: Developer Guide](../implement/developer-guide.md)

</div>
